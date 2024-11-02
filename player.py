import pygame

from circleshape import CircleShape
from shot import Shot
from constants import *


class Player(CircleShape):
    """The player spaceship

    It's a circular sprite, but also includes a rotational value.
    """

    def __init__(self, position):
        super().__init__(position, radius=PLAYER_RADIUS)

        self.rotation = 0
        self.shot_cooldown = 0

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
        """Update the player spaceship

        This is a common pattern in simpler games: Each entity has an
        `update()` method, that gets called at each tick of the games clock.
        The update method checks certain conditions (like keys being pressed,
        events that have fired, etc.) and calls a list of entity-methods that
        do the actual updating.

        Note that the update has nothing to do with the *drawing* of the
        entity. This happens *after* the update is done.
        """

        # decrease shot cooldown timer
        # if this is > 0, player cannot shoot
        self.shot_cooldown -= dt

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_UP]:
            self.accelerate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        self.move()

    def rotate(self, dt: float):
        """Update spaceship rotation"""
        self.rotation += dt * PLAYER_TURN_SPEED

    def accelerate(self, dt: float):
        """Accelerate the spaceship in the current direction"""
        a = PLAYER_ACCELERATION * dt
        v = pygame.Vector2(0, 1).rotate(self.rotation) * a
        self.velocity += v
        if self.velocity.magnitude() >= PLAYER_MAX_SPEED:
            self.velocity = (
                pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_MAX_SPEED
            )

    def move(self):
        """Move the player spaceship ahead"""

        # forward pointing unit-vector
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += self.velocity

    def shoot(self):
        """Spawn a new shot"""
        if self.shot_cooldown > 0:
            return
        shot = Shot(self.position)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = forward * SHOT_SPEED
        self.shot_cooldown = SHOT_COOLDOWN
