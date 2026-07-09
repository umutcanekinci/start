import pygame

import settings
from input_handler import InputHandler
from world import GameWorld


class Player:
    _HITBOX = {
        'vampire': (17,  2, 31, 57),
        'peasant': (17, 11, 29, 52),
    }

    def __init__(self, world: GameWorld, location, input_handler: InputHandler,
                 width: int = 64, height: int = 64):
        self._world  = world
        self._input  = input_handler

        self.x       = float(location[0])
        self.y       = float(location[1])
        self.width   = width
        self.height  = height

        self.vel_x     = 0.0
        self.vel_y     = 0.0
        self.on_ground = True

        self.mov_speed  = settings.PLAYER_SPEED
        self.left       = False
        self.right      = False
        self.standing   = True
        self.walk_count = 0
        self.facing     = 1

        self.score   = 0
        self.hp      = settings.MAX_HP
        self.max_hp  = settings.MAX_HP
        self.vampire = False

        self._shoot_timer = 0
        self._jump_sound  = pygame.mixer.Sound('assets/sounds/jump.wav')

        self.hitbox     = pygame.Rect(0, 0, 0, 0)
        self.walk_left  = []
        self.walk_right = []

    @property
    def control(self) -> str:
        return self._input.control

    @control.setter
    def control(self, value: str):
        self._input.control = value

    # ---------------------------------------------------------------- role

    def _update_hitbox(self):
        ox, oy, w, h = self._HITBOX['vampire' if self.vampire else 'peasant']
        self.hitbox = pygame.Rect(int(self.x) + ox, int(self.y) + oy, w, h)

    def be_vampire(self):
        self.walk_right = [pygame.image.load(f'assets/images/vampire/R{i}E.png') for i in range(1, 10)]
        self.walk_left  = [pygame.image.load(f'assets/images/vampire/L{i}E.png') for i in range(1, 10)]
        self.mov_speed  = settings.VAMPIRE_SPEED
        self.vampire    = True
        self._update_hitbox()

    def be_peasant(self):
        self.walk_right = [pygame.image.load(f'assets/images/peasant/R{i}.png') for i in range(1, 10)]
        self.walk_left  = [pygame.image.load(f'assets/images/peasant/L{i}.png') for i in range(1, 10)]
        self.mov_speed  = settings.PLAYER_SPEED
        self.vampire    = False
        self._update_hitbox()

    # ---------------------------------------------------------------- input / update

    def update(self):
        self.move()
        self.shoot()
        self.jump()
        self.physics_update()

    def move(self):
        if self._input.is_moving_right():
            self.vel_x = min(self.vel_x + settings.ACCEL, self.mov_speed)
            self.left, self.right, self.standing = False, True, False
        elif self._input.is_moving_left():
            self.vel_x = max(self.vel_x - settings.ACCEL, -self.mov_speed)
            self.left, self.right, self.standing = True, False, False
        else:
            self.vel_x *= settings.FRICTION
            if abs(self.vel_x) < 0.4:
                self.vel_x    = 0.0
                self.standing = True
                self.walk_count = 0
            else:
                self.standing = False

        new_x = self.x + self.vel_x
        if new_x > self._world.window_w - 20:
            new_x -= self._world.window_w
        elif new_x < -20:
            new_x += self._world.window_w
        self.x = new_x

    def jump(self):
        if self._input.is_jump_pressed() and self.on_ground:
            self.vel_y     = settings.JUMP_POWER
            self.on_ground = False
            if not self.vampire:
                self._jump_sound.play()

    def shoot(self):
        if self.vampire:
            return
        if self._shoot_timer > 0:
            self._shoot_timer -= 1
            return
        if self._input.is_fire_pressed() and len(self._world.bullets) < settings.MAX_BULLETS:
            self.facing = -1 if self.left else 1
            self._world.bullets.append(Projectile(
                int(self.x) + self.width // 2,
                int(self.y) + self.height // 2,
                settings.BULLET_RADIUS,
                settings.BLACK,
                self.facing,
            ))
            self._shoot_timer = settings.SHOOT_COOLDOWN

    # ---------------------------------------------------------------- physics

    def physics_update(self):
        self.vel_y = min(self.vel_y + settings.GRAVITY, settings.MAX_FALL_SPEED)
        prev_y     = self.y
        self.y    += self.vel_y
        self.on_ground = False

        if self.y >= settings.FLOOR_Y:
            self.y         = settings.FLOOR_Y
            self.vel_y     = 0.0
            self.on_ground = True
            self._update_hitbox()
            return

        if self.vel_y > 0:
            ox, oy, _, _ = self._HITBOX['vampire' if self.vampire else 'peasant']
            foot  = 58 if self.vampire else 49
            reach = 31 if self.vampire else 29
            hb_x  = int(self.x) + ox

            prev_foot = prev_y + oy + foot
            curr_foot = self.y  + oy + foot

            for plat in self._world.platforms:
                in_x = hb_x + reach >= plat.x and hb_x <= plat.x + plat.width
                if in_x and prev_foot <= plat.y <= curr_foot:
                    self.y         = float(plat.y - oy - foot)
                    self.vel_y     = 0.0
                    self.on_ground = True
                    break

        self._update_hitbox()

    # ---------------------------------------------------------------- animation

    def draw(self, surface: pygame.Surface):
        frames = self.walk_left if self.left else self.walk_right
        if not frames:
            return

        if self.walk_count + 1 >= len(frames) * 3:
            self.walk_count = 0

        ix, iy = int(self.x), int(self.y)
        if not self.standing:
            surface.blit(frames[self.walk_count // 3], (ix, iy))
            self.walk_count += 1
        else:
            surface.blit(frames[0], (ix, iy))

        self._update_hitbox()

    def intro_jump(self):
        if self.on_ground:
            self.vel_y     = settings.JUMP_POWER * 0.65
            self.on_ground = False

        self.vel_y = min(self.vel_y + settings.GRAVITY, settings.MAX_FALL_SPEED)
        self.y    += self.vel_y

        if self.y >= settings.FLOOR_Y:
            self.y         = settings.FLOOR_Y
            self.vel_y     = 0.0
            self.on_ground = True


class Platform:
    _tile_cache: dict[int, pygame.Surface] = {}

    def __init__(self, location: tuple, width: int, height: int):
        self.x, self.y = location
        self.width     = width
        self.height    = height
        self.tile      = self._get_tile(height)

    @classmethod
    def _get_tile(cls, size: int) -> pygame.Surface:
        """A square tile scaled to `size`, cached per platform height.

        platfor_tile.png is a seamless 128x128 tile, not a stretchable
        banner -- scaling it non-uniformly to a platform's full w x h would
        squash the grass top, so it's kept square and tiled edge-to-edge
        across the platform width instead.
        """
        tile = cls._tile_cache.get(size)
        if tile is None:
            img  = pygame.image.load("assets/images/platfor_tile.png").convert_alpha()
            tile = pygame.transform.scale(img, (size, size))
            cls._tile_cache[size] = tile
        return tile

    def draw(self, surface: pygame.Surface):
        tile_w    = self.tile.get_width()
        x         = self.x
        remaining = self.width
        while remaining > 0:
            w = min(tile_w, remaining)
            surface.blit(self.tile, (x, self.y), (0, 0, w, self.height))
            x += w
            remaining -= w


class Projectile:
    def __init__(self, x: int, y: int, radius: int, color: tuple, facing: int):
        self.x         = float(x)
        self.y         = float(y)
        self.radius    = radius
        self.color     = color
        self.mov_speed = settings.BULLET_SPEED * facing

    @property
    def rect(self) -> pygame.Rect:
        r = self.radius
        return pygame.Rect(int(self.x) - r, int(self.y) - r, r * 2, r * 2)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)