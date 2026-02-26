"""Drawing / rendering — all visual output lives here, no game logic."""
from dataclasses import dataclass, field
from typing import List

import pygame

from .constants import WIDTH, HEIGHT


# ---------------------------------------------------------------------------
#  Background state & rendering
# ---------------------------------------------------------------------------

@dataclass
class BackgroundState:
    """Encapsulates scrolling-background state (images, position, tier)."""

    images: List[pygame.Surface] = field(repr=False)
    y: int = 0
    current: pygame.Surface = field(default=None, repr=False)
    upgraded: bool = False

    # -- factory --

    @classmethod
    def create(cls, images: List[pygame.Surface]) -> "BackgroundState":
        """Build an initial state from the four background images."""
        return cls(
            images=images,
            y=-HEIGHT,
            current=images[0],
            upgraded=False,
        )

    # -- logic: scroll position & tier selection (score-driven) --

    def update(self, score: int) -> None:
        """Advance scroll position and pick the current background tier."""
        self.y += 2 if score > 3000 else 1
        if self.y >= 0:
            self.y = -HEIGHT

        if score >= 15000:
            self.current = self.images[3]
        elif score >= 10000:
            self.current = self.images[2]
        elif score >= 3000 and not self.upgraded:
            self.current = self.images[1]
            self.upgraded = True
        elif score == 0:
            self.current = self.images[0]
            self.upgraded = False

    def reset(self) -> None:
        """Reset to the initial background (used on game-over)."""
        self.current = self.images[0]
        self.upgraded = False
        self.y = -HEIGHT


# ---------------------------------------------------------------------------
#  Individual draw helpers
# ---------------------------------------------------------------------------

def draw_background(screen: pygame.Surface, bg: BackgroundState) -> None:
    """Blit the tiled scrolling background."""
    screen.blit(bg.current, (0, bg.y))
    top = bg.current.copy()
    screen.blit(top, top.get_rect(topleft=(0, bg.y + HEIGHT)))


def draw_pause(screen: pygame.Surface) -> None:
    """Render the PAUSE overlay text."""
    font = pygame.font.SysFont("Comic Sans MS", 40)
    text = font.render("PAUSE", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))


# ---------------------------------------------------------------------------
#  Full game-world renderer
# ---------------------------------------------------------------------------

def draw_game_world(screen, groups, player) -> int:
    """Draw every game entity onto *screen* and return bullets-consumed count.

    The returned ``ammo_consumed`` is the number of player bullets that flew
    off the top of the screen this frame (must be subtracted from the ammo
    counter by the caller).

    Draw order (bottom → top):
        refills → black holes → meteors → enemy1 → enemy2 + bullets →
        bosses + bullets + health bars → player → explosions → player bullets
    """
    # --- refills / pickups ---
    for grp in (groups.bullet_refill, groups.health_refill,
                groups.double_refill, groups.extra_score):
        grp.draw(screen)

    # --- black holes ---
    groups.black_holes.draw(screen)

    # --- meteors ---
    groups.meteors.draw(screen)
    groups.meteors2.draw(screen)

    # --- enemy1 ---
    groups.enemy1.draw(screen)

    # --- enemy2 + enemy bullets ---
    groups.enemy2.draw(screen)
    groups.enemy2_bullets.draw(screen)

    # --- bosses + boss bullets + health bars ---
    bstate = groups.boss_state
    for i in range(3):
        boss_grp = groups.boss[i]
        groups.boss_bullets[i].draw(screen)
        boss_grp.draw(screen)

        if boss_grp:
            obj = boss_grp.sprites()[0]
            bar = bstate.bar_rects[i]
            bar.center = (obj.rect.centerx, obj.rect.top - 5)
            pygame.draw.rect(screen, (255, 0, 0), bar)
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (bar.left, bar.top, max(0, bstate.health[i]), bar.height),
            )

    # --- player ---
    screen.blit(player.image.copy(), player.rect)

    # --- explosions ---
    for expl in groups.explosions:
        expl.update()
        screen.blit(expl.image, expl.rect)

    for expl in groups.explosions2:
        expl.update()
        screen.blit(expl.image, expl.rect)

    # --- player bullets ---
    ammo_consumed = 0
    for bullet in groups.bullets:
        bullet.update()
        screen.blit(bullet.image, bullet.rect)
        if bullet.rect.bottom < 0:
            bullet.kill()
            ammo_consumed += 1

    return ammo_consumed
