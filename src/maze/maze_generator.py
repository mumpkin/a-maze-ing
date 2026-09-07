"""MazeGenerator definition."""

from abc import ABC, abstractmethod

import globals
import utils
from enums import CellState
from utils import Point

from .cell import Cell


class MazeGenerator(ABC):
    """Abstract maze generator that implement maze generation tools.

    Attributes
    ----------
    grid : list[Cell]
        Grid that represent maze's cells.
    optimal_path : list[Cell]
        List of cell that represent maze optimal resolution path.

    Methods
    -------
    init_maze
        Initialize maze corresponding configuration.
    save
        Save the maze information in an output file.
    generate
        Generate the maze's grid by making connections between cells.
    """

    def __init__(self) -> None:
        """MazeGenerator default constructor."""
        self.grid: list[Cell] = []
        self.optimal_path: list[Cell] = []

    def init_maze(self) -> None:
        """Initialize default maze to prepare generation."""
        self.grid = []
        self._instanciate_cells()
        self._define_neighbourhood()
        self._ft_lock()

    def save(self) -> None:
        """Save the maze information in an output file."""
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
    def generate(self, engine: utils.RenderEngine | None = None) -> None:
        """Generate the maze's grid by making connections between cells.

        Parameters
        ----------
        engine : RenderEngine, default=None
            Engine instance used to render the maze's grid at each generation
            steps.
        """
        pass

    def _instanciate_cells(self) -> None:
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
        for cell in self.grid:
            for neighbour in self.grid:
                cell.add_neighbour(neighbour)

    def _ft_lock(self) -> None:
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
