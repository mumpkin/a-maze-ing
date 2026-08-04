"""."""

import json
import random
from typing import Optional, Self

from enums import CellState, Compass
from globals import config
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
        return json.dumps({**self.pos.__dict__, "state": self.state.value})

    def _validate_neighbouring(
        self, neighbouring_cell: Self
    ) -> Compass | None:
        """Return a Compass direction if neighbouring_cell is."""
        diff_x = self.pos.x - neighbouring_cell.pos.x
        diff_y = self.pos.y - neighbouring_cell.pos.y
        if diff_x == 0:
            if diff_y == 1:
                return Compass.NORTH
            if diff_y == -1:
                return Compass.SOUTH
        if diff_y == 0:
            if diff_x == 1:
                return Compass.EAST
            if diff_x == -1:
                return Compass.WEST
        return None

    def get_random_neighbour(self) -> Optional[tuple[Compass, Self]]:
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

    def set_neighbours(self, neighbouring_cell: Self) -> None:
        """Set the list of direct neighbours of this cell."""
        relative_pos = self._validate_neighbouring(neighbouring_cell)
        if relative_pos:
            self._neighbours[relative_pos] = neighbouring_cell

    def get_connections(self) -> dict[Compass, bool]:
        """Return the list of cells connected to this one."""
        return self._connections

    def set_connection(self, pos: Compass) -> None:
        """Add the given cell to the list of connected cells."""
        self._connections[pos] = True

    def hexa_compass(self) -> int:
        """Return the hexadecimal value related to the cell connections."""
        decimal_value = sum([n.value for n in self._connections.keys()])
        return int(
            str(decimal_value),
            base=16,
        )
