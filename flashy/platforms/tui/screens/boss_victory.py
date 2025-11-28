"""Boss victory screen - shown after defeating a boss."""

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Footer, Header, Static

from flashy.platforms.tui.base import STORY_CSS, StoryScreen


class BossVictoryScreen(StoryScreen):
    """Screen showing boss defeat celebration."""

    CSS = (
        STORY_CSS
        + """
    BossVictoryScreen {
        align: center middle;
    }

    .story-box {
        border: double green;
    }

    .victory-emoji {
        text-align: center;
        color: green;
        padding: 1;
    }

    .story-title {
        color: green;
    }
    """
    )

    def __init__(self, player_name: str, world_number: int) -> None:
        super().__init__()
        self.player_name = player_name
        self.world_number = world_number

    def compose(self) -> ComposeResult:
        from flashy.core.worlds import get_world

        world = get_world(self.world_number)
        if not world:
            yield Static("World not found!")
            return

        yield Header()
        with Center():
            with Vertical(classes="story-box"):
                yield Static("🎉  VICTORY!  🎉", classes="victory-emoji")
                yield Static(
                    f"You defeated {world.boss_name}!", classes="story-title"
                )
                yield Static(
                    "    /\\_/\\\n"
                    "   ( ^.^ )\n"
                    "    > ^ <\n"
                    "   /|   |\\",
                    classes="ascii-art",
                )
                yield Static(world.boss_defeat, classes="story-text")
                yield Static(
                    "Press any key to continue...", classes="continue-hint"
                )
        yield Footer()

    def action_continue(self) -> None:
        """Continue to next world intro or game complete."""
        from flashy.core.flow import BossVictoryDismissed
        from flashy.platforms.tui.base import get_app

        self.app.pop_screen()
        get_app(self).navigate(
            BossVictoryDismissed(
                player_name=self.player_name,
                world_number=self.world_number,
            )
        )
