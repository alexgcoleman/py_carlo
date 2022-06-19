import pytest
from typing import List

import py_carlo.situ.coin as coin

import random

from collections import Counter

TOLERANCE = 0.05
NUM_FLIPS = 100

random.seed(1)


def test_flip_coin_distr() -> None:
    """Test that the distribution of flipping
    a coin is within the TOLERANCE of 50/50"""
    results = Counter([coin.flip_coin() for _ in range(NUM_FLIPS)])

    min_bounds = (NUM_FLIPS // 2) * (1-(TOLERANCE * 2))
    max_bounds = (NUM_FLIPS // 2) * (1+(TOLERANCE * 2))
    assert min_bounds <= results['HEADS'] <= max_bounds


def test_n_consecutive_false_short_flips() -> None:
    """Test that check_for_n_consecutive always returns
    false for any sequence where the number of flips is
    below 'n'"""
    for num_flips in range(1, NUM_FLIPS + 1):
        assert coin.check_for_n_consecutive(
            flips=["HEADS"] * num_flips,
            result='HEADS',
            n=num_flips-1)
