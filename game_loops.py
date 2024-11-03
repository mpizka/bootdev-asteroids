"""Module game_loops contains the different states the game can be in."""

import pygame
from pygame import Surface
from pygame.sprite import Group

from assets import ASSETS
from asteroid import Asteroid
from constants import *
from player import Player
from score import draw_scoreboard
from shot import Shot
from explosion import Explosion

STATE_QUIT = 1
STATE_ENDLESS = 2


class Loop:
    """A game loop or state"""

    def __init__(self, screen: Surface, state: int):
        self.screen = screen
        self.state = state

    def step(self, dt: float) -> int:
        """Subclasse have to override this.

        Step returns the state that should be changed into
        or 0 if no statechange should happen"""
        raise NotImplementedError("Loops must implement `step()`")


class Endless(Loop):
    """Endless game. Asteroids spawn continuously from the edges."""

    def __init__(self, screen):
        super().__init__(screen, STATE_ENDLESS)

        # setup groups
        self.drawable = pygame.sprite.Group()
        self.updateable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()

        # Set default groups for classes
        Player.set_default_groups(self.drawable, self.updateable)
        Asteroid.set_default_groups(self.asteroids, self.updateable, self.drawable)
        Shot.set_default_groups(self.shots, self.updateable, self.drawable)
        Explosion.set_default_groups(self.drawable, self.updateable)

        self.asteroid_cooldown = 0

        # instanciate player
        self.player = Player(pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        # score tracker
        self.score_font = pygame.font.Font(size=12)  # type: ignore
        self.score = 0

        # instanciate player
        player = Player(pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def step(self, dt: float) -> int:
        """A single step in this game loop"""

        for event in pygame.event.get():
            # the `QUIT` event is emitted e.g. by pressing [X] in the window
            if event.type == pygame.QUIT:
                return STATE_QUIT
            # we quit the game if the user presses Q or ESC
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_q,
                pygame.K_ESCAPE,
            ]:
                return STATE_QUIT

        # redraw background
        self.screen.blit(ASSETS["bkgrd.jpg"], (0, 0))

        # spawn asteroids
        self.asteroid_cooldown -= dt
        if self.asteroid_cooldown <= 0:
            Asteroid.spawn()
            self.asteroid_cooldown = ASTEROID_SPAWN_COOLDOWN

        # run updates and remove out-of-screen objects
        for u in self.updateable:
            if (
                u.position.x > SCREEN_WIDTH
                or u.position.x < 0
                or u.position.y > SCREEN_HEIGHT
                or u.position.y < 0
            ):
                if u is self.player:
                    print(f"Game over! {self.score=}")
                    return STATE_QUIT
                u.kill()
                continue
            u.update(dt)

        # determine if asteroids hit player
        for a in self.asteroids:
            if a.collides_with(self.player):
                print(f"Game over! {self.score=}")
                return STATE_QUIT

        # determine if shots hit asteroids
        for a in self.asteroids:
            for s in self.shots:
                if a.collides_with(s):
                    a.split()
                    a.explode()
                    s.kill()
                    self.score += 1
                    break

        # draw sprites
        for d in self.drawable:
            d.draw(self.screen)

        # draw scoreboard
        draw_scoreboard(self.score, self.screen)

        return self.state
