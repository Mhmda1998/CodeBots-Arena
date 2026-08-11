"""
Aggressive Bot — always attacks, never defends.
Good for testing the engine, but weak against smart opponents.
"""
from codebots import Bot, State


class AggressiveBot(Bot):
    name = "Berserker"
    color = "#FF3333"
    author = "CodeBots Team"

    def on_init(self) -> None:
        self.opening_move = "move_forward"

    def on_turn(self, state: State) -> str:
        if state.turn_number == 0:
            return self.opening_move
        if state.can_special():
            return "special"
        if state.enemy_distance <= 1:
            return "attack"
        if state.my_energy < 10:
            return "wait"
        return "move_forward"
