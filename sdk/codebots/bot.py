"""
CodeBots Arena - Bot SDK
Base classes for writing your battle bot.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class State:
    """
    The full state of the arena, passed to your bot each turn.
    Read these fields to decide your next action.
    """
    # Self stats
    my_health: int = 100
    my_energy: int = 0
    my_position: int = 0  # -5 .. +5 on a horizontal axis
    my_special_cooldown: int = 0  # turns until special is ready

    # Enemy stats
    enemy_health: int = 100
    enemy_energy: int = 50
    enemy_position: int = 0

    # Derived
    enemy_distance: int = 0  # absolute distance between bots
    turn_number: int = 0
    max_turns: int = 50

    # Last enemy action (for prediction)
    enemy_last_action: str | None = None

    def hp_percent(self) -> float:
        return self.my_health / 100.0

    def can_special(self) -> bool:
        return self.my_special_cooldown == 0 and self.my_energy >= 30


class Bot(ABC):
    """
    Base class for all CodeBots.
    Inherit from this and implement on_turn().
    """
    name: str = "Anonymous"
    color: str = "#888888"
    author: str = "unknown"

    def __init__(self):
        self.moves_log: list[str] = []

    def on_init(self) -> None:
        """Optional: called once before the match starts."""
        pass

    @abstractmethod
    def on_turn(self, state: State) -> str:
        """
        Required: called every turn.
        Return one of: 'attack', 'defend', 'heal', 'move_left',
        'move_right', 'special', 'wait'.
        """
        raise NotImplementedError


# Allowed actions
ACTIONS = {"attack", "defend", "heal", "move_left", "move_right", "special", "wait"}


def validate_action(action: str) -> str:
    """Sanitize and validate the action returned by a bot."""
    if not isinstance(action, str):
        return "wait"
    action = action.strip().lower()
    return action if action in ACTIONS else "wait"
