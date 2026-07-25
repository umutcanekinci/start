import settings
from combat import CombatSystem
from entities import Player, Projectile


class _Idle:
    """A no-input FakeInputHandler stand-in, local to keep these tests
    self-contained (see tests/conftest.py's FakeInputHandler for the
    settable version used elsewhere)."""
    control = "idle"
    def is_moving_right(self) -> bool: return False
    def is_moving_left(self) -> bool: return False
    def is_jump_pressed(self) -> bool: return False
    def is_fire_pressed(self) -> bool: return False


def make_player(world, x: float, y: float, role: str) -> Player:
    p = Player(world, (x, y), _Idle())
    (p.be_vampire if role == "vampire" else p.be_peasant)()
    p.x, p.y = x, y
    p._update_hitbox()
    return p


def test_no_overlap_no_bullets_resolves_to_none(world):
    combat = CombatSystem(world)
    vampire = make_player(world, 0, 0, "vampire")
    peasant = make_player(world, 500, 500, "peasant")
    peasant_hp = peasant.hp

    result = combat.resolve(vampire, peasant)

    assert result is None
    assert peasant.hp == peasant_hp


def test_contact_damages_the_peasant_each_overlapping_frame(world):
    combat = CombatSystem(world)
    vampire = make_player(world, 100, 100, "vampire")
    peasant = make_player(world, 100, 100, "peasant")  # same spot -- hitboxes overlap
    start_hp = peasant.hp

    result = combat.resolve(vampire, peasant)

    assert result is None
    assert peasant.hp == start_hp - settings.CONTACT_DAMAGE


def test_vampire_wins_when_contact_drops_peasant_hp_to_zero(world):
    combat = CombatSystem(world)
    vampire = make_player(world, 100, 100, "vampire")
    peasant = make_player(world, 100, 100, "peasant")
    peasant.hp = settings.CONTACT_DAMAGE

    result = combat.resolve(vampire, peasant)

    assert result is vampire
    assert peasant.hp <= 0


def test_bullet_out_of_bounds_is_removed_without_damage(world):
    combat = CombatSystem(world)
    vampire = make_player(world, 400, 100, "vampire")
    peasant = make_player(world, 700, 700, "peasant")  # far from the bullet
    bullet = Projectile(x=world.window_w - 1, y=100, radius=5, color=settings.BLACK, facing=1)
    world.bullets.append(bullet)
    start_hp = vampire.hp

    combat.resolve(vampire, peasant)

    assert bullet not in world.bullets
    assert vampire.hp == start_hp


def test_bullet_hitting_the_vampire_deals_damage_and_is_consumed(world):
    combat = CombatSystem(world)
    vampire = make_player(world, 400, 100, "vampire")
    peasant = make_player(world, 700, 700, "peasant")
    hb = vampire.hitbox
    # Positioned so bullet.x + mov_speed lands inside the vampire's hitbox.
    bullet = Projectile(x=hb.centerx - settings.BULLET_SPEED, y=hb.centery, radius=5, color=settings.BLACK, facing=1)
    world.bullets.append(bullet)
    start_hp = vampire.hp

    result = combat.resolve(vampire, peasant)

    assert bullet not in world.bullets
    assert vampire.hp == start_hp - settings.BULLET_DAMAGE
    assert result is None


def test_peasant_wins_when_a_bullet_drops_vampire_hp_to_zero(world):
    combat = CombatSystem(world)
    vampire = make_player(world, 400, 100, "vampire")
    peasant = make_player(world, 700, 700, "peasant")
    vampire.hp = settings.BULLET_DAMAGE
    hb = vampire.hitbox
    bullet = Projectile(x=hb.centerx - settings.BULLET_SPEED, y=hb.centery, radius=5, color=settings.BLACK, facing=1)
    world.bullets.append(bullet)

    result = combat.resolve(vampire, peasant)

    assert result is peasant
    assert vampire.hp <= 0


def test_bullet_that_misses_stays_in_the_world(world):
    combat = CombatSystem(world)
    vampire = make_player(world, 400, 100, "vampire")
    peasant = make_player(world, 700, 700, "peasant")
    bullet = Projectile(x=10, y=10, radius=5, color=settings.BLACK, facing=1)  # nowhere near the vampire
    world.bullets.append(bullet)

    combat.resolve(vampire, peasant)

    assert bullet in world.bullets


def test_begin_round_resets_positions_velocity_flags_hp_and_clears_bullets(world):
    combat = CombatSystem(world)
    p1 = make_player(world, 0, 0, "peasant")
    p2 = make_player(world, 0, 0, "peasant")
    p1.hp = p2.hp = 1
    p1.vel_x = p1.vel_y = 5.0
    p1.left = True
    world.bullets.append(Projectile(1, 1, 5, settings.BLACK, 1))

    combat.begin_round(p1, p1, p2)

    assert world.bullets == []
    cx = world.window_w // 2
    assert (p1.x, p1.y) == (float(cx + 100), settings.FLOOR_Y)
    assert (p2.x, p2.y) == (float(cx - 100), settings.FLOOR_Y)
    for p in (p1, p2):
        assert (p.vel_x, p.vel_y) == (0.0, 0.0)
        assert p.on_ground is True
        assert (p.left, p.right) == (False, False)
        assert p.hp == settings.MAX_HP


def test_begin_round_turns_the_old_vampire_into_a_peasant(world, monkeypatch):
    # random.choice could re-pick p1 as the new vampire too (50/50), which
    # would flip it right back -- force p2 so this test isn't flaky.
    import combat as combat_module

    combat = CombatSystem(world)
    p1 = make_player(world, 0, 0, "vampire")
    p2 = make_player(world, 0, 0, "peasant")
    monkeypatch.setattr(combat_module.random, "choice", lambda seq: seq[1])

    combat.begin_round(p1, p1, p2)

    assert p1.vampire is False


def test_begin_round_picks_the_new_vampire_via_random_choice(world, monkeypatch):
    import combat as combat_module

    p1 = make_player(world, 0, 0, "peasant")
    p2 = make_player(world, 0, 0, "peasant")
    combat = CombatSystem(world)

    monkeypatch.setattr(combat_module.random, "choice", lambda seq: seq[1])
    vampire, peasant = combat.begin_round(p1, p1, p2)

    assert vampire is p2
    assert peasant is p1
    assert p2.vampire is True
    assert p1.vampire is False
