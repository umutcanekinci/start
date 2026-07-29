import pygame

from pygamine import GameObject


class Cursor(GameObject):
    def __init__(self):
        super().__init__()
        self._frame = 0

        self._normal = [pygame.image.load(f"assets/images/cursor/normal/N-{i}.png") for i in range(17)]
        self._click  = [pygame.image.load(f"assets/images/cursor/click/L-{i}.png") for i in range(8)]
        self._click2 = [pygame.image.load(f"assets/images/cursor/click2/L2-{i}.png") for i in range(13)]
        self._state  = self._normal
        self.rect.size = self._normal[0].get_size()

    def draw(self, surface) -> None:
        if self._frame >= len(self._state):
            self._frame = 0
        surface.blit(self._state[self._frame], self.rect)
        self._frame += 1