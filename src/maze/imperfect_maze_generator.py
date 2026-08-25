"""ImperfectMazeGenerator definition."""

from random import choice, randint, sample
from typing import Optional

from typing_extensions import override

import globals
from enums import CellState, Compass
from utils import RenderEngine

from . import MazeGenerator
from .cell import Cell


class ImperfectMazeGenerator(MazeGenerator):
    """Imperfect maze generator class."""

    def _check_direction(self, cell: Cell, direction: Compass) -> bool:
        match direction:
            case Compass.EAST:
                east_neighbour = cell.get_neighbours()[Compass.EAST]
                if east_neighbour:
                    print(f"west cell:{east_neighbour.conns_to_hexa()}")
                if (
                    east_neighbour
                    and east_neighbour.pos.y < globals.config.width
                    and east_neighbour.state == CellState.VISITED
                    and east_neighbour.conns_to_hexa() == "D"
                ):
                    print("East direction invalid")
                    cell.set_connection(Compass.SOUTH)
                    east_neighbour.set_connection(Compass.SOUTH)
                    return False
            case Compass.SOUTH:
                south_neighbour = cell.get_neighbours()[Compass.EAST]
                if south_neighbour:
                    print(f"west cell:{south_neighbour.conns_to_hexa()}")
                if (
                    south_neighbour
                    and south_neighbour.state == CellState.VISITED
                    and south_neighbour.conns_to_hexa() == "E"
                ):
                    print("East direction invalid")
                    return False
                pass

        return True

    def _select_direction(self, cell: Cell, direction: Compass) -> Compass:
        match direction:
            case Compass.NORTH:
                return Compass.EAST
            case Compass.SOUTH:
                return Compass.EAST
            case _:
                return Compass.NORTH

    def _directional_dig(
        self, cell: Cell, cell_list: list[Cell], direction: Compass
    ) -> bool:
        print()
        if (
            direction == Compass.NORTH or direction == Compass.SOUTH
        ) and cell.get_connections()[Compass.EAST] is False:
            return False
        elif (
            direction == Compass.EAST or direction == Compass.WEST
        ) and cell.get_connections()[Compass.SOUTH] is False:
            return False

        if self._check_direction(cell, direction) is False:
            return False

        to_unset = self._select_direction(cell, direction)

        print(
            f"cell: {cell.pos}. Resolving in direction={direction} and affecting {to_unset} neighbours"
        )
        print()
        if to_unset and cell.get_neighbours()[to_unset] is False:
            return False

        cell.unset_connection(to_unset)
        neighbour = cell.get_neighbours()[direction]

        while neighbour and neighbour.state == CellState.VISITED:
            cell_list.append(neighbour)
            neighbour.unset_connection(to_unset)
            neighbour = neighbour.get_neighbours()[direction]

        for cell in sample(cell_list, k=max(1, len(cell_list) // 4)):
            cell.set_connection(to_unset)
        return True

    def _build_row(
        self, cell: Optional[Cell], engine: Optional[RenderEngine] = None
    ) -> None:
        if not cell:
            return
        if cell.state == CellState.IDLE:
            return

        cells_list: list[Cell] = [cell]
        print("Testing towards EAST")
        if self._directional_dig(cell, cells_list, Compass.EAST) is False:
            print("Testing towards WEST")
            _ = self._directional_dig(cell, cells_list, Compass.WEST)
        if engine:
            engine.render()
        # if len(cells_list) > 1:
        # col_pair = sample(cells_list, k=2)
        # self._build_col(col_pair[0].get_neighbours()[Compass.EAST], engine)
        #     self._build_col(col_pair[1].get_neighbours()[Compass.WEST], engine)

    def _build_col(
        self, cell: Optional[Cell], engine: Optional[RenderEngine] = None
    ) -> None:
        if not cell:
            return
        if cell.state == CellState.IDLE:
            return

        cells_list: list[Cell] = [cell]
        print("Testing towards SOUTH")
        if self._directional_dig(cell, cells_list, Compass.SOUTH) is False:
            print("Testing towards NORTH")
            _ = self._directional_dig(cell, cells_list, Compass.NORTH)
        if engine:
            engine.render()
        if len(cells_list) > 1:
            row_pair = sample(cells_list, k=2)
            self._build_row(row_pair[0].get_neighbours()[Compass.EAST], engine)
            # self._build_row(row_pair[1].get_neighbours()[Compass.WEST], engine)

    @override
    def generate(self, engine: Optional[RenderEngine] = None) -> None:
        """."""
        for cell in self.grid:
            if cell.state != CellState.LOCKED:
                cell.state = CellState.VISITED
                cell.set_connection(Compass.NORTH)
                cell.set_connection(Compass.EAST)
                cell.set_connection(Compass.SOUTH)
                cell.set_connection(Compass.WEST)
        # if randint(0, 1) == 0:
        #    self._build_row(self.grid[randint(0, globals.config.width)])
        # else:
        #    self._build_collumn(
        #        self.grid[
        #            randint(0, globals.config.height)
        #            * (globals.config.width + 1)
        #        ]
        #    )
        self._build_col(self.grid[randint(0, globals.config.width - 2)])
        if engine:
            engine.render()
