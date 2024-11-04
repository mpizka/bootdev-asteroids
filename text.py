from pygame import Surface
from pygame.font import Font

from constants import *


def draw_bottom_right(screen: Surface, line: str):
    """Draw a line to the bottom right"""
    score_font = Font(size=SCORE_SIZE)  # type: ignore
    scoreboard = score_font.render(line, False, SCORE_COLOR)
    screen.blit(
        source=scoreboard,
        dest=(
            SCREEN_WIDTH - scoreboard.get_width(),
            SCREEN_HEIGHT - scoreboard.get_height(),
        ),
    )


def draw_lines_mid(screen: Surface, lines: list[str]):
    """Draw centered lines in the middle of the screen"""
    mid_font = Font(size=36)  # type: ignore
    y_offset = 0
    for l in lines:
        text = mid_font.render(l, False, SCORE_COLOR)
        w, h = text.get_width(), text.get_height()
        dest = (SCREEN_WIDTH / 2 - w / 2, SCREEN_HEIGHT / 2 - h / 2 + y_offset)
        screen.blit(text, dest)
        y_offset += h + 10
