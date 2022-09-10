from dataclasses import dataclass
from datetime import datetime, timedelta
import math
import time

from lib.drawer import RubiksCubeDrawer
from lib.game_mode import GameMode
from lib.result import Result, save_result
from lib.rubiks_cube import Move, RubiksCube
from lib.scrambler import RubiksCubeScrambler
from lib.solver import M2Solver, Target
from lib.utils import clear_screen


@dataclass
class SolutionInput:
    edge_targets: list[Target]
    corner_targets: list[Target]
    corner_duration: timedelta
    edge_duration: timedelta
    total_duration: timedelta


def _select_game_mode() -> GameMode:
    print("Choose a game mode:")
    print("[CE] Corners, then edges (type as you go)")
    print("[EC] Edges, then corners (memorize everything and then type)")
    print()
    while True:
        user_input = input("# ")
        try:
            return GameMode[user_input.upper()]
        except KeyError:
            print("Invalid input. Please choose a game mode from the list above.")


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


def _input_solution_CE() -> SolutionInput:
    start = time.time()
    corner_targets = _input_targets(f"Corners:\n# ")
    corner_end_time = time.time()
    edge_targets = _input_targets(f"Edges:\n# ")
    edge_end_time = time.time()
    corner_duration = timedelta(seconds = corner_end_time - start)
    edge_duration = timedelta(seconds = edge_end_time - corner_end_time)
    total_duration = corner_duration + edge_duration
    return SolutionInput(edge_targets, corner_targets, corner_duration, edge_duration, total_duration)


def _save_and_display_result(result: Result) -> None:
    save_result(result)
    print("Memorization successful!" if result.success else "Memorization failed.")
    print(f"Corners: {_human_readable_time(result.corner_duration)}")
    print(f"Edges:   {_human_readable_time(result.edge_duration)}")
    print(f"Total:   {_human_readable_time(result.total_duration)}")


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
    si = _input_solution_CE()
    # Check solution
    rc = rc.apply([Move.Z2])
    rc = M2Solver.apply_solution(rc, si.edge_targets, si.corner_targets)
    print("\n" + RubiksCubeDrawer.draw(rc) + "\n")
    success = rc.is_solved()
    # Save and print stats
    result = Result(
        start_utc,
        scramble,
        si.corner_duration,
        si.edge_duration,
        si.total_duration,
        si.edge_targets,
        si.corner_targets,
        success,
        game_mode
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
