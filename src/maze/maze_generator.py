from typing import Any
from abc import ABC, abstractmethod


class MazeGenerator(ABC):
    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def get_config_key(self, key: str) -> Any:
        return self._config.get(key)

    @abstractmethod
    def build_maze(self) -> Any:
        """
        Builds the maze and displays the shortest route
        between the entry point and the exit point
        """
        pass

    def write_output(self) -> None:
        """
        Writes the maze output into the filename
        Specified in the configuration file
        """
        try:
            pass
            # with open(self.get_config_key('OUTPUT_FILENAME'), 'w') as file:
        except FileNotFoundError as fe:
            print(fe)
