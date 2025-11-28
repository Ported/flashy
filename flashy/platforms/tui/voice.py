"""Voice input widget for Textual - wraps existing VoiceInputHandler."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.message import Message
from textual.widget import Widget
from textual.widgets import Static

if TYPE_CHECKING:
    from textual.app import App


class VoiceInput(Widget):
    """Widget that wraps VoiceInputHandler for use in Textual."""

    DEFAULT_CSS = """
    VoiceInput {
        height: auto;
    }

    VoiceInput #voice-status {
        text-align: center;
        color: $text-muted;
    }

    VoiceInput #voice-partial {
        text-align: center;
        color: cyan;
        text-style: italic;
        height: 1;
    }

    VoiceInput .listening {
        color: green;
    }
    """

    class AnswerReceived(Message):
        """Sent when voice input receives a valid answer."""

        def __init__(self, answer: int | None, raw_text: str) -> None:
            super().__init__()
            self.answer = answer
            self.raw_text = raw_text

    def __init__(self, expected: int | None = None, id: str | None = None) -> None:  # noqa: A002
        super().__init__(id=id)
        self.expected = expected
        self._handler = None
        self._listening = False
        self._app_ref: App | None = None

    def compose(self):
        yield Static("🎤 Initializing...", id="voice-status")
        yield Static("", id="voice-partial")

    def on_mount(self) -> None:
        """Initialize and start listening."""
        self._app_ref = self.app
        self.run_worker(self._init_and_listen, thread=True)

    def _call_ui(self, callback, *args) -> None:
        """Call a UI method from worker thread."""
        if self._app_ref:
            self._app_ref.call_from_thread(callback, *args)

    def _init_and_listen(self) -> None:
        """Initialize handler and get one answer (runs in worker thread)."""
        try:
            from flashy.platforms.tui.input_handler import VoiceInputHandler

            self._call_ui(self._set_status, "🎤 Loading model...")
            self._handler = VoiceInputHandler()

            self._listening = True
            self._call_ui(self._set_status, "🎤 Listening...")
            self._call_ui(self._set_listening_style, True)

            def on_partial(text: str) -> None:
                """Update partial text display from worker thread."""
                self._call_ui(self._set_partial, text)

            # Get one answer using existing handler
            answer, raw_text = self._handler.get_answer(
                prompt="", expected=self.expected, on_partial=on_partial
            )

            self._listening = False
            self._call_ui(self.post_message, self.AnswerReceived(answer, raw_text))

        except Exception as e:
            self._call_ui(self._set_status, f"Voice error: {e}")

    def _set_status(self, text: str) -> None:
        """Update status label."""
        try:
            self.query_one("#voice-status", Static).update(text)
        except Exception:
            pass

    def _set_listening_style(self, listening: bool) -> None:
        """Update listening style."""
        try:
            status = self.query_one("#voice-status", Static)
            if listening:
                status.add_class("listening")
            else:
                status.remove_class("listening")
        except Exception:
            pass

    def _set_partial(self, text: str) -> None:
        """Update partial recognition text."""
        try:
            partial = self.query_one("#voice-partial", Static)
            partial.update(f'"{text}"' if text else "")
        except Exception:
            pass

    def stop(self) -> None:
        """Stop listening."""
        self._listening = False
