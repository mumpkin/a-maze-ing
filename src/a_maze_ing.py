"""AMAAAAZIIIIIING !!!!."""

import json

from globals import config
from maze import PerfectMazeGenerator

if __name__ == "__main__":
    """Main."""
    print("-- CONFIG:", json.dumps(config.toJSON(), indent=4))
    maze = PerfectMazeGenerator()
