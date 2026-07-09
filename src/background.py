import random

import pygame

_LAYERS_DIR    = "assets/images/bg_layers"
_SKY_FILE      = f"{_LAYERS_DIR}/parallax-mountain-bg.png"
_HORIZON_FILES = [
    f"{_LAYERS_DIR}/parallax-mountain-montain-far.png",
    f"{_LAYERS_DIR}/parallax-mountain-mountains.png",
    f"{_LAYERS_DIR}/parallax-mountain-trees.png",
    f"{_LAYERS_DIR}/parallax-mountain-foreground-trees.png",
]
_HORIZON_HEIGHT = 300  # on-screen height of the stacked mountain/tree layers


class ParallaxBackground:
    """Static backdrop baked from layered mountain art, re-randomized per round.

    The map never scrolls, so there's no camera offset to animate -- the
    whole stack is pre-blitted into one surface once, and randomize() just
    re-bakes it with a fresh horizontal phase per layer so repeat rounds
    don't look identical.
    """

    def __init__(self, window_w: int, window_h: int):
        self._window_w = window_w
        self._window_h = window_h
        self._sky = pygame.transform.scale(
            pygame.image.load(_SKY_FILE).convert_alpha(), (window_w, window_h)
        )
        self._horizon_layers = [self._load_layer(path) for path in _HORIZON_FILES]
        self.surface = pygame.Surface((window_w, window_h)).convert()
        self.randomize()

    @staticmethod
    def _load_layer(path: str) -> pygame.Surface:
        img   = pygame.image.load(path).convert_alpha()
        scale = _HORIZON_HEIGHT / img.get_height()
        return pygame.transform.scale(img, (int(img.get_width() * scale), _HORIZON_HEIGHT))

    def randomize(self) -> None:
        self.surface.blit(self._sky, (0, 0))
        y = self._window_h - _HORIZON_HEIGHT
        for layer in self._horizon_layers:
            w = layer.get_width()
            x = -random.randint(0, w - 1)
            while x < self._window_w:
                self.surface.blit(layer, (x, y))
                x += w
