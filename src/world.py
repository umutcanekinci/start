from dataclasses import dataclass, field


@dataclass
class GameWorld:
    window_w: int
    window_h: int
    two_players: bool = True
    platforms: list = field(default_factory=list)
    bullets: list = field(default_factory=list)