"""
Tactician Bot — controls range and energy instead of rushing in.
Keeps a comfortable distance, strikes when the special is worth it.
"""
from codebots import Bot, State


class TacticianBot(Bot):
    name = "Strategist"
    color = "#9B59FF"
    author = "CodeBots Team"

    # Preferred distance from the enemy.
    IDEAL_RANGE = 2

    def on_init(self) -> None:
        self.energy_saved = False

    def on_turn(self, state: State) -> str:
        distance = state.enemy_distance

        # Too close: create space or block the hit.
        if distance <= 1:
            if state.enemy_last_action == "attack":
                return "defend"
            if state.my_health < 45:
                return "heal"
            if state.can_special():
                return "special"
            if state.enemy_position > state.my_position:
                return "move_left"
            return "move_right"

        # At range: punish a wounded enemy with the special.
        if state.can_special() and state.enemy_health <= 55:
            return "special"

        # Too far: close the gap to the ideal range.
        if distance > self.IDEAL_RANGE + 1:
            if state.enemy_position > state.my_position:
                return "move_right"
            return "move_left"

        # In the ideal range: poke occasionally, otherwise recover energy.
        if distance == self.IDEAL_RANGE and state.turn_number % 4 == 0:
            return "attack"
        if state.my_energy < 30:
            return "wait"
        if state.enemy_health < 35:
            return "attack"
        return "wait"
