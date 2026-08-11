# Changelog

All notable changes to CodeBots Arena will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-11

### 🎉 Initial Release

#### Added
- **Battle Engine** — turn-based combat with 7 actions (attack, defend, heal, move, special, wait)
- **SDK** — `Bot` base class + `State` dataclass for players
- **FastAPI Server** — submit, match, leaderboard, bot-info endpoints
- **ELO Matchmaking** — standard chess-style rating system
- **Sandbox** — RestrictedPython + subprocess for safe bot execution
- **React Frontend** — Monaco-based code editor, leaderboard, home page
- **3 Example Bots** — aggressive, defensive, adaptive
- **Docker Support** — Dockerfile for both server and client + docker-compose
- **CI Pipeline** — GitHub Actions for Python tests + Node build
- **Documentation** — README, CONTRIBUTING, ARCHITECTURE, ROADMAP
- **MIT License**

#### Stats
- 30+ files
- 3,000+ lines of code
- 100% Python (backend) + TypeScript (frontend)
