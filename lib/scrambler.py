from typing import Callable
import random

from lib.rubiks_cube import Layer, Move


class RubiksCubeScrambler:
    @staticmethod
    def random_scramble() -> list[Move]:
        scramble: list[Move] = []
        allowed_moves = [m for m in Move if m.is_outer_turn()]
        recent_layers: set[Layer] = set()
        # Get the one layer affected by the given move
        # Since only outer turns are allowed, there will be exactly one affected layer
        layer: Callable[[Move], Layer] = lambda m: next(iter(m.affected_layers()))
        for _ in range(20):
            weights = [0 if layer(m) in recent_layers else 1 for m in allowed_moves]
            m = random.choices(allowed_moves, weights=weights, k=1)[0]
            scramble.append(m)
            # If this move is parallel to the previous one, the previous layer is still recently affected
            if len(recent_layers) == 0 or layer(m) not in next(iter(recent_layers)).parallel():
                recent_layers = {layer(m)}
            else:
                recent_layers.add(layer(m))
        return scramble
