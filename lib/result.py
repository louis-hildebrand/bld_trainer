from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
import csv
import math
import os

from lib.game_mode import GameMode
from lib.rubiks_cube import Move
from lib.solver import Target


_RESULTS_FILENAME = "results/memo.csv"
_HEADER_ROW = [
    "start_utc",
    "scramble",
    "corners_millis",
    "edges_millis",
    "total_millis",
    "edge_solution",
    "corner_solution",
    "success",
    "game_mode"
]


@dataclass
class Result:
    start_utc: datetime
    scramble: list[Move]
    corner_duration: timedelta
    edge_duration: timedelta
    total_duration: timedelta
    edge_solution: list[Target]
    corner_solution: list[Target]
    success: bool
    game_mode: GameMode


def _initialize_results_file() -> None:
    os.makedirs(os.path.dirname(_RESULTS_FILENAME), exist_ok=True)
    with open(_RESULTS_FILENAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(_HEADER_ROW)


def _duration_to_millis(td: timedelta | None) -> int | None:
    return None if td is None else math.floor(td.total_seconds() * 1000)


def save_result(result: Result) -> None:
    if not os.path.exists(_RESULTS_FILENAME):
        _initialize_results_file()
    with open(_RESULTS_FILENAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            result.start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            " ".join([str(m) for m in result.scramble]),
            _duration_to_millis(result.corner_duration),
            _duration_to_millis(result.edge_duration),
            _duration_to_millis(result.total_duration),
            "".join([str(t) for t in result.edge_solution]),
            "".join([str(t) for t in result.corner_solution]),
            result.success,
            str(result.game_mode)
        ])
