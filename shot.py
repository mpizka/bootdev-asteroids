import pygame

from circleshape import CircleShape
from constants import SHOT_RADIUS, SHOT_SPEED


class Shot(CircleShape):

    def __init__(self, position):
        super().__init__(position, radius=SHOT_RADIUS)

    def draw(self, screen: pygame.Surface):
        """Shots are just drawn as circles"""
        pygame.draw.circle(
            surface=screen,
            color="#FF00FF",
            center=self.position,
            radius=self.radius,
            width=1,
        )

    def update(self, dt: float):
        """Asteroids move by their velicity (which is a Vector2) at each frame"""
        self.position += self.velocity * dt
