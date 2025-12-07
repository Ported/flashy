import 'package:flutter_test/flutter_test.dart';
import 'package:flashy_app/core/models.dart';

void main() {
  group('PlayerProgress stars', () {
    test('get stars default zero', () {
      final progress = PlayerProgress();
      expect(progress.getStars(1), equals(0));
    });

    test('set stars', () {
      final progress = PlayerProgress();
      progress.setStars(1, 3);
      expect(progress.getStars(1), equals(3));
    });

    test('set stars keeps best', () {
      final progress = PlayerProgress();
      progress.setStars(1, 3);
      progress.setStars(1, 2); // Worse score
      expect(progress.getStars(1), equals(3)); // Still 3
    });

    test('set stars updates if better', () {
      final progress = PlayerProgress();
      progress.setStars(1, 2);
      progress.setStars(1, 3); // Better score
      expect(progress.getStars(1), equals(3));
    });
  });

  group('PlayerProgress best scores', () {
    test('get best score default zero', () {
      final progress = PlayerProgress();
      expect(progress.getBestScore(1), equals(0));
    });

    test('set best score', () {
      final progress = PlayerProgress();
      progress.setBestScore(1, 2700);
      expect(progress.getBestScore(1), equals(2700));
    });

    test('set best score keeps best', () {
      final progress = PlayerProgress();
      progress.setBestScore(1, 2700);
      progress.setBestScore(1, 2500); // Worse score
      expect(progress.getBestScore(1), equals(2700)); // Still 2700
    });

    test('set best score updates if better', () {
      final progress = PlayerProgress();
      progress.setBestScore(1, 2500);
      progress.setBestScore(1, 2700); // Better score
      expect(progress.getBestScore(1), equals(2700));
    });

    test('get total best score empty', () {
      final progress = PlayerProgress();
      expect(progress.getTotalBestScore(), equals(0));
    });

    test('get total best score single level', () {
      final progress = PlayerProgress();
      progress.setBestScore(1, 2700);
      expect(progress.getTotalBestScore(), equals(2700));
    });

    test('get total best score multiple levels', () {
      final progress = PlayerProgress();
      progress.setBestScore(1, 2700);
      progress.setBestScore(2, 2500);
      progress.setBestScore(3, 2800);
      expect(progress.getTotalBestScore(), equals(8000));
    });

    test('total score only counts best per level', () {
      final progress = PlayerProgress();
      // Play level 1 three times
      progress.setBestScore(1, 2500);
      progress.setBestScore(1, 2700); // Better
      progress.setBestScore(1, 2600); // Worse than best
      // Play level 2 once
      progress.setBestScore(2, 2400);

      // Total should be best of level 1 (2700) + level 2 (2400)
      expect(progress.getTotalBestScore(), equals(5100));
    });
  });

  group('PlayerProgress unlocked', () {
    test('level 1 always unlocked', () {
      final progress = PlayerProgress();
      expect(progress.isUnlocked(1), isTrue);
    });

    test('level 2 locked initially', () {
      final progress = PlayerProgress();
      expect(progress.isUnlocked(2), isFalse);
    });

    test('level 2 unlocked after 2 stars on 1', () {
      final progress = PlayerProgress();
      progress.setStars(1, 2);
      expect(progress.isUnlocked(2), isTrue);
    });

    test('get highest unlocked initial', () {
      final progress = PlayerProgress();
      expect(progress.getHighestUnlocked(), equals(1));
    });

    test('get highest unlocked after progress', () {
      final progress = PlayerProgress();
      progress.setStars(1, 3);
      progress.setStars(2, 2);
      expect(progress.getHighestUnlocked(), equals(3));
    });
  });

  group('PlayerProgress serialization', () {
    test('serialize and deserialize', () {
      final progress = PlayerProgress();
      progress.setStars(1, 3);
      progress.setStars(2, 2);
      progress.setBestScore(1, 2700);
      progress.setBestScore(2, 2500);

      final serialized = progress.serialize();
      final restored = PlayerProgress.deserialize(serialized);

      expect(restored.getStars(1), equals(3));
      expect(restored.getStars(2), equals(2));
      expect(restored.getBestScore(1), equals(2700));
      expect(restored.getBestScore(2), equals(2500));
    });

    test('deserialize empty', () {
      final progress = PlayerProgress.deserialize('{}');
      expect(progress.getStars(1), equals(0));
      expect(progress.getBestScore(1), equals(0));
    });
  });
}
