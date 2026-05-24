import random

import settings
from world import GameWorld


class CombatSystem:
    def __init__(self, world: GameWorld):
        self._world = world

    def resolve(self, vampire, peasant):
        """Returns the winning player this frame, or None if the round continues."""
        if vampire.hitbox.colliderect(peasant.hitbox):
            peasant.hp -= settings.CONTACT_DAMAGE
            if peasant.hp <= 0:
                return vampire

        for bullet in self._world.bullets[:]:
            bullet.x += bullet.mov_speed
            if not (0 < bullet.x < self._world.window_w):
                self._world.bullets.remove(bullet)
                continue
            if bullet.rect.colliderect(vampire.hitbox):
                vampire.hp -= settings.BULLET_DAMAGE
                self._world.bullets.remove(bullet)
                if vampire.hp <= 0:
                    return peasant

        return None

    def begin_round(self, old_vampire, p1, p2):
        """Resets positions/HP for a new round. Returns (new_vampire, new_peasant)."""
        self._world.bullets.clear()

        cx = self._world.window_w // 2
        p1.x, p1.y = float(cx + 100), settings.FLOOR_Y
        p2.x, p2.y = float(cx - 100), settings.FLOOR_Y
        for p in (p1, p2):
            p.vel_x = p.vel_y = 0.0
            p.on_ground = True
            p.left = p.right = False
            p.hp = settings.MAX_HP

        old_vampire.be_peasant()
        vampire = random.choice((p1, p2))
        vampire.be_vampire()
        peasant = p2 if vampire is p1 else p1
        return vampire, peasant