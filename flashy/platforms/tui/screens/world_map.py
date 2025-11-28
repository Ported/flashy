"""World map screen showing level progress."""

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, ListItem, ListView, Static

from flashy.history import load_progress


class WorldMapScreen(Screen):
    """World map screen showing level progress with interactive level selection."""

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]

    CSS = """
    WorldMapScreen {
        align: center middle;
    }

    #map-box {
        width: 60;
        height: auto;
        border: double cyan;
        padding: 1 2;
    }

    #world-title {
        text-align: center;
        text-style: bold;
        color: cyan;
        padding: 1;
    }

    #level-list {
        height: auto;
        max-height: 15;
        background: transparent;
        padding: 0 1;
    }

    #level-list > ListItem {
        padding: 0 1;
    }

    #level-list > ListItem:hover {
        background: $primary 20%;
    }

    #level-list > ListItem.-selected {
        background: $primary 40%;
    }

    .level-text {
        width: 100%;
    }

    .level-locked {
        color: $text-muted;
    }

    .level-playable {
        color: green;
    }

    .level-completed {
        color: white;
    }

    #player-info {
        text-align: center;
        color: $text-muted;
        padding-top: 1;
    }

    #hint {
        text-align: center;
        color: $text-muted;
        padding-top: 1;
    }

    #error-msg {
        text-align: center;
        color: $error;
        height: 1;
    }
    """

    def __init__(
        self,
        player_name: str,
        selected_level: int | None = None,
        world_number: int | None = None,
    ) -> None:
        super().__init__()
        self.player_name = player_name
        self.selected_level = selected_level  # Level to highlight on open
        # Determine world from selected_level or default to highest unlocked
        if world_number is not None:
            self.world_number = world_number
        elif selected_level is not None:
            self.world_number = (selected_level - 1) // 10 + 1
        else:
            self.world_number = self._get_current_world()

    def _get_current_world(self) -> int:
        """Determine the current world based on progress."""
        progress = load_progress(self.player_name)
        # Find highest world where level 1 is unlocked
        for world_num in range(4, 0, -1):
            first_level = (world_num - 1) * 10 + 1
            if progress.is_unlocked(first_level):
                return world_num
        return 1

    def compose(self) -> ComposeResult:
        from flashy.core.worlds import get_world

        world = get_world(self.world_number)
        if not world:
            yield Static("World not found!")
            return

        yield Header()

        with Center():
            with Vertical(id="map-box"):
                emoji = world.theme_emoji
                title = f"{emoji}  {world.name.upper()}  {emoji}"
                yield Static(title, id="world-title")
                yield Static(f"Player: {self.player_name}", id="player-info")
                yield ListView(id="level-list")
                yield Static("", id="error-msg")
                yield Static("↑↓ Select • Enter Play • Q Quit", id="hint")
        yield Footer()

    def on_mount(self) -> None:
        """Populate level list and focus on current level."""
        self._refresh_levels()

    def _refresh_levels(self) -> None:
        """Refresh the level list."""
        from flashy.core.levels import get_levels_for_world

        list_view = self.query_one("#level-list", ListView)
        list_view.clear()

        progress = load_progress(self.player_name)
        levels = get_levels_for_world(self.world_number)

        # Find current playable level in this world (for default selection)
        first_level = (self.world_number - 1) * 10 + 1
        last_level = self.world_number * 10
        current_level = first_level
        for i in range(first_level, last_level + 1):
            if progress.is_unlocked(i) and progress.get_stars(i) < 3:
                current_level = i
                break
            if progress.is_unlocked(i):
                current_level = i

        # Use selected_level if provided, otherwise use current
        focus_level = self.selected_level or current_level

        # Show levels from top (10) to bottom (1)
        focus_index = 0
        for idx, level in enumerate(reversed(levels)):
            stars = progress.get_stars(level.number)
            is_unlocked = progress.is_unlocked(level.number)

            # Build star display
            if is_unlocked:
                star_str = "⭐" * stars + "·" * (3 - stars)
            else:
                star_str = "···"

            # Determine style
            if not is_unlocked:
                style = "level-locked"
                icon = "🔒"
            elif stars < 3:
                style = "level-playable"
                icon = "▶"
            else:
                style = "level-completed"
                icon = "✓"

            lvl_num = level.level_in_world
            text = f" {icon} {star_str} [{lvl_num:2d}] {level.name}"
            if not is_unlocked:
                text += " 🔒"

            item = ListItem(
                Static(text, classes=f"level-text {style}"),
                id=f"level-{level.number}",
            )
            list_view.append(item)

            # Track which index to focus
            if level.number == focus_level:
                focus_index = idx

        # Focus the list and select the right level
        list_view.focus()
        if focus_index < len(list_view.children):
            list_view.index = focus_index

    @on(ListView.Selected)
    def level_selected(self, event: ListView.Selected) -> None:
        """Handle level selection."""
        from flashy.core.flow import LevelSelected

        item_id = event.item.id
        if not item_id or not item_id.startswith("level-"):
            return

        level_num = int(item_id[6:])  # Remove "level-" prefix
        progress = load_progress(self.player_name)

        error_msg = self.query_one("#error-msg", Static)

        if not progress.is_unlocked(level_num):
            error_msg.update("🔒 Level locked! Need 2 stars on previous level.")
            return

        # Clear error
        error_msg.update("")

        # Use GameFlow to determine where to go (gameplay, friend meet, or boss intro)
        from flashy.platforms.tui.base import get_app

        get_app(self).navigate(LevelSelected(self.player_name, level_number=level_num))

    def action_quit(self) -> None:
        """Quit to player select."""
        self.app.pop_screen()
