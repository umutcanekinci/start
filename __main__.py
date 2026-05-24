import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from game import Game

if __name__ == "__main__":
    Game().run()