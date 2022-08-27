import time

from lib.drawer import RubiksCubeDrawer
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


def main():
    while True:
        # Generate random scramble and print scramble sequence
        scramble = RubiksCubeScrambler.random_scramble()
        print(f"Scramble: {' '.join([str(m) for m in scramble])}")
        rc = RubiksCube().apply(scramble)
        print()
        print(RubiksCubeDrawer.draw(rc))
        print()
        # Input solution
        input("Press ENTER to start")
        start = time.time()
        print()
        corner_targets = _input_targets(f"Corners:\n# ")
        edge_targets = _input_targets(f"Edges:\n# ")
        end = time.time()
        # Check solution
        rc = rc.apply([Move.Z2])
        rc = M2Solver.apply_solution(rc, edge_targets, corner_targets)
        print()
        print(RubiksCubeDrawer.draw(rc))
        print()
        if rc.is_solved():
            print(f"Memorization successful!")
        else:
            print(f"Memorization failed.")
        print(f"Time: {end - start:.2f} s")
        print()
        input("Press ENTER to continue")
        clear_screen()
        time.sleep(0.1)


if __name__ == "__main__":
    main()
