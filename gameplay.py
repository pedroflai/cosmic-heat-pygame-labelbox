"""Main gameplay loop — state machine, input, rendering."""
import sys

import pygame

from classes import controls
from classes.constants import WIDTH, HEIGHT, FPS, SHOOT_DELAY
from classes.display import get_screen
from classes import sound
from classes.ui import show_game_over, music_background, draw_hud
from classes.assets import get_assets
from classes.player import Player
from classes.bullets import Bullet
from classes.groups import GameGroups, State
from classes.spawner import spawn_tick
from classes.draw import BackgroundState, draw_background, draw_pause, draw_game_world
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

    # --- background ---
    bg_imgs = [assets.backgrounds[k] for k in ('bg1', 'bg2', 'bg3', 'bg4')]
    bg = BackgroundState.create(bg_imgs)

    # --- input ---
    last_shot_time = 0

    initial_pos = (WIDTH // 2, HEIGHT - 100)

    # ========================  GAME LOOP  ========================
    while running:

        # --- events ---
        events = pygame.event.get()
        controls.update(events)

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if controls.action_pressed("quit"):
            running = False

        if controls.action_pressed("pause"):
            if state == State.PLAYING:
                state = State.PAUSED
            elif state == State.PAUSED:
                state = State.PLAYING

        # --- paused ---
        if state == State.PAUSED:
            draw_pause(screen)
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
            bg.reset()
            state = State.PLAYING
            continue

        # --- movement ---
        x_in, y_in = controls.get_movement()
        player.move(x_in, y_in)

        # --- auto-fire ---
        now = pygame.time.get_ticks()
        if controls.action_holding("shoot") and bullet_counter > 0 and now - last_shot_time > SHOOT_DELAY:
            last_shot_time = now
            groups.bullets.add(Bullet(player.rect.centerx, player.rect.top))
            bullet_counter -= 1

        # --- background ---
        bg.update(score)
        draw_background(screen, bg)

        if score > hi_score:
            hi_score = score

        # --- spawning ---
        spawn_tick(score, groups, assets)

        # --- death check ---
        if player_life <= 0:
            state = State.GAME_OVER
            continue

        # --- collisions ---
        life_d, ammo_d, score_d = process_refills(groups, player, score)
        player_life = min(200, player_life + life_d)
        bullet_counter = min(200, bullet_counter + ammo_d)
        score += score_d

        player_life += process_black_holes(groups, player, score)

        ld, sd = process_hazard_group(groups.meteors, groups, player, assets, score)
        player_life += ld; score += sd

        ld, sd = process_hazard_group(groups.meteors2, groups, player, assets, score)
        player_life += ld; score += sd

        ld, sd = process_enemy1(groups, player, assets)
        player_life += ld; score += sd

        ld, sd = process_enemy2(groups, player, assets)
        player_life += ld; score += sd

        for i in range(3):
            ld, sd = process_boss(i, groups, player, assets)
            player_life += ld; score += sd

        # --- render world ---
        bullet_counter -= draw_game_world(screen, groups, player)

        # --- HUD ---
        draw_hud(screen, player_life, bullet_counter, score, hi_score,
                 assets.ui['life_bar'], assets.ui['bullet_bar'],
                 assets.refills['extra_score'])

        pygame.display.flip()
        clock.tick(FPS)

    sound.stop_music()
    pygame.quit()
