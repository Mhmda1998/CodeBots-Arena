"""
CodeBots Arena - FastAPI Server
Exposes REST endpoints for submitting bots, running matches, and viewing leaderboard.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from arena.engine import BattleEngine
from leaderboard import Leaderboard
from matchmaking.elo import rank_label

app = FastAPI(
    title="CodeBots Arena API",
    version="0.1.0",
    description="AI vs AI Code Battle Arena — REST API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

leaderboard = Leaderboard()
SUBMISSIONS_DIR = Path("./submissions")
SUBMISSIONS_DIR.mkdir(exist_ok=True)


class BotSubmission(BaseModel):
    bot_id: str = Field(..., min_length=3, max_length=64)
    name: str = Field(..., min_length=1, max_length=64)
    author: str = Field(..., min_length=1, max_length=64)
    code: str = Field(..., min_length=10)


class MatchRequest(BaseModel):
    bot_a_id: str
    bot_b_id: str
    max_turns: int = Field(default=50, ge=10, le=200)


def _load_bot_class(bot_path: Path):
    """Safely load a Bot class from a Python file."""
    spec = importlib.util.spec_from_file_location(bot_path.stem, bot_path)
    if not spec or not spec.loader:
        raise HTTPException(400, "Could not load bot file")
    module = importlib.util.module_from_spec(spec)
    sys.modules[bot_path.stem] = module
    spec.loader.exec_module(module)
    for attr in dir(module):
        obj = getattr(module, attr)
        if isinstance(obj, type) and attr != "Bot" and obj.__bases__[0].__name__ == "Bot":
            return obj
    raise HTTPException(400, "No Bot subclass found in uploaded code")


@app.get("/")
def root() -> dict:
    return {
        "service": "CodeBots Arena",
        "version": "0.1.0",
        "endpoints": ["/health", "/leaderboard", "/match", "/submit"],
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "registered_bots": len(leaderboard.bots)}


@app.post("/submit")
async def submit_bot(payload: BotSubmission) -> dict:
    """Submit a bot from inline code."""
    bot_path = SUBMISSIONS_DIR / f"{payload.bot_id}.py"
    bot_path.write_text(payload.code, encoding="utf-8")
    try:
        BotClass = _load_bot_class(bot_path)
        instance = BotClass()
        leaderboard.register(
            bot_id=payload.bot_id,
            name=payload.name or instance.name,
            author=payload.author or instance.author,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"Bot execution failed: {e}")
    return {"ok": True, "bot_id": payload.bot_id}


@app.post("/submit_file")
async def submit_bot_file(
    bot_id: str,
    name: str,
    author: str,
    file: UploadFile = File(...),
) -> dict:
    """Submit a bot as an uploaded .py file."""
    if not file.filename or not file.filename.endswith(".py"):
        raise HTTPException(400, "Only .py files allowed")
    content = await file.read()
    bot_path = SUBMISSIONS_DIR / f"{bot_id}.py"
    bot_path.write_bytes(content)
    try:
        BotClass = _load_bot_class(bot_path)
        instance = BotClass()
        leaderboard.register(bot_id=bot_id, name=name or instance.name, author=author or instance.author)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"Bot execution failed: {e}")
    return {"ok": True, "bot_id": bot_id}


@app.get("/leaderboard")
def get_leaderboard(limit: int = 20) -> list[dict]:
    return leaderboard.to_json()[:limit]


@app.post("/match")
def run_match(req: MatchRequest) -> dict:
    """Run a match between two registered bots."""
    bot_a_path = SUBMISSIONS_DIR / f"{req.bot_a_id}.py"
    bot_b_path = SUBMISSIONS_DIR / f"{req.bot_b_id}.py"
    if not bot_a_path.exists():
        raise HTTPException(404, f"Bot A not found: {req.bot_a_id}")
    if not bot_b_path.exists():
        raise HTTPException(404, f"Bot B not found: {req.bot_b_id}")

    try:
        ClassA = _load_bot_class(bot_a_path)
        ClassB = _load_bot_class(bot_b_path)
        engine = BattleEngine(ClassA(), ClassB(), max_turns=req.max_turns)
        result = engine.run()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Match failed: {e}")

    leaderboard.record_match(req.bot_a_id, req.bot_b_id, result.winner)

    return {
        "winner": result.winner,
        "turns_played": result.turns_played,
        "duration_ms": result.duration_ms,
        "bot_a": {"name": result.bot_a_name, "final_hp": result.bot_a_final_hp},
        "bot_b": {"name": result.bot_b_name, "final_hp": result.bot_b_final_hp},
        "log": [
            {
                "turn": e.turn,
                "actor": e.actor,
                "action": e.action,
                "effect": e.effect,
                "damage": e.damage_dealt,
                "healing": e.healing_done,
            }
            for e in result.log
        ],
    }


@app.get("/bot/{bot_id}")
def get_bot(bot_id: str) -> dict:
    if bot_id not in leaderboard.bots:
        raise HTTPException(404, "Bot not found")
    b = leaderboard.bots[bot_id]
    return {
        "bot_id": b.bot_id,
        "name": b.name,
        "author": b.author,
        "rating": b.elo.rating,
        "rank_label": rank_label(b.elo.rating),
        "wins": b.elo.wins,
        "losses": b.elo.losses,
        "draws": b.elo.draws,
        "matches": b.elo.matches,
    }
