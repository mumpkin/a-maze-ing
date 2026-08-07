"""AMAAAAZIIIIIING !!!!."""

import json

from globals import config

# from maze.perfect_maze_generator import PerfectMazeGenerator
# from utils import RenderEngine

if __name__ == "__main__":
    """Main."""
    print("-- CONFIG:", json.dumps(config.toJSON(), indent=4))
    # maze = PerfectMazeGenerator()
    # maze.write_output()
    # engine = RenderEngine(maze.maze)
    # engine.render()
