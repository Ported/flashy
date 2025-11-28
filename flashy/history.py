"""Session history logging and progress tracking.

This module handles file I/O for player progress and session logging.
Data models are imported from flashy.core.models.
"""

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from flashy.core.models import LevelResult, PlayerProgress, ProblemResult

# Re-export models for backward compatibility
__all__ = [
    "LevelResult",
    "PlayerProgress",
    "ProblemResult",
    "get_history_path",
    "get_players_dir",
    "get_speech_log_path",
    "list_players",
    "load_progress",
    "log_session",
    "log_speech_recognition",
    "player_exists",
    "save_progress",
]


def get_history_path() -> Path:
    """Get the path to the history file."""
    history_dir = Path.home() / ".flashy"
    history_dir.mkdir(exist_ok=True)
    return history_dir / "history.log"


def get_speech_log_path() -> Path:
    """Get the path to the speech recognition log file."""
    history_dir = Path.home() / ".flashy"
    history_dir.mkdir(exist_ok=True)
    return history_dir / "speech.log"


def log_speech_recognition(
    raw_transcript: str,
    parsed_number: int | None,
    expected: int | None,
    matched: bool,
) -> None:
    """Log a speech recognition result for debugging.

    Args:
        raw_transcript: The raw text from the speech recognizer
        parsed_number: The number parsed from the transcript (None if unparseable)
        expected: The expected answer (None if not provided)
        matched: Whether it was considered a match
    """
    log_path = get_speech_log_path()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "transcript": raw_transcript,
        "parsed": parsed_number,
        "expected": expected,
        "matched": matched,
    }

    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def log_session(result: LevelResult) -> None:
    """Append a level result to the history log.

    Each entry is a single JSON line with a timestamp.
    """
    history_path = get_history_path()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "level_number": result.level_number,
        "level_name": result.level_name,
        "score": result.total_score,
        "correct": result.correct_count,
        "total": result.total_problems,
        "best_streak": result.best_streak,
        "time_seconds": result.total_time_seconds,
        "problems": [asdict(p) for p in result.problems],
    }

    with open(history_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def get_players_dir() -> Path:
    """Get the path to the players directory."""
    players_dir = Path.home() / ".flashy" / "players"
    players_dir.mkdir(parents=True, exist_ok=True)
    return players_dir


def list_players() -> list[str]:
    """List all player names."""
    players_dir = get_players_dir()
    players = []
    for path in players_dir.glob("*.json"):
        players.append(path.stem)
    return sorted(players)


def load_progress(player_name: str) -> PlayerProgress:
    """Load player progress from disk."""
    players_dir = get_players_dir()
    progress_path = players_dir / f"{player_name}.json"

    if not progress_path.exists():
        return PlayerProgress()

    try:
        with open(progress_path) as f:
            data = json.load(f)
            # Convert string keys back to int (JSON only supports string keys)
            stars = {int(k): v for k, v in data.get("stars", {}).items()}
            return PlayerProgress(stars=stars)
    except (json.JSONDecodeError, KeyError):
        return PlayerProgress()


def save_progress(player_name: str, progress: PlayerProgress) -> None:
    """Save player progress to disk."""
    players_dir = get_players_dir()
    progress_path = players_dir / f"{player_name}.json"

    data = {"stars": progress.stars}

    with open(progress_path, "w") as f:
        json.dump(data, f, indent=2)


def player_exists(player_name: str) -> bool:
    """Check if a player profile exists."""
    players_dir = get_players_dir()
    return (players_dir / f"{player_name}.json").exists()
