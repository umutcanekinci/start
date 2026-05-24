import pygame

import settings
from world import GameWorld


class GameRenderer:
    def __init__(self, window: pygame.Surface, world: GameWorld):
        self._window = window
        self._world = world

        bg = pygame.image.load("res/images/bg.jpg")
        self._background = pygame.transform.scale(bg, (world.window_w, world.window_h))

        self._font_sm    = pygame.font.SysFont("ComicSansMs", 18)
        self._font_hud   = pygame.font.SysFont("ComicSansMs", 22)
        self._font_title = pygame.font.SysFont("ComicSansMs", 42)

        self._lbl_vampire = self._font_sm.render("VAMPIRE", True, settings.HP_RED)
        self._lbl_peasant = self._font_sm.render("PEASANT", True, settings.HP_GREEN)

    # ------------------------------------------------------------------ game

    def draw_game(self, p1, p2, vampire, current_level: int, score_surfs):
        self._window.blit(self._background, (0, 0))

        for plat in self._world.platforms:
            plat.draw(self._window)
        for bullet in self._world.bullets:
            bullet.draw(self._window)

        self._draw_sprite_hud(p1, vampire)
        if p2 is not None:
            self._draw_sprite_hud(p2, vampire)

        self._draw_top_hud(p1, p2, current_level, score_surfs)

    def _draw_sprite_hud(self, player, vampire):
        ix, iy = int(player.x), int(player.y)
        self._draw_role_tag(player, ix, iy, vampire)
        self._draw_health_bar(player, ix, iy)
        player.draw(self._window)

    def _draw_role_tag(self, player, ix, iy, vampire):
        is_vampire = vampire is player
        role_lbl = self._lbl_vampire if is_vampire else self._lbl_peasant
        tag_x = ix + (player.width - role_lbl.get_width()) // 2
        tag_y = iy - 46
        tag_bg = pygame.Rect(tag_x - 3, tag_y - 1, role_lbl.get_width() + 6, role_lbl.get_height() + 2)
        pygame.draw.rect(self._window, (0, 0, 0, 160), tag_bg, border_radius=3)
        self._window.blit(role_lbl, (tag_x, tag_y))

    def _draw_health_bar(self, player, ix, iy):
        bar_w, bar_h = 52, 7
        bar_x = ix + (player.width - bar_w) // 2
        bar_y = iy - 12
        pct   = max(0.0, player.hp / player.max_hp)
        fill  = int(bar_w * pct)
        hp_color = settings.HP_GREEN if pct > 0.5 else (settings.HP_YELLOW if pct > 0.25 else settings.HP_RED)
        pygame.draw.rect(self._window, (40, 40, 40), (bar_x, bar_y, bar_w, bar_h))
        if fill > 0:
            pygame.draw.rect(self._window, hp_color, (bar_x, bar_y, fill, bar_h))
        pygame.draw.rect(self._window, settings.LIGHT_GREY, (bar_x, bar_y, bar_w, bar_h), 1)

    def _draw_top_hud(self, p1, p2, current_level: int, score_surfs):
        pad, panel_h = 6, 32

        p1_surf = score_surfs[0]
        p1_w    = p1_surf.get_width() + pad * 2
        p1_rect = pygame.Rect(0, 0, p1_w, panel_h)
        pygame.draw.rect(self._window, settings.PANEL_BG, p1_rect)
        pygame.draw.rect(self._window, settings.BLUE, p1_rect, 1)
        self._window.blit(p1_surf, (pad, (panel_h - p1_surf.get_height()) // 2))

        if p2 is not None:
            p2_surf = score_surfs[1]
            p2_w    = p2_surf.get_width() + pad * 2
            p2_rect = pygame.Rect(self._world.window_w - p2_w, 0, p2_w, panel_h)
            pygame.draw.rect(self._window, settings.PANEL_BG, p2_rect)
            pygame.draw.rect(self._window, settings.RED, p2_rect, 1)
            self._window.blit(p2_surf, (self._world.window_w - p2_w + pad, (panel_h - p2_surf.get_height()) // 2))

        lvl_name = settings.LEVELS[current_level]['name']
        lvl_surf = self._font_sm.render(lvl_name, True, settings.LIGHT_GREY)
        self._window.blit(lvl_surf, (self._world.window_w // 2 - lvl_surf.get_width() // 2, 8))

    # ------------------------------------------------------------ level select

    def draw_level_select(self, pos):
        self._window.blit(self._background, (0, 0))

        overlay = pygame.Surface((self._world.window_w, self._world.window_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self._window.blit(overlay, (0, 0))

        title = self._font_title.render("SELECT LEVEL", True, settings.WHITE)
        self._window.blit(title, (self._world.window_w // 2 - title.get_width() // 2, 60))

        for i, lvl in enumerate(settings.LEVELS):
            rect       = self.level_card_rect(i)
            hovered    = rect.collidepoint(pos)
            bg_col     = (70, 70, 110) if hovered else (35, 35, 60)
            border_col = settings.WHITE if hovered else settings.MID_GREY

            pygame.draw.rect(self._window, bg_col,     rect, border_radius=10)
            pygame.draw.rect(self._window, border_col, rect, 2, border_radius=10)

            num_surf = self._font_hud.render(f"Level {i + 1}", True, settings.LIGHT_GREY)
            self._window.blit(num_surf, (rect.centerx - num_surf.get_width() // 2, rect.y + 10))

            name_surf = self._font_sm.render(lvl['name'], True, settings.WHITE)
            self._window.blit(name_surf, (rect.centerx - name_surf.get_width() // 2, rect.y + 34))

            preview = pygame.Rect(rect.x + 8, rect.y + 60, rect.w - 16, rect.h - 80)
            pygame.draw.rect(self._window, (20, 20, 40), preview, border_radius=4)
            sx = preview.w / self._world.window_w
            sy = preview.h / self._world.window_h
            for (px, py), pw, ph in lvl['platforms']:
                prect = pygame.Rect(
                    preview.x + int(px * sx),
                    preview.y + int(py * sy),
                    max(4, int(pw * sx)),
                    max(3, int(ph * sy)),
                )
                pygame.draw.rect(self._window, settings.MAROON, prect, border_radius=2)

            if hovered:
                hint = self._font_sm.render("Click to play", True, settings.YELLOW)
                self._window.blit(hint, (rect.centerx - hint.get_width() // 2, rect.bottom - 22))


    def level_card_rect(self, i: int) -> pygame.Rect:
        n       = len(settings.LEVELS)
        cw, ch  = 180, 210
        gap     = 25
        total_w = n * cw + (n - 1) * gap
        start_x = (self._world.window_w - total_w) // 2
        return pygame.Rect(start_x + i * (cw + gap), (self._world.window_h - ch) // 2, cw, ch)