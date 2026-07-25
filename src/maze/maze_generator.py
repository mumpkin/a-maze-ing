"""."""

from abc import ABC, abstractmethod
from typing import Any


class MazeGenerator(ABC):
    """."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    @abstractmethod
    def build_maze(self) -> Any:
        """Build the maze."""
        pass

    def write_output(self) -> None:
        """Write the maze output into the filename."""
        try:
            pass
            # with open(self.get_config_key('OUTPUT_FILENAME'), 'w') as file:
        except FileNotFoundError as fe:
            print(fe)
