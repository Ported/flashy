"""Data models for game state - pure data, no I/O."""

from dataclasses import dataclass, field


@dataclass
class PlayerProgress:
    """Player's game progress - stars, best scores, and unlocked levels."""

    stars: dict[int, int] = field(default_factory=dict)  # level_number -> stars (1-3)
    best_scores: dict[int, int] = field(default_factory=dict)  # level_number -> score

    def get_stars(self, level: int) -> int:
        """Get stars for a level (0 if not completed)."""
        return self.stars.get(level, 0)

    def set_stars(self, level: int, stars: int) -> None:
        """Set stars for a level, keeping the best."""
        current = self.stars.get(level, 0)
        if stars > current:
            self.stars[level] = stars

    def get_best_score(self, level: int) -> int:
        """Get best score for a level (0 if not completed)."""
        return self.best_scores.get(level, 0)

    def set_best_score(self, level: int, score: int) -> None:
        """Set best score for a level, keeping the best."""
        current = self.best_scores.get(level, 0)
        if score > current:
            self.best_scores[level] = score

    def get_total_best_score(self) -> int:
        """Get sum of best scores across all levels."""
        return sum(self.best_scores.values())

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
