import settings
from entities import Player


def make_player(world, input_handler, x=100.0, y=100.0):
    return Player(world, (x, y), input_handler)


def test_vampire_never_shoots(world, input_handler):
    p = make_player(world, input_handler)
    p.be_vampire()
    input_handler.fire = True

    p.shoot()

    assert world.bullets == []


def test_peasant_shoots_facing_right_by_default(world, input_handler):
    p = make_player(world, input_handler)
    p.be_peasant()
    input_handler.fire = True

    p.shoot()

    assert len(world.bullets) == 1
    assert p.facing == 1
    assert world.bullets[0].mov_speed == settings.BULLET_SPEED  # facing 1 -> positive


def test_peasant_shoots_facing_left_when_moving_left(world, input_handler):
    p = make_player(world, input_handler)
    p.be_peasant()
    p.left = True
    input_handler.fire = True

    p.shoot()

    assert p.facing == -1
    assert world.bullets[0].mov_speed == -settings.BULLET_SPEED


def test_shoot_does_nothing_without_fire_pressed(world, input_handler):
    p = make_player(world, input_handler)
    p.be_peasant()

    p.shoot()

    assert world.bullets == []


def test_shoot_respects_the_cooldown_between_shots(world, input_handler):
    # shoot() checks _shoot_timer > 0 *before* decrementing, so it takes
    # exactly SHOOT_COOLDOWN decrement-only calls to walk the timer from
    # SHOOT_COOLDOWN down to 0, and one further call to actually fire again.
    p = make_player(world, input_handler)
    p.be_peasant()
    input_handler.fire = True

    p.shoot()
    assert len(world.bullets) == 1

    for _ in range(settings.SHOOT_COOLDOWN):
        p.shoot()
    assert len(world.bullets) == 1  # still on cooldown

    p.shoot()  # cooldown just expired
    assert len(world.bullets) == 2


def test_shoot_stops_once_max_bullets_reached(world, input_handler):
    # Bypasses _shoot_timer directly between shots so this test is only
    # about the MAX_BULLETS cap; cooldown timing has its own dedicated test.
    p = make_player(world, input_handler)
    p.be_peasant()
    input_handler.fire = True

    for _ in range(settings.MAX_BULLETS):
        p._shoot_timer = 0
        p.shoot()
    assert len(world.bullets) == settings.MAX_BULLETS

    p._shoot_timer = 0
    p.shoot()
    assert len(world.bullets) == settings.MAX_BULLETS  # capped


def test_be_vampire_sets_vampire_hitbox_dimensions_and_speed(world, input_handler):
    p = make_player(world, input_handler, x=10.0, y=20.0)
    p.be_vampire()

    ox, oy, w, h = Player._HITBOX["vampire"]
    assert (p.hitbox.x, p.hitbox.y, p.hitbox.w, p.hitbox.h) == (10 + ox, 20 + oy, w, h)
    assert p.mov_speed == settings.VAMPIRE_SPEED
    assert p.vampire is True


def test_be_peasant_sets_peasant_hitbox_dimensions_and_speed(world, input_handler):
    p = make_player(world, input_handler, x=10.0, y=20.0)
    p.be_vampire()  # start as vampire so switching back is a real change
    p.be_peasant()

    ox, oy, w, h = Player._HITBOX["peasant"]
    assert (p.hitbox.x, p.hitbox.y, p.hitbox.w, p.hitbox.h) == (10 + ox, 20 + oy, w, h)
    assert p.mov_speed == settings.PLAYER_SPEED
    assert p.vampire is False
