import pygame

from constants import *


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

    # game loop
    while 1:

        # get and process events
        for event in pygame.event.get():
            # the `QUIT` event is emitted e.g. by pressing [X] in the window
            if event.type == pygame.QUIT:
                return

        # `fill` draws rectangles of color on a surface
        # The color can be a pygame color or an RGB sequence
        # https://www.pygame.org/docs/ref/surface.html#pygame.Surface.fill
        screen.fill(pygame.Color(0, 0, 0))

        # Draw the surface to the actual display
        # https://www.pygame.org/docs/ref/display.html#pygame.display.flip
        pygame.display.flip()


if __name__ == "__main__":
    main()
