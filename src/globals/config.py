"""Load and validate the global config."""

import json
import os
import sys
from typing import Self

import dotenv
from pydantic import (
    BaseModel,
    Field,
    model_validator,
)

from enums import ConfigKey
from utils import Point


class Config(BaseModel):
    """Config representation."""

    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: Point
    exit: Point
    output_file: str
    perfect: bool = Field(default=True)
    seed: int | None = Field(default=None)
    delay: float = Field(gt=0)

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
    def get_env() -> dict[ConfigKey, str]:
        """Return the environment variables."""
        vars: dict[ConfigKey, str] = {}
        missing_vars: list[str] = []

        for option in [o for o in ConfigKey]:
            var: str | None = os.getenv(option.value.upper())
            if not var:
                missing_vars.append(option.value)
            else:
                vars.update({option: var})

        if len(missing_vars) != 0:
            raise ValueError(f"Missing config options: {missing_vars}.")

        return vars

    @model_validator(mode="after")
    def _check_entry(self) -> Self:
        if self.entry.x not in range(self.width):
            raise ValueError(
                f"Entry X must be between 0 and {self.width}(excluded)."
            )
        if self.entry.y not in range(self.height):
            raise ValueError(
                f"Entry Y must be between 0 and {self.height}(excluded)."
            )
        return self

    @model_validator(mode="after")
    def _check_exit(self) -> Self:
        if self.exit.x not in range(self.width):
            raise ValueError(
                f"Exit X must be between 0 and {self.width}(excluded)."
            )
        if self.exit.y not in range(self.height):
            raise ValueError(
                f"Exit Y must be between 0 and {self.height}(excluded)."
            )
        return self

    @model_validator(mode="after")
    def _check_entry_exit_not_eq(self) -> Self:
        if self.entry == self.exit:
            raise ValueError("Entry and Exit must not be equal.")
        return self

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
                width=int(env[ConfigKey.WIDTH]),
                height=int(env[ConfigKey.HEIGHT]),
                entry=Point(
                    x=int(env[ConfigKey.ENTRY].split(",")[0]),
                    y=int(env[ConfigKey.ENTRY].split(",")[1]),
                ),
                exit=Point(
                    x=int(env[ConfigKey.EXIT].split(",")[0]),
                    y=int(env[ConfigKey.EXIT].split(",")[1]),
                ),
                output_file=env[ConfigKey.OUTPUT_FILE],
                perfect=env[ConfigKey.PERFECT].lower() == "true",
                seed=int(env[ConfigKey.SEED])
                if env[ConfigKey.SEED].isdigit()
                else None,
                delay=float(env[ConfigKey.DELAY]),
            )
            return config
        except Exception as err:
            print(f"Config error: {err}", file=sys.stderr)
            sys.exit(1)


config: Config = Config.load_config(sys.argv[1])
