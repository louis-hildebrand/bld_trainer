from __future__ import annotations
from enum import auto, Enum


class GameMode(Enum):
    CE = auto()
    EC = auto()

    def __str__(self: GameMode) -> str:
        return self.name
