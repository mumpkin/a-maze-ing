"""Cell Module for neighbours handling."""

from enum import Enum


class Compass(Enum):
    """Compass enum to represent cardinal direction."""

    NORTH = 8
    EAST = 4
    SOUTH = 2
    WEST = 1
