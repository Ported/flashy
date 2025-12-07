import 'package:flutter_test/flutter_test.dart';
import 'package:flashy_app/core/scoring.dart';

void main() {
  group('calculateScore', () {
    test('incorrect answer scores zero', () {
      expect(
        calculateScore(1.0, isCorrect: false, streak: 0),
        equals(0),
      );
      expect(
        calculateScore(1.0, isCorrect: false, streak: 10),
        equals(0),
      );
    });

    test('correct answer base points', () {
      // Slow answer (no speed bonus), no streak
      final score = calculateScore(10.0, isCorrect: true, streak: 0);
      expect(score, equals(basePoints));
    });

    test('fast answer bonus', () {
      // Under fastThreshold gets fastBonus
      final score = calculateScore(
        fastThreshold - 0.5,
        isCorrect: true,
        streak: 0,
      );
      expect(score, equals((basePoints * fastBonus).toInt()));
    });

    test('medium answer bonus', () {
      // Between FAST and MEDIUM threshold gets mediumBonus
      final time = (fastThreshold + mediumThreshold) / 2;
      final score = calculateScore(time, isCorrect: true, streak: 0);
      expect(score, equals((basePoints * mediumBonus).toInt()));
    });

    test('slow answer no bonus', () {
      // Over mediumThreshold gets no bonus
      final score = calculateScore(
        mediumThreshold + 1,
        isCorrect: true,
        streak: 0,
      );
      expect(score, equals(basePoints));
    });

    test('streak multiplier applied', () {
      // With streak of 5, should get 2x multiplier
      final scoreNoStreak = calculateScore(10.0, isCorrect: true, streak: 0);
      final scoreWithStreak = calculateScore(10.0, isCorrect: true, streak: 5);
      expect(scoreWithStreak, equals(scoreNoStreak * 2));
    });

    test('speed and streak combine', () {
      // Fast answer with streak should combine bonuses
      final score = calculateScore(
        fastThreshold - 0.5,
        isCorrect: true,
        streak: 5,
      );
      final expected = (basePoints * fastBonus * 2.0).toInt(); // 2x streak
      expect(score, equals(expected));
    });
  });

  group('getStreakMultiplier', () {
    test('no streak', () {
      expect(getStreakMultiplier(0), equals(1.0));
      expect(getStreakMultiplier(1), equals(1.0));
      expect(getStreakMultiplier(2), equals(1.0));
    });

    test('small streak', () {
      expect(getStreakMultiplier(3), equals(1.5));
      expect(getStreakMultiplier(4), equals(1.5));
    });

    test('medium streak', () {
      expect(getStreakMultiplier(5), equals(2.0));
      expect(getStreakMultiplier(9), equals(2.0));
    });

    test('large streak', () {
      expect(getStreakMultiplier(10), equals(3.0));
      expect(getStreakMultiplier(100), equals(3.0));
    });
  });

  group('calculateStars', () {
    test('zero total returns zero stars', () {
      expect(calculateStars(0, 0, 0.0), equals(0));
    });

    test('perfect and fast gets 3 stars', () {
      // 10/10 correct, 3 seconds per problem average
      expect(calculateStars(10, 10, 30.0), equals(3));
    });

    test('perfect but slow gets 2 stars', () {
      // 10/10 correct, 10 seconds per problem average
      expect(calculateStars(10, 10, 100.0), equals(2));
    });

    test('80 percent correct gets 2 stars', () {
      // 8/10 correct
      expect(calculateStars(8, 10, 50.0), equals(2));
    });

    test('60 percent correct gets 1 star', () {
      // 6/10 correct
      expect(calculateStars(6, 10, 50.0), equals(1));
    });

    test('below 60 percent gets 0 stars', () {
      // 5/10 correct
      expect(calculateStars(5, 10, 50.0), equals(0));
    });
  });
}
