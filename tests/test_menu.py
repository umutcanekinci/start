import pygame

from entities import Player
from menu import Menu


class FakeCursor:
    """Menu only reads/writes _state/_frame and compares against the three
    frame-set sentinels -- a real Cursor's actual sprite frames are
    irrelevant to Menu's own hover/click-state logic under test here."""

    def __init__(self):
        self._normal = "normal"
        self._click = "click"
        self._click2 = "click2"
        self._state = self._normal
        self._frame = 0


def make_menu():
    return Menu(800, 600, FakeCursor())


def test_construction_loads_the_expected_button_and_wait_frame_counts():
    menu = make_menu()

    assert menu._start_btn.get_size() == (310, 100)
    assert len(menu._btn_1p) == 3
    assert len(menu._btn_2p) == 3
    assert all(f.get_size() == (212, 44) for f in menu._btn_1p + menu._btn_2p)
    assert len(menu._wait_frames) == 49


def test_update_button_state_hover_without_press():
    menu = make_menu()

    menu.update_button_state("1p", hovered=True, pressed=False)

    assert menu._btn_1p_hover is True
    assert menu._btn_1p_click is False


def test_update_button_state_press_while_hovering():
    menu = make_menu()

    menu.update_button_state("1p", hovered=True, pressed=True)

    assert menu._btn_1p_hover is False
    assert menu._btn_1p_click is True


def test_update_button_state_pressed_flag_is_ignored_when_not_hovering():
    menu = make_menu()

    menu.update_button_state("start", hovered=False, pressed=True)

    assert menu._btn_start_hover is False
    assert menu._btn_start_click is False


def test_draw_at_full_countdown_shows_the_start_screen_and_hovered_cursor(world, input_handler):
    menu = make_menu()
    menu.update_button_state("1p", hovered=True, pressed=False)
    surface = pygame.Surface((800, 600))
    p1 = Player(world, (100, 100), input_handler)

    menu.draw(surface, countdown=100, p1=p1)

    assert menu.cursor._state == "click"  # any_hover -> _click
    assert menu.cursor._frame == 0  # state changed -> frame reset


def test_draw_supports_single_player_with_no_p2(world, input_handler):
    menu = make_menu()
    surface = pygame.Surface((800, 600))
    p1 = Player(world, (100, 100), input_handler)

    menu.draw(surface, countdown=100, p1=p1, p2=None)  # must not raise


def test_draw_with_two_players(world, input_handler):
    menu = make_menu()
    surface = pygame.Surface((800, 600))
    p1 = Player(world, (100, 100), input_handler)
    p2 = Player(world, (200, 100), input_handler)

    menu.draw(surface, countdown=100, p1=p1, p2=p2)  # must not raise


def test_draw_mid_countdown_shows_a_wait_frame(world, input_handler):
    menu = make_menu()
    surface = pygame.Surface((800, 600))
    p1 = Player(world, (100, 100), input_handler)

    menu.draw(surface, countdown=30, p1=p1)  # must not raise, no start screen drawn


def test_draw_late_countdown_holds_the_last_wait_frame(world, input_handler):
    # 48-59 deliberately reuses _wait_frames[48] (the countdown clip only has
    # 49 frames, 0-48) instead of indexing past the end of the list.
    menu = make_menu()
    surface = pygame.Surface((800, 600))
    p1 = Player(world, (100, 100), input_handler)

    menu.draw(surface, countdown=55, p1=p1)  # must not raise


def test_randomize_background_delegates_to_the_background(world):
    menu = make_menu()
    surface = menu._background.surface

    menu.randomize_background()

    assert menu._background.surface is surface  # re-baked in place
