# CodeBots Arena — Architecture

## 🏗 High-Level

```
┌─────────────────────────────────────────────────────────────┐
│  Player's Browser  →  React Frontend (port 3000)           │
│                            ↕ HTTP/JSON                      │
│  FastAPI Backend (port 8000)                                │
│    ├── /submit  →  save bot file + register in leaderboard  │
│    ├── /match   →  load two bots → run engine → log result  │
│    └── /leaderboard → return top N bots                     │
│                            ↕                                │
│  BattleEngine (pure Python)                                 │
│    └── uses sandbox for safe init() execution               │
│                            ↕                                │
│  Submissions directory (./submissions/*.py)                 │
└─────────────────────────────────────────────────────────────┘
```

## 🧩 Components

### 1. SDK (`sdk/codebots/`)
- `Bot` — abstract base class
- `State` — read-only state passed to `on_turn()`
- `validate_action` — sanitize bot output
- Distributed as `pip install codebots-arena`

### 2. Engine (`server/arena/`)
- `BattleEngine` — runs a match (no I/O, pure logic)
- `TurnEvent` — one event in the log
- `BattleResult` — final result + JSONL replay
- `MAX_TURNS = 50`, `ARENA_MIN/MAX = ±5`

### 3. Matchmaking (`server/matchmaking/`)
- `update_elo` — standard ELO formula
- `expected_score` — probability of A winning
- `rank_label` — Wood → Grandmaster tiers

### 4. Leaderboard (`server/leaderboard/`)
- In-memory `Leaderboard` class (replace with Redis for production)
- `record_match` updates both bots' ratings
- `top(N)` returns sorted slice

### 5. API (`server/api/`)
- `POST /submit` — register a bot from inline code
- `POST /submit_file` — register a bot from file upload
- `POST /match` — run a match between two registered bots
- `GET /leaderboard` — return top bots
- `GET /bot/{id}` — return one bot's info

### 6. Sandbox (`server/sandbox/`)
- `safe_exec` — runs init code in a RestrictedPython + subprocess sandbox
- Used to validate bots before allowing them to compete

### 7. Frontend (`client/`)
- React 18 + TypeScript + Vite
- Monaco editor for bot coding
- Tailwind CSS for styling
- 4 pages: Home, Editor, Leaderboard, Battle

## 🔄 Match Flow

```
1. Player submits bot code via /submit
   → saved to submissions/{bot_id}.py
   → BotClass instantiated once to validate
   → registered in leaderboard

2. Player requests match via /match
   → load ClassA from submissions/{a_id}.py
   → load ClassB from submissions/{b_id}.py
   → engine.run() simulates the battle
   → result.winner returned to caller
   → leaderboard.record_match() updates ELO

3. Frontend polls /leaderboard to display rankings
```

## 🛡 Security

- All bot code runs in RestrictedPython (no `import os`, `eval`, etc.)
- Init code runs in a subprocess with a 2-second timeout
- No filesystem/network access from inside bots (yet)
- For production: use Docker + cgroups for stronger isolation

## 📈 Scaling

- **Single server**: 100s of concurrent matches (Python asyncio)
- **Horizontal**: split into workers (Celery + Redis)
- **Hot path**: engine is pure CPU, scales linearly with cores
- **Storage**: switch from in-memory to Redis for leaderboard

## 🧪 Testing

- `pytest tests/` runs all engine + ELO tests
- Engine is fully deterministic (no I/O, no time dependency in logic)
- Can simulate thousands of matches for stress testing
