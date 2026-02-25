"""Centralized display module for single window initialization."""
import pygame
from classes.constants import WIDTH, HEIGHT

_screen = None


def init_display():
    """Initialize pygame and create the game window. Should be called once at startup."""
    global _screen
    if _screen is None:
        pygame.init()
        _screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cosmic Heat")
    return _screen


def get_screen():
    """Get the shared screen surface. Raises error if not initialized."""
    if _screen is None:
        raise RuntimeError("Display not initialized. Call init_display() first.")
    return _screen
