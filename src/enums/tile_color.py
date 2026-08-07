"""TileColor enum."""

from enum import Enum


class TileColor(str, Enum):
    """Possible tile colors."""

    DEFAULT = "\033[49m"
    WALL = "\033[100m"
    ENTRY = "\033[102m"
    EXIT = "\033[101m"
    LOCKED = "\033[106m"
    MAZE = "\033[107m"
    PATH = "\033[105m"
