"""Render definition."""

import subprocess

import globals
from enums import CellState, Compass, TileColor
from maze import Cell, MazeGenerator


class RenderEngine:
    """Engine to render da maze."""

    def __init__(self, maze: MazeGenerator) -> None:
        """Render default constructor."""
        self.maze: MazeGenerator = maze

    def _get_tile_color(self, cell: Cell) -> TileColor:
        """
        Get tile color according to a cell attributes.

        Keyword parameters:
        cell: Cell -- A cell lul (╯°□°)╯︵ ┻━┻.
        """
        match cell.pos:
            case globals.config.entry:
                return TileColor.ENTRY
            case globals.config.exit:
                return TileColor.EXIT
            case _:
                pass
        if cell in self.maze.optimal_path:
            return TileColor.OPTIMAL_PATH
        match cell.state:
            case CellState.LOCKED:
                return TileColor.LOCKED
            case CellState.IDLE:
                return TileColor.IDLE
            case CellState.VISITED:
                return TileColor.VISITED
            case CellState.VISITING:
                return TileColor.VISITING

    def _draw_tile(self, color: TileColor | None = None) -> None:
        """
        Draw the tile.

        Keyword parameters:
        color: TileColor -- Color used by the terminal.
        """
        tile: str = "  "
        if color:
            print(color.value + tile, end="")
        else:
            print(TileColor.IDLE.value + tile, end="")

    def _draw_eol(self) -> None:
        """Draw the end of line."""
        print(TileColor.TRANSPARENT.value)

    def _draw_wall_row(self, row: list[Cell] | None = None) -> None:
        self._draw_tile()
        if row:
            for cell in row:
                north_neighbour = cell.get_neighbours().get(Compass.NORTH)
                if (
                    cell.state == CellState.LOCKED
                    and north_neighbour
                    and north_neighbour.state == CellState.LOCKED
                ):
                    self._draw_tile(self._get_tile_color(cell))
                elif (
                    cell.state == CellState.VISITED
                    and north_neighbour
                    and north_neighbour.state == CellState.VISITED
                    and cell.get_connections()[Compass.NORTH]
                ):
                    if (
                        cell.pos == globals.config.entry
                        or cell.pos == globals.config.exit
                    ):
                        self._draw_tile(TileColor.VISITED)
                    else:
                        self._draw_tile(self._get_tile_color(cell))

                else:
                    self._draw_tile()
                self._draw_tile()
        else:
            for _ in range(globals.config.width):
                self._draw_tile()
                self._draw_tile()
        self._draw_eol()

    def _draw_cells_row(self, row: list[Cell]) -> None:
        """
        Draw row of cells in the terminal.

        Keyword parameters:
        row: list[Cell] -- Row of cells to draw.
        """
        self._draw_tile()
        for cell in row:
            east_neighbour = cell.get_neighbours().get(Compass.EAST)
            self._draw_tile(self._get_tile_color(cell))
            if (
                cell.state == CellState.LOCKED
                and east_neighbour
                and east_neighbour.state == CellState.LOCKED
            ):
                self._draw_tile(self._get_tile_color(cell))
            elif (
                cell.state == CellState.VISITED
                and east_neighbour
                and east_neighbour.state == CellState.VISITED
                and cell.get_connections()[Compass.EAST]
            ):
                if (
                    cell.pos == globals.config.entry
                    or cell.pos == globals.config.exit
                ):
                    self._draw_tile(TileColor.VISITED)
                else:
                    self._draw_tile(self._get_tile_color(cell))

            else:
                self._draw_tile()
        self._draw_eol()

    def render(self) -> None:
        """Render the maze."""
        _ = subprocess.run(["clear", "-x"])
        row = []
        for y in range(globals.config.height):
            row = [cell for cell in self.maze.grid if cell.pos.y == y]
            self._draw_wall_row(row)
            self._draw_cells_row(row)
        self._draw_wall_row()
