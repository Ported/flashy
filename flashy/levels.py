"""Level definitions - curated problem sequences for each level."""

from dataclasses import dataclass
from enum import Enum

from flashy.problems import Operation, Problem


class LevelType(Enum):
    """Type of level determining its role in the world."""

    INTRO = "intro"  # Easy warmup levels (1-3)
    BUILD = "build"  # Building difficulty (4-5)
    FRIEND = "friend"  # Meet a friend, story moment (6)
    CHALLENGE = "challenge"  # Harder levels (7-8)
    PREBOSS = "preboss"  # Tough preparation (9)
    BOSS = "boss"  # Timed boss battle (10)


@dataclass(frozen=True)
class Level:
    """Configuration for a game level with curated problems."""

    number: int  # Global level number (1-40)
    world_number: int  # Which world (1-4)
    level_in_world: int  # Position in world (1-10)
    name: str
    level_type: LevelType
    problems: tuple[Problem, ...]  # Curated problem sequence
    time_limit: int | None = None  # Seconds, only for boss levels


# Helper functions to create problems concisely
def add(a: int, b: int) -> Problem:
    """Create an addition problem."""
    return Problem(a, b, Operation.ADD, a + b)


def sub(a: int, b: int) -> Problem:
    """Create a subtraction problem (a - b)."""
    return Problem(a, b, Operation.SUBTRACT, a - b)


def mul(a: int, b: int) -> Problem:
    """Create a multiplication problem."""
    return Problem(a, b, Operation.MULTIPLY, a * b)


def div(a: int, b: int) -> Problem:
    """Create a division problem (a / b)."""
    return Problem(a, b, Operation.DIVIDE, a // b)


# =============================================================================
# WORLD 1: ADDITION ALPS (Levels 1-10)
# =============================================================================

LEVEL_1 = Level(
    number=1,
    world_number=1,
    level_in_world=1,
    name="Trailhead",
    level_type=LevelType.INTRO,
    problems=(
        add(1, 1),  # 2 - warmup
        add(2, 1),  # 3
        add(1, 2),  # 3
        add(2, 2),  # 4 - building
        add(3, 2),  # 5
        add(4, 3),  # 7 - small spike
        add(2, 3),  # 5 - relief
        add(3, 3),  # 6
        add(4, 2),  # 6
        add(5, 5),  # 10 - satisfying finish!
    ),
)

LEVEL_2 = Level(
    number=2,
    world_number=1,
    level_in_world=2,
    name="Foothills",
    level_type=LevelType.INTRO,
    problems=(
        add(2, 3),  # 5 - warmup
        add(3, 2),  # 5
        add(4, 2),  # 6
        add(3, 4),  # 7 - building
        add(5, 3),  # 8
        add(6, 4),  # 10 - spike
        add(4, 3),  # 7 - relief
        add(5, 4),  # 9
        add(4, 5),  # 9
        add(6, 6),  # 12 - doubles are satisfying
    ),
)

LEVEL_3 = Level(
    number=3,
    world_number=1,
    level_in_world=3,
    name="Snowy Path",
    level_type=LevelType.INTRO,
    problems=(
        add(3, 3),  # 6 - warmup
        add(4, 4),  # 8
        add(5, 3),  # 8
        add(6, 3),  # 9 - building
        add(5, 5),  # 10
        add(7, 4),  # 11 - spike
        add(5, 4),  # 9 - relief
        add(6, 5),  # 11
        add(7, 3),  # 10
        add(8, 4),  # 12 - finish strong
    ),
)

LEVEL_4 = Level(
    number=4,
    world_number=1,
    level_in_world=4,
    name="Alpine Meadow",
    level_type=LevelType.BUILD,
    problems=(
        add(5, 4),  # 9 - warmup
        add(6, 3),  # 9
        add(4, 7),  # 11
        add(8, 4),  # 12 - building
        add(6, 6),  # 12
        add(9, 5),  # 14 - spike
        add(7, 5),  # 12 - relief
        add(8, 6),  # 14
        add(7, 7),  # 14
        add(9, 6),  # 15 - bigger numbers now
    ),
)

LEVEL_5 = Level(
    number=5,
    world_number=1,
    level_in_world=5,
    name="Mountain Trail",
    level_type=LevelType.BUILD,
    problems=(
        add(6, 5),  # 11 - warmup
        add(7, 4),  # 11
        add(8, 5),  # 13
        add(7, 7),  # 14 - building
        add(9, 5),  # 14
        add(8, 9),  # 17 - spike
        add(6, 7),  # 13 - relief
        add(9, 6),  # 15
        add(8, 8),  # 16
        add(9, 9),  # 18 - double 9s!
    ),
)

LEVEL_6 = Level(
    number=6,
    world_number=1,
    level_in_world=6,
    name="Carry's Roost",
    level_type=LevelType.FRIEND,
    problems=(
        add(5, 5),  # 10 - friendly warmup
        add(6, 4),  # 10
        add(7, 5),  # 12
        add(8, 4),  # 12 - moderate
        add(9, 3),  # 12
        add(7, 6),  # 13 - small spike
        add(6, 6),  # 12 - relief
        add(8, 5),  # 13
        add(7, 7),  # 14
        add(10, 5),  # 15 - first 10!
    ),
)

LEVEL_7 = Level(
    number=7,
    world_number=1,
    level_in_world=7,
    name="Rocky Pass",
    level_type=LevelType.CHALLENGE,
    problems=(
        add(7, 6),  # 13 - warmup
        add(8, 7),  # 15
        add(9, 6),  # 15
        add(8, 8),  # 16 - building
        add(9, 7),  # 16
        add(12, 9),  # 21 - spike!
        add(8, 6),  # 14 - relief
        add(10, 8),  # 18
        add(9, 9),  # 18
        add(11, 9),  # 20 - hitting 20s
    ),
)

LEVEL_8 = Level(
    number=8,
    world_number=1,
    level_in_world=8,
    name="Steep Cliffs",
    level_type=LevelType.CHALLENGE,
    problems=(
        add(8, 7),  # 15 - warmup
        add(9, 8),  # 17
        add(10, 7),  # 17
        add(11, 8),  # 19 - building
        add(12, 7),  # 19
        add(13, 9),  # 22 - spike!
        add(9, 8),  # 17 - relief
        add(11, 9),  # 20
        add(12, 8),  # 20
        add(12, 12),  # 24 - double 12s!
    ),
)

LEVEL_9 = Level(
    number=9,
    world_number=1,
    level_in_world=9,
    name="Final Ascent",
    level_type=LevelType.PREBOSS,
    problems=(
        add(9, 8),  # 17 - warmup
        add(10, 9),  # 19
        add(11, 8),  # 19
        add(12, 9),  # 21 - building intensity
        add(13, 8),  # 21
        add(14, 11),  # 25 - spike!
        add(10, 9),  # 19 - brief relief
        add(13, 10),  # 23
        add(12, 12),  # 24
        add(15, 10),  # 25 - ready for boss
    ),
)

LEVEL_10 = Level(
    number=10,
    world_number=1,
    level_in_world=10,
    name="Summit's Challenge",
    level_type=LevelType.BOSS,
    time_limit=90,  # 90 seconds for 10 problems
    problems=(
        add(8, 7),  # 15 - warmup
        add(9, 8),  # 17
        add(10, 9),  # 19
        add(11, 8),  # 19
        add(12, 9),  # 21
        add(13, 8),  # 21
        add(11, 11),  # 22
        add(14, 9),  # 23
        add(12, 12),  # 24
        add(15, 10),  # 25 - finale!
    ),
)

# All levels in order
LEVELS = [
    LEVEL_1,
    LEVEL_2,
    LEVEL_3,
    LEVEL_4,
    LEVEL_5,
    LEVEL_6,
    LEVEL_7,
    LEVEL_8,
    LEVEL_9,
    LEVEL_10,
]


def get_level(level_num: int) -> Level | None:
    """Get level by number. Returns None if level doesn't exist."""
    for level in LEVELS:
        if level.number == level_num:
            return level
    return None


def get_next_level(current_level: int) -> Level | None:
    """Get the next level after the current one. Returns None if no more levels."""
    return get_level(current_level + 1)


def get_total_levels() -> int:
    """Return total number of levels available."""
    return len(LEVELS)


def get_levels_for_world(world_num: int) -> list[Level]:
    """Get all levels in a specific world."""
    return [level for level in LEVELS if level.world_number == world_num]
