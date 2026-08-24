"""PerfectMazeGenerator definition."""

import random
from time import sleep
from typing import override

import globals
import utils
from enums import CellState, Compass
from maze import Cell

from . import MazeGenerator


class PerfectMazeGenerator(MazeGenerator):
    """Perfect maze generator."""

    def _is_maze_generated(self) -> bool:
        for cell in self.grid:
            match cell.state:
                case CellState.VISITED | CellState.LOCKED:
                    continue
                case _:
                    return False
        return True

    def _connect_visiting(self, visiting: list[Cell]):
        for index, cell in enumerate(visiting[:-1]):
            for dir, neig in cell.get_neighbours().items():
                if visiting[index + 1] == neig:
                    match dir:
                        case Compass.NORTH:
                            cell.set_connection(Compass.NORTH)
                            visiting[index + 1].set_connection(Compass.SOUTH)
                        case Compass.EAST:
                            cell.set_connection(Compass.EAST)
                            visiting[index + 1].set_connection(Compass.WEST)
                        case Compass.SOUTH:
                            cell.set_connection(Compass.SOUTH)
                            visiting[index + 1].set_connection(Compass.NORTH)
                        case Compass.WEST:
                            cell.set_connection(Compass.WEST)
                            visiting[index + 1].set_connection(Compass.EAST)

    @override
    def generate(self, engine: utils.RenderEngine | None = None) -> None:
        """Generate maze."""

        visiting: list[Cell] = [
            cell for cell in self.grid if cell.pos == globals.config.entry
        ]
        for cell in self.grid:
            if cell.pos == globals.config.exit:
                cell.state = CellState.VISITED
                break
        while not self._is_maze_generated():
            if len(visiting) == 0:
                visiting.append(
                    random.choice(
                        [
                            cell
                            for cell in self.grid
                            if cell.state == CellState.IDLE
                        ]
                    )
                )
            next_cell: Cell = visiting[-1].get_random_neighbour()[1]
            if next_cell in visiting:
                while not visiting[-1] == next_cell:
                    visiting[-1].state = CellState.IDLE
                    _ = visiting.pop()
            elif next_cell.state == CellState.IDLE:
                next_cell.state = CellState.VISITING
                visiting.append(next_cell)
            elif next_cell.state == CellState.VISITED:
                visiting.append(next_cell)
                self._connect_visiting(visiting)
                for cell in visiting:
                    cell.state = CellState.VISITED
                    visiting = []
            if engine is not None:
                engine.render()
            sleep(0.05)
