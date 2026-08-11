"""
Defensive Bot — heals, defends, only attacks when safe.
Hard to kill but slow to win.
"""
from codebots import Bot, State


class DefensiveBot(Bot):
    name = "Guardian"
    color = "#3388FF"
    author = "CodeBots Team"

    def on_turn(self, state: State) -> str:
        if state.my_health < 40:
            return "heal"
        if state.enemy_distance <= 1 and state.enemy_health < 30:
            return "attack"
        if state.enemy_distance <= 1:
            return "defend"
        if state.my_energy >= 30 and state.can_special():
            return "special"
        return "wait"
