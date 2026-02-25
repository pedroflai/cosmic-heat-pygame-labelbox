"""Main gameplay loop — state machine, input, rendering."""
import sys

import pygame

from classes.controls import get_movement_input
from classes.constants import WIDTH, HEIGHT, FPS, SHOOT_DELAY
from classes.display import get_screen
from classes import sound
from classes.ui import show_game_over, music_background, draw_hud
from classes.assets import get_assets
from classes.player import Player
from classes.bullets import Bullet
from classes.groups import GameGroups, State
from classes.spawner import spawn_tick
from classes.collisions import (
    process_refills,
    process_black_holes,
    process_hazard_group,
    process_enemy1,
    process_enemy2,
    process_boss,
)


def main():
    """Run the core gameplay loop."""
    music_background()
    screen = get_screen()
    clock = pygame.time.Clock()
    assets = get_assets()

    # --- state ---
    groups = GameGroups()
    player = Player()
    score = 0
    hi_score = 0
    player_life = 200
    bullet_counter = 200
    state = State.PLAYING
    running = True

    # --- background scroll ---
    bg_imgs = [assets.backgrounds[k] for k in ('bg1', 'bg2', 'bg3', 'bg4')]
    bg_y = -HEIGHT
    bg_current = bg_imgs[0]
    bg_top = bg_imgs[0].copy()
    bg_upgraded = False

    # --- input ---
    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    is_shooting = False
    last_shot_time = 0

    initial_pos = (WIDTH // 2, HEIGHT - 100)

    # ========================  GAME LOOP  ========================
    while running:

        # --- events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_p, pygame.K_PAUSE):
                    if state == State.PLAYING:
                        state = State.PAUSED
                    elif state == State.PAUSED:
                        state = State.PLAYING
                elif event.key == pygame.K_SPACE and state == State.PLAYING:
                    is_shooting = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    is_shooting = False

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0 and state == State.PLAYING:
                    is_shooting = True
                elif event.button == 7:
                    if state == State.PLAYING:
                        state = State.PAUSED
                    elif state == State.PAUSED:
                        state = State.PLAYING

            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 0:
                    is_shooting = False

        # --- paused ---
        if state == State.PAUSED:
            font = pygame.font.SysFont('Comic Sans MS', 40)
            text = font.render("PAUSE", True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pygame.display.flip()
            clock.tick(FPS)
            continue

        # --- game over ---
        if state == State.GAME_OVER:
            show_game_over(score)
            groups.empty_all()
            score = 0
            player_life = 200
            bullet_counter = 200
            player.rect.topleft = initial_pos
            bg_current = bg_imgs[0]
            bg_top = bg_imgs[0].copy()
            bg_upgraded = False
            bg_y = -HEIGHT
            state = State.PLAYING
            is_shooting = False
            continue

        # --- movement ---
        keys = pygame.key.get_pressed()
        x_in, y_in = get_movement_input(keys, joystick)
        player.move(x_in, y_in)

        # --- auto-fire ---
        now = pygame.time.get_ticks()
        if is_shooting and bullet_counter > 0 and now - last_shot_time > SHOOT_DELAY:
            last_shot_time = now
            groups.bullets.add(Bullet(player.rect.centerx, player.rect.top))
            bullet_counter -= 1

        # --- background scroll ---
        bg_y += 2 if score > 3000 else 1
        if bg_y >= 0:
            bg_y = -HEIGHT

        if score >= 15000:
            bg_current = bg_imgs[3]
        elif score >= 10000:
            bg_current = bg_imgs[2]
        elif score >= 3000 and not bg_upgraded:
            bg_current = bg_imgs[1]
            bg_upgraded = True
        elif score == 0:
            bg_current = bg_imgs[0]
            bg_upgraded = False

        bg_top = bg_current.copy()
        screen.blit(bg_current, (0, bg_y))
        top_rect = bg_top.get_rect(topleft=(0, bg_y + HEIGHT))
        screen.blit(bg_top, top_rect)

        if score > hi_score:
            hi_score = score

        # --- spawning ---
        spawn_tick(score, groups, assets)

        # --- death check ---
        if player_life <= 0:
            state = State.GAME_OVER
            continue

        # --- collisions & drawing ---
        life_d, ammo_d, score_d = process_refills(groups, player, screen, score)
        player_life = min(200, player_life + life_d)
        bullet_counter = min(200, bullet_counter + ammo_d)
        score += score_d

        player_life += process_black_holes(groups, player, screen, score)

        ld, sd = process_hazard_group(groups.meteors, groups, player, screen, assets, score)
        player_life += ld; score += sd

        ld, sd = process_hazard_group(groups.meteors2, groups, player, screen, assets, score)
        player_life += ld; score += sd

        ld, sd = process_enemy1(groups, player, screen, assets)
        player_life += ld; score += sd

        ld, sd = process_enemy2(groups, player, screen, assets)
        player_life += ld; score += sd

        for i in range(3):
            ld, sd = process_boss(i, groups, player, screen, assets)
            player_life += ld; score += sd

        # --- render: player, explosions, bullets ---
        screen.blit(player.image.copy(), player.rect)

        for expl in groups.explosions:
            expl.update()
            screen.blit(expl.image, expl.rect)

        for expl in groups.explosions2:
            expl.update()
            screen.blit(expl.image, expl.rect)

        for bullet in groups.bullets:
            bullet.update()
            screen.blit(bullet.image, bullet.rect)
            if bullet.rect.bottom < 0:
                bullet.kill()
                bullet_counter -= 1

        # --- HUD ---
        draw_hud(screen, player_life, bullet_counter, score, hi_score,
                 assets.ui['life_bar'], assets.ui['bullet_bar'],
                 assets.refills['extra_score'])

        pygame.display.flip()
        clock.tick(FPS)

    sound.stop_music()
    pygame.quit()
