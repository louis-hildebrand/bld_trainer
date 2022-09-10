from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
import csv
import math
import os

from lib.rubiks_cube import Move
from lib.solver import Target


_RESULTS_FILENAME = "results/memo.csv"
_HEADER_ROW = [
    "start_utc",
    "scramble",
    "duration_millis",
    "edge_solution",
    "corner_solution",
    "success",
    "game_mode"
]


@dataclass
class Result:
    start_utc: datetime
    scramble: list[Move]
    total_duration: timedelta
    edge_solution: list[Target]
    corner_solution: list[Target]
    success: bool
    game_mode: str


def _initialize_results_file() -> None:
    os.makedirs(os.path.dirname(_RESULTS_FILENAME), exist_ok=True)
    with open(_RESULTS_FILENAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(_HEADER_ROW)


def save_result(result: Result) -> None:
    if not os.path.exists(_RESULTS_FILENAME):
        _initialize_results_file()
    with open(_RESULTS_FILENAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            result.start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            " ".join([str(m) for m in result.scramble]),
            None if result.total_duration is None else math.floor(result.total_duration.total_seconds() * 1000),
            "".join([str(t) for t in result.edge_solution]),
            "".join([str(t) for t in result.corner_solution]),
            result.success,
            result.game_mode
        ])
