try:
    import colorama
except ImportError:
    colorama = None

from lib.rubiks_cube import Color, RubiksCube


class RubiksCubeDrawer:
    @staticmethod
    def _ansi_start(color: Color) -> str:
        if not colorama:
            return ""
        else:
            match color:
                case Color.WHITE:
                    return colorama.Back.WHITE + colorama.Fore.BLACK
                case Color.GREEN:
                    return colorama.Back.GREEN + colorama.Fore.BLACK
                case Color.RED:
                    return colorama.Back.RED
                case Color.BLUE:
                    return colorama.Back.BLUE
                case Color.ORANGE:
                    return colorama.Back.MAGENTA
                case Color.YELLOW:
                    return colorama.Back.YELLOW + colorama.Fore.BLACK

    ANSI_END = colorama.Back.RESET + colorama.Fore.RESET if colorama else ""

    @staticmethod
    def _cell(color: Color) -> str:
        letter = color.name[0]
        return RubiksCubeDrawer._ansi_start(color) + f" {letter} " + RubiksCubeDrawer.ANSI_END

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
