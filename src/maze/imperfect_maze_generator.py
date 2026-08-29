"""ImperfectMazeGenerator definition."""

import random
from socket import EAI_SERVICE
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

    def _dispatch_logical_split(
        self, area: dict[str, Point], engine: RenderEngine | None
    ) -> None:
        """Select which split to perform next.

        If the areas width is higher than its width, split vertically.
        Otherwise split horizontally.
        """
        width = area["top-right"].x - area["top-left"].x
        height = area["bottom-left"].y - area["top-left"].y
        if width > height:
            self._vertical_split(area, Compass.SOUTH, engine)
        else:
            self._horizontal_split(area, Compass.EAST, engine)

    def _define_horizontal_areas(
        self, original_corners: dict[str, Point], starting_cell: Cell
    ) -> tuple[dict[str, Point], dict[str, Point]]:
        """Return the up and down area after performing a vertical split."""
        upper_area: dict[str, Point] = dict(
            {
                "top-left": Point(
                    x=starting_cell.pos.x, y=original_corners["top-left"].y
                ),
                "top-right": Point(
                    x=original_corners["top-right"].x,
                    y=original_corners["top-right"].y,
                ),
                "bottom-left": Point(
                    original_corners["bottom-left"].x,
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
                    x=original_corners["top-left"].x, y=starting_cell.pos.y
                ),
                "top-right": Point(
                    x=original_corners["top-right"].x, y=starting_cell.pos.y
                ),
                "bottom-left": Point(
                    x=starting_cell.pos.x,
                    y=original_corners["bottom-left"].y,
                ),
                "bottom-right": original_corners["bottom-right"],
            }
        )
        return upper_area, lower_area

    def _define_vertical_areas(
        self, original_corners: dict[str, Point], starting_cell: Cell
    ) -> tuple[dict[str, Point], dict[str, Point]]:
        """Return the left and right area after performing a vertical split."""
        left_area: dict[str, Point] = dict(
            {
                "top-left": original_corners["top-left"],
                "top-right": Point(
                    x=starting_cell.pos.x, y=original_corners["top-right"].y
                ),
                "bottom-left": original_corners["bottom-left"],
                "bottom-right": Point(
                    x=starting_cell.pos.x, y=original_corners["bottom-right"].y
                ),
            }
        )
        right_area: dict[str, Point] = dict(
            {
                "top-left": Point(
                    x=starting_cell.pos.x + 1, y=original_corners["top-left"].y
                ),
                "top-right": original_corners["top-right"],
                "bottom-left": Point(
                    x=starting_cell.pos.x + 1,
                    y=original_corners["bottom-left"].y,
                ),
                "bottom-right": original_corners["bottom-right"],
            }
        )
        return left_area, right_area

    def _horizontal_split(
        self,
        area_corners: dict[str, Point],
        direction: Compass,
        engine: RenderEngine | None,
    ) -> None:
        """Split horizontally the given area."""
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
                # if (
                #     globals.config.width >= 9 and globals.config.height >= 7
                # ) and not (
                #     next_cell.pos.x == globals.config.width // 2
                #     and next_cell.pos.y == globals.config.height // 2 - 2
                # ):
                next_cell.unset_connection(direction_to_unset)
            next_cell = next_cell.get_neighbours()[direction]
            if engine is not None:
                _ = stdout.write("\033[H")
                _ = stdout.flush()
                engine.render()
                sleep(globals.config.delay)

        if len(segment_cells) > 0:
            segments.append(segment_cells)
        for segment_cells in segments:
            path_number = random.randint(1, max(1, len(segment_cells) // 2))
            random_sample = random.sample(segment_cells, k=max(1, path_number))
            for cell in random_sample:
                cell.set_connection(direction_to_unset)
        upper_area, lower_area = self._define_horizontal_areas(
            area_corners, starting_cell
        )
        if engine is not None:
            _ = stdout.write("\033[H")
            _ = stdout.flush()
            engine.render()
            sleep(globals.config.delay)
        self._dispatch_logical_split(upper_area, engine)
        self._dispatch_logical_split(lower_area, engine)

    def _vertical_split(
        self,
        area_corners: dict[str, Point],
        direction: Compass,
        engine: RenderEngine | None,
    ) -> None:
        """Split vertically the given area."""
        if (
            area_corners["bottom-left"].y - area_corners["top-left"].y < 1
            or area_corners["top-right"].x - area_corners["top-left"].x < 1
        ):
            return
        starting_cell: Cell = self.grid[
            random.randint(
                area_corners["top-left"].x + 1, area_corners["top-right"].x - 1
            )
            + area_corners["top-left"].y * globals.config.width
        ]
        next_cell: Cell | None = starting_cell
        direction_to_unset: Compass = Compass.EAST
        segments: list[list[Cell]] = []
        segment_cells: list[Cell] = []

        while next_cell and next_cell.pos.y <= area_corners["bottom-left"].y:
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
                # if (
                #     globals.config.width >= 9 and globals.config.height >= 7
                # ) and not (
                #     next_cell.pos.x == globals.config.width // 2
                #     and next_cell.pos.y == globals.config.height // 2 - 2
                # ):
                next_cell.unset_connection(direction_to_unset)
            next_cell = next_cell.get_neighbours()[direction]
            if engine is not None:
                _ = stdout.write("\033[H")
                _ = stdout.flush()
                engine.render()
                sleep(globals.config.delay)

        if len(segment_cells) > 0:
            segments.append(segment_cells)
        for segment_cells in segments:
            path_number = random.randint(1, max(1, len(segment_cells) // 2))
            random_sample = random.sample(segment_cells, k=max(1, path_number))
            for cell in random_sample:
                cell.set_connection(direction_to_unset)
        left_area, right_area = self._define_vertical_areas(
            area_corners, starting_cell
        )
        if engine is not None:
            _ = stdout.write("\033[H")
            _ = stdout.flush()
            engine.render()
            sleep(globals.config.delay)
        self._dispatch_logical_split(left_area, engine)
        self._dispatch_logical_split(right_area, engine)

    def _open_closed_path(
        self,
        cell: Cell,
        closed_directions: list[Compass],
    ) -> None:
        """Open a random wall if a cell is considered a dead end.

        Parameters
        ----------
        cell: Cell
            A cell from the grid presenting a dead end.
        closed_directions: list[Compass]
            A list containing the possibly valid directions towards neighbours
            of the current cell to create a new path
        """
        for dir in closed_directions:
            neighbour = cell.get_neighbours()[dir]
            if (
                neighbour and neighbour.state == CellState.LOCKED
            ) or cell.get_connections()[dir]:
                closed_directions.remove(dir)
        if len(closed_directions) == 0:
            return
        to_open = random.choice(closed_directions)
        cell.set_connection(to_open)

    def _biggus_roomus_violatus(self, cell: Cell) -> None:
        """Violate the integrity of overly large rooms by raising a wall."""
        north_neighbour = cell.get_neighbours()[Compass.WEST]
        south_neighbour = cell.get_neighbours()[Compass.SOUTH]
        if (cell and north_neighbour and south_neighbour) and (
            cell.get_connections()[Compass.NORTH]
            and cell.get_connections()[Compass.EAST]
            and cell.get_connections()[Compass.WEST]
            and cell.get_connections()[Compass.SOUTH]
            and north_neighbour.get_connections()[Compass.EAST]
            and north_neighbour.get_connections()[Compass.WEST]
            and south_neighbour.get_connections()[Compass.EAST]
            and south_neighbour.get_connections()[Compass.WEST]
        ):
            direction = [d for d in Compass]
            cell.unset_connection(random.choice(direction))

    def _does_cell_have_locked_neighbour(self, cell: Cell) -> bool:
        """Check if the curent cell has any locked neighbours."""
        neighbours = cell.get_neighbours()
        for _, v in neighbours.items():
            if v and v.state == CellState.LOCKED:
                return True
        return False

    def _eliminate_deadends(self) -> None:
        """Destroy dead ends by randomly hollowing walls.

        This method targets cells with only one connection and tries to connect
        the afore-mentionned cell with one of its neighbour.
        """
        for cell in self.grid:
            if cell.state == CellState.LOCKED:
                continue
            self._biggus_roomus_violatus(cell)
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
                    continue

    def _imperfect_generation(self, engine: RenderEngine | None) -> None:
        """Perform the creation of the maze."""
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
            step-by-
        """
        import time

        # toki = time.time()
        random.seed(1788027394.5928006)
        # print(f"seed: {toki}")
        for cell in self.grid:
            if cell.state != CellState.LOCKED:
                cell.state = CellState.VISITED
                cell.set_connection(Compass.NORTH)
                cell.set_connection(Compass.EAST)
                cell.set_connection(Compass.SOUTH)
                cell.set_connection(Compass.WEST)
        # if globals.config.seed is not None:
        # random.seed(globals.config.seed)
        self._imperfect_generation(engine=engine)
        self._eliminate_deadends()
