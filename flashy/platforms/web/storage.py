"""Web storage backend using browser localStorage via Pyodide."""

import json
from dataclasses import asdict
from datetime import datetime

from flashy.core.models import LevelResult, PlayerProgress

# When running in Pyodide, js module gives access to browser APIs
try:
    from js import localStorage  # type: ignore[import-not-found]
except ImportError:
    # Fallback for testing outside browser
    localStorage = None


class WebStorage:
    """Storage backend using browser localStorage.

    Data is stored as JSON strings with the following keys:
    - flashy_players: List of player names
    - flashy_player_{name}: Player progress JSON
    - flashy_history: Array of session log entries
    """

    def _get(self, key: str) -> str | None:
        """Get a value from localStorage."""
        if localStorage is None:
            return None
        return localStorage.getItem(key)

    def _set(self, key: str, value: str) -> None:
        """Set a value in localStorage."""
        if localStorage is None:
            return
        localStorage.setItem(key, value)

    def load_progress(self, player_name: str) -> PlayerProgress:
        """Load player progress from localStorage."""
        data_str = self._get(f"flashy_player_{player_name}")
        if not data_str:
            return PlayerProgress()

        try:
            data = json.loads(data_str)
            stars = {int(k): v for k, v in data.get("stars", {}).items()}
            best_scores = {int(k): v for k, v in data.get("best_scores", {}).items()}
            return PlayerProgress(stars=stars, best_scores=best_scores)
        except (json.JSONDecodeError, KeyError):
            return PlayerProgress()

    def save_progress(self, player_name: str, progress: PlayerProgress) -> None:
        """Save player progress to localStorage."""
        # Ensure player is in the players list
        players = self.list_players()
        if player_name not in players:
            players.append(player_name)
            self._set("flashy_players", json.dumps(players))

        # Save progress
        data = {"stars": progress.stars, "best_scores": progress.best_scores}
        self._set(f"flashy_player_{player_name}", json.dumps(data))

    def log_session(self, result: LevelResult) -> None:
        """Append a session result to history."""
        history_str = self._get("flashy_history") or "[]"
        try:
            history = json.loads(history_str)
        except json.JSONDecodeError:
            history = []

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

        history.append(entry)
        self._set("flashy_history", json.dumps(history))

    def load_history(self) -> list[dict]:
        """Load session history from localStorage."""
        history_str = self._get("flashy_history") or "[]"
        try:
            return json.loads(history_str)
        except json.JSONDecodeError:
            return []

    def log_speech_recognition(
        self,
        raw_transcript: str,
        parsed_number: int | None,
        expected: int | None,
        matched: bool,
    ) -> None:
        """Log speech recognition (stored in memory only for web)."""
        # For web, we might just console.log this or skip
        pass

    def list_players(self) -> list[str]:
        """List all player names."""
        players_str = self._get("flashy_players")
        if not players_str:
            return []
        try:
            return json.loads(players_str)
        except json.JSONDecodeError:
            return []

    def player_exists(self, player_name: str) -> bool:
        """Check if a player exists."""
        return player_name in self.list_players()
