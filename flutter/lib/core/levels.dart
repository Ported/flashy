// Level definitions - curated problem sequences for each level.
import 'problems.dart';

/// Type of level determining its role in the world.
enum LevelType {
  intro, // Easy warmup levels (1-3)
  build, // Building difficulty (4-5)
  friend, // Meet a friend, story moment (6)
  challenge, // Harder levels (7-8)
  preboss, // Tough preparation (9)
  boss, // Timed boss battle (10)
}

/// Configuration for a game level with curated problems.
class Level {
  const Level({
    required this.number,
    required this.worldNumber,
    required this.levelInWorld,
    required this.name,
    required this.levelType,
    required this.problems,
    this.timeLimit,
  });

  /// Global level number (1-40).
  final int number;

  /// Which world (1-4).
  final int worldNumber;

  /// Position in world (1-10).
  final int levelInWorld;

  /// Level name.
  final String name;

  /// Type of level.
  final LevelType levelType;

  /// Curated problem sequence.
  final List<Problem> problems;

  /// Seconds for timed levels (only for boss levels).
  final int? timeLimit;
}

// Helper functions to create problems concisely
Problem _add(int a, int b) => Problem(
      operand1: a,
      operand2: b,
      operation: Operation.add,
      answer: a + b,
    );

Problem _sub(int a, int b) => Problem(
      operand1: a,
      operand2: b,
      operation: Operation.subtract,
      answer: a - b,
    );

Problem _mul(int a, int b) => Problem(
      operand1: a,
      operand2: b,
      operation: Operation.multiply,
      answer: a * b,
    );

Problem _div(int a, int b) => Problem(
      operand1: a,
      operand2: b,
      operation: Operation.divide,
      answer: a ~/ b,
    );

// =============================================================================
// WORLD 1: ADDITION ALPS (Levels 1-10)
// =============================================================================

final _level1 = Level(
  number: 1,
  worldNumber: 1,
  levelInWorld: 1,
  name: 'Trailhead',
  levelType: LevelType.intro,
  problems: [
    _add(1, 1), _add(2, 1), _add(3, 2), _add(2, 2), _add(1, 4),
    _add(4, 3), _add(5, 6), _add(3, 3), _add(4, 2), _add(5, 5),
  ],
);

final _level2 = Level(
  number: 2,
  worldNumber: 1,
  levelInWorld: 2,
  name: 'Foothills',
  levelType: LevelType.intro,
  problems: [
    _add(2, 3), _add(3, 2), _add(4, 2), _add(7, 5), _add(9, 6),
    _add(6, 4), _add(4, 3), _add(8, 8), _add(3, 7), _add(9, 7),
  ],
);

final _level3 = Level(
  number: 3,
  worldNumber: 1,
  levelInWorld: 3,
  name: 'Snowy Path',
  levelType: LevelType.intro,
  problems: [
    _add(8, 6), _add(3, 9), _add(2, 12), _add(9, 7), _add(7, 5),
    _add(15, 8), _add(4, 18), _add(21, 9), _add(24, 24), _add(20, 10),
  ],
);

final _level4 = Level(
  number: 4,
  worldNumber: 1,
  levelInWorld: 4,
  name: 'Alpine Meadow',
  levelType: LevelType.build,
  problems: [
    _add(16, 15), _add(12, 20), _add(8, 27), _add(17, 9), _add(6, 0),
    _add(0, 34), _add(26, 24), _add(30, 20), _add(50, 10), _add(34, 23),
  ],
);

final _level5 = Level(
  number: 5,
  worldNumber: 1,
  levelInWorld: 5,
  name: 'Mountain Trail',
  levelType: LevelType.build,
  problems: [
    _add(25, 25), _add(13, 17), _add(21, 18), _add(19, 26), _add(32, 16),
    _add(15, 19), _add(12, 31), _add(17, 36), _add(40, 40), _add(50, 56),
  ],
);

final _level6 = Level(
  number: 6,
  worldNumber: 1,
  levelInWorld: 6,
  name: "Carry's Roost",
  levelType: LevelType.friend,
  problems: [
    _add(94, 17), _add(27, 92), _add(83, 72), _add(26, 17), _add(72, 20),
    _add(54, 21), _add(82, 84), _add(27, 26), _add(10, 70), _add(14, 74),
  ],
);

final _level7 = Level(
  number: 7,
  worldNumber: 1,
  levelInWorld: 7,
  name: 'Rocky Pass',
  levelType: LevelType.challenge,
  problems: [
    _add(100, 300), _add(150, 250), _add(250, 250), _add(145, 165), _add(132, 249),
    _add(180, 220), _add(257, 278), _add(190, 10), _add(200, 700), _add(123, 123),
  ],
);

final _level8 = Level(
  number: 8,
  worldNumber: 1,
  levelInWorld: 8,
  name: 'Steep Cliffs',
  levelType: LevelType.challenge,
  problems: [
    _add(200, 142), _add(400, 298), _add(220, 127), _add(726, 176), _add(178, 654),
    _add(550, 259), _add(163, 21), _add(72, 764), _add(400, 550), _add(121, 212),
  ],
);

final _level9 = Level(
  number: 9,
  worldNumber: 1,
  levelInWorld: 9,
  name: 'Final Ascent',
  levelType: LevelType.preboss,
  problems: [
    _add(100, 100), _add(200, 300), _add(250, 120), _add(500, 400), _add(320, 180),
    _add(430, 170), _add(880, 110), _add(120, 530), _add(780, 115), _add(500, 300),
  ],
);

final _level10 = Level(
  number: 10,
  worldNumber: 1,
  levelInWorld: 10,
  name: "Summit's Challenge",
  levelType: LevelType.boss,
  timeLimit: 90,
  problems: [
    _add(748, 129), _add(73, 810), _add(257, 180), _add(128, 256), _add(459, 123),
    _add(100, 700), _add(82, 27), _add(64, 12), _add(128, 412), _add(499, 499),
  ],
);

// =============================================================================
// WORLD 2: SUBTRACTION SWAMP (Levels 11-20)
// =============================================================================

final _level11 = Level(
  number: 11,
  worldNumber: 2,
  levelInWorld: 1,
  name: 'Marsh Edge',
  levelType: LevelType.intro,
  problems: [
    _sub(3, 1), _sub(4, 2), _sub(5, 3), _sub(4, 1), _sub(5, 2),
    _sub(6, 4), _sub(5, 1), _sub(6, 3), _sub(7, 4), _sub(8, 4),
  ],
);

final _level12 = Level(
  number: 12,
  worldNumber: 2,
  levelInWorld: 2,
  name: 'Muddy Waters',
  levelType: LevelType.intro,
  problems: [
    _sub(7, 3), _sub(8, 2), _sub(19, 6), _sub(6, 6), _sub(8, 5),
    _sub(12, 7), _sub(15, 5), _sub(18, 8), _sub(14, 7), _sub(20, 10),
  ],
);

final _level13 = Level(
  number: 13,
  worldNumber: 2,
  levelInWorld: 3,
  name: 'Foggy Path',
  levelType: LevelType.intro,
  problems: [
    _sub(16, 8), _sub(76, 8), _sub(64, 32), _sub(10, 6), _sub(19, 17),
    _sub(998, 997), _sub(834, 832), _sub(763, 760), _sub(128, 16), _sub(512, 256),
  ],
);

final _level14 = Level(
  number: 14,
  worldNumber: 2,
  levelInWorld: 4,
  name: 'Lily Pads',
  levelType: LevelType.build,
  problems: [
    _sub(0, 1), _sub(1, 3), _sub(8, 16), _sub(100, 200), _sub(13, 17),
    _sub(18, 22), _sub(5, 110), _sub(17, 127), _sub(128, 543), _sub(0, 888),
  ],
);

final _level15 = Level(
  number: 15,
  worldNumber: 2,
  levelInWorld: 5,
  name: 'Cypress Grove',
  levelType: LevelType.build,
  problems: [
    _sub(200, 100), _sub(500, 250), _sub(120, 50), _sub(750, 500), _sub(500, 800),
    _sub(30, 70), _sub(900, 901), _sub(250, 260), _sub(600, 900), _sub(80, 80),
  ],
);

final _level16 = Level(
  number: 16,
  worldNumber: 2,
  levelInWorld: 6,
  name: "Borrow's Hollow",
  levelType: LevelType.friend,
  problems: [
    _sub(50, 15), _sub(40, 24), _sub(17, 8), _sub(8, 17), _sub(0, 867),
    _sub(0, 42), _sub(25, 25), _sub(100, 234), _sub(764, 523), _sub(834, 398),
  ],
);

final _level17 = Level(
  number: 17,
  worldNumber: 2,
  levelInWorld: 7,
  name: 'Murky Depths',
  levelType: LevelType.challenge,
  problems: [
    _sub(396, 782), _sub(743, 172), _sub(983, 682), _sub(143, 259), _sub(238, 263),
    _sub(749, 260), _sub(154, 98), _sub(762, 871), _sub(954, 958), _sub(402, 678),
  ],
);

final _level18 = Level(
  number: 18,
  worldNumber: 2,
  levelInWorld: 8,
  name: 'Tangled Vines',
  levelType: LevelType.challenge,
  problems: [
    _sub(0, 20), _sub(-20, 90), _sub(-10, -5), _sub(-55, -70), _sub(-19, 10),
    _sub(20, -9), _sub(-15, 6), _sub(800, -100), _sub(0, -10), _sub(-21, -11),
  ],
);

final _level19 = Level(
  number: 19,
  worldNumber: 2,
  levelInWorld: 9,
  name: "Swamp's Heart",
  levelType: LevelType.preboss,
  problems: [
    _sub(750, 250), _sub(250, 500), _sub(1000, 500), _sub(800, 300), _sub(450, 150),
    _sub(450, 500), _sub(650, 450), _sub(50, 300), _sub(-100, 250), _sub(-500, 250),
  ],
);

final _level20 = Level(
  number: 20,
  worldNumber: 2,
  levelInWorld: 10,
  name: "Minus's Throne",
  levelType: LevelType.boss,
  timeLimit: 90,
  problems: [
    _sub(654, -909), _sub(-712, 163), _sub(-587, -822), _sub(-218, 390), _sub(-14, 962),
    _sub(-682, -17), _sub(-68, -923), _sub(234, 599), _sub(709, 603), _sub(-490, -385),
  ],
);

// =============================================================================
// WORLD 3: MULTIPLICATION MEADOWS (Levels 21-30)
// =============================================================================

final _level21 = Level(
  number: 21,
  worldNumber: 3,
  levelInWorld: 1,
  name: 'Flower Field',
  levelType: LevelType.intro,
  problems: [
    _mul(1, 1), _mul(0, 2), _mul(3, 0), _mul(1, 4), _mul(4, 1),
    _mul(1, 6), _mul(1, 9), _mul(12, 1), _mul(120, 1), _mul(1, 17),
  ],
);

final _level22 = Level(
  number: 22,
  worldNumber: 3,
  levelInWorld: 2,
  name: 'Butterfly Path',
  levelType: LevelType.intro,
  problems: [
    _mul(2, 3), _mul(2, 6), _mul(2, 10), _mul(2, 7), _mul(2, 9),
    _mul(2, 2), _mul(2, 1), _mul(13, 2), _mul(5, 2), _mul(8, 2),
  ],
);

final _level23 = Level(
  number: 23,
  worldNumber: 3,
  levelInWorld: 3,
  name: 'Clover Patch',
  levelType: LevelType.intro,
  problems: [
    _mul(3, 3), _mul(4, 3), _mul(5, 3), _mul(4, 4), _mul(6, 2),
    _mul(5, 4), _mul(3, 4), _mul(6, 3), _mul(5, 5), _mul(7, 2),
  ],
);

final _level24 = Level(
  number: 24,
  worldNumber: 3,
  levelInWorld: 4,
  name: 'Honeybee Hive',
  levelType: LevelType.build,
  problems: [
    _mul(4, 3), _mul(5, 3), _mul(4, 4), _mul(6, 3), _mul(5, 4),
    _mul(7, 3), _mul(4, 5), _mul(6, 4), _mul(5, 5), _mul(8, 3),
  ],
);

final _level25 = Level(
  number: 25,
  worldNumber: 3,
  levelInWorld: 5,
  name: 'Dandelion Dell',
  levelType: LevelType.build,
  problems: [
    _mul(5, -4), _mul(6, 3), _mul(-5, -5), _mul(7, 3), _mul(6, 4),
    _mul(-8, 3), _mul(4, 6), _mul(-7, -4), _mul(6, 5), _mul(9, 3),
  ],
);

final _level26 = Level(
  number: 26,
  worldNumber: 3,
  levelInWorld: 6,
  name: "Times's Burrow",
  levelType: LevelType.friend,
  problems: [
    _mul(4, 4), _mul(5, 4), _mul(6, 3), _mul(5, 5), _mul(7, 3),
    _mul(6, 4), _mul(4, 5), _mul(7, 4), _mul(6, 5), _mul(8, 4),
  ],
);

final _level27 = Level(
  number: 27,
  worldNumber: 3,
  levelInWorld: 7,
  name: 'Pollen Storm',
  levelType: LevelType.challenge,
  problems: [
    _mul(60, 4), _mul(12, 8), _mul(7, 9), _mul(4, 12), _mul(10, 5),
    _mul(9, 8), _mul(8, 8), _mul(32, 2), _mul(24, 3), _mul(9, 12),
  ],
);

final _level28 = Level(
  number: 28,
  worldNumber: 3,
  levelInWorld: 8,
  name: 'Rainbow Bridge',
  levelType: LevelType.challenge,
  problems: [
    _mul(14, 8), _mul(7, 21), _mul(18, 8), _mul(13, 3), _mul(9, 14),
    _mul(6, 17), _mul(-5, 17), _mul(-19, -5), _mul(14, -7), _mul(-20, -20),
  ],
);

final _level29 = Level(
  number: 29,
  worldNumber: 3,
  levelInWorld: 9,
  name: 'Final Bloom',
  levelType: LevelType.preboss,
  problems: [
    _mul(10, 50), _mul(40, 10), _mul(100, 6), _mul(18, 10), _mul(80, 2),
    _mul(40, 20), _mul(50, 15), _mul(13, 20), _mul(-20, 10), _mul(400, -2),
  ],
);

final _level30 = Level(
  number: 30,
  worldNumber: 3,
  levelInWorld: 10,
  name: "Calculata's Garden",
  levelType: LevelType.boss,
  timeLimit: 90,
  problems: [
    _mul(25, 12), _mul(34, 15), _mul(19, 23), _mul(74, 17), _mul(64, 9),
    _mul(7, 123), _mul(462, 87), _mul(239, 874), _mul(38, 18), _mul(873, 67),
  ],
);

// =============================================================================
// WORLD 4: DIVISION DESERT (Levels 31-40)
// =============================================================================

final _level31 = Level(
  number: 31,
  worldNumber: 4,
  levelInWorld: 1,
  name: 'Oasis Gate',
  levelType: LevelType.intro,
  problems: [
    _div(2, 1), _div(4, 2), _div(6, 2), _div(4, 1), _div(6, 3),
    _div(8, 2), _div(3, 1), _div(8, 4), _div(9, 3), _div(10, 2),
  ],
);

final _level32 = Level(
  number: 32,
  worldNumber: 4,
  levelInWorld: 2,
  name: 'Sandy Trail',
  levelType: LevelType.intro,
  problems: [
    _div(6, 2), _div(8, 2), _div(9, 3), _div(10, 2), _div(12, 3),
    _div(12, 4), _div(8, 4), _div(10, 5), _div(12, 2), _div(15, 3),
  ],
);

final _level33 = Level(
  number: 33,
  worldNumber: 4,
  levelInWorld: 3,
  name: 'Dune Ridge',
  levelType: LevelType.intro,
  problems: [
    _div(8, 2), _div(10, 2), _div(12, 3), _div(12, 4), _div(14, 2),
    _div(16, 4), _div(9, 3), _div(15, 5), _div(16, 2), _div(18, 3),
  ],
);

final _level34 = Level(
  number: 34,
  worldNumber: 4,
  levelInWorld: 4,
  name: 'Scorpion Pass',
  levelType: LevelType.build,
  problems: [
    _div(10, 2), _div(12, 3), _div(14, 2), _div(15, 3), _div(16, 4),
    _div(18, 2), _div(12, 4), _div(20, 4), _div(18, 3), _div(20, 5),
  ],
);

final _level35 = Level(
  number: 35,
  worldNumber: 4,
  levelInWorld: 5,
  name: 'Mirage Valley',
  levelType: LevelType.build,
  problems: [
    _div(12, 3), _div(14, 2), _div(16, 4), _div(18, 3), _div(20, 4),
    _div(21, 3), _div(15, 5), _div(24, 4), _div(20, 5), _div(24, 3),
  ],
);

final _level36 = Level(
  number: 36,
  worldNumber: 4,
  levelInWorld: 6,
  name: "Remainder's Rest",
  levelType: LevelType.friend,
  problems: [
    _div(10, 2), _div(12, 3), _div(15, 3), _div(16, 4), _div(18, 2),
    _div(20, 4), _div(14, 2), _div(21, 3), _div(24, 4), _div(25, 5),
  ],
);

final _level37 = Level(
  number: 37,
  worldNumber: 4,
  levelInWorld: 7,
  name: 'Sandstorm',
  levelType: LevelType.challenge,
  problems: [
    _div(14, 2), _div(18, 3), _div(20, 4), _div(21, 3), _div(24, 4),
    _div(27, 3), _div(16, 4), _div(28, 4), _div(30, 5), _div(32, 4),
  ],
);

final _level38 = Level(
  number: 38,
  worldNumber: 4,
  levelInWorld: 8,
  name: 'Sunscorch',
  levelType: LevelType.challenge,
  problems: [
    _div(18, 3), _div(24, 4), _div(25, 5), _div(27, 3), _div(28, 4),
    _div(36, 4), _div(20, 4), _div(30, 5), _div(35, 5), _div(36, 6),
  ],
);

final _level39 = Level(
  number: 39,
  worldNumber: 4,
  levelInWorld: 9,
  name: "Pyramid's Shadow",
  levelType: LevelType.preboss,
  problems: [
    _div(24, 4), _div(27, 3), _div(30, 5), _div(32, 4), _div(35, 5),
    _div(42, 6), _div(28, 4), _div(36, 4), _div(40, 5), _div(45, 5),
  ],
);

final _level40 = Level(
  number: 40,
  worldNumber: 4,
  levelInWorld: 10,
  name: "Sphinx's Riddles",
  levelType: LevelType.boss,
  timeLimit: 90,
  problems: [
    _div(18, 3), _div(24, 4), _div(27, 3), _div(28, 4), _div(30, 5),
    _div(35, 5), _div(36, 4), _div(40, 5), _div(42, 6), _div(48, 6),
  ],
);

/// All levels in order.
final List<Level> levels = [
  // World 1: Addition Alps
  _level1, _level2, _level3, _level4, _level5,
  _level6, _level7, _level8, _level9, _level10,
  // World 2: Subtraction Swamp
  _level11, _level12, _level13, _level14, _level15,
  _level16, _level17, _level18, _level19, _level20,
  // World 3: Multiplication Meadows
  _level21, _level22, _level23, _level24, _level25,
  _level26, _level27, _level28, _level29, _level30,
  // World 4: Division Desert
  _level31, _level32, _level33, _level34, _level35,
  _level36, _level37, _level38, _level39, _level40,
];

/// Get level by number. Returns null if level doesn't exist.
Level? getLevel(int levelNum) {
  for (final level in levels) {
    if (level.number == levelNum) {
      return level;
    }
  }
  return null;
}

/// Get the next level after the current one. Returns null if no more levels.
Level? getNextLevel(int currentLevel) {
  return getLevel(currentLevel + 1);
}

/// Return total number of levels available.
int getTotalLevels() {
  return levels.length;
}

/// Get all levels in a specific world.
List<Level> getLevelsForWorld(int worldNum) {
  return levels.where((level) => level.worldNumber == worldNum).toList();
}
