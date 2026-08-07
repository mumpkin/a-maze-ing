"""CellState enum."""

from enum import Enum


class CellState(str, Enum):
    """Possible states of a Cell."""

    IDLE = "idle"
    VISITED = "visited"
    LOCKED = "locked"
