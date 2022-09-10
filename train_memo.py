from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import math
import time

from lib.drawer import RubiksCubeDrawer
from lib.result import Result, save_result
from lib.rubiks_cube import Move, RubiksCube
from lib.scrambler import RubiksCubeScrambler
from lib.solver import M2Solver, Target
from lib.utils import clear_screen


class GameMode(Enum):
    CE_NODELAY = (False, False)
    EC_DELAY = (True, True)

    def edges_first(self: GameMode) -> bool:
        return self.value[0]

    def has_delay(self: GameMode) -> bool:
        return self.value[1]

    def __str__(self: GameMode) -> str:
        return self.name


@dataclass
class SolutionInput:
    edge_targets: list[Target]
    corner_targets: list[Target]
    total_duration: timedelta


def _select_game_mode() -> GameMode:
    print("Choose a game mode:")
    print("[CE] Corners, then edges (type as you go)")
    print("[EC] Edges, then corners (memorize everything and then type)")
    print()
    while True:
        user_input = input("# ")
        match user_input.upper():
            case "CE": return GameMode.CE_NODELAY
            case "EC": return GameMode.EC_DELAY
            case _:    print("Invalid input. Please choose a game mode from the list above.")


def _input_targets(msg: str) -> list[Target]:
    while True:
        raw_target_str = input(msg).upper().replace(" ", "")
        try:
            return [Target[t] for t in raw_target_str]
        except KeyError as ke:
            print(f"Invalid target {ke}. Please try again.\n")


def _human_readable_time(t: timedelta) -> str:
    ms = t.microseconds // 1000
    s = math.floor(t.total_seconds())
    m, s = divmod(s, 60)
    return f"{m:d}:{s:02d}.{ms:03d}"


def _input_solution(game_mode: GameMode) -> SolutionInput:
    start = time.time()
    end = 0  # Get Pylance to stop complaining about end being possibly unbound 
    if game_mode.has_delay():
        input("Press ENTER when you are ready to enter your solution")
        end = time.time()
        print()
    if game_mode.edges_first():
        edge_targets = _input_targets(f"Edges:\n# ")
        corner_targets = _input_targets(f"Corners:\n# ")
    else:
        corner_targets = _input_targets(f"Corners:\n# ")
        edge_targets = _input_targets(f"Edges:\n# ")
    if not game_mode.has_delay():
        end = time.time()
    return SolutionInput(edge_targets, corner_targets, timedelta(seconds = end - start))


def _save_and_display_result(result: Result) -> None:
    save_result(result)
    print("Memorization successful!" if result.success else "Memorization failed.")
    print(f"Time: {_human_readable_time(result.total_duration)}")


def _do_solve(game_mode: GameMode) -> None:
    clear_screen()
    # Generate random scramble and print scramble sequence
    scramble = RubiksCubeScrambler.random_scramble()
    print(f"Scramble: {' '.join([str(m) for m in scramble])}")
    rc = RubiksCube().apply(scramble)
    print("\n" + RubiksCubeDrawer.draw(rc) + "\n")
    # Input solution
    input("Press ENTER to start")
    print()
    start_utc = datetime.utcnow()
    si = _input_solution(game_mode)
    # Check solution
    rc = rc.apply([Move.Z2])
    rc = M2Solver.apply_solution(rc, si.edge_targets, si.corner_targets)
    print("\n" + RubiksCubeDrawer.draw(rc) + "\n")
    success = rc.is_solved()
    # Save and print stats
    result = Result(
        start_utc,
        scramble,
        si.total_duration,
        si.edge_targets,
        si.corner_targets,
        success,
        str(game_mode)
    )
    _save_and_display_result(result)
    input("\nPress ENTER to continue")
    time.sleep(0.1)


def main():
    clear_screen()
    game_mode = _select_game_mode()
    try:
        while True:
            _do_solve(game_mode)
    except KeyboardInterrupt:
        print()
        print("Exiting...")


if __name__ == "__main__":
    main()
