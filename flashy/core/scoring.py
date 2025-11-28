"""Score calculation - pure functions for computing points."""

# Base points for a correct answer
BASE_POINTS = 100

# Time thresholds for speed bonus (in seconds)
FAST_THRESHOLD = 2.0  # Under 2 seconds = fast
MEDIUM_THRESHOLD = 5.0  # Under 5 seconds = medium

# Speed bonus multipliers
FAST_BONUS = 1.5
MEDIUM_BONUS = 1.2

# Streak multipliers
STREAK_THRESHOLDS = [
    (3, 1.5),  # 3+ streak = 1.5x
    (5, 2.0),  # 5+ streak = 2x
    (10, 3.0),  # 10+ streak = 3x
]


def calculate_score(time_taken: float, is_correct: bool, streak: int) -> int:
    """Calculate points for a single problem.

    Args:
        time_taken: Time in seconds to answer
        is_correct: Whether the answer was correct
        streak: Current streak count (consecutive correct answers)

    Returns:
        Points earned (0 if incorrect)
    """
    if not is_correct:
        return 0

    points = float(BASE_POINTS)

    # Apply speed bonus
    if time_taken < FAST_THRESHOLD:
        points *= FAST_BONUS
    elif time_taken < MEDIUM_THRESHOLD:
        points *= MEDIUM_BONUS

    # Apply streak multiplier
    streak_multiplier = get_streak_multiplier(streak)
    points *= streak_multiplier

    return int(points)


def get_streak_multiplier(streak: int) -> float:
    """Get the multiplier for the current streak."""
    multiplier = 1.0
    for threshold, mult in STREAK_THRESHOLDS:
        if streak >= threshold:
            multiplier = mult
    return multiplier


# Star thresholds
STAR_3_ACCURACY = 1.0  # 100% correct
STAR_3_TIME_PER_PROBLEM = 5.0  # Average under 5 seconds per problem
STAR_2_ACCURACY = 0.8  # 80% correct
STAR_1_ACCURACY = 0.6  # 60% correct


def calculate_stars(
    correct: int,
    total: int,
    total_time: float,
) -> int:
    """Calculate stars earned for a level.

    Args:
        correct: Number of correct answers
        total: Total number of problems
        total_time: Total time taken in seconds

    Returns:
        Stars earned (0-3)
        - 3 stars: 100% correct AND fast (under 5s per problem average)
        - 2 stars: 80%+ correct OR 100% correct but slow
        - 1 star: 60%+ correct
        - 0 stars: Below 60% (level not passed)
    """
    if total == 0:
        return 0

    accuracy = correct / total
    avg_time = total_time / total

    # 3 stars: perfect AND fast
    if accuracy >= STAR_3_ACCURACY and avg_time <= STAR_3_TIME_PER_PROBLEM:
        return 3

    # 2 stars: 80%+ OR perfect but slow
    if accuracy >= STAR_2_ACCURACY or accuracy >= STAR_3_ACCURACY:
        return 2

    # 1 star: 60%+
    if accuracy >= STAR_1_ACCURACY:
        return 1

    # 0 stars: below 60%
    return 0
