"""Cell definition."""

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

    def _validate_neighbouring(self, cell: Self) -> Compass | None:
        """
        Return a Compass direction if neighbouring_cell is.

        Parameters
        ----------
        cell: `Cell`
            Cell to check wheter it is a neighbour to the current cell

        Return
        ---------
        If the Cell object passed in argument is a neighbour,
        return its direction as a `Compass`, otherwise `None`
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
        """Return a cell in the neighbouring of the current cell.

        Return
        ---------
        A `tuple` containing the direction of the neighbour along with
        the neighbour itself
        """
        neighbours: list[tuple[Compass, Self]] = [
            (c, n) for c, n in self._neighbours.items() if n is not None
        ]

        return random.choice(neighbours)

    def get_neighbours(self) -> dict[Compass, Self | None]:
        """Return the current cell's neighbours list.

        Return
        ----------
        A `dictionnary` containing all neighbours of the current cell
        """
        return self._neighbours

    def add_neighbour(self, cell: Self) -> None:
        """
        Add a new valid cell as self neighbour.

        Parameters
        ----------
        cell: `Cell`
            Cell to add as neighbour to the current cell
            if its position is valid.
        """
        compass_dir = self._validate_neighbouring(cell)
        if compass_dir:
            self._neighbours[compass_dir] = cell

    def get_connections(self) -> dict[Compass, bool]:
        """Return the connectivity status between all neighbours to this cell.

        Return
        ----------
        A `dictionnary` containing four pairs of `Compass` : `bool`, the `bool`
        being the opening status in the direction pointed by `Compass`
        """
        return self._connections

    def set_connection(self, direction: Compass) -> None:
        """Connect the current cell to the cell in the specified direction.

        Parameters
        ----------
        direction: `Compass`
            Compass direction to set to `True`.
        """
        neighbour = self._neighbours[direction]
        if neighbour and neighbour.state != CellState.LOCKED:
            self._connections[direction] = True
            for dir, val in neighbour._neighbours.items():
                if val == self:
                    neighbour._connections[dir] = True

    def set_all_connections(self) -> None:
        """Connect all neighbours to the current cell."""
        for c in [Compass.NORTH, Compass.EAST, Compass.SOUTH, Compass.WEST]:
            self.set_connection(c)

    def unset_connection(self, direction: Compass) -> None:
        """Disconnect the current cell to the cell in the given direction.

        Parameters
        ----------
        direction: `Compass`
            Compass direction to set to `False`.
        """
        neighbour = self._neighbours[direction]
        if neighbour and neighbour.state != CellState.LOCKED:
            self._connections[direction] = False
            for dir, val in neighbour._neighbours.items():
                if val == self:
                    neighbour._connections[dir] = False

    def unset_all_connections(self) -> None:
        """Remove all connections bound to the current cell."""
        for c in [Compass.NORTH, Compass.EAST, Compass.SOUTH, Compass.WEST]:
            self.unset_connection(c)

    def conns_to_decimal(self) -> int:
        """Return the decimal value related to the cell connections.

        Return
        ----------
        A `int` ranging from 0 to 15 depending on the connections
        bound to the current cell
        """
        return sum([k.value for k, v in self._connections.items() if v])

    def conns_to_hexa(self) -> str:
        """Return the hexadecimal value related to the cell connections.

        Return
        ----------
        A `str` representing a hexadecimal number depending on the connections
        bound to the current cell
        """
        decimal_value = self.conns_to_decimal()
        return hex(15 - decimal_value).removeprefix("0x").upper()
