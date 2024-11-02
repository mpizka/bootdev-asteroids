import pygame

from constants import *
from player import Player
from asteroid import Asteroid
from shot import Shot
from score import draw_scoreboard


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
    # load background image
    bkgrd = pygame.image.load("assets/bkgrd.jpg")

    # A `pygame.time.Clock` is a time-tracking object
    clock = pygame.time.Clock()
    # delta time
    dt = 0

    # groups for updating and drawing
    drawable = pygame.sprite.Group()
    updateable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set default groups for classes
    Player.set_default_groups(drawable, updateable)
    Asteroid.set_default_groups(asteroids, updateable, drawable)
    Shot.set_default_groups(shots, updateable, drawable)

    # asteroid spawn cooldown
    asteroid_cooldown = 0

    # score tracker
    score_font = pygame.font.Font(size=12)  # type: ignore
    score = 0

    # instanciate player
    player = Player(pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

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

        screen.blit(bkgrd, (0, 0))

        # update and draw
        # NOTE: This is not how you would usually do this in pygame. Normally
        # you call the groups update and draw methods. however, in the case of
        # this project, our `draw` methods work slightly different from drawing in
        # most pygame games:
        # https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group.draw

        # spawn asteroids
        asteroid_cooldown -= dt
        if asteroid_cooldown <= 0:
            Asteroid.spawn()
            asteroid_cooldown = ASTEROID_SPAWN_COOLDOWN

        # run updates and remove out-of-screen objects
        for u in updateable:
            if (
                u.position.x > SCREEN_WIDTH
                or u.position.x < 0
                or u.position.y > SCREEN_HEIGHT
                or u.position.y < 0
            ):
                if u is player:
                    print(f"Game over! {score=}")
                    return
                u.kill()
                continue
            u.update(dt)

        # determine if asteroids hit player
        for a in asteroids:
            if a.collides_with(player):
                print(f"Game over! {score=}")
                return

        # determine if shots hit asteroids
        for a in asteroids:
            for s in shots:
                if a.collides_with(s):
                    a.split()
                    s.kill()
                    score += 1
                    break

        # draw sprites
        for d in drawable:
            d.draw(screen)

        # draw scoreboard
        draw_scoreboard(score, screen)

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
