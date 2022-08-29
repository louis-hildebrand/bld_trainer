from __future__ import annotations
from enum import Enum, auto

from lib.rubiks_cube import Move, RubiksCube


class Target(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()
    H = auto()
    I = auto()
    J = auto()
    K = auto()
    L = auto()
    M = auto()
    N = auto()
    O = auto()
    P = auto()
    Q = auto()
    R = auto()
    S = auto()
    T = auto()
    U = auto()
    V = auto()
    W = auto()
    X = auto()

    def flip(self: Target) -> Target:
        """
        Actual target in case this target appears as the second in its pair
        """
        match self:
            case Target.C:
                return Target.W
            case Target.E:
                return Target.O
            case Target.O:
                return Target.E
            case Target.W:
                return Target.C
            case _:
                return self

    def __str__(self: Target) -> str:
        return self.name


class M2Solver:
    _EDGE_ALGORITHMS = {
        Target.A: Move.parse("M2"),
        Target.B: Move.parse("(R U R' U') M2 (U R U' R')"),
        Target.C: Move.parse("U2 M' U2 M'"),
        Target.D: Move.parse("(L' U' L U) M2 (U' L' U L)"),
        Target.E: Move.parse("D M' U R2 U' M U R2 U' D' M2"),
        Target.F: Move.parse("(U R U') M2 (U R' U')"),
        Target.H: Move.parse("(U' L' U) M2 (U' L U)"),
        Target.I: Move.parse("(B' R B) M2 (B' R' B)"),
        Target.J: Move.parse("(R' B' R B) M2 (B' R' B R)"),
        Target.K: Move.parse("(B' R' B) M2 (B' R B)"),
        Target.L: Move.parse("(B' R2 B) M2 (B' R2 B)"),
        Target.M: Move.parse("(B' R B) (U R2 U') M2 (U R2 U') (B' R' B)"),
        Target.N: Move.parse("(U' L U) M2 (U' L' U)"),
        Target.O: Move.parse("M2 D U R2 U' M' U R2 U' M D'"),
        Target.P: Move.parse("(U R' U') M2 (U R U')"),
        Target.Q: Move.parse("(B L' B') M2 (B L B')"),
        Target.R: Move.parse("(B L2 B') M2 (B L2 B')"),
        Target.S: Move.parse("(B L B') M2 (B L' B')"),
        Target.T: Move.parse("(L B L' B') M2 (B L B' L')"),
        Target.V: Move.parse("(U R2 U') M2 (U R2 U')"),
        Target.W: Move.parse("M U2 M U2"),
        Target.X: Move.parse("(U' L2 U) M2 (U' L2 U)"),
    }
    _PARITY_ALGORITHM = Move.parse("(D' L2 D) M2 (D' L2 D)")
    _L_ALG = "R U' R' U' R U R' F' R U R' U' R' F R"
    _CORNER_ALGORITHMS = {
        Target.B: Move.parse(f"(R D') ({_L_ALG}) (D R')"),
        Target.C: Move.parse(f"F ({_L_ALG}) F'"),
        Target.D: Move.parse(f"(F2 D' F') ({_L_ALG}) (F D F2)"),
        Target.E: Move.parse(f"(F' D) ({_L_ALG}) (D' F)"),
        Target.F: Move.parse(f"(F2 D) ({_L_ALG}) (D' F2)"),
        Target.G: Move.parse(f"(F D) ({_L_ALG}) (D' F')"),
        Target.H: Move.parse(f"D ({_L_ALG}) D'"),
        Target.I: Move.parse(f"R' ({_L_ALG}) R"),
        Target.J: Move.parse(f"R2 ({_L_ALG}) R2"),
        Target.K: Move.parse(f"R ({_L_ALG}) R'"),
        Target.L: Move.parse(_L_ALG),
        Target.M: Move.parse(f"(R' F) ({_L_ALG}) (F' R)"),
        Target.O: Move.parse(f"(D' R) ({_L_ALG}) (R' D)"),
        Target.P: Move.parse(f"D' ({_L_ALG}) D"),
        Target.R: Move.parse(f"F2 ({_L_ALG}) F2"),
        Target.S: Move.parse(f"(D2 R) ({_L_ALG}) (R' D2)"),
        Target.T: Move.parse(f"D2 ({_L_ALG}) D2"),
        Target.U: Move.parse(f"F' ({_L_ALG}) F"),
        Target.V: Move.parse(f"(R' D') ({_L_ALG}) (D R)"),
        Target.W: Move.parse(f"(R2 F) ({_L_ALG}) (F' R2)"),
        Target.X: Move.parse(f"(D F') ({_L_ALG}) (F D')"),
    }

    @staticmethod
    def apply_solution(rc: RubiksCube, edge_targets: list[Target], corner_targets: list[Target]) -> RubiksCube:
        alg: list[Move] = []
        # Edges
        for (i, target) in enumerate(edge_targets):
            if i % 2 == 1:
                target = target.flip()
            alg += M2Solver._EDGE_ALGORITHMS[target]
        # Parity
        if len(edge_targets) % 2 == 1:
            alg += M2Solver._PARITY_ALGORITHM
        # Corners
        for target in corner_targets:
            alg += M2Solver._CORNER_ALGORITHMS[target]
        return rc.apply(alg)
