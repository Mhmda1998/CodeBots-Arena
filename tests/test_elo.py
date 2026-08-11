"""Tests for ELO matchmaking."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "server"))

from matchmaking.elo import expected_score, update_elo, rank_label


def test_expected_score_equal():
    assert expected_score(1200, 1200) == pytest.approx(0.5)


def test_update_elo_win():
    new_a, new_b = update_elo(1200, 1200, 1.0, k=32)
    assert new_a > 1200
    assert new_b < 1200


def test_update_elo_loss():
    new_a, new_b = update_elo(1200, 1200, 0.0, k=32)
    assert new_a < 1200
    assert new_b > 1200


def test_update_elo_draw():
    new_a, new_b = update_elo(1200, 1200, 0.5, k=32)
    assert new_a == pytest.approx(1200, abs=0.01)
    assert new_b == pytest.approx(1200, abs=0.01)


def test_rank_labels():
    assert rank_label(900) == "Wood"
    assert rank_label(1100) == "Bronze"
    assert rank_label(1300) == "Silver"
    assert rank_label(1500) == "Gold"
    assert rank_label(1700) == "Platinum"
    assert rank_label(1900) == "Diamond"
    assert rank_label(2100) == "Master"
    assert rank_label(2500) == "Grandmaster"


import pytest
