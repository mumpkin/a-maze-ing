"""MazeGenerator definition."""

from abc import ABC, abstractmethod
from typing import Optional

import globals
from enums import CellState
from utils import Point, RenderEngine

from .cell import Cell


class MazeGenerator(ABC):
    """Abstract maze generator that implement maze generation tools."""

    def __init__(self) -> None:
        """MazeGenerator default constructor."""
        self.grid: list[Cell] = []
        self.optimal_path: list[Cell] = []
        self._init_maze()

    def _instanciate_cells(self) -> None:
        """Instancate cells in self maze."""
        for i in range(globals.config.width * globals.config.height):
            self.grid.append(
                Cell(
                    Point(
                        x=i % globals.config.width,
                        y=i // globals.config.width,
                    )
                )
            )

    def _define_neighbourhood(self) -> None:
        """Set cells neighbours."""
        for cell in self.grid:
            for neighbour in self.grid:
                cell.add_neighbour(neighbour)

    def _ft_lock(self) -> None:
        """Set cells state to LOCK to draw 42 symbol."""
        if globals.config.width >= 9 and globals.config.height >= 7:
            center: Point = Point(
                x=globals.config.width // 2, y=globals.config.height // 2
            )
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

    def _init_maze(self) -> None:
        """Initialize default maze to prepare generation."""
        self._instanciate_cells()
        self._define_neighbourhood()
        self._ft_lock()
        pass

    def write_output(self) -> None:
        """Write the maze output into the filename."""
        try:
            with open(globals.config.output_file, "w") as file:
                for i in range(globals.config.height):
                    line: list[Cell] = sorted(
                        [cell for cell in self.grid if cell.pos.y == i],
                        key=lambda cell: cell.pos.x,
                    )
                    print(
                        "".join([cell.conns_to_hexa() for cell in line]),
                        file=file,
                    )
        except Exception as fe:
            print(fe)

    @abstractmethod
    def generate(self, renderer: Optional[RenderEngine] = None) -> None:
        """Generate the maze."""
        pass
