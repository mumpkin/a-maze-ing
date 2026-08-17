"""AMAAAAZIIIIIING !!!!."""

import json
from random import seed

from globals import config
from maze.imperfect_maze_generator import ImperfectMazeGenerator

# from maze.perfect_maze_generator import PerfectMazeGenerator
from utils import RenderEngine

if __name__ == "__main__":
    """Main."""
    # seed(520)
    # print("-- CONFIG:", json.dumps(config.toJSON(), indent=4))
    maze = ImperfectMazeGenerator()
    maze.write_output()
    engine = RenderEngine(maze)
    maze.generate()
    engine.render()
    maze.write_output()
    print()
