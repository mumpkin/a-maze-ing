"""."""

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

    def _validate_neighbouring(
        self, neighbouring_cell: Self
    ) -> Compass | None:
        """Return a Compass direction if neighbouring_cell is."""
        diff_x = self.pos.x - neighbouring_cell.pos.x
        diff_y = self.pos.y - neighbouring_cell.pos.y
        if diff_x == 0:
            if diff_y == 1 and self.pos.y < config.height:
                return Compass.NORTH
            if diff_y == -1 and self.pos.y > 0:
                return Compass.SOUTH
        if diff_y == 0:
            if diff_x == 1 and self.pos.x < config.width:
                return Compass.EAST
            if diff_x == -1 and self.pos.x > 0:
                return Compass.WEST
        return None

    def get_random_neighbour(self) -> Optional[tuple[Compass, Self]]:
        """."""
        idle_neighbours = [
            n
            for n in self._neighbours.items()
            if n[1] is not None and n[1].state == CellState.IDLE
        ]
        if len(idle_neighbours) == 0:
            return None
        # compass_dir, neighbour = random.choice(
        #      list(self._neighbours.items())
        # )
        compass_dir, neighbour = random.choice(idle_neighbours)
        while not neighbour or neighbour.state != "idle":
            compass_dir, neighbour = random.choice(idle_neighbours)
        #   compass_dir, neighbour = random.choice(
        #       list(self._neighbours.items())
        #   )
        return (compass_dir, neighbour)

    def get_neighbours(self) -> dict[Compass, Optional[Self]]:
        """Return the direct cell neighbours list."""
        return self._neighbours

    def set_neighbours(self, neighbouring_cell: Self) -> None:
        """Set the list of direct neighbours of this cell."""
        relative_pos = self._validate_neighbouring(neighbouring_cell)
        if relative_pos:
            self._neighbours[relative_pos] = neighbouring_cell

    def get_connections(self) -> int:
        """Return the value of cells connected to this one."""
        # return self._connections
        val: int = 0
        for k, v in self._connections.items():
            if v is True:
                val += int(k.value)
        return val

    def set_connection(self, pos: Compass) -> None:
        """Add the given cell to the list of connected cells."""
        self._connections[pos] = True

    def hexa_compass(self) -> int:
        """."""
        # decimal_value = sum([n.value for n in self._connections.keys()])
        decimal_value: int = self.get_connections()
        return int(decimal_value)
