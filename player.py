import pygame

from circleshape import CircleShape
from constants import PLAYER_RADIUS


class Player(CircleShape):
    """The player spaceship

    It's a circular sprite, but also includes a rotational value.
    """

    def __init__(self, x, y):
        super().__init__(x, y, radius=PLAYER_RADIUS)

        self.rotation = 0

    def draw(self, screen: pygame.Surface):
        """Override the `CircleShape.draw` method to draw the spaceship"""
        pygame.draw.polygon(
            surface=screen,
            color="#FFFFFF",
            points=self.triangle(),
            width=2,
        )

    def triangle(self):
        """Returns the 3 points of a triangle pointing forward Accorind gto `self.rotation`"""
        # unit vector pointing forward
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # vector pointing to the right
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5

        # pygame Vector classes can be used to determine points very easily
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
