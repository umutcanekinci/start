import pygame

from cursor import Cursor


def test_construction_loads_all_three_frame_sets_and_starts_normal():
    cursor = Cursor()

    assert len(cursor._normal) == 17
    assert len(cursor._click) == 8
    assert len(cursor._click2) == 13
    assert cursor._state is cursor._normal
    assert cursor._frame == 0
    assert cursor.rect.size == cursor._normal[0].get_size()


def test_draw_advances_the_frame_each_call():
    cursor = Cursor()
    surface = pygame.Surface((32, 32))

    cursor.draw(surface)
    assert cursor._frame == 1

    cursor.draw(surface)
    assert cursor._frame == 2


def test_draw_wraps_back_to_the_first_frame_at_the_end_of_the_current_state():
    cursor = Cursor()
    cursor._state = cursor._click  # shortest set, 8 frames
    cursor._frame = 8  # one past the last valid index

    cursor.draw(surface=pygame.Surface((32, 32)))

    # draw() resets an out-of-range frame to 0 before blitting, then
    # advances -- so one call from an overrun index lands on frame 1.
    assert cursor._frame == 1


def test_switching_state_takes_effect_on_the_next_draw():
    cursor = Cursor()
    cursor.draw(pygame.Surface((32, 32)))  # frame 1 in _normal

    cursor._state = cursor._click2
    cursor._frame = 0
    cursor.draw(pygame.Surface((32, 32)))

    assert cursor._state is cursor._click2
    assert cursor._frame == 1
