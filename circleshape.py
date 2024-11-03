from __future__ import annotations
import pygame


class CircleShape(pygame.sprite.Sprite):
    """Base Class for our ingame objects

    Our subclass of Sprite stores position, velocity and radius.
    """

    __groups = []

    @classmethod
    def set_default_groups(cls, *groups):
        """Set the default `pygame.sprite.Group`s instances of this class belong to"""
        cls.__groups = groups

    def __init__(self, position, radius):
        super().__init__(*self.__groups)

        # The reason we are re-building a vector here: because otherwise
        # multiple objects would suddenly SHARE position-vectors with all sorts
        # of hillarious consequences.
        self.position = pygame.Vector2(position.x, position.y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def debug_draw_hitbox(self, screen):
        """Draws the hitbox on the screen for debug purposes"""
        pygame.draw.circle(
            surface=screen,
            color="#FF0000",
            center=self.position,
            radius=self.radius,
            width=1,
        )

    def draw(self, screen):
        """Every object should have a "draw" method that draws itself onto
        a screen

        Needs to be overridden by subclasses.
        """
        pass

    def update(self, dt):
        """Update the sprite by the delta-time

        Needs to be overridden by subclasses.
        """
        pass

    def collides_with(self, other: CircleShape) -> bool:
        sp = self.position
        op = other.position
        distance = sp.distance_to(op)
        return distance <= self.radius + other.radius
