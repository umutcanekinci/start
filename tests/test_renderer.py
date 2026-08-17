import pygame
import pytest

import settings
from entities import Platform, Player, Projectile
from renderer import GameRenderer


@pytest.fixture
def renderer(world):
    world.platforms = [Platform(loc, w, h) for loc, w, h in settings.LEVELS[0]["platforms"]]
    return GameRenderer(pygame.Surface((world.window_w, world.window_h)), world)


def test_level_card_rect_lays_cards_out_left_to_right_centered_in_the_window(renderer):
    assert renderer.level_card_rect(0) == pygame.Rect(105, 195, 180, 210)
    assert renderer.level_card_rect(1) == pygame.Rect(310, 195, 180, 210)
    assert renderer.level_card_rect(2) == pygame.Rect(515, 195, 180, 210)


def score_surfaces():
    font = pygame.font.SysFont(None, 20)
    return [font.render("P1   0", True, settings.WHITE), font.render("P2   0", True, settings.WHITE)]


def test_draw_game_with_two_players_and_a_bullet_does_not_raise(renderer, world, input_handler):
    p1 = Player(world, (100, settings.FLOOR_Y), input_handler)
    p2 = Player(world, (200, settings.FLOOR_Y), input_handler)
    p1.be_peasant()
    p2.be_vampire()
    world.bullets.append(Projectile(50, 50, settings.BULLET_RADIUS, settings.BLACK, 1))

    renderer.draw_game(p1, p2, vampire=p2, current_level=0, score_surfs=score_surfaces())


def test_draw_game_single_player_with_no_p2_does_not_raise(renderer, world, input_handler):
    p1 = Player(world, (100, settings.FLOOR_Y), input_handler)
    p1.be_peasant()

    renderer.draw_game(p1, None, vampire=p1, current_level=0, score_surfs=score_surfaces())


def test_draw_level_select_does_not_raise_hovered_or_not(renderer):
    renderer.draw_level_select((0, 0))  # no card hovered
    renderer.draw_level_select(renderer.level_card_rect(1).center)  # hovering card 1


def test_health_bar_color_tiers_by_hp_fraction(renderer, world, input_handler):
    p1 = Player(world, (100, settings.FLOOR_Y), input_handler)
    p1.be_peasant()
    ix, iy = int(p1.x), int(p1.y)
    bar_x = ix + (p1.width - 52) // 2
    bar_y = iy - 12
    sample = (bar_x + 1, bar_y + 1)  # inside the fill for every tier tested below

    p1.hp = p1.max_hp  # > 50% -> green
    renderer._draw_health_bar(p1, ix, iy)
    assert renderer._window.get_at(sample)[:3] == settings.HP_GREEN

    p1.hp = int(p1.max_hp * 0.4)  # 25%-50% -> yellow
    renderer._draw_health_bar(p1, ix, iy)
    assert renderer._window.get_at(sample)[:3] == settings.HP_YELLOW

    p1.hp = int(p1.max_hp * 0.1)  # <= 25% -> red
    renderer._draw_health_bar(p1, ix, iy)
    assert renderer._window.get_at(sample)[:3] == settings.HP_RED
