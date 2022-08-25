from __future__ import annotations
from enum import auto, Enum
from typing import TypeVar


from lib.utils import flatten, cycle


T = TypeVar("T")


class Color(Enum):
    WHITE = auto()
    GREEN = auto()
    RED = auto()
    BLUE = auto()
    ORANGE = auto()
    YELLOW = auto()


class Layer(Enum):
    U = "U"
    F = "F"
    R = "R"
    B = "B"
    L = "L"
    D = "D"
    M = "M"
    E = "E"
    S = "S"

    def parallel(self: Layer) -> set[Layer]:
        match self:
            case Layer.U | Layer.E | Layer.D:
                return {Layer.U, Layer.E, Layer.D}
            case Layer.F | Layer.S | Layer.B:
                return {Layer.F, Layer.S, Layer.B}
            case Layer.R | Layer.M | Layer.L:
                return {Layer.R, Layer.M, Layer.L}
            case _:
                raise ValueError(f"Invalid layer '{self}'.")

    def __str__(self: Layer) -> str:
        return self.value


class Move(Enum):
    # (layer, double, prime)
    U = (Layer.U, False, False)
    U_PRIME = (Layer.U, False, True)
    U2 = (Layer.U, True, False)
    F = (Layer.F, False, False)
    F_PRIME = (Layer.F, False, True)
    F2 = (Layer.F, True, False)
    R = (Layer.R, False, False)
    R_PRIME = (Layer.R, False, True)
    R2 = (Layer.R, True, False)
    B = (Layer.B, False, False)
    B_PRIME = (Layer.B, False, True)
    B2 = (Layer.B, True, False)
    L = (Layer.L, False, False)
    L_PRIME = (Layer.L, False, True)
    L2 = (Layer.L, True, False)
    D = (Layer.D, False, False)
    D_PRIME = (Layer.D, False, True)
    D2 = (Layer.D, True, False)
    M = (Layer.M, False, False)
    M_PRIME = (Layer.M, False, True)
    M2 = (Layer.M, True, False)
    E = (Layer.E, False, False)
    E_PRIME = (Layer.E, False, True)
    E2 = (Layer.E, True, False)
    S = (Layer.S, False, False)
    S_PRIME = (Layer.S, False, True)
    S2 = (Layer.S, True, False)

    @staticmethod
    def _parse(move: str) -> Move:
        move = move.replace("'", "_PRIME")
        return Move[move]

    @staticmethod
    def parse(moves: str) -> list[Move]:
        return [Move._parse(m) for m in moves.replace("(", "").replace(")", "").split(" ")]

    def __str__(self: Move) -> str:
        val = self.value
        return str(val[0]) + ("2" if val[1] else "") + ("'" if val[2] else "")


class Sticker(Enum):
    def __str__(self: Sticker) -> str:
        return self.name

    def __repr__(self: Sticker) -> str:
        return self.name


class CenterSticker(Sticker):
    U = 0
    F = 1
    R = 2
    B = 3
    L = 4
    D = 5


class CornerSticker(Sticker):
    UBL = 0
    UBR = 1
    UFR = 2
    UFL = 3
    FLU = 4
    FRU = 5
    FDR = 6
    FDL = 7
    RFU = 8
    RBU = 9
    RBD = 10
    RDF = 11
    BRU = 12
    BLU = 13
    BDL = 14
    BDR = 15
    LBU = 16
    LFU = 17
    LDF = 18
    LBD = 19
    DFL = 20
    DFR = 21
    DBR = 22
    DBL = 23


class EdgeSticker(Sticker):
    UB = 0
    UR = 1
    UF = 2
    UL = 3
    FU = 4
    FR = 5
    FD = 6
    FL = 7
    RU = 8
    RB = 9
    RD = 10
    RF = 11
    BU = 12
    BL = 13
    BD = 14
    BR = 15
    LU = 16
    LF = 17
    LD = 18
    LB = 19
    DF = 20
    DR = 21
    DB = 22
    DL = 23


class RubiksCube:
    @staticmethod
    def _initial_stickers() -> list[Color]:
        centers = [Color.WHITE, Color.GREEN, Color.RED, Color.BLUE, Color.ORANGE, Color.YELLOW]
        return flatten([[c] * 4 for c in centers])

    def __init__(
        self: RubiksCube,
        centers: list[Color] = [Color.WHITE, Color.GREEN, Color.RED, Color.BLUE, Color.ORANGE, Color.YELLOW],
        corners: list[Color] = _initial_stickers(),
        edges: list[Color] = _initial_stickers()
    ) -> None:
        """
        By default, initializes a solved Rubik's Cube with green front and white top.
        """
        self._centers = centers
        self._corners = corners
        self._edges = edges

    def _apply_single(self: RubiksCube, m: Move) -> RubiksCube:
        CE = CenterSticker
        CO = CornerSticker
        E = EdgeSticker
        # Get the corner and edge cycles for the clockwise 90 degree turn of the appropriate layer
        center_cycles: list[list[CenterSticker]] = []
        corner_cycles: list[list[CornerSticker]] = []
        edge_cycles: list[list[EdgeSticker]] = []
        match m.value:
            case (Layer.U, double, prime):
                corner_cycles = [
                    [CO.UBL, CO.UBR, CO.UFR, CO.UFL],
                    [CO.FLU, CO.LBU, CO.BRU, CO.RFU],
                    [CO.FRU, CO.LFU, CO.BLU, CO.RBU]
                ]
                edge_cycles = [
                    [E.UB, E.UR, E.UF, E.UL],
                    [E.FU, E.LU, E.BU, E.RU]
                ]
            case (Layer.F, double, prime):
                corner_cycles = [
                    [CO.UFR, CO.RDF, CO.DFL, CO.LFU],
                    [CO.UFL, CO.RFU, CO.DFR, CO.LDF],
                    [CO.FLU, CO.FRU, CO.FDR, CO.FDL]
                ]
                edge_cycles = [
                    [E.UF, E.RF, E.DF, E.LF],
                    [E.FU, E.FR, E.FD, E.FL]
                ]
            case (Layer.R, double, prime):
                corner_cycles = [
                    [CO.UBR, CO.BDR, CO.DFR, CO.FRU],
                    [CO.UFR, CO.BRU, CO.DBR, CO.FDR],
                    [CO.RFU, CO.RBU, CO.RBD, CO.RDF]
                ]
                edge_cycles = [
                    [E.UR, E.BR, E.DR, E.FR],
                    [E.RU, E.RB, E.RD, E.RF]
                ]
            case (Layer.B, double, prime):
                corner_cycles = [
                    [CO.UBL, CO.LBD, CO.DBR, CO.RBU],
                    [CO.UBR, CO.LBU, CO.DBL, CO.RBD],
                    [CO.BRU, CO.BLU, CO.BDL, CO.BDR]
                ]
                edge_cycles = [
                    [E.UB, E.LB, E.DB, E.RB],
                    [E.BU, E.BL, E.BD, E.BR]
                ]
            case (Layer.L, double, prime):
                corner_cycles = [
                    [CO.UBL, CO.FLU, CO.DFL, CO.BDL],
                    [CO.UFL, CO.FDL, CO.DBL, CO.BLU],
                    [CO.LBU, CO.LFU, CO.LDF, CO.LBD]
                ]
                edge_cycles = [
                    [E.UL, E.FL, E.DL, E.BL],
                    [E.LU, E.LF, E.LD, E.LB]
                ]
            case (Layer.D, double, prime):
                corner_cycles = [
                    [CO.FDR, CO.RBD, CO.BDL, CO.LDF],
                    [CO.FDL, CO.RDF, CO.BDR, CO.LBD],
                    [CO.DFL, CO.DFR, CO.DBR, CO.DBL]
                ]
                edge_cycles = [
                    [E.FD, E.RD, E.BD, E.LD],
                    [E.DF, E.DR, E.DB, E.DL]
                ]
            case (Layer.M, double, prime):
                center_cycles = [[CE.U, CE.F, CE.D, CE.B]]
                edge_cycles = [[E.UB, E.FU, E.DF, E.BD], [E.UF, E.FD, E.DB, E.BU]]
            case (Layer.E, double, prime):
                center_cycles = [[CE.F, CE.R, CE.B, CE.L]]
                edge_cycles = [[E.FR, E.RB, E.BL, E.LF], [E.FL, E.RF, E.BR, E.LB]]
            case (Layer.S, double, prime):
                center_cycles = [[CE.U, CE.R, CE.D, CE.L]]
                edge_cycles = [[E.UR, E.RD, E.DL, E.LU], [E.UL, E.RU, E.DR, E.LD]]
            case _:
                raise ValueError(f"Invalid move '{m}'.")
        # Adjust the cycles for double or counterclockwise moves
        if double:
            def repeat_cycles(cycles: list[list[T]]) -> list[list[T]]:
                return flatten([[[c[0], c[2]], [c[1], c[3]]] for c in cycles])
            center_cycles = repeat_cycles(center_cycles)
            corner_cycles = repeat_cycles(corner_cycles)
            edge_cycles = repeat_cycles(edge_cycles)
        elif prime:
            center_cycles = [cc[::-1] for cc in center_cycles]
            corner_cycles = [cc[::-1] for cc in corner_cycles]
            edge_cycles = [ec[::-1] for ec in edge_cycles]
        # Apply the cycles
        def apply_cycles(stickers: list[Color], cycles: list[list[int]]) -> list[Color]:
            for c in cycles:
                stickers = cycle(stickers, c)
            return stickers
        centers = apply_cycles(self._centers, [[s.value for s in cec] for cec in center_cycles])
        corners = apply_cycles(self._corners, [[s.value for s in coc] for coc in corner_cycles])
        edges = apply_cycles(self._edges, [[s.value for s in ec] for ec in edge_cycles])
        return RubiksCube(centers, corners, edges)

    def apply(self: RubiksCube, moves: list[Move]) -> RubiksCube:
        rc = self
        for m in moves:
            rc = rc._apply_single(m)
        return rc

    def sticker_colors(self: RubiksCube) -> dict[Sticker, Color]:
        out: dict[Sticker, Color] = {}
        for center in CenterSticker:
            out[center] = self._centers[center.value]
        for corner in CornerSticker:
            out[corner] = self._corners[corner.value]
        for edge in EdgeSticker:
            out[edge] = self._edges[edge.value]
        return out

    def __eq__(self: RubiksCube, o: object) -> bool:
        # TODO: Account for rotations
        return (isinstance(o, RubiksCube)
            and self._centers == o._centers
            and self._corners == o._corners
            and self._edges == o._edges)

    def is_solved(self: RubiksCube) -> bool:
        return self == RubiksCube()
