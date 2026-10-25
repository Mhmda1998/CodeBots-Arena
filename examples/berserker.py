"""
Berserker Bot — chases the enemy down and never backs off.
Deals heavy damage but leaves itself wide open.
"""
from codebots import Bot, State


class BerserkerBot(Bot):
    name = "Rampage"
    color = "#FF6B00"
    author = "CodeBots Team"

    def on_init(self) -> None:
        self.chase_direction = "move_right"

    def on_turn(self, state: State) -> str:
        # Keep chasing: flip direction when we overshoot the enemy.
        if state.enemy_position > state.my_position:
            self.chase_direction = "move_right"
        elif state.enemy_position < state.my_position:
            self.chase_direction = "move_left"

        if state.enemy_distance <= 1:
            # In range: hit hard, never defend.
            if state.can_special() and state.enemy_health <= 60:
                return "special"
            return "attack"

        if state.my_health < 25 and state.turn_number % 3 == 0:
            return "heal"

        if state.enemy_distance == 2:
            return "attack"

        return self.chase_direction
