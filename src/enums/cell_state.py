"""."""

from enum import Enum


class CellState(str, Enum):
    """."""

    IDLE = "idle"
    VISITED = "visited"
    LOCKED = "locked"
