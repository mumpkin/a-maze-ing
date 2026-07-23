from dataclasses import dataclass
from typing import Self


@dataclass
class Point:
    x: int
    y: int

    @classmethod
    def zero(cls) -> Self:
        return cls(0, 0)
