"""Core game logic - pure Python, no I/O dependencies.

This package contains the platform-independent game logic that can be
used by any frontend (TUI, web, iOS, etc.).
"""

from flashy.core.flow import (
    AppStarted,
    BossIntroDismissed,
    BossVictoryDismissed,
    FriendMeetDismissed,
    GameCompleteDismissed,
    GameEvent,
    GameFlow,
    IntroDismissed,
    LevelCompleted,
    LevelSelected,
    NewPlayerCreated,
    PlayerSelected,
    ResultContinue,
    ResultReplay,
    Screen,
    ScreenRequest,
    WorldIntroDismissed,
)
from flashy.core.levels import (
    Level,
    get_level,
    get_levels_for_world,
)
from flashy.core.models import LevelResult, PlayerProgress, ProblemResult
from flashy.core.number_parser import is_fuzzy_match, is_give_up, parse_spoken_number
from flashy.core.problems import Operation, Problem, generate_problem
from flashy.core.scoring import (
    calculate_score,
    calculate_stars,
    get_streak_multiplier,
)
from flashy.core.worlds import World, get_world

__all__ = [
    # flow
    "AppStarted",
    "BossIntroDismissed",
    "BossVictoryDismissed",
    "FriendMeetDismissed",
    "GameCompleteDismissed",
    "GameEvent",
    "GameFlow",
    "IntroDismissed",
    "LevelCompleted",
    "LevelSelected",
    "NewPlayerCreated",
    "PlayerSelected",
    "ResultContinue",
    "ResultReplay",
    "Screen",
    "ScreenRequest",
    "WorldIntroDismissed",
    # levels
    "Level",
    "get_level",
    "get_levels_for_world",
    # models
    "LevelResult",
    "PlayerProgress",
    "ProblemResult",
    # number_parser
    "is_fuzzy_match",
    "is_give_up",
    "parse_spoken_number",
    # problems
    "Operation",
    "Problem",
    "generate_problem",
    # scoring
    "calculate_score",
    "calculate_stars",
    "get_streak_multiplier",
    # worlds
    "World",
    "get_world",
]
