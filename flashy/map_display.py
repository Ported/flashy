"""World map display - ASCII art progress visualization."""

from flashy.history import PlayerProgress
from flashy.levels import LevelType, get_levels_for_world
from flashy.worlds import World

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
RESET = "\033[0m"


def _stars_display(count: int) -> str:
    """Return star display string like ⭐⭐· for 2 stars."""
    filled = "⭐" * count
    empty = "·" * (3 - count)
    return filled + empty


def _level_icon(level_type: LevelType, world: World) -> str:
    """Get the icon for a level based on its type."""
    if level_type == LevelType.BOSS:
        return world.boss_emoji
    elif level_type == LevelType.FRIEND:
        return world.friend_emoji
    else:
        return "  "  # Regular levels just show stars


def display_world_map(world: World, progress: PlayerProgress) -> None:
    """Display the ASCII map for a world.

    Shows all levels with:
    - Star ratings for completed levels
    - Lock icon for locked levels
    - Current level marker
    - Special icons for friend and boss levels
    """
    levels = get_levels_for_world(world.number)

    # Find current level (highest unlocked that isn't 3-starred)
    current_level = 1
    for level in levels:
        if progress.is_unlocked(level.number):
            if progress.get_stars(level.number) < 3:
                current_level = level.number
                break
            current_level = level.number

    # Header
    print(f"\n{'═' * 44}")
    print(f"   {world.theme_emoji}  {world.name.upper()}  {world.theme_emoji}")
    print(f"{'═' * 44}\n")

    # Display levels from top (10) to bottom (1)
    for level in reversed(levels):
        stars = progress.get_stars(level.number)
        is_unlocked = progress.is_unlocked(level.number)
        is_current = level.number == current_level

        # Level icon (boss/friend emoji or stars)
        icon = _level_icon(level.level_type, world)

        # Build the line
        if is_current:
            marker = f"{GREEN}→ ◉{RESET}"
        elif is_unlocked:
            marker = "   "
        else:
            marker = f"{DIM}   {RESET}"

        if is_unlocked:
            star_str = _stars_display(stars)
            name = level.name
            lock = ""
        else:
            star_str = f"{DIM}···{RESET}"
            name = f"{DIM}{level.name}{RESET}"
            lock = f" {DIM}🔒{RESET}"

        # Format: → ◉  ⭐⭐· [3] Snowy Path      🔒
        level_num = f"[{level.level_in_world:2d}]"
        print(f" {marker} {icon}{star_str} {level_num} {name}{lock}")

        # Draw connector line (except after last level)
        if level.level_in_world > 1:
            if is_unlocked or progress.is_unlocked(level.number - 1):
                print("        │")
            else:
                print(f"        {DIM}│{RESET}")

    print(f"\n{'═' * 44}\n")


def display_star_result(stars: int, is_new_best: bool = False) -> None:
    """Display the star result with animation-like effect."""
    if stars == 0:
        print(f"\n{RED}Level not passed!{RESET}")
        print("You need 60% correct to earn a star.\n")
        return

    star_display = "⭐" * stars + "·" * (3 - stars)

    if stars == 3:
        color = GREEN
        message = "PERFECT!"
    elif stars == 2:
        color = YELLOW
        message = "Great job!"
    else:
        color = RESET
        message = "Keep practicing!"

    print(f"\n{color}{'★' * 20}{RESET}")
    print(f"   {star_display}  {stars} STAR{'S' if stars != 1 else ''}!")
    if is_new_best:
        print(f"   {GREEN}★ NEW BEST! ★{RESET}")
    print(f"   {message}")
    print(f"{color}{'★' * 20}{RESET}\n")

    if stars < 2:
        print(f"{YELLOW}You need 2 stars to unlock the next level.{RESET}\n")
