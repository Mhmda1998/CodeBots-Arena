"""
Tests for the battle engine.
Run with: pytest tests/
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "sdk"))
sys.path.insert(0, str(Path(__file__).parent.parent / "server"))

import pytest

from arena.engine import BattleEngine
from codebots import Bot, State


class AlwaysAttack(Bot):
    name = "Attacker"
    color = "#FF0000"
    author = "test"

    def on_turn(self, state: State) -> str:
        return "attack"


class AlwaysHeal(Bot):
    name = "Healer"
    color = "#00FF00"
    author = "test"

    def on_turn(self, state: State) -> str:
        return "heal"


class AlwaysWait(Bot):
    name = "Waiter"
    color = "#0000FF"
    author = "test"

    def on_turn(self, state: State) -> str:
        return "wait"


def test_battle_runs():
    engine = BattleEngine(AlwaysAttack(), AlwaysHeal(), max_turns=20)
    result = engine.run()
    assert result.turns_played > 0
    assert result.bot_a_name == "Attacker"
    assert result.bot_b_name == "Healer"


def test_wait_bot_eventually_loses():
    engine = BattleEngine(AlwaysAttack(), AlwaysWait(), max_turns=10)
    result = engine.run()
    # attacker should kill waiter
    assert result.winner in ("A", None)


def test_action_validation():
    from codebots import validate_action
    assert validate_action("ATTACK") == "attack"
    assert validate_action("invalid") == "wait"
    assert validate_action(None) == "wait"  # type: ignore
    assert validate_action(123) == "wait"  # type: ignore


def test_state_defaults():
    s = State()
    assert s.my_health == 100
    assert s.max_turns == 50
    assert s.hp_percent() == 1.0
    assert not s.can_special()
