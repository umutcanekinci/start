import pygame

from settings import WHITE


class Menu:
    def __init__(self, window_w: int, window_h: int, cursor):
        self.cursor   = cursor
        self.window_w = window_w
        self.window_h = window_h

        self._btn_1p_hover    = self._btn_1p_click    = False
        self._btn_2p_hover    = self._btn_2p_click    = False
        self._btn_start_hover = self._btn_start_click = False

        self._font_sm = pygame.font.SysFont("ComicSansMs", 18)
        self._lbl_p1  = self._font_sm.render("P1", True, WHITE)
        self._lbl_p2  = self._font_sm.render("P2", True, WHITE)

        bg = pygame.image.load("assets/images/bg.jpg")
        self._background = pygame.transform.scale(bg, (window_w, window_h))

        self._start_btn = pygame.transform.scale(
            pygame.image.load("assets/images/buttons/start.png"), (310, 100)
        )
        self._btn_1p = [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/buttons/oneplayer{'' if i == 0 else i + 1}.png"),
                (212, 44),
            )
            for i in range(3)
        ]
        self._btn_2p = [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/buttons/twoplayer{'' if i == 0 else i + 1}.png"),
                (212, 44),
            )
            for i in range(3)
        ]
        self._wait_frames = [
            pygame.image.load(f"assets/images/wait/321-{i}-removebg-preview.png") for i in range(49)
        ]

    def update_button_state(self, btn_name: str, hovered: bool, pressed: bool):
        setattr(self, f'_btn_{btn_name}_hover', hovered and not pressed)
        setattr(self, f'_btn_{btn_name}_click', hovered and pressed)

    def draw(self, surface: pygame.Surface, countdown: int, p1, p2=None):
        """Draw the main menu. Pass p2=None for single-player mode."""
        surface.blit(self._background, (0, 0))
        cx, cy = self.window_w // 2, self.window_h // 2

        if countdown == 100:
            surface.blit(self._start_btn, (cx - 155, cy - 250))

            state_1p = 2 if self._btn_1p_hover else (1 if self._btn_1p_click else 0)
            state_2p = 2 if self._btn_2p_hover else (1 if self._btn_2p_click else 0)
            surface.blit(self._btn_1p[state_1p], (cx - 106, cy - 130))
            surface.blit(self._btn_2p[state_2p], (cx - 106, cy - 66))

            any_hover = self._btn_1p_hover or self._btn_2p_hover or self._btn_start_hover
            any_click = self._btn_1p_click or self._btn_2p_click or self._btn_start_click
            new_state = (
                self.cursor._click if any_hover else
                self.cursor._click2 if any_click else
                self.cursor._normal
            )
            if new_state is not self.cursor._state:
                self.cursor._state = new_state
                self.cursor._frame = 0

        players = [(p1, self._lbl_p1)]
        if p2 is not None:
            players.append((p2, self._lbl_p2))

        for p, lbl in players:
            surface.blit(lbl, (int(p.x) + p.width // 4 + 8, int(p.y) - p.height // 2))
            p.draw(surface)

        if 0 < countdown < 48:
            scaled = pygame.transform.scale(self._wait_frames[countdown], (300, 300))
            surface.blit(scaled, (250, 30))
        elif 48 <= countdown < 60:
            scaled = pygame.transform.scale(self._wait_frames[48], (300, 300))
            surface.blit(scaled, (250, 30))
