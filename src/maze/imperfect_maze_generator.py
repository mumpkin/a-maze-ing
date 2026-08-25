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

    # def _check_direction(self, cell: Cell, direction: Compass) -> bool:
    #     match direction:
    #         case Compass.EAST:
    #             east_neighbour = cell.get_neighbours()[Compass.EAST]
    #             if east_neighbour:
    #                 print(f"east cell:{east_neighbour.conns_to_hexa()}")
    #             if (
    #                 east_neighbour
    #                 and east_neighbour.pos.x < globals.config.width
    #                 and east_neighbour.state == CellState.VISITED
    #                 and not east_neighbour.get_connections()[Compass.EAST]
    #             ):
    #                 print("East route invalid")
    #                 cell.set_connection(Compass.SOUTH)
    #                 east_neighbour.set_connection(Compass.SOUTH)
    #                 return False
    #         case Compass.SOUTH:
    #             south_neighbour = cell.get_neighbours()[Compass.SOUTH]
    #             if south_neighbour:
    #                 print(f"south cell:{south_neighbour.conns_to_hexa()}")
    #             if (
    #                 south_neighbour
    #                 and south_neighbour.pos.y > 0
    #                 and south_neighbour.state == CellState.VISITED
    #                 and not south_neighbour.get_connections()[Compass.SOUTH]
    #             ):
    #                 print("South route invalid")
    #                 return False
    #         case _:
    #             print(f"route {direction} valid")
    #             return True
    #     return True

    def _select_direction(self, direction: Compass) -> Compass:
        match direction:
            case Compass.NORTH:
                return Compass.EAST
            case Compass.SOUTH:
                return Compass.EAST
            case _:
                return Compass.NORTH

    def _directional_dig(
        self, cell: Cell, cell_list: list[Cell], direction: Compass
    ) -> None:
        print()
        if (
            direction == Compass.NORTH or direction == Compass.SOUTH
        ) and cell.get_connections()[Compass.EAST] is False:
            return
        elif (
            direction == Compass.EAST or direction == Compass.WEST
        ) and cell.get_connections()[Compass.SOUTH] is False:
            return

        # if self._check_direction(cell, direction) is False:
        #     return

        to_unset = self._select_direction(direction)

        print(
            f"cell: {cell.pos}. Resolving in direction={direction} and affecting {to_unset} neighbours"
        )
        if to_unset and cell.get_neighbours()[to_unset] is False:
            return

        if direction == Compass.SOUTH or direction == Compass.WEST:
            cell.unset_connection(to_unset)
        neighbour = cell.get_neighbours()[direction]

        while (
            neighbour
            and neighbour.state == CellState.VISITED
            and neighbour.get_connections()[direction]
        ):
            cell_list.append(neighbour)
            neighbour.unset_connection(to_unset)
            neighbour = neighbour.get_neighbours()[direction]

        for cell in sample(cell_list, k=1):
            cell.set_connection(to_unset)

    def _build_row(
        self,
        cell: Cell,
        direction: Compass,
        engine: Optional[RenderEngine] = None,
    ) -> None:
        # if cell.state == CellState.VISITED:
        #     return

        cells_list: list[Cell] = [cell]
        print("Testing towards EAST")
        self._directional_dig(cell, cells_list, direction)
        if engine:
            engine.render()

        li = list(filter(lambda x: x.pos.x % 2 == 0, cells_list))
        print("Filter size:", li)
        # for col in sample(li, k=len(li)):
        #     side = choice([Compass.NORTH, Compass.SOUTH])
        #     self._build_row(col, side, engine)

    def _build_col(
        self,
        cell: Cell,
        direction: Compass,
        engine: Optional[RenderEngine] = None,
    ) -> None:
        cells_list: list[Cell] = [cell]
        self._directional_dig(cell, cells_list, direction)
        if engine:
            engine.render()
        li = list(filter(lambda x: x.pos.y % 2 == 0, cells_list))
        print("Filter size:", li)
        for row in sample(li, k=len(li)):
            side = choice([Compass.EAST, Compass.WEST])
            self._build_row(row, side, engine)

    # ---IDEA---
    # Should make a initial cut and the handle the separate spaces recursively with coordinates
    # like top right/left and bottom right-left of the zone and then make the rows and collums
    # while preventing the program from going further than those limits to avoid overwriting on previous cells

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
        self._build_col(
            self.grid[randint(0, globals.config.width - 2)], Compass.SOUTH
        )
        if engine:
            engine.render()
