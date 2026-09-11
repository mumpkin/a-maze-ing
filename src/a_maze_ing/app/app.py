"""App."""

import os
import subprocess
import sys
from enum import Enum, auto

from ..enums.color_scheme import ColorScheme, FiredColorScheme, IcedColorScheme
from ..globals.config import config
from ..maze.imperfect_maze_generator import ImperfectMazeGenerator
from ..maze.maze_generator import MazeGenerator
from ..maze.perfect_maze_generator import PerfectMazeGenerator
from ..utils.render import RenderEngine


class AppState(Enum):
    """Available app states."""

    TitleScreen = auto()
    Maze = auto()
    VizualiseMaze = auto()
    Config = auto()
    ColorScheme = auto()


class App:
    """App definition.

    Attributes
    ----------
    state : AppState, default=AppState.TitleScreen
        State of the app, screen currently displayed.
    generator : MazeGenerator
        Generator instance, its type depends on `config.perfect`.
    """

    def __init__(self) -> None:
        self.state: AppState = AppState.TitleScreen
        self.generator: MazeGenerator = (
            PerfectMazeGenerator()
            if config.perfect
            else ImperfectMazeGenerator()
        )
        self.schemes_index: int = 0
        self.color_schemes: list[ColorScheme] = [
            ColorScheme(),
            IcedColorScheme(),
            FiredColorScheme(),
        ]
        self.selected_colors: ColorScheme = self.color_schemes[
            self.schemes_index
        ]
        self.engine: RenderEngine = RenderEngine(self.generator)
        self.engine.color_scheme = self.selected_colors

    def run(self) -> None:
        """Run the app."""
        while True:
            match self.state:
                case AppState.TitleScreen:
                    self._title_screen()
                case AppState.Maze:
                    self._maze_screen()
                case AppState.VizualiseMaze:
                    self._vizualise_maze_screen()
                case AppState.Config:
                    self._config_screen()
                case AppState.ColorScheme:
                    self._color_scheme_screen()

    def _title_screen(self) -> None:
        _ = subprocess.run("clear")
        print("\033[?25l", end="")
        self._print_title_menu()
        self._route_title_action(self._get_user_input())

    def _print_title_menu(self) -> None:
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
            "s: instant generation  ",
            "v: vizualise generation",
            "c: show config         ",
            "o: color scheme        ",
            "q: quit                ",
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

    def _route_title_action(self, action: str) -> None:
        match action.lower():
            case "s":
                _ = subprocess.run("clear")
                self.state = AppState.Maze
            case "v":
                _ = subprocess.run("clear")
                self.state = AppState.VizualiseMaze
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

    def _config_screen(self) -> None:
        _ = subprocess.run("clear")
        print("\033[?25l", end="")
        self._print_config()
        self._route_config_action(self._get_user_input())

    def _print_config(self) -> None:
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
            f"- WIDTH: {config.width}",
            f"- HEIGHT: {config.height}",
            f"- ENTRY: {config.entry.__dict__}",
            f"- EXIT: {config.exit.__dict__}",
            f"- PERFECT: {config.perfect}",
            f"- SEED: {config.seed}",
            f"- DELAY: {config.delay}",
            f"- OUTPUT FILE: {config.output_file}",
            f"- CONGIF FILE: {sys.argv[1]}",
        ]
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
        print("t: title screen - q: quit".center(term_width))

    def _route_config_action(self, action: str) -> None:
        match action.lower():
            case "t":
                _ = subprocess.run("clear")
                self.state = AppState.TitleScreen
            case "q":
                _ = subprocess.run("clear")
                exit(0)
            case _:
                pass

    def _maze_screen(self) -> None:
        _ = subprocess.run("clear")
        self.generator.init_maze()
        _ = subprocess.run("clear")
        self.generator.generate()
        self.generator.compute_optimal_path()
        self.engine.render()
        print(
            "r: re-generate{} - s: save - t: title screen - q: quit".format(
                " - h: hide optimal path"
                if self.engine.opti_toggle
                else " - h: show optimal path"
            )
        )
        self._route_maze_action()

    def _vizualise_maze_screen(self) -> None:
        _ = subprocess.run("clear")
        self.generator.init_maze()
        _ = subprocess.run("clear")
        self.generator.generate(self.engine)
        _ = subprocess.run("clear")
        self.generator.compute_optimal_path(self.engine)
        _ = subprocess.run("clear")
        self.engine.render()
        print(
            "r: re-generate{} - s: save - t: title screen - q: quit".format(
                " - h: hide optimal path"
                if self.engine.opti_toggle
                else " - h: show optimal path"
            )
        )
        self._route_maze_action()

    def _route_maze_action(self) -> None:
        while True:
            action = self._get_user_input()
            match action.lower():
                case "r":
                    _ = subprocess.run("clear")
                    self.state = self.state
                    break
                case "h":
                    _ = subprocess.run("clear")
                    self.engine.opti_toggle = not self.engine.opti_toggle
                    self.engine.render()
                    print(
                        "r: re-generate",
                        "- h: hide optimal path"
                        if self.engine.opti_toggle
                        else "- h: show optimal path",
                        "- s: save - t: title screen - q: quit",
                    )

                case "s":
                    self.generator.save()
                    print(
                        f"\rSaved grid to: {config.output_file}\033[K",
                        end="\r",
                    )
                case "t":
                    _ = subprocess.run("clear")
                    self.state = AppState.TitleScreen
                    break
                case "q":
                    _ = subprocess.run("clear")
                    exit(0)
                case _:
                    if action == "\n":
                        action = "newline"
                    print(f"\rInvalid input: '{action}'\033[K", end="\r")

    def _color_scheme_screen(self) -> None:
        _ = subprocess.run("clear")
        print("\033[?25l", end="")
        self._print_color_scheme()
        self._route_color_scheme_action(self._get_user_input())

    def _print_color_scheme(self) -> None:
        term_width, term_height = os.get_terminal_size()
        bg = self.selected_colors.VISITING
        heading: list[str] = [
            f"\033[1m{bg}",
            " _______ _______ ___     _______ _______ ",
            "|   _   |   _   |   |   |   _   |   _   |",
            "|.  1___|.  |   |.  |   |.  |   |.  l   |",
            "|.  |___|.  |   |.  |___|.  |   |.  _   |",
            "|:  1   |:  1   |:  1   |:  1   |:  |   |",
            "|::.. . |::.. . |::.. . |::.. . |::.|:. |",
            "`-------`-------`-------`-------`--- --- ",
            "_______ _______ ___ ___ _______ ___ ___ _______ _______ ",
            "|   _   |   _   |   Y   |   _   |   Y   |   _   |   _   |",
            "|   1___|.  1___|.  1   |.  1___|.      |.  1___|   1___|",
            "|____   |.  |___|.  _   |.  __)_|. \\_/  |.  __)_|____   |",
            "|:  1   |:  1   |:  |   |:  1   |:  |   |:  1   |:  1   |",
            "|::.. . |::.. . |::.|:. |::.. . |::.|:. |::.. . |::.. . |",
            "`-------`-------`--- ---`-------`--- ---`-------`-------'",
            "",
            "\033[0m",
            *[c.name for c in self.color_schemes],
            "",
            "j|k: ↓|↑ - return: save selection - t: title screen - q: quit",
        ]
        title_height: int = len(heading)
        for _ in range((term_height - title_height) // 2):
            print()
        for line in heading:
            if (
                line == self.selected_colors.name
                and line == self.engine.color_scheme.name
            ):
                print(f"> [{line}] <".center(term_width))
            elif line == self.selected_colors.name:
                print(f"> {line} <".center(term_width))
            elif line == self.engine.color_scheme.name:
                print(f"[ {line} ]".center(term_width))
            elif line == f"\033[1m{bg}" or line == "\033[0m" or line == bg:
                print(line)
            else:
                print(line.center(term_width))

    def _route_color_scheme_action(self, action: str) -> None:
        match action:
            case "j":
                self.schemes_index += 1
                if self.schemes_index > len(self.color_schemes) - 1:
                    self.schemes_index = 0
                self.selected_colors = self.color_schemes[self.schemes_index]
            case "k":
                self.schemes_index -= 1
                if self.schemes_index < 0:
                    self.schemes_index = len(self.color_schemes) - 1
                self.selected_colors = self.color_schemes[self.schemes_index]
            case "\n":
                self.engine.color_scheme = self.selected_colors
            case "t":
                self.state = AppState.TitleScreen
            case "q":
                _ = subprocess.run("clear")
                exit(0)
            case _:
                pass

    def _wait_term_size(self, width: int, height: int) -> None:
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
