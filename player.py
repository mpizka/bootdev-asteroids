import pygame

from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED


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
        # NOTE: pyright doesn't detect the operator validity correctly here
        #       since pygame doesn't use a lot of type hints
        a = self.position + forward * self.radius  # type: ignore
        b = self.position - forward * self.radius - right  # type: ignore
        c = self.position - forward * self.radius + right  # type: ignore
        return [a, b, c]

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_LEFT]:
            self.rotate(-dt)

    def rotate(self, dt: float):
        """Update spaceship rotation"""
        self.rotation += dt * PLAYER_TURN_SPEED
