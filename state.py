"""Module state contains the different states the game can be in."""

from __future__ import annotations

import pygame
from pygame import Surface
from pygame.sprite import Group

from assets import ASSETS
from asteroid import Asteroid
from constants import *
from player import Player
import text
from shot import Shot
from explosion import Explosion


class Loop:
    """A game loop or state"""

    def __init__(self, screen: Surface, storage: dict):
        self.screen = screen
        self.storage = storage

    def step(self, dt: float) -> Loop:
        """Subclasse have to override this.

        Step returns the state that should be changed into"""
        raise NotImplementedError("Loops must implement `step()`")


class Menu(Loop):
    """Display Game Menu"""

    def __init__(self, screen, storage):
        super().__init__(screen, storage)
        self.score = storage.get("score", 0)

    def step(self, dt: float) -> Loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Quit(self.screen, storage={})
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return Quit(self.screen, storage={})
                if event.key == pygame.K_e:
                    return Endless(self.screen, {})
                if event.key == pygame.K_l:
                    return Level(self.screen, {}, level=1)

        # redraw background
        self.screen.blit(ASSETS["bkgrd.jpg"], (0, 0))

        # draw title logo
        logo = ASSETS["logo_400.png"]
        x = SCREEN_WIDTH / 2 - logo.get_width() / 2
        y = SCREEN_HEIGHT / 4 - logo.get_height() / 2 + 20
        self.screen.blit(logo, (x, y))

        # draw menu
        text.draw_lines_mid(
            self.screen,
            lines=[
                "-GAME MODE-",
                "E: Endless",
                "L: Level  ",
            ],
            y_start=SCREEN_HEIGHT / 5 * 3,
        )
        return self


class GameOver(Loop):
    """Game Over Screen, draws score"""

    def __init__(self, screen, storage):
        super().__init__(screen, storage)
        self.score = storage.get("score", 0)

    def step(self, dt: float) -> Loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Quit(self.screen, storage={})
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return Menu(self.screen, storage={})

        # redraw background
        self.screen.blit(ASSETS["bkgrd.jpg"], (0, 0))

        # draw text
        text.draw_lines_mid(
            self.screen,
            lines=[
                "-- GAME OVER --",
                f"SCORE: {self.score}",
            ],
        )

        return self


class Quit(Loop):
    """State to quit the game"""

    def __init__(self, screen, storage):
        super().__init__(screen, storage)


class Pause(Loop):
    """State to pause the game

    Takes a state as argument which is returned when un-pausing"""

    def __init__(self, screen, storage, previous_state: Loop):
        super().__init__(screen, storage)
        self.previous_state = previous_state

    def step(self, dt: float) -> Loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Quit(self.screen, storage={})
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return Menu(self.screen, storage={})
                if event.key == pygame.K_p:
                    return self.previous_state

        # draw text
        text.draw_lines_mid(self.screen, lines=["-- GAME PAUSED --"])

        return self


class LevelCleared(Loop):
    """Level Clear Screen"""

    def __init__(self, screen, storage: dict, level):
        super().__init__(screen, storage)
        self.level = level

    def step(self, dt: float) -> Loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Quit(self.screen, storage={})
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return Menu(self.screen, storage={})
                if event.key == pygame.K_n:
                    return Level(self.screen, self.storage, self.level + 1)

        # draw text
        text.draw_lines_mid(
            self.screen,
            lines=[f"-- LEVEL {self.level} cleared --", "Press N to continue"],
        )

        return self


class Level(Loop):
    """Level Based Game

    A set number of asteroids spawn at once. Objects going over the edge of the
    screen re-appear on the other side (except for shots)"""

    def __init__(self, screen, storage: dict, level):
        super().__init__(screen, storage)

        self.level = level

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

        # spawn player
        self.player = Player(pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        # spawn asteroids
        for _ in range(self.level * 2):
            Asteroid.spawn(size=ASTEROID_SIZES)

        # score tracker
        self.score = self.storage.get("score", 0)

    def step(self, dt: float) -> Loop:
        """A single step in this game loop"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Quit(self.screen, storage={})
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return Menu(self.screen, storage={})
                if event.key == pygame.K_p:
                    return Pause(self.screen, self.storage, self)

        # redraw background
        self.screen.blit(ASSETS["bkgrd.jpg"], (0, 0))

        # run updates and remove out-of-screen objects
        for u in self.updateable:

            # shots don't wrap around
            if isinstance(u, Shot) and (
                u.position.x > SCREEN_WIDTH
                or u.position.x < 0
                or u.position.y > SCREEN_HEIGHT
                or u.position.y < 0
            ):
                u.kill()
                continue

            if u.position.x - u.radius > SCREEN_WIDTH:
                u.position.x = -u.radius

            if u.position.x < -u.radius:
                u.position.x = SCREEN_WIDTH + u.radius

            if u.position.y - u.radius > SCREEN_HEIGHT:
                u.position.y = -u.radius

            if u.position.y < -u.radius:
                u.position.y = SCREEN_HEIGHT + u.radius

            u.update(dt)

        # determine if asteroids hit player
        for a in self.asteroids:
            if a.collides_with(self.player):
                self.storage["score"] = self.score
                return GameOver(self.screen, storage=self.storage)

        # determine if shots hit asteroids
        for a in self.asteroids:
            for s in self.shots:
                if a.collides_with(s):
                    s.kill()
                    a.split()
                    a.explode()
                    self.score += 1
                    break

        # check if level complete
        if len(self.asteroids) == 0:
            self.storage["score"] = self.score
            return LevelCleared(self.screen, storage=self.storage, level=self.level)

        # draw sprites
        for d in self.drawable:
            d.draw(self.screen)

        # draw scoreboard
        text.draw_bottom_right(self.screen, f"SCORE: {self.score}")

        return self


class Endless(Loop):
    """Endless game. Asteroids spawn continuously from the edges."""

    def __init__(self, screen, storage: dict):
        super().__init__(screen, storage)

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
        self.score = 0

    def step(self, dt: float) -> Loop:
        """A single step in this game loop"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Quit(self.screen, storage={})
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return Menu(self.screen, storage={})
                if event.key == pygame.K_p:
                    return Pause(self.screen, self.storage, self)

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
                # detect ship crashing into the void
                if u is self.player:
                    self.storage["score"] = self.score
                    return GameOver(self.screen, storage=self.storage)
                u.kill()
                continue
            u.update(dt)

        # determine if asteroids hit player
        for a in self.asteroids:
            if a.collides_with(self.player):
                self.storage["score"] = self.score
                return GameOver(self.screen, storage=self.storage)

        # determine if shots hit asteroids
        for a in self.asteroids:
            for s in self.shots:
                if a.collides_with(s):
                    s.kill()
                    a.split()
                    a.explode()
                    self.score += 1
                    break

        # draw sprites
        for d in self.drawable:
            d.draw(self.screen)

        # draw scoreboard
        text.draw_bottom_right(self.screen, f"SCORE: {self.score}")

        return self
