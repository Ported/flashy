"""Game flow state machine - defines screen transitions.

This module owns all navigation logic. Screens emit events, and GameFlow
determines what screen to show next. This ensures consistent game flow
across all platforms (TUI, web, iOS).
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from flashy.core.levels import get_level
from flashy.core.models import PlayerProgress
from flashy.core.worlds import get_world


class Screen(Enum):
    """All possible screens in the game."""

    PLAYER_SELECT = auto()
    NEW_PLAYER = auto()
    INTRO = auto()
    WORLD_INTRO = auto()
    WORLD_MAP = auto()
    FRIEND_MEET = auto()
    BOSS_INTRO = auto()
    GAMEPLAY = auto()
    RESULT = auto()
    BOSS_VICTORY = auto()
    GAME_COMPLETE = auto()


@dataclass(frozen=True)
class ScreenRequest:
    """Request to show a specific screen with parameters."""

    screen: Screen
    params: dict[str, Any]

    def __repr__(self) -> str:
        return f"ScreenRequest({self.screen.name}, {self.params})"


# --- Events that trigger screen transitions ---


@dataclass(frozen=True)
class GameEvent:
    """Base class for game events."""

    pass


@dataclass(frozen=True)
class AppStarted(GameEvent):
    """App has started."""

    pass


@dataclass(frozen=True)
class PlayerSelected(GameEvent):
    """Player selected from player list."""

    player_name: str
    is_new_player: bool  # True if this is a brand new player


@dataclass(frozen=True)
class NewPlayerCreated(GameEvent):
    """New player profile created."""

    player_name: str


@dataclass(frozen=True)
class IntroDismissed(GameEvent):
    """Intro story screen dismissed."""

    player_name: str


@dataclass(frozen=True)
class WorldIntroDismissed(GameEvent):
    """World intro story screen dismissed."""

    player_name: str
    world_number: int


@dataclass(frozen=True)
class LevelSelected(GameEvent):
    """Level selected from world map."""

    player_name: str
    level_number: int


@dataclass(frozen=True)
class FriendMeetDismissed(GameEvent):
    """Friend meet story screen dismissed."""

    player_name: str
    level_number: int


@dataclass(frozen=True)
class BossIntroDismissed(GameEvent):
    """Boss intro story screen dismissed."""

    player_name: str
    level_number: int


@dataclass(frozen=True)
class LevelCompleted(GameEvent):
    """Level gameplay completed."""

    player_name: str
    level_number: int
    stars: int
    is_new_best: bool
    correct: int
    total: int
    score: int
    best_streak: int


@dataclass(frozen=True)
class ResultContinue(GameEvent):
    """Continue button pressed on result screen."""

    player_name: str
    level_number: int
    stars: int


@dataclass(frozen=True)
class ResultReplay(GameEvent):
    """Replay button pressed on result screen."""

    player_name: str
    level_number: int


@dataclass(frozen=True)
class BossVictoryDismissed(GameEvent):
    """Boss victory screen dismissed."""

    player_name: str
    world_number: int


@dataclass(frozen=True)
class GameCompleteDismissed(GameEvent):
    """Game complete screen dismissed."""

    pass


class GameFlow:
    """Determines screen transitions based on game events.

    This is the single source of truth for game navigation. All platforms
    should use this to ensure consistent behavior.
    """

    def handle(
        self, event: GameEvent, progress: PlayerProgress | None = None
    ) -> ScreenRequest:
        """Handle a game event and return the next screen to show.

        Args:
            event: The game event that occurred.
            progress: Player's current progress (needed for some transitions).

        Returns:
            ScreenRequest indicating which screen to show next.
        """
        if isinstance(event, AppStarted):
            return ScreenRequest(Screen.PLAYER_SELECT, {})

        if isinstance(event, PlayerSelected):
            if event.is_new_player:
                return ScreenRequest(Screen.NEW_PLAYER, {})
            # Existing player - check if they've played before
            if progress and progress.get_highest_unlocked() > 1:
                # Return to world map
                return ScreenRequest(
                    Screen.WORLD_MAP,
                    {"player_name": event.player_name},
                )
            # New-ish player, show intro
            return ScreenRequest(
                Screen.INTRO,
                {"player_name": event.player_name},
            )

        if isinstance(event, NewPlayerCreated):
            return ScreenRequest(
                Screen.INTRO,
                {"player_name": event.player_name},
            )

        if isinstance(event, IntroDismissed):
            return ScreenRequest(
                Screen.WORLD_INTRO,
                {"player_name": event.player_name, "world_number": 1},
            )

        if isinstance(event, WorldIntroDismissed):
            return ScreenRequest(
                Screen.WORLD_MAP,
                {"player_name": event.player_name, "world_number": event.world_number},
            )

        if isinstance(event, LevelSelected):
            level = get_level(event.level_number)
            if level is None:
                return ScreenRequest(
                    Screen.WORLD_MAP,
                    {"player_name": event.player_name},
                )

            # Check for story screens before certain levels
            if level.level_in_world == 6:
                # Friend meet before level 6
                return ScreenRequest(
                    Screen.FRIEND_MEET,
                    {
                        "player_name": event.player_name,
                        "world_number": level.world_number,
                        "level_number": event.level_number,
                    },
                )
            if level.level_in_world == 10:
                # Boss intro before level 10
                return ScreenRequest(
                    Screen.BOSS_INTRO,
                    {
                        "player_name": event.player_name,
                        "world_number": level.world_number,
                        "level_number": event.level_number,
                    },
                )

            # Regular level - go straight to gameplay
            return ScreenRequest(
                Screen.GAMEPLAY,
                {"player_name": event.player_name, "level_number": event.level_number},
            )

        if isinstance(event, FriendMeetDismissed):
            return ScreenRequest(
                Screen.GAMEPLAY,
                {"player_name": event.player_name, "level_number": event.level_number},
            )

        if isinstance(event, BossIntroDismissed):
            return ScreenRequest(
                Screen.GAMEPLAY,
                {"player_name": event.player_name, "level_number": event.level_number},
            )

        if isinstance(event, LevelCompleted):
            return ScreenRequest(
                Screen.RESULT,
                {
                    "player_name": event.player_name,
                    "level_number": event.level_number,
                    "stars": event.stars,
                    "is_new_best": event.is_new_best,
                    "correct": event.correct,
                    "total": event.total,
                    "score": event.score,
                    "best_streak": event.best_streak,
                },
            )

        if isinstance(event, ResultContinue):
            level = get_level(event.level_number)
            if level and level.level_in_world == 10 and event.stars >= 2:
                # Beat the boss! Show victory screen
                return ScreenRequest(
                    Screen.BOSS_VICTORY,
                    {
                        "player_name": event.player_name,
                        "world_number": level.world_number,
                    },
                )

            # Regular continue - back to world map
            if event.stars >= 2:
                next_level = event.level_number + 1
            else:
                next_level = event.level_number
            return ScreenRequest(
                Screen.WORLD_MAP,
                {"player_name": event.player_name, "selected_level": next_level},
            )

        if isinstance(event, ResultReplay):
            return ScreenRequest(
                Screen.GAMEPLAY,
                {"player_name": event.player_name, "level_number": event.level_number},
            )

        if isinstance(event, BossVictoryDismissed):
            next_world = get_world(event.world_number + 1)
            if next_world:
                # More worlds to explore
                return ScreenRequest(
                    Screen.WORLD_INTRO,
                    {
                        "player_name": event.player_name,
                        "world_number": event.world_number + 1,
                    },
                )
            # All worlds complete!
            return ScreenRequest(
                Screen.GAME_COMPLETE,
                {"player_name": event.player_name},
            )

        if isinstance(event, GameCompleteDismissed):
            return ScreenRequest(Screen.PLAYER_SELECT, {})

        # Unknown event - return to player select as fallback
        return ScreenRequest(Screen.PLAYER_SELECT, {})
