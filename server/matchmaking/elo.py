"""ELO rating utilities for CodeBots Arena."""

from __future__ import annotations

import math


def expected_score(rating_a: float, rating_b: float) -> float:
    """Return the expected score of player A against player B."""
    return 1.0 / (1.0 + math.pow(10.0, (rating_b - rating_a) / 400.0))


def update_elo(
    rating_a: float,
    rating_b: float,
    score_a: float,
    k: float = 32,
) -> tuple[float, float]:
    """Update two ELO ratings.

    score_a:
        1.0 = A wins
        0.5 = draw
        0.0 = A loses
    """
    expected_a = expected_score(rating_a, rating_b)
    expected_b = 1.0 - expected_a
    score_b = 1.0 - score_a

    new_a = rating_a + k * (score_a - expected_a)
    new_b = rating_b + k * (score_b - expected_b)

    return new_a, new_b


def rank_label(rating: float) -> str:
    """Convert an ELO rating to its rank label."""
    if rating < 1000:
        return "Wood"
    if rating < 1200:
        return "Bronze"
    if rating < 1400:
        return "Silver"
    if rating < 1600:
        return "Gold"
    if rating < 1800:
        return "Platinum"
    if rating < 2000:
        return "Diamond"
    if rating < 2400:
        return "Master"
    return "Grandmaster"
