"""ImperfectMazeGenerator definition."""

from random import choice, sample
from typing import Optional

from enums import CellState, Compass
from utils import RenderEngine

from . import MazeGenerator
from .cell import Cell


class ImperfectMazeGenerator(MazeGenerator):
    """Imperfect maze generator class."""

    def _directional_dig(
        self, cell: Cell, cell_list: list[Cell], direction: Compass
    ) -> None:
        print()
        if cell.state == CellState.IDLE:
            cell.state = CellState.VISITED
        neighbour = cell.get_neighbours()[direction]
        print(cell.get_neighbours())
        if neighbour:
            print("neighbour:  " + neighbour.state)
            while neighbour and neighbour.state == CellState.IDLE:
                neighbour.state = CellState.VISITED
                cell_list.append(neighbour)
                if neighbour.get_neighbours()[direction]:
                    neighbour.set_connection(direction)
                    neighbour = neighbour.get_neighbours()[direction]
                print("List:", [cp.pos for cp in cell_list])
            choice(cell_list).state = CellState.IDLE

    def _build_row(
        self, cell: Optional[Cell], engine: Optional[RenderEngine] = None
    ) -> None:
        if not cell:
            return
        if cell.state == CellState.VISITED:
            return

        cells_list: list[Cell] = [cell]
        self._directional_dig(cell, cells_list, Compass.EAST)
        self._directional_dig(cell, cells_list, Compass.WEST)
        print("List:", [cp.pos for cp in cells_list])
        # if len(cells_list) > 1:
        #     next_pair = sample(cells_list, k=2)
        #     self._build_row(
        #         next_pair[0].get_neighbours()[Compass.NORTH], engine
        #     )
        #     self._build_row(
        #         next_pair[1].get_neighbours()[Compass.SOUTH], engine
        #     )

    def _build_collumn(
        self, cell: Optional[Cell], engine: Optional[RenderEngine] = None
    ) -> None:
        if not cell:
            return
        if cell.state == CellState.VISITED:
            return

        cells_list: list[Cell] = [cell]
        self._directional_dig(cell, cells_list, Compass.SOUTH)
        self._directional_dig(cell, cells_list, Compass.NORTH)
        print("List:", [cp.pos for cp in cells_list])
        if len(cells_list) > 1:
            next_pair = sample(cells_list, k=2)
            self._build_row(
                next_pair[0].get_neighbours()[Compass.EAST], engine
            )
            self._build_row(
                next_pair[1].get_neighbours()[Compass.WEST], engine
            )

    def generate(self, engine: Optional[RenderEngine] = None) -> None:
        """."""
        for cell in self.grid:
            print(cell.state)
            if cell.state != CellState.LOCKED:
                cell.state = CellState.VISITED
                cell.get_connections()[Compass.NORTH]
                cell.get_connections()[Compass.EAST]
                cell.get_connections()[Compass.SOUTH]
                cell.get_connections()[Compass.WEST]
                print()
                print(cell.get_connections())
                print(cell.get_neighbours())
        # if randint(0, 1) == 0:
        #    self._build_row(self.grid[randint(0, globals.config.width)])
        # else:
        #    self._build_collumn(
        #        self.grid[
        #            randint(0, globals.config.height)
        #            * (globals.config.width + 1)
        #        ]
        #    )
        # self._build_collumn(self.grid[randint(0, globals.config.width - 1)])
