import 'package:flutter_test/flutter_test.dart';
import 'package:flashy_app/core/game.dart';
import 'package:flashy_app/core/models.dart';
import 'package:flashy_app/core/storage.dart';

void main() {
  group('GameController', () {
    test('init loads level', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);
      expect(controller.level, isNotNull);
      expect(controller.level.number, equals(1));
      expect(controller.problemIndex, equals(0));
      expect(controller.totalScore, equals(0));
      expect(controller.streak, equals(0));
    });

    test('init invalid level throws', () {
      expect(
        () => GameController(playerName: 'test_player', levelNumber: 999),
        throwsA(isA<ArgumentError>()),
      );
    });

    test('current problem returns first', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);
      final problem = controller.currentProblem;
      expect(problem, isNotNull);
      expect(problem, equals(controller.level.problems[0]));
    });

    test('is complete initially false', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);
      expect(controller.isComplete, isFalse);
    });

    test('total problems', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);
      expect(controller.totalProblems, equals(controller.level.problems.length));
    });

    test('submit correct answer', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);
      final problem = controller.currentProblem!;

      final feedback = controller.submitAnswer(problem.answer, timeTaken: 2.0);

      expect(feedback.isCorrect, isTrue);
      expect(feedback.correctAnswer, equals(problem.answer));
      expect(feedback.pointsEarned, greaterThan(0));
      expect(feedback.streak, equals(1));
    });

    test('submit wrong answer', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);
      final problem = controller.currentProblem!;

      final wrongAnswer = problem.answer + 100;
      final feedback = controller.submitAnswer(wrongAnswer, timeTaken: 2.0);

      expect(feedback.isCorrect, isFalse);
      expect(feedback.correctAnswer, equals(problem.answer));
      expect(feedback.pointsEarned, equals(0));
      expect(feedback.streak, equals(0));
    });

    test('submit null answer is wrong', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);
      final feedback = controller.submitAnswer(null, timeTaken: 2.0);

      expect(feedback.isCorrect, isFalse);
      expect(feedback.pointsEarned, equals(0));
    });

    test('streak builds on correct', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);

      // Answer first 3 correctly
      late AnswerFeedback feedback;
      for (var i = 0; i < 3; i++) {
        final problem = controller.currentProblem;
        if (problem == null) break;
        feedback = controller.submitAnswer(problem.answer, timeTaken: 2.0);
      }

      expect(feedback.streak, equals(3));
      expect(controller.bestStreak, equals(3));
    });

    test('streak resets on wrong', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);

      // Get 2 correct
      for (var i = 0; i < 2; i++) {
        final problem = controller.currentProblem;
        if (problem == null) break;
        controller.submitAnswer(problem.answer, timeTaken: 2.0);
      }

      expect(controller.streak, equals(2));

      // Get one wrong
      final problem = controller.currentProblem;
      if (problem != null) {
        final feedback = controller.submitAnswer(problem.answer + 100, timeTaken: 2.0);
        expect(feedback.streak, equals(0));
        expect(controller.bestStreak, equals(2)); // Best preserved
      }
    });

    test('total score accumulates', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);

      var total = 0;
      for (var i = 0; i < 3; i++) {
        final problem = controller.currentProblem;
        if (problem == null) break;
        final feedback = controller.submitAnswer(problem.answer, timeTaken: 2.0);
        total += feedback.pointsEarned;
      }

      expect(controller.totalScore, equals(total));
      expect(controller.totalScore, greaterThan(0));
    });

    test('correct count', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);

      // 2 correct, 1 wrong
      for (var i = 0; i < 3; i++) {
        final problem = controller.currentProblem;
        if (problem == null) break;
        if (i < 2) {
          controller.submitAnswer(problem.answer, timeTaken: 2.0);
        } else {
          controller.submitAnswer(problem.answer + 100, timeTaken: 2.0);
        }
      }

      expect(controller.correctCount, equals(2));
      expect(controller.problemsAnswered, equals(3));
    });

    test('problem advances after answer', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);

      final firstProblem = controller.currentProblem;
      controller.submitAnswer(0, timeTaken: 1.0); // Wrong answer
      final secondProblem = controller.currentProblem;

      expect(firstProblem, isNot(equals(secondProblem)));
      expect(controller.problemIndex, equals(1));
    });

    test('is complete after all answered', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);

      for (var i = 0; i < controller.totalProblems; i++) {
        final problem = controller.currentProblem;
        if (problem == null) break;
        controller.submitAnswer(problem.answer, timeTaken: 1.0);
      }

      expect(controller.isComplete, isTrue);
      expect(controller.currentProblem, isNull);
    });

    test('submit after complete throws', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);

      // Complete all problems
      for (var i = 0; i < controller.totalProblems; i++) {
        final problem = controller.currentProblem;
        if (problem == null) break;
        controller.submitAnswer(problem.answer, timeTaken: 1.0);
      }

      expect(
        () => controller.submitAnswer(5, timeTaken: 1.0),
        throwsStateError,
      );
    });

    test('finish saves progress', () async {
      final mockStorage = MemoryStorageBackend();
      await mockStorage.saveProgress('test_player', PlayerProgress());

      final controller = GameController(
        playerName: 'test_player',
        levelNumber: 1,
        storage: mockStorage,
      );

      // Answer all correctly
      for (var i = 0; i < controller.totalProblems; i++) {
        final problem = controller.currentProblem;
        if (problem == null) break;
        controller.submitAnswer(problem.answer, timeTaken: 2.0);
      }

      final (stars, _) = await controller.finish();

      expect(stars, greaterThanOrEqualTo(0));

      // Verify progress was saved
      final savedProgress = await mockStorage.loadProgress('test_player');
      expect(savedProgress, isNotNull);
      expect(savedProgress!.getStars(1), greaterThan(0));
    });

    test('finish returns stars', () async {
      final mockStorage = MemoryStorageBackend();
      await mockStorage.saveProgress('test_player', PlayerProgress());

      final controller = GameController(
        playerName: 'test_player',
        levelNumber: 1,
        storage: mockStorage,
      );

      // Answer all correctly and fast for 3 stars
      for (var i = 0; i < controller.totalProblems; i++) {
        final problem = controller.currentProblem;
        if (problem == null) break;
        controller.submitAnswer(problem.answer, timeTaken: 1.0);
      }

      final (stars, _) = await controller.finish();
      expect(stars, equals(3)); // Perfect and fast
    });

    test('results recorded', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);

      final problem = controller.currentProblem!;
      controller.submitAnswer(problem.answer, timeTaken: 2.5);

      expect(controller.results.length, equals(1));
      final result = controller.results[0];
      expect(result.isCorrect, isTrue);
      expect(result.correctAnswer, equals(problem.answer));
      expect(result.givenAnswer, equals(problem.answer));
      expect(result.timeSeconds, equals(2.5));
      expect(result.points, greaterThan(0));
    });
  });

  group('Timed levels', () {
    test('regular level not timed', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);
      expect(controller.isTimed, isFalse);
      expect(controller.timeLimit, isNull);
    });

    test('boss level is timed', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 10);
      expect(controller.isTimed, isTrue);
      expect(controller.timeLimit, equals(90));
    });

    test('time remaining untimed', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);
      expect(controller.timeRemaining(50.0), equals(double.infinity));
    });

    test('time remaining timed', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 10);
      expect(controller.timeRemaining(0.0), equals(90.0));
      expect(controller.timeRemaining(30.0), equals(60.0));
      expect(controller.timeRemaining(90.0), equals(0.0));
      expect(controller.timeRemaining(100.0), equals(0.0)); // Clamped to 0
    });

    test('is time expired untimed', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);
      expect(controller.isTimeExpired(1000.0), isFalse);
    });

    test('is time expired timed', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 10);
      expect(controller.isTimeExpired(89.0), isFalse);
      expect(controller.isTimeExpired(90.0), isTrue);
      expect(controller.isTimeExpired(91.0), isTrue);
    });
  });

  group('AnswerFeedback', () {
    test('feedback fields', () {
      const feedback = AnswerFeedback(
        isCorrect: true,
        pointsEarned: 150,
        correctAnswer: 7,
        streak: 3,
        streakMultiplier: 1.5,
      );

      expect(feedback.isCorrect, isTrue);
      expect(feedback.pointsEarned, equals(150));
      expect(feedback.correctAnswer, equals(7));
      expect(feedback.streak, equals(3));
      expect(feedback.streakMultiplier, equals(1.5));
    });
  });

  group('Cheat methods', () {
    test('cheat pass all', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);
      controller.cheatPassAll();

      expect(controller.isComplete, isTrue);
      expect(controller.correctCount, equals(controller.totalProblems));
    });

    test('cheat fail all', () {
      final controller = GameController(playerName: 'test_player', levelNumber: 1);
      controller.cheatFailAll();

      expect(controller.isComplete, isTrue);
      expect(controller.correctCount, equals(0));
    });
  });
}
