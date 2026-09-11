"""Modules that contains `Point` class definition."""

import math
from dataclasses import dataclass
from typing import Self, override


@dataclass
class Point:
    """
    Point for a 2D coordinate space.

    Attributes
    ----------
    x : int
        Positional value on the horizontal axis from left to right.
    y : int
        Positional value on the vertical axis from top to bikini bottom.

    Methods
    -------
    zero
        Return the `Point` instance with attributes set to 0.
    tranlate
        Do a point translation.
    scale
        Multiply self's attributes by the scale factor.
    distance
        Return the distance between self and a point.
    """

    x: int
    y: int

    @classmethod
    def zero(cls) -> Self:
        """Return the `Point` instance with attributes set to 0."""
        return cls(0, 0)

    def __str__(self) -> str:
        """Allow Point to be returned as a str for display purposes."""
        return f"[x={self.x},y={self.y}]"

    def __add__(self, value: "Point") -> "Point":
        """Return self+value.

        Parameters
        ----------
        value : Point
            Another Point instance whose attributes are added
            to self's attributes in the creation a new point instance

        Returns
        -------
        Point
            A new Point instance with `x=self.x + value.x, y=self.y + value.y`
            as its attributes
        """
        return Point(x=self.x + value.x, y=self.y + value.y)

    def __mul__(self, value: int) -> "Point":
        """Return self * value.

        Parameters
        ----------
        value : Point
            Another Point instance whose attributes are multiplied to
            self's attributes in the creation a new point instance

        Returns
        -------
        Point
            A new Point instance with `x=self.x * value.x, y=self.y * value.y`
            as its attributes
        """
        return Point(x=self.x * value, y=self.y * value)

    @override
    def __eq__(self, value: object) -> bool:
        """Return self == value.

        Parameters
        ----------
        value : Point
            Another Point instance whose attributes are Compared to
            self's attributes

        Returns
        -------
        bool
            `True if (self.x == value.x and self.y == value.y) else False`
        """
        if not isinstance(value, Point):
            return NotImplemented
        return self.x == value.x and self.y == value.y

    def translate(self, point: "Point") -> None:
        """
        Do a point translation by adding another Point's attributes to self's.

        Parameters
        ----------
        point : Point
            Point instance whose attributes will be added to self's.
        """
        self.x += point.x
        self.y += point.y

    def scale(self, factor: int) -> None:
        """Multiply self's attributes by the scale factor.

        Parameters
        ----------
        factor : int
            Scale factor.
        """
        self.x *= factor
        self.y *= factor

    def distance(self, point: "Point") -> int:
        """
        Return the distance between self and a point.

        Parameters
        ----------
        point : Point
            Point instance to which we want to calculate self's distance.
        """
        return int(
            math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)
        )
