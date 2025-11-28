#!/usr/bin/env python3
"""Run all checks: linting, type checking, tests, i18n, and build.

Usage:
    poetry run python scripts/check.py          # Run unit tests only
    poetry run python scripts/check.py --e2e    # Include E2E tests
    poetry run python scripts/check.py --all    # Same as --e2e
"""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def run_command(name: str, cmd: list[str]) -> bool:
    """Run a command and return True if successful."""
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"\n{name} FAILED")
        return False
    print(f"{name} passed")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all project checks")
    parser.add_argument(
        "--e2e", "--all", action="store_true", help="Include E2E tests (slower)"
    )
    args = parser.parse_args()

    checks = [
        ("Ruff (linting)", ["poetry", "run", "ruff", "check", "."]),
        ("Pyright (type checking)", ["poetry", "run", "pyright"]),
        ("i18n check", ["poetry", "run", "python", "scripts/check_i18n.py"]),
        ("Web build", ["poetry", "run", "python", "flashy/platforms/web/build.py"]),
    ]

    # Add appropriate test command
    if args.e2e:
        checks.append(("Pytest (all tests)", ["poetry", "run", "pytest"]))
    else:
        checks.append(
            ("Pytest (unit tests)", ["poetry", "run", "pytest", "tests/unit"])
        )

    failed = []
    for name, cmd in checks:
        if not run_command(name, cmd):
            failed.append(name)

    print(f"\n{'='*60}")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        return 1
    else:
        print("All checks passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
