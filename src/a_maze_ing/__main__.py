"""A-MAZE-ING.

 _____     _____ _____ _____ _____     _____ _____ _____
|  _  |___|     |  _  |__   |   __|___|     |   | |   __|
|     |___| | | |     |   __|   __|___|-   -| | | |  |  |
|__|__|   |_|_|_|__|__|_____|_____|   |_____|_|___|_____|
"""

import sys

from . import App

if __name__ == "__main__":
    """Run the app."""
    try:
        if len(sys.argv) <= 1:
            raise Exception("You must provide a config file as argument.")
        app = App()
        app.run()
    except Exception as e:
        print("[ERROR]:", e, file=sys.stderr)
