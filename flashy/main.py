"""Main entry point - Flashy's Journey Home."""

import sys

from flashy.game import display_level_summary, run_boss_level, run_level
from flashy.history import (
    list_players,
    load_progress,
    log_session,
    player_exists,
    save_progress,
)
from flashy.input_handler import InputHandler, TextInputHandler, VoiceInputHandler
from flashy.levels import LevelType, get_level, get_next_level
from flashy.map_display import display_star_result, display_world_map
from flashy.scoring import calculate_stars
from flashy.story import (
    display_boss_intro,
    display_boss_victory,
    display_flashy_intro,
    display_friend_meeting,
    display_game_complete,
    display_world_intro,
)
from flashy.worlds import get_world

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
DIM = "\033[2m"
RESET = "\033[0m"


def _select_player() -> str:
    """Display player selection screen and return selected player name."""
    print(f"\n{CYAN}{'═' * 44}{RESET}")
    print(f"   🐕  {CYAN}FLASHY{RESET} - Math Adventure")
    print(f"{CYAN}{'═' * 44}{RESET}\n")

    players = list_players()

    if players:
        print("Who's playing today?\n")
        for i, name in enumerate(players, 1):
            # Show progress summary
            progress = load_progress(name)
            total_stars = sum(progress.stars.values())
            highest = progress.get_highest_unlocked()
            print(f"  {GREEN}{i}.{RESET} {name}")
            print(f"     {DIM}⭐ {total_stars} stars | Level {highest}{RESET}")
        print(f"\n  {YELLOW}N.{RESET} New player")
        print()

        while True:
            choice = input("Choose (1-" + str(len(players)) + " or N) > ").strip()

            if choice.lower() == "n":
                return _create_new_player()

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(players):
                    name = players[idx]
                    print(f"\n{GREEN}Welcome back, {name}!{RESET}\n")
                    return name
            except ValueError:
                pass

            print("Invalid choice, try again.")
    else:
        print("Welcome to Flashy! Let's create your profile.\n")
        return _create_new_player()


def _create_new_player() -> str:
    """Create a new player profile."""
    print("\nWhat's your name?\n")

    while True:
        name = input("Name > ").strip()

        if not name:
            print("Please enter a name.")
            continue

        # Sanitize name (remove special chars that could cause file issues)
        safe_name = "".join(c for c in name if c.isalnum() or c in " -_").strip()
        if not safe_name:
            print("Please use letters and numbers only.")
            continue

        if player_exists(safe_name):
            print(f"'{safe_name}' already exists! Choose another name.")
            continue

        # Create empty progress file
        from flashy.history import PlayerProgress

        save_progress(safe_name, PlayerProgress())
        print(f"\n{GREEN}Welcome, {safe_name}! Let's begin your adventure!{RESET}\n")
        return safe_name


def _create_input_handler() -> InputHandler:
    """Create the input handler, preferring voice with text fallback."""
    if "--text" in sys.argv:
        print("Using text input mode.\n")
        return TextInputHandler()

    try:
        handler = VoiceInputHandler()
        print("Using voice input mode. Say your answer!\n")
        print('Say "skip" or "give up" to skip a problem.\n')
        return handler
    except Exception as e:
        print(f"Voice input unavailable ({e}), using text input.\n")
        return TextInputHandler()


def main() -> None:
    """Run the Flashy game."""
    # Select or create player
    player_name = _select_player()

    # Load saved progress
    progress = load_progress(player_name)

    # Show intro on first play
    if not progress.stars:
        display_flashy_intro()

    input_handler = _create_input_handler()

    # Find current level (highest unlocked that isn't 3-starred)
    current_level_num = 1
    for i in range(1, 11):  # World 1 has levels 1-10
        if progress.is_unlocked(i) and progress.get_stars(i) < 3:
            current_level_num = i
            break
        if progress.is_unlocked(i):
            current_level_num = i

    last_world_shown = 0
    last_friend_shown = 0

    try:
        while True:
            level = get_level(current_level_num)
            if level is None:
                print("Congratulations! You've completed all available levels!")
                break

            world = get_world(level.world_number)
            if world is None:
                break

            # Show world intro when entering a new world
            if level.world_number != last_world_shown and level.level_in_world == 1:
                display_world_intro(world)
                last_world_shown = level.world_number

            # Show world map
            display_world_map(world, progress)

            # Check if level is unlocked
            if not progress.is_unlocked(level.number):
                print(f"Level {level.number} is locked!")
                print("You need 2 stars on the previous level to unlock it.\n")
                # Go back to highest playable level
                current_level_num = max(1, current_level_num - 1)
                continue

            # Show friend meeting before friend level (only once)
            if (
                level.level_type == LevelType.FRIEND
                and level.number != last_friend_shown
            ):
                display_friend_meeting(world)
                last_friend_shown = level.number

            # Show boss intro before boss level
            if level.level_type == LevelType.BOSS:
                display_boss_intro(world)

            # Run the level
            if level.level_type == LevelType.BOSS:
                result = run_boss_level(level, input_handler)
            else:
                result = run_level(level, input_handler)

            display_level_summary(result)

            # Calculate stars
            stars = calculate_stars(
                result.correct_count,
                result.total_problems,
                result.total_time_seconds,
            )

            # Check if this is a new best
            old_stars = progress.get_stars(level.number)
            is_new_best = stars > old_stars

            # Save progress
            progress.set_stars(level.number, stars)
            save_progress(player_name, progress)

            # Log the session
            log_session(result)

            # Show star result
            display_star_result(stars, is_new_best)

            # Handle boss victory
            if level.level_type == LevelType.BOSS and stars >= 2:
                display_boss_victory(world)

                # Check if game complete (level 10 with 2+ stars = World 1 done)
                if level.number == 10:
                    display_game_complete()
                    break

            # Check if can progress
            if stars < 2:
                # Retry current level
                choice = input("Try again? (y/n) > ").strip().lower()
                if choice in ("n", "no", "q", "quit", "exit"):
                    print("\nKeep practicing! See you next time!\n")
                    break
                # Replay same level
                continue

            # Check for next level
            next_level = get_next_level(current_level_num)
            if next_level is None:
                print("\nYou've completed all available levels!")
                print("More worlds coming soon!\n")
                break

            # Ask if player wants to continue or replay for more stars
            print(f"Next up: Level {next_level.number}: {next_level.name}")
            if stars < 3:
                extra = 3 - stars
                print(f"(Or replay for {extra} more star{'s' if extra > 1 else ''})")
            choice = input("Continue? (y/n/replay) > ").strip().lower()

            if choice in ("n", "no", "q", "quit", "exit"):
                print("\nGreat job! See you next time!\n")
                break
            elif choice in ("r", "replay", "again"):
                # Replay current level
                continue
            else:
                current_level_num = next_level.number

    except KeyboardInterrupt:
        print(f"\n\nThanks for playing, {player_name}! Goodbye!\n")
        save_progress(player_name, progress)


if __name__ == "__main__":
    main()
