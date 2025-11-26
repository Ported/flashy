"""Tests for level definitions."""

from flashy.levels import (
    LEVELS,
    LevelType,
    get_level,
    get_levels_for_world,
    get_next_level,
    get_total_levels,
)
from flashy.problems import Operation


class TestLevels:
    """Tests for level definitions."""

    def test_levels_are_numbered_sequentially(self) -> None:
        for i, level in enumerate(LEVELS, start=1):
            assert level.number == i

    def test_all_levels_have_problems(self) -> None:
        for level in LEVELS:
            assert len(level.problems) > 0

    def test_all_levels_have_10_problems(self) -> None:
        for level in LEVELS:
            assert len(level.problems) == 10

    def test_first_level_is_addition(self) -> None:
        first = LEVELS[0]
        # All problems should be addition
        for problem in first.problems:
            assert problem.operation == Operation.ADD

    def test_world_1_levels_are_addition(self) -> None:
        world_1_levels = get_levels_for_world(1)
        for level in world_1_levels:
            for problem in level.problems:
                assert problem.operation == Operation.ADD

    def test_boss_levels_have_time_limit(self) -> None:
        for level in LEVELS:
            if level.level_type == LevelType.BOSS:
                assert level.time_limit is not None
                assert level.time_limit > 0

    def test_non_boss_levels_have_no_time_limit(self) -> None:
        for level in LEVELS:
            if level.level_type != LevelType.BOSS:
                assert level.time_limit is None


class TestGetLevel:
    """Tests for get_level function."""

    def test_get_existing_level(self) -> None:
        level = get_level(1)
        assert level is not None
        assert level.number == 1

    def test_get_nonexistent_level(self) -> None:
        level = get_level(999)
        assert level is None

    def test_get_level_zero(self) -> None:
        level = get_level(0)
        assert level is None


class TestGetNextLevel:
    """Tests for get_next_level function."""

    def test_next_level_exists(self) -> None:
        next_level = get_next_level(1)
        assert next_level is not None
        assert next_level.number == 2

    def test_no_next_level_after_last(self) -> None:
        last_level_num = len(LEVELS)
        next_level = get_next_level(last_level_num)
        assert next_level is None


class TestGetTotalLevels:
    """Tests for get_total_levels function."""

    def test_total_matches_levels_list(self) -> None:
        assert get_total_levels() == len(LEVELS)

    def test_total_is_positive(self) -> None:
        assert get_total_levels() > 0


class TestGetLevelsForWorld:
    """Tests for get_levels_for_world function."""

    def test_world_1_has_10_levels(self) -> None:
        world_1_levels = get_levels_for_world(1)
        assert len(world_1_levels) == 10

    def test_world_1_levels_numbered_1_to_10(self) -> None:
        world_1_levels = get_levels_for_world(1)
        numbers = [level.number for level in world_1_levels]
        assert numbers == list(range(1, 11))

    def test_nonexistent_world_returns_empty(self) -> None:
        world_99_levels = get_levels_for_world(99)
        assert world_99_levels == []
