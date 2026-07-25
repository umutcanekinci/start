"""Shared pytest setup and fixtures for hunted's app-level test suite.

Run from the repo root (`uv run pytest`, matching how __main__.py assumes
cwd == repo root for its own "assets/..."-relative paths).
"""

import os

# Dummy SDL drivers so pygame can run headless (e.g. in CI) without opening a
# real window or probing for a sound device. Must be set before pygame is
# imported anywhere.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest

from world import GameWorld

pygame.init()
# Platform loads its tile via convert_alpha(), which raises without a
# display surface. Application.__init__ normally provides one; these tests
# construct game objects directly, with no Application/Game involved, so
# they need their own.
pygame.display.set_mode((1, 1))


class FakeInputHandler:
    """Settable stand-in for input_handler.InputHandler (a runtime_checkable
    Protocol -- any object with these four methods satisfies it)."""

    def __init__(self):
        self.control = "test"
        self.right = False
        self.left = False
        self.jump = False
        self.fire = False

    def is_moving_right(self) -> bool:
        return self.right

    def is_moving_left(self) -> bool:
        return self.left

    def is_jump_pressed(self) -> bool:
        return self.jump

    def is_fire_pressed(self) -> bool:
        return self.fire


@pytest.fixture
def input_handler() -> FakeInputHandler:
    return FakeInputHandler()


@pytest.fixture
def world() -> GameWorld:
    return GameWorld(window_w=800, window_h=600)
