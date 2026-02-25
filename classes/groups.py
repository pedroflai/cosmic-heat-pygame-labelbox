"""Game state container — sprite groups, boss state, and game-state enum."""
from enum import Enum, auto

import pygame


class State(Enum):
    """Top-level game states."""
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class BossState:
    """Tracks health, spawn flag, and health-bar rect for each boss."""

    _DEFAULTS = [
        # (max_health, bar_width)
        (150, 150),
        (150, 150),
        (200, 200),
    ]

    def __init__(self):
        self.reset()

    def reset(self):
        self.health = [hp for hp, _ in self._DEFAULTS]
        self.spawned = [False, False, False]
        self.bar_rects = [
            pygame.Rect(0, 0, w, 5) for _, w in self._DEFAULTS
        ]


class GameGroups:
    """All sprite groups and boss state needed by the game loop."""

    def __init__(self):
        # visual effects
        self.explosions = pygame.sprite.Group()
        self.explosions2 = pygame.sprite.Group()

        # player projectiles
        self.bullets = pygame.sprite.Group()

        # enemies
        self.enemy1 = pygame.sprite.Group()
        self.enemy2 = pygame.sprite.Group()
        self.enemy2_bullets = pygame.sprite.Group()

        # bosses (indexed 0-2)
        self.boss = [pygame.sprite.Group() for _ in range(3)]
        self.boss_bullets = [pygame.sprite.Group() for _ in range(3)]

        # refills / pickups
        self.bullet_refill = pygame.sprite.Group()
        self.health_refill = pygame.sprite.Group()
        self.double_refill = pygame.sprite.Group()
        self.extra_score = pygame.sprite.Group()

        # environmental hazards
        self.meteors = pygame.sprite.Group()
        self.meteors2 = pygame.sprite.Group()
        self.black_holes = pygame.sprite.Group()

        # boss tracking
        self.boss_state = BossState()

    # -- helpers --

    def _all_groups(self):
        """Yield every sprite group for bulk operations."""
        yield self.explosions
        yield self.explosions2
        yield self.bullets
        yield self.enemy1
        yield self.enemy2
        yield self.enemy2_bullets
        for g in self.boss:
            yield g
        for g in self.boss_bullets:
            yield g
        yield self.bullet_refill
        yield self.health_refill
        yield self.double_refill
        yield self.extra_score
        yield self.meteors
        yield self.meteors2
        yield self.black_holes

    def empty_all(self):
        """Clear every group and reset boss state."""
        for g in self._all_groups():
            g.empty()
        self.boss_state.reset()
