"""Color Schemes enums."""

from typing_extensions import final


class ColorScheme:
    """."""

    def __init__(self):
        self.TRANSPARENT = "\033[49m"
        self.ENTRY = "\033[102m"
        self.EXIT = "\033[101m"
        self.IDLE = "\033[100m"
        self.LOCKED = "\033[106m"
        self.VISITED = "\033[107m"
        self.VISITING = "\033[105m"
        self.OPTIMAL_PATH = "\033[43m"


@final
class IceColorScheme(ColorScheme):
    """Iced color scheme."""

    def __init__(self):
        super().__init__()
        self.TRANSPARENT = "\033[49m"
        self.ENTRY = "\033[45m"
        self.EXIT = "\033[43m"
        self.IDLE = "\033[44m"
        self.LOCKED = "\033[107m"
        self.VISITED = "\033[104m"
        self.VISITING = "\033[106m"
        self.OPTIMAL_PATH = "\033[103m"
