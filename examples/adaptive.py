"""
Adaptive Bot — reads the enemy's pattern and counters it.
This is a smarter bot — uses simple state tracking.
"""
from codebots import Bot, State
from collections import Counter


class AdaptiveBot(Bot):
    name = "AdaptiveMind"
    color = "#33FF88"
    author = "CodeBots Team"

    def on_init(self) -> None:
        self.enemy_pattern: list[str] = []
        self.my_strategy = "balanced"

    def on_turn(self, state: State) -> str:
        if state.enemy_last_action:
            self.enemy_pattern.append(state.enemy_last_action)
            if len(self.enemy_pattern) > 5:
                self.enemy_pattern.pop(0)

        if state.can_special() and state.enemy_health < 50:
            return "special"

        if self.enemy_pattern:
            most_common = Counter(self.enemy_pattern).most_common(1)[0][0]
            if most_common == "attack" and state.enemy_distance <= 1:
                return "defend"
            if most_common == "heal" and state.enemy_distance <= 2:
                return "attack"

        if state.my_health < 30:
            return "heal"
        if state.enemy_distance <= 1:
            return "attack"
        return "move_forward"
