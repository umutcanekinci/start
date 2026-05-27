# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Game

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game (__main__.py adds src/ and src/pygame_core/ to sys.path)
python __main__.py
```

There are no automated tests or lint configurations in this project.

## Architecture Overview

### Entry Point and Game Class

`__main__.py` injects `src/` and `src/pygame_core/` into `sys.path`, then calls `Game().run()`. `src/game.py` defines `Game`, which inherits from `pygame_core.Application`.

Unlike the project's sibling games (2048-idle-evolution, tower-defense), `start` does **not** use `PanelManager` / `PanelLoaderExt` / YAML config — UI is hand-rolled in `src/menu.py` and `src/renderer.py`, and configuration lives in `src/settings.py` as plain Python constants.

### pygame_core — Shared Submodule

`src/pygame_core/` is a git submodule pointing at `https://github.com/umutcanekinci/pygame-core.git`. The same submodule is used by `2048-idle-evolution`, `terraria`, and `tower-defense`. Changes here propagate to all four projects — bump via `scripts/sync-pygame-core.bat`.

This project uses only a small slice of pygame_core: `Application`, `Mouse`, and `GameObject` (for `Cursor`).

### Game State Machine

`Game` dispatches on `self._state`, which takes one of three string constants:

| State | Driven by | Drawn by |
|-------|-----------|----------|
| `STATE_MENU` | `_handle_menu_event` / `_update_menu` | `Menu.draw()` |
| `STATE_LEVEL_SELECT` | `_handle_level_select_event` / `_update_level_select` | `GameRenderer.draw_level_select()` |
| `STATE_GAME` | `_update_game` (no event handler — input is polled in `Player`) | `GameRenderer.draw_game()` |

State transitions happen in-band inside the handlers (e.g. `_update_menu` flips to `STATE_LEVEL_SELECT` after a countdown).

### Subsystems (composed in `Game.__init__`)

| Attribute | Class | Responsibility |
|-----------|-------|----------------|
| `_world` | `GameWorld` (dataclass, `src/world.py`) | Window size, platforms list, bullets list, `two_players` flag |
| `_menu` | `Menu` (`src/menu.py`) | Main-menu buttons + countdown frames + button-state visuals |
| `_audio` | `AudioManager` (`src/audio.py`) | Two music tracks (menu / game) on the default mixer |
| `_renderer` | `GameRenderer` (`src/renderer.py`) | Level-select and in-game drawing |
| `_combat` | `CombatSystem` (`src/combat.py`) | Bullet physics, contact damage, round transitions |
| `_cursor` | `Cursor` (`src/cursor.py`, extends `pygame_core.GameObject`) | Custom mouse cursor with normal/click/click2/help/writing states |

### Players and Input

`Player` (`src/entities.py`) has two roles toggled by `be_vampire()` / `be_peasant()` (loads different sprite sets + speed). `CombatSystem.begin_round()` randomly assigns vampire on each new round.

Input is dispatched through `InputHandler` (Protocol in `src/input_handler.py`):
- `KeyboardInputHandler(control)` where `control` is `"L"` (WASD + Space), `"R"` (Arrows + RCtrl), or `"RL"` (both keysets, used in 1-player mode).
- `AIInputHandler` drives the opponent in 1-player mode. It has separate vampire/peasant strategies and reads opponent position + platform layout to decide moves.

### Levels

`settings.LEVELS` defines three platform layouts (`Classic`, `Towers`, `Arena`). Level selection happens on `STATE_LEVEL_SELECT`; `_handle_level_select_event` rebuilds `_world.platforms` from `LEVELS[i]['platforms']` before entering the game.

### Assets

All images and sounds live under `assets/` (`assets/images/`, `assets/sounds/`). Loaded directly with `pygame.image.load()` / `pygame.mixer.Sound()` — there is no asset manifest. Naming conventions:
- `assets/images/vampire/R{i}E.png`, `L{i}E.png` for vampire walk frames (1-9)
- `assets/images/peasant/R{i}.png`, `L{i}.png` for peasant walk frames
- `assets/images/cursor/{normal,click,click2,help,writing}/N-{i}.png` etc.

### Persistence

None. Scores and round state are kept in memory only.

### What's missing relative to the modern sibling projects

This project predates the YAML-driven layout, the `app/domain/gameplay/ui` package split, and `pygame_core.AssetManager`. If extending significantly, consider porting it onto those patterns (see `2048-idle-evolution` / `tower-defense` for examples).
