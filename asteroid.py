from __future__ import annotations
import random

import pygame

from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):

    def __init__(self, position, radius):
        super().__init__(position, radius)

    def draw(self, screen: pygame.Surface):
        """Asteroids are just drawn as circles"""
        pygame.draw.circle(
            surface=screen,
            color="#FFFFFF",
            center=self.position,
            radius=self.radius,
            width=2,
        )

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

        # don't split too small asteroids
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        split_angle = random.uniform(20, 50)
        v1 = self.velocity.rotate(split_angle) * 1.2
        v2 = self.velocity.rotate(-split_angle) * 1.2
        radius = self.radius - ASTEROID_MIN_RADIUS
        a1 = Asteroid(self.position, radius)
        a2 = Asteroid(self.position, radius)
        a1.velocity = v1
        a2.velocity = v2

    @classmethod
    def spawn(cls):
        """Spawn an asteroid

        The asteroid will be spawned randomly at one of the 4 screen edges, and
        have a velocity away from it. The asteroid will be added to all `*groups`
        """
        position_mod = random.uniform(0, 1)
        speed = random.randint(40, 100)
        rotation = random.randint(-30, 30)
        edge = random.choice(("top", "bottom", "left", "right"))
        match edge:
            case "top":
                velocity = pygame.Vector2(0, 1).rotate(rotation) * speed
                position = pygame.Vector2(
                    SCREEN_WIDTH * position_mod, ASTEROID_MAX_RADIUS
                )
            case "bottom":
                velocity = pygame.Vector2(0, -1).rotate(rotation) * speed
                position = pygame.Vector2(
                    SCREEN_WIDTH * position_mod, SCREEN_HEIGHT - ASTEROID_MAX_RADIUS
                )
            case "left":
                velocity = pygame.Vector2(1, 0).rotate(rotation) * speed
                position = pygame.Vector2(
                    ASTEROID_MAX_RADIUS, SCREEN_HEIGHT * position_mod
                )
            case "right":
                velocity = pygame.Vector2(-1, 0).rotate(rotation) * speed
                position = pygame.Vector2(
                    SCREEN_WIDTH - ASTEROID_MAX_RADIUS, SCREEN_HEIGHT * position_mod
                )

        asteroid = Asteroid(
            position,
            ASTEROID_MIN_RADIUS * random.randint(1, ASTEROID_KINDS),
        )
        asteroid.velocity = velocity
