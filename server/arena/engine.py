"""Deterministic battle engine for CodeBots Arena."""

from __future__ import annotations

from dataclasses import dataclass, field

from codebots import Bot, State, validate_action


MAX_TURNS = 50
ARENA_MIN = -5
ARENA_MAX = 5

ATTACK_DAMAGE = 15
SPECIAL_DAMAGE = 30
HEAL_AMOUNT = 12
START_HEALTH = 100
START_ENERGY = 50
SPECIAL_COST = 30
SPECIAL_COOLDOWN = 3


@dataclass
class TurnEvent:
    """One event generated during a battle."""

    turn: int
    bot_a_action: str
    bot_b_action: str
    bot_a_health: int
    bot_b_health: int
    bot_a_position: int
    bot_b_position: int


@dataclass
class BattleResult:
    """Final result of a battle."""

    winner: str | None
    turns_played: int
    bot_a_name: str
    bot_b_name: str
    events: list[TurnEvent] = field(default_factory=list)

    def to_jsonl(self) -> str:
        """Return the battle events as JSONL."""
        import json

        return "\n".join(
            json.dumps(
                {
                    "turn": event.turn,
                    "bot_a_action": event.bot_a_action,
                    "bot_b_action": event.bot_b_action,
                    "bot_a_health": event.bot_a_health,
                    "bot_b_health": event.bot_b_health,
                    "bot_a_position": event.bot_a_position,
                    "bot_b_position": event.bot_b_position,
                }
            )
            for event in self.events
        )


class BattleEngine:
    """Runs a deterministic two-bot battle."""

    def __init__(
        self,
        bot_a: Bot,
        bot_b: Bot,
        max_turns: int = MAX_TURNS,
    ):
        self.bot_a = bot_a
        self.bot_b = bot_b
        self.max_turns = max(1, min(max_turns, MAX_TURNS))

    def _state(
        self,
        my_health: int,
        my_energy: int,
        my_position: int,
        my_cooldown: int,
        enemy_health: int,
        enemy_energy: int,
        enemy_position: int,
        turn: int,
        enemy_last_action: str | None,
    ) -> State:
        return State(
            my_health=my_health,
            my_energy=my_energy,
            my_position=my_position,
            my_special_cooldown=my_cooldown,
            enemy_health=enemy_health,
            enemy_energy=enemy_energy,
            enemy_position=enemy_position,
            enemy_distance=abs(my_position - enemy_position),
            turn_number=turn,
            max_turns=self.max_turns,
            enemy_last_action=enemy_last_action,
        )

    @staticmethod
    def _apply_damage(
        health: int,
        damage: int,
        defending: bool,
    ) -> int:
        if defending:
            damage = max(1, damage // 2)
        return max(0, health - damage)

    @staticmethod
    def _move(position: int, direction: int) -> int:
        return max(ARENA_MIN, min(ARENA_MAX, position + direction))

    def _apply_action(
        self,
        action: str,
        health: int,
        energy: int,
        position: int,
        cooldown: int,
        enemy_health: int,
        enemy_position: int,
        enemy_defending: bool,
    ) -> tuple[int, int, int, int, int]:
        """Apply one action.

        Returns:
            health, energy, position, cooldown, damage_to_enemy
        """
        damage = 0

        if action == "attack":
            if abs(position - enemy_position) <= 2:
                damage = ATTACK_DAMAGE

        elif action == "defend":
            pass

        elif action == "heal":
            health = min(START_HEALTH, health + HEAL_AMOUNT)
            energy = min(START_ENERGY, energy + 5)

        elif action == "move_left":
            position = self._move(position, -1)
            energy = min(START_ENERGY, energy + 2)

        elif action == "move_right":
            position = self._move(position, 1)
            energy = min(START_ENERGY, energy + 2)

        elif action == "special":
            if cooldown == 0 and energy >= SPECIAL_COST:
                damage = SPECIAL_DAMAGE
                energy -= SPECIAL_COST
                cooldown = SPECIAL_COOLDOWN

        elif action == "wait":
            energy = min(START_ENERGY, energy + 5)

        if damage:
            damage = max(1, damage // 2) if enemy_defending else damage

        return health, energy, position, cooldown, damage

    def run(self) -> BattleResult:
        """Run the complete battle."""
        health_a = START_HEALTH
        health_b = START_HEALTH

        energy_a = START_ENERGY
        energy_b = START_ENERGY

        position_a = -1
        position_b = 1

        cooldown_a = 0
        cooldown_b = 0

        last_a: str | None = None
        last_b: str | None = None

        events: list[TurnEvent] = []

        self.bot_a.on_init()
        self.bot_b.on_init()

        winner: str | None = None

        for turn in range(1, self.max_turns + 1):
            state_a = self._state(
                health_a,
                energy_a,
                position_a,
                cooldown_a,
                health_b,
                energy_b,
                position_b,
                turn,
                last_b,
            )

            state_b = self._state(
                health_b,
                energy_b,
                position_b,
                cooldown_b,
                health_a,
                energy_a,
                position_a,
                turn,
                last_a,
            )

            action_a = validate_action(self.bot_a.on_turn(state_a))
            action_b = validate_action(self.bot_b.on_turn(state_b))

            self.bot_a.moves_log.append(action_a)
            self.bot_b.moves_log.append(action_b)

            defending_a = action_a == "defend"
            defending_b = action_b == "defend"

            (
                health_a,
                energy_a,
                position_a,
                cooldown_a,
                damage_a,
            ) = self._apply_action(
                action_a,
                health_a,
                energy_a,
                position_a,
                cooldown_a,
                health_b,
                position_b,
                defending_b,
            )

            (
                health_b,
                energy_b,
                position_b,
                cooldown_b,
                damage_b,
            ) = self._apply_action(
                action_b,
                health_b,
                energy_b,
                position_b,
                cooldown_b,
                health_a,
                position_a,
                defending_a,
            )

            health_b = max(0, health_b - damage_a)
            health_a = max(0, health_a - damage_b)

            events.append(
                TurnEvent(
                    turn=turn,
                    bot_a_action=action_a,
                    bot_b_action=action_b,
                    bot_a_health=health_a,
                    bot_b_health=health_b,
                    bot_a_position=position_a,
                    bot_b_position=position_b,
                )
            )

            last_a = action_a
            last_b = action_b

            if health_a <= 0 and health_b <= 0:
                winner = None
                break
            if health_b <= 0:
                winner = "A"
                break
            if health_a <= 0:
                winner = "B"
                break

            if cooldown_a > 0:
                cooldown_a -= 1
            if cooldown_b > 0:
                cooldown_b -= 1

        return BattleResult(
            winner=winner,
            turns_played=len(events),
            bot_a_name=self.bot_a.name,
            bot_b_name=self.bot_b.name,
            events=events,
        )
