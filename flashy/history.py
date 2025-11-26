"""Session history logging and progress tracking."""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class PlayerProgress:
    """Player's game progress - stars and unlocked levels."""

    stars: dict[int, int] = field(default_factory=dict)  # level_number -> stars (1-3)

    def get_stars(self, level: int) -> int:
        """Get stars for a level (0 if not completed)."""
        return self.stars.get(level, 0)

    def set_stars(self, level: int, stars: int) -> None:
        """Set stars for a level, keeping the best score."""
        current = self.stars.get(level, 0)
        if stars > current:
            self.stars[level] = stars

    def get_highest_unlocked(self) -> int:
        """Get the highest level that has been unlocked."""
        if not self.stars:
            return 1  # Start with level 1 unlocked

        # Find highest completed level with 2+ stars
        highest = 0
        for level_num, star_count in self.stars.items():
            if star_count >= 2:
                highest = max(highest, level_num)

        # Next level after highest completed is unlocked
        return highest + 1

    def is_unlocked(self, level: int) -> bool:
        """Check if a level is unlocked (playable)."""
        if level == 1:
            return True
        # Level is unlocked if previous level has 2+ stars
        return self.get_stars(level - 1) >= 2


@dataclass
class ProblemResult:
    """Result of a single problem attempt."""

    problem: str
    correct_answer: int
    given_answer: int | None
    is_correct: bool
    time_seconds: float
    points: int


@dataclass
class LevelResult:
    """Result of completing a level."""

    level_number: int
    level_name: str
    total_score: int
    correct_count: int
    total_problems: int
    best_streak: int
    total_time_seconds: float
    problems: list[ProblemResult]


def get_history_path() -> Path:
    """Get the path to the history file."""
    history_dir = Path.home() / ".flashy"
    history_dir.mkdir(exist_ok=True)
    return history_dir / "history.log"


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


def get_progress_path() -> Path:
    """Get the path to the progress file."""
    progress_dir = Path.home() / ".flashy"
    progress_dir.mkdir(exist_ok=True)
    return progress_dir / "progress.json"


def load_progress() -> PlayerProgress:
    """Load player progress from disk."""
    progress_path = get_progress_path()

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


def save_progress(progress: PlayerProgress) -> None:
    """Save player progress to disk."""
    progress_path = get_progress_path()

    data = {"stars": progress.stars}

    with open(progress_path, "w") as f:
        json.dump(data, f, indent=2)
