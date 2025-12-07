// Score calculation - pure functions for computing points.

/// Base points for a correct answer.
const int basePoints = 100;

/// Time thresholds for speed bonus (in seconds).
const double fastThreshold = 2.0; // Under 2 seconds = fast
const double mediumThreshold = 5.0; // Under 5 seconds = medium

/// Speed bonus multipliers.
const double fastBonus = 1.5;
const double mediumBonus = 1.2;

/// Streak multipliers: (threshold, multiplier).
const List<(int, double)> streakThresholds = [
  (3, 1.5), // 3+ streak = 1.5x
  (5, 2.0), // 5+ streak = 2x
  (10, 3.0), // 10+ streak = 3x
];

/// Calculate points for a single problem.
///
/// [timeTaken] Time in seconds to answer.
/// [isCorrect] Whether the answer was correct.
/// [streak] Current streak count (consecutive correct answers).
///
/// Returns points earned (0 if incorrect).
int calculateScore(double timeTaken, {required bool isCorrect, required int streak}) {
  if (!isCorrect) {
    return 0;
  }

  var points = basePoints.toDouble();

  // Apply speed bonus
  if (timeTaken < fastThreshold) {
    points *= fastBonus;
  } else if (timeTaken < mediumThreshold) {
    points *= mediumBonus;
  }

  // Apply streak multiplier
  final streakMultiplier = getStreakMultiplier(streak);
  points *= streakMultiplier;

  return points.toInt();
}

/// Get the multiplier for the current streak.
double getStreakMultiplier(int streak) {
  var multiplier = 1.0;
  for (final (threshold, mult) in streakThresholds) {
    if (streak >= threshold) {
      multiplier = mult;
    }
  }
  return multiplier;
}

/// Star thresholds.
const double star3Accuracy = 1.0; // 100% correct
const double star3TimePerProblem = 5.0; // Average under 5 seconds per problem
const double star2Accuracy = 0.8; // 80% correct
const double star1Accuracy = 0.6; // 60% correct

/// Calculate stars earned for a level.
///
/// [correct] Number of correct answers.
/// [total] Total number of problems.
/// [totalTime] Total time taken in seconds.
///
/// Returns stars earned (0-3):
/// - 3 stars: 100% correct AND fast (under 5s per problem average)
/// - 2 stars: 80%+ correct OR 100% correct but slow
/// - 1 star: 60%+ correct
/// - 0 stars: Below 60% (level not passed)
int calculateStars(int correct, int total, double totalTime) {
  if (total == 0) {
    return 0;
  }

  final accuracy = correct / total;
  final avgTime = totalTime / total;

  // 3 stars: perfect AND fast
  if (accuracy >= star3Accuracy && avgTime <= star3TimePerProblem) {
    return 3;
  }

  // 2 stars: 80%+ OR perfect but slow
  if (accuracy >= star2Accuracy || accuracy >= star3Accuracy) {
    return 2;
  }

  // 1 star: 60%+
  if (accuracy >= star1Accuracy) {
    return 1;
  }

  // 0 stars: below 60%
  return 0;
}
