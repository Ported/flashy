"""World introduction screen - shown when entering a new world."""

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Footer, Header, Static

from flashy.platforms.tui.base import STORY_CSS, StoryScreen


class WorldIntroScreen(StoryScreen):
    """Screen showing world introduction story."""

    CSS = (
        STORY_CSS
        + """
    WorldIntroScreen {
        align: center middle;
    }

    .world-emoji {
        text-align: center;
        padding: 1;
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
                yield Static(
                    f"{world.theme_emoji}  {world.theme_emoji}  {world.theme_emoji}",
                    classes="world-emoji",
                )
                yield Static(world.name.upper(), classes="story-title")
                yield Static(world.intro_text, classes="story-text")
                yield Static(
                    "Press any key to continue...", classes="continue-hint"
                )
        yield Footer()

    def action_continue(self) -> None:
        """Continue to the world map."""
        from flashy.core.flow import WorldIntroDismissed
        from flashy.platforms.tui.base import get_app

        self.app.pop_screen()
        get_app(self).navigate(
            WorldIntroDismissed(self.player_name, world_number=self.world_number)
        )
