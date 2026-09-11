"""MazeGenerator definition."""

from abc import ABC, abstractmethod
from sys import stdout
from time import sleep

from ..enums.cell_state import CellState
from ..enums.compass import Compass
from ..globals.config import config
from ..utils import render
from ..utils.point import Point
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
        self.optimal_path = []
        self._instanciate_cells()
        self._define_neighbourhood()
        self._ft_lock()

    def save(self) -> None:
        """Save the maze information in an output file."""
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

                print(file=file)
                print(f"{config.entry.x},{config.entry.y}", file=file)
                print(f"{config.exit.x},{config.exit.y}", file=file)
                print(self._get_optimal_as_cardinal(), file=file)

        except Exception as fe:
            print(fe)

    def _get_optimal_as_cardinal(self) -> str:
        result: list[str] = []
        current_cell: Cell = self.optimal_path.pop(0)

        while len(self.optimal_path) != 0:
            for compass, cell in current_cell.get_neighbours().items():
                if cell in self.optimal_path:
                    match compass:
                        case Compass.NORTH:
                            result.append("N")
                        case Compass.EAST:
                            result.append("E")
                        case Compass.SOUTH:
                            result.append("S")
                        case Compass.WEST:
                            result.append("W")
                    current_cell = self.optimal_path.pop(0)
        return "".join(result)

    @abstractmethod
    def generate(self, engine: render.RenderEngine | None = None) -> None:
        """Generate a maze.

        The generation follows a inspired logic from the
        recursive division algorithm.

        Parameters
        ----------
        engine : `RenderEngine`
            Passing this argument into the program allows to render the maze
            step-by-step.
        """
        pass

    def compute_optimal_path(
        self, engine: render.RenderEngine | None = None
    ) -> None:
        """Compute the optimal path from the grid.

        Parameters
        ----------
        engine : RenderEngine
            Used for step-by-step generation.
        """
        entry = [c for c in self.grid if c.pos == config.entry][0]
        exit = [c for c in self.grid if c.pos == config.exit][0]
        paths: list[list[Cell]] = [[entry]]
        has_found_optimal_path = False
        while not has_found_optimal_path:
            for path in paths:
                curr_cell = path[-1]
                curr_cell.state = CellState.VISITING
                possible_cells = [
                    cell
                    for dir, cell in curr_cell.get_neighbours().items()
                    if cell not in path
                    and curr_cell.get_connections()[dir]
                    and cell
                    and cell.state != CellState.VISITING
                ]
                for n in possible_cells:
                    new_path = [*path, n]
                    if n:
                        n.state = CellState.VISITING
                    paths.append(new_path)
                    if engine is not None:
                        _ = stdout.write("\033[H")
                        _ = stdout.flush()
                        engine.render()
                        sleep(config.delay)
            for path in paths:
                if exit in path:
                    self.optimal_path = self._return_optimal_path(paths)
                    has_found_optimal_path = True
                    break
        self._clear_visited()

    def _return_optimal_path(self, paths: list[list[Cell]]) -> list[Cell]:
        exit = [c for c in self.grid if c.pos == config.exit][0]
        legal_paths = [p for p in paths if exit in p]
        legal_paths.sort(key=len)
        return legal_paths[0][: legal_paths[0].index(exit) + 1]

    def _clear_visited(self) -> None:
        for c in self.grid:
            if c.state == CellState.VISITING:
                c.state = CellState.VISITED

    def _instanciate_cells(self) -> None:
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
        for cell in self.grid:
            for neighbour in self.grid:
                cell.add_neighbour(neighbour)

    def _ft_lock(self) -> None:
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
                if (
                    locker + center == config.entry
                    or locker + center == config.exit
                ):
                    raise Exception(
                        "ENTRY and EXIT can't be equal:\n"
                        + "\n".join(
                            [
                                f"- {p.x + center.x},{p.y + center.y}"
                                for p in ft_pos
                            ]
                        )
                        + f"\n inside a `W={config.width} x H={config.height}`"
                        + " maze.",
                    )
                for cell in self.grid:
                    from_center = locker + center
                    if (
                        cell.pos.x == from_center.x
                        and cell.pos.y == from_center.y
                    ):
                        cell.state = CellState.LOCKED
