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

    def __init__(self, player_name: str, selected_level: int | None = None) -> None:
        super().__init__()
        self.player_name = player_name
        self.selected_level = selected_level  # Level to highlight on open

    def compose(self) -> ComposeResult:
        from flashy.worlds import WORLD_1

        yield Header()

        with Center():
            with Vertical(id="map-box"):
                yield Static(f"🏔️  {WORLD_1.name.upper()}  🏔️", id="world-title")
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
        from flashy.levels import get_levels_for_world

        list_view = self.query_one("#level-list", ListView)
        list_view.clear()

        progress = load_progress(self.player_name)
        levels = get_levels_for_world(1)

        # Find current playable level (for default selection)
        current_level = 1
        for i in range(1, 11):
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
        from flashy.levels import get_level
        from flashy.ui.screens.boss_intro import BossIntroScreen
        from flashy.ui.screens.friend_meet import FriendMeetScreen
        from flashy.ui.screens.gameplay import GameplayScreen

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

        # Get level info to check type
        level = get_level(level_num)
        if not level:
            return

        # Show story screens for special levels
        if level.level_in_world == 6:  # Friend level
            self.app.push_screen(
                FriendMeetScreen(self.player_name, level.world_number, level_num)
            )
        elif level.level_in_world == 10:  # Boss level
            self.app.push_screen(
                BossIntroScreen(self.player_name, level.world_number, level_num)
            )
        else:
            self.app.push_screen(GameplayScreen(self.player_name, level_num))

    def action_quit(self) -> None:
        """Quit to player select."""
        self.app.pop_screen()
