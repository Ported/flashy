# Flashy - Development Guide

## Running Checks

Run these regularly, especially before committing:

```bash
poetry run ruff check . && poetry run pyright && poetry run pytest
```

## Project Structure

- `flashy/` - Main package
  - `problems.py` - Problem generation (pure functions)
  - `levels.py` - Level definitions (abstracted for easy iteration)
  - `scoring.py` - Score calculation
  - `game.py` - Core game loop
  - `input_handler.py` - Input abstraction (text now, voice later)
  - `history.py` - Session logging to ~/.flashy/history.log
  - `main.py` - Entry point
- `tests/` - Unit tests

## Running the Game

```bash
poetry run flashy
```
