"""ImperfectMazeGenerator definition."""

import random
from sys import stdout
from time import sleep
from typing import override

import globals
from enums import CellState, Compass
from utils import Point, RenderEngine

from . import MazeGenerator
from .cell import Cell


class ImperfectMazeGenerator(MazeGenerator):
    """Imperfect maze generator class."""

    def _find_large_rooms(self, cell: Cell) -> bool:
        """Check if the current cell is at the center of a 3x3 room.

        Parameters
        ----------
        cell: `Cell`
            The cell we want to check for being the center of a 3x3 open space.
        """
        n_neighbour = cell.get_neighbours()[Compass.NORTH]
        e_neighbour = cell.get_neighbours()[Compass.EAST]
        s_neighbour = cell.get_neighbours()[Compass.SOUTH]
        w_neighbour = cell.get_neighbours()[Compass.WEST]
        if not (n_neighbour and e_neighbour and s_neighbour and w_neighbour):
            return False
        if (
            all(cell.get_connections().values())
            and n_neighbour.get_connections()[Compass.EAST]
            and n_neighbour.get_connections()[Compass.WEST]
            and s_neighbour.get_connections()[Compass.EAST]
            and s_neighbour.get_connections()[Compass.WEST]
            and e_neighbour.get_connections()[Compass.NORTH]
            and e_neighbour.get_connections()[Compass.SOUTH]
            and w_neighbour.get_connections()[Compass.NORTH]
            and w_neighbour.get_connections()[Compass.SOUTH]
        ):
            return True
        return False

    def _anihilate_large_rooms(self) -> None:
        """I was loosing hope."""
        for c in self.grid:
            if self._find_large_rooms(c):
                random_direction = random.choice(
                    [Compass.NORTH, Compass.EAST, Compass.SOUTH, Compass.WEST]
                )
                c.unset_connection(random_direction)

    def _is_a_deadend(self, cell: Cell) -> bool:
        """Check if the cell passed in argument is a dead end.

        Parameters
        ----------
        cell: `Cell`
            The cell we want to check for being a dead end.
        """
        match cell.conns_to_decimal():
            case 0:
                return True
            case 1:
                return True
            case 2:
                return True
            case 4:
                return True
            case 8:
                return True
            case _:
                return False

    def _does_cell_have_locked_neighbour(self, cell: Cell) -> bool:
        """Check if the curent cell has any locked neighbours.

        Parameters
        ----------
        cell: `Cell`
            The cell whose neighbours we want to check the states.
        """
        neighbours = cell.get_neighbours()
        for _, v in neighbours.items():
            if v and v.state == CellState.LOCKED:
                return True
        return False

    def _open_closed_path(
        self,
        cell: Cell,
        closed_directions: list[Compass],
    ) -> None:
        """Open a random wall if a cell is considered a dead end.

        Parameters
        ----------
        cell: `Cell`
            A cell from the grid presenting a dead end.
        closed_directions: `list[Compass]`
            A list containing the possibly valid directions towards neighbours
            of the current cell to create a new path
        """
        for dir in closed_directions:
            neighbour = cell.get_neighbours()[dir]
            if (neighbour and neighbour.state == CellState.LOCKED) or (
                cell.get_connections()[dir]
                or cell.get_neighbours()[dir] is None
            ):
                closed_directions.remove(dir)
        if len(closed_directions) == 0:
            return
        for d in closed_directions:
            neighbour = cell.get_neighbours()[d]
            if (
                neighbour
                and neighbour.state == CellState.VISITED
                and self._is_a_deadend(neighbour)
            ):
                cell.set_connection(d)
                return
        legitimate_directions = random.sample(
            closed_directions, k=len(closed_directions)
        )
        for to_open in legitimate_directions:
            cell.set_connection(to_open)
            print(f"{to_open}--{cell.pos}--{cell.get_connections()}")
            if not self._is_a_deadend(cell):
                break

    def _eliminate_deadends(self, engine: RenderEngine | None) -> None:
        """Destroy dead ends by randomly hollowing walls.

        This method targets cells with only one connection and tries to connect
        the afore-mentionned cell with one of its neighbour.

        Parameters
        ----------
        engine: `RenderEngine`
            Passing this argument into the program allows to render the maze
            step-by-step
        """
        for cell in self.grid:
            if cell.state == CellState.LOCKED:
                continue
            match cell.conns_to_decimal():
                case 8:
                    closed_directions = [
                        Compass.NORTH,
                        Compass.EAST,
                        Compass.SOUTH,
                    ]
                    self._open_closed_path(cell, closed_directions)
                case 4:
                    closed_directions = [
                        Compass.NORTH,
                        Compass.EAST,
                        Compass.WEST,
                    ]
                    self._open_closed_path(cell, closed_directions)
                case 2:
                    closed_directions = [
                        Compass.NORTH,
                        Compass.SOUTH,
                        Compass.WEST,
                    ]
                    self._open_closed_path(cell, closed_directions)
                case 1:
                    closed_directions = [
                        Compass.EAST,
                        Compass.SOUTH,
                        Compass.WEST,
                    ]
                    self._open_closed_path(cell, closed_directions)
                case 0:
                    closed_directions = [
                        Compass.NORTH,
                        Compass.EAST,
                        Compass.SOUTH,
                        Compass.WEST,
                    ]
                    self._open_closed_path(cell, closed_directions)
                    self._open_closed_path(cell, closed_directions)
                case _:
                    if self._does_cell_have_locked_neighbour(cell):
                        closed_directions = [
                            Compass.NORTH,
                            Compass.EAST,
                            Compass.SOUTH,
                            Compass.WEST,
                        ]
                        self._open_closed_path(cell, closed_directions)
            self._render_progress(engine)

    def _define_horizontal_areas(
        self, original_area: dict[str, Point], starting_cell: Cell
    ) -> tuple[dict[str, Point], dict[str, Point]]:
        """Return the upper and lower areas after a horizontal split.

        Parameters
        ----------
        original_area: `dict[str, Point]`
            The area that is split into two parts by a horizontal line
        starting_cell: `Cell`
            The cell from wich we began splitting the previous area
        """
        upper_area: dict[str, Point] = dict(
            {
                "top-left": Point(
                    x=starting_cell.pos.x, y=original_area["top-left"].y
                ),
                "top-right": Point(
                    x=original_area["top-right"].x,
                    y=original_area["top-right"].y,
                ),
                "bottom-left": Point(
                    original_area["bottom-left"].x,
                    y=starting_cell.pos.y - 1,
                ),
                "bottom-right": Point(
                    x=starting_cell.pos.x,
                    y=starting_cell.pos.y - 1,
                ),
            }
        )
        lower_area: dict[str, Point] = dict(
            {
                "top-left": Point(
                    x=original_area["top-left"].x, y=starting_cell.pos.y
                ),
                "top-right": Point(
                    x=original_area["top-right"].x, y=starting_cell.pos.y
                ),
                "bottom-left": Point(
                    x=starting_cell.pos.x,
                    y=original_area["bottom-left"].y,
                ),
                "bottom-right": original_area["bottom-right"],
            }
        )
        return upper_area, lower_area

    def _define_vertical_areas(
        self, original_area: dict[str, Point], starting_cell: Cell
    ) -> tuple[dict[str, Point], dict[str, Point]]:
        """Return the upper and lower areas after a vertical split.

        Parameters
        ----------
        original_area: `dict[str, Point]`
            The area that is split into two parts by a vertical line
        starting_cell: `Cell`
            The cell from wich we began splitting the previous area
        """
        left_area: dict[str, Point] = dict(
            {
                "top-left": original_area["top-left"],
                "top-right": Point(
                    x=starting_cell.pos.x, y=original_area["top-right"].y
                ),
                "bottom-left": original_area["bottom-left"],
                "bottom-right": Point(
                    x=starting_cell.pos.x, y=original_area["bottom-right"].y
                ),
            }
        )
        right_area: dict[str, Point] = dict(
            {
                "top-left": Point(
                    x=starting_cell.pos.x + 1, y=original_area["top-left"].y
                ),
                "top-right": original_area["top-right"],
                "bottom-left": Point(
                    x=starting_cell.pos.x + 1,
                    y=original_area["bottom-left"].y,
                ),
                "bottom-right": original_area["bottom-right"],
            }
        )
        return left_area, right_area

    def _render_progress(self, engine: RenderEngine | None) -> None:
        """Display the progress in creating the maze in the terminal.

        Parameters
        ----------
        engine: `RenderEngine`
            Passing this argument into the program allows to render the maze
            step-by-step
        """
        if engine is not None:
            _ = stdout.write("\033[H")
            _ = stdout.flush()
            engine.render()
            sleep(globals.config.delay)

    def _horizontal_split(
        self,
        area_corners: dict[str, Point],
        direction: Compass,
        engine: RenderEngine | None,
    ) -> None:
        """Split horizontally the given area.

        Parameters
        ----------
        area: `dict[str, Point]`
            The area delimited by four coordinates from wich to create the
            next section
        direction: `Compass`
            Direction in wich the maze will be built
        engine: `RenderEngine`
            Passing this argument into the program allows to render the maze
            step-by-step
        """
        if (
            area_corners["bottom-left"].y - area_corners["top-left"].y < 1
            or area_corners["top-right"].x - area_corners["top-left"].x < 1
        ):
            return
        starting_cell = self.grid[
            area_corners["top-left"].x
            + random.randint(
                area_corners["top-left"].y + 1, area_corners["bottom-left"].y
            )
            * globals.config.width
        ]
        next_cell: Cell | None = starting_cell
        direction_to_unset = Compass.NORTH
        segments: list[list[Cell]] = []
        segment_cells: list[Cell] = []

        while next_cell and next_cell.pos.x <= area_corners["top-right"].x:
            if not (
                next_cell.pos == globals.config.entry
                or next_cell.pos == globals.config.exit
            ):
                if next_cell.state == CellState.VISITED:
                    segment_cells.append(next_cell)
                elif len(segment_cells) > 0:
                    segments.append(segment_cells)
                    segment_cells = []
                next_cell.unset_connection(direction_to_unset)
            next_cell = next_cell.get_neighbours()[direction]
            self._render_progress(engine)

        if len(segment_cells) > 0:
            segments.append(segment_cells)
        for segment_cells in segments:
            path_number = random.randint(1, max(1, len(segment_cells) // 2))
            random_sample = random.sample(segment_cells, k=max(1, path_number))
            for cell in random_sample:
                cell.set_connection(direction_to_unset)
                self._render_progress(engine)
        upper_area, lower_area = self._define_horizontal_areas(
            area_corners, starting_cell
        )
        self._render_progress(engine)
        self._dispatch_logical_split(upper_area, engine)
        self._dispatch_logical_split(lower_area, engine)

    def _vertical_split(
        self,
        area: dict[str, Point],
        direction: Compass,
        engine: RenderEngine | None,
    ) -> None:
        """Split vertically the given area.

        Parameters
        ----------
        area: `dict[str, Point]`
            The area delimited by four coordinates from wich to create the
            next section
        direction: `Compass`
            Direction in wich the maze will be built
        engine: `RenderEngine`
            Passing this argument into the program allows to render the maze
            step-by-step
        """
        if (
            area["bottom-left"].y - area["top-left"].y < 1
            or area["top-right"].x - area["top-left"].x < 1
        ):
            return
        starting_cell: Cell = self.grid[
            random.randint(area["top-left"].x + 1, area["top-right"].x - 1)
            + area["top-left"].y * globals.config.width
        ]
        next_cell: Cell | None = starting_cell
        direction_to_unset: Compass = Compass.EAST
        segments: list[list[Cell]] = []
        segment_cells: list[Cell] = []

        while next_cell and next_cell.pos.y <= area["bottom-left"].y:
            if not (
                next_cell.pos == globals.config.entry
                or next_cell.pos == globals.config.exit
            ):
                east_neighbour = next_cell.get_neighbours()[Compass.EAST]
                if next_cell.state == CellState.VISITED and not (
                    east_neighbour and east_neighbour.state == CellState.LOCKED
                ):
                    segment_cells.append(next_cell)
                elif len(segment_cells) > 0:
                    segments.append(segment_cells)
                    segment_cells = []
                next_cell.unset_connection(direction_to_unset)
            next_cell = next_cell.get_neighbours()[direction]
            self._render_progress(engine)

        if len(segment_cells) > 0:
            segments.append(segment_cells)
        for segment_cells in segments:
            path_number = random.randint(1, max(1, len(segment_cells) // 2))
            random_sample = random.sample(segment_cells, k=max(1, path_number))
            for cell in random_sample:
                cell.set_connection(direction_to_unset)
                self._render_progress(engine)
        left_area, right_area = self._define_vertical_areas(
            area, starting_cell
        )
        self._render_progress(engine)
        self._dispatch_logical_split(left_area, engine)
        self._dispatch_logical_split(right_area, engine)

    def _dispatch_logical_split(
        self, area: dict[str, Point], engine: RenderEngine | None
    ) -> None:
        """Select which split to perform next.

        If the areas width is higher than its width, split vertically.
        Otherwise split horizontally.

        Parameters
        ----------
        area: `dict[str, Point]`
            The area delimited by four coordinates from wich to create the
            next section
        engine: `RenderEngine`
            Passing this argument into the program allows to render the maze
            step-by-step
        """
        width = area["top-right"].x - area["top-left"].x
        height = area["bottom-left"].y - area["top-left"].y
        if width > height:
            self._vertical_split(area, Compass.SOUTH, engine)
        else:
            self._horizontal_split(area, Compass.EAST, engine)

    def _imperfect_generation(self, engine: RenderEngine | None) -> None:
        """Perform the creation of the maze.

        Parameters
        ----------
        engine: `RenderEngine`
            Passing this argument into the program allows to render the maze
            step-by-step
        """
        corners = dict(
            {
                "top-left": Point(x=0, y=0),
                "top-right": Point(x=globals.config.width - 1, y=0),
                "bottom-left": Point(x=0, y=globals.config.height - 1),
                "bottom-right": Point(
                    x=globals.config.width - 1, y=globals.config.height - 1
                ),
            }
        )
        self._dispatch_logical_split(corners, engine)

    @override
    def generate(self, engine: RenderEngine | None = None) -> None:
        """Generate an imperfect maze.

        The generation follows a inspired logic from the
        recursive division algorithm.

        Parameters
        ----------
        engine: `RenderEngine`
            Passing this argument into the program allows to render the maze
            step-by-step
        """
        for cell in self.grid:
            if cell.state != CellState.LOCKED:
                cell.state = CellState.VISITED
                cell.set_connection(Compass.NORTH)
                cell.set_connection(Compass.EAST)
                cell.set_connection(Compass.SOUTH)
                cell.set_connection(Compass.WEST)
        if globals.config.seed is not None:
            random.seed(globals.config.seed)
        self._imperfect_generation(engine=engine)
        self._eliminate_deadends(engine=engine)
        self._anihilate_large_rooms()
