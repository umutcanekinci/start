# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] – 2026-08-12

### Added

- Startup splash screen.
- CI workflow running `pygamine`'s test suite, a real app-level test suite covering physics, combat
  and AI, and an app-level smoke test that boots `Game()` and cycles every state.
- itch.io/storefront cover art.

### Changed

- Replaced unlicensed music with CC BY-SA 4.0 tracks by wyver9, and unlicensed background/platform
  art with CC0 parallax background and tiled ground.
- Renamed the `pygame_core` submodule/dependency to `pygamine`.
- Converged `pygame_core` with sibling projects; letterboxing now lives in Hunted itself.

### Fixed

- Editable `pygame-core` install not actually taking effect.
- Stale sibling-project references in `CLAUDE.md`.

## [0.1.0] – 2026-07-07

Initial release. Renamed from an earlier prototype ("start") to The Hunted, migrated onto
`pygame_core` with a single-player AI opponent mode, PyInstaller build/release automation, and
itch.io publishing.
