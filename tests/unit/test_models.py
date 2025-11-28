"""Tests for data models."""

from flashy.core.models import PlayerProgress


class TestPlayerProgressStars:
    """Tests for stars tracking."""

    def test_get_stars_default_zero(self) -> None:
        progress = PlayerProgress()
        assert progress.get_stars(1) == 0

    def test_set_stars(self) -> None:
        progress = PlayerProgress()
        progress.set_stars(1, 3)
        assert progress.get_stars(1) == 3

    def test_set_stars_keeps_best(self) -> None:
        progress = PlayerProgress()
        progress.set_stars(1, 3)
        progress.set_stars(1, 2)  # Worse score
        assert progress.get_stars(1) == 3  # Still 3

    def test_set_stars_updates_if_better(self) -> None:
        progress = PlayerProgress()
        progress.set_stars(1, 2)
        progress.set_stars(1, 3)  # Better score
        assert progress.get_stars(1) == 3


class TestPlayerProgressBestScores:
    """Tests for best score tracking."""

    def test_get_best_score_default_zero(self) -> None:
        progress = PlayerProgress()
        assert progress.get_best_score(1) == 0

    def test_set_best_score(self) -> None:
        progress = PlayerProgress()
        progress.set_best_score(1, 2700)
        assert progress.get_best_score(1) == 2700

    def test_set_best_score_keeps_best(self) -> None:
        progress = PlayerProgress()
        progress.set_best_score(1, 2700)
        progress.set_best_score(1, 2500)  # Worse score
        assert progress.get_best_score(1) == 2700  # Still 2700

    def test_set_best_score_updates_if_better(self) -> None:
        progress = PlayerProgress()
        progress.set_best_score(1, 2500)
        progress.set_best_score(1, 2700)  # Better score
        assert progress.get_best_score(1) == 2700

    def test_get_total_best_score_empty(self) -> None:
        progress = PlayerProgress()
        assert progress.get_total_best_score() == 0

    def test_get_total_best_score_single_level(self) -> None:
        progress = PlayerProgress()
        progress.set_best_score(1, 2700)
        assert progress.get_total_best_score() == 2700

    def test_get_total_best_score_multiple_levels(self) -> None:
        progress = PlayerProgress()
        progress.set_best_score(1, 2700)
        progress.set_best_score(2, 2500)
        progress.set_best_score(3, 2800)
        assert progress.get_total_best_score() == 8000

    def test_total_score_only_counts_best_per_level(self) -> None:
        """Playing a level multiple times only counts the best score."""
        progress = PlayerProgress()
        # Play level 1 three times
        progress.set_best_score(1, 2500)
        progress.set_best_score(1, 2700)  # Better
        progress.set_best_score(1, 2600)  # Worse than best
        # Play level 2 once
        progress.set_best_score(2, 2400)

        # Total should be best of level 1 (2700) + level 2 (2400)
        assert progress.get_total_best_score() == 5100


class TestPlayerProgressUnlocked:
    """Tests for level unlocking."""

    def test_level_1_always_unlocked(self) -> None:
        progress = PlayerProgress()
        assert progress.is_unlocked(1)

    def test_level_2_locked_initially(self) -> None:
        progress = PlayerProgress()
        assert not progress.is_unlocked(2)

    def test_level_2_unlocked_after_2_stars_on_1(self) -> None:
        progress = PlayerProgress()
        progress.set_stars(1, 2)
        assert progress.is_unlocked(2)

    def test_get_highest_unlocked_initial(self) -> None:
        progress = PlayerProgress()
        assert progress.get_highest_unlocked() == 1

    def test_get_highest_unlocked_after_progress(self) -> None:
        progress = PlayerProgress()
        progress.set_stars(1, 3)
        progress.set_stars(2, 2)
        assert progress.get_highest_unlocked() == 3
