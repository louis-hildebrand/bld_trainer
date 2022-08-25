from colorama import Back as ANSI

from lib.rubiks_cube import Color, RubiksCube


class RubiksCubeDrawer:
    ANSI_START = {
        Color.WHITE: ANSI.WHITE,
        Color.GREEN: ANSI.GREEN,
        Color.RED: ANSI.RED,
        Color.BLUE: ANSI.BLUE,
        Color.ORANGE: ANSI.MAGENTA,
        Color.YELLOW: ANSI.YELLOW
    }
    ANSI_END = ANSI.RESET

    @staticmethod
    def _cell(color: Color) -> str:
        return RubiksCubeDrawer.ANSI_START[color] + "   " + RubiksCubeDrawer.ANSI_END

    @staticmethod
    def draw(rc: RubiksCube) -> str:
        sticker_colors = rc.sticker_colors()
        out = (
            "..........    +---------    +\n" +
            "..........    |^UBL^UB^UBR^ |\n" +
            "..........    |^UL ^U ^UR ^ |\n" +
            "..........    |^UFL^UF^UFR^ |\n" +
            "+---------    +---------    + ---------   +---------    +\n" +
            "|^LBU^LU^LFU^ |^FLU^FU^FRU^ |^RFU^RU^RBU^ |^BRU^BU^BLU^ |\n" +
            "|^LB ^L ^LF^  |^FL ^F ^FR^  |^RF ^R ^RB ^ |^BR ^B ^BL ^ |\n" +
            "|^LBD^LD^LDF^ |^FDL^FD^FDR^ |^RDF^RD^RBD^ |^BDR^BD^BDL^ |\n" +
            "+---------    +---------    +---------    +---------    +\n" +
            "..........    |^DFL^DF^DFR^ |\n" +
            "..........    |^DL ^D ^DR^  |\n" +
            "..........    |^DBL^DB^DBR^ |\n" +
            "..........    +---------    +"
        )
        out = out.replace(" ", "")
        out = out.replace(".", " ")
        for (sticker, color) in sticker_colors.items():
            out = out.replace("^" + str(sticker) + "^", "^" + RubiksCubeDrawer._cell(color) + "^")
        out = out.replace("^", "")
        return out
