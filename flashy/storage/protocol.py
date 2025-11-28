"""Storage protocol defining the interface for storage backends."""

from typing import Protocol

from flashy.core.models import LevelResult, PlayerProgress


class StorageBackend(Protocol):
    """Protocol for storage backends.

    All storage operations go through this interface, allowing different
    implementations (file system, localStorage, database, etc.).
    """

    def load_progress(self, player_name: str) -> PlayerProgress:
        """Load player progress.

        Args:
            player_name: The player's name.

        Returns:
            The player's progress, or a new PlayerProgress if not found.
        """
        ...

    def save_progress(self, player_name: str, progress: PlayerProgress) -> None:
        """Save player progress.

        Args:
            player_name: The player's name.
            progress: The progress to save.
        """
        ...

    def log_session(self, result: LevelResult) -> None:
        """Log a completed level session.

        Args:
            result: The level result to log.
        """
        ...

    def log_speech_recognition(
        self,
        raw_transcript: str,
        parsed_number: int | None,
        expected: int | None,
        matched: bool,
    ) -> None:
        """Log a speech recognition result for debugging.

        Args:
            raw_transcript: The raw text from the speech recognizer.
            parsed_number: The number parsed from the transcript (None if unparseable).
            expected: The expected answer (None if not provided).
            matched: Whether it was considered a match.
        """
        ...

    def list_players(self) -> list[str]:
        """List all player names.

        Returns:
            Sorted list of player names.
        """
        ...

    def player_exists(self, player_name: str) -> bool:
        """Check if a player profile exists.

        Args:
            player_name: The player's name.

        Returns:
            True if the player exists, False otherwise.
        """
        ...
