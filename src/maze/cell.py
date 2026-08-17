"""Cell definition."""

import json
import random
from typing import Optional, Self

from enums import CellState, Compass
from utils import Point


class Cell:
    """Representation of a cell in the maze's grid."""

    def __init__(self, pos: Point) -> None:
        self.pos: Point = pos
        self.state: CellState = CellState.IDLE
        self._neighbours: dict[Compass, Optional[Self]] = {
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

    def get_random_idle_neighbour(self) -> Optional[tuple[Compass, Self]]:
        """Return an idle cell that neighbouring the current cell."""
        idle_neighbours = [
            n
            for n in self._neighbours.items()
            if n[1] is not None and n[1].state == CellState.IDLE
        ]
        if len(idle_neighbours) == 0:
            return None
        compass_dir, neighbour = random.choice(idle_neighbours)
        while not neighbour or neighbour.state != "idle":
            compass_dir, neighbour = random.choice(idle_neighbours)
        return (compass_dir, neighbour)

    def get_neighbours(self) -> dict[Compass, Optional[Self]]:
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
        self._connections[dir] = False
        neighbour = self._neighbours[dir]
        if neighbour:
            for dir, val in neighbour._neighbours.items():
                if val == self:
                    neighbour._connections[dir] = False

    def unset_all_connections(self) -> None:
        """Remove all connections linked to the current cell in both ways."""
        for c in [Compass.NORTH, Compass.EAST, Compass.SOUTH, Compass.WEST]:
            self.unset_connection(c)

    def conns_to_hexa(self) -> str:
        """Return the hexadecimal value related to the cell connections."""
        decimal_value = sum(
            [k.value for k, v in self._connections.items() if v]
        )
        return hex(decimal_value).removeprefix("0x").upper()
