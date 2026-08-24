"""AMAAAAZIIIIIING !!!!."""

from maze import PerfectMazeGenerator
from utils import RenderEngine

if __name__ == "__main__":
    """Main."""
    maze = PerfectMazeGenerator()
    engine = RenderEngine(maze)
    maze.generate(engine)
    maze.write_output()
