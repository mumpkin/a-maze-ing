"""Cell Module for neighbours handling."""

from enum import Enum


class Compass(Enum):
    """Compass enum to represent cardinal direction."""

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
