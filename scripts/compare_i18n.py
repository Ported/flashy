#!/usr/bin/env python3
"""Compare Python i18n.py strings with Flutter ARB files.

Checks that:
1. All Python keys have corresponding Flutter ARB entries
2. The English values match between Python and Flutter
3. The Swedish values match between Python and Flutter
"""

import json
import sys
from pathlib import Path

# Map Python keys to Flutter ARB keys
KEY_MAPPING = {
    "app.title": "appTitle",
    "app.tagline": "appTagline",
    "loading.pyodide": "loadingPyodide",
    "loading.python": "loadingPython",
    "loading.speech": "loadingSpeech",
    "loading.ready": "loadingReady",
    "player.who_playing": "playerWhoPlaying",
    "player.no_players": "playerNoPlayers",
    "player.new_player": "playerNewPlayer",
    "player.level": "playerLevel",
    "player.new_title": "playerNewTitle",
    "player.enter_name": "playerEnterName",
    "player.create": "playerCreate",
    "player.cancel": "playerCancel",
    "player.error_empty": "playerErrorEmpty",
    "player.error_invalid": "playerErrorInvalid",
    "player.error_exists": "playerErrorExists",
    "player.error_too_long": "playerErrorTooLong",
    "player.error_taken": "playerErrorTaken",
    "player.error_registration": "playerErrorRegistration",
    "player.error_connection": "playerErrorConnection",
    "player.registering": "playerRegistering",
    "nav.back": "navBack",
    "nav.continue": "navContinue",
    "nav.replay": "navReplay",
    "gameplay.score": "gameplayScore",
    "gameplay.type_answer": "gameplayTypeAnswer",
    "gameplay.listening": "gameplayListening",
    "gameplay.mic_request": "gameplayMicRequest",
    "gameplay.correct": "gameplayCorrect",
    "gameplay.wrong": "gameplayWrong",
    "gameplay.enter": "gameplayEnter",
    "result.complete": "resultComplete",
    "result.failed": "resultFailed",
    "result.new_best": "resultNewBest",
    "result.correct": "resultCorrect",
    "result.score": "resultScore",
    "result.time": "resultTime",
    "result.updating": "resultUpdating",
    "leaderboard.title": "leaderboardTitle",
    "victory.title": "victoryTitle",
    "game_complete.title": "gameCompleteTitle",
    "game_complete.hint": "gameCompleteHint",
    "game_complete.story": "gameCompleteStory",
    "intro.flashy": "introFlashy",
    "intro.story": "introStory",
    "intro.hint": "introHint",
    "input.voice": "inputVoice",
    "input.keyboard": "inputKeyboard",
    "world.1.name": "world1Name",
    "world.2.name": "world2Name",
    "world.3.name": "world3Name",
    "world.4.name": "world4Name",
    "world.1.intro": "world1Intro",
    "world.2.intro": "world2Intro",
    "world.3.intro": "world3Intro",
    "world.4.intro": "world4Intro",
    "world.1.friend_name": "world1FriendName",
    "world.1.friend_intro": "world1FriendIntro",
    "world.2.friend_name": "world2FriendName",
    "world.2.friend_intro": "world2FriendIntro",
    "world.3.friend_name": "world3FriendName",
    "world.3.friend_intro": "world3FriendIntro",
    "world.4.friend_name": "world4FriendName",
    "world.4.friend_intro": "world4FriendIntro",
    "world.1.boss_name": "world1BossName",
    "world.1.boss_intro": "world1BossIntro",
    "world.1.boss_defeat": "world1BossDefeat",
    "world.2.boss_name": "world2BossName",
    "world.2.boss_intro": "world2BossIntro",
    "world.2.boss_defeat": "world2BossDefeat",
    "world.3.boss_name": "world3BossName",
    "world.3.boss_intro": "world3BossIntro",
    "world.3.boss_defeat": "world3BossDefeat",
    "world.4.boss_name": "world4BossName",
    "world.4.boss_intro": "world4BossIntro",
    "world.4.boss_defeat": "world4BossDefeat",
}

# Add level names
for i in range(1, 41):
    KEY_MAPPING[f"level.{i}.name"] = f"level{i}Name"


def load_python_translations():
    """Load translations from Python i18n.py."""
    # Import the Python module
    sys.path.insert(0, str(Path(__file__).parent.parent / "flashy" / "core"))
    from i18n import TRANSLATIONS
    return TRANSLATIONS


def load_flutter_arb(lang: str):
    """Load translations from Flutter ARB file."""
    arb_path = Path(__file__).parent.parent / "flutter" / "lib" / "l10n" / f"app_{lang}.arb"
    with open(arb_path) as f:
        return json.load(f)


def normalize_string(s: str) -> str:
    """Normalize string for comparison (handle different quote styles, etc)."""
    # Normalize newlines
    s = s.replace("\\n", "\n")
    # Strip whitespace
    return s.strip()


def compare_translations():
    """Compare Python and Flutter translations."""
    print("=" * 60)
    print("I18N Comparison: Python i18n.py vs Flutter ARB files")
    print("=" * 60)

    py_trans = load_python_translations()
    flutter_en = load_flutter_arb("en")
    flutter_sv = load_flutter_arb("sv")

    errors = []
    warnings = []

    # Check each Python key
    for py_key, flutter_key in KEY_MAPPING.items():
        # Check English
        py_en = py_trans["en"].get(py_key)
        fl_en = flutter_en.get(flutter_key)

        if py_en is None:
            warnings.append(f"Python missing key: {py_key}")
            continue

        if fl_en is None:
            errors.append(f"Flutter EN missing key: {flutter_key} (Python: {py_key})")
            continue

        # Compare values
        py_en_norm = normalize_string(py_en)
        fl_en_norm = normalize_string(fl_en)

        if py_en_norm != fl_en_norm:
            errors.append(
                f"EN mismatch for {flutter_key}:\n"
                f"  Python: {repr(py_en_norm)}\n"
                f"  Flutter: {repr(fl_en_norm)}"
            )

        # Check Swedish
        py_sv = py_trans["sv"].get(py_key)
        fl_sv = flutter_sv.get(flutter_key)

        if py_sv is None:
            warnings.append(f"Python SV missing key: {py_key}")
            continue

        if fl_sv is None:
            errors.append(f"Flutter SV missing key: {flutter_key} (Python: {py_key})")
            continue

        py_sv_norm = normalize_string(py_sv)
        fl_sv_norm = normalize_string(fl_sv)

        if py_sv_norm != fl_sv_norm:
            errors.append(
                f"SV mismatch for {flutter_key}:\n"
                f"  Python: {repr(py_sv_norm)}\n"
                f"  Flutter: {repr(fl_sv_norm)}"
            )

    # Check for Flutter keys not in Python
    flutter_keys = set(k for k in flutter_en.keys() if not k.startswith("@"))
    mapped_flutter_keys = set(KEY_MAPPING.values())
    extra_flutter = flutter_keys - mapped_flutter_keys

    if extra_flutter:
        for key in sorted(extra_flutter):
            # Skip metadata keys
            if key.startswith("@@"):
                continue
            warnings.append(f"Flutter has extra key not in Python: {key}")

    # Print results
    print(f"\nChecked {len(KEY_MAPPING)} key mappings\n")

    if warnings:
        print("WARNINGS:")
        print("-" * 40)
        for w in warnings:
            print(f"  {w}")
        print()

    if errors:
        print("ERRORS:")
        print("-" * 40)
        for e in errors:
            print(f"  {e}")
        print()
        print(f"Total errors: {len(errors)}")
        return 1
    else:
        print("All translations match!")
        return 0


if __name__ == "__main__":
    sys.exit(compare_translations())
