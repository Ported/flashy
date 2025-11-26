"""Game controller - manages game lifecycle for a level attempt."""

from dataclasses import dataclass

from flashy.history import (
    LevelResult,
    ProblemResult,
    load_progress,
    log_session,
    save_progress,
)
from flashy.levels import Level, get_level
from flashy.number_parser import is_fuzzy_match
from flashy.problems import Problem
from flashy.scoring import calculate_score, calculate_stars, get_streak_multiplier


@dataclass
class AnswerFeedback:
    """Feedback from submitting an answer."""

    is_correct: bool
    points_earned: int
    correct_answer: int
    streak: int
    streak_multiplier: float


class GameController:
    """Controls game lifecycle for a single level attempt.

    The controller owns all game state and logic:
    - Serving problems
    - Receiving and validating answers
    - Calculating scores with streak bonuses
    - Saving progress and history

    The UI should just display controller state and route input.
    """

    def __init__(self, player_name: str, level_number: int) -> None:
        self.player_name = player_name
        self.level_number = level_number
        level = get_level(level_number)
        if level is None:
            raise ValueError(f"Level {level_number} not found")
        self.level: Level = level
        self.problem_index = 0
        self.results: list[ProblemResult] = []
        self.total_score = 0
        self.streak = 0
        self.best_streak = 0
        self.total_time = 0.0

    @property
    def current_problem(self) -> Problem | None:
        """Get current problem, or None if complete."""
        if self.problem_index >= len(self.level.problems):
            return None
        return self.level.problems[self.problem_index]

    @property
    def is_complete(self) -> bool:
        """Check if all problems have been answered."""
        return self.problem_index >= len(self.level.problems)

    @property
    def correct_count(self) -> int:
        """Count of correct answers so far."""
        return sum(1 for r in self.results if r.is_correct)

    @property
    def problems_answered(self) -> int:
        """Number of problems answered so far."""
        return len(self.results)

    @property
    def total_problems(self) -> int:
        """Total number of problems in this level."""
        return len(self.level.problems)

    @property
    def time_limit(self) -> int | None:
        """Time limit in seconds for this level, or None if untimed."""
        return self.level.time_limit

    @property
    def is_timed(self) -> bool:
        """Check if this level has a time limit (boss battle)."""
        return self.level.time_limit is not None

    def time_remaining(self, elapsed: float) -> float:
        """Get remaining time given elapsed wall-clock seconds.

        Args:
            elapsed: Seconds since level started

        Returns:
            Remaining seconds, or float('inf') if untimed
        """
        if self.level.time_limit is None:
            return float("inf")
        return max(0.0, self.level.time_limit - elapsed)

    def is_time_expired(self, elapsed: float) -> bool:
        """Check if time has expired.

        Args:
            elapsed: Seconds since level started

        Returns:
            True if timed level and time has run out
        """
        if self.level.time_limit is None:
            return False
        return elapsed >= self.level.time_limit

    def submit_answer(self, answer: int | None, time_taken: float) -> AnswerFeedback:
        """Submit answer for current problem.

        Args:
            answer: The answer given (None if skipped)
            time_taken: Time in seconds to answer

        Returns:
            AnswerFeedback with result details
        """
        problem = self.current_problem
        if problem is None:
            raise ValueError("No current problem - game is complete")

        is_correct = answer is not None and is_fuzzy_match(answer, problem.answer)

        # Update streak
        if is_correct:
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
        else:
            self.streak = 0

        # Calculate score using scoring.py
        points = calculate_score(time_taken, is_correct, self.streak)
        self.total_score += points
        self.total_time += time_taken

        # Record result
        self.results.append(
            ProblemResult(
                problem=problem.display(),
                correct_answer=problem.answer,
                given_answer=answer,
                is_correct=is_correct,
                time_seconds=time_taken,
                points=points,
            )
        )

        # Advance to next problem
        self.problem_index += 1

        return AnswerFeedback(
            is_correct=is_correct,
            points_earned=points,
            correct_answer=problem.answer,
            streak=self.streak,
            streak_multiplier=get_streak_multiplier(self.streak),
        )

    def finish(self) -> tuple[int, bool]:
        """Finish the level. Saves progress and history.

        Returns:
            Tuple of (stars earned, is_new_best)
        """
        stars = calculate_stars(
            self.correct_count, self.total_problems, self.total_time
        )

        # Save progress
        progress = load_progress(self.player_name)
        old_stars = progress.get_stars(self.level_number)
        progress.set_stars(self.level_number, stars)
        save_progress(self.player_name, progress)

        # Log session history
        log_session(
            LevelResult(
                level_number=self.level_number,
                level_name=self.level.name,
                total_score=self.total_score,
                correct_count=self.correct_count,
                total_problems=self.total_problems,
                best_streak=self.best_streak,
                total_time_seconds=self.total_time,
                problems=self.results,
            )
        )

        return stars, stars > old_stars
