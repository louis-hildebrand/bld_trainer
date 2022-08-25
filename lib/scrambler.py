import random

from lib.rubiks_cube import Layer, Move


class RubiksCubeScrambler:
    @staticmethod
    def random_scramble() -> list[Move]:
        scramble: list[Move] = []
        allowed_moves = [e for e in Move if e.value[0] in {Layer.U, Layer.F, Layer.R, Layer.B, Layer.L, Layer.D}]
        weights = [1 for _ in allowed_moves]
        for _ in range(20):
            m = random.choices(allowed_moves, weights=weights, k=1)[0]
            scramble.append(m)
            parallel_layers = m.value[0].parallel()
            weights = [0 if e.value[0] in parallel_layers else 1 for e in allowed_moves]
        return scramble
