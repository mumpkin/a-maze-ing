"""Modules that contains `Point` class definition."""

import math
from dataclasses import dataclass
from typing import Self, override


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

    def __add__(self, value: "Point") -> "Point":
        """Return self+value."""
        return Point(x=self.x + value.x, y=self.y + value.y)

    def __mul__(self, value: int) -> "Point":
        """Return self*value."""
        return Point(x=self.x * value, y=self.y * value)

    @override
    def __eq__(self, value: object) -> bool:
        """Return self==value."""
        if not isinstance(value, Point):
            return NotImplemented
        return self.x == value.x and self.y == value.y

    def translate(self, point: "Point") -> None:
        """
        Do a point translation.

        Keyword parameters:
        point: Point -- Point that contains translation values.
        """
        self.x += point.x
        self.y += point.y

    def scale(self, factor: int) -> None:
        """
        Do an uniform scaling by multiplying the point by the scale factor.

        Keyword parameters:
        factor: int -- Scale factor.
        """
        self.x *= factor
        self.y *= factor

    def distance(self, point: "Point") -> int:
        """
        Return the distance between self and a point.

        Keyword parameters:
        point: Point -- Point to get distance to.
        """
        return int(
            math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)
        )
