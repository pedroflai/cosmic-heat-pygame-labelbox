import pygame

from .constants import WIDTH, HEIGHT


class Player:

    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 100, 100, 100)
        self.speed = 10
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.original_image = self.image.copy()
        self.direction = 'down'

    def move(self, x_input, y_input):
        """Move the player by (x_input, y_input) scaled by speed.

        x_input / y_input are -1..+1 (keyboard) or floats from a joystick.
        Handles screen-edge clamping and left/right sprite flip.
        """
        if x_input:
            self.rect.x = max(0, min(WIDTH - self.rect.width,
                                     self.rect.x + int(x_input * self.speed)))
            if x_input < 0:
                self.image = pygame.transform.flip(self.original_image, True, False)
            else:
                self.image = self.original_image
        if y_input:
            self.rect.y = max(0, min(HEIGHT - self.rect.height,
                                     self.rect.y + int(y_input * self.speed)))
