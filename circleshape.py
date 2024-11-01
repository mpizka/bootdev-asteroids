import pygame


class CircleShape(pygame.sprite.Sprite):
    """Base Class for our ingame objects

    Our subclass of Sprite stores position, velocity and radius.
    """

    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)  # type: ignore
        else:
            super().__init__()

        # This is actually a convenience for pygame.math.Vector2
        # It's just a 2D vector
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

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
