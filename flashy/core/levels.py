"""Level definitions - curated problem sequences for each level."""

from dataclasses import dataclass
from enum import Enum

from flashy.core.problems import Operation, Problem


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
        add(1, 1),
        add(2, 1),
        add(3, 2),
        add(2, 2),
        add(1, 4),
        add(4, 3),
        add(5, 6),
        add(3, 3),
        add(4, 2),
        add(5, 5),
    ),
)

LEVEL_2 = Level(
    number=2,
    world_number=1,
    level_in_world=2,
    name="Foothills",
    level_type=LevelType.INTRO,
    problems=(
        add(2, 3),
        add(3, 2),
        add(4, 2),
        add(7, 5),
        add(9, 6),
        add(6, 4),
        add(4, 3),
        add(8, 8),
        add(3, 7),
        add(9, 7),
    ),
)

LEVEL_3 = Level(
    number=3,
    world_number=1,
    level_in_world=3,
    name="Snowy Path",
    level_type=LevelType.INTRO,
    problems=(
        add(8, 6),
        add(3, 9),
        add(2, 12),
        add(9, 7),
        add(7, 5),
        add(15, 8),
        add(4, 18),
        add(21, 9),
        add(24, 24),
        add(20, 10),
    ),
)

LEVEL_4 = Level(
    number=4,
    world_number=1,
    level_in_world=4,
    name="Alpine Meadow",
    level_type=LevelType.BUILD,
    problems=(
        add(16, 15),
        add(12, 20),
        add(8, 27),
        add(17, 9),
        add(6, 0),
        add(0, 34),
        add(26, 24),
        add(30, 20),
        add(50, 10),
        add(34, 23),
    ),
)

LEVEL_5 = Level(
    number=5,
    world_number=1,
    level_in_world=5,
    name="Mountain Trail",
    level_type=LevelType.BUILD,
    problems=(
        add(25, 25),
        add(13, 17),
        add(21, 18),
        add(19, 26),
        add(32, 16),
        add(15, 19),
        add(12, 31),
        add(17, 36),
        add(40, 40),
        add(50, 56),
    ),
)

LEVEL_6 = Level(
    number=6,
    world_number=1,
    level_in_world=6,
    name="Carry's Roost",
    level_type=LevelType.FRIEND,
    problems=(
        add(94, 17),
        add(27, 92),
        add(83, 72),
        add(26, 17),
        add(72, 20),
        add(54, 21),
        add(82, 84),
        add(27, 26),
        add(10, 70),
        add(14, 74),
    ),
)

LEVEL_7 = Level(
    number=7,
    world_number=1,
    level_in_world=7,
    name="Rocky Pass",
    level_type=LevelType.CHALLENGE,
    problems=(
        add(100, 300),
        add(150, 250),
        add(250, 250),
        add(145, 165),
        add(132, 249),
        add(180, 220),
        add(257, 278),
        add(190, 10),
        add(200, 700),
        add(123, 123),
    ),
)

LEVEL_8 = Level(
    number=8,
    world_number=1,
    level_in_world=8,
    name="Steep Cliffs",
    level_type=LevelType.CHALLENGE,
    problems=(
        add(200, 142),
        add(400, 298),
        add(220, 127),
        add(726, 176),
        add(178, 654),
        add(550, 259),
        add(163, 21),
        add(72, 764),
        add(400, 550),
        add(121, 212),
    ),
)

LEVEL_9 = Level(
    number=9,
    world_number=1,
    level_in_world=9,
    name="Final Ascent",
    level_type=LevelType.PREBOSS,
    problems=(
        add(100, 100),
        add(200, 300),
        add(250, 120),
        add(500, 400),
        add(320, 180),
        add(430, 170),
        add(880, 110),
        add(120, 530),
        add(780, 115),
        add(500, 300),
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
        add(748, 129),
        add(73, 810),
        add(257, 180),
        add(128, 256),
        add(459, 123),
        add(100, 700),
        add(82, 27),
        add(64, 12),
        add(128, 412),
        add(499, 499),
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
        sub(3, 1),
        sub(4, 2),
        sub(5, 3),
        sub(4, 1),
        sub(5, 2),
        sub(6, 4),
        sub(5, 1),
        sub(6, 3),
        sub(7, 4),
        sub(8, 4),
    ),
)

LEVEL_12 = Level(
    number=12,
    world_number=2,
    level_in_world=2,
    name="Muddy Waters",
    level_type=LevelType.INTRO,
    problems=(
        sub(7, 3),
        sub(8, 2),
        sub(19, 6),
        sub(6, 6),
        sub(8, 5),
        sub(12, 7),
        sub(15, 5),
        sub(18, 8),
        sub(14, 7),
        sub(20, 10),
    ),
)

LEVEL_13 = Level(
    number=13,
    world_number=2,
    level_in_world=3,
    name="Foggy Path",
    level_type=LevelType.INTRO,
    problems=(
        sub(16, 8),
        sub(76, 8),
        sub(64, 32),
        sub(10, 6),
        sub(19, 17),
        sub(998, 997),
        sub(834, 832),
        sub(763, 760),
        sub(128, 16),
        sub(512, 256),
    ),
)

LEVEL_14 = Level(
    number=14,
    world_number=2,
    level_in_world=4,
    name="Lily Pads",
    level_type=LevelType.BUILD,
    problems=(
        sub(0, 1),
        sub(1, 3),
        sub(8, 16),
        sub(100, 200),
        sub(13, 17),
        sub(18, 22),
        sub(5, 110),
        sub(17, 127),
        sub(128, 543),
        sub(0, 888),
    ),
)

LEVEL_15 = Level(
    number=15,
    world_number=2,
    level_in_world=5,
    name="Cypress Grove",
    level_type=LevelType.BUILD,
    problems=(
        sub(10, 4),
        sub(11, 5),
        sub(12, 6),
        sub(13, 7),
        sub(14, 8),
        sub(15, 7),
        sub(12, 5),
        sub(14, 6),
        sub(16, 8),
        sub(17, 9),
    ),
)

LEVEL_16 = Level(
    number=16,
    world_number=2,
    level_in_world=6,
    name="Borrow's Hollow",
    level_type=LevelType.FRIEND,
    problems=(
        sub(10, 5),
        sub(11, 6),
        sub(12, 7),
        sub(13, 8),
        sub(11, 4),
        sub(14, 7),
        sub(12, 6),
        sub(15, 8),
        sub(13, 6),
        sub(16, 8),
    ),
)

LEVEL_17 = Level(
    number=17,
    world_number=2,
    level_in_world=7,
    name="Murky Depths",
    level_type=LevelType.CHALLENGE,
    problems=(
        sub(12, 5),
        sub(14, 6),
        sub(15, 7),
        sub(16, 8),
        sub(17, 9),
        sub(18, 9),
        sub(13, 5),
        sub(15, 6),
        sub(17, 8),
        sub(19, 10),
    ),
)

LEVEL_18 = Level(
    number=18,
    world_number=2,
    level_in_world=8,
    name="Tangled Vines",
    level_type=LevelType.CHALLENGE,
    problems=(
        sub(14, 6),
        sub(16, 7),
        sub(17, 8),
        sub(18, 9),
        sub(19, 10),
        sub(20, 9),
        sub(15, 6),
        sub(18, 8),
        sub(20, 10),
        sub(21, 11),
    ),
)

LEVEL_19 = Level(
    number=19,
    world_number=2,
    level_in_world=9,
    name="Swamp's Heart",
    level_type=LevelType.PREBOSS,
    problems=(
        sub(16, 7),
        sub(18, 9),
        sub(19, 10),
        sub(20, 11),
        sub(21, 12),
        sub(23, 11),
        sub(17, 8),
        sub(20, 9),
        sub(22, 11),
        sub(24, 12),
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
        sub(15, 7),
        sub(17, 8),
        sub(18, 9),
        sub(19, 10),
        sub(20, 11),
        sub(21, 12),
        sub(22, 11),
        sub(23, 12),
        sub(24, 12),
        sub(25, 13),
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
        div(2, 1),
        div(4, 2),
        div(6, 2),
        div(4, 1),
        div(6, 3),
        div(8, 2),
        div(3, 1),
        div(8, 4),
        div(9, 3),
        div(10, 2),
    ),
)

LEVEL_22 = Level(
    number=22,
    world_number=3,
    level_in_world=2,
    name="Sandy Trail",
    level_type=LevelType.INTRO,
    problems=(
        div(6, 2),
        div(8, 2),
        div(9, 3),
        div(10, 2),
        div(12, 3),
        div(12, 4),
        div(8, 4),
        div(10, 5),
        div(12, 2),
        div(15, 3),
    ),
)

LEVEL_23 = Level(
    number=23,
    world_number=3,
    level_in_world=3,
    name="Dune Ridge",
    level_type=LevelType.INTRO,
    problems=(
        div(8, 2),
        div(10, 2),
        div(12, 3),
        div(12, 4),
        div(14, 2),
        div(16, 4),
        div(9, 3),
        div(15, 5),
        div(16, 2),
        div(18, 3),
    ),
)

LEVEL_24 = Level(
    number=24,
    world_number=3,
    level_in_world=4,
    name="Scorpion Pass",
    level_type=LevelType.BUILD,
    problems=(
        div(10, 2),
        div(12, 3),
        div(14, 2),
        div(15, 3),
        div(16, 4),
        div(18, 2),
        div(12, 4),
        div(20, 4),
        div(18, 3),
        div(20, 5),
    ),
)

LEVEL_25 = Level(
    number=25,
    world_number=3,
    level_in_world=5,
    name="Mirage Valley",
    level_type=LevelType.BUILD,
    problems=(
        div(12, 3),
        div(14, 2),
        div(16, 4),
        div(18, 3),
        div(20, 4),
        div(21, 3),
        div(15, 5),
        div(24, 4),
        div(20, 5),
        div(24, 3),
    ),
)

LEVEL_26 = Level(
    number=26,
    world_number=3,
    level_in_world=6,
    name="Remainder's Rest",
    level_type=LevelType.FRIEND,
    problems=(
        div(10, 2),
        div(12, 3),
        div(15, 3),
        div(16, 4),
        div(18, 2),
        div(20, 4),
        div(14, 2),
        div(21, 3),
        div(24, 4),
        div(25, 5),
    ),
)

LEVEL_27 = Level(
    number=27,
    world_number=3,
    level_in_world=7,
    name="Sandstorm",
    level_type=LevelType.CHALLENGE,
    problems=(
        div(14, 2),
        div(18, 3),
        div(20, 4),
        div(21, 3),
        div(24, 4),
        div(27, 3),
        div(16, 4),
        div(28, 4),
        div(30, 5),
        div(32, 4),
    ),
)

LEVEL_28 = Level(
    number=28,
    world_number=3,
    level_in_world=8,
    name="Sunscorch",
    level_type=LevelType.CHALLENGE,
    problems=(
        div(18, 3),
        div(24, 4),
        div(25, 5),
        div(27, 3),
        div(28, 4),
        div(36, 4),
        div(20, 4),
        div(30, 5),
        div(35, 5),
        div(36, 6),
    ),
)

LEVEL_29 = Level(
    number=29,
    world_number=3,
    level_in_world=9,
    name="Pyramid's Shadow",
    level_type=LevelType.PREBOSS,
    problems=(
        div(24, 4),
        div(27, 3),
        div(30, 5),
        div(32, 4),
        div(35, 5),
        div(42, 6),
        div(28, 4),
        div(36, 4),
        div(40, 5),
        div(45, 5),
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
        div(18, 3),
        div(24, 4),
        div(27, 3),
        div(28, 4),
        div(30, 5),
        div(35, 5),
        div(36, 4),
        div(40, 5),
        div(42, 6),
        div(48, 6),
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
        mul(2, 1),
        mul(2, 2),
        mul(3, 2),
        mul(2, 3),
        mul(2, 4),
        mul(3, 3),
        mul(2, 2),
        mul(4, 2),
        mul(3, 2),
        mul(5, 2),
    ),
)

LEVEL_32 = Level(
    number=32,
    world_number=4,
    level_in_world=2,
    name="Butterfly Path",
    level_type=LevelType.INTRO,
    problems=(
        mul(2, 3),
        mul(3, 3),
        mul(4, 2),
        mul(3, 4),
        mul(5, 2),
        mul(4, 3),
        mul(2, 4),
        mul(5, 3),
        mul(4, 4),
        mul(6, 2),
    ),
)

LEVEL_33 = Level(
    number=33,
    world_number=4,
    level_in_world=3,
    name="Clover Patch",
    level_type=LevelType.INTRO,
    problems=(
        mul(3, 3),
        mul(4, 3),
        mul(5, 3),
        mul(4, 4),
        mul(6, 2),
        mul(5, 4),
        mul(3, 4),
        mul(6, 3),
        mul(5, 5),
        mul(7, 2),
    ),
)

LEVEL_34 = Level(
    number=34,
    world_number=4,
    level_in_world=4,
    name="Honeybee Hive",
    level_type=LevelType.BUILD,
    problems=(
        mul(4, 3),
        mul(5, 3),
        mul(4, 4),
        mul(6, 3),
        mul(5, 4),
        mul(7, 3),
        mul(4, 5),
        mul(6, 4),
        mul(5, 5),
        mul(8, 3),
    ),
)

LEVEL_35 = Level(
    number=35,
    world_number=4,
    level_in_world=5,
    name="Dandelion Dell",
    level_type=LevelType.BUILD,
    problems=(
        mul(5, 4),
        mul(6, 3),
        mul(5, 5),
        mul(7, 3),
        mul(6, 4),
        mul(8, 3),
        mul(4, 6),
        mul(7, 4),
        mul(6, 5),
        mul(9, 3),
    ),
)

LEVEL_36 = Level(
    number=36,
    world_number=4,
    level_in_world=6,
    name="Times's Burrow",
    level_type=LevelType.FRIEND,
    problems=(
        mul(4, 4),
        mul(5, 4),
        mul(6, 3),
        mul(5, 5),
        mul(7, 3),
        mul(6, 4),
        mul(4, 5),
        mul(7, 4),
        mul(6, 5),
        mul(8, 4),
    ),
)

LEVEL_37 = Level(
    number=37,
    world_number=4,
    level_in_world=7,
    name="Pollen Storm",
    level_type=LevelType.CHALLENGE,
    problems=(
        mul(6, 4),
        mul(7, 4),
        mul(6, 5),
        mul(8, 4),
        mul(7, 5),
        mul(9, 4),
        mul(5, 6),
        mul(8, 5),
        mul(7, 6),
        mul(9, 5),
    ),
)

LEVEL_38 = Level(
    number=38,
    world_number=4,
    level_in_world=8,
    name="Rainbow Bridge",
    level_type=LevelType.CHALLENGE,
    problems=(
        mul(7, 5),
        mul(8, 4),
        mul(6, 6),
        mul(9, 4),
        mul(7, 6),
        mul(8, 6),
        mul(5, 7),
        mul(9, 5),
        mul(8, 7),
        mul(7, 7),
    ),
)

LEVEL_39 = Level(
    number=39,
    world_number=4,
    level_in_world=9,
    name="Final Bloom",
    level_type=LevelType.PREBOSS,
    problems=(
        mul(8, 5),
        mul(7, 6),
        mul(9, 5),
        mul(8, 6),
        mul(7, 7),
        mul(9, 6),
        mul(6, 7),
        mul(8, 7),
        mul(9, 7),
        mul(8, 8),
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
        mul(7, 5),
        mul(8, 5),
        mul(6, 6),
        mul(9, 5),
        mul(7, 6),
        mul(8, 6),
        mul(7, 7),
        mul(9, 6),
        mul(8, 7),
        mul(9, 9),
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
