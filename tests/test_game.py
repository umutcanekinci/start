"""Game() pulls in the full asset tree (sprites, sounds, the parallax
background) -- constructing it is exactly what scripts/smoke_test.py already
does headlessly for CI, so it's safe to build once here too. `game` is
module-scoped for the same reason; every test sets its own `_state` (and any
other precondition it needs) before acting, so sharing the instance across
tests in this file is safe -- exactly the pattern scripts/smoke_test.py
itself follows by cycling one Game() through every state in sequence."""

import pygame
import pytest

import settings
from game import Game
from input_handler import AIInputHandler


@pytest.fixture(scope="module")
def game():
    return Game()


def click(game_, position):
    game_.mouse.position = position
    game_.handle_event(pygame.event.Event(pygame.MOUSEBUTTONUP))


def test_game_boots_and_cycles_through_every_state(game):
    # Mirrors scripts/smoke_test.py.
    assert game._state == Game.STATE_MENU
    game.update()
    game.draw()

    game._state = Game.STATE_LEVEL_SELECT
    game.update()
    game.draw()

    game._enter_game()
    assert game._state == Game.STATE_GAME
    game.update()
    game.draw()


def test_btn_rect_returns_rects_centered_on_the_window(game):
    cx, cy = game._world.window_w // 2, game._world.window_h // 2

    assert game._btn_rect("1p") == pygame.Rect(cx - 106, cy - 130, 212, 44)
    assert game._btn_rect("2p") == pygame.Rect(cx - 106, cy - 66, 212, 44)
    assert game._btn_rect("start") == pygame.Rect(cx - 155, cy - 250, 310, 100)


def test_clicking_start_kicks_off_the_countdown(game):
    game._state = Game.STATE_MENU
    game._countdown = 100

    click(game, game._btn_rect("start").center)

    assert game._countdown == 0


def test_clicking_1p_selects_single_player(game):
    game._state = Game.STATE_MENU

    click(game, game._btn_rect("1p").center)

    assert game._world.two_players is False
    assert game._p1.control == "RL"


def test_clicking_2p_selects_two_player(game):
    game._state = Game.STATE_MENU

    click(game, game._btn_rect("2p").center)

    assert game._world.two_players is True
    assert game._p1.control == "R"
    assert game._p2.control == "L"


def test_step_intro_single_player_only_moves_p1(game):
    game._world.two_players = False
    p1_y_before, p2_y_before = game._p1.y, game._p2.y

    game._step_intro()

    # intro_jump() always advances y (gravity/velocity integration runs
    # unconditionally once called), so an untouched p2 is proof it was
    # never called for this player in single-player mode.
    assert game._p1.y != p1_y_before
    assert game._p2.y == p2_y_before


def test_step_intro_two_player_seq_2_moves_both_players_every_call(game):
    game._world.two_players = True
    game._intro_seq = 2
    p1_y_before, p2_y_before = game._p1.y, game._p2.y

    game._step_intro()

    assert game._p1.y != p1_y_before
    assert game._p2.y != p2_y_before


def test_step_intro_two_player_seq_1_holds_p2_until_p1_descends_past_the_threshold(game):
    game._world.two_players = True
    game._intro_seq = 1
    game._intro_flag = False
    game._p1.y = 490.0
    game._p2.y = 490.0
    p2_y_before = game._p2.y

    game._step_intro()  # p1 still above the 340 gate -- p2 must not move yet
    assert game._p2.y == p2_y_before
    assert game._intro_flag is False

    game._p1.y = 340.0  # force p1 past the gate
    game._step_intro()

    assert game._intro_flag is True
    assert game._p2.y != p2_y_before


def test_step_intro_two_player_seq_3_holds_p1_until_p2_descends_past_the_threshold(game):
    game._world.two_players = True
    game._intro_seq = 3
    game._intro_flag = False
    game._p1.y = 490.0
    game._p2.y = 490.0
    p1_y_before = game._p1.y

    game._step_intro()  # p2 still above the 340 gate -- p1 must not move yet
    assert game._p1.y == p1_y_before
    assert game._intro_flag is False

    game._p2.y = 340.0  # force p2 past the gate
    game._step_intro()

    assert game._intro_flag is True
    assert game._p1.y != p1_y_before


def test_update_menu_advances_the_countdown_by_one(game):
    game._state = Game.STATE_MENU
    game._countdown = 10

    game._update_menu()

    assert game._countdown == 11
    assert game._state == Game.STATE_MENU


def test_update_menu_transitions_to_level_select_once_countdown_reaches_60(game):
    game._state = Game.STATE_MENU
    game._countdown = 59

    game._update_menu()

    assert game._countdown == 60
    assert game._state == Game.STATE_LEVEL_SELECT
    game._state = Game.STATE_MENU  # restore, so later tests get their expected starting state


def test_handle_level_select_event_selecting_a_level_enters_game(game):
    game._state = Game.STATE_LEVEL_SELECT
    rect = game._renderer.level_card_rect(1)

    click(game, rect.center)

    assert game._current_level == 1
    assert game._state == Game.STATE_GAME
    assert len(game._world.platforms) == len(settings.LEVELS[1]["platforms"])


def test_single_player_mode_binds_an_ai_handler_to_p2(game):
    # Explicit rather than relying on leftover two_players state from an
    # earlier test -- _reset_players() only attaches AIInputHandler when
    # two_players is False *at the moment it runs* (see _make_player()).
    game._state = Game.STATE_LEVEL_SELECT
    game._world.two_players = False

    click(game, game._renderer.level_card_rect(0).center)  # -> _reset_players() -> _enter_game()

    assert isinstance(game._p2._input, AIInputHandler)
    assert game._p2._input._self is game._p2
    assert game._p2._input._target is game._p1


def test_update_level_select_switches_the_cursor_state_when_hovering_a_card(game):
    game._state = Game.STATE_LEVEL_SELECT
    rect = game._renderer.level_card_rect(0)

    game.mouse.position = rect.center
    game._update_level_select()
    assert game._cursor._state is game._cursor._click

    game.mouse.position = (0, 0)  # outside every card
    game._update_level_select()
    assert game._cursor._state is game._cursor._normal


def test_update_game_awards_a_point_and_starts_a_new_round_on_a_kill(game, monkeypatch):
    game._state = Game.STATE_GAME
    game._enter_game()
    winner = game._p1
    start_score = winner.score

    monkeypatch.setattr(game._combat, "resolve", lambda vampire, peasant: winner)
    monkeypatch.setattr(
        game._combat, "begin_round",
        lambda vampire, p1, p2: (game._vampire, game._peasant),
    )

    game._update_game()

    assert winner.score == start_score + 1


def test_on_exit_request_from_level_select_returns_to_the_menu(game):
    game._state = Game.STATE_LEVEL_SELECT
    game._countdown = 42

    game.on_exit_request()

    assert game._state == Game.STATE_MENU
    assert game._countdown == 100


def test_on_exit_request_from_game_returns_to_the_menu_and_clears_bullets(game):
    game._state = Game.STATE_GAME
    game._world.bullets.append(object())

    game.on_exit_request()

    assert game._state == Game.STATE_MENU
    assert game._world.bullets == []


def test_on_exit_request_from_the_menu_delegates_to_the_real_quit(game, monkeypatch):
    # From STATE_MENU there's nowhere softer to fall back to -- it's really
    # quitting. Application.exit() calls sys.exit(), so it's monkeypatched
    # rather than actually invoked here.
    game._state = Game.STATE_MENU
    calls = []
    monkeypatch.setattr(game, "exit", lambda: calls.append(True))

    game.on_exit_request()

    assert calls == [True]
