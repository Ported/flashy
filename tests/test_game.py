"""Tests for GameController."""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from flashy.game import AnswerFeedback, GameController


class TestGameController:
    """Tests for GameController."""

    def test_init_loads_level(self) -> None:
        controller = GameController("test_player", 1)
        assert controller.level is not None
        assert controller.level.number == 1
        assert controller.problem_index == 0
        assert controller.total_score == 0
        assert controller.streak == 0

    def test_init_invalid_level_raises(self) -> None:
        with pytest.raises(ValueError, match="Level 999 not found"):
            GameController("test_player", 999)

    def test_current_problem_returns_first(self) -> None:
        controller = GameController("test_player", 1)
        problem = controller.current_problem
        assert problem is not None
        assert problem == controller.level.problems[0]

    def test_is_complete_initially_false(self) -> None:
        controller = GameController("test_player", 1)
        assert not controller.is_complete

    def test_total_problems(self) -> None:
        controller = GameController("test_player", 1)
        assert controller.total_problems == len(controller.level.problems)

    def test_submit_correct_answer(self) -> None:
        controller = GameController("test_player", 1)
        problem = controller.current_problem
        assert problem is not None

        feedback = controller.submit_answer(problem.answer, time_taken=2.0)

        assert feedback.is_correct is True
        assert feedback.correct_answer == problem.answer
        assert feedback.points_earned > 0
        assert feedback.streak == 1

    def test_submit_wrong_answer(self) -> None:
        controller = GameController("test_player", 1)
        problem = controller.current_problem
        assert problem is not None

        wrong_answer = problem.answer + 100
        feedback = controller.submit_answer(wrong_answer, time_taken=2.0)

        assert feedback.is_correct is False
        assert feedback.correct_answer == problem.answer
        assert feedback.points_earned == 0
        assert feedback.streak == 0

    def test_submit_none_answer_is_wrong(self) -> None:
        controller = GameController("test_player", 1)
        feedback = controller.submit_answer(None, time_taken=2.0)

        assert feedback.is_correct is False
        assert feedback.points_earned == 0

    def test_streak_builds_on_correct(self) -> None:
        controller = GameController("test_player", 1)

        # Answer first 3 correctly
        feedback: Any = None
        for _ in range(3):
            problem = controller.current_problem
            if problem is None:
                break
            feedback = controller.submit_answer(problem.answer, time_taken=2.0)

        assert feedback is not None
        assert feedback.streak == 3
        assert controller.best_streak == 3

    def test_streak_resets_on_wrong(self) -> None:
        controller = GameController("test_player", 1)

        # Get 2 correct
        for _ in range(2):
            problem = controller.current_problem
            if problem is None:
                break
            controller.submit_answer(problem.answer, time_taken=2.0)

        assert controller.streak == 2

        # Get one wrong
        problem = controller.current_problem
        if problem is not None:
            feedback = controller.submit_answer(problem.answer + 100, time_taken=2.0)
            assert feedback.streak == 0
            assert controller.best_streak == 2  # Best preserved

    def test_total_score_accumulates(self) -> None:
        controller = GameController("test_player", 1)

        total = 0
        for _ in range(3):
            problem = controller.current_problem
            if problem is None:
                break
            feedback = controller.submit_answer(problem.answer, time_taken=2.0)
            total += feedback.points_earned

        assert controller.total_score == total
        assert controller.total_score > 0

    def test_correct_count(self) -> None:
        controller = GameController("test_player", 1)

        # 2 correct, 1 wrong
        for i in range(3):
            problem = controller.current_problem
            if problem is None:
                break
            if i < 2:
                controller.submit_answer(problem.answer, time_taken=2.0)
            else:
                controller.submit_answer(problem.answer + 100, time_taken=2.0)

        assert controller.correct_count == 2
        assert controller.problems_answered == 3

    def test_problem_advances_after_answer(self) -> None:
        controller = GameController("test_player", 1)

        first_problem = controller.current_problem
        controller.submit_answer(0, time_taken=1.0)  # Wrong answer
        second_problem = controller.current_problem

        assert first_problem != second_problem
        assert controller.problem_index == 1

    def test_is_complete_after_all_answered(self) -> None:
        controller = GameController("test_player", 1)

        for _ in range(controller.total_problems):
            problem = controller.current_problem
            if problem is None:
                break
            controller.submit_answer(problem.answer, time_taken=1.0)

        assert controller.is_complete
        assert controller.current_problem is None

    def test_submit_after_complete_raises(self) -> None:
        controller = GameController("test_player", 1)

        # Complete all problems
        for _ in range(controller.total_problems):
            problem = controller.current_problem
            if problem is None:
                break
            controller.submit_answer(problem.answer, time_taken=1.0)

        with pytest.raises(ValueError, match="No current problem"):
            controller.submit_answer(5, time_taken=1.0)

    @patch("flashy.game.save_progress")
    @patch("flashy.game.log_session")
    def test_finish_saves_progress(
        self, mock_log: MagicMock, mock_save: MagicMock
    ) -> None:
        controller = GameController("test_player", 1)

        # Answer all correctly
        for _ in range(controller.total_problems):
            problem = controller.current_problem
            if problem is None:
                break
            controller.submit_answer(problem.answer, time_taken=2.0)

        stars, is_new_best = controller.finish()

        assert stars >= 0
        mock_save.assert_called_once()
        mock_log.assert_called_once()

    @patch("flashy.game.save_progress")
    @patch("flashy.game.log_session")
    def test_finish_returns_stars(
        self, mock_log: MagicMock, mock_save: MagicMock
    ) -> None:
        controller = GameController("test_player", 1)

        # Answer all correctly and fast for 3 stars
        for _ in range(controller.total_problems):
            problem = controller.current_problem
            if problem is None:
                break
            controller.submit_answer(problem.answer, time_taken=1.0)

        stars, _ = controller.finish()
        assert stars == 3  # Perfect and fast

    def test_results_recorded(self) -> None:
        controller = GameController("test_player", 1)

        problem = controller.current_problem
        assert problem is not None
        controller.submit_answer(problem.answer, time_taken=2.5)

        assert len(controller.results) == 1
        result = controller.results[0]
        assert result.is_correct is True
        assert result.correct_answer == problem.answer
        assert result.given_answer == problem.answer
        assert result.time_seconds == 2.5
        assert result.points > 0


class TestAnswerFeedback:
    """Tests for AnswerFeedback dataclass."""

    def test_feedback_fields(self) -> None:
        feedback = AnswerFeedback(
            is_correct=True,
            points_earned=150,
            correct_answer=7,
            streak=3,
            streak_multiplier=1.5,
        )

        assert feedback.is_correct is True
        assert feedback.points_earned == 150
        assert feedback.correct_answer == 7
        assert feedback.streak == 3
        assert feedback.streak_multiplier == 1.5
