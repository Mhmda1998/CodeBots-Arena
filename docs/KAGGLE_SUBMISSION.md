# Kaggle Submission Guide

How to package CodeBots Arena for an AI-vs-AI code competition.

## Package layout

Submit a repository containing:

```
codebots/           # the SDK (sdk/codebots in this repo)
arena/              # the deterministic battle engine (server/arena in this repo)
examples/           # reference bots
```

Copy `sdk/codebots/` and `server/arena/` into a single flat package so that
`from codebots import Bot, State` and `from arena.engine import BattleEngine`
both work at the top level.

## Submission format

A submission is a single Python file that defines **one** class inheriting from
`codebots.Bot`. The class must expose:

- `name: str` — display name, max 64 characters.
- `color: str` — hex colour, e.g. `"#3388FF"`.
- `author: str` — display name of the author.
- `on_turn(state) -> str` — the strategy.

Optional: `on_init()` for per-match setup.

```python
from codebots import Bot, State


class SubmissionBot(Bot):
    name = "SubmissionBot"
    color = "#3388FF"
    author = "your name"

    def on_turn(self, state: State) -> str:
        if state.enemy_distance <= 1:
            return "attack"
        return "move_right"
```

## Evaluation

Every submission plays a fixed set of matches against the reference bots
(`aggressive`, `defensive`, `adaptive`, `berserker`, `tactician`) in both
positions (A/B order swapped). The engine is fully deterministic, so the same
seed always produces the same result.

Scoring:

- Win = 1 point, draw = 0.5, loss = 0.
- A bot that raises an exception or returns an invalid action is treated as
  `wait` for that turn and does not disqualify the submission.

## Submission checklist

1. `name`, `color`, `author` set.
2. `on_turn` never raises — guard against empty history and `None` values.
3. Return only one of the seven valid action strings.
4. Strategy completes a full 50-turn match in well under the 2-second
   per-turn budget (the sandbox enforces a 2s init timeout).
5. No imports other than `codebots` (and standard-library-free logic).

## Local verification

```bash
pip install -e sdk
python -m pytest tests -q
python -m arena.play --bot examples/tactician.py --opponent examples/defensive.py
```

Run your bot against all five reference bots before submitting — a strategy that
only beats one of them will not survive the leaderboard.

## Scoring summary

| Outcome | Points |
|---|---|
| Win | 1.0 |
| Draw | 0.5 |
| Loss | 0.0 |
| Invalid / timeout turn | 0.0 for that turn (treated as `wait`) |
