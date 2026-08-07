"""Render definition."""

import subprocess
from typing import Optional

import globals
from enums import CellState, TileColor
from maze import Cell

from .point import Point


class RenderEngine:
    """Engine to render da maze."""

    def __init__(self, maze: list[Cell]):
        """Render default constructor."""
        self.maze = maze

    def _put_tile(self, color: Optional[TileColor] = None):
        """."""
        tile: str = "  "
        if color:
            print(color.value + tile, end="")
        else:
            print(TileColor.WALL.value + tile, end="")

    def _put_eol(self):
        """."""
        print(TileColor.DEFAULT.value)

    def _dispatch_color(self, cell: Cell) -> None:
        """."""
        match cell.pos:
            case globals.config.entry:
                self._put_tile(TileColor.ENTRY)
                return
            case globals.config.exit:
                self._put_tile(TileColor.EXIT)
                return
        match cell.state:
            case CellState.LOCKED:
                self._put_tile(TileColor.LOCKED)
                return
            case CellState.IDLE:
                self._put_tile(TileColor.MAZE)
                return

    def _put_line(self, line: Optional[list[Cell]] = None) -> None:
        self._put_tile()
        if not line:
            for i in range(globals.config.width):
                self._put_tile()
                self._put_tile()
        else:
            for cell in line:
                self._dispatch_color(cell)
                self._put_tile()
        self._put_eol()

    def render(self) -> None:
        """."""
        subprocess.run(["clear", "-x"])
        for y in range(globals.config.height):
            self._put_line()
            self._put_line([cell for cell in self.maze if cell.pos.y == y])
        self._put_line()
