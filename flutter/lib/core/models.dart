// Data models for game state - pure data, no I/O.
import 'dart:convert';

/// Player's game progress - stars, best scores, and unlocked levels.
class PlayerProgress {
  PlayerProgress({
    Map<int, int>? stars,
    Map<int, int>? bestScores,
  })  : _stars = stars ?? {},
        _bestScores = bestScores ?? {};

  final Map<int, int> _stars; // level_number -> stars (1-3)
  final Map<int, int> _bestScores; // level_number -> score

  /// Read-only access to stars map.
  Map<int, int> get stars => Map.unmodifiable(_stars);

  /// Read-only access to best scores map.
  Map<int, int> get bestScores => Map.unmodifiable(_bestScores);

  /// Get stars for a level (0 if not completed).
  int getStars(int level) {
    return _stars[level] ?? 0;
  }

  /// Set stars for a level, keeping the best.
  void setStars(int level, int stars) {
    final current = _stars[level] ?? 0;
    if (stars > current) {
      _stars[level] = stars;
    }
  }

  /// Get best score for a level (0 if not completed).
  int getBestScore(int level) {
    return _bestScores[level] ?? 0;
  }

  /// Set best score for a level, keeping the best.
  void setBestScore(int level, int score) {
    final current = _bestScores[level] ?? 0;
    if (score > current) {
      _bestScores[level] = score;
    }
  }

  /// Get sum of best scores across all levels.
  int getTotalBestScore() {
    return _bestScores.values.fold(0, (sum, score) => sum + score);
  }

  /// Get the highest level that has been unlocked.
  int getHighestUnlocked() {
    if (_stars.isEmpty) {
      return 1; // Start with level 1 unlocked
    }

    // Find highest completed level with 2+ stars
    var highest = 0;
    for (final entry in _stars.entries) {
      if (entry.value >= 2) {
        if (entry.key > highest) {
          highest = entry.key;
        }
      }
    }

    // Next level after highest completed is unlocked
    return highest + 1;
  }

  /// Check if a level is unlocked (playable).
  bool isUnlocked(int level) {
    if (level == 1) {
      return true;
    }
    // Level is unlocked if previous level has 2+ stars
    return getStars(level - 1) >= 2;
  }

  /// Get total stars earned across all levels.
  int getTotalStars() {
    return _stars.values.fold(0, (sum, stars) => sum + stars);
  }

  /// Convert to JSON for storage.
  Map<String, dynamic> toJson() {
    return {
      'stars': _stars.map((k, v) => MapEntry(k.toString(), v)),
      'best_scores': _bestScores.map((k, v) => MapEntry(k.toString(), v)),
    };
  }

  /// Create from JSON.
  factory PlayerProgress.fromJson(Map<String, dynamic> json) {
    final starsData = json['stars'] as Map<String, dynamic>? ?? {};
    final scoresData = json['best_scores'] as Map<String, dynamic>? ?? {};

    return PlayerProgress(
      stars: starsData.map((k, v) => MapEntry(int.parse(k), v as int)),
      bestScores: scoresData.map((k, v) => MapEntry(int.parse(k), v as int)),
    );
  }

  /// Serialize to JSON string.
  String serialize() {
    return jsonEncode(toJson());
  }

  /// Deserialize from JSON string.
  factory PlayerProgress.deserialize(String data) {
    return PlayerProgress.fromJson(jsonDecode(data) as Map<String, dynamic>);
  }
}

/// Result of a single problem attempt.
class ProblemResult {
  const ProblemResult({
    required this.problem,
    required this.correctAnswer,
    required this.givenAnswer,
    required this.isCorrect,
    required this.timeSeconds,
    required this.points,
  });

  final String problem;
  final int correctAnswer;
  final int? givenAnswer;
  final bool isCorrect;
  final double timeSeconds;
  final int points;

  /// Convert to JSON for storage.
  Map<String, dynamic> toJson() {
    return {
      'problem': problem,
      'correct_answer': correctAnswer,
      'given_answer': givenAnswer,
      'is_correct': isCorrect,
      'time_seconds': timeSeconds,
      'points': points,
    };
  }

  /// Create from JSON.
  factory ProblemResult.fromJson(Map<String, dynamic> json) {
    return ProblemResult(
      problem: json['problem'] as String,
      correctAnswer: json['correct_answer'] as int,
      givenAnswer: json['given_answer'] as int?,
      isCorrect: json['is_correct'] as bool,
      timeSeconds: (json['time_seconds'] as num).toDouble(),
      points: json['points'] as int,
    );
  }
}

/// Result of completing a level.
class LevelResult {
  const LevelResult({
    required this.levelNumber,
    required this.levelName,
    required this.totalScore,
    required this.correctCount,
    required this.totalProblems,
    required this.bestStreak,
    required this.totalTimeSeconds,
    required this.problems,
  });

  final int levelNumber;
  final String levelName;
  final int totalScore;
  final int correctCount;
  final int totalProblems;
  final int bestStreak;
  final double totalTimeSeconds;
  final List<ProblemResult> problems;
}
