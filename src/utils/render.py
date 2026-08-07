"""Render definition."""

import subprocess
from typing import Optional

import globals
from enums import CellState, Compass, TileColor
from maze import Cell


class RenderEngine:
    """Engine to render da maze."""

    def __init__(self, maze: list[Cell]) -> None:
        """Render default constructor."""
        self.maze = maze

    def _put_tile(self, color: Optional[TileColor] = None) -> None:
        """."""
        tile: str = "  "
        if color:
            print(color.value + tile, end="")
        else:
            print(TileColor.WALL.value + tile, end="")

    def _put_eol(self) -> None:
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
                self._put_tile(TileColor.WALL)
            case CellState.VISITED:
                self._put_tile(TileColor.MAZE)
                return

    def _put_wall_row(self, row: Optional[list[Cell]] = None) -> None:
        self._put_tile()
        if row:
            for cell in row:
                south_neighbour = cell.get_neighbours().get(Compass.SOUTH)
                if (
                    cell.state == CellState.LOCKED
                    and south_neighbour
                    and south_neighbour.state == CellState.LOCKED
                ):
                    self._dispatch_color(cell)
                else:
                    self._put_tile()
                self._put_tile()
        else:
            for _ in range(globals.config.width):
                self._put_tile()
                self._put_tile()
        self._put_eol()

    def _put_cell_row(self, row: list[Cell]) -> None:
        self._put_tile()
        for cell in row:
            east_neighbour = cell.get_neighbours().get(Compass.EAST)
            self._dispatch_color(cell)
            if (
                cell.state == CellState.LOCKED
                and east_neighbour
                and east_neighbour.state == CellState.LOCKED
            ):
                self._dispatch_color(cell)
            else:
                self._put_tile()
        self._put_eol()

    def render(self) -> None:
        """."""
        subprocess.run(["clear", "-x"])
        row = []
        for y in range(globals.config.height):
            row = [cell for cell in self.maze if cell.pos.y == y]
            self._put_wall_row(row)
            self._put_cell_row(row)
        self._put_wall_row()
