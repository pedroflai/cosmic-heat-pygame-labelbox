"""UI helpers: HUD drawing, game-over screen, win screen, background music."""
import pygame

from .constants import WIDTH, HEIGHT
from .display import get_screen
from . import sound


def music_background():
    """Load and play the background music loop."""
    sound.load_music('game_sounds/background_music.mp3')
    sound.set_music_volume(0.25)
    sound.play_music(loops=-1)


def show_game_over(score):
    """Display the GAME OVER splash and wait before returning."""
    screen = get_screen()
    font = pygame.font.SysFont('Impact', 50)
    font_small = pygame.font.SysFont('Impact', 30)
    text = font.render("GAME OVER", True, (139, 0, 0))
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
    score_text = font_small.render(f"Final Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()
    sound.load_music('game_sounds/gameover.mp3')
    sound.play_music()
    pygame.time.delay(4000)
    music_background()


def show_game_win():
    """Display the WIN splash and wait before returning."""
    screen = get_screen()
    font = pygame.font.SysFont('Impact', 50)
    text = font.render("AWESOME! GO ON!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    sound.load_music('game_sounds/win.mp3')
    sound.play_music()
    pygame.time.delay(1000)
    music_background()


def draw_hud(screen, player_life, bullet_counter, score, hi_score,
             life_bar_image, bullet_bar_image, extra_score_img):
    """Draw the heads-up display (life bar, bullet bar, score, hi-score)."""

    # --- Life bar ---
    player_life_surface = pygame.Surface((200, 25), pygame.SRCALPHA, 32)
    player_life_surface.set_alpha(216)

    player_life_bar_width = int(player_life / 200 * 200)
    player_life_bar_width = max(0, min(player_life_bar_width, 200))

    player_life_bar = pygame.Surface((player_life_bar_width, 30), pygame.SRCALPHA, 32)
    player_life_bar.set_alpha(216)

    if player_life > 50:
        player_life_bar.fill((152, 251, 152))
    else:
        player_life_bar.fill((0, 0, 0))

    player_life_surface.blit(life_bar_image, (0, 0))
    player_life_surface.blit(player_life_bar, (35, 0))
    screen.blit(player_life_surface, (10, 10))

    # --- Bullet bar ---
    bullet_counter_surface = pygame.Surface((200, 25), pygame.SRCALPHA, 32)
    bullet_counter_surface.set_alpha(216)
    bullet_counter_bar = pygame.Surface(((bullet_counter / 200) * 200, 30), pygame.SRCALPHA, 32)
    bullet_counter_bar.set_alpha(216)
    if bullet_counter > 50:
        bullet_counter_bar.fill((255, 23, 23))
    else:
        bullet_counter_bar.fill((0, 0, 0))
    bullet_counter_surface.blit(bullet_bar_image, (0, 0))
    bullet_counter_surface.blit(bullet_counter_bar, (35, 0))
    bullet_y_pos = player_life_surface.get_height() + 20
    screen.blit(bullet_counter_surface, (10, bullet_y_pos))

    # --- Score ---
    score_surface = pygame.font.SysFont('Comic Sans MS', 30).render(
        f'{score}', True, (238, 232, 170))
    score_image_rect = score_surface.get_rect()
    score_image_rect.x = WIDTH - score_image_rect.width - extra_score_img.get_width() - 10
    score_image_rect.y = 10
    screen.blit(extra_score_img, (
        score_image_rect.right + 5,
        score_image_rect.centery - extra_score_img.get_height() // 2))
    screen.blit(score_surface, score_image_rect)

    # --- Hi-score ---
    hi_score_surface = pygame.font.SysFont('Comic Sans MS', 20).render(
        f'HI-SCORE: {hi_score}', True, (255, 255, 255))
    hi_score_surface.set_alpha(128)
    hi_score_x_pos = (screen.get_width() - hi_score_surface.get_width()) // 2
    screen.blit(hi_score_surface, (hi_score_x_pos, 0))
