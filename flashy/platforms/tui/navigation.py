"""Navigation module - bridges GameFlow to TUI screens.

This module maps the platform-independent Screen enum and ScreenRequest
to actual Textual screen instances.
"""

from textual.screen import Screen as TextualScreen

from flashy.core.flow import Screen, ScreenRequest


def create_screen(request: ScreenRequest) -> TextualScreen:
    """Create a TUI screen from a ScreenRequest.

    Args:
        request: The screen request from GameFlow.

    Returns:
        A Textual screen instance.
    """
    # Import screens here to avoid circular imports
    from flashy.platforms.tui.screens.boss_intro import BossIntroScreen
    from flashy.platforms.tui.screens.boss_victory import BossVictoryScreen
    from flashy.platforms.tui.screens.friend_meet import FriendMeetScreen
    from flashy.platforms.tui.screens.game_complete import GameCompleteScreen
    from flashy.platforms.tui.screens.gameplay import GameplayScreen
    from flashy.platforms.tui.screens.intro import IntroScreen
    from flashy.platforms.tui.screens.new_player import NewPlayerScreen
    from flashy.platforms.tui.screens.player_select import PlayerSelectScreen
    from flashy.platforms.tui.screens.result import ResultScreen
    from flashy.platforms.tui.screens.world_intro import WorldIntroScreen
    from flashy.platforms.tui.screens.world_map import WorldMapScreen

    params = request.params

    match request.screen:
        case Screen.PLAYER_SELECT:
            return PlayerSelectScreen()

        case Screen.NEW_PLAYER:
            return NewPlayerScreen()

        case Screen.INTRO:
            return IntroScreen(params["player_name"])

        case Screen.WORLD_INTRO:
            return WorldIntroScreen(
                params["player_name"],
                params["world_number"],
            )

        case Screen.WORLD_MAP:
            return WorldMapScreen(
                params["player_name"],
                selected_level=params.get("selected_level"),
                world_number=params.get("world_number"),
            )

        case Screen.FRIEND_MEET:
            return FriendMeetScreen(
                params["player_name"],
                params["world_number"],
                params["level_number"],
            )

        case Screen.BOSS_INTRO:
            return BossIntroScreen(
                params["player_name"],
                params["world_number"],
                params["level_number"],
            )

        case Screen.GAMEPLAY:
            return GameplayScreen(
                params["player_name"],
                params["level_number"],
            )

        case Screen.RESULT:
            return ResultScreen(
                player_name=params["player_name"],
                level_number=params["level_number"],
                correct=params["correct"],
                total=params["total"],
                stars=params["stars"],
                is_new_best=params["is_new_best"],
                total_score=params.get("score", 0),
                best_streak=params.get("best_streak", 0),
            )

        case Screen.BOSS_VICTORY:
            return BossVictoryScreen(
                params["player_name"],
                params["world_number"],
            )

        case Screen.GAME_COMPLETE:
            return GameCompleteScreen(params.get("player_name", ""))

        case _:
            # Fallback to player select
            return PlayerSelectScreen()
