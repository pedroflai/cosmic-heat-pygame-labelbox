"""Asset loading and management — all images and sounds loaded once at startup."""
import pygame

from .constants import WIDTH, HEIGHT
from . import sound


class GameAssets:
    """Centralized asset storage loaded once at startup."""

    def __init__(self):
        # Backgrounds
        self.backgrounds = {}

        # Explosion animation frames
        self.explosions = {}

        # Enemy & boss images
        self.enemies = {}
        self.bosses = {}

        # Powerups & refills
        self.refills = {}

        # Environmental hazards
        self.meteors = {}
        self.black_holes = []

        # UI elements
        self.ui = {}

        # Menu assets
        self.menu = {}

        # Sound effects
        self.sounds = {}

    def load_all(self, screen=None):
        """Load all game assets. Pass screen to show loading progress."""
        steps = [
            ("Loading backgrounds...", self._load_backgrounds),
            ("Loading explosions...", self._load_explosions),
            ("Loading enemies...", self._load_enemies),
            ("Loading bosses...", self._load_bosses),
            ("Loading powerups...", self._load_refills),
            ("Loading meteors...", self._load_meteors),
            ("Loading UI...", self._load_ui),
            ("Loading menu...", self._load_menu),
            ("Loading sounds...", self._load_sounds),
        ]
        for message, loader in steps:
            if screen:
                self._show_loading(screen, message)
            loader()

        if screen:
            self._show_loading(screen, "Ready!")
            pygame.time.delay(300)

    # ---- loading screen ----

    def _show_loading(self, screen, message):
        """Display a loading message on a black screen."""
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('Arial', 30)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(80)

    # ---- private loaders ----

    def _load_backgrounds(self):
        self.backgrounds['bg1'] = pygame.image.load('images/bg/background.jpg').convert()
        self.backgrounds['bg2'] = pygame.image.load('images/bg/background2.png').convert()
        self.backgrounds['bg3'] = pygame.image.load('images/bg/background3.png').convert()
        self.backgrounds['bg4'] = pygame.image.load('images/bg/background4.png').convert()

    def _load_explosions(self):
        self.explosions['explosion1'] = [
            pygame.image.load(f"images/explosion/explosion{i}.png") for i in range(8)
        ]
        self.explosions['explosion2'] = [
            pygame.image.load(f"images/explosion2/explosion{i}.png") for i in range(18)
        ]
        self.explosions['explosion3'] = [
            pygame.image.load(f"images/explosion3/explosion{i}.png") for i in range(18)
        ]

    def _load_enemies(self):
        self.enemies['enemy1'] = [
            pygame.image.load('images/enemy/enemy1_1.png').convert_alpha(),
            pygame.image.load('images/enemy/enemy1_2.png').convert_alpha(),
            pygame.image.load('images/enemy/enemy1_3.png').convert_alpha(),
        ]
        self.enemies['enemy2'] = [
            pygame.image.load('images/enemy/enemy2_1.png').convert_alpha(),
            pygame.image.load('images/enemy/enemy2_2.png').convert_alpha(),
        ]

    def _load_bosses(self):
        self.bosses['boss1'] = pygame.image.load('images/boss/boss1.png').convert_alpha()
        self.bosses['boss2'] = pygame.image.load('images/boss/boss2_1.png').convert_alpha()
        self.bosses['boss3'] = pygame.image.load('images/boss/boss3.png').convert_alpha()

    def _load_refills(self):
        self.refills['health'] = pygame.image.load('images/refill/health_refill.png').convert_alpha()
        self.refills['bullet'] = pygame.image.load('images/refill/bullet_refill.png').convert_alpha()
        self.refills['double'] = pygame.image.load('images/refill/double_refill.png').convert_alpha()
        self.refills['extra_score'] = pygame.image.load('images/score/score_coin.png').convert_alpha()

    def _load_meteors(self):
        self.meteors['meteor1'] = [
            pygame.image.load('images/meteors/meteor_1.png').convert_alpha(),
            pygame.image.load('images/meteors/meteor_2.png').convert_alpha(),
            pygame.image.load('images/meteors/meteor_3.png').convert_alpha(),
            pygame.image.load('images/meteors/meteor_4.png').convert_alpha(),
        ]
        self.meteors['meteor2'] = [
            pygame.image.load('images/meteors/meteor2_1.png').convert_alpha(),
            pygame.image.load('images/meteors/meteor2_2.png').convert_alpha(),
            pygame.image.load('images/meteors/meteor2_3.png').convert_alpha(),
            pygame.image.load('images/meteors/meteor2_4.png').convert_alpha(),
        ]
        self.black_holes = [
            pygame.image.load('images/hole/black_hole.png').convert_alpha(),
            pygame.image.load('images/hole/black_hole2.png').convert_alpha(),
        ]

    def _load_ui(self):
        self.ui['life_bar'] = pygame.image.load("images/life_bar.png").convert_alpha()
        self.ui['bullet_bar'] = pygame.image.load("images/bullet_bar.png").convert_alpha()

    def _load_menu(self):
        img = pygame.image.load('images/mainmenu.jpg').convert()
        self.menu['background'] = pygame.transform.scale(img, (WIDTH, HEIGHT))
        self.menu['logo'] = pygame.image.load('images/ch.png').convert_alpha()

    def _load_sounds(self):
        self.sounds['warning'] = sound.load_sound('game_sounds/warning.mp3')
        self.sounds['menu_explosion'] = sound.load_sound('game_sounds/explosions/explosion1.wav')
        self.sounds['menu_explosion'].set_volume(0.25)


# ---- singleton access ----

_assets = None


def get_assets():
    """Get the global GameAssets instance (must be loaded first)."""
    global _assets
    if _assets is None:
        _assets = GameAssets()
    return _assets


def load_all_assets(screen=None):
    """Load every asset at startup with optional loading screen."""
    assets = get_assets()
    assets.load_all(screen)
    return assets
