"""Load and validate the global config."""

import json
import os
import sys
from enum import Enum
from typing import Self

import dotenv
from pydantic import BaseModel, Field

from utils import Point


class ConfigOption(str, Enum):
    """Available config options."""

    WIDTH = "width"
    HEIGHT = "height"
    ENTRY = "entry"
    EXIT = "exit"
    OUTPUT_FILE = "output_file"
    PERFECT = "perfect"
    SEED = "seed"


class Config(BaseModel):
    """Config representation."""

    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: Point
    exit: Point
    output_file: str
    perfect: bool = Field(default=True)
    seed: int | None = Field(default=None)

    def toJSON(self) -> str:
        """Return the json representation of Config."""
        return json.dumps(
            {
                "width": self.width,
                "height": self.height,
                "entry": self.entry.__dict__,
                "exit": self.exit.__dict__,
                "output_file": self.output_file,
                "perfect": self.perfect,
                "seed": self.seed,
            },
            indent=4,
        )

    @staticmethod
    def get_env() -> dict[ConfigOption, str]:
        """Return the environment variables."""
        vars: dict[ConfigOption, str] = {}
        missing_vars: list[str] = []

        for option in [o for o in ConfigOption]:
            var: str | None = os.getenv(option.value.upper())
            if not var:
                missing_vars.append(option.value)
            else:
                vars.update({option: var})

        if len(missing_vars) != 0:
            raise ValueError(f"Missing config options: {missing_vars}.")

        return vars

    @classmethod
    def load_config(cls, path: str) -> Self:
        """
        Return the instance of config.

        Keyword Argument:
        path: str -- Path to the config file.
        """
        try:
            _ = dotenv.load_dotenv(path)
            env = Config.get_env()

            config = cls(
                width=int(env[ConfigOption.WIDTH]),
                height=int(env[ConfigOption.HEIGHT]),
                entry=Point(
                    x=int(env[ConfigOption.ENTRY].split(",")[0]),
                    y=int(env[ConfigOption.ENTRY].split(",")[1]),
                ),
                exit=Point(
                    x=int(env[ConfigOption.EXIT].split(",")[0]),
                    y=int(env[ConfigOption.EXIT].split(",")[1]),
                ),
                output_file=env[ConfigOption.OUTPUT_FILE],
                perfect=env[ConfigOption.PERFECT].lower() == "true",
                seed=int(env[ConfigOption.SEED])
                if env[ConfigOption.SEED].isdigit()
                else None,
            )
            return config
        except Exception as err:
            print(f"Config error: {err}")
            sys.exit(1)


config: Config = Config.load_config(sys.argv[1])
