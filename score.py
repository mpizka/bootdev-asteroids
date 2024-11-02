import pygame

from constants import *


def draw_scoreboard(score: int, screen: pygame.Surface):
    """Draw the scoreboard in the screen"""
    score_font = pygame.font.Font(size=SCORE_SIZE)  # type: ignore
    scoreboard = score_font.render(f"SCORE: {score}", False, SCORE_COLOR)
    screen.blit(
        source=scoreboard,
        dest=(
            SCREEN_WIDTH - scoreboard.get_width(),
            SCREEN_HEIGHT - scoreboard.get_height(),
        ),
    )
