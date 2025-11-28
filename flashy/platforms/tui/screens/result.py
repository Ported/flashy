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
        from flashy.core.flow import ResultContinue
        from flashy.platforms.tui.base import get_app

        self.app.pop_screen()
        get_app(self).navigate(
            ResultContinue(
                player_name=self.player_name,
                level_number=self.level_number,
                stars=self.stars,
            )
        )

    def action_replay(self) -> None:
        """Replay the level."""
        from flashy.core.flow import ResultReplay
        from flashy.platforms.tui.base import get_app

        self.app.pop_screen()
        get_app(self).navigate(
            ResultReplay(player_name=self.player_name, level_number=self.level_number)
        )
