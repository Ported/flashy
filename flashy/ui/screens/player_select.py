"""Player selection screen."""

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, ListItem, ListView, Static

from flashy.history import list_players, load_progress


class PlayerSelectScreen(Screen):
    """Player selection screen."""

    BINDINGS = [
        Binding("n", "new_player", "New Player", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]

    CSS = """
    PlayerSelectScreen {
        align: center middle;
    }

    #title {
        text-align: center;
        text-style: bold;
        color: cyan;
        padding: 1;
    }

    #subtitle {
        text-align: center;
        color: white;
        padding-bottom: 1;
    }

    #player-list {
        width: 50;
        height: auto;
        max-height: 15;
        border: solid green;
        padding: 1;
    }

    .player-item {
        padding: 0 1;
    }

    .player-stats {
        color: $text-muted;
        text-style: italic;
    }

    #new-player-btn {
        margin-top: 1;
    }

    #dog-art {
        text-align: center;
        color: yellow;
    }

    #welcome-box {
        width: 60;
        height: auto;
        border: double cyan;
        padding: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Vertical(id="welcome-box"):
                yield Static(
                    "    /\\_/\\\n"
                    "   ( o.o )\n"
                    "    > ^ <\n"
                    "   /|   |\\",
                    id="dog-art",
                )
                yield Static("🐕 FLASHY", id="title")
                yield Static("Math Adventure", id="subtitle")
                yield Static("Who's playing today?", id="prompt")
                yield ListView(id="player-list")
                yield Button("✨ New Player", id="new-player-btn", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        """Populate player list on mount."""
        self._refresh_players()
        # Focus list if there are players, otherwise focus the button
        players = list_players()
        if players:
            self.query_one("#player-list", ListView).focus()
        else:
            self.query_one("#new-player-btn", Button).focus()

    def _refresh_players(self) -> None:
        """Refresh the player list."""
        list_view = self.query_one("#player-list", ListView)
        list_view.clear()

        players = list_players()
        if players:
            for name in players:
                progress = load_progress(name)
                total_stars = sum(progress.stars.values())
                highest = progress.get_highest_unlocked()

                stats_text = f"  ⭐ {total_stars} stars | Level {highest}"
                item = ListItem(
                    Static(f"  {name}"),
                    Static(stats_text, classes="player-stats"),
                    id=f"player-{name}",
                )
                list_view.append(item)
        else:
            list_view.append(ListItem(Static("  No players yet!"), id="no-players"))

    @on(ListView.Selected)
    def player_selected(self, event: ListView.Selected) -> None:
        """Handle player selection."""

        item_id = event.item.id
        if item_id and item_id.startswith("player-"):
            player_name = item_id[7:]  # Remove "player-" prefix
            self._start_game(player_name)

    @on(Button.Pressed, "#new-player-btn")
    def new_player_pressed(self) -> None:
        """Handle new player button press."""
        from flashy.ui.screens.new_player import NewPlayerScreen

        self.app.push_screen(NewPlayerScreen())

    def action_new_player(self) -> None:
        """Action to create new player."""
        from flashy.ui.screens.new_player import NewPlayerScreen

        self.app.push_screen(NewPlayerScreen())

    def action_quit(self) -> None:
        """Quit the app."""
        self.app.exit()

    def _start_game(self, player_name: str) -> None:
        """Start the game with selected player."""
        from flashy.ui.screens.intro import IntroScreen
        from flashy.ui.screens.world_map import WorldMapScreen

        # Load progress and check if new player
        progress = load_progress(player_name)
        if not progress.stars:
            # New player - show intro
            self.app.push_screen(IntroScreen(player_name))
        else:
            # Returning player - go to map
            self.app.push_screen(WorldMapScreen(player_name))
