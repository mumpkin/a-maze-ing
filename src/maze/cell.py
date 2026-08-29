"""Cell definition."""

import json
import random
from typing import Self

from enums import CellState, Compass
from utils import Point


class Cell:
    """Representation of a cell in the maze's grid."""

    def __init__(self, pos: Point) -> None:
        self.pos: Point = pos
        self.state: CellState = CellState.IDLE
        self._neighbours: dict[Compass, Self | None] = {
            Compass.NORTH: None,
            Compass.EAST: None,
            Compass.SOUTH: None,
            Compass.WEST: None,
        }
        self._connections: dict[Compass, bool] = {
            Compass.NORTH: False,
            Compass.EAST: False,
            Compass.SOUTH: False,
            Compass.WEST: False,
        }

    def toJSON(self) -> str:
        """."""
        return json.dumps({**self.pos.__dict__, "state": self.state.value})

    def _validate_neighbouring(self, cell: Self) -> Compass | None:
        """
        Return a Compass direction if neighbouring_cell is.

        Keyword parameter:
        cell: Cell -- Cell to validate and to get compass direction.
        """
        diff_x = self.pos.x - cell.pos.x
        diff_y = self.pos.y - cell.pos.y
        if diff_x == 0:
            if diff_y == -1:
                return Compass.SOUTH
            if diff_y == 1:
                return Compass.NORTH
        if diff_y == 0:
            if diff_x == -1:
                return Compass.EAST
            if diff_x == 1:
                return Compass.WEST
        return None

    def get_random_neighbour(self) -> tuple[Compass, Self]:
        """Return a cell that neighbouring the current cell."""
        neighbours: list[tuple[Compass, Self]] = [
            (c, n) for c, n in self._neighbours.items() if n is not None
        ]

        return random.choice(neighbours)

    def get_neighbours(self) -> dict[Compass, Self | None]:
        """Return the direct cell neighbours list."""
        return self._neighbours

    def add_neighbour(self, cell: Self) -> None:
        """
        Add a new valid cell as self neighbour.

        Keyword parameters:
        cell: Cell -- Cell to add as neighbour if its position is valid.
        """
        compass_dir = self._validate_neighbouring(cell)
        if compass_dir:
            self._neighbours[compass_dir] = cell

    def get_connections(self) -> dict[Compass, bool]:
        """Return the list of cells connected to this one."""
        return self._connections

    def set_connection(self, direction: Compass) -> None:
        """
        Connect the given cell to the cell in the specified direction.

        Keyword parameters:
        dir: Compass -- Compass direction to set to `True`.
        """
        neighbour = self._neighbours[direction]
        if neighbour and neighbour.state != CellState.LOCKED:
            self._connections[direction] = True
            for dir, val in neighbour._neighbours.items():
                if val == self:
                    neighbour._connections[dir] = True

    def unset_connection(self, dir: Compass) -> None:
        """
        Remove the connection to the given direction.

        Keyword parameters:
        dir: Compass -- Compass direction to set to `True`.
        """
        neighbour = self._neighbours[dir]
        if neighbour:
            self._connections[dir] = False
            for dir, val in neighbour._neighbours.items():
                if val == self:
                    neighbour._connections[dir] = False

    def unset_all_connections(self) -> None:
        """Remove all connections linked to the current cell in both ways."""
        for c in [Compass.NORTH, Compass.EAST, Compass.SOUTH, Compass.WEST]:
            self.unset_connection(c)

    def conns_to_decimal(self) -> int:
        """Return the decimal value related to the cell connections."""
        return sum([k.value for k, v in self._connections.items() if v])

    def conns_to_hexa(self) -> str:
        """Return the hexadecimal value related to the cell connections."""
        decimal_value = self.conns_to_decimal()
        return hex(decimal_value).removeprefix("0x").upper()
