"""Player input helpers."""
import pygame

JOYSTICK_DEAD_ZONE = 0.1


def get_movement_input(keys, joystick=None):
    """Return (x_input, y_input) from keyboard and optional joystick.

    Keyboard produces integer -1/0/+1; joystick produces floats in [-1, 1]
    and overrides the keyboard axis when outside the dead zone.
    The caller multiplies these by the player speed to move the sprite.
    """
    x_input = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    y_input = keys[pygame.K_DOWN]  - keys[pygame.K_UP]

    if joystick is not None:
        ax = joystick.get_axis(0)
        ay = joystick.get_axis(1)
        if abs(ax) > JOYSTICK_DEAD_ZONE:
            x_input = ax
        if abs(ay) > JOYSTICK_DEAD_ZONE:
            y_input = ay

    return x_input, y_input
