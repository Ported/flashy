"""File-based storage implementation."""

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from flashy.core.models import LevelResult, PlayerProgress


class FileStorage:
    """File-based storage backend.

    Stores player progress and session logs in the user's home directory.
    """

    def __init__(self, base_dir: Path | None = None) -> None:
        """Initialize file storage.

        Args:
            base_dir: Base directory for storage. Defaults to ~/.flashy
        """
        self._base_dir = base_dir or (Path.home() / ".flashy")
        self._base_dir.mkdir(exist_ok=True)

    @property
    def _players_dir(self) -> Path:
        """Get the players directory, creating it if needed."""
        players_dir = self._base_dir / "players"
        players_dir.mkdir(parents=True, exist_ok=True)
        return players_dir

    @property
    def _history_path(self) -> Path:
        """Get the history file path."""
        return self._base_dir / "history.log"

    @property
    def _speech_log_path(self) -> Path:
        """Get the speech log file path."""
        return self._base_dir / "speech.log"

    def load_progress(self, player_name: str) -> PlayerProgress:
        """Load player progress from disk."""
        progress_path = self._players_dir / f"{player_name}.json"

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

    def save_progress(self, player_name: str, progress: PlayerProgress) -> None:
        """Save player progress to disk."""
        progress_path = self._players_dir / f"{player_name}.json"
        data = {"stars": progress.stars}

        with open(progress_path, "w") as f:
            json.dump(data, f, indent=2)

    def log_session(self, result: LevelResult) -> None:
        """Append a level result to the history log."""
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

        with open(self._history_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def log_speech_recognition(
        self,
        raw_transcript: str,
        parsed_number: int | None,
        expected: int | None,
        matched: bool,
    ) -> None:
        """Log a speech recognition result for debugging."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "transcript": raw_transcript,
            "parsed": parsed_number,
            "expected": expected,
            "matched": matched,
        }

        with open(self._speech_log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def list_players(self) -> list[str]:
        """List all player names."""
        players = []
        for path in self._players_dir.glob("*.json"):
            players.append(path.stem)
        return sorted(players)

    def player_exists(self, player_name: str) -> bool:
        """Check if a player profile exists."""
        return (self._players_dir / f"{player_name}.json").exists()


# Default storage instance
_default_storage: FileStorage | None = None


def get_default_storage() -> FileStorage:
    """Get the default file storage instance."""
    global _default_storage
    if _default_storage is None:
        _default_storage = FileStorage()
    return _default_storage
