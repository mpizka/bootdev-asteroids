import random

import pygame

from assets import ASSETS
from circleshape import CircleShape
from constants import *


class Shot(CircleShape):
    """Projectiles for the normal PLasma Cannon"""

    def __init__(self, position):
        super().__init__(position, radius=SHOT_RADIUS)
        self.kind = random.randint(1, SHOT_KINDS)

    def draw(self, screen: pygame.Surface):
        """Shots are just drawn as circles"""
        img = ASSETS[f"shot_{self.kind}.png"]
        offset = img.get_rect().height / 2
        x = self.position.x - offset
        y = self.position.y - offset
        screen.blit(img, (x, y))

        if DEBUG_SHOW_HITBOX:
            self.debug_draw_hitbox(screen)

    def update(self, dt: float):
        self.position += self.velocity * dt


class Mjolnir(CircleShape):
    """Projectiles for the Mjolnir Cannon"""

    def __init__(self, position):
        super().__init__(position, radius=MJOLNIR_RADIUS)
        self.kind = random.randint(1, MJOLNIR_KINDS)

    def draw(self, screen: pygame.Surface):
        """Shots are just drawn as circles"""
        img = ASSETS[f"mjolnir_{self.kind}.png"]
        offset = img.get_rect().height / 2
        x = self.position.x - offset
        y = self.position.y - offset
        screen.blit(img, (x, y))

        if DEBUG_SHOW_HITBOX:
            self.debug_draw_hitbox(screen)

    def update(self, dt: float):
        self.position += self.velocity * dt
