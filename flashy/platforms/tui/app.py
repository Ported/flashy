"""Main Textual application for Flashy."""

from textual.app import App
from textual.binding import Binding

from flashy.core.flow import AppStarted, GameEvent, GameFlow
from flashy.core.models import PlayerProgress
from flashy.platforms.tui.navigation import create_screen


class FlashyApp(App):
    """Main Flashy application."""

    TITLE = "Flashy - Math Adventure"
    CSS_PATH = "styles.tcss"

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.player_name: str | None = None
        self._flow = GameFlow()

    def on_mount(self) -> None:
        """Called when app is mounted."""
        self.navigate(AppStarted())

    def set_player(self, name: str) -> None:
        """Set the current player."""
        self.player_name = name

    def navigate(
        self, event: GameEvent, progress: PlayerProgress | None = None
    ) -> None:
        """Handle a game event and navigate to the appropriate screen.

        Args:
            event: The game event that occurred.
            progress: Optional player progress for context-dependent navigation.
        """
        request = self._flow.handle(event, progress)
        screen = create_screen(request)
        self.push_screen(screen)


def run_app() -> None:
    """Run the Flashy TUI application."""
    app = FlashyApp()
    app.run()
