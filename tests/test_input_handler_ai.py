from entities import Player
from input_handler import AIInputHandler


def make_player(world, input_handler, x: float, vampire: bool = False, left: bool = False) -> Player:
    p = Player(world, (x, 0.0), input_handler)
    p.vampire = vampire
    p.left = left
    return p


def make_ai(world, input_handler, self_x, target_x, *, self_vampire=False, self_left=False):
    ai = AIInputHandler()
    me     = make_player(world, input_handler, self_x, vampire=self_vampire, left=self_left)
    target = make_player(world, input_handler, target_x)
    ai.bind(me, target)
    return ai, me, target


def test_unbound_handler_reports_no_input(world, input_handler):
    ai = AIInputHandler()
    assert ai.is_moving_right() is False
    assert ai.is_moving_left() is False
    assert ai.is_jump_pressed() is False
    assert ai.is_fire_pressed() is False


def test_dx_is_the_direct_difference_within_half_the_window(world, input_handler):
    ai, _, _ = make_ai(world, input_handler, self_x=100, target_x=200)
    assert ai._dx() == 100


def test_dx_wraps_the_short_way_when_target_is_past_the_far_edge(world, input_handler):
    # self near x=10, target near x=790 on an 800-wide screen -- the short
    # path is 20px leftward (wrapping through x=0), not 780px rightward.
    ai, _, _ = make_ai(world, input_handler, self_x=10, target_x=790)
    assert ai._dx() == -20


def test_dx_wraps_the_short_way_in_the_other_direction(world, input_handler):
    ai, _, _ = make_ai(world, input_handler, self_x=790, target_x=10)
    assert ai._dx() == 20


def test_vampire_closes_in_past_the_small_deadzone(world, input_handler):
    ai, _, _ = make_ai(world, input_handler, self_x=100, target_x=200, self_vampire=True)  # dx=100
    assert ai.is_moving_right() is True
    assert ai.is_moving_left() is False


def test_vampire_holds_still_inside_the_deadzone(world, input_handler):
    ai, _, _ = make_ai(world, input_handler, self_x=100, target_x=102, self_vampire=True)  # dx=2
    assert ai.is_moving_right() is False
    assert ai.is_moving_left() is False


def test_peasant_retreats_when_the_vampire_is_too_close(world, input_handler):
    # dx=-30 (target/vampire to the left): abs(dx) < 80 -> retreat, i.e.
    # move away from it (right).
    ai, _, _ = make_ai(world, input_handler, self_x=100, target_x=70)
    assert ai.is_moving_right() is True
    assert ai.is_moving_left() is False


def test_peasant_closes_in_when_the_vampire_is_too_far(world, input_handler):
    # dx=200: abs(dx) > 180 -> close the distance (move right, toward it).
    ai, _, _ = make_ai(world, input_handler, self_x=100, target_x=300)
    assert ai.is_moving_right() is True


def test_peasant_turns_to_face_the_target_when_in_range_but_facing_away(world, input_handler):
    # dx=100 (in the 80-180 "hold" band), facing left while target is to
    # the right -> turn toward it.
    ai, _, _ = make_ai(world, input_handler, self_x=100, target_x=200, self_left=True)
    assert ai.is_moving_right() is True


def test_peasant_holds_position_when_in_range_and_already_facing_target(world, input_handler):
    ai, _, _ = make_ai(world, input_handler, self_x=100, target_x=200, self_left=False)
    assert ai.is_moving_right() is False
    assert ai.is_moving_left() is False
