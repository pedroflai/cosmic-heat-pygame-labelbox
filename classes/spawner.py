"""Spawning rules — decides what to spawn each frame based on score."""
import random

from .constants import WIDTH, HEIGHT
from .enemies import Enemy1, Enemy2
from .bosses import Boss1, Boss2, Boss3
from .meteors import Meteors, Meteors2, BlackHole
from .refill import ExtraScore


def spawn_tick(score, groups, assets):
    """Run one frame of spawn logic.  Mutates *groups* in-place."""

    # --- basic enemies (always) ---
    if random.randint(0, 120) == 0:
        img = random.choice(assets.enemies['enemy1'])
        groups.enemy1.add(Enemy1(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50),
            img,
        ))

    # --- shooting enemies (score >= 3000, max 2) ---
    if score >= 3000 and random.randint(0, 40) == 0 and len(groups.enemy2) < 2:
        img = random.choice(assets.enemies['enemy2'])
        groups.enemy2.add(Enemy2(
            random.randint(200, WIDTH - 100),
            random.randint(-HEIGHT, -100),
            img,
        ))

    # --- bosses (one-time spawns) ---
    _BOSS_CFG = [
        (5000,  Boss1, 'boss1'),
        (10000, Boss2, 'boss2'),
        (15000, Boss3, 'boss3'),
    ]
    for idx, (threshold, cls, key) in enumerate(_BOSS_CFG):
        if score >= threshold and not groups.boss_state.spawned[idx]:
            assets.sounds['warning'].play()
            groups.boss[idx].add(cls(
                random.randint(200, WIDTH - 100),
                random.randint(-HEIGHT, -100),
                assets.bosses[key],
            ))
            groups.boss_state.spawned[idx] = True

    # --- extra score coins ---
    if random.randint(0, 60) == 0:
        img = assets.refills['extra_score']
        groups.extra_score.add(ExtraScore(
            random.randint(50, WIDTH - 50),
            random.randint(-HEIGHT, -50 - img.get_rect().height),
            img,
        ))

    # --- diagonal meteors (score > 3000) ---
    if score > 3000 and random.randint(0, 100) == 0:
        img = random.choice(assets.meteors['meteor1'])
        groups.meteors.add(Meteors(
            random.randint(0, 50),
            random.randint(0, 50),
            img,
        ))

    # --- vertical meteors (always) ---
    if random.randint(0, 90) == 0:
        img = random.choice(assets.meteors['meteor2'])
        groups.meteors2.add(Meteors2(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50 - img.get_rect().height),
            img,
        ))

    # --- black holes (score > 1000) ---
    if score > 1000 and random.randint(0, 500) == 0:
        img = random.choice(assets.black_holes)
        groups.black_holes.add(BlackHole(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50 - img.get_rect().height),
            img,
        ))
