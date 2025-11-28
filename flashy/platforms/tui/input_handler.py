"""Input handling - abstraction for text and voice input."""

from __future__ import annotations

import json
import queue
import sys
import urllib.request
import zipfile
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

from flashy.core.number_parser import is_fuzzy_match, is_give_up, parse_spoken_number
from flashy.history import log_speech_recognition

if TYPE_CHECKING:
    pass

SAMPLE_RATE = 16000
VOSK_MODEL_NAME = "vosk-model-en-us-0.22-lgraph"
VOSK_MODEL_URL = f"https://alphacephei.com/vosk/models/{VOSK_MODEL_NAME}.zip"

# Grammar constraint - only recognize number words for better accuracy
NUMBER_WORDS = json.dumps([
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety", "hundred", "and",
    "free",  # often misheard as "three"
    "minus", "negative",  # for negative numbers
    "skip", "give up", "pass", "next",
    "[unk]",
])


class InputHandler(Protocol):
    """Protocol for getting answers from the user."""

    def get_answer(
        self, prompt: str = "> ", expected: int | None = None
    ) -> tuple[int | None, str]:
        """Get an answer from the user.

        Args:
            prompt: The prompt to display
            expected: Optional expected answer for real-time matching (voice only)

        Returns:
            Tuple of (parsed_answer, raw_input)
            parsed_answer is None if input couldn't be parsed or user gave up
        """
        ...


class TextInputHandler:
    """Read answers from stdin."""

    def get_answer(
        self, prompt: str = "> ", expected: int | None = None  # noqa: ARG002
    ) -> tuple[int | None, str]:
        """Get an answer from stdin.

        Args:
            prompt: The prompt to display
            expected: Ignored for text input

        Returns:
            Tuple of (parsed_answer, raw_input)
        """
        try:
            raw = input(prompt)
        except EOFError:
            return None, ""

        raw = raw.strip()

        # Check for give up
        if is_give_up(raw):
            return None, raw

        try:
            answer = int(raw)
            return answer, raw
        except ValueError:
            return None, raw


def _get_vosk_model_path() -> Path:
    """Get the path to the Vosk model directory."""
    return Path.home() / ".flashy" / "models" / VOSK_MODEL_NAME


def _ensure_vosk_model() -> Path:
    """Download the Vosk model if not present."""
    model_path = _get_vosk_model_path()

    if model_path.exists():
        return model_path

    model_path.parent.mkdir(parents=True, exist_ok=True)
    zip_path = model_path.parent / "model.zip"

    print("Downloading Vosk speech model...")
    urllib.request.urlretrieve(VOSK_MODEL_URL, zip_path)

    print("Extracting model...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(model_path.parent)

    zip_path.unlink()
    print("Model ready!\n")
    return model_path


class VoiceInputHandler:
    """Get answers via voice using Vosk speech recognition."""

    def __init__(self) -> None:
        """Initialize the voice input handler."""
        # Import here to make vosk optional
        import sounddevice as sd  # noqa: F401 - verify it's available
        from vosk import Model, SetLogLevel

        SetLogLevel(-1)  # Suppress Vosk logs

        model_path = _ensure_vosk_model()
        self._model = Model(str(model_path))

    def get_answer(
        self,
        prompt: str = "> ",
        expected: int | None = None,
        on_partial: Callable[[str], None] | None = None,
    ) -> tuple[int | None, str]:
        """Get an answer via voice recognition.

        Streams audio and checks for matches in real-time.
        Returns immediately when:
        - The expected answer is recognized (if expected is provided)
        - A give-up phrase is recognized
        - User presses Ctrl+C

        Args:
            prompt: The prompt to display (shown before listening)
            expected: Expected answer for instant matching
            on_partial: Optional callback for partial recognition updates

        Returns:
            Tuple of (parsed_answer, raw_transcript)
        """
        import sounddevice as sd
        from vosk import KaldiRecognizer

        # Use grammar constraint if model supports it (lgraph models do)
        # Models without lgraph don't support grammar constraints
        if "lgraph" in VOSK_MODEL_NAME or "small" in VOSK_MODEL_NAME:
            recognizer = KaldiRecognizer(self._model, SAMPLE_RATE, NUMBER_WORDS)
        else:
            recognizer = KaldiRecognizer(self._model, SAMPLE_RATE)

        q: queue.Queue[bytes] = queue.Queue()

        def audio_callback(
            indata: bytes, frames: int, time: object, status: object  # noqa: ARG001
        ) -> None:
            if status:
                print(f"Audio status: {status}", file=sys.stderr)
            q.put(bytes(indata))

        last_partial = ""

        def update_display(text: str) -> None:
            """Update the display with current partial/final text."""
            nonlocal last_partial
            if on_partial:
                # Use callback for TUI mode
                on_partial(text)
            else:
                # Terminal mode - update in place
                clear_len = len(prompt) + len(last_partial) + 5
                print("\r" + " " * clear_len + "\r", end="", flush=True)
                print(f"{prompt}{text}", end="", flush=True)
            last_partial = text

        if not on_partial:
            print(prompt, end="", flush=True)

        try:
            with sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=4000,  # Smaller blocks for faster response
                dtype="int16",
                channels=1,
                callback=audio_callback,
            ):
                while True:
                    data = q.get()

                    if recognizer.AcceptWaveform(data):
                        # Final result
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "")

                        if text:
                            # Show final result
                            update_display(text)
                            if not on_partial:
                                print()  # Newline after final

                            # Check for give up
                            if is_give_up(text):
                                return None, text

                            # Parse number
                            number = parse_spoken_number(text)
                            if number is not None:
                                matched = expected is None or is_fuzzy_match(
                                    number, expected
                                )
                                log_speech_recognition(text, number, expected, matched)
                                return number, text

                            # Reset for next attempt
                            last_partial = ""
                            if not on_partial:
                                print(prompt, end="", flush=True)
                    else:
                        # Partial result - show what we're hearing
                        partial = json.loads(recognizer.PartialResult())
                        text = partial.get("partial", "")

                        if text and text != last_partial:
                            update_display(text)

                            # Check for early match with expected (fuzzy matching)
                            if expected is not None:
                                number = parse_spoken_number(text)
                                matched = is_fuzzy_match(number, expected)
                                log_speech_recognition(text, number, expected, matched)
                                if matched:
                                    if not on_partial:
                                        print()  # Newline after partial
                                    return number, text

                            # Check for give up in partial
                            if is_give_up(text):
                                if not on_partial:
                                    print()  # Newline after partial
                                return None, text

        except KeyboardInterrupt:
            if not on_partial:
                print("\n")
            return None, ""
