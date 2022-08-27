from typing import TypeVar
import os


T = TypeVar("T")


def flatten(x: list[list[T]]) -> list[T]:
    out: list[T] = []
    for sublist in x:
        out += sublist
    return out


def cycle(x: list[T], idx: list[int]) -> list[T]:
    """
    Example: cycle(['A', 'B', 'C', 'D'], [0, 3, 1]) returns ['B', 'D', 'C', 'A']
    """
    out = [e for e in x]
    n = len(idx)
    temp = out[idx[-1]]
    for i in range(n - 1, 0, -1):
        out[idx[i]] = out[idx[i - 1]]
    out[idx[0]] = temp
    return out


def clear_screen() -> None:
    os.system("cls||clear")
