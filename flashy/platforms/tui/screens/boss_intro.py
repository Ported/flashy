"""Boss introduction screen - shown before level 10."""

from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Footer, Header, Static

from flashy.platforms.tui.base import STORY_CSS, StoryScreen

# ASCII art for bosses
BOSS_ART = {
    "Summit": (  # Mountain Goat
        "    /|\n   / |\n  /  |--\\\n /  (o  o)\n/____\\__/"
    ),
    "Minus": (  # Frog King
        '  @..@\n (----)\n( >__< )\n ^^^"^^^'
    ),
    "The Sphinx of Splits": (  # Sphinx
        "    /\\  /\\\n   /  \\/  \\\n  | (o)(o) |\n   \\  --  /\n    \\____/"
    ),
    "Countess Calculata": (  # Fox
        "  /\\   /\\\n /  \\_/  \\\n | (o o) |\n  \\  ^  /\n   \\___/"
    ),
}


class BossIntroScreen(StoryScreen):
    """Screen showing boss introduction challenge."""

    CSS = (
        STORY_CSS
        + """
    BossIntroScreen {
        align: center middle;
    }

    .story-box {
        border: double red;
    }

    .boss-emoji {
        text-align: center;
        color: red;
        padding: 1;
    }

    .story-title {
        color: red;
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
                yield Static("⚔️  BOSS BATTLE  ⚔️", classes="boss-emoji")
                # Show boss ASCII art if available
                art = BOSS_ART.get(world.boss_name, "")
                if art:
                    yield Static(art, classes="ascii-art")
                yield Static(
                    f"{world.boss_emoji} {world.boss_name} {world.boss_emoji}",
                    classes="boss-emoji",
                )
                yield Static(world.boss_intro, classes="story-text")
                yield Static(
                    "Press any key to begin the battle...", classes="continue-hint"
                )
        yield Footer()

    def action_continue(self) -> None:
        """Continue to boss battle."""
        from flashy.core.flow import BossIntroDismissed
        from flashy.platforms.tui.base import get_app

        self.app.pop_screen()
        get_app(self).navigate(
            BossIntroDismissed(self.player_name, level_number=self.level_number)
        )
