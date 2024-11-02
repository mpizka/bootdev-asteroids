import pygame

from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    """The main function"""
    # init pygame
    pygame.init()

    # create GUI window as `screen` object
    # A running pygame application has a single `display` instance.
    # `set_mode` creates and returns a `Surface` (a pixel display you can draw on)
    # The surface has to be "flipped" onto the screen to become visible
    # https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # A `pygame.time.Clock` is a time-tracking object
    clock = pygame.time.Clock()
    # delta time
    dt = 0

    # groups for updating and drawing
    drawable = pygame.sprite.Group()
    updateable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # NOTE: extremely unhappy with this, see my notes in `circleshape.py`
    Player.containers = (drawable, updateable)  # type: ignore
    Asteroid.containers = (asteroids, updateable, drawable)  # type: ignore
    AsteroidField.containers = (updateable,)  # type: ignore
    Shot.containers = (shots, updateable, drawable)  # type: ignore

    # instanciate player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # game loop
    while 1:

        # get and process events
        # this needs to happen regularly, as pygame communicates with the underlying
        # system through an event loop, which has a maximum number of events
        # it can hold.
        for event in pygame.event.get():
            # the `QUIT` event is emitted e.g. by pressing [X] in the window
            if event.type == pygame.QUIT:
                return
            # we quit the game if the user presses Q or ESC
            # all keys are implemented as pygame constants
            # which are listed here:
            # https://www.pygame.org/docs/ref/key.html
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_q,
                pygame.K_ESCAPE,
            ]:
                return

        # `fill` draws rectangles of color on a surface
        # The color can be a pygame color or an RGB sequence
        # https://www.pygame.org/docs/ref/surface.html#pygame.Surface.fill
        screen.fill(pygame.Color(0, 0, 0))

        # update and draw
        # NOTE: This is not how you would usually do this in pygame. Normally
        # you call the groups update and draw methods. however, in the case of
        # this project, our `draw` methods work slightly different from drawing in
        # most pygame games:
        # https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group.draw
        for u in updateable:
            u.update(dt)
        for a in asteroids:
            if a.collides_with(player):
                print("Game over!")
                return
        for a in asteroids:
            for s in shots:
                if a.collides_with(s):
                    a.split()
                    s.kill()
                    break
        for d in drawable:
            d.draw(screen)

        # Draw the surface to the actual display
        # https://www.pygame.org/docs/ref/display.html#pygame.display.flip
        pygame.display.flip()

        # limit the framerate to a maximum of 60FPS
        # this also returns the delta-time that has passed since the last
        # time Clock.tick() has been called
        # The argument to `tick` is the intended framerate in FPS
        dt_milliseconds = clock.tick(60)
        dt = dt_milliseconds / 1000


if __name__ == "__main__":
    main()
