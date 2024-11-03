"""Module state contains the different states the game can be in."""

from __future__ import annotations

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


class Loop:
    """A game loop or state"""

    def __init__(self, screen: Surface, storage: dict):
        self.screen = screen
        self.storage = storage

    def step(self, dt: float) -> Loop:
        """Subclasse have to override this.

        Step returns the state that should be changed into"""
        raise NotImplementedError("Loops must implement `step()`")


class GameOver(Loop):
    """Game Over Screen, draws score"""

    def __init__(self, screen, storage):
        super().__init__(screen, storage)
        self.gameover_font = pygame.font.Font(size=36)  # type: ignore
        self.score = storage.get("score", 0)

    def step(self, dt: float) -> Loop:

        for event in pygame.event.get():
            # the `QUIT` event is emitted e.g. by pressing [X] in the window
            if event.type == pygame.QUIT:
                return Quit(self.screen, storage={})
            # we quit the game if the user presses Q or ESC
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_q,
                pygame.K_ESCAPE,
            ]:
                return Quit(self.screen, storage={})
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                return Endless(self.screen, self.storage)

        # redraw background
        self.screen.blit(ASSETS["bkgrd.jpg"], (0, 0))

        game_over_text = self.gameover_font.render(
            "-- GAME OVER --",
            False,
            SCORE_COLOR,
        )
        w_got = game_over_text.get_width()
        h_got = game_over_text.get_height()
        self.screen.blit(
            source=game_over_text,
            dest=(
                SCREEN_WIDTH / 2 - w_got / 2,
                SCREEN_HEIGHT / 2 - h_got / 2,
            ),
        )

        scoreboard = self.gameover_font.render(
            f"SCORE: {self.score}",
            False,
            SCORE_COLOR,
        )
        w_sb = scoreboard.get_width()
        h_sb = scoreboard.get_height()
        self.screen.blit(
            source=scoreboard,
            dest=(
                SCREEN_WIDTH / 2 - w_sb / 2,
                SCREEN_HEIGHT / 2 - h_sb / 2 + h_got + 10,
            ),
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
        self.pause_font = pygame.font.Font(size=36)  # type: ignore

    def step(self, dt: float) -> Loop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return self.previous_state

        # display -- PAUSE -- text
        pause_text = self.pause_font.render(
            "-- GAME PAUSED --",
            False,
            SCORE_COLOR,
        )
        w_got = pause_text.get_width()
        h_got = pause_text.get_height()
        self.screen.blit(
            source=pause_text,
            dest=(
                SCREEN_WIDTH / 2 - w_got / 2,
                SCREEN_HEIGHT / 2 - h_got / 2,
            ),
        )
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
        self.score_font = pygame.font.Font(size=12)  # type: ignore
        self.score = 0

    def step(self, dt: float) -> Loop:
        """A single step in this game loop"""

        for event in pygame.event.get():
            # the `QUIT` event is emitted e.g. by pressing [X] in the window
            if event.type == pygame.QUIT:
                return Quit(self.screen, storage={})
            # we quit the game if the user presses Q or ESC
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_q,
                pygame.K_ESCAPE,
            ]:
                return Quit(self.screen, storage={})
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
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
        draw_scoreboard(self.score, self.screen)

        return self
