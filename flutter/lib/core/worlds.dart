// World definitions - story content and theming.
import 'problems.dart';

/// Configuration for a game world.
class World {
  const World({
    required this.number,
    required this.name,
    required this.themeEmoji,
    required this.operation,
    required this.friendName,
    required this.friendEmoji,
    required this.bossName,
    required this.bossEmoji,
    required this.introText,
    required this.friendText,
    required this.bossIntro,
    required this.bossDefeat,
    required this.background,
    required this.pathColor,
    required this.nodeColor,
    required this.nodeGlow,
    required this.mapWaypoints,
  });

  final int number;
  final String name;
  final String themeEmoji;
  final Operation operation;
  final String friendName;
  final String friendEmoji;
  final String bossName;
  final String bossEmoji;
  final String introText;
  final String friendText;
  final String bossIntro;
  final String bossDefeat;

  /// Path relative to assets/ folder.
  final String background;

  /// SVG path stroke color.
  final String pathColor;

  /// Level node background color.
  final String nodeColor;

  /// Level node glow/shadow color.
  final String nodeGlow;

  /// Map layout - list of waypoints the path passes through (0-100 coordinate space).
  /// Format: "x1,y1 x2,y2 x3,y3 ..." - the curve will smoothly pass through each point.
  final String mapWaypoints;
}

/// World 1: Addition Alps
const world1 = World(
  number: 1,
  name: 'Addition Alps',
  themeEmoji: '🏔️',
  operation: Operation.add,
  friendName: 'Carry',
  friendEmoji: '🦉',
  bossName: 'Summit',
  bossEmoji: '🐐',
  introText:
      'Flashy woke up alone in the cold mountains.\n'
      '"Where am I? I need to find my way home!"\n'
      'The only way forward is up through the Addition Alps...',
  friendText:
      '"Hoo-hoo! I\'m Carry the Owl!"\n'
      '"I\'ve watched many travelers climb these peaks."\n'
      '"Remember: when numbers get big, just carry on!"\n'
      '"Let me help you on your journey home."',
  bossIntro:
      '"So, little pup, you think you can cross MY mountain?"\n'
      '"I am Summit, guardian of the Alps!"\n'
      '"Prove your addition skills... if you can keep up!"',
  bossDefeat:
      '"Impressive, little one! You\'ve earned passage."\n'
      '"The path ahead leads to the Subtraction Swamp."\n'
      '"May your numbers stay strong!"',
  background: 'backgrounds/world-1-addition-alps.webp',
  pathColor: '#4d350b',
  nodeColor: '#2d5a3d',
  nodeGlow: '#4a8c5c',
  mapWaypoints: '75,82 50,82 22,70 33,45 50,65 65,65 75,47 65,25 52,15',
);

/// World 2: Subtraction Swamp
const world2 = World(
  number: 2,
  name: 'Subtraction Swamp',
  themeEmoji: '🌿',
  operation: Operation.subtract,
  friendName: 'Borrow',
  friendEmoji: '🐢',
  bossName: 'Minus',
  bossEmoji: '🐸',
  introText:
      'The mountains gave way to murky wetlands.\n'
      '"It\'s so foggy here... but I must keep going!"\n'
      'Flashy stepped carefully into the Subtraction Swamp...',
  friendText:
      '"Slow down there, young pup!"\n'
      '"I\'m Borrow the Turtle. I\'ve lived here for centuries."\n'
      '"When you need to take away more than you have,"\n'
      '"just borrow from your neighbor. Works every time!"',
  bossIntro:
      '"RIBBIT! Who dares enter my swamp?"\n'
      '"I am Minus, the Frog King!"\n'
      '"Let\'s see if you can subtract as fast as I can jump!"',
  bossDefeat:
      '"RIBBIT... you\'ve bested me, small one."\n'
      '"The meadows lie ahead. Enjoy the flowers!"\n'
      '"Hop along now!"',
  background: 'backgrounds/world-2-subtraction-swamp.webp',
  pathColor: '#C4D95C',
  nodeColor: '#6c5e0f',
  nodeGlow: '#d3a769',
  mapWaypoints: '30,90 55,85 80,70 85,45 40,70 40,50 75,40 50,15',
);

/// World 3: Multiplication Meadows
const world3 = World(
  number: 3,
  name: 'Multiplication Meadows',
  themeEmoji: '🌸',
  operation: Operation.multiply,
  friendName: 'Times',
  friendEmoji: '🐰',
  bossName: 'Countess Calculata',
  bossEmoji: '🦊',
  introText:
      'Beautiful flowers swayed in the breeze.\n'
      '"What a lovely place... but I must keep moving!"\n'
      'The Multiplication Meadows bloomed with possibility...',
  friendText:
      '"Oh my, oh my! A visitor!" *hops excitedly*\n'
      '"I\'m Times the Rabbit! I multiply EVERYTHING!"\n'
      '"One carrot becomes two, two become four!"\n'
      '"Multiplication is just fast addition, you know!"',
  bossIntro:
      '"Well, well... the lost puppy arrives."\n'
      '"I am Countess Calculata, master of multiplication!"\n'
      '"Beat me, and the desert path shall open!"',
  bossDefeat:
      '"Magnificent! You\'ve mastered multiplication!"\n'
      '"The desert lies ahead. Stay hydrated!"\n'
      '"Your home draws ever closer."',
  background: 'backgrounds/world-3-multiplication-meadows.webp',
  pathColor: '#e8c4d4',
  nodeColor: '#7a4a6a',
  nodeGlow: '#b888a8',
  mapWaypoints: '90,80 50,80 20,90 10,68 50,60 65,60 72,45 40,35 10,40',
);

/// World 4: Division Desert
const world4 = World(
  number: 4,
  name: 'Division Desert',
  themeEmoji: '🏜️',
  operation: Operation.divide,
  friendName: 'Remainder',
  friendEmoji: '🐪',
  bossName: 'The Sphinx of Splits',
  bossEmoji: '🦁',
  introText:
      'The heat hit Flashy like a wall.\n'
      '"So hot... but I can almost smell home!"\n'
      'The Division Desert stretched endlessly before...',
  friendText:
      '"Ah, a traveler! I am Remainder the Camel."\n'
      '"I carry what\'s left over from every division."\n'
      '"Remember: divide means to share equally!"\n'
      '"Split it up fair, and you\'ll find your answer."',
  bossIntro:
      '"HALT, wanderer! None pass without solving my riddles."\n'
      '"I am the Sphinx of Splits!"\n'
      '"Divide correctly, or be lost to the sands forever!"',
  bossDefeat:
      '"You have wisdom beyond your years, young pup."\n'
      '"Look there, beyond the dunes..."\n'
      '"Is that... your HOME?"',
  background: 'backgrounds/world-4-division-desert.webp',
  pathColor: '#d3c749',
  nodeColor: '#d17109',
  nodeGlow: '#fcb519',
  mapWaypoints: '80,90 40,90 40,80 70,70 65,55 35,55 40,35 80,40 65,15',
);

/// All worlds in order.
const List<World> worlds = [world1, world2, world3, world4];

/// Get world by number. Returns null if world doesn't exist.
World? getWorld(int worldNum) {
  for (final world in worlds) {
    if (world.number == worldNum) {
      return world;
    }
  }
  return null;
}
