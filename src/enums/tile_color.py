"""TileColor enum."""

from enum import Enum


class TileColor(str, Enum):
    """Possible tile colors."""

    TRANSPARENT = "\033[49m"
    ENTRY = "\033[102m"
    EXIT = "\033[101m"
    IDLE = "\033[100m"
    LOCKED = "\033[106m"
    VISITED = "\033[107m"
    OPTIMAL_PATH = "\033[105m"
