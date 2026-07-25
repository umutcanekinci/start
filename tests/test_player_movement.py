import settings
from entities import Player


def make_player(world, input_handler, x=400.0, y=settings.FLOOR_Y):
    return Player(world, (x, y), input_handler)


def test_moving_right_accelerates_up_to_mov_speed(world, input_handler):
    p = make_player(world, input_handler)
    input_handler.right = True

    p.move()
    assert p.vel_x == settings.ACCEL
    assert (p.left, p.right, p.standing) == (False, True, False)

    for _ in range(50):  # far more than enough frames to hit the cap
        p.move()
    assert p.vel_x == p.mov_speed


def test_moving_left_accelerates_up_to_negative_mov_speed(world, input_handler):
    p = make_player(world, input_handler)
    input_handler.left = True

    p.move()
    assert p.vel_x == -settings.ACCEL
    assert (p.left, p.right, p.standing) == (True, False, False)

    for _ in range(50):
        p.move()
    assert p.vel_x == -p.mov_speed


def test_releasing_input_decays_velocity_via_friction_then_stops(world, input_handler):
    p = make_player(world, input_handler)
    input_handler.right = True
    for _ in range(50):
        p.move()
    assert p.vel_x == p.mov_speed

    input_handler.right = False
    prev = p.vel_x
    p.move()
    assert p.vel_x == prev * settings.FRICTION
    assert p.standing is False

    for _ in range(100):  # decay to below the 0.4 snap-to-zero threshold
        p.move()
    assert p.vel_x == 0.0
    assert p.standing is True
    assert p.walk_count == 0


def test_wraps_from_right_edge_to_the_left_side(world, input_handler):
    p = make_player(world, input_handler, x=world.window_w - 21)
    input_handler.right = True

    p.move()  # x + ACCEL pushes past window_w - 20

    assert p.x == (world.window_w - 21 + settings.ACCEL) - world.window_w
    assert p.x < 0


def test_wraps_from_left_edge_to_the_right_side(world, input_handler):
    p = make_player(world, input_handler, x=-19.0)
    input_handler.left = True

    p.move()  # x - ACCEL pushes past -20

    assert p.x == (-19.0 - settings.ACCEL) + world.window_w
    assert p.x > world.window_w - 25
