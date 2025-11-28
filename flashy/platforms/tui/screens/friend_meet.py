"""Friend meeting screen - shown before level 6."""

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Footer, Header, Static

from flashy.platforms.tui.base import STORY_CSS, StoryScreen

# ASCII art for friends
FRIEND_ART = {
    "Carry": (  # Owl
        '   ,___,\n   (O,O)\n   /)_)\n    ""'
    ),
    "Borrow": (  # Turtle
        "    ___\n .-'   '-.\n/  .   .  \\\n| (o) (o) |\n \\   <   /\n  '-----'"
    ),
    "Remainder": (  # Camel
        "   //\n  (o>\n //\\\\\n//  \\\\"
    ),
    "Times": (  # Rabbit
        " (\\_/)\n (O.O)\n (> <)"
    ),
}


class FriendMeetScreen(StoryScreen):
    """Screen showing friend meeting story."""

    CSS = (
        STORY_CSS
        + """
    FriendMeetScreen {
        align: center middle;
    }

    .friend-emoji {
        text-align: center;
        padding: 1;
    }
    """
    )

    def __init__(self, player_name: str, world_number: int, level_number: int) -> None:
        super().__init__()
        self.player_name = player_name
        self.world_number = world_number
        self.level_number = level_number

    def compose(self) -> ComposeResult:
        from flashy.core.worlds import get_world

        world = get_world(self.world_number)
        if not world:
            yield Static("World not found!")
            return

        yield Header()
        with Center():
            with Vertical(classes="story-box"):
                # Show friend ASCII art if available
                art = FRIEND_ART.get(world.friend_name, "")
                if art:
                    yield Static(art, classes="ascii-art")
                yield Static(
                    f"{world.friend_emoji} {world.friend_name} {world.friend_emoji}",
                    classes="friend-emoji",
                )
                yield Static(f"Meet {world.friend_name}!", classes="story-title")
                yield Static(world.friend_text, classes="story-text")
                yield Static("Press any key to continue...", classes="continue-hint")
        yield Footer()

    def action_continue(self) -> None:
        """Continue to gameplay."""
        from flashy.core.flow import FriendMeetDismissed
        from flashy.platforms.tui.base import get_app

        self.app.pop_screen()
        get_app(self).navigate(
            FriendMeetDismissed(self.player_name, level_number=self.level_number)
        )
