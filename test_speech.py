#!/usr/bin/env python3
"""Quick test utility for speech recognition."""

import signal
import sys


def main():
    """Test Vosk speech recognition."""
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))

    from flashy.platforms.tui.input_handler import VoiceInputHandler

    print("Loading Vosk model...")
    handler = VoiceInputHandler()
    print("Vosk ready! Speak numbers (Ctrl+C to stop)\n")

    try:
        while True:
            answer, raw = handler.get_answer(prompt="Say a number: ", expected=None)
            if raw == "":  # Ctrl+C pressed during recognition
                break
            print(f"  -> Parsed: {answer}, Raw: '{raw}'\n")
    except KeyboardInterrupt:
        pass

    print("\nDone!")


if __name__ == "__main__":
    main()
