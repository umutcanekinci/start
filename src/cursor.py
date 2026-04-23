import pygame

class Cursor:
    def __init__(self):
        self._frame = 0
        self._normal = [pygame.image.load(f"res/images/cursor/normal/N-{i}.png") for i in range(17)]
        self._click = [pygame.image.load(f"res/images/cursor/click/L-{i}.png") for i in range(8)]
        self._click2 = [pygame.image.load(f"res/images/cursor/click2/L2-{i}.png") for i in range(13)]
        self._state = self._normal

    def draw(self, surface, pos):
            if self._frame >= len(self._state):
                self._frame = 0
            surface.blit(self._state[self._frame], pos)
            self._frame += 1