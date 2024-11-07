import pygame
from pygame import Surface
from pygame.font import Font, SysFont

from assets import FONT_ASSETS
from constants import *


def draw_bottom_right(screen: Surface, line: str):
    """Draw a line to the bottom right"""
    font = FONT_ASSETS["monogram.ttf"]

    scoreboard, _ = font.render(
        line,
        fgcolor=SCORE_COLOR,
        size=SCORE_SIZE,
    )
    screen.blit(
        source=scoreboard,
        dest=(
            SCREEN_WIDTH - scoreboard.get_width(),
            SCREEN_HEIGHT - scoreboard.get_height(),
        ),
    )


def draw_lines_mid(screen: Surface, lines: list[str], y_start=None):
    """Write lines in the middle of the screen, centered along X and Y axis

    If y_start is set, it becomes the vertical starting point instead.
    """
    font = FONT_ASSETS["monogram.ttf"]

    # height of a line
    h = font.get_sized_height(MENU_SIZE)
    # total height of text
    total_h = h * len(lines) + MENU_SPACING * (len(lines) - 1)

    if y_start is None:
        y_start = SCREEN_HEIGHT / 2 - total_h / 2
    y_offset = 0
    for l in lines:
        text, _ = font.render(l, fgcolor=MENU_COLOR, size=MENU_SIZE)
        w = text.get_width()
        dest = (SCREEN_WIDTH / 2 - w / 2, y_start + y_offset)
        screen.blit(text, dest)
        y_offset += h + MENU_SPACING
