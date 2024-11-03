import pygame

import assets
from constants import *
from player import Player
from asteroid import Asteroid
from shot import Shot
from score import draw_scoreboard
from explosion import Explosion
import state


def main():
    """The main function"""
    # init pygame
    pygame.init()

    # load assets
    assets.load()

    # create GUI window as `screen` object
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # A `pygame.time.Clock` is a time-tracking object
    clock = pygame.time.Clock()
    # delta time
    dt = 0

    # cross-state value dictionary
    game_vals = {}

    current_state = state.Endless(screen, game_vals)

    # game loop
    while 1:

        current_state = current_state.step(dt)
        if isinstance(current_state, state.Quit):
            return

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
