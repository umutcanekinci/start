import settings
from entities import Platform, Player


def make_player(world, input_handler, x=400.0, y=0.0):
    return Player(world, (x, y), input_handler)


def test_jump_sets_upward_velocity_when_on_ground(world, input_handler):
    p = make_player(world, input_handler)
    p.on_ground = True
    input_handler.jump = True

    p.jump()

    assert p.vel_y == settings.JUMP_POWER
    assert p.on_ground is False


def test_jump_does_nothing_while_airborne(world, input_handler):
    p = make_player(world, input_handler)
    p.on_ground = False
    p.vel_y = 3.0
    input_handler.jump = True

    p.jump()

    assert p.vel_y == 3.0


def test_gravity_accumulates_and_caps_at_max_fall_speed(world, input_handler):
    p = make_player(world, input_handler, y=0.0)
    p.vel_y = settings.MAX_FALL_SPEED - 0.1

    p.physics_update()
    assert p.vel_y == settings.MAX_FALL_SPEED

    p.physics_update()  # stays capped, doesn't keep accumulating
    assert p.vel_y == settings.MAX_FALL_SPEED


def test_lands_on_the_floor_and_stops_falling(world, input_handler):
    p = make_player(world, input_handler, y=settings.FLOOR_Y - 1)
    p.vel_y = 10.0  # this step alone would carry it past the floor

    p.physics_update()

    assert p.y == settings.FLOOR_Y
    assert p.vel_y == 0.0
    assert p.on_ground is True


def test_lands_on_a_platform_within_its_x_range(world, input_handler):
    # Peasant hitbox offset/foot per entities.Player._HITBOX: ox=17, oy=11,
    # foot=49. Solved so this single physics_update() step's foot arc
    # (prev_foot..curr_foot) straddles the platform's y exactly.
    plat = Platform((380, 300), width=100, height=20)
    world.platforms.append(plat)
    p = make_player(world, input_handler, x=400.0, y=239.6)
    p.vel_y = 0.0  # -> 0.5 after one frame's gravity

    p.physics_update()

    assert p.on_ground is True
    assert p.vel_y == 0.0
    assert p.y == float(plat.y - 11 - 49)  # snapped to stand on the platform
    assert p.y < settings.FLOOR_Y  # landed on the platform, not the floor


def test_falls_through_a_platform_outside_its_x_range(world, input_handler):
    plat = Platform((1000, 300), width=100, height=20)  # far off to the side
    world.platforms.append(plat)
    p = make_player(world, input_handler, x=400.0, y=239.6)
    p.vel_y = 0.0

    p.physics_update()

    assert p.on_ground is False
    assert p.y == 239.6 + 0.5  # gravity applied normally, no platform caught it
