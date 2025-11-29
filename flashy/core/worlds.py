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
    background: str  # Path relative to assets/ folder
    # Visual theming for world map
    path_color: str  # SVG path stroke color
    node_color: str  # Level node background color
    node_glow: str  # Level node glow/shadow color
    # Map layout - list of waypoints the path passes through (0-100 coordinate space)
    # Format: "x1,y1 x2,y2 x3,y3 ..." - the curve will smoothly pass through each point
    map_waypoints: str


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
    background="backgrounds/world-1-addition-alps.webp",
    path_color="#4d350b",  # Warm cream trail
    node_color="#2d5a3d",  # Forest green
    node_glow="#4a8c5c",  # Lighter green glow
    # Waypoints: start at bottom, zigzag up the mountain
    map_waypoints="80,90 50,93 20,73 30,50 55,50 75,25 50,15",
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
        '"The meadows lie ahead. Enjoy the flowers!"\n'
        '"Hop along now!"'
    ),
    background="backgrounds/world-2-subtraction-swamp.webp",
    path_color="#556644",  # Mossy green
    node_color="#3a5a4a",  # Swamp green
    node_glow="#5a7a6a",  # Murky glow
    map_waypoints="30,90 55,85 80,70 85,45 40,70 40,45 75,30 50,15",
)

WORLD_3 = World(
    number=3,
    name="Multiplication Meadows",
    theme_emoji="🌸",
    operation=Operation.MULTIPLY,
    friend_name="Times",
    friend_emoji="🐰",
    boss_name="Countess Calculata",
    boss_emoji="🦊",
    intro_text=(
        "Beautiful flowers swayed in the breeze.\n"
        '"What a lovely place... but I must keep moving!"\n'
        "The Multiplication Meadows bloomed with possibility..."
    ),
    friend_text=(
        '"Oh my, oh my! A visitor!" *hops excitedly*\n'
        '"I\'m Times the Rabbit! I multiply EVERYTHING!"\n'
        '"One carrot becomes two, two become four!"\n'
        '"Multiplication is just fast addition, you know!"'
    ),
    boss_intro=(
        '"Well, well... the lost puppy arrives."\n'
        '"I am Countess Calculata, master of multiplication!"\n'
        '"Beat me, and the desert path shall open!"'
    ),
    boss_defeat=(
        '"Magnificent! You\'ve mastered multiplication!"\n'
        '"The desert lies ahead. Stay hydrated!"\n'
        '"Your home draws ever closer."'
    ),
    background="backgrounds/world-3-multiplication-meadows.webp",
    path_color="#e8c4d4",  # Soft pink
    node_color="#7a4a6a",  # Meadow purple
    node_glow="#b888a8",  # Floral glow
    map_waypoints="90,90 60,90 30,80 30,70 50,60 80,40 30,20 50,15",
)

WORLD_4 = World(
    number=4,
    name="Division Desert",
    theme_emoji="🏜️",
    operation=Operation.DIVIDE,
    friend_name="Remainder",
    friend_emoji="🐪",
    boss_name="The Sphinx of Splits",
    boss_emoji="🦁",
    intro_text=(
        "The heat hit Flashy like a wall.\n"
        '"So hot... but I can almost smell home!"\n'
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
        '"Look there, beyond the dunes..."\n'
        '"Is that... your HOME?"'
    ),
    background="backgrounds/world-4-division-desert.webp",
    path_color="#c9a86c",  # Sandy trail
    node_color="#8b6914",  # Desert gold
    node_glow="#d4a84b",  # Golden glow
    map_waypoints="80,90 40,90 40,80 75,70 75,55 35,55 50,15",
)

WORLDS = [WORLD_1, WORLD_2, WORLD_3, WORLD_4]


def get_world(world_num: int) -> World | None:
    """Get world by number. Returns None if world doesn't exist."""
    for world in WORLDS:
        if world.number == world_num:
            return world
    return None
