"""Tests for score calculation."""

from flashy.core.scoring import (
    BASE_POINTS,
    FAST_BONUS,
    FAST_THRESHOLD,
    MEDIUM_BONUS,
    MEDIUM_THRESHOLD,
    calculate_score,
    get_streak_multiplier,
)


class TestCalculateScore:
    """Tests for score calculation."""

    def test_incorrect_answer_scores_zero(self) -> None:
        assert calculate_score(1.0, is_correct=False, streak=0) == 0
        assert calculate_score(1.0, is_correct=False, streak=10) == 0

    def test_correct_answer_base_points(self) -> None:
        # Slow answer (no speed bonus), no streak
        score = calculate_score(10.0, is_correct=True, streak=0)
        assert score == BASE_POINTS

    def test_fast_answer_bonus(self) -> None:
        # Under FAST_THRESHOLD gets FAST_BONUS
        score = calculate_score(FAST_THRESHOLD - 0.5, is_correct=True, streak=0)
        assert score == int(BASE_POINTS * FAST_BONUS)

    def test_medium_answer_bonus(self) -> None:
        # Between FAST and MEDIUM threshold gets MEDIUM_BONUS
        time = (FAST_THRESHOLD + MEDIUM_THRESHOLD) / 2
        score = calculate_score(time, is_correct=True, streak=0)
        assert score == int(BASE_POINTS * MEDIUM_BONUS)

    def test_slow_answer_no_bonus(self) -> None:
        # Over MEDIUM_THRESHOLD gets no bonus
        score = calculate_score(MEDIUM_THRESHOLD + 1, is_correct=True, streak=0)
        assert score == BASE_POINTS

    def test_streak_multiplier_applied(self) -> None:
        # With streak of 5, should get 2x multiplier
        score_no_streak = calculate_score(10.0, is_correct=True, streak=0)
        score_with_streak = calculate_score(10.0, is_correct=True, streak=5)
        assert score_with_streak == score_no_streak * 2

    def test_speed_and_streak_combine(self) -> None:
        # Fast answer with streak should combine bonuses
        score = calculate_score(FAST_THRESHOLD - 0.5, is_correct=True, streak=5)
        expected = int(BASE_POINTS * FAST_BONUS * 2.0)  # 2x streak multiplier
        assert score == expected


class TestGetStreakMultiplier:
    """Tests for streak multiplier calculation."""

    def test_no_streak(self) -> None:
        assert get_streak_multiplier(0) == 1.0
        assert get_streak_multiplier(1) == 1.0
        assert get_streak_multiplier(2) == 1.0

    def test_small_streak(self) -> None:
        assert get_streak_multiplier(3) == 1.5
        assert get_streak_multiplier(4) == 1.5

    def test_medium_streak(self) -> None:
        assert get_streak_multiplier(5) == 2.0
        assert get_streak_multiplier(9) == 2.0

    def test_large_streak(self) -> None:
        assert get_streak_multiplier(10) == 3.0
        assert get_streak_multiplier(100) == 3.0
