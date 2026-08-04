"""Modules that contains `Point` class definition."""

import math
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

    def __add__(self, point: Point) -> Point:
        """."""
        return Point(x=self.x + point.x, y=self.y + point.y)

    def add(self, point: Point) -> None:
        """."""
        self.x += point.x
        self.y += point.y

    def __mul__(self, value: int) -> Point:
        """."""
        return Point(x=self.x * value, y=self.y * value)

    def scale(self, nb: int) -> None:
        """."""
        self.x *= nb
        self.y *= nb

    def distance_to(self, point: Point) -> int:
        """."""
        return int(
            math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)
        )
