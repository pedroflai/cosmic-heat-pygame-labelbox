"""All projectile (bullet) sprites: player, enemy, and boss bullets."""
import math

import pygame

from .constants import HEIGHT
from . import sound


class Bullet(pygame.sprite.Sprite):
    """Player bullet — flies upward."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/bullets/bullet1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y - 10
        self.speed = 10
        self.shoot_sound = sound.load_sound('game_sounds/shooting/shoot.mp3')
        self.shoot_sound.set_volume(0.4)
        self.shoot_sound.play()

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top <= 1:
            self.kill()


class Enemy2Bullet(pygame.sprite.Sprite):
    """Bullet fired by Enemy2 — drops straight down."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/bullets/bullet4.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y + 10
        self.speed = 8
        self.shoot_sound = sound.load_sound('game_sounds/shooting/shoot2.mp3')
        self.shoot_sound.set_volume(0.3)
        self.shoot_sound.play()

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.kill()


class Boss1Bullet(pygame.sprite.Sprite):
    """Bullet fired by Boss1 — drops straight down, fast."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/bullets/bulletboss1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y + 10
        self.speed = 10
        self.shoot_sound = sound.load_sound('game_sounds/shooting/boss1shoot.mp3')
        self.shoot_sound.set_volume(0.4)
        self.shoot_sound.play()

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.kill()


class Boss2Bullet(pygame.sprite.Sprite):
    """Homing bullet fired by Boss2 — follows a direction vector and rotates."""

    def __init__(self, x, y, direction):
        super().__init__()
        self.image_orig = pygame.image.load('images/bullets/bulletboss2.png').convert_alpha()
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y + 10
        self.speed = 11
        self.direction = direction
        self.shoot_sound = sound.load_sound('game_sounds/shooting/boss2shoot.mp3')
        self.shoot_sound.set_volume(0.4)
        self.shoot_sound.play()

    def update(self):
        self.rect.move_ip(self.direction.x * self.speed, self.direction.y * self.speed)
        angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
        self.image = pygame.transform.rotate(self.image_orig, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.top > HEIGHT:
            self.kill()


class Boss3Bullet(pygame.sprite.Sprite):
    """Homing bullet fired by Boss3 — faster variant of Boss2Bullet."""

    def __init__(self, x, y, direction):
        super().__init__()
        self.image_orig = pygame.image.load('images/bullets/bulletboss3.png').convert_alpha()
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y + 10
        self.speed = 15
        self.direction = direction
        self.shoot_sound = sound.load_sound('game_sounds/shooting/boss2shoot.mp3')
        self.shoot_sound.set_volume(0.4)
        self.shoot_sound.play()

    def update(self):
        self.rect.move_ip(self.direction.x * self.speed, self.direction.y * self.speed)
        angle = math.degrees(math.atan2(self.direction.y, self.direction.x))
        self.image = pygame.transform.rotate(self.image_orig, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.top > HEIGHT:
            self.kill()
