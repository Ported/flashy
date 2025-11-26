"""Result screen showing level completion."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Static


class ResultScreen(Screen):
    """Screen showing level results."""

    BINDINGS = [
        Binding("enter", "continue", "Continue", show=True),
        Binding("r", "replay", "Replay", show=True),
    ]

    CSS = """
    ResultScreen {
        align: center middle;
    }

    #result-box {
        width: 50;
        height: auto;
        border: double yellow;
        padding: 2;
    }

    #result-box Static {
        text-align: center;
        padding: 1;
    }

    #title {
        text-style: bold;
    }

    #message {
        color: $text-muted;
    }

    .success {
        color: green;
    }

    .warning {
        color: yellow;
    }

    .fail {
        color: red;
    }
    """

    def __init__(
        self,
        player_name: str,
        level_number: int,
        correct: int,
        total: int,
        stars: int,
        is_new_best: bool,
        total_score: int = 0,
        best_streak: int = 0,
    ) -> None:
        super().__init__()
        self.player_name = player_name
        self.level_number = level_number
        self.correct = correct
        self.total = total
        self.stars = stars
        self.is_new_best = is_new_best
        self.total_score = total_score
        self.best_streak = best_streak

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Vertical(id="result-box"):
                if self.stars >= 2:
                    yield Static("Level Complete!", id="title", classes="success")
                else:
                    yield Static("Keep Trying!", id="title", classes="warning")

                star_display = "⭐" * self.stars + "·" * (3 - self.stars)
                yield Static(star_display, id="stars")

                if self.is_new_best:
                    yield Static("★ NEW BEST! ★", classes="success")

                yield Static(f"Correct: {self.correct}/{self.total}", id="stats")

                # Show score and streak
                score_text = f"Score: {self.total_score}"
                if self.best_streak >= 2:
                    score_text += f"  |  Best streak: {self.best_streak}"
                yield Static(score_text, id="score-stats")

                if self.stars < 2:
                    yield Static(
                        "You need 2 stars to unlock the next level.",
                        id="message",
                    )
                else:
                    yield Static(
                        "Press ENTER to continue or R to replay",
                        id="message",
                    )
        yield Footer()

    def action_continue(self) -> None:
        """Continue to map (or boss victory if applicable)."""
        from flashy.levels import get_level
        from flashy.ui.screens.boss_victory import BossVictoryScreen
        from flashy.ui.screens.world_map import WorldMapScreen

        self.app.pop_screen()

        # Check if this was a boss level with 2+ stars
        level = get_level(self.level_number)
        if level and level.level_in_world == 10 and self.stars >= 2:
            # Show boss victory screen
            self.app.push_screen(
                BossVictoryScreen(self.player_name, level.world_number)
            )
        else:
            # If passed (2+ stars), highlight next level; otherwise current level
            if self.stars >= 2:
                next_level = get_level(self.level_number + 1)
                highlight = next_level.number if next_level else self.level_number
            else:
                highlight = self.level_number
            self.app.push_screen(WorldMapScreen(self.player_name, highlight))

    def action_replay(self) -> None:
        """Replay the level."""
        from flashy.ui.screens.gameplay import GameplayScreen

        self.app.pop_screen()
        self.app.push_screen(GameplayScreen(self.player_name, self.level_number))
