import pygame

from circleshape import CircleShape


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
