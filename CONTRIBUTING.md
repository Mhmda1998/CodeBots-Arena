# Contributing to CodeBots Arena

Thanks for your interest in making CodeBots Arena better! 🎮

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/Mhmda1998/CodeBots-Arena.git
cd CodeBots-Arena

# Backend
cd server
pip install -r requirements.txt
python main.py

# Frontend (in another terminal)
cd ../client
npm install
npm run dev
```

## 🧪 Running Tests

```bash
pip install -r tests/requirements.txt
pytest tests/ -v
```

## 📁 Project Layout

- `server/arena/` — battle engine (the core game logic)
- `server/api/` — FastAPI endpoints
- `server/matchmaking/` — ELO pairing
- `server/leaderboard/` — rankings
- `server/sandbox/` — safe bot execution
- `client/` — React frontend
- `sdk/` — Python SDK for bot authors
- `examples/` — sample bots to learn from
- `tests/` — pytest test suite

## 🎯 Where to Contribute

### Easy issues (good first PR)
- 🐛 Fix typos in docs
- 🤖 Add a new example bot
- 📝 Improve a docstring
- 🎨 Add a new game action (e.g. `dodge`, `charge`)

### Medium
- 🧠 Add a new matchmaking strategy
- 🏆 Add a tournament mode
- 🎬 Build the replay viewer
- 📊 Add stats graphs

### Hard
- 🔌 Implement a WebSocket for live battle streaming
- 🤝 Add team battles (2v2, 3v3)
- 🌐 Add internationalization (i18n)
- 🪙 TON/NFT integration for premium bots

## 🧬 Coding Standards

- Python: PEP 8, type hints, no `any`
- TypeScript: strict mode, no `any`
- File size: keep files under 300 lines
- Tests: every new feature needs a test
- Commit messages: `type(scope): description` (e.g. `feat(engine): add dodge action`)

## 🤖 Adding a New Action

1. Add the action string to `ACTIONS` set in `sdk/codebots/bot.py`
2. Add logic in `BattleEngine._apply_turn` in `server/arena/engine.py`
3. Add a test in `tests/test_engine.py`
4. Update the README action list
5. (Optional) Add a UI button in `client/src/pages/Editor.tsx`

## 📬 Pull Request Process

1. Fork the repo
2. Create a branch: `git checkout -b feat/amazing-feature`
3. Make your changes
4. Run tests: `pytest tests/ -v`
5. Push: `git push origin feat/amazing-feature`
6. Open a PR on GitHub

## 💬 Questions?

Open an issue or reach out:
- ✈️ Telegram: [@Q7344](https://t.me/Q7344)
- 🐙 GitHub: [@Mhmda1998](https://github.com/Mhmda1998)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.
