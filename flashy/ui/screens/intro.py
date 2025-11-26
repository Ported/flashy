"""Introduction screen for new players."""

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Footer, Header, Static

from flashy.ui.base import STORY_CSS, StoryScreen


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
                    " /\\_/\\\n"
                    " ( o.o )\n"
                    " > ^ <\n"
                    " /|   |\\",
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
        from flashy.ui.screens.world_intro import WorldIntroScreen

        self.app.pop_screen()
        # Show world intro before the map
        self.app.push_screen(WorldIntroScreen(self.player_name, world_number=1))
