# CodeBots Arena — Bot API

Complete reference for writing a bot that runs inside the arena.

## Minimal bot

```python
from codebots import Bot, State


class MyBot(Bot):
    name = "MyBot"
    color = "#3388FF"
    author = "you"

    def on_turn(self, state: State) -> str:
        return "attack"
```

Your class must inherit from `codebots.Bot` and implement `on_turn(state)`.

## The `State` object

`on_turn` receives a frozen snapshot of the arena:

| Field | Type | Meaning |
|---|---|---|
| `my_health` | `int` | Your health, 0–100 |
| `my_energy` | `int` | Your energy, 0–50 |
| `my_position` | `int` | Your position on the axis, -5 … +5 |
| `my_special_cooldown` | `int` | Turns until `special` is ready again |
| `enemy_health` | `int` | Enemy health, 0–100 |
| `enemy_energy` | `int` | Enemy energy, 0–50 |
| `enemy_position` | `int` | Enemy position on the axis |
| `enemy_distance` | `int` | Absolute distance between you |
| `turn_number` | `int` | Current turn, starts at 1 |
| `max_turns` | `int` | Maximum turns in the match (50) |
| `enemy_last_action` | `str \| None` | Enemy's previous action |

Helper methods:

- `state.hp_percent()` — your health as a 0.0–1.0 fraction.
- `state.can_special()` — `True` when the special is off cooldown **and** you have at least 30 energy.

## Actions

Return exactly one string per turn:

| Action | Effect |
|---|---|
| `attack` | 15 damage if the enemy is within 2 tiles |
| `special` | 30 damage, costs 30 energy, 3-turn cooldown |
| `defend` | Incoming damage is halved (minimum 1) |
| `heal` | Restore 12 health (max 100) and gain 5 energy |
| `move_left` | Step one tile left, gain 2 energy |
| `move_right` | Step one tile right, gain 2 energy |
| `wait` | Gain 5 energy |

Any unknown or invalid action is sanitised to `wait`, so a typo never crashes a match.

## Arena rules

- Start: 100 health, 50 energy, positions -1 and +1.
- Attack range: 2 tiles.
- The match ends when a bot reaches 0 health, or after `max_turns` (default 50) — the bot with more health wins; a draw is possible.

## Running locally

```bash
pip install -e sdk
python -m pytest tests -q
```

To run your own bot against an example:

```python
from arena.engine import BattleEngine
from codebots import Bot
from examples.aggressive import AggressiveBot

result = BattleEngine(MyBot(), AggressiveBot()).run()
print(result.winner, result.turns_played)
```

## Submission

POST your bot to `/submit`:

```json
{
  "bot_id": "my-bot-v1",
  "name": "MyBot",
  "author": "you",
  "code": "from codebots import Bot, State\n..."
}
```

`bot_id` must be 3–64 characters; `code` at least 10 characters.

## Safety

Submitted code is executed inside a sandbox (`server/sandbox/runner.py`) built on RestrictedPython, with a 2-second timeout and a restricted builtin set. `open`, `import`, `eval`, `exec` and filesystem access are unavailable. Keep your bot pure logic — no network, no files, no imports beyond `codebots`.
