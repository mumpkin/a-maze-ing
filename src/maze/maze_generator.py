"""MazeGenerator definition."""

from abc import ABC, abstractmethod
from typing import Callable, Optional

from enums import CellState
from globals import config
from utils import Point

from .cell import Cell


class MazeGenerator(ABC):
    """Abstract maze generator that implement maze generation tools."""

    def __init__(self) -> None:
        """MazeGenerator default constructor."""
        self.grid: list[Cell] = []
        self._init_grid()

    def _instanciate_cells(self) -> None:
        """Instancate cells in self maze grid."""
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
        """Set cells neighbours."""
        for cell in self.grid:
            for neighbour in self.grid:
                cell.add_neighbour(neighbour)

    def _ft_lock(self) -> None:
        """Set cells state to LOCK to draw 42 symbol."""
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

    def _init_grid(self) -> None:
        """Initialize default grid to prepare maze generation."""
        self._instanciate_cells()
        self._define_neighbourhood()
        self._ft_lock()
        pass

    def write_output(self) -> None:
        """Write the maze output into the filename."""
        try:
            with open(config.output_file, "w") as file:
                for i in range(config.height):
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
    def generate(self, renderer: Optional[Callable]) -> None:
        """Generate the maze."""
        pass
