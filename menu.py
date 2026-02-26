import sys
import random

import pygame

from classes.constants import WIDTH, HEIGHT, BLACK, WHITE, RED
from classes.display import get_screen
from classes import controls
from classes import sound
from classes.assets import get_assets


def animate_screen():
    screen = get_screen()
    for i in range(0, 20):
        screen.blit(mainmenu_img, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
        screen.blit(mainmenu_img, (random.randint(-5, 5), random.randint(-5, 5)))
        pygame.display.flip()
        pygame.time.wait(10)


# Use pre-loaded assets (loaded in main.py before this module is imported)
_assets = get_assets()
mainmenu_img = _assets.menu['background']
logo_img = _assets.menu['logo']
explosion_sound = _assets.sounds['menu_explosion']

screen = get_screen()

sound.load_music('game_sounds/menu.mp3')
sound.set_music_volume(0.25)
sound.play_music(-1)

clock = pygame.time.Clock()

logo_x = (WIDTH - logo_img.get_width()) // 2
logo_y = 50

play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 205, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 205, 50)

selected_button = 0
show_menu = True


def main():
    global show_menu, selected_button
    show_menu = True
    screen = get_screen()

    while show_menu:
        events = pygame.event.get()
        controls.update(events)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_button_rect.collidepoint(x, y):
                    explosion_sound.play()
                    animate_screen()
                    show_menu = False
                    import gameplay
                    gameplay.main()
                    return
                elif quit_button_rect.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

        if controls.action_pressed("up"):
            selected_button = 0
        elif controls.action_pressed("down"):
            selected_button = 1

        if controls.action_pressed("shoot"):
            if selected_button == 0:
                explosion_sound.play()
                animate_screen()
                show_menu = False
                screen.fill(BLACK)
                import gameplay
                gameplay.main()
                return
            elif selected_button == 1:
                pygame.quit()
                sys.exit()

        screen.blit(mainmenu_img, (0, 0))

        screen.blit(logo_img, (logo_x, logo_y))

        font = pygame.font.SysFont('Comic Sans MS', 40)
        text = font.render("Play", True, WHITE)
        pygame.draw.rect(screen, BLACK, play_button_rect, border_radius=10)
        if selected_button == 0:
            pygame.draw.rect(screen, RED, play_button_rect, border_radius=10, width=4)
        text_rect = text.get_rect()
        text_rect.center = play_button_rect.center
        screen.blit(text, text_rect)
        text = font.render("Exit", True, WHITE)
        pygame.draw.rect(screen, BLACK, quit_button_rect, border_radius=10)
        if selected_button == 1:
            pygame.draw.rect(screen, RED, quit_button_rect, border_radius=10, width=4)
        text_rect = text.get_rect()
        text_rect.center = quit_button_rect.center
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pygame.quit()
