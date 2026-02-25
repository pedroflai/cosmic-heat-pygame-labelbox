import pygame
from classes.constants import WIDTH, HEIGHT
from classes.display import get_screen
from classes import sound


def music_background():
    sound.load_music('game_sounds/background_music.mp3')
    sound.set_music_volume(0.25)
    sound.play_music(loops=-1)


def show_game_over(score):
    screen = get_screen()
    font = pygame.font.SysFont('Impact', 50)
    font_small = pygame.font.SysFont('Impact', 30)
    text = font.render("GAME OVER", True, (139, 0, 0))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
    score_text = font_small.render(f"Final Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()
    sound.load_music('game_sounds/gameover.mp3')
    sound.play_music()
    pygame.time.delay(4000)
    music_background()


def show_game_win():
    screen = get_screen()
    font = pygame.font.SysFont('Impact', 50)
    text = font.render("AWESOME! GO ON!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    sound.load_music('game_sounds/win.mp3')
    sound.play_music()
    pygame.time.delay(1000)
    music_background()
