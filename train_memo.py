from datetime import datetime, timedelta
import math
import time

from lib.drawer import RubiksCubeDrawer
from lib.result import save_result
from lib.rubiks_cube import Move, RubiksCube
from lib.scrambler import RubiksCubeScrambler
from lib.solver import M2Solver, Target
from lib.utils import clear_screen


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


def main():
    while True:
        clear_screen()
        # Generate random scramble and print scramble sequence
        scramble = RubiksCubeScrambler.random_scramble()
        print(f"Scramble: {' '.join([str(m) for m in scramble])}")
        rc = RubiksCube().apply(scramble)
        print()
        print(RubiksCubeDrawer.draw(rc))
        print()
        # Input solution
        input("Press ENTER to start")
        print()
        start_utc = datetime.utcnow()
        start = time.time()
        corner_targets = _input_targets(f"Corners:\n# ")
        corner_end_time = time.time()
        edge_targets = _input_targets(f"Edges:\n# ")
        edge_end_time = time.time()
        # Check solution
        rc = rc.apply([Move.Z2])
        rc = M2Solver.apply_solution(rc, edge_targets, corner_targets)
        print()
        print(RubiksCubeDrawer.draw(rc))
        print()
        # Save and print stats
        success = rc.is_solved()
        corners_duration = timedelta(seconds = corner_end_time - start)
        edges_duration = timedelta(seconds = edge_end_time - corner_end_time)
        save_result(
            start_utc, scramble, corners_duration, edges_duration, corner_targets, edge_targets, success
        )
        print("Memorization successful!" if success else "Memorization failed.")
        print(f"Corners: {_human_readable_time(corners_duration)}")
        print(f"Edges:   {_human_readable_time(edges_duration)}")
        print(f"Total:   {_human_readable_time(corners_duration + edges_duration)}")
        print()
        input("Press ENTER to continue")
        time.sleep(0.1)


if __name__ == "__main__":
    main()
