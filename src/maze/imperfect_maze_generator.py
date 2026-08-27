"""ImperfectMazeGenerator definition."""

from random import choice, randint, sample
from time import sleep

from typing_extensions import override

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
        width = area["top-right"].x - area["top-left"].x
        height = area["bottom-left"].y - area["top-left"].y
        if width > height:
            self._vertical_split(area, Compass.SOUTH, engine)
        else:
            self._horizontal_split(area, Compass.EAST, engine)

    def _ignore_logo_area(self, cell: Cell) -> bool:
        if globals.config.width >= 9 and globals.config.height >= 7:
            x = globals.config.width // 2
            y = globals.config.height // 2
            if (
                cell.pos.x < x - 3
                or cell.pos.x > x + 3
                or cell.pos.y < y - 2
                or cell.pos.y > y + 2
            ) and not (
                cell.pos.x > x - 2
                and cell.pos.x < x
                and cell.pos.y > y - 2
                and cell.pos.y < y + 2
            ):
                return False
        return True

    def _define_horizontal_areas(
        self, original_corners: dict[str, Point], starting_cell: Cell
    ) -> tuple[dict[str, Point], dict[str, Point]]:
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
        first_area: dict[str, Point] = dict(
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
        return first_area, right_area

    def _horizontal_split(
        self,
        area_corners: dict[str, Point],
        direction: Compass,
        engine: RenderEngine | None,
    ) -> None:
        if (
            area_corners["bottom-left"].y - area_corners["top-left"].y < 1
            or area_corners["top-right"].x - area_corners["top-left"].x < 1
        ):
            return
        starting_cell = self.grid[
            area_corners["top-left"].x
            + randint(
                area_corners["top-left"].y + 1, area_corners["bottom-left"].y
            )
            * globals.config.width
        ]
        next_cell = starting_cell
        direction_to_unset = Compass.NORTH
        li: list[Cell] = []

        while next_cell and next_cell.pos.x <= area_corners["top-right"].x:
            if not (
                next_cell.pos == globals.config.entry
                or next_cell.pos == globals.config.exit
            ):
                li.append(next_cell)
                next_cell.unset_connection(direction_to_unset)
            next_cell = next_cell.get_neighbours()[direction]
            while next_cell and self._ignore_logo_area(next_cell):
                next_cell = next_cell.get_neighbours()[direction]
        if len(li) > 0:
            path_number = randint(1, max(1, len(li) // 2))
            random_sample = sample(li, k=max(1, path_number))
            # random_sample = sample(li, k=1)
            for cell in random_sample:
                cell.set_connection(direction_to_unset)

        upper_area, lower_area = self._define_horizontal_areas(
            area_corners, starting_cell
        )
        if engine:
            # starting_cell.state = CellState.VISITING
            engine.render()
            sleep(0.001)
            # starting_cell.state = CellState.VISITED
        self._dispatch_logical_split(upper_area, engine)
        self._dispatch_logical_split(lower_area, engine)

    def _vertical_split(
        self,
        area_corners: dict[str, Point],
        direction: Compass,
        engine: RenderEngine | None,
    ) -> None:
        if (
            area_corners["bottom-left"].y - area_corners["top-left"].y < 1
            or area_corners["top-right"].x - area_corners["top-left"].x < 1
        ):
            return
        starting_cell: Cell = self.grid[
            randint(
                area_corners["top-left"].x + 1, area_corners["top-right"].x
            )
            + area_corners["top-left"].y * globals.config.width
        ]
        next_cell: Cell | None = starting_cell
        direction_to_unset: Compass = Compass.EAST
        li: list[Cell] = []

        while next_cell and next_cell.pos.y <= area_corners["bottom-left"].y:
            if not (
                next_cell.pos == globals.config.entry
                or next_cell.pos == globals.config.exit
            ):
                li.append(next_cell)
                next_cell.unset_connection(direction_to_unset)
            next_cell = next_cell.get_neighbours()[direction]
            while next_cell and self._ignore_logo_area(next_cell):
                next_cell = next_cell.get_neighbours()[direction]
        if len(li) > 0:
            path_number = randint(1, max(1, len(li) // 2))
            random_sample = sample(li, k=max(1, path_number))
            # random_sample = sample(li, k=1)
            for cell in random_sample:
                cell.set_connection(direction_to_unset)

        left_area, right_area = self._define_vertical_areas(
            area_corners, starting_cell
        )
        if engine:
            # starting_cell.state = CellState.VISITING
            engine.render()
            sleep(0.001)
            # starting_cell.state = CellState.VISITED
        self._dispatch_logical_split(left_area, engine)
        self._dispatch_logical_split(right_area, engine)

    def _inital_split(self, engine: RenderEngine | None):
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
        self._vertical_split(corners, Compass.SOUTH, engine)
        # Must check with seed if still works
        for c in self.grid:
            match c.sum_connections_value():
                case 8:
                    rand_dir = [Compass.NORTH, Compass.EAST, Compass.SOUTH]
                    c.set_connection(sample(rand_dir, k=1)[0])
                case 4:
                    rand_dir = [Compass.NORTH, Compass.EAST, Compass.WEST]
                    c.set_connection(sample(rand_dir, k=1)[0])
                case 2:
                    rand_dir = [Compass.NORTH, Compass.SOUTH, Compass.WEST]
                    c.set_connection(sample(rand_dir, k=1)[0])
                case 1:
                    rand_dir = [Compass.EAST, Compass.SOUTH, Compass.WEST]
                    c.set_connection(sample(rand_dir, k=1)[0])

    @override
    def generate(self, engine: RenderEngine | None = None) -> None:
        """."""
        for cell in self.grid:
            if cell.state != CellState.LOCKED:
                cell.state = CellState.VISITED
                cell.set_connection(Compass.NORTH)
                cell.set_connection(Compass.EAST)
                cell.set_connection(Compass.SOUTH)
                cell.set_connection(Compass.WEST)
        self._inital_split(engine=engine)
