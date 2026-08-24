"""PerfectMazeGenerator definition."""

import random
from typing import override

from enums.cell_state import CellState
from maze import Cell
from utils import RenderEngine

from . import MazeGenerator


class PerfectMazeGenerator(MazeGenerator):
    """Perfect maze generator."""

    def _is_maze_generated(self) -> bool:
        for cell in self.grid:
            if not cell.state == CellState.VISITED:
                return False
        return True

    @override
    def generate(self, engine: RenderEngine | None = None) -> None:
        """Generate maze."""
        visiting: list[Cell] = []
        while self._is_maze_generated():
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
