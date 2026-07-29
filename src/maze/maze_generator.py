"""."""

from abc import ABC, abstractmethod
import sys
from typing import Any

from globals.config import config
from maze.cell import Cell
from utils import Point


class MazeGenerator(ABC):
    """."""

    def __init__(self) -> None:
        self.grid: list[Cell] = []

    def init_grid(self) -> None:
        """"."""
        for i in range(config.width * config.height):
            self.grid.append(Cell(Point(i % config.width, i // config.width)))

    def write_grid(self) -> None:
        """Display the maze's current state on the ter function."""
        y: int = 0
        output_file = open(config.output_file, 'w')
        for i in range(len(self.grid)):
            if i > 0 and i % config.width == 0:
                print(file=output_file)
                y += 1
            # print(f"({self.grid[i].pos.x} -- {self.grid[i].pos.y})", end='')
            print(f"{self.grid[i].hexa_compass()}", file=output_file, end="")
            if i < len(self.grid) - 1 and i % config.width != config.width - 1:
                print("-", file=output_file, end='')
        print("\n\n", file=output_file)
        print("Entry", config.entry, file=output_file)
        print("Exit", config.exit, file=output_file)

    @abstractmethod
    def generate_maze(self) -> Any:
        """Build the maze."""
        pass

    def write_ouput_file(self) -> None:
        """Write the maze into the filename.

        Firstly, write each cell as an hexademinal value.
        Then write the entry point and the exit point coordinates.
        Finally, write the optimal path using cardinal directions
        """
        try:
            pass
            # with open(self.get_config_key('OUTPUT_FILENAME'), 'w') as file:
        except FileNotFoundError as fe:
            print("Caught FileNotFoundError:   ", fe)
            sys.exit(1)
        except PermissionError as pe:
            print("Caught PermissionError:   ", pe)
            sys.exit(1)
