"""Shared base classes and utilities for Flashy UI screens."""

from abc import abstractmethod
from typing import TYPE_CHECKING, cast

from textual.binding import Binding
from textual.screen import Screen

if TYPE_CHECKING:
    from flashy.platforms.tui.app import FlashyApp


def get_app(screen: Screen) -> "FlashyApp":
    """Get the typed FlashyApp from a screen.

    This is a helper to provide proper typing for the app.
    """
    from flashy.platforms.tui.app import FlashyApp

    return cast(FlashyApp, screen.app)


# Common CSS for story-style screens
STORY_CSS = """
.story-box {
    width: 60;
    height: auto;
    border: double yellow;
    padding: 2;
}

.ascii-art {
    text-align: center;
    color: cyan;
}

.story-title {
    text-align: center;
    text-style: bold;
    color: cyan;
    padding: 1;
}

.story-text {
    text-align: center;
    padding: 1;
}

.continue-hint {
    text-align: center;
    color: $text-muted;
    padding-top: 1;
}
"""


class StoryScreen(Screen):
    """Base class for story/cutscene screens.

    Any key press continues to the next screen.
    Subclasses should implement action_continue().
    """

    BINDINGS = [
        Binding("enter", "continue", "Continue", show=True),
        Binding("space", "continue", "Continue"),
    ]

    def on_key(self, event) -> None:
        """Handle any key press to continue."""
        self.action_continue()

    @abstractmethod
    def action_continue(self) -> None:
        """Continue to the next screen. Subclasses must implement."""
        ...
