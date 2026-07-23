import sys
from io import TextIOWrapper
from typing import Any

from enums import ConfigKey

from .point import Point

config: dict[ConfigKey, Any] = dict()


def _get_config_line(line: str) -> tuple[ConfigKey, Any]:
    if len(line.strip()) == 0:
        raise ValueError("Config file corrupted!")

    data: list[str] = line.split("#")[0].strip().split("=")

    if len(data) == 2:
        match data[0].lower():
            case ConfigKey.WIDTH.value:
                width: int = int(data[1])
                if width <= 0:
                    raise ValueError("")
                return (ConfigKey.WIDTH, int(data[1]))

            case ConfigKey.HEIGHT.value:
                return (ConfigKey.HEIGHT, int(data[1]))

            case ConfigKey.ENTRY.value:
                coords = data[1].split(",")
                if len(coords) != 2:
                    raise ValueError("Wrong ENTRY value format.")
                return ConfigKey.ENTRY, Point(
                    int(coords[0].strip()), int(coords[1].strip())
                )

            case ConfigKey.EXIT.value:
                coords = data[1].split(",")
                if len(coords) != 2:
                    raise ValueError("Wrong EXIT value format.")
                return ConfigKey.EXIT, Point(
                    int(coords[0].strip()), int(coords[1].strip())
                )

            case ConfigKey.OUTPUT_FILE.value:
                return (ConfigKey.OUTPUT_FILE, data[1])

            case ConfigKey.PERFECT.value:
                match data[1].lower():
                    case "true":
                        return (ConfigKey.PERFECT, True)
                    case "false":
                        return (ConfigKey.PERFECT, False)
                    case _:
                        raise ValueError(
                            "Wrong PERFECT format (true or false)"
                        )

            case ConfigKey.SEED.value:
                if not data[1].isdigit():
                    return (ConfigKey.SEED, None)
                return (ConfigKey.SEED, int(data[1]))

            case _:
                raise ValueError("Unknown config key.")

    raise ValueError("Config file corrupted!")


def _get_config_data(file: TextIOWrapper) -> dict[ConfigKey, Any]:
    data: dict[ConfigKey, Any] = {}
    line: str = file.readline()
    while len(line) > 0:
        key, value = _get_config_line(line)
        data.update({key: value})
        line = file.readline()
    return data


def load_config(path: str) -> dict[ConfigKey, Any]:
    """
    Return the configuation.

    Keyword arguments:
    path: str -- Path to the config file.
    """
    file = open(path, "r")
    config = _get_config_data(file)

    return config


try:
    config = load_config(sys.argv[1])
except Exception as err:
    print(err, file=sys.stderr)
    sys.exit(1)
