"""Game complete screen - Flashy finds home!"""

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Footer, Header, Static

from flashy.platforms.tui.base import STORY_CSS, StoryScreen


class GameCompleteScreen(StoryScreen):
    """Final screen when player completes all worlds - Flashy goes home!"""

    CSS = (
        STORY_CSS
        + """
    GameCompleteScreen {
        align: center middle;
    }

    .story-box {
        border: double magenta;
    }

    .home-emoji {
        text-align: center;
        padding: 1;
    }

    .story-title {
        color: magenta;
    }

    .congratulations {
        text-align: center;
        color: green;
        text-style: bold;
        padding: 1;
    }

    .ascii-art {
        text-align: center;
        color: yellow;
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
                yield Static("🏠  HOME AT LAST!  🏠", classes="home-emoji")
                yield Static("THE END", classes="story-title")
                # Flashy with family
                yield Static(
                    "      /\\_/\\           /\\_/\\           /\\_/\\\n"
                    "     ( ^.^ )         ( o.o )         ( o.o )\n"
                    "      > ^ <           > ^ <           > ^ <\n"
                    "     /|   |\\   ~     /|   |\\   ~     /|   |\\\n"
                    "     FLASHY           MOM             DAD",
                    classes="ascii-art",
                )
                yield Static(
                    '"FLASHY! You\'re home!"\n\n'
                    "Flashy bounded through the meadow into the arms\n"
                    "of Mom and Dad. The long journey was over.\n\n"
                    '"I climbed mountains, crossed swamps,\n'
                    "survived the desert, and ran through meadows!\n"
                    'And I made so many friends along the way!"\n\n'
                    f"Thanks to {self.player_name}, Flashy made it home safely.",
                    classes="story-text",
                )
                yield Static(
                    "Congratulations, Math Champion!",
                    classes="congratulations",
                )
                yield Static(
                    "Press any key to return to menu...", classes="continue-hint"
                )
        yield Footer()

    def action_continue(self) -> None:
        """Return to player select screen."""
        from flashy.core.flow import GameCompleteDismissed
        from flashy.platforms.tui.base import get_app

        self.app.pop_screen()
        get_app(self).navigate(GameCompleteDismissed())
