import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius=radius)

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
        x = self.position.x
        y = self.position.y
        a1 = Asteroid(x, y, radius)
        a2 = Asteroid(x, y, radius)
        a1.velocity = v1
        a2.velocity = v2
