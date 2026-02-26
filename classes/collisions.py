"""Collision & update logic — generic functions that read entity class attributes."""
import random

import pygame

from .constants import WIDTH, HEIGHT
from .explosions import Explosion, Explosion2
from .refill import BulletRefill, HealthRefill, DoubleRefill


# ---------------------------------------------------------------------------
#  Speed scaling table (shared by meteors, extra_score, black holes)
# ---------------------------------------------------------------------------

_SPEED_TIERS = [
    (20000, 10),
    (15000, 8),
    (10000, 6),
    (3000,  4),
]


def _scale_speed(sprite, score):
    """Set sprite.speed based on the current score."""
    for threshold, spd in _SPEED_TIERS:
        if score >= threshold:
            sprite.speed = spd
            return


# ---------------------------------------------------------------------------
#  Refill / pickup processing
# ---------------------------------------------------------------------------

def process_refills(groups, player, score):
    """Update all refills & check collisions; return (life_delta, ammo_delta, score_delta)."""
    life_d = ammo_d = score_d = 0

    for group in (groups.bullet_refill, groups.health_refill,
                  groups.double_refill, groups.extra_score):
        for sprite in group:
            sprite.update()

            if player.rect.colliderect(sprite.rect):
                if sprite.health_restore and life_d + 200 > 0:
                    life_d += sprite.health_restore
                if sprite.ammo_restore and ammo_d + 200 > 0:
                    ammo_d += sprite.ammo_restore
                score_d += sprite.score_bonus
                sprite.sound_effect.play()
                sprite.kill()

            # extra_score and similar hazards speed up with score
            _scale_speed(sprite, score)

    return life_d, ammo_d, score_d


# ---------------------------------------------------------------------------
#  Black holes
# ---------------------------------------------------------------------------

def process_black_holes(groups, player, score):
    """Update black holes & check collisions; return life_delta."""
    life_d = 0
    for obj in groups.black_holes:
        obj.update()
        if obj.rect.colliderect(player.rect):
            life_d -= 1
            obj.sound_effect.play()
        _scale_speed(obj, score)
    return life_d


# ---------------------------------------------------------------------------
#  Meteors (type 1 & 2) — generic hazard with bullet-killable sprites
# ---------------------------------------------------------------------------

def process_hazard_group(group, groups, player, assets, score):
    """Update & handle collisions for a meteor/hazard group.

    Each sprite in *group* must have class attrs:
        contact_damage, score_on_contact, score_on_kill, drop_chance
    Returns (life_delta, score_delta).
    """
    life_d = score_d = 0
    expl_imgs = assets.explosions['explosion1']
    drop_img = assets.refills['double']

    for obj in list(group):
        obj.update()

        # player collision → damage + explosion + kill
        if obj.rect.colliderect(player.rect):
            life_d -= obj.contact_damage
            groups.explosions.add(Explosion(obj.rect.center, expl_imgs))
            obj.kill()
            score_d += obj.score_on_contact
            continue

        # bullet collision → explosion + kill + optional drop
        hits = pygame.sprite.spritecollide(obj, groups.bullets, True)
        for _ in hits:
            groups.explosions.add(Explosion(obj.rect.center, expl_imgs))
            obj.kill()
            score_d += obj.score_on_kill
            if random.randint(0, obj.drop_chance) == 0:
                groups.double_refill.add(DoubleRefill(
                    obj.rect.centerx, obj.rect.centery, drop_img))
            break  # sprite is dead after first hit

        _scale_speed(obj, score)

    return life_d, score_d


# ---------------------------------------------------------------------------
#  Enemy1 — bouncing enemies (same pattern as hazards but different update)
# ---------------------------------------------------------------------------

def process_enemy1(groups, player, assets):
    """Update & process collisions for Enemy1 group.

    Returns (life_delta, score_delta).
    """
    life_d = score_d = 0
    expl_imgs = assets.explosions['explosion1']
    bullet_img = assets.refills['bullet']
    health_img = assets.refills['health']

    for obj in list(groups.enemy1):
        obj.update(groups.enemy1)

    for obj in list(groups.enemy1):
        if obj.rect.colliderect(player.rect):
            life_d -= obj.contact_damage
            groups.explosions.add(Explosion(obj.rect.center, expl_imgs))
            obj.kill()
            score_d += obj.score_on_contact
            continue

        hits = pygame.sprite.spritecollide(obj, groups.bullets, True)
        for _ in hits:
            groups.explosions.add(Explosion(obj.rect.center, expl_imgs))
            obj.kill()
            score_d += obj.score_on_kill

            if random.randint(0, obj.drop_chance_bullet) == 0:
                groups.bullet_refill.add(BulletRefill(
                    obj.rect.centerx, obj.rect.centery, bullet_img))
            if random.randint(0, obj.drop_chance_health) == 0:
                groups.health_refill.add(HealthRefill(
                    random.randint(50, WIDTH - 30),
                    random.randint(-HEIGHT, -30),
                    health_img))
            break

    return life_d, score_d


# ---------------------------------------------------------------------------
#  Enemy2 — shooting enemy
# ---------------------------------------------------------------------------

def process_enemy2(groups, player, assets):
    """Update enemy2 + their bullets, handle collisions.

    Returns (life_delta, score_delta).
    """
    life_d = score_d = 0
    expl_imgs = assets.explosions['explosion2']
    expl3_imgs = assets.explosions['explosion3']
    drop_img = assets.refills['double']

    for obj in list(groups.enemy2):
        obj.update(groups.enemy2, groups.enemy2_bullets, player)

    groups.enemy2_bullets.update()

    for obj in list(groups.enemy2):
        if obj.rect.colliderect(player.rect):
            life_d -= obj.contact_damage
            groups.explosions2.add(Explosion2(obj.rect.center, expl_imgs))
            obj.kill()
            score_d += obj.score_on_contact
            continue

        hits = pygame.sprite.spritecollide(obj, groups.bullets, True)
        for _ in hits:
            groups.explosions2.add(Explosion2(obj.rect.center, expl_imgs))
            obj.kill()
            score_d += obj.score_on_kill
            if random.randint(0, obj.drop_chance) == 0:
                groups.double_refill.add(DoubleRefill(
                    obj.rect.centerx, obj.rect.centery, drop_img))
            break

    # enemy bullets hitting player
    for bullet in list(groups.enemy2_bullets):
        if bullet.rect.colliderect(player.rect):
            life_d -= 10  # Enemy2.bullet_damage
            groups.explosions.add(Explosion(player.rect.center, expl3_imgs))
            bullet.kill()

    return life_d, score_d


# ---------------------------------------------------------------------------
#  Boss (generic for boss index 0/1/2)
# ---------------------------------------------------------------------------

def process_boss(idx, groups, player, assets):
    """Update boss[idx] + their bullets, handle collisions.

    Returns (life_delta, score_delta).
    """
    boss_group = groups.boss[idx]
    bullet_group = groups.boss_bullets[idx]
    bstate = groups.boss_state
    life_d = score_d = 0

    if not boss_group:
        return life_d, score_d

    expl_imgs = assets.explosions['explosion2']
    expl3_imgs = assets.explosions['explosion3']
    drop_img = assets.refills['double']

    for obj in list(boss_group):
        obj.update(bullet_group, player)

    bullet_group.update()

    for obj in list(boss_group):
        # contact damage (doesn't kill the boss)
        if obj.rect.colliderect(player.rect):
            life_d -= obj.contact_damage
            groups.explosions2.add(Explosion2(obj.rect.center, expl_imgs))

        # player bullets hitting boss
        hits = pygame.sprite.spritecollide(obj, groups.bullets, True)
        for _ in hits:
            groups.explosions2.add(Explosion2(obj.rect.center, expl_imgs))
            bstate.health[idx] -= obj.hp_per_bullet

            if bstate.health[idx] <= 0:
                groups.explosions.add(Explosion(obj.rect.center, expl3_imgs))
                obj.kill()
                score_d += obj.score_on_kill
                if random.randint(0, obj.drop_chance) == 0:
                    groups.double_refill.add(DoubleRefill(
                        obj.rect.centerx, obj.rect.centery, drop_img))
                break

        # boss cleanup when health reaches zero outside bullet loop
        if bstate.health[idx] <= 0 and obj.alive():
            groups.explosions2.add(Explosion2(obj.rect.center, expl_imgs))
            obj.kill()

    # boss bullets hitting player
    for bullet in list(bullet_group):
        if bullet.rect.colliderect(player.rect):
            # Use the boss class bullet_damage (get from first sprite or use stored ref)
            life_d -= 20  # all bosses currently deal 20 bullet damage
            groups.explosions.add(Explosion(player.rect.center, expl3_imgs))
            bullet.kill()

    return life_d, score_d
