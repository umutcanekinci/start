from typing import Protocol, runtime_checkable

import pygame


@runtime_checkable
class InputHandler(Protocol):
    def is_moving_right(self) -> bool: ...
    def is_moving_left(self) -> bool: ...
    def is_jump_pressed(self) -> bool: ...
    def is_fire_pressed(self) -> bool: ...


class KeyboardInputHandler:
    def __init__(self, control: str):
        self.control = control

    def is_moving_right(self) -> bool:
        keys = pygame.key.get_pressed()
        return (
            (self.control in ("R", "RL") and keys[pygame.K_RIGHT]) or
            (self.control in ("L", "RL") and keys[ord('d')])
        )

    def is_moving_left(self) -> bool:
        keys = pygame.key.get_pressed()
        return (
            (self.control in ("R", "RL") and keys[pygame.K_LEFT]) or
            (self.control in ("L", "RL") and keys[ord('a')])
        )

    def is_jump_pressed(self) -> bool:
        keys = pygame.key.get_pressed()
        return (
            (self.control in ("R", "RL") and keys[pygame.K_UP]) or
            (self.control in ("L", "RL") and keys[pygame.K_w])
        )

    def is_fire_pressed(self) -> bool:
        keys = pygame.key.get_pressed()
        arrows = self.control in ("R", "RL")
        wasd   = self.control in ("L", "RL")
        return (
            (arrows and (keys[pygame.K_RCTRL] or keys[pygame.K_SPACE])) or
            (wasd   and  keys[pygame.K_SPACE])
        )