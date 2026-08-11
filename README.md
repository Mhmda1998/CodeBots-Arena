<div align="center">

# 🤖⚔️ CodeBots Arena

### **The AI vs AI Code Battle Arena**

*Write your bot's brain. Watch it fight. Climb the global leaderboard.*

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub Stars](https://img.shields.io/github/stars/Mhmda1998/CodeBots-Arena?style=social)](https://github.com/Mhmda1998/CodeBots-Arena)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/Q7344)

[Quick Start](#-quick-start) • [How It Works](#-how-it-works) • [Write Your Bot](#-write-your-bot) • [Leaderboard](#-leaderboard)

</div>

---

## 🎯 What is CodeBots Arena?

**CodeBots Arena** is the world's first **pure AI-vs-AI competitive coding game**. You don't play the game — **your code does**.

- 🤖 **Code a bot** in Python (simple, beginner-friendly API)
- ⚔️ **Send it into the arena** — it fights other players' bots automatically
- 🏆 **Climb the ELO leaderboard** — the smarter your strategy, the higher you rank
- 🎬 **Watch replays** — every battle is recorded as an animation
- 🌐 **Global competition** — anyone, anywhere, can challenge your bot

> 💡 **Think Chess.com meets AI/ML competitions meets Rock-Paper-Scissors — but your CODE is the player.**

---

## 🌟 Why CodeBots Arena is Different

| Feature | Description |
|---------|-------------|
| 🧠 **AI vs AI, not Player vs Player** | The game plays itself — your *strategy* is the only thing that matters |
| 📚 **Learn by doing** | Beginners learn Python, algorithms, and game theory while having fun |
| 🏆 **Fair ranking** | Pure logic wins — no pay-to-win, no luck, no skill ceiling |
| 🔄 **Replay system** | Every battle is a shareable animation (great for learning) |
| 🌍 **Truly global** | 24/7 matchmaking with players worldwide |
| 🔌 **Open-source** | MIT licensed — fork it, host your own tournaments |

---

## 🎮 Game Modes

### 1. 🏟 Arena Battle (Main Mode)
Two bots enter a 2D grid arena. Each turn, your bot decides:
- `attack` — strike the enemy if in range
- `defend` — block incoming damage
- `heal` — restore health
- `move_left` / `move_right` — reposition
- `special` — unleash your ultimate ability (cooldown-based)

**Last bot standing wins.** Match length: 50 turns max.

### 2. 🧩 Code Golf
Same problem, 100 players. Shortest working code wins.

### 3. ⚡ Speed Solve
First bot to solve a programming puzzle wins the round.

### 4. 🏆 Tournament Mode (Weekly)
Bracket-style elimination. Top 32 bots compete for prizes.

---

## 🚀 Quick Start

### For Players (Write Your Bot)

```bash
# 1. Install the SDK
pip install codebots-arena

# 2. Create your bot
codebots init my-awesome-bot
cd my-awesome-bot

# 3. Edit bot.py with your strategy
# 4. Submit it
codebots submit
```

### For Self-Hosters (Run Your Own Server)

```bash
# 1. Clone the repo
git clone https://github.com/Mhmda1998/CodeBots-Arena.git
cd CodeBots-Arena

# 2. Start backend
cd server
pip install -r requirements.txt
python main.py

# 3. Start frontend
cd ../client
npm install
npm run dev
```

Open `http://localhost:3000` and start battling!

---

## 🤖 Write Your First Bot

```python
from codebots import Bot, State

class MyBot(Bot):
    def on_init(self):
        self.name = "Thunder"
        self.color = "#FF6B35"
    
    def on_turn(self, state: State) -> str:
        # state has: my_health, enemy_health, distance, my_energy, etc.
        
        if state.enemy_distance <= 1 and state.enemy_health > 20:
            return "attack"
        
        if state.my_health < 30:
            return "heal"
        
        if state.enemy_distance > 2:
            return "move_forward"
        
        return "defend"
```

**That's it.** Submit it, and watch it fight. Improve it. Climb the ranks.

---

## 🏗 Architecture

```
CodeBots-Arena/
├── server/                    # Backend (Python + FastAPI)
│   ├── arena/                 # ⚔️ Battle engine (the core)
│   │   ├── engine.py          # Game loop & rules
│   │   ├── physics.py         # Movement, collision, damage
│   │   └── events.py          # Battle event system
│   ├── matchmaking/           # 🎯 ELO-based pairing
│   ├── leaderboard/           # 🏆 Global rankings
│   ├── sandbox/               # 🔒 Safe bot execution
│   └── api/                   # 🌐 REST endpoints
├── client/                    # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── components/
│   │   │   ├── CodeEditor/    # Monaco-based Python editor
│   │   │   ├── BattleViewer/  # Canvas-based replay
│   │   │   └── Leaderboard/   # Live ranking display
│   │   └── pages/
├── sdk/                       # 📦 Player SDK (pip package)
│   └── codebots/
│       ├── bot.py             # Base Bot class
│       └── state.py           # State object
├── examples/                  # 🤖 Sample bots
│   ├── aggressive.py
│   ├── defensive.py
│   └── adaptive.py
├── docs/                      # 📚 Documentation
└── replays/                   # 🎬 Battle recordings
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **Game Engine** | Python 3.11+ (async) |
| **Backend API** | FastAPI |
| **Sandbox** | RestrictedPython + Docker |
| **Database** | PostgreSQL |
| **Cache/Leaderboard** | Redis (Sorted Sets) |
| **Frontend** | React + TypeScript + Vite |
| **Code Editor** | Monaco Editor |
| **Battle Animation** | HTML5 Canvas |
| **Replays** | JSONL → WebSocket streaming |

---

## 🏆 Leaderboard

The global leaderboard uses **ELO rating** (like chess):
- Win against a higher-rated bot = +big points
- Lose against a lower-rated bot = -big points
- Updated every match in real-time

**Top bots get featured on the homepage!** 🌟

---

## 🤝 Contributing

We love contributions! Whether it's:
- 🐛 Bug reports
- 💡 New game modes
- 🤖 Better example bots
- 📖 Documentation improvements
- 🌐 Translations

Check [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

Copyright © 2026 Mohammed Ghabban

---

## 💖 Support the Project

If you believe in this project, consider supporting:

[![TON Wallet](https://img.shields.io/badge/TON-0098EA?style=for-the-badge&logo=ton&logoColor=white)](https://tonviewer.com/UQCxl11ULxxz9X-nvXoNOEgIosMCtHTHcmL032Tylt0u_QMe)

**💎 Wallet Address:**
```
UQCxl11ULxxz9X-nvXoNOEgIosMCtHTHcmL032Tylt0u_QMe
```

**🌐 Supported Networks & Tokens:**
- 💎 **TON** (native)
- 💵 **USDT** (jUSDT on TON)
- 🪙 **NOT**, **DOGS**, and other TON-based tokens
- 🟢 Any **Jetton standard** token

> ⭐ **The easiest way to support:** Star this repo and share it with fellow developers!

---

## 📬 Connect

- 🐙 GitHub: [@Mhmda1998](https://github.com/Mhmda1998)
- 💼 LinkedIn: [m-ghaban](https://www.linkedin.com/in/m-ghaban)
- ✈️ Telegram: [@Q7344](https://t.me/Q7344)
- 🅧 X: [@mhmda811](https://x.com/mhmda811)

---

<div align="center">

### 🌟 *Built with passion by [Mohammed Ghabban](https://github.com/Mhmda1998) from Sana'a, Yemen* 🌟

**The future of competitive coding is autonomous. Be part of it.**

</div>
