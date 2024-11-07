import pygame

from assets import ASSETS
from circleshape import CircleShape
from constants import *


class Explosion(CircleShape):
    """An explosion

    Explosions go through steps after they are spawned, with the time from one
    step to the next  being controlled by `EXPLOSION_STEP_DURATION`. After the
    maximum step is reached, explosions automatically despawn."""

    def __init__(self, position, radius):
        super().__init__(position, radius)
        self.step = 1
        self.step_time = 0
        self.size = 2 * radius

    def update(self, dt: float):
        self.step_time += dt
        if self.step_time >= EXPLOSION_STEP_DURATION:
            self.step += 1
            self.step_time = 0
        if self.step > EXPLOSION_STEPS:
            self.kill()

    def draw(self, screen: pygame.Surface):
        """Draw the current stage of the explosion with the correct radius"""

        asset_name = f"explosion_{self.step}.png"
        base_img = ASSETS[asset_name]
        # transform stage image to correct radius
        scaled_img = pygame.transform.scale(base_img, (self.size, self.size))
        x = self.position.x - self.radius
        y = self.position.y - self.radius
        screen.blit(scaled_img, (x, y))
