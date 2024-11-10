import pygame
from pygame.transform import rotate
from pygame import Vector2

from assets import ASSETS
from circleshape import CircleShape
from shot import Mjolnir, Shot
from constants import *
from explosion import Explosion


class Taurus(CircleShape):
    """The Taurus mobile defense platform"""

    def __init__(self, position):
        super().__init__(position, radius=TAURUS_RADIUS)

        # cooldown for the plasma shots
        self.shot_cooldown = 0
        # cooldown for the mjolnir cannon
        self.mjolnir_cooldown = 0

        # engine running states
        self.engine_top = False
        self.engine_bottom = False
        self.engine_left = False
        self.engine_right = False

    def draw(self, screen: pygame.Surface):
        """Draw the Taurus and the currently running engines"""

        taurus = ASSETS["taurus.png"]
        taurus_cd = ASSETS["taurus_cd.png"]
        t_r = taurus.get_rect()
        th = t_r.height
        tw = t_r.width

        engine_top = ASSETS["taurus_engine_top.png"]
        engine_bottom = ASSETS["taurus_engine_bottom.png"]
        engine_left = ASSETS["taurus_engine_left.png"]
        engine_right = ASSETS["taurus_engine_right.png"]

        # all the engine images are 10 x 24 or 24 x 10

        # rot_img = pygame.transform.rotate(ASSETS[asset_name], -self.rotation)
        # blit the engines
        if self.engine_top:
            x, y = self.position.x - 5, self.position.y - 50 - 20
            screen.blit(engine_top, (x, y))
        if self.engine_bottom:
            x, y = self.position.x - 5, self.position.y + 50
            screen.blit(engine_bottom, (x, y))
        if self.engine_left:
            x, y = self.position.x - 50 - 20, self.position.y - 5
            screen.blit(engine_left, (x, y))
        if self.engine_right:
            x, y = self.position.x + 50, self.position.y - 5
            screen.blit(engine_right, (x, y))

        # blit the station on top
        x = self.position.x - tw / 2
        y = self.position.y - th / 2
        screen.blit(taurus_cd if self.mjolnir_cooldown > 0 else taurus, (x, y))

        if DEBUG_SHOW_HITBOX:
            self.debug_draw_hitbox(screen)

    def update(self, dt: float):
        """Update the Taurus"""

        # decrease shot cooldown timer
        # if this is > 0, player cannot shoot
        self.shot_cooldown -= dt
        self.mjolnir_cooldown -= dt

        self.engine_top = self.engine_bottom = self.engine_left = self.engine_right = (
            False
        )

        keys = pygame.key.get_pressed()
        m_left, m_mid, m_right = pygame.mouse.get_pressed()
        if any((keys[pygame.K_RIGHT], keys[pygame.K_d])):
            self.engine_left = True
        if any((keys[pygame.K_LEFT], keys[pygame.K_a])):
            self.engine_right = True
        if any((keys[pygame.K_UP], keys[pygame.K_w])):
            self.engine_bottom = True
        if any((keys[pygame.K_DOWN], keys[pygame.K_s])):
            self.engine_top = True
        # left mouse: shoot plasma cannon
        if m_left:
            self.shoot()
        # right mouse: fore mjolnir cannon
        if m_right:
            self.fire_mjolnir()

        self.accelerate(dt)
        self.move()

    def accelerate(self, dt: float):
        """Accelerate the spaceship in the current direction"""
        a = TAURUS_ACCELERATION * dt
        v_down = pygame.Vector2(0, 1) * a * int(self.engine_top)
        v_up = pygame.Vector2(0, -1) * a * int(self.engine_bottom)
        v_left = pygame.Vector2(-1, 0) * a * int(self.engine_right)
        v_right = pygame.Vector2(1, 0) * a * int(self.engine_left)
        v = v_down + v_up + v_left + v_right
        velocity_old = self.velocity
        self.velocity += v
        if self.velocity.magnitude() >= TAURUS_MAX_SPEED:
            self.velocity = velocity_old

    def move(self):
        """Move the player spaceship ahead"""

        # forward pointing unit-vector
        self.position += self.velocity

    def shoot(self):
        """Spawn a new shot"""
        if self.shot_cooldown > 0:
            return
        # the direction vector for the shot, from position:
        # mouse-vector - position-vector
        v_mouse = Vector2(pygame.mouse.get_pos())
        direction = self.position - v_mouse
        direction.normalize_ip()
        shot = Shot(self.position - direction * self.radius)  # type: ignore
        shot.velocity = -direction * SHOT_SPEED
        self.shot_cooldown = SHOT_COOLDOWN

    def fire_mjolnir(self):
        """Fire the Mjolnir close-range defense cannon"""
        if self.mjolnir_cooldown > 0:
            return

        v_mouse = Vector2(pygame.mouse.get_pos())
        direction = self.position - v_mouse
        direction.normalize_ip()
        pos = self.position - direction * self.radius  # type: ignore
        shot_1 = Mjolnir(pos)
        shot_2 = Mjolnir(pos)
        shot_3 = Mjolnir(pos)
        shot_1.velocity = -direction.rotate(20) * MJOLNIR_SPEED
        shot_2.velocity = -direction * MJOLNIR_SPEED
        shot_3.velocity = -direction.rotate(-20) * MJOLNIR_SPEED

        self.mjolnir_cooldown = MJOLNIR_COOLDOWN

    def explode(self):
        Explosion(self.position, self.radius * 1.5)
