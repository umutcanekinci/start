# The Hunted

My first pygame project. A local 1-or-2-player platformer where one player is the vampire and the other is the peasant. Each round the role assignments are randomised.

![Gameplay](docs/preview.gif)

## Gameplay

- In every round, one player becomes the **vampire** and the other a **peasant**, chosen randomly.
- The vampire is **faster** and wins by catching/touching the peasant.
- Only the peasant can **fire bullets**.
- 1-player mode pits you against a built-in **AI opponent** with separate vampire / peasant behaviours.

### Screenshots

| Menu | Level select | Round in progress |
|------|--------------|-------------------|
| ![](docs/screenshot-1.png) | ![](docs/screenshot-2.png) | ![](docs/screenshot-3.png) |

### Controls

| Action | Player 1 | Player 2 |
|---|---|---|
| Move | Arrow keys | WASD |
| Jump | Up arrow | W |
| Fire | Right Ctrl | Space |

In 1-player mode you control **both keysets** and play against the AI.

## Requirements

- Python 3.12+
- [pygame-ce](https://github.com/pygame-community/pygame-ce) (resolved automatically from `pyproject.toml` / `uv.lock`)
- [uv](https://docs.astral.sh/uv/) (optional but recommended)

## Running

```bash
git clone --recurse-submodules https://github.com/umutcanekinci/hunted.git
cd hunted
uv sync
uv run python __main__.py
```

If you forgot `--recurse-submodules`: `git submodule update --init`.

Without `uv`: `pip install .` then `python __main__.py`.

## Project layout

```
__main__.py            Entry point — injects src/ + src/pygame_core/ into sys.path
src/game.py            Game class — state machine over menu / level-select / game
src/world.py           GameWorld dataclass (platforms, bullets, window dims)
src/entities.py        Player, Platform, Projectile
src/combat.py          Bullet physics + round transitions
src/input_handler.py   KeyboardInputHandler + AIInputHandler protocols
src/menu.py            Main-menu drawing + button states
src/renderer.py        Level-select + in-game drawing
src/audio.py           Menu / game music
src/cursor.py          Custom multi-state cursor
src/settings.py        Physics, combat, colors, and 3 level layouts
src/pygame_core/       Engine submodule (used only for Application + Mouse + GameObject)
assets/                Images and sounds
```

See [CLAUDE.md](CLAUDE.md) for the full architecture overview.

## Contributing

1. Fork this repository.
2. Clone your fork: `git clone --recurse-submodules https://github.com/<you>/hunted.git`
3. Create a branch: `git checkout -b feature/<your-feature>`
4. Commit + push: `git commit -am "<message>" && git push origin feature/<your-feature>`
5. Open a pull request.

## Author

Umutcan Ekinci — [umutcannekinci@gmail.com](mailto:umutcannekinci@gmail.com)

See also the [contributors](https://github.com/umutcanekinci/hunted/contributors).

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file.
