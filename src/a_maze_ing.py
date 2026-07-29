"""AMAAAAZIIIIIING !!!!."""

from globals import config
from maze.perfect_maze_generator import PerfectMazeGenerator

if __name__ == "__main__":
    """Main."""
    print(config)
    print()
    maze = PerfectMazeGenerator()
    maze.init_grid()
    maze.write_grid()
    # print(maze.grid)
