"""New player creation screen."""

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Static

from flashy.history import PlayerProgress, player_exists, save_progress


class NewPlayerScreen(Screen):
    """Screen for creating a new player."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    CSS = """
    NewPlayerScreen {
        align: center middle;
    }

    #new-player-box {
        width: 50;
        height: auto;
        border: double green;
        padding: 2;
    }

    #title {
        text-align: center;
        text-style: bold;
        color: green;
        padding-bottom: 1;
    }

    #name-input {
        margin: 1 0;
    }

    #error-msg {
        color: red;
        text-align: center;
        height: 1;
    }

    #buttons {
        margin-top: 1;
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Vertical(id="new-player-box"):
                yield Static("✨ New Player", id="title")
                yield Static("What's your name?")
                yield Input(placeholder="Enter your name...", id="name-input")
                yield Static("", id="error-msg")
                with Horizontal(id="buttons"):
                    yield Button("Create", id="create-btn", variant="success")
                    yield Button("Cancel", id="cancel-btn", variant="error")
        yield Footer()

    def on_mount(self) -> None:
        """Focus the input on mount."""
        self.query_one("#name-input", Input).focus()

    @on(Button.Pressed, "#create-btn")
    def create_pressed(self) -> None:
        """Handle create button press."""
        self._try_create()

    @on(Button.Pressed, "#cancel-btn")
    def cancel_pressed(self) -> None:
        """Handle cancel button press."""
        self.app.pop_screen()

    @on(Input.Submitted)
    def input_submitted(self) -> None:
        """Handle enter press in input."""
        self._try_create()

    def action_cancel(self) -> None:
        """Cancel and go back."""
        self.app.pop_screen()

    def _try_create(self) -> None:
        """Try to create the player."""
        from flashy.ui.screens.intro import IntroScreen

        name_input = self.query_one("#name-input", Input)
        error_label = self.query_one("#error-msg", Static)
        name = name_input.value.strip()

        if not name:
            error_label.update("Please enter a name")
            return

        # Sanitize name
        safe_name = "".join(c for c in name if c.isalnum() or c in " -_").strip()
        if not safe_name:
            error_label.update("Please use letters and numbers only")
            return

        if player_exists(safe_name):
            error_label.update(f"'{safe_name}' already exists!")
            return

        # Create player
        save_progress(safe_name, PlayerProgress())

        # Go back and refresh, then start intro
        self.app.pop_screen()
        self.app.push_screen(IntroScreen(safe_name))
