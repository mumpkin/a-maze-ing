"""ImperfectMazeGenerator definition."""

from glob import glob
from random import choice, randint, sample
from time import sleep
from turtle import width
from typing import Optional

from typing_extensions import override

import globals
from enums import CellState, Compass
from globals.config import config
from utils import Point, RenderEngine

from . import MazeGenerator
from .cell import Cell


class ImperfectMazeGenerator(MazeGenerator):
    """Imperfect maze generator class."""

    def _select_direction(self, direction: Compass) -> Compass:
        match direction:
            case Compass.NORTH | Compass.SOUTH:
                return Compass.EAST
            case Compass.EAST | Compass.WEST:
                return Compass.NORTH

    def _ignore_logo_area(self, cell: Cell) -> bool:
        pos = cell.pos
        if pos:
            pass
        return False

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
        msg: str,
    ) -> None:
        if (
            area_corners["bottom-left"].y - area_corners["top-left"].y < 1
            or area_corners["top-right"].x - area_corners["top-left"].x < 1
        ):
            return
        starting_cell = self.grid[
            area_corners["top-left"].x
            + randint(
                area_corners["top-left"].y, area_corners["bottom-left"].y
            )
            * globals.config.width
        ]
        next_cell = starting_cell
        direction_to_unset = self._select_direction(direction)
        li: list[Cell] = []

        while (
            next_cell
            and next_cell.pos.x <= area_corners["top-right"].x
            and not (
                next_cell.pos == globals.config.entry
                or next_cell.pos == globals.config.exit
            )
        ):
            li.append(next_cell)
            next_cell.unset_connection(direction_to_unset)
            next_cell = next_cell.get_neighbours()[direction]
            while next_cell and self._ignore_logo_area(next_cell):
                next_cell = next_cell.get_neighbours()[direction]
        if len(li) > 0:
            random_sample = sample(li, k=max(1, len(li) // 2))
            for cell in random_sample:
                cell.set_connection(direction_to_unset)

        upper_area, lower_area = self._define_horizontal_areas(
            area_corners, starting_cell
        )

        print(
            f"Horizontal split: {msg}\n",
            f"starting cell: {starting_cell.pos}\n",
            f"Direction : {direction_to_unset}\n",
            f"Upper area:\n{upper_area}\nLower area: \n{lower_area}",
        )
        if engine:
            # starting_cell.state = CellState.VISITING
            engine.render()
            sleep(0.01)
            # starting_cell.state = CellState.VISITED
        self._vertical_split(upper_area, Compass.SOUTH, engine, msg + "-->Up")
        self._vertical_split(
            lower_area, Compass.SOUTH, engine, msg + "-->Down"
        )

    def _vertical_split(
        self,
        area_corners: dict[str, Point],
        direction: Compass,
        engine: RenderEngine | None,
        msg: str,
    ) -> None:
        if (
            area_corners["bottom-left"].y - area_corners["top-left"].y < 1
            or area_corners["top-right"].x - area_corners["top-left"].x < 1
        ):
            return
        starting_cell: Cell = self.grid[
            randint(area_corners["top-left"].x, area_corners["top-right"].x)
            + area_corners["top-left"].y * globals.config.width
        ]
        next_cell: Cell | None = starting_cell
        direction_to_unset: Compass = self._select_direction(direction)
        li: list[Cell] = []
        while (
            next_cell
            and next_cell.pos.y <= area_corners["bottom-left"].y
            and not (
                next_cell.pos == globals.config.entry
                or next_cell.pos == globals.config.exit
            )
        ):
            li.append(next_cell)
            next_cell.unset_connection(direction_to_unset)
            next_cell = next_cell.get_neighbours()[direction]
            while next_cell and self._ignore_logo_area(next_cell):
                next_cell = next_cell.get_neighbours()[direction]
        if len(li) > 0:
            random_sample = sample(li, k=max(1, len(li) // 2))
            for cell in random_sample:
                cell.set_connection(direction_to_unset)

        left_area, right_area = self._define_vertical_areas(
            area_corners, starting_cell
        )

        print(
            f"Vertical split: {msg}\n",
            f"starting cell: {starting_cell.pos}\n",
            f"Direction : {direction_to_unset}\n",
            f"Left area:\n{left_area}\nRight area: \n{right_area}",
        )
        if engine:
            # starting_cell.state = CellState.VISITING
            engine.render()
            sleep(0.01)
            # starting_cell.state = CellState.VISITED
        self._horizontal_split(
            left_area, Compass.EAST, engine, msg + "-->Left"
        )
        self._horizontal_split(
            right_area, Compass.EAST, engine, msg + "-->Right"
        )

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
        self._vertical_split(corners, Compass.SOUTH, engine, "Split")
        # self._horizontal_split(corners, Compass.EAST, engine)

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
        # self._build_col(
        #     self.grid[randint(0, globals.config.width - 2)], Compass.SOUTH
        # )
        self._inital_split(engine)
        if engine:
            engine.render()
