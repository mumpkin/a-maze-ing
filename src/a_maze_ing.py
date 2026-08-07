"""AMAAAAZIIIIIING !!!!."""

import json

from globals import config

if __name__ == "__main__":
    """Main."""
    print("-- CONFIG:", json.dumps(config.toJSON(), indent=4))
