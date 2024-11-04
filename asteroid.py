from __future__ import annotations
import random

import pygame
from pygame import Vector2

from assets import ASSETS
from circleshape import CircleShape
from constants import *
from explosion import Explosion


class Asteroid(CircleShape):

    def __init__(self, position, radius, size, kind=None):
        super().__init__(position, radius)
        self.size = size
        if kind is None:
            kind = random.randint(1, ASTEROID_KINDS)
        self.kind = kind

    def draw(self, screen: pygame.Surface):
        """Asteroids are just drawn as circles"""
        img = ASSETS[f"asteroid_{self.size}_{self.kind}.png"]
        x = self.position.x - img.get_width() / 2
        y = self.position.y - img.get_height() / 2
        screen.blit(img, (x, y))
        if DEBUG_SHOW_HITBOX:
            self.debug_draw_hitbox(screen)

    def update(self, dt: float):
        """Asteroids move by their velicity (which is a Vector2) at each frame"""
        self.position += self.velocity * dt

    def split(self):
        """Asteroids split when getting shot

        New velocitiy vectors are 20-50 deg different from current one, and
        move faster.
        """
        # remove the current asteroid
        self.kill()

        # don't split small asteroids
        if self.size == 1:
            return

        split_size = self.size - 1
        split_angle = random.uniform(20, 50)
        v1 = self.velocity.rotate(split_angle) * 1.2
        v2 = self.velocity.rotate(-split_angle) * 1.2
        radius = ASTEROID_MIN_RADIUS * split_size
        a1 = Asteroid(self.position, radius, split_size, self.kind)
        a2 = Asteroid(self.position, radius, split_size, self.kind)
        a1.velocity = v1
        a2.velocity = v2

    def explode(self):
        Explosion(self.position, self.radius)

    @classmethod
    def spawn(cls, size=None):
        """Spawn an asteroid

        The asteroid will be spawned randomly at one of the 4 screen edges, and
        have a velocity away from it. The asteroid will be added to all `*groups`
        """
        if size is None:
            size = random.randint(1, ASTEROID_SIZES)
        radius = ASTEROID_MIN_RADIUS * size
        half_r = radius / 2
        position_mod = random.uniform(0, 1)
        speed = random.randint(40, 100)
        rotation = random.randint(-30, 30)
        edge = random.choice(("top", "bottom", "left", "right"))
        match edge:
            case "top":
                velocity = Vector2(0, 1).rotate(rotation) * speed
                position = Vector2(SCREEN_WIDTH * position_mod, half_r)
            case "bottom":
                velocity = Vector2(0, -1).rotate(rotation) * speed
                position = Vector2(SCREEN_WIDTH * position_mod, SCREEN_HEIGHT - half_r)
            case "left":
                velocity = Vector2(1, 0).rotate(rotation) * speed
                position = Vector2(half_r, SCREEN_HEIGHT * position_mod)
            case "right":
                velocity = Vector2(-1, 0).rotate(rotation) * speed
                position = Vector2(SCREEN_WIDTH - half_r, SCREEN_HEIGHT * position_mod)

        asteroid = Asteroid(position, radius, size)
        asteroid.velocity = velocity
