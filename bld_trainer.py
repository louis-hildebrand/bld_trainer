from lib.drawer import RubiksCubeDrawer
from lib.rubiks_cube import RubiksCube
from lib.scrambler import RubiksCubeScrambler
from lib.solver import M2Solver, Target


def _input_targets(msg: str) -> list[Target]:
    while True:
        raw_target_str = input(msg).upper().replace(" ", "")
        try:
            return [Target[t] for t in raw_target_str]
        except KeyError as ke:
            print(f"Invalid target {ke}. Please try again.\n")


def main():
    # Generate random scramble and print scramble sequence
    scramble = RubiksCubeScrambler.random_scramble()
    print(f"Scramble: {' '.join([str(m) for m in scramble])}")
    rc = RubiksCube().apply(scramble)
    print()
    print(RubiksCubeDrawer.draw(rc))
    print()
    # Input solution
    corner_targets = _input_targets(f"Corners:\n# ")
    edge_targets = _input_targets(f"Edges:\n# ")
    # Check solutions
    solved_cube = M2Solver.apply_solution(rc, edge_targets, corner_targets)
    print()
    print(RubiksCubeDrawer.draw(solved_cube))
    print()
    if solved_cube.is_solved():
        print(f"Memorization successful!")
    else:
        print(f"Memorization failed.")
    print()


if __name__ == "__main__":
    main()
