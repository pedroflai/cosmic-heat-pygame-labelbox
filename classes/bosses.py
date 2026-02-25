"""Boss sprite classes."""
import math
import random

import pygame

from .constants import WIDTH, HEIGHT
from .bullets import Boss1Bullet, Boss2Bullet, Boss3Bullet


class Boss1(pygame.sprite.Sprite):
    """First boss — moves side to side, fires triple bullets."""

    # combat attributes (read by collisions.py)
    contact_damage = 20
    hp_per_bullet = 5
    score_on_kill = 400
    bullet_damage = 20
    drop_chance = 20   # 1-in-N for double refill

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6
        self.direction = random.choice([(-1, 0), (1, 0)])
        self.shoot_timer = 0
        self.shots_fired = 0

    def update(self, enemy_bullets_group, player):
        self.rect.x += math.sin(pygame.time.get_ticks() * 0.01) * 3
        self.rect.y += math.sin(pygame.time.get_ticks() * 0.01) * 3
        if self.shots_fired < 20:
            dx, dy = self.direction
            self.rect.x += dx * self.speed
            self.rect.y = max(self.rect.y, 50)

            if self.rect.left < 5:
                self.rect.left = 5
                self.direction = (1, 0)
            elif self.rect.right > WIDTH - 5:
                self.rect.right = WIDTH - 5
                self.direction = (-1, 0)

            self.shoot_timer += 1
            if self.shoot_timer >= 60:
                bullet1 = Boss1Bullet(self.rect.centerx - 20, self.rect.bottom)
                bullet2 = Boss1Bullet(self.rect.centerx + 20, self.rect.bottom)
                bullet3 = Boss1Bullet(self.rect.centerx, self.rect.bottom)
                enemy_bullets_group.add(bullet1, bullet2, bullet3)
                self.shoot_timer = 0
                self.shots_fired += 1
        else:
            self.speed = 10
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            direction = pygame.math.Vector2(dx, dy).normalize()

            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed


class Boss2(pygame.sprite.Sprite):
    """Second boss — 8-directional movement, homing bullets."""

    # combat attributes
    contact_damage = 2
    hp_per_bullet = 8
    score_on_kill = 800
    bullet_damage = 20
    drop_chance = 20

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1),
                                         (-1, -1), (1, -1), (-1, 1), (1, 1)])
        self.direction_x, self.direction_y = self.direction
        self.shoot_timer = 0
        self.shots_fired = 0

    def update(self, enemy_bullets_group, player):
        self.rect.x += math.sin(pygame.time.get_ticks() * 0.01) * 2
        self.rect.y += math.sin(pygame.time.get_ticks() * 0.01) * 2
        if self.shots_fired < 20:
            dx, dy = self.direction
            if self.direction in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                self.speed = 5 / math.sqrt(2)
            else:
                self.speed = 5
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

            if self.rect.left < 5:
                self.rect.left = 5
                self.direction_x = 1
                if self.direction_y == 0:
                    self.direction_y = 1
            elif self.rect.right > WIDTH - 5:
                self.rect.right = WIDTH - 5
                self.direction_x = -1
                if self.direction_y == 0:
                    self.direction_y = 1
            elif self.rect.top < 70:
                self.rect.top = 70
                self.direction_y = 1
                if self.direction_x == 0:
                    self.direction_x = 1
            elif self.rect.bottom > HEIGHT - 5:
                self.rect.bottom = HEIGHT - 5
                self.direction_y = -1
                if self.direction_x == 0:
                    self.direction_x = 1

            self.direction = (self.direction_x, self.direction_y)
            self.shoot_timer += 1
            if self.shoot_timer >= 100:
                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery
                direction = pygame.math.Vector2(dx, dy).normalize()
                bullet = Boss2Bullet(self.rect.centerx, self.rect.bottom, direction)
                enemy_bullets_group.add(bullet)
                self.shoot_timer = 0
                self.shots_fired += 1
        else:
            if self.speed != 5:
                self.speed = 5 / math.sqrt(2)
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            direction = pygame.math.Vector2(dx, dy).normalize()

            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed

            self.direction_x = direction.x / abs(direction.x) if direction.x != 0 else 0
            self.direction_y = direction.y / abs(direction.y) if direction.y != 0 else 0
            self.direction = (self.direction_x, self.direction_y)


class Boss3(pygame.sprite.Sprite):
    """Third boss — teleports, homing bullets, 8-directional movement."""

    # combat attributes
    contact_damage = 1
    hp_per_bullet = 6
    score_on_kill = 1000
    bullet_damage = 20
    drop_chance = 20

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1),
                                         (-1, -1), (1, -1), (-1, 1), (1, 1)])
        self.direction_x, self.direction_y = self.direction
        self.shoot_timer = 0
        self.shots_fired = 0
        self.teleport_timer = 0
        self.teleport_interval = 160

    def update(self, enemy_bullets_group, player):
        self.rect.x += math.sin(pygame.time.get_ticks() * 0.01) * 2
        self.rect.y += math.sin(pygame.time.get_ticks() * 0.01) * 2
        if self.shots_fired < 20:
            dx, dy = self.direction
            if self.direction in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                self.speed = 5 / math.sqrt(2)
            else:
                self.speed = 5
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

            if self.rect.left < 5:
                self.rect.left = 5
                self.direction_x = 1
                if self.direction_y == 0:
                    self.direction_y = 1
            elif self.rect.right > WIDTH - 5:
                self.rect.right = WIDTH - 5
                self.direction_x = -1
                if self.direction_y == 0:
                    self.direction_y = 1
            elif self.rect.top < 70:
                self.rect.top = 70
                self.direction_y = 1
                if self.direction_x == 0:
                    self.direction_x = 1
            elif self.rect.bottom > HEIGHT - 5:
                self.rect.bottom = HEIGHT - 5
                self.direction_y = -1
                if self.direction_x == 0:
                    self.direction_x = 1

            self.direction = (self.direction_x, self.direction_y)
            self.shoot_timer += 1
            if self.shoot_timer >= 120:
                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery
                direction = pygame.math.Vector2(dx, dy).normalize()
                bullet = Boss3Bullet(self.rect.centerx, self.rect.bottom, direction)
                enemy_bullets_group.add(bullet)
                self.shoot_timer = 0
                self.shots_fired += 1
        else:
            if self.speed != 5:
                self.speed = 5 / math.sqrt(2)
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            direction = pygame.math.Vector2(dx, dy).normalize()

            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed

            self.direction_x = direction.x / abs(direction.x) if direction.x != 0 else 0
            self.direction_y = direction.y / abs(direction.y) if direction.y != 0 else 0
            self.direction = (self.direction_x, self.direction_y)

        self.teleport_timer += 1
        if self.teleport_timer >= self.teleport_interval:
            self.rect.centerx = random.randint(50, WIDTH - 50)
            self.rect.centery = random.randint(100, HEIGHT - 100)
            self.teleport_timer = 0
