#!/usr/bin/env python3
"""Check for hardcoded user-facing strings in index.html that should use i18n.

This script scans the JavaScript sections of index.html for string literals
that appear to be user-facing text (English sentences) that should be
translated using the t() function.

Run as part of linting: poetry run python scripts/check_i18n.py
"""

import re
import sys
from pathlib import Path

# Patterns that indicate a string should be translated
USER_FACING_PATTERNS = [
    # Sentences with capital start and punctuation
    r"'[A-Z][^']{10,}[.!?]'",
    r'"[A-Z][^"]{10,}[.!?]"',
    # Common UI text patterns
    r"'[A-Z][a-z]+ [a-z]+ [a-z]+'",  # "Name too long"
    r'"[A-Z][a-z]+ [a-z]+ [a-z]+"',
]

# Strings that are allowed (technical, not user-facing, or special cases)
ALLOWED_STRINGS = {
    # Strings shown before Pyodide loads (t() not available yet)
    "Loading Pyodide",
    "Setting up Python",
    # HTML placeholders that are updated by updateTranslations()
    "Enter your name",
    "Leaderboard",
    "Create",
    "Cancel",
    "Back",
    "Continue",
    "Replay",
    "Enter",
    # Technical/code strings
    "active",
    "screen",
    "locked",
    "completed",
    "perfect",
    "available",
    "has-input",
    "correct",
    "incorrect",
    "top-3",
    "current-player",
    "problem-display",
    "timer",
    "timer low",
    # Element IDs and selectors
    "loading-status",
    "player-select-screen",
    "new-player-screen",
    "intro-screen",
    "world-intro-screen",
    "friend-meet-screen",
    "boss-intro-screen",
    "gameplay-screen",
    "result-screen",
    "boss-victory-screen",
    "game-complete-screen",
    "leaderboard-screen",
    "world-map-screen",
    # API/storage keys
    "flashy_language",
    "flashy_token_",
    "Content-Type",
    "application/json",
    # Python code embedded in JS
    "from flashy",
    "import",
    "WebStorage",
    "PlayerProgress",
    "GameController",
    "GameFlow",
    # Console/debug
    "console.",
    "Error:",
    # CSS classes
    "world-",
    "level-item",
    "leaderboard-entry",
    # Event names
    "click",
    "keydown",
    # Misc technical
    "POST",
    "GET",
    "True",
    "False",
    "None",
}

# Regex to find strings that use t() - these are fine
T_FUNCTION_PATTERN = re.compile(r"t\(['\"`][^'\"]+['\"`]\)")


def is_in_script_section(content: str, pos: int) -> bool:
    """Check if position is inside a <script> tag."""
    # Find the last <script> before pos
    last_script_start = content.rfind("<script", 0, pos)
    if last_script_start == -1:
        return False
    # Find the </script> after that
    script_end = content.find("</script>", last_script_start)
    return script_end == -1 or pos < script_end


def check_file(filepath: Path) -> list[tuple[int, str, str]]:
    """Check a file for hardcoded strings that should be translated.

    Returns list of (line_number, string_found, context).
    """
    content = filepath.read_text()
    lines = content.split("\n")
    issues: list[tuple[int, str, str]] = []

    for line_num, line in enumerate(lines, 1):
        # Skip lines that use t() function
        if "t(" in line or "t`" in line:
            continue

        # Skip comment lines
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("/*"):
            continue

        # Skip console.log/warn/error lines - these are for developers
        if "console." in line:
            continue

        # Look for string patterns that might be user-facing
        # Find all quoted strings in the line
        strings = re.findall(r"'([^']*)'|\"([^\"]*)\"", line)

        for match in strings:
            s = match[0] or match[1]

            # Skip empty or very short strings
            if len(s) < 3:
                continue

            # Skip if it's a technical/allowed string
            if any(allowed in s for allowed in ALLOWED_STRINGS):
                continue

            # Skip if it looks like an ID, class, or path
            if s.startswith("#") or s.startswith(".") or "/" in s:
                continue

            # Skip if it looks like a template variable or Python code
            if "${" in s or "{{" in s or s.startswith("from ") or "=" in s:
                continue

            # Skip SVG path data (e.g., "M10 2L2 10L10 18")
            if re.match(r"^M[\d\s.MLHVCSQTAZ,-]+$", s, re.IGNORECASE):
                continue

            # Check if it looks like user-facing English text
            # Has spaces and starts with capital letter
            if " " in s and s[0].isupper() and len(s) > 15:
                # This looks like a sentence that should be translated
                context = line.strip()[:80]
                issues.append((line_num, s, context))

    return issues


def main() -> int:
    """Main entry point."""
    # Find index.html
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    index_html = project_root / "flashy" / "platforms" / "web" / "index.html"

    if not index_html.exists():
        print(f"Error: {index_html} not found")
        return 1

    issues = check_file(index_html)

    if issues:
        print("i18n check failed! Found hardcoded strings that should use t():")
        print()
        for line_num, string, context in issues:
            print(f"  Line {line_num}: {string!r}")
            print(f"    Context: {context}")
            print()
        print(f"Found {len(issues)} issue(s).")
        print()
        print("To fix:")
        print("  1. Add the string to flashy/core/i18n.py TRANSLATIONS")
        print("  2. Replace the hardcoded string with t('your.key.name')")
        return 1

    print("i18n check passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
