import 'package:flutter_test/flutter_test.dart';
import 'package:flashy_app/core/levels.dart';
import 'package:flashy_app/core/problems.dart';

void main() {
  group('Levels', () {
    test('levels are numbered sequentially', () {
      for (var i = 0; i < levels.length; i++) {
        expect(levels[i].number, equals(i + 1));
      }
    });

    test('all levels have problems', () {
      for (final level in levels) {
        expect(level.problems.isNotEmpty, isTrue);
      }
    });

    test('all levels have 10 problems', () {
      for (final level in levels) {
        expect(level.problems.length, equals(10));
      }
    });

    test('first level is addition', () {
      final first = levels[0];
      for (final problem in first.problems) {
        expect(problem.operation, equals(Operation.add));
      }
    });

    test('world 1 levels are addition', () {
      final world1Levels = getLevelsForWorld(1);
      for (final level in world1Levels) {
        for (final problem in level.problems) {
          expect(problem.operation, equals(Operation.add));
        }
      }
    });

    test('boss levels have time limit', () {
      for (final level in levels) {
        if (level.levelType == LevelType.boss) {
          expect(level.timeLimit, isNotNull);
          expect(level.timeLimit, greaterThan(0));
        }
      }
    });

    test('non-boss levels have no time limit', () {
      for (final level in levels) {
        if (level.levelType != LevelType.boss) {
          expect(level.timeLimit, isNull);
        }
      }
    });
  });

  group('getLevel', () {
    test('get existing level', () {
      final level = getLevel(1);
      expect(level, isNotNull);
      expect(level!.number, equals(1));
    });

    test('get nonexistent level', () {
      final level = getLevel(999);
      expect(level, isNull);
    });

    test('get level zero', () {
      final level = getLevel(0);
      expect(level, isNull);
    });
  });

  group('getNextLevel', () {
    test('next level exists', () {
      final nextLevel = getNextLevel(1);
      expect(nextLevel, isNotNull);
      expect(nextLevel!.number, equals(2));
    });

    test('no next level after last', () {
      final lastLevelNum = levels.length;
      final nextLevel = getNextLevel(lastLevelNum);
      expect(nextLevel, isNull);
    });
  });

  group('getTotalLevels', () {
    test('total matches levels list', () {
      expect(getTotalLevels(), equals(levels.length));
    });

    test('total is positive', () {
      expect(getTotalLevels(), greaterThan(0));
    });

    test('total is 40', () {
      expect(getTotalLevels(), equals(40));
    });
  });

  group('getLevelsForWorld', () {
    test('world 1 has 10 levels', () {
      final world1Levels = getLevelsForWorld(1);
      expect(world1Levels.length, equals(10));
    });

    test('world 1 levels numbered 1 to 10', () {
      final world1Levels = getLevelsForWorld(1);
      final numbers = world1Levels.map((l) => l.number).toList();
      expect(numbers, equals(List.generate(10, (i) => i + 1)));
    });

    test('nonexistent world returns empty', () {
      final world99Levels = getLevelsForWorld(99);
      expect(world99Levels, isEmpty);
    });
  });
}
