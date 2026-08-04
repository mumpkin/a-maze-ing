"""."""

import json
import math
from abc import ABC, abstractmethod
from typing import Any

from enums import CellState
from globals import config
from utils import Point

from .cell import Cell


class MazeGenerator(ABC):
    """."""

    def __init__(self) -> None:
        """."""
        self.grid: list[Cell] = []
        self._init_grid()
        self._ft_lock()

    def _instanciate_cells(self) -> None:
        """."""
        for i in range(config.width * config.height):
            self.grid.append(
                Cell(
                    Point(
                        x=i % config.width,
                        y=i // config.width,
                    )
                )
            )

    def _define_neighbourhood(self) -> None:
        """."""
        for cell in self.grid:
            for neighbour in self.grid:
                cell.set_neighbours(neighbour)

    def _ft_lock(self) -> None:
        """."""

        if config.width >= 9 and config.height >= 7:
            center: Point = Point(x=config.width // 2, y=config.height // 2)
            ft_pos = [
                *[Point(x=-3, y=a) for a in range(-2, 1)],
                Point(x=-2, y=0),
                *[Point(x=-1, y=a) for a in range(0, 3)],
                *[Point(x=a, y=-2) for a in range(1, 4)],
                Point(x=3, y=-1),
                *[Point(x=a, y=0) for a in range(1, 4)],
                Point(x=1, y=1),
                *[Point(x=a, y=2) for a in range(1, 4)],
            ]
            for locker in ft_pos:
                for cell in self.grid:
                    from_center = locker + center
                    if (
                        cell.pos.x == from_center.x
                        and cell.pos.y == from_center.y
                    ):
                        cell.state = CellState.LOCKED
        for index, cell in enumerate(self.grid):
            if index % config.width == 0:
                print("\n", end="")
            print("██" if cell.state != CellState.LOCKED else "  ", end="")

    def _init_grid(self) -> None:
        """."""
        self._instanciate_cells()
        self._define_neighbourhood()
        pass

    # @abstractmethod
    # def build_maze(self) -> Any:
    #     """Build the maze."""
    #     pass

    def write_output(self) -> None:
        """Write the maze output into the filename."""
        try:
            pass
            # with open(self.get_config_key('OUTPUT_FILENAME'), 'w') as file:
        except FileNotFoundError as fe:
            print(fe)
