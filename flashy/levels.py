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

# =============================================================================
# WORLD 2: SUBTRACTION SWAMP (Levels 11-20)
# =============================================================================

LEVEL_11 = Level(
    number=11,
    world_number=2,
    level_in_world=1,
    name="Marsh Edge",
    level_type=LevelType.INTRO,
    problems=(
        sub(3, 1),  # 2 - warmup
        sub(4, 2),  # 2
        sub(5, 3),  # 2
        sub(4, 1),  # 3 - building
        sub(5, 2),  # 3
        sub(6, 4),  # 2 - easy spike
        sub(5, 1),  # 4 - relief
        sub(6, 3),  # 3
        sub(7, 4),  # 3
        sub(8, 4),  # 4 - finish
    ),
)

LEVEL_12 = Level(
    number=12,
    world_number=2,
    level_in_world=2,
    name="Muddy Waters",
    level_type=LevelType.INTRO,
    problems=(
        sub(5, 2),  # 3 - warmup
        sub(6, 3),  # 3
        sub(7, 4),  # 3
        sub(8, 5),  # 3 - building
        sub(7, 3),  # 4
        sub(9, 5),  # 4 - spike
        sub(6, 2),  # 4 - relief
        sub(8, 4),  # 4
        sub(9, 4),  # 5
        sub(10, 5),  # 5 - first 10!
    ),
)

LEVEL_13 = Level(
    number=13,
    world_number=2,
    level_in_world=3,
    name="Foggy Path",
    level_type=LevelType.INTRO,
    problems=(
        sub(7, 3),  # 4 - warmup
        sub(8, 4),  # 4
        sub(9, 5),  # 4
        sub(10, 6),  # 4 - building
        sub(9, 4),  # 5
        sub(11, 5),  # 6 - spike
        sub(8, 3),  # 5 - relief
        sub(10, 4),  # 6
        sub(11, 6),  # 5
        sub(12, 6),  # 6 - finish strong
    ),
)

LEVEL_14 = Level(
    number=14,
    world_number=2,
    level_in_world=4,
    name="Lily Pads",
    level_type=LevelType.BUILD,
    problems=(
        sub(9, 4),  # 5 - warmup
        sub(10, 5),  # 5
        sub(11, 6),  # 5
        sub(12, 7),  # 5 - building
        sub(10, 3),  # 7
        sub(13, 6),  # 7 - spike
        sub(11, 5),  # 6 - relief
        sub(12, 5),  # 7
        sub(14, 7),  # 7
        sub(15, 8),  # 7 - bigger numbers
    ),
)

LEVEL_15 = Level(
    number=15,
    world_number=2,
    level_in_world=5,
    name="Cypress Grove",
    level_type=LevelType.BUILD,
    problems=(
        sub(10, 4),  # 6 - warmup
        sub(11, 5),  # 6
        sub(12, 6),  # 6
        sub(13, 7),  # 6 - building
        sub(14, 8),  # 6
        sub(15, 7),  # 8 - spike
        sub(12, 5),  # 7 - relief
        sub(14, 6),  # 8
        sub(16, 8),  # 8
        sub(17, 9),  # 8 - teens subtraction
    ),
)

LEVEL_16 = Level(
    number=16,
    world_number=2,
    level_in_world=6,
    name="Borrow's Hollow",
    level_type=LevelType.FRIEND,
    problems=(
        sub(10, 5),  # 5 - friendly warmup
        sub(11, 6),  # 5
        sub(12, 7),  # 5
        sub(13, 8),  # 5 - moderate
        sub(11, 4),  # 7
        sub(14, 7),  # 7 - small spike
        sub(12, 6),  # 6 - relief
        sub(15, 8),  # 7
        sub(13, 6),  # 7
        sub(16, 8),  # 8 - meet Borrow!
    ),
)

LEVEL_17 = Level(
    number=17,
    world_number=2,
    level_in_world=7,
    name="Murky Depths",
    level_type=LevelType.CHALLENGE,
    problems=(
        sub(12, 5),  # 7 - warmup
        sub(14, 6),  # 8
        sub(15, 7),  # 8
        sub(16, 8),  # 8 - building
        sub(17, 9),  # 8
        sub(18, 9),  # 9 - spike
        sub(13, 5),  # 8 - relief
        sub(15, 6),  # 9
        sub(17, 8),  # 9
        sub(19, 10),  # 9 - hitting teens
    ),
)

LEVEL_18 = Level(
    number=18,
    world_number=2,
    level_in_world=8,
    name="Tangled Vines",
    level_type=LevelType.CHALLENGE,
    problems=(
        sub(14, 6),  # 8 - warmup
        sub(16, 7),  # 9
        sub(17, 8),  # 9
        sub(18, 9),  # 9 - building
        sub(19, 10),  # 9
        sub(20, 9),  # 11 - spike!
        sub(15, 6),  # 9 - relief
        sub(18, 8),  # 10
        sub(20, 10),  # 10
        sub(21, 11),  # 10 - twenty-ones!
    ),
)

LEVEL_19 = Level(
    number=19,
    world_number=2,
    level_in_world=9,
    name="Swamp's Heart",
    level_type=LevelType.PREBOSS,
    problems=(
        sub(16, 7),  # 9 - warmup
        sub(18, 9),  # 9
        sub(19, 10),  # 9
        sub(20, 11),  # 9 - building intensity
        sub(21, 12),  # 9
        sub(23, 11),  # 12 - spike!
        sub(17, 8),  # 9 - brief relief
        sub(20, 9),  # 11
        sub(22, 11),  # 11
        sub(24, 12),  # 12 - ready for boss
    ),
)

LEVEL_20 = Level(
    number=20,
    world_number=2,
    level_in_world=10,
    name="Minus's Throne",
    level_type=LevelType.BOSS,
    time_limit=90,  # 90 seconds for 10 problems
    problems=(
        sub(15, 7),  # 8 - warmup
        sub(17, 8),  # 9
        sub(18, 9),  # 9
        sub(19, 10),  # 9
        sub(20, 11),  # 9
        sub(21, 12),  # 9
        sub(22, 11),  # 11
        sub(23, 12),  # 11
        sub(24, 12),  # 12
        sub(25, 13),  # 12 - finale!
    ),
)

# =============================================================================
# WORLD 3: DIVISION DESERT (Levels 21-30)
# =============================================================================

LEVEL_21 = Level(
    number=21,
    world_number=3,
    level_in_world=1,
    name="Oasis Gate",
    level_type=LevelType.INTRO,
    problems=(
        div(2, 1),  # 2 - warmup with 1s
        div(4, 2),  # 2
        div(6, 2),  # 3
        div(4, 1),  # 4 - building
        div(6, 3),  # 2
        div(8, 2),  # 4 - easy spike
        div(3, 1),  # 3 - relief
        div(8, 4),  # 2
        div(9, 3),  # 3
        div(10, 2),  # 5 - finish
    ),
)

LEVEL_22 = Level(
    number=22,
    world_number=3,
    level_in_world=2,
    name="Sandy Trail",
    level_type=LevelType.INTRO,
    problems=(
        div(6, 2),  # 3 - warmup
        div(8, 2),  # 4
        div(9, 3),  # 3
        div(10, 2),  # 5 - building
        div(12, 3),  # 4
        div(12, 4),  # 3 - spike
        div(8, 4),  # 2 - relief
        div(10, 5),  # 2
        div(12, 2),  # 6
        div(15, 3),  # 5 - first 15!
    ),
)

LEVEL_23 = Level(
    number=23,
    world_number=3,
    level_in_world=3,
    name="Dune Ridge",
    level_type=LevelType.INTRO,
    problems=(
        div(8, 2),  # 4 - warmup
        div(10, 2),  # 5
        div(12, 3),  # 4
        div(12, 4),  # 3 - building
        div(14, 2),  # 7
        div(16, 4),  # 4 - spike
        div(9, 3),  # 3 - relief
        div(15, 5),  # 3
        div(16, 2),  # 8
        div(18, 3),  # 6 - finish strong
    ),
)

LEVEL_24 = Level(
    number=24,
    world_number=3,
    level_in_world=4,
    name="Scorpion Pass",
    level_type=LevelType.BUILD,
    problems=(
        div(10, 2),  # 5 - warmup
        div(12, 3),  # 4
        div(14, 2),  # 7
        div(15, 3),  # 5 - building
        div(16, 4),  # 4
        div(18, 2),  # 9 - spike
        div(12, 4),  # 3 - relief
        div(20, 4),  # 5
        div(18, 3),  # 6
        div(20, 5),  # 4 - bigger numbers
    ),
)

LEVEL_25 = Level(
    number=25,
    world_number=3,
    level_in_world=5,
    name="Mirage Valley",
    level_type=LevelType.BUILD,
    problems=(
        div(12, 3),  # 4 - warmup
        div(14, 2),  # 7
        div(16, 4),  # 4
        div(18, 3),  # 6 - building
        div(20, 4),  # 5
        div(21, 3),  # 7 - spike
        div(15, 5),  # 3 - relief
        div(24, 4),  # 6
        div(20, 5),  # 4
        div(24, 3),  # 8 - challenge ahead
    ),
)

LEVEL_26 = Level(
    number=26,
    world_number=3,
    level_in_world=6,
    name="Remainder's Rest",
    level_type=LevelType.FRIEND,
    problems=(
        div(10, 2),  # 5 - friendly warmup
        div(12, 3),  # 4
        div(15, 3),  # 5
        div(16, 4),  # 4 - moderate
        div(18, 2),  # 9
        div(20, 4),  # 5 - small spike
        div(14, 2),  # 7 - relief
        div(21, 3),  # 7
        div(24, 4),  # 6
        div(25, 5),  # 5 - meet Remainder!
    ),
)

LEVEL_27 = Level(
    number=27,
    world_number=3,
    level_in_world=7,
    name="Sandstorm",
    level_type=LevelType.CHALLENGE,
    problems=(
        div(14, 2),  # 7 - warmup
        div(18, 3),  # 6
        div(20, 4),  # 5
        div(21, 3),  # 7 - building
        div(24, 4),  # 6
        div(27, 3),  # 9 - spike
        div(16, 4),  # 4 - relief
        div(28, 4),  # 7
        div(30, 5),  # 6
        div(32, 4),  # 8 - getting tough
    ),
)

LEVEL_28 = Level(
    number=28,
    world_number=3,
    level_in_world=8,
    name="Sunscorch",
    level_type=LevelType.CHALLENGE,
    problems=(
        div(18, 3),  # 6 - warmup
        div(24, 4),  # 6
        div(25, 5),  # 5
        div(27, 3),  # 9 - building
        div(28, 4),  # 7
        div(36, 4),  # 9 - spike!
        div(20, 4),  # 5 - relief
        div(30, 5),  # 6
        div(35, 5),  # 7
        div(36, 6),  # 6 - six times tables!
    ),
)

LEVEL_29 = Level(
    number=29,
    world_number=3,
    level_in_world=9,
    name="Pyramid's Shadow",
    level_type=LevelType.PREBOSS,
    problems=(
        div(24, 4),  # 6 - warmup
        div(27, 3),  # 9
        div(30, 5),  # 6
        div(32, 4),  # 8 - building intensity
        div(35, 5),  # 7
        div(42, 6),  # 7 - spike!
        div(28, 4),  # 7 - brief relief
        div(36, 4),  # 9
        div(40, 5),  # 8
        div(45, 5),  # 9 - ready for boss
    ),
)

LEVEL_30 = Level(
    number=30,
    world_number=3,
    level_in_world=10,
    name="Sphinx's Riddles",
    level_type=LevelType.BOSS,
    time_limit=90,  # 90 seconds for 10 problems
    problems=(
        div(18, 3),  # 6 - warmup
        div(24, 4),  # 6
        div(27, 3),  # 9
        div(28, 4),  # 7
        div(30, 5),  # 6
        div(35, 5),  # 7
        div(36, 4),  # 9
        div(40, 5),  # 8
        div(42, 6),  # 7
        div(48, 6),  # 8 - finale!
    ),
)

# =============================================================================
# WORLD 4: MULTIPLICATION MEADOWS (Levels 31-40)
# =============================================================================

LEVEL_31 = Level(
    number=31,
    world_number=4,
    level_in_world=1,
    name="Flower Field",
    level_type=LevelType.INTRO,
    problems=(
        mul(2, 1),  # 2 - warmup
        mul(2, 2),  # 4
        mul(3, 2),  # 6
        mul(2, 3),  # 6 - building
        mul(2, 4),  # 8
        mul(3, 3),  # 9 - easy spike
        mul(2, 2),  # 4 - relief
        mul(4, 2),  # 8
        mul(3, 2),  # 6
        mul(5, 2),  # 10 - first 10!
    ),
)

LEVEL_32 = Level(
    number=32,
    world_number=4,
    level_in_world=2,
    name="Butterfly Path",
    level_type=LevelType.INTRO,
    problems=(
        mul(2, 3),  # 6 - warmup
        mul(3, 3),  # 9
        mul(4, 2),  # 8
        mul(3, 4),  # 12 - building
        mul(5, 2),  # 10
        mul(4, 3),  # 12 - spike
        mul(2, 4),  # 8 - relief
        mul(5, 3),  # 15
        mul(4, 4),  # 16
        mul(6, 2),  # 12 - doubles are fun
    ),
)

LEVEL_33 = Level(
    number=33,
    world_number=4,
    level_in_world=3,
    name="Clover Patch",
    level_type=LevelType.INTRO,
    problems=(
        mul(3, 3),  # 9 - warmup
        mul(4, 3),  # 12
        mul(5, 3),  # 15
        mul(4, 4),  # 16 - building
        mul(6, 2),  # 12
        mul(5, 4),  # 20 - spike
        mul(3, 4),  # 12 - relief
        mul(6, 3),  # 18
        mul(5, 5),  # 25
        mul(7, 2),  # 14 - finish strong
    ),
)

LEVEL_34 = Level(
    number=34,
    world_number=4,
    level_in_world=4,
    name="Honeybee Hive",
    level_type=LevelType.BUILD,
    problems=(
        mul(4, 3),  # 12 - warmup
        mul(5, 3),  # 15
        mul(4, 4),  # 16
        mul(6, 3),  # 18 - building
        mul(5, 4),  # 20
        mul(7, 3),  # 21 - spike
        mul(4, 5),  # 20 - relief
        mul(6, 4),  # 24
        mul(5, 5),  # 25
        mul(8, 3),  # 24 - bigger numbers
    ),
)

LEVEL_35 = Level(
    number=35,
    world_number=4,
    level_in_world=5,
    name="Dandelion Dell",
    level_type=LevelType.BUILD,
    problems=(
        mul(5, 4),  # 20 - warmup
        mul(6, 3),  # 18
        mul(5, 5),  # 25
        mul(7, 3),  # 21 - building
        mul(6, 4),  # 24
        mul(8, 3),  # 24 - spike
        mul(4, 6),  # 24 - relief
        mul(7, 4),  # 28
        mul(6, 5),  # 30
        mul(9, 3),  # 27 - nines!
    ),
)

LEVEL_36 = Level(
    number=36,
    world_number=4,
    level_in_world=6,
    name="Times's Burrow",
    level_type=LevelType.FRIEND,
    problems=(
        mul(4, 4),  # 16 - friendly warmup
        mul(5, 4),  # 20
        mul(6, 3),  # 18
        mul(5, 5),  # 25 - moderate
        mul(7, 3),  # 21
        mul(6, 4),  # 24 - small spike
        mul(4, 5),  # 20 - relief
        mul(7, 4),  # 28
        mul(6, 5),  # 30
        mul(8, 4),  # 32 - meet Times!
    ),
)

LEVEL_37 = Level(
    number=37,
    world_number=4,
    level_in_world=7,
    name="Pollen Storm",
    level_type=LevelType.CHALLENGE,
    problems=(
        mul(6, 4),  # 24 - warmup
        mul(7, 4),  # 28
        mul(6, 5),  # 30
        mul(8, 4),  # 32 - building
        mul(7, 5),  # 35
        mul(9, 4),  # 36 - spike
        mul(5, 6),  # 30 - relief
        mul(8, 5),  # 40
        mul(7, 6),  # 42
        mul(9, 5),  # 45 - getting tough
    ),
)

LEVEL_38 = Level(
    number=38,
    world_number=4,
    level_in_world=8,
    name="Rainbow Bridge",
    level_type=LevelType.CHALLENGE,
    problems=(
        mul(7, 5),  # 35 - warmup
        mul(8, 4),  # 32
        mul(6, 6),  # 36
        mul(9, 4),  # 36 - building
        mul(7, 6),  # 42
        mul(8, 6),  # 48 - spike!
        mul(5, 7),  # 35 - relief
        mul(9, 5),  # 45
        mul(8, 7),  # 56
        mul(7, 7),  # 49 - sevens!
    ),
)

LEVEL_39 = Level(
    number=39,
    world_number=4,
    level_in_world=9,
    name="Final Bloom",
    level_type=LevelType.PREBOSS,
    problems=(
        mul(8, 5),  # 40 - warmup
        mul(7, 6),  # 42
        mul(9, 5),  # 45
        mul(8, 6),  # 48 - building intensity
        mul(7, 7),  # 49
        mul(9, 6),  # 54 - spike!
        mul(6, 7),  # 42 - brief relief
        mul(8, 7),  # 56
        mul(9, 7),  # 63
        mul(8, 8),  # 64 - ready for boss
    ),
)

LEVEL_40 = Level(
    number=40,
    world_number=4,
    level_in_world=10,
    name="Calculata's Garden",
    level_type=LevelType.BOSS,
    time_limit=90,  # 90 seconds for 10 problems
    problems=(
        mul(7, 5),  # 35 - warmup
        mul(8, 5),  # 40
        mul(6, 6),  # 36
        mul(9, 5),  # 45
        mul(7, 6),  # 42
        mul(8, 6),  # 48
        mul(7, 7),  # 49
        mul(9, 6),  # 54
        mul(8, 7),  # 56
        mul(9, 9),  # 81 - finale!
    ),
)

# All levels in order
LEVELS = [
    # World 1: Addition Alps
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
    # World 2: Subtraction Swamp
    LEVEL_11,
    LEVEL_12,
    LEVEL_13,
    LEVEL_14,
    LEVEL_15,
    LEVEL_16,
    LEVEL_17,
    LEVEL_18,
    LEVEL_19,
    LEVEL_20,
    # World 3: Division Desert
    LEVEL_21,
    LEVEL_22,
    LEVEL_23,
    LEVEL_24,
    LEVEL_25,
    LEVEL_26,
    LEVEL_27,
    LEVEL_28,
    LEVEL_29,
    LEVEL_30,
    # World 4: Multiplication Meadows
    LEVEL_31,
    LEVEL_32,
    LEVEL_33,
    LEVEL_34,
    LEVEL_35,
    LEVEL_36,
    LEVEL_37,
    LEVEL_38,
    LEVEL_39,
    LEVEL_40,
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
