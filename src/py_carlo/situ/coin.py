from __future__ import annotations

from typing import List
import random

COIN_RESULTS = ['HEADS', 'TAILS']


def flip_coin() -> str:
    return random.choice(COIN_RESULTS)


def flip_n_coins(n: int) -> List[str]:
    return [flip_coin() for _ in range(n)]


def check_for_n_consecutive(
        flips: List[str],
        result: str,
        n: int) -> bool:
    """Checks for n consecutive instances of 'result' in 
    the list 'flips', returns True if they exist in that 
    sequence"""
    if (n > len(flips)) or (result not in flips):
        return False

    consecutive = 0
    for flip in flips:
        if flip == result:
            consecutive += 1
        else:
            consecutive = 0

        if consecutive >= n:
            return True

    else:
        return False
