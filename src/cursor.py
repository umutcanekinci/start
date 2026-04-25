import pygame

class Cursor:
    def __init__(self):
        self._frame = 0
        self._pos   = (0, 0)
        self._normal = [pygame.image.load(f"res/images/cursor/normal/N-{i}.png") for i in range(17)]
        self._click  = [pygame.image.load(f"res/images/cursor/click/L-{i}.png") for i in range(8)]
        self._click2 = [pygame.image.load(f"res/images/cursor/click2/L2-{i}.png") for i in range(13)]
        self._state  = self._normal

    def set_position(self, pos) -> None:
        self._pos = pos

    def draw(self, surface) -> None:
        if self._frame >= len(self._state):
            self._frame = 0
        surface.blit(self._state[self._frame], self._pos)
        self._frame += 1