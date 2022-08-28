from __future__ import annotations
from datetime import datetime, timedelta
import csv
import math
import os

from lib.rubiks_cube import Move
from lib.solver import Target


_RESULTS_FILENAME = "results/memo.csv"
_HEADER_ROW = [
    "datetime_utc", "scramble", "corner_time_millis", "edge_time_millis", "corner_solution", "edge_solution", "success"
]

def _initialize_results_file() -> None:
    os.makedirs(os.path.dirname(_RESULTS_FILENAME), exist_ok=True)
    with open(_RESULTS_FILENAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(_HEADER_ROW)

def save_result(
    dt: datetime, scramble: list[Move], corner_time: timedelta, edge_time: timedelta, corner_solution: list[Target],
    edge_solution: list[Target], success: bool
) -> None:
    if not os.path.exists(_RESULTS_FILENAME):
        _initialize_results_file()
    with open(_RESULTS_FILENAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            " ".join([str(m) for m in scramble]),
            math.floor(corner_time.total_seconds() * 1000),
            math.floor(edge_time.total_seconds() * 1000),
            "".join([str(t) for t in corner_solution]),
            "".join([str(t) for t in edge_solution]),
            success
        ])
