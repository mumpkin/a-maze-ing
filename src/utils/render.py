"""Render definition."""

from typing import final

import globals
import maze
from enums import CellState, ColorScheme, Compass


@final
class RenderEngine:
    """Engine to render da maze."""

    def __init__(self, maze: maze.MazeGenerator) -> None:
        """Render default constructor."""
        self.maze = maze
        self._color_scheme: ColorScheme = ColorScheme()

    def _get_tile_color(self, cell: maze.Cell) -> str:
        """
        Get tile color according to a cell attributes.

        Keyword parameters:
        cell: Cell -- A cell lul (╯°□°)╯︵ ┻━┻.
        """
        match cell.pos:
            case globals.config.entry:
                return self._color_scheme.ENTRY
            case globals.config.exit:
                return self._color_scheme.EXIT
            case _:
                pass
        if cell in self.maze.optimal_path:
            return self._color_scheme.OPTIMAL_PATH
        match cell.state:
            case CellState.LOCKED:
                return self._color_scheme.LOCKED
            case CellState.IDLE:
                return self._color_scheme.IDLE
            case CellState.VISITED:
                return self._color_scheme.VISITED
            case CellState.VISITING:
                return self._color_scheme.VISITING

    def set_color_scheme(self, color_scheme: ColorScheme) -> None:
        """."""
        self._color_scheme = color_scheme

    def get_color_scheme(self) -> ColorScheme:
        """."""
        return self._color_scheme

    def _draw_tile(self, color: str | None = None) -> None:
        """
        Draw the tile.

        Keyword parameters:
        color: TileColor -- Color used by the terminal.
        """
        tile: str = "  "
        if color:
            print(color + tile, end="")
        else:
            print(self._color_scheme.IDLE + tile, end="")

    def _draw_eol(self) -> None:
        """Draw the end of line."""
        print(self._color_scheme.TRANSPARENT)

    def _draw_wall_row(self, row: list[maze.Cell] | None = None) -> None:
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
                    (
                        cell.state == CellState.VISITED
                        or cell.state == CellState.VISITING
                    )
                    and north_neighbour
                    and (
                        north_neighbour.state == CellState.VISITED
                        or north_neighbour.state == CellState.VISITING
                    )
                    and cell.get_connections()[Compass.NORTH]
                ):
                    if (
                        cell.pos == globals.config.entry
                        or cell.pos == globals.config.exit
                    ):
                        self._draw_tile(self._color_scheme.VISITED)
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

    def _draw_cells_row(self, row: list[maze.Cell]) -> None:
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
                (
                    cell.state == CellState.VISITED
                    or cell.state == CellState.VISITING
                )
                and east_neighbour
                and (
                    east_neighbour.state == CellState.VISITED
                    or east_neighbour.state == CellState.VISITING
                )
                and cell.get_connections()[Compass.EAST]
            ):
                if (
                    cell.pos == globals.config.entry
                    or cell.pos == globals.config.exit
                ):
                    self._draw_tile(self._color_scheme.VISITED)
                else:
                    self._draw_tile(self._get_tile_color(cell))

            else:
                self._draw_tile()
        self._draw_eol()

    def render(self) -> None:
        """Render the maze."""
        row = []
        for y in range(globals.config.height):
            row = [cell for cell in self.maze.grid if cell.pos.y == y]
            self._draw_wall_row(row)
            self._draw_cells_row(row)
        self._draw_wall_row()
