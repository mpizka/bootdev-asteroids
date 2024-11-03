from __future__ import annotations
import random

import pygame
from pygame import Vector2

from assets import ASSETS
from circleshape import CircleShape
from constants import *
from explosion import Explosion


class Asteroid(CircleShape):

    def __init__(self, position, radius, kind):
        super().__init__(position, radius)
        self.kind = kind

    def draw(self, screen: pygame.Surface):
        """Asteroids are just drawn as circles"""
        x = self.position.x - self.radius
        y = self.position.y - self.radius
        screen.blit(ASSETS[f"asteroid_{self.kind}_1.png"], (x, y))
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
        if self.kind == 1:
            return

        split_kind = self.kind - 1
        split_angle = random.uniform(20, 50)
        v1 = self.velocity.rotate(split_angle) * 1.2
        v2 = self.velocity.rotate(-split_angle) * 1.2
        radius = ASTEROID_MIN_RADIUS * split_kind
        a1 = Asteroid(self.position, radius, split_kind)
        a2 = Asteroid(self.position, radius, split_kind)
        a1.velocity = v1
        a2.velocity = v2

    def explode(self):
        Explosion(self.position, self.radius)

    @classmethod
    def spawn(cls):
        """Spawn an asteroid

        The asteroid will be spawned randomly at one of the 4 screen edges, and
        have a velocity away from it. The asteroid will be added to all `*groups`
        """
        kind = random.randint(1, ASTEROID_KINDS)
        radius = ASTEROID_MIN_RADIUS * kind
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

        asteroid = Asteroid(position, radius, kind)
        asteroid.velocity = velocity
