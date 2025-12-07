// Game controller - manages game lifecycle for a level attempt.
import 'levels.dart';
import 'models.dart';
import 'problems.dart';
import 'scoring.dart';
import 'storage.dart';

/// Feedback from submitting an answer.
class AnswerFeedback {
  const AnswerFeedback({
    required this.isCorrect,
    required this.pointsEarned,
    required this.correctAnswer,
    required this.streak,
    required this.streakMultiplier,
  });

  final bool isCorrect;
  final int pointsEarned;
  final int correctAnswer;
  final int streak;
  final double streakMultiplier;
}

/// Controls game lifecycle for a single level attempt.
///
/// The controller owns all game state and logic:
/// - Serving problems
/// - Receiving and validating answers
/// - Calculating scores with streak bonuses
/// - Saving progress and history
///
/// The UI should just display controller state and route input.
class GameController {
  GameController({
    required this.playerName,
    required int levelNumber,
    StorageBackend? storage,
  })  : _levelNumber = levelNumber,
        _storage = storage {
    final level = getLevel(levelNumber);
    if (level == null) {
      throw ArgumentError('Level $levelNumber not found');
    }
    this.level = level;
  }

  final String playerName;
  final int _levelNumber;
  final StorageBackend? _storage;

  late final Level level;
  int _problemIndex = 0;
  final List<ProblemResult> _results = [];
  int _totalScore = 0;
  int _streak = 0;
  int _bestStreak = 0;
  double _totalTime = 0.0;

  /// Get the level number.
  int get levelNumber => _levelNumber;

  /// Get the current problem index.
  int get problemIndex => _problemIndex;

  /// Get the list of results.
  List<ProblemResult> get results => List.unmodifiable(_results);

  /// Get total score.
  int get totalScore => _totalScore;

  /// Get current streak.
  int get streak => _streak;

  /// Get best streak achieved.
  int get bestStreak => _bestStreak;

  /// Get total time spent.
  double get totalTime => _totalTime;

  /// Get current problem, or null if complete.
  Problem? get currentProblem {
    if (_problemIndex >= level.problems.length) {
      return null;
    }
    return level.problems[_problemIndex];
  }

  /// Check if all problems have been answered.
  bool get isComplete => _problemIndex >= level.problems.length;

  /// Count of correct answers so far.
  int get correctCount => _results.where((r) => r.isCorrect).length;

  /// Number of problems answered so far.
  int get problemsAnswered => _results.length;

  /// Total number of problems in this level.
  int get totalProblems => level.problems.length;

  /// Time limit in seconds for this level, or null if untimed.
  int? get timeLimit => level.timeLimit;

  /// Check if this level has a time limit (boss battle).
  bool get isTimed => level.timeLimit != null;

  /// Get remaining time given elapsed wall-clock seconds.
  ///
  /// [elapsed] Seconds since level started.
  ///
  /// Returns remaining seconds, or infinity if untimed.
  double timeRemaining(double elapsed) {
    if (level.timeLimit == null) {
      return double.infinity;
    }
    final remaining = level.timeLimit! - elapsed;
    return remaining > 0 ? remaining : 0.0;
  }

  /// Check if time has expired.
  ///
  /// [elapsed] Seconds since level started.
  ///
  /// Returns true if timed level and time has run out.
  bool isTimeExpired(double elapsed) {
    if (level.timeLimit == null) {
      return false;
    }
    return elapsed >= level.timeLimit!;
  }

  /// Submit answer for current problem.
  ///
  /// [answer] The answer given (null if skipped).
  /// [timeTaken] Time in seconds to answer.
  ///
  /// Returns AnswerFeedback with result details.
  AnswerFeedback submitAnswer(int? answer, {required double timeTaken}) {
    final problem = currentProblem;
    if (problem == null) {
      throw StateError('No current problem - game is complete');
    }

    // For numpad input, we use exact matching (no fuzzy voice matching)
    final isCorrect = answer != null && answer == problem.answer;

    // Update streak
    if (isCorrect) {
      _streak += 1;
      if (_streak > _bestStreak) {
        _bestStreak = _streak;
      }
    } else {
      _streak = 0;
    }

    // Calculate score using scoring module
    final points = calculateScore(
      timeTaken,
      isCorrect: isCorrect,
      streak: _streak,
    );
    _totalScore += points;
    _totalTime += timeTaken;

    // Record result
    _results.add(
      ProblemResult(
        problem: problem.display(),
        correctAnswer: problem.answer,
        givenAnswer: answer,
        isCorrect: isCorrect,
        timeSeconds: timeTaken,
        points: points,
      ),
    );

    // Advance to next problem
    _problemIndex += 1;

    return AnswerFeedback(
      isCorrect: isCorrect,
      pointsEarned: points,
      correctAnswer: problem.answer,
      streak: _streak,
      streakMultiplier: getStreakMultiplier(_streak),
    );
  }

  /// Finish the level. Saves progress and history.
  ///
  /// Returns tuple of (stars earned, is_new_best).
  Future<(int, bool)> finish() async {
    final stars = calculateStars(correctCount, totalProblems, _totalTime);

    final storage = _storage;
    if (storage != null) {
      // Save progress via storage backend
      final progress = await storage.loadProgress(playerName);
      final actualProgress = progress ?? PlayerProgress();
      final oldStars = actualProgress.getStars(_levelNumber);
      actualProgress.setStars(_levelNumber, stars);
      actualProgress.setBestScore(_levelNumber, _totalScore);
      await storage.saveProgress(playerName, actualProgress);

      return (stars, stars > oldStars);
    }

    // No storage - just return stars
    return (stars, true);
  }

  // --- Cheat methods for dev/testing ---

  /// Complete all remaining problems with correct answers.
  ///
  /// Useful for testing progression without playing through levels.
  void cheatPassAll() {
    while (!isComplete) {
      final problem = currentProblem;
      if (problem != null) {
        submitAnswer(problem.answer, timeTaken: 1.0);
      }
    }
  }

  /// Complete all remaining problems with wrong answers.
  ///
  /// Useful for testing failure states.
  void cheatFailAll() {
    while (!isComplete) {
      final problem = currentProblem;
      if (problem != null) {
        submitAnswer(problem.answer + 999, timeTaken: 1.0);
      }
    }
  }
}
