"""World definitions - story content and theming."""

from dataclasses import dataclass

from flashy.core.problems import Operation


@dataclass(frozen=True)
class World:
    """Configuration for a game world."""

    number: int
    name: str
    theme_emoji: str
    operation: Operation
    friend_name: str
    friend_emoji: str
    boss_name: str
    boss_emoji: str
    intro_text: str
    friend_text: str
    boss_intro: str
    boss_defeat: str


# World definitions
WORLD_1 = World(
    number=1,
    name="Addition Alps",
    theme_emoji="🏔️",
    operation=Operation.ADD,
    friend_name="Carry",
    friend_emoji="🦉",
    boss_name="Summit",
    boss_emoji="🐐",
    intro_text=(
        "Flashy woke up alone in the cold mountains.\n"
        '"Where am I? I need to find my way home!"\n'
        "The only way forward is up through the Addition Alps..."
    ),
    friend_text=(
        '"Hoo-hoo! I\'m Carry the Owl!"\n'
        '"I\'ve watched many travelers climb these peaks."\n'
        '"Remember: when numbers get big, just carry on!"\n'
        '"Let me help you on your journey home."'
    ),
    boss_intro=(
        '"So, little pup, you think you can cross MY mountain?"\n'
        '"I am Summit, guardian of the Alps!"\n'
        '"Prove your addition skills... if you can keep up!"'
    ),
    boss_defeat=(
        '"Impressive, little one! You\'ve earned passage."\n'
        '"The path ahead leads to the Subtraction Swamp."\n'
        '"May your numbers stay strong!"'
    ),
)

WORLD_2 = World(
    number=2,
    name="Subtraction Swamp",
    theme_emoji="🌿",
    operation=Operation.SUBTRACT,
    friend_name="Borrow",
    friend_emoji="🐢",
    boss_name="Minus",
    boss_emoji="🐸",
    intro_text=(
        "The mountains gave way to murky wetlands.\n"
        '"It\'s so foggy here... but I must keep going!"\n'
        "Flashy stepped carefully into the Subtraction Swamp..."
    ),
    friend_text=(
        '"Slow down there, young pup!"\n'
        "\"I'm Borrow the Turtle. I've lived here for centuries.\"\n"
        '"When you need to take away more than you have,"\n'
        '"just borrow from your neighbor. Works every time!"'
    ),
    boss_intro=(
        '"RIBBIT! Who dares enter my swamp?"\n'
        '"I am Minus, the Frog King!"\n'
        '"Let\'s see if you can subtract as fast as I can jump!"'
    ),
    boss_defeat=(
        '"RIBBIT... you\'ve bested me, small one."\n'
        '"The desert lies ahead. Stay hydrated!"\n'
        '"Hop along now!"'
    ),
)

WORLD_3 = World(
    number=3,
    name="Division Desert",
    theme_emoji="🏜️",
    operation=Operation.DIVIDE,
    friend_name="Remainder",
    friend_emoji="🐪",
    boss_name="The Sphinx of Splits",
    boss_emoji="🦁",
    intro_text=(
        "The heat hit Flashy like a wall.\n"
        '"So hot... but I can see green meadows in the distance!"\n'
        "The Division Desert stretched endlessly before..."
    ),
    friend_text=(
        '"Ah, a traveler! I am Remainder the Camel."\n'
        '"I carry what\'s left over from every division."\n'
        '"Remember: divide means to share equally!"\n'
        '"Split it up fair, and you\'ll find your answer."'
    ),
    boss_intro=(
        '"HALT, wanderer! None pass without solving my riddles."\n'
        '"I am the Sphinx of Splits!"\n'
        '"Divide correctly, or be lost to the sands forever!"'
    ),
    boss_defeat=(
        '"You have wisdom beyond your years, young pup."\n'
        '"The meadows await. Your home draws near."\n'
        '"Go forth with my blessing."'
    ),
)

WORLD_4 = World(
    number=4,
    name="Multiplication Meadows",
    theme_emoji="🌸",
    operation=Operation.MULTIPLY,
    friend_name="Times",
    friend_emoji="🐰",
    boss_name="Countess Calculata",
    boss_emoji="🦊",
    intro_text=(
        "Beautiful flowers swayed in the breeze.\n"
        '"I can almost smell home! It must be close!"\n'
        "The Multiplication Meadows bloomed with possibility..."
    ),
    friend_text=(
        '"Oh my, oh my! A visitor!" *hops excitedly*\n'
        '"I\'m Times the Rabbit! I multiply EVERYTHING!"\n'
        '"One carrot becomes two, two become four!"\n'
        '"Multiplication is just fast addition, you know!"'
    ),
    boss_intro=(
        '"Well, well... the lost puppy finally arrives."\n'
        '"I am Countess Calculata, master of all operations!"\n'
        '"Beat me, and you\'ll find your way home at last!"'
    ),
    boss_defeat=(
        '"Magnificent! You\'ve mastered it all!"\n'
        '"Look there, beyond the meadow..."\n'
        '"Is that... your HOME?"'
    ),
)

WORLDS = [WORLD_1, WORLD_2, WORLD_3, WORLD_4]


def get_world(world_num: int) -> World | None:
    """Get world by number. Returns None if world doesn't exist."""
    for world in WORLDS:
        if world.number == world_num:
            return world
    return None
