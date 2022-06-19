import pytest
from typing import List

import py_carlo.situ.coin as coin

import random

from collections import Counter

TOLERANCE = 0.05
NUM_FLIPS = 100

random.seed(1)

HEADS = coin.CoinResult.HEADS
TAILS = coin.CoinResult.TAILS


def test_flip_coin_distr() -> None:
    """Test that the distribution of flipping
    a coin is within the TOLERANCE of 50/50"""
    results = Counter([coin.flip_coin() for _ in range(NUM_FLIPS)])

    min_bounds = (NUM_FLIPS // 2) * (1-(TOLERANCE * 2))
    max_bounds = (NUM_FLIPS // 2) * (1+(TOLERANCE * 2))
    assert min_bounds <= results[HEADS] <= max_bounds


def test_n_consecutive_false_short_flips() -> None:
    """Test that check_for_n_consecutive always returns
    false for any sequence where the number of flips is
    below 'n'"""
    for num_flips in range(1, NUM_FLIPS + 1):
        assert coin.check_for_n_consecutive(
            flips=[HEADS] * num_flips,
            result=HEADS,
            n=num_flips-1)


@pytest.mark.parametrize(
    "flips,result,n,expected", [
        ([HEADS], HEADS, 1, True),
        ([HEADS], TAILS, 1, False),
        ([TAILS], HEADS, 1, False),
        ([TAILS], TAILS, 1, True),
        ([HEADS, HEADS, TAILS, HEADS], HEADS, 2, True),
        ([HEADS, HEADS, TAILS, HEADS], HEADS, 3, False),
        ([HEADS, TAILS, TAILS, HEADS], HEADS, 2, False),
        ([HEADS, TAILS, TAILS, HEADS], TAILS, 2, True)
    ]
)
def test_n_consecutive_assorted(
    flips: List[coin.CoinResult],
    result: coin.CoinResult,
    n: int,
    expected: bool
) -> None:
    """Checks assorted values for test_n_consecutive"""
    assert coin.check_for_n_consecutive(flips, result, n) == expected


def test_n_consecutive_true():
    """Exhaustively tests known true return values".

    Creates a sequence of consecutive values in the middle
    of the flips sequence, and checks if they all return True"""
    for num_consec in range(1, NUM_FLIPS + 1):
        to_pad = NUM_FLIPS - num_consec
        l_pad = to_pad // 2
        r_pad = to_pad - l_pad

        # check consecutive heads
        assert coin.check_for_n_consecutive(
            flips=[TAILS] * l_pad + [HEADS] * num_consec + [TAILS] * r_pad,
            result=HEADS,
            n=num_consec)

        # check consecutive tails
        assert coin.check_for_n_consecutive(
            flips=[HEADS] * l_pad + [TAILS] * num_consec + [HEADS] * r_pad,
            result=TAILS,
            n=num_consec)


def test_n_consecutive_false():
    """Exhaustively tests known false return values

    Creates sequences of n-1 length consecutive flips, separated
    by the other result, and checks that all return False"""
    for num_consec_to_check in range(NUM_FLIPS):
        sequence = ([HEADS] * (num_consec_to_check - 1)) + [TAILS]

        num_repeats = NUM_FLIPS // (num_consec_to_check + 1)
        r_padding = [TAILS] * (NUM_FLIPS % (num_consec_to_check + 1))

        assert not coin.check_for_n_consecutive(
            flips=(sequence * num_repeats) + r_padding,
            result=HEADS,
            n=num_consec_to_check
        )
