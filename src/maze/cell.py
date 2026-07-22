from typing import Self


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y


class Cell:
    """Representation of a cell in the maze's grid."""

    def __init__(self, position: Point) -> None:
        self.pos: Point = position
        self.is_visited: bool = False
        self._neighbours: list[Self] = []
        self._connections: list[Self] = []

    def get_neighbours(self) -> list[Self]:
        """Return direct cell neighbours list."""

        return self._neighbours


    def set_neighbours(self, grid: list[Self]) -> None:
        """Set the list of direct neighbours of this cell."""

        width: int = max(grid, key=lambda c: c.pos.x).pos.x
        height: int = max(grid, key=lambda c: c.pos.y).pos.y

        self._neighbours = [
            cell for cell in grid if self.is_neighbour(cell, width, height)
        ]

    def get_connections(self) -> list[Self]:
        """Return the list of cells connected to this one."""

        return self._connections

    def connect_to(self, cell: Self) -> None:
        """Add the given cell to the list of connected cells."""

        self._connections.append(cell)

    def is_neighbour(self, cell: Self, width: int, height: int) -> bool:
        """Check if the"""
        if (
            cell.pos.x < 0
            or cell.pos.y < 0
            or cell.pos.x > width
            or cell.pos.y > height
        ):
            return False
        if not (
            (cell.pos.x == self.pos.x and cell.pos.y == self.pos.y - 1)
            or (cell.pos.x == self.pos.x and cell.pos.y == self.pos.y + 1)
            or (cell.pos.x == self.pos.x - 1 and cell.pos.y == self.pos.y)
            or (cell.pos.x == self.pos.x + 1 and cell.pos.y == self.pos.y)
        ):
            return False
        return True
