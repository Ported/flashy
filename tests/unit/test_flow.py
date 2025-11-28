"""Tests for game flow state machine."""

from flashy.core.flow import (
    AppStarted,
    BossIntroDismissed,
    BossVictoryDismissed,
    FriendMeetDismissed,
    GameCompleteDismissed,
    GameFlow,
    IntroDismissed,
    LevelCompleted,
    LevelSelected,
    NewPlayerCreated,
    PlayerSelected,
    ResultContinue,
    ResultReplay,
    Screen,
    WorldIntroDismissed,
)
from flashy.core.models import PlayerProgress


class TestGameFlow:
    """Tests for GameFlow state machine."""

    def setup_method(self) -> None:
        self.flow = GameFlow()

    def test_app_started_goes_to_player_select(self) -> None:
        result = self.flow.handle(AppStarted())
        assert result.screen == Screen.PLAYER_SELECT

    def test_new_player_selected_goes_to_new_player(self) -> None:
        result = self.flow.handle(PlayerSelected("test", is_new_player=True))
        assert result.screen == Screen.NEW_PLAYER

    def test_existing_player_no_progress_goes_to_intro(self) -> None:
        progress = PlayerProgress()  # No stars
        result = self.flow.handle(PlayerSelected("test", is_new_player=False), progress)
        assert result.screen == Screen.INTRO
        assert result.params["player_name"] == "test"

    def test_existing_player_with_progress_goes_to_world_map(self) -> None:
        progress = PlayerProgress(stars={1: 3, 2: 2})  # Has played
        result = self.flow.handle(PlayerSelected("test", is_new_player=False), progress)
        assert result.screen == Screen.WORLD_MAP
        assert result.params["player_name"] == "test"

    def test_new_player_created_goes_to_intro(self) -> None:
        result = self.flow.handle(NewPlayerCreated("newbie"))
        assert result.screen == Screen.INTRO
        assert result.params["player_name"] == "newbie"

    def test_intro_dismissed_goes_to_world_intro(self) -> None:
        result = self.flow.handle(IntroDismissed("test"))
        assert result.screen == Screen.WORLD_INTRO
        assert result.params["world_number"] == 1

    def test_world_intro_dismissed_goes_to_world_map(self) -> None:
        result = self.flow.handle(WorldIntroDismissed("test", world_number=2))
        assert result.screen == Screen.WORLD_MAP
        assert result.params["world_number"] == 2


class TestLevelSelection:
    """Tests for level selection flow."""

    def setup_method(self) -> None:
        self.flow = GameFlow()

    def test_regular_level_goes_to_gameplay(self) -> None:
        result = self.flow.handle(LevelSelected("test", level_number=1))
        assert result.screen == Screen.GAMEPLAY
        assert result.params["level_number"] == 1

    def test_level_6_goes_to_friend_meet(self) -> None:
        result = self.flow.handle(LevelSelected("test", level_number=6))
        assert result.screen == Screen.FRIEND_MEET
        assert result.params["level_number"] == 6
        assert result.params["world_number"] == 1

    def test_level_16_goes_to_friend_meet(self) -> None:
        """Level 16 is level 6 of world 2."""
        result = self.flow.handle(LevelSelected("test", level_number=16))
        assert result.screen == Screen.FRIEND_MEET
        assert result.params["level_number"] == 16
        assert result.params["world_number"] == 2

    def test_level_10_goes_to_boss_intro(self) -> None:
        result = self.flow.handle(LevelSelected("test", level_number=10))
        assert result.screen == Screen.BOSS_INTRO
        assert result.params["level_number"] == 10

    def test_friend_meet_dismissed_goes_to_gameplay(self) -> None:
        result = self.flow.handle(FriendMeetDismissed("test", level_number=6))
        assert result.screen == Screen.GAMEPLAY
        assert result.params["level_number"] == 6

    def test_boss_intro_dismissed_goes_to_gameplay(self) -> None:
        result = self.flow.handle(BossIntroDismissed("test", level_number=10))
        assert result.screen == Screen.GAMEPLAY
        assert result.params["level_number"] == 10


class TestLevelCompletion:
    """Tests for level completion flow."""

    def setup_method(self) -> None:
        self.flow = GameFlow()

    def test_level_completed_goes_to_result(self) -> None:
        result = self.flow.handle(
            LevelCompleted(
                player_name="test",
                level_number=1,
                stars=3,
                is_new_best=True,
                correct=10,
                total=10,
                score=1000,
                best_streak=10,
            )
        )
        assert result.screen == Screen.RESULT
        assert result.params["stars"] == 3
        assert result.params["score"] == 1000

    def test_result_continue_regular_goes_to_world_map(self) -> None:
        result = self.flow.handle(
            ResultContinue(player_name="test", level_number=5, stars=2)
        )
        assert result.screen == Screen.WORLD_MAP
        assert result.params["selected_level"] == 6  # Next level

    def test_result_continue_failed_stays_on_same_level(self) -> None:
        result = self.flow.handle(
            ResultContinue(player_name="test", level_number=5, stars=1)
        )
        assert result.screen == Screen.WORLD_MAP
        assert result.params["selected_level"] == 5  # Same level

    def test_result_continue_boss_victory_goes_to_boss_victory(self) -> None:
        result = self.flow.handle(
            ResultContinue(player_name="test", level_number=10, stars=3)
        )
        assert result.screen == Screen.BOSS_VICTORY
        assert result.params["world_number"] == 1

    def test_result_continue_boss_failed_goes_to_world_map(self) -> None:
        result = self.flow.handle(
            ResultContinue(player_name="test", level_number=10, stars=1)
        )
        assert result.screen == Screen.WORLD_MAP

    def test_result_replay_goes_to_gameplay(self) -> None:
        result = self.flow.handle(ResultReplay(player_name="test", level_number=5))
        assert result.screen == Screen.GAMEPLAY
        assert result.params["level_number"] == 5


class TestBossVictoryAndGameComplete:
    """Tests for boss victory and game completion flow."""

    def setup_method(self) -> None:
        self.flow = GameFlow()

    def test_boss_victory_world_1_goes_to_world_2_intro(self) -> None:
        result = self.flow.handle(
            BossVictoryDismissed(player_name="test", world_number=1)
        )
        assert result.screen == Screen.WORLD_INTRO
        assert result.params["world_number"] == 2

    def test_boss_victory_world_3_goes_to_world_4_intro(self) -> None:
        result = self.flow.handle(
            BossVictoryDismissed(player_name="test", world_number=3)
        )
        assert result.screen == Screen.WORLD_INTRO
        assert result.params["world_number"] == 4

    def test_boss_victory_final_world_goes_to_game_complete(self) -> None:
        result = self.flow.handle(
            BossVictoryDismissed(player_name="test", world_number=4)
        )
        assert result.screen == Screen.GAME_COMPLETE

    def test_game_complete_dismissed_goes_to_player_select(self) -> None:
        result = self.flow.handle(GameCompleteDismissed())
        assert result.screen == Screen.PLAYER_SELECT
