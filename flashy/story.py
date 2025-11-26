"""Story moments - ASCII art and narrative display."""

from flashy.worlds import World

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


# ASCII Art for characters
FLASHY_ART = r"""
    /\_/\
   ( o.o )
    > ^ <
   /|   |\
"""

FLASHY_HAPPY_ART = r"""
    /\_/\
   ( ^.^ )
    > ^ <  ~
   /|   |\
"""

OWL_ART = r"""
   ,_,
  (o,o)
  {`"'}
  -"-"-
"""

GOAT_ART = r"""
    /|  |\
   / |  | \
  (  @  @  )
   \  __  /
    \/  \/
"""

TURTLE_ART = r"""
     _____
   .'     '.
  /  o   o  \
  |    _    |
  '._./ \_.'
    |___|
"""

FROG_ART = r"""
    @..@
   (----)
  ( >__< )
  ^^    ^^
"""

CAMEL_ART = r"""
      //
  ___//___
 /   @@   \
 |   __   |
 |  /  \  |
  \/    \/
"""

SPHINX_ART = r"""
    /\  /\
   /  \/  \
  ( o    o )
   \  ^^  /
    '-..-'
"""

RABBIT_ART = r"""
   (\ /)
   ( . .)
   c(")(")
"""

FOX_ART = r"""
   /\   /\
  /  \ /  \
 ( o   o )
  \  w  /
   '---'
"""

HOME_ART = r"""
       /\
      /  \
     /    \
    /______\
    |  []  |
    |______|
"""


def _print_boxed(text: str, width: int = 44) -> None:
    """Print text in a box."""
    lines = text.strip().split("\n")
    print("┌" + "─" * (width - 2) + "┐")
    for line in lines:
        # Handle lines that are too long
        while len(line) > width - 4:
            print(f"│ {line[:width-4]} │")
            line = line[width - 4 :]
        padding = width - 4 - len(line)
        print(f"│ {line}{' ' * padding} │")
    print("└" + "─" * (width - 2) + "┘")


def display_flashy_intro() -> None:
    """Display Flashy's introduction at game start."""
    print(f"\n{CYAN}")
    print(FLASHY_ART)
    print(RESET)
    _print_boxed(
        "FLASHY\n\n"
        '"Oh no! Where am I?"\n'
        '"I chased that butterfly too far..."\n'
        '"I need to find my way home!"'
    )
    print()
    input(f"{YELLOW}Press Enter to begin your journey...{RESET}")


def display_world_intro(world: World) -> None:
    """Display introduction when entering a new world."""
    print(f"\n{'═' * 44}")
    print(f"   {world.theme_emoji}  Entering: {world.name}  {world.theme_emoji}")
    print(f"{'═' * 44}\n")

    print(f"{CYAN}")
    print(FLASHY_ART)
    print(RESET)

    _print_boxed(world.intro_text)
    print()
    input(f"{YELLOW}Press Enter to continue...{RESET}")


def display_friend_meeting(world: World) -> None:
    """Display friend meeting story moment."""
    # Get the right art for this world's friend
    friend_art = {
        1: OWL_ART,
        2: TURTLE_ART,
        3: CAMEL_ART,
        4: RABBIT_ART,
    }.get(world.number, OWL_ART)

    print(f"\n{'═' * 44}")
    print(f"   {world.friend_emoji}  A New Friend!  {world.friend_emoji}")
    print(f"{'═' * 44}\n")

    print(f"{GREEN}")
    print(friend_art)
    print(RESET)

    _print_boxed(f"{world.friend_name.upper()}\n\n{world.friend_text}")
    print()

    print(f"{CYAN}")
    print(FLASHY_HAPPY_ART)
    print(RESET)

    _print_boxed(
        "FLASHY\n\n"
        f'"Thank you, {world.friend_name}!"\n'
        '"I\'ll remember your advice!"'
    )
    print()
    input(f"{YELLOW}Press Enter to continue...{RESET}")


def display_boss_intro(world: World) -> None:
    """Display boss introduction before battle."""
    # Get the right art for this world's boss
    boss_art = {
        1: GOAT_ART,
        2: FROG_ART,
        3: SPHINX_ART,
        4: FOX_ART,
    }.get(world.number, GOAT_ART)

    print(f"\n{'═' * 44}")
    print(f"   {world.boss_emoji}  BOSS BATTLE!  {world.boss_emoji}")
    print(f"{'═' * 44}\n")

    print(f"{YELLOW}")
    print(boss_art)
    print(RESET)

    _print_boxed(f"{world.boss_name.upper()}\n\n{world.boss_intro}")
    print()

    print(f"{CYAN}")
    print(FLASHY_ART)
    print(RESET)

    _print_boxed("FLASHY\n\n" '"I\'m not afraid! Let\'s do this!"')
    print()
    input(f"{YELLOW}Press Enter to start the challenge...{RESET}")


def display_boss_victory(world: World) -> None:
    """Display victory message after defeating boss."""
    print(f"\n{GREEN}{'★' * 44}{RESET}")
    print(f"\n   {world.boss_emoji}  VICTORY!  {world.boss_emoji}\n")
    print(f"{GREEN}{'★' * 44}{RESET}\n")

    _print_boxed(f"{world.boss_name.upper()}\n\n{world.boss_defeat}")
    print()

    print(f"{GREEN}")
    print(FLASHY_HAPPY_ART)
    print(RESET)

    if world.number < 4:
        _print_boxed("FLASHY\n\n" '"I did it! Onward to the next world!"')
    else:
        _print_boxed("FLASHY\n\n" '"Is that... could it be... HOME?!"')
    print()
    input(f"{YELLOW}Press Enter to continue...{RESET}")


def display_game_complete() -> None:
    """Display the ending when the player completes the game."""
    print(f"\n{GREEN}{'★' * 44}")
    print(f"{'★' * 44}")
    print(f"{'★' * 44}{RESET}\n")

    print(f"{CYAN}")
    print(HOME_ART)
    print(RESET)

    print("\n   🏠  FLASHY MADE IT HOME!  🏠\n")

    print(f"{GREEN}")
    print(FLASHY_HAPPY_ART)
    print(RESET)

    _print_boxed(
        "FLASHY\n\n"
        '"HOME! I\'m finally home!"\n'
        '"Thank you for helping me on my journey!"\n'
        '"You\'re the best mathematician ever!"'
    )

    print(f"\n{GREEN}{'★' * 44}")
    print("   CONGRATULATIONS! YOU WIN!")
    print(f"{'★' * 44}{RESET}\n")

    input(f"{YELLOW}Press Enter to continue...{RESET}")
