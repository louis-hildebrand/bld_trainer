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
    U = auto()
    F = auto()
    R = auto()
    B = auto()
    L = auto()
    D = auto()
    M = auto()
    E = auto()
    S = auto()

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
        return self.name


class Direction(Enum):
    CW = auto()
    CCW = auto()
    DOUBLE = auto()


class Move(Enum):
    U = [(Layer.U, Direction.CW)]
    U_PRIME = [(Layer.U, Direction.CCW)]
    U2 = [(Layer.U, Direction.DOUBLE)]
    F = [(Layer.F, Direction.CW)]
    F_PRIME = [(Layer.F, Direction.CCW)]
    F2 = [(Layer.F, Direction.DOUBLE)]
    R = [(Layer.R, Direction.CW)]
    R_PRIME = [(Layer.R, Direction.CCW)]
    R2 = [(Layer.R, Direction.DOUBLE)]
    B = [(Layer.B, Direction.CW)]
    B_PRIME = [(Layer.B, Direction.CCW)]
    B2 = [(Layer.B, Direction.DOUBLE)]
    L = [(Layer.L, Direction.CW)]
    L_PRIME = [(Layer.L, Direction.CCW)]
    L2 = [(Layer.L, Direction.DOUBLE)]
    D = [(Layer.D, Direction.CW)]
    D_PRIME = [(Layer.D, Direction.CCW)]
    D2 = [(Layer.D, Direction.DOUBLE)]
    M = [(Layer.M, Direction.CW)]
    M_PRIME = [(Layer.M, Direction.CCW)]
    M2 = [(Layer.M, Direction.DOUBLE)]
    E = [(Layer.E, Direction.CW)]
    E_PRIME = [(Layer.E, Direction.CCW)]
    E2 = [(Layer.E, Direction.DOUBLE)]
    S = [(Layer.S, Direction.CW)]
    S_PRIME = [(Layer.S, Direction.CCW)]
    S2 = [(Layer.S, Direction.DOUBLE)]
    X = [(Layer.R, Direction.CW), (Layer.M, Direction.CCW), (Layer.L, Direction.CCW)]
    X_PRIME = [(Layer.R, Direction.CCW), (Layer.M, Direction.CW), (Layer.L, Direction.CW)]
    X2 = [(Layer.R, Direction.DOUBLE), (Layer.M, Direction.DOUBLE), (Layer.L, Direction.DOUBLE)]
    Y = [(Layer.U, Direction.CW), (Layer.E, Direction.CCW), (Layer.D, Direction.CCW)]
    Y_PRIME = [(Layer.U, Direction.CCW), (Layer.E, Direction.CW), (Layer.D, Direction.CW)]
    Y2 = [(Layer.U, Direction.DOUBLE), (Layer.E, Direction.DOUBLE), (Layer.D, Direction.DOUBLE)]
    Z = [(Layer.F, Direction.CW), (Layer.S, Direction.CW), (Layer.B, Direction.CCW)]
    Z_PRIME = [(Layer.F, Direction.CCW), (Layer.S, Direction.CCW), (Layer.B, Direction.CW)]
    Z2 = [(Layer.F, Direction.DOUBLE), (Layer.S, Direction.DOUBLE), (Layer.B, Direction.DOUBLE)]

    def affected_layers(self: Move) -> set[Layer]:
        return {x[0] for x in self.value}

    def is_outer_turn(self: Move) -> bool:
        return len(self.value) == 1 and self.value[0][0] in {Layer.U, Layer.F, Layer.R, Layer.B, Layer.L, Layer.D}

    @staticmethod
    def _parse(move: str) -> Move:
        move = move.replace("'", "_PRIME")
        return Move[move]

    @staticmethod
    def parse(moves: str) -> list[Move]:
        return [Move._parse(m) for m in moves.replace("(", "").replace(")", "").split(" ")]

    def __str__(self: Move) -> str:
        if len(self.value) == 1:
            v: tuple[Layer, Direction] = self.value[0]
            return str(v[0]) + ("" if v[1] is Direction.CW else "'" if v[1] is Direction.CCW else "2")
        else:
            return self.name.replace("_PRIME", "'")


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

    @staticmethod
    def _get_cw_cycles(layer: Layer) -> tuple[list[list[CenterSticker]], list[list[CornerSticker]], list[list[EdgeSticker]]]:
        CE = CenterSticker
        CO = CornerSticker
        E = EdgeSticker
        match layer:
            case Layer.U:
                center_cycles = []
                corner_cycles = [
                    [CO.UBL, CO.UBR, CO.UFR, CO.UFL],
                    [CO.FLU, CO.LBU, CO.BRU, CO.RFU],
                    [CO.FRU, CO.LFU, CO.BLU, CO.RBU]
                ]
                edge_cycles = [[E.UB, E.UR, E.UF, E.UL], [E.FU, E.LU, E.BU, E.RU]]
            case Layer.F:
                center_cycles = []
                corner_cycles = [
                    [CO.UFR, CO.RDF, CO.DFL, CO.LFU],
                    [CO.UFL, CO.RFU, CO.DFR, CO.LDF],
                    [CO.FLU, CO.FRU, CO.FDR, CO.FDL]
                ]
                edge_cycles = [[E.UF, E.RF, E.DF, E.LF], [E.FU, E.FR, E.FD, E.FL]]
            case Layer.R:
                center_cycles = []
                corner_cycles = [
                    [CO.UBR, CO.BDR, CO.DFR, CO.FRU],
                    [CO.UFR, CO.BRU, CO.DBR, CO.FDR],
                    [CO.RFU, CO.RBU, CO.RBD, CO.RDF]
                ]
                edge_cycles = [[E.UR, E.BR, E.DR, E.FR], [E.RU, E.RB, E.RD, E.RF]]
            case Layer.B:
                center_cycles = []
                corner_cycles = [
                    [CO.UBL, CO.LBD, CO.DBR, CO.RBU],
                    [CO.UBR, CO.LBU, CO.DBL, CO.RBD],
                    [CO.BRU, CO.BLU, CO.BDL, CO.BDR]
                ]
                edge_cycles = [[E.UB, E.LB, E.DB, E.RB], [E.BU, E.BL, E.BD, E.BR]]
            case Layer.L:
                center_cycles = []
                corner_cycles = [
                    [CO.UBL, CO.FLU, CO.DFL, CO.BDL],
                    [CO.UFL, CO.FDL, CO.DBL, CO.BLU],
                    [CO.LBU, CO.LFU, CO.LDF, CO.LBD]
                ]
                edge_cycles = [[E.UL, E.FL, E.DL, E.BL], [E.LU, E.LF, E.LD, E.LB]]
            case Layer.D:
                center_cycles = []
                corner_cycles = [
                    [CO.FDR, CO.RBD, CO.BDL, CO.LDF],
                    [CO.FDL, CO.RDF, CO.BDR, CO.LBD],
                    [CO.DFL, CO.DFR, CO.DBR, CO.DBL]
                ]
                edge_cycles = [[E.FD, E.RD, E.BD, E.LD], [E.DF, E.DR, E.DB, E.DL]]
            case Layer.M:
                center_cycles = [[CE.U, CE.F, CE.D, CE.B]]
                corner_cycles = []
                edge_cycles = [[E.UB, E.FU, E.DF, E.BD], [E.UF, E.FD, E.DB, E.BU]]
            case Layer.E:
                center_cycles = [[CE.F, CE.R, CE.B, CE.L]]
                corner_cycles = []
                edge_cycles = [[E.FR, E.RB, E.BL, E.LF], [E.FL, E.RF, E.BR, E.LB]]
            case Layer.S:
                center_cycles = [[CE.U, CE.R, CE.D, CE.L]]
                corner_cycles = []
                edge_cycles = [[E.UR, E.RD, E.DL, E.LU], [E.UL, E.RU, E.DR, E.LD]]
            case _:
                raise ValueError(f"Invalid layer '{layer}'.")
        return (center_cycles, corner_cycles, edge_cycles)

    @staticmethod
    def _get_cycles(m: Move) -> tuple[list[list[CenterSticker]], list[list[CornerSticker]], list[list[EdgeSticker]]]:
        center_cycles: list[list[CenterSticker]] = []
        corner_cycles: list[list[CornerSticker]] = []
        edge_cycles: list[list[EdgeSticker]] = []
        for (layer, direction) in m.value:
            # Get the cycles for the clockwise turn of the layer
            (cec, coc, ec) = RubiksCube._get_cw_cycles(layer)
            # Adjust the cycles for double or counterclockwise moves
            match direction:
                case Direction.CW:
                    pass
                case Direction.CCW:
                    cec = [c[::-1] for c in cec]
                    coc = [c[::-1] for c in coc]
                    ec = [c[::-1] for c in ec]
                case Direction.DOUBLE:
                    # Assumes the cycles all have a length of 4
                    def repeat_cycles(cycles: list[list[T]]) -> list[list[T]]:
                        return flatten([[[c[0], c[2]], [c[1], c[3]]] for c in cycles])
                    cec = repeat_cycles(cec)
                    coc = repeat_cycles(coc)
                    ec = repeat_cycles(ec)
                case _:
                    raise ValueError(f"Invalid direction '{direction}'.")
            center_cycles += cec
            corner_cycles += coc
            edge_cycles += ec
        return (center_cycles, corner_cycles, edge_cycles)

    def _apply_single(self: RubiksCube, m: Move) -> RubiksCube:
        (center_cycles, corner_cycles, edge_cycles) = RubiksCube._get_cycles(m)
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

    def orient(self: RubiksCube, top_color: Color = Color.WHITE, front_color: Color = Color.GREEN) -> RubiksCube:
        # Find sticker matching the desired top color
        top_index = self._centers.index(top_color)
        match top_index:
            case CenterSticker.U.value:
                rc = self
            case CenterSticker.F.value:
                rc = self.apply([Move.X])
            case CenterSticker.R.value:
                rc = self.apply([Move.Z_PRIME])
            case CenterSticker.B.value:
                rc = self.apply([Move.X_PRIME])
            case CenterSticker.L.value:
                rc = self.apply([Move.Z])
            case CenterSticker.D.value:
                rc = self.apply([Move.Z2])
            case _:
                raise ValueError(f"Unable to find sticker with color '{top_color}' to move to top.")
        # Find sticker matching the desired front color
        front_index = rc._centers.index(front_color)
        match front_index:
            case CenterSticker.U.value:
                raise ValueError(
                    f"Attempt to place the same color on top and on front ('{top_color}' and '{front_color}')."
                )
            case CenterSticker.F.value:
                pass
            case CenterSticker.R.value:
                rc = self.apply([Move.Y])
            case CenterSticker.B.value:
                rc = self.apply([Move.Y2])
            case CenterSticker.L.value:
                rc = self.apply([Move.Y_PRIME])
            case CenterSticker.D.value:
                raise ValueError(
                    f"Attempt to place opposite colors on top and on front ('{top_color}' and '{front_color}')."
                )
            case _:
                raise ValueError(f"Unable to find sticker with color '{front_color}' to move to front.")
        return rc

    def __eq__(self: RubiksCube, o: object) -> bool:
        """
        Checks whether two Rubik's Cubes are equal, *including overall orientation*.
        """
        return (isinstance(o, RubiksCube)
            and self._centers == o._centers
            and self._corners == o._corners
            and self._edges == o._edges)

    def is_solved(self: RubiksCube) -> bool:
        return self.orient() == RubiksCube()
