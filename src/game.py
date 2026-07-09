import random

import pygame
from pygame_core.application import Application
from pygame_core.mouse import Mouse
from pygame_core.splash_screen import SplashScreen
import settings
from audio import AudioManager
from combat import CombatSystem
from cursor import Cursor
from entities import Platform, Player
from input_handler import AIInputHandler, KeyboardInputHandler
from menu import Menu
from renderer import GameRenderer
from world import GameWorld



class Game(Application):
    STATE_MENU         = "menu"
    STATE_LEVEL_SELECT = "level_select"
    STATE_GAME         = "game"

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 1024 * 3)
        self._cursor = Cursor()
        _mouse = Mouse()
        _mouse.cursor = self._cursor

        super().__init__(
            size=(settings.VIRTUAL_W, settings.VIRTUAL_H),
            title=settings.TITLE,
            fps=settings.FPS,
            mouse=_mouse,
        )
        _mouse.set_cursor_visible(False)

        self._splash = SplashScreen(
            ["assets/images/branding/pygame_logo.png"],
            fade_ms=settings.SPLASH_FADE_MS, hold_ms=settings.SPLASH_HOLD_MS,
        )

        self._world = GameWorld(window_w=settings.VIRTUAL_W, window_h=settings.VIRTUAL_H)
        self._world.platforms = [Platform(loc, w, h) for loc, w, h in settings.LEVELS[0]['platforms']]

        self._menu     = Menu(settings.VIRTUAL_W, settings.VIRTUAL_H, self._cursor)
        self._audio    = AudioManager()
        self._renderer = GameRenderer(self.window, self._world)
        self._combat   = CombatSystem(self._world)

        self._font_hud   = pygame.font.SysFont("ComicSansMs", 22)
        self._score_surfs: list[pygame.Surface] = [None, None]

        self._current_level = 0
        self._state         = self.STATE_MENU
        self._vampire       = None
        self._peasant       = None
        self._countdown     = 100
        self._intro_seq     = random.choice((1, 2, 3))
        self._intro_flag    = False

        self._p1 = self._make_player(
            (self._world.platforms[1].x - 64 + 18, settings.FLOOR_Y), "R"
        )
        self._p2 = self._make_player(
            (self._world.platforms[0].x + self._world.platforms[0].width - 17, settings.FLOOR_Y), "L", is_p2=True
        )
        self._p1.left = True
        self._p1.be_peasant()
        self._p2.be_peasant()
        self._bind_ai()
        self._refresh_scores()

        self._audio.play_menu()

    # ------------------------------------------------------------------ helpers

    def _make_player(self, location, control: str, is_p2: bool = False) -> Player:
        if not self._world.two_players:
            handler = AIInputHandler() if is_p2 else KeyboardInputHandler("RL")
        else:
            handler = KeyboardInputHandler(control)
        return Player(self._world, location, handler)

    def _bind_ai(self) -> None:
        if isinstance(self._p2._input, AIInputHandler):
            self._p2._input.bind(self._p2, self._p1)

    def _refresh_scores(self):
        self._score_surfs[0] = self._font_hud.render(f"P1   {self._p1.score}", True, settings.WHITE)
        self._score_surfs[1] = self._font_hud.render(f"P2   {self._p2.score}", True, settings.WHITE)

    def _btn_rect(self, name: str) -> pygame.Rect:
        cx, cy = self._world.window_w // 2, self._world.window_h // 2
        return {
            '1p':    pygame.Rect(cx - 106, cy - 130, 212,  44),
            '2p':    pygame.Rect(cx - 106, cy -  66, 212,  44),
            'start': pygame.Rect(cx - 155, cy - 250, 310, 100),
        }[name]

    def _reset_players(self):
        self._p1 = self._make_player(
            (self._world.platforms[1].x - 64 + 18, settings.FLOOR_Y), "R"
        )
        self._p2 = self._make_player(
            (self._world.platforms[0].x + self._world.platforms[0].width - 17, settings.FLOOR_Y), "L", is_p2=True
        )
        self._p1.left = True
        self._p1.be_peasant()
        self._p2.be_peasant()
        self._bind_ai()
        self._intro_seq  = random.choice((1, 2, 3))
        self._intro_flag = False
        self._refresh_scores()

    # -------------------------------------------------------- Application overrides

    def run(self) -> None:
        # SplashScreen runs its own loop with direct pygame.display.update()
        # calls, bypassing Application._present()'s scale step -- draw it
        # straight onto the real display surface rather than the offscreen
        # logical canvas, or it would never actually reach the screen.
        self._splash.run(self.display_surface, self.clock, self._fps)
        super().run()

    def on_exit_request(self) -> None:
        if self._state == self.STATE_GAME:
            self._audio.stop_game()
            self._world.bullets.clear()
            self._reset_players()
            self._audio.play_menu()
            self._menu.randomize_background()
            self._countdown = 100
            self._state = self.STATE_MENU
        elif self._state == self.STATE_LEVEL_SELECT:
            self._reset_players()
            self._audio.play_menu()
            self._menu.randomize_background()
            self._countdown = 100
            self._state = self.STATE_MENU
        else:
            super().on_exit_request()

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._state == self.STATE_MENU:
            self._handle_menu_event(event)
        elif self._state == self.STATE_LEVEL_SELECT:
            self._handle_level_select_event(event)

    def update(self) -> None:
        if self._state == self.STATE_MENU:
            self._update_menu()
        elif self._state == self.STATE_LEVEL_SELECT:
            self._update_level_select()
        elif self._state == self.STATE_GAME:
            self._update_game()

    def draw(self) -> None:
        pos = self.mouse.position
        if self._state == self.STATE_MENU:
            p2 = self._p2 if self._world.two_players else None
            self._menu.draw(self.window, self._countdown, self._p1, p2)
        elif self._state == self.STATE_LEVEL_SELECT:
            self._renderer.draw_level_select(pos)
        elif self._state == self.STATE_GAME:
            self._renderer.draw_game(
                self._p1, self._p2, self._vampire, self._current_level, self._score_surfs
            )

    # -------------------------------------------------------------------- menu

    def _handle_menu_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONUP:
            pos = self.mouse.position
            if self._btn_rect('start').collidepoint(pos):
                self._countdown = 0
            elif self._btn_rect('1p').collidepoint(pos):
                self._world.two_players = False
                self._p1.control = "RL"
            elif self._btn_rect('2p').collidepoint(pos):
                self._world.two_players = True
                self._p1.control = "R"
                self._p2.control = "L"

    def _update_menu(self) -> None:
        self._update_menu_button_states(self.mouse.position)
        self._step_intro()

        if self._countdown < 100:
            self._countdown += 1
        if self._countdown == 60:
            self._audio.pause_all()
            self._audio.stop_menu()
            self._renderer.randomize_background()
            self._state = self.STATE_LEVEL_SELECT

    def _update_menu_button_states(self, pos) -> None:
        for name in ('1p', '2p', 'start'):
            hovered = self._btn_rect(name).collidepoint(pos)
            pressed = pygame.mouse.get_pressed()[0] if hovered else False
            self._menu.update_button_state(name, hovered, pressed)

    def _step_intro(self) -> None:
        if self._world.two_players:
            if self._intro_seq == 1:
                self._p1.intro_jump()
                if self._p1.y <= 340:
                    self._intro_flag = True
                if self._intro_flag:
                    self._p2.intro_jump()
            elif self._intro_seq == 2:
                self._p1.intro_jump()
                self._p2.intro_jump()
            else:
                self._p2.intro_jump()
                if self._p2.y <= 340:
                    self._intro_flag = True
                if self._intro_flag:
                    self._p1.intro_jump()
        else:
            self._p1.intro_jump()

    # ---------------------------------------------------------------- level select

    def _update_level_select(self) -> None:
        pos = self.mouse.position
        any_hover = any(
            self._renderer.level_card_rect(i).collidepoint(pos)
            for i in range(len(settings.LEVELS))
        )
        self._cursor._state = self._cursor._click if any_hover else self._cursor._normal

    def _handle_level_select_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONUP:
            pos = self.mouse.position
            for i in range(len(settings.LEVELS)):
                if self._renderer.level_card_rect(i).collidepoint(pos):
                    self._current_level = i
                    self._world.platforms = [
                        Platform(loc, w, h)
                        for loc, w, h in settings.LEVELS[i]['platforms']
                    ]
                    self._reset_players()
                    self._enter_game()
                    return

    # ---------------------------------------------------------------------- game

    def _enter_game(self) -> None:
        for p in (self._p1, self._p2):
            p.y = settings.FLOOR_Y
            p.vel_y = p.vel_x = 0.0
            p.on_ground = True
            p.hp = settings.MAX_HP

        self._renderer.randomize_background()
        self._audio.play_game()

        self._vampire = random.choice((self._p1, self._p2))
        self._vampire.be_vampire()
        self._peasant = self._p2 if self._vampire is self._p1 else self._p1

        self._state = self.STATE_GAME

    def _update_game(self) -> None:
        self._p1.update()
        self._p2.update()
        winner = self._combat.resolve(self._vampire, self._peasant)
        if winner is not None:
            winner.score += 1
            self._vampire, self._peasant = self._combat.begin_round(
                self._vampire, self._p1, self._p2
            )
            self._renderer.randomize_background()
            self._refresh_scores()