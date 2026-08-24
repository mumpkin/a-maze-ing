"""AMAAAAZIIIIIING !!!!."""

import json

<<<<<<< HEAD
# from random import seed
from globals import config
from maze.imperfect_maze_generator import ImperfectMazeGenerator

# from maze.perfect_maze_generator import PerfectMazeGenerator
=======
import globals
from maze import PerfectMazeGenerator
>>>>>>> 23aaa95 (wip)
from utils import RenderEngine

if __name__ == "__main__":
    """Main."""
<<<<<<< HEAD
    # seed(520)
    print("-- CONFIG:", json.dumps(config.toJSON(), indent=4))
    maze = ImperfectMazeGenerator()
    maze.write_output()
    engine = RenderEngine(maze)
    maze.generate()
    engine.render()
    print()
=======
    maze = PerfectMazeGenerator()
    maze.write_output()
    engine = RenderEngine(maze)
    maze.generate(engine)
    engine.render()
>>>>>>> 23aaa95 (wip)
