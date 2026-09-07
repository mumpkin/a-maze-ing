"""Color Schemes enums."""

from typing import final


class ColorScheme:
    """Default color scheme."""

    def __init__(self) -> None:
        self.name: str = "Default"
        self.TRANSPARENT: str = "\033[49m"
        self.ENTRY: str = "\033[102m"
        self.EXIT: str = "\033[101m"
        self.IDLE: str = "\033[100m"
        self.LOCKED: str = "\033[106m"
        self.VISITED: str = "\033[107m"
        self.VISITING: str = "\033[105m"
        self.OPTIMAL_PATH: str = "\033[43m"


@final
class IcedColorScheme(ColorScheme):
    """Iced color scheme."""

    def __init__(self) -> None:
        super().__init__()
        self.name: str = "Iced"
        self.TRANSPARENT = "\033[49m"
        self.ENTRY = "\033[45m"
        self.EXIT = "\033[43m"
        self.IDLE = "\033[44m"
        self.LOCKED = "\033[107m"
        self.VISITED = "\033[101m"
        self.VISITING = "\033[106m"
        self.OPTIMAL_PATH = "\033[103m"


@final
class FiredColorScheme(ColorScheme):
    """Fired color scheme."""

    def __init__(self) -> None:
        super().__init__()
        self.name: str = "R.I.P tes n'œils"
        self.TRANSPARENT = "\033[49m"
        self.ENTRY = "\033[45m"
        self.EXIT = "\033[43m"
        self.IDLE = "\033[101m"
        self.LOCKED = "\033[105m"
        self.VISITED = "\033[106m"
        self.VISITING = "\033[44m"
        self.OPTIMAL_PATH = "\033[107m"
