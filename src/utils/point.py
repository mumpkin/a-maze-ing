"""Modules that contains `Point` class definition."""

from dataclasses import dataclass
from typing import Self


@dataclass
class Point:
    """
    Point for a 2D coordinate space.

    Keyword attributes:
    x: int -- Positional value on the horizontal axis from left to right.
    y: int -- Positional value on the vertical axis from top to bikini bottom.
    """

    x: int
    y: int

    @classmethod
    def zero(cls) -> Self:
        """Return the `Point` instance with attributes set to 0."""
        return cls(0, 0)
