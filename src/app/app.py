"""App."""

import os
import subprocess
import sys
from enum import Enum, auto

import globals
from maze import MazeGenerator, PerfectMazeGenerator
from maze.imperfect_maze_generator import ImperfectMazeGenerator
from utils import RenderEngine


class AppState(Enum):
    """."""

    TitleScreen = auto()
    Maze = auto()
    Config = auto()
    ColorScheme = auto()


class App:
    """App definition."""

    def __init__(self):
        self.state: AppState = AppState.TitleScreen
        self.generator: MazeGenerator = (
            PerfectMazeGenerator()
            if globals.config.perfect
            else ImperfectMazeGenerator()
        )
        self.engine: RenderEngine = RenderEngine(self.generator)

    def run(self) -> None:
        """Run the app."""
        while True:
            match self.state:
                case AppState.TitleScreen:
                    self._title()
                case AppState.Maze:
                    self._maze()
                case AppState.Config:
                    self._config()
                case AppState.ColorScheme:
                    self._color_scheme()

    def _title(self):
        _ = subprocess.run("clear")
        print("\033[?25l", end="")
        self._print_title()
        self._route_title_action(self._get_user_input())

    def _print_title(self):
        """."""
        term_width, term_height = os.get_terminal_size()
        heading: list[str] = [
            "\033[1m",
            " _______     ___ ___ _______ _______ _______     ___ ______  _______ ",  # noqa: E501
            "|   _   |   |   Y   |   _   |   _   |   _   |   |   |   _  \\|   _   |",  # noqa: E501
            "|.  1   |   |.      |.  1   |___|   |.  1___|   |.  |.  |   |.  |___|",  # noqa: E501
            "|.  _   |   |. \\_/  |.  _   |/  ___/|.  __)_    |.  |.  |   |.  |   |",  # noqa: E501
            "|:  |   |   |:  |   |:  |   |:  1  \\|:  1   |   |:  |:  |   |:  1   |",  # noqa: E501
            "|::.|:. |   |::.|:. |::.|:. |::.. . |::.. . |   |::.|::.|   |::.. . |",  # noqa: E501
            "`--- ---'   `--- ---`--- ---`-------`-------'   `---`--- ---`-------'",  # noqa: E501
            "\033[0m",
            "s: start       ",
            "c: show config ",
            "o: color scheme",
            "q: quit        ",
        ]
        title_height: int = len(heading)
        title_width: int = len(max(heading, key=len))
        if title_width >= term_width or title_height >= term_height:
            self._wait_term_size(title_width, title_height)
            term_width, term_height = os.get_terminal_size()
        for _ in range((term_height - title_height) // 2):
            print()
        for line in heading:
            print(line.center(term_width))

    def _route_title_action(self, action: str):
        match action.lower():
            case "s":
                _ = subprocess.run("clear")
                self.state = AppState.Maze
            case "c":
                _ = subprocess.run("clear")
                self.state = AppState.Config
            case "o":
                _ = subprocess.run("clear")
                self.state = AppState.ColorScheme
            case "q":
                _ = subprocess.run("clear")
                exit(0)
            case _:
                pass

    def _config(self):
        _ = subprocess.run("clear")
        print("\033[?25l", end="")
        self._print_config()
        self._route_config_action(self._get_user_input())

    def _print_config(self):
        """."""
        term_width, term_height = os.get_terminal_size()
        heading: list[str] = [
            "\033[1m",
            " _______ _______ ______  _______ ___ _______ ",
            "|   _   |   _   |   _  \\|   _   |   |   _   |",
            "|.  1___|.  |   |.  |   |.  1___|.  |.  |___|",
            "|.  |___|.  |   |.  |   |.  __) |.  |.  |   |",
            "|:  1   |:  1   |:  |   |:  |   |:  |:  1   |",
            "|::.. . |::.. . |::.|   |::.|   |::.|::.. . |",
            "`-------`-------`--- ---`---'   `---`-------'",
            "\033[0m",
        ]
        configs: list[str] = [
            f"- WIDTH: {globals.config.width}",
            f"- HEIGHT: {globals.config.height}",
            f"- ENTRY: {globals.config.entry.__dict__}",
            f"- EXIT: {globals.config.exit.__dict__}",
            f"- PERFECT: {globals.config.perfect}",
            f"- SEED: {globals.config.seed}",
            f"- OUTPUT FILE: {globals.config.output_file}",
            f"- CONGIF FILE: {sys.argv[1]}",
        ]
        title_height: int = len(configs) + len(heading)
        title_width: int = len(max(heading, key=len))
        if title_width >= term_width or title_height >= term_height:
            self._wait_term_size(title_width, title_height)
            term_width, term_height = os.get_terminal_size()
        option_width: int = len(max(configs, key=len))
        fill_menu: str = "".join(
            [" " for _ in range((term_width - option_width) // 2)]
        )
        for _ in range((term_height - len(heading) - len(configs)) // 2):
            print()
        for line in heading:
            print(line.center(term_width))
        for line in configs:
            print(fill_menu + line)
        print()
        print("t: title screen - s: start - q: quit".center(term_width))

    def _route_config_action(self, action: str):
        match action.lower():
            case "s":
                _ = subprocess.run("clear")
                self.state = AppState.Maze
            case "t":
                _ = subprocess.run("clear")
                self.state = AppState.TitleScreen
            case "q":
                _ = subprocess.run("clear")
                exit(0)
            case _:
                pass

    def _maze(self):
        """."""
        _ = subprocess.run("clear")
        self.generator.generate(self.engine)
        print("r: re-generate - t: title screen - q: quit")
        self._route_maze_action(self._get_user_input())

    def _route_maze_action(self, action: str):
        match action.lower():
            case "r":
                _ = subprocess.run("clear")
                self.state = AppState.Maze
            case "t":
                _ = subprocess.run("clear")
                self.state = AppState.TitleScreen
            case "q":
                _ = subprocess.run("clear")
                exit(0)
            case _:
                pass

    def _color_scheme(self):
        _ = subprocess.run("clear")
        print("\033[?25l", end="")
        self._print_color_scheme()
        self._route_color_scheme_action(self._get_user_input())

    def _print_color_scheme(self):
        """."""
        term_width, term_height = os.get_terminal_size()
        heading: list[str] = [
            "\033[1m",
            " _______ _______ ___     _______ _______ _______ ",
            "|   _   |   _   |   |   |   _   |   _   |   _   |",
            "|.  1___|.  |   |.  |   |.  |   |.  l   |   1___|",
            "|.  |___|.  |   |.  |___|.  |   |.  _   |____   |",
            "|:  1   |:  1   |:  1   |:  1   |:  |   |:  1   |",
            "|::.. . |::.. . |::.. . |::.. . |::.|:. |::.. . |",
            "`-------`-------`-------`-------`--- ---`-------'",
            "\033[0m",
            "s: start      ",
            "c: show config",
            "q: quit       ",
        ]
        title_height: int = len(heading)
        title_width: int = len(max(heading, key=len))
        if title_width >= term_width or title_height >= term_height:
            self._wait_term_size(title_width, title_height)
            term_width, term_height = os.get_terminal_size()
        for _ in range((term_height - title_height) // 2):
            print()
        for line in heading:
            print(line.center(term_width))

    def _route_color_scheme_action(self, action: str):
        match action:
            case "j":
                print("pouik")
            case "k":
                print("pouak")
            case "\n":
                pass
            case "t":
                self.state = AppState.TitleScreen
            case "s":
                self.state = AppState.Maze
            case _:
                pass

    def _wait_term_size(self, width: int, height: int):
        term_width, term_height = os.get_terminal_size()
        while width >= term_width or height >= term_height:
            _ = subprocess.run("clear")
            print("\033[1m")
            print("Adviced terminal size:".center(term_width))
            print(f"{width}x{height}".center(term_width))
            print("\033[0m")
            print("return: retry - i: ignore - q: quit".center(term_width))
            term_width, term_height = os.get_terminal_size()
            user_input = self._get_user_input()
            match user_input:
                case "\n":
                    continue
                case "i":
                    break
                case "q":
                    exit(0)
                case _:
                    pass
        _ = subprocess.run("clear")

    def _get_user_input(self) -> str:
        import sys
        import termios

        fd = sys.stdin.fileno()
        orig = termios.tcgetattr(fd)

        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ICANON
        new[6][termios.VMIN] = 1
        new[6][termios.VTIME] = 0

        try:
            termios.tcsetattr(fd, termios.TCSAFLUSH, new)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, orig)
