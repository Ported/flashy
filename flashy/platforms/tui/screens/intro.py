"""Introduction screen for new players."""

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Footer, Header, Static

from flashy.platforms.tui.base import STORY_CSS, StoryScreen


class IntroScreen(StoryScreen):
    """Introduction screen for new players."""

    CSS = (
        STORY_CSS
        + """
    IntroScreen {
        align: center middle;
    }
    """
    )

    def __init__(self, player_name: str) -> None:
        super().__init__()
        self.player_name = player_name

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Vertical(classes="story-box"):
                yield Static(
                    " /\\_/\\\n ( o.o )\n > ^ <\n /|   |\\",
                    classes="ascii-art",
                )
                yield Static("FLASHY", classes="story-title")
                yield Static(
                    '"Oh no! Where am I?"\n\n'
                    '"I chased that butterfly too far..."\n\n'
                    '"I need to find my way home!"',
                    classes="story-text",
                )
                yield Static(
                    "Press any key to begin your journey...", classes="continue-hint"
                )
        yield Footer()

    def action_continue(self) -> None:
        """Continue to the world intro."""
        from flashy.core.flow import IntroDismissed
        from flashy.platforms.tui.base import get_app

        self.app.pop_screen()
        get_app(self).navigate(IntroDismissed(self.player_name))
