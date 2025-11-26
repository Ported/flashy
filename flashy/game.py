"""Game session logic - core game loop."""

import time

from flashy.history import LevelResult, ProblemResult
from flashy.input_handler import InputHandler
from flashy.levels import Level
from flashy.number_parser import is_fuzzy_match
from flashy.scoring import calculate_score, get_streak_multiplier

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


def run_level(level: Level, input_handler: InputHandler) -> LevelResult:
    """Run a single level and return the results.

    Args:
        level: The level configuration
        input_handler: Handler for getting user input

    Returns:
        LevelResult with all statistics
    """
    print(f"\n{'=' * 40}")
    print(f"Level {level.number}: {level.name}")
    print(f"{'=' * 40}\n")

    problems_results: list[ProblemResult] = []
    results_so_far: list[bool] = []  # Track correct/wrong for progress bar
    total_score = 0
    correct_count = 0
    streak = 0
    best_streak = 0
    total_time = 0.0

    num_problems = len(level.problems)
    for i, problem in enumerate(level.problems):
        # Display progress as colored dots: ● ● ● ◉ ○ ○ ○
        done = " ".join(
            f"{GREEN}●{RESET}" if ok else f"{RED}●{RESET}" for ok in results_so_far
        )
        current = "◉"
        remaining = " ".join("○" for _ in range(num_problems - i - 1))
        parts = [p for p in [done, current, remaining] if p]
        print(" ".join(parts))
        print(f"  {problem.display()} = _\n")

        # Get answer with timing
        start_time = time.time()
        answer, raw_input = input_handler.get_answer(
            prompt="🎤 ", expected=problem.answer
        )
        elapsed = time.time() - start_time
        total_time += elapsed

        # Check answer (with fuzzy matching for voice recognition)
        is_correct = is_fuzzy_match(answer, problem.answer)
        is_exact = answer == problem.answer

        if is_correct:
            streak += 1
            best_streak = max(best_streak, streak)
            points = calculate_score(elapsed, is_correct, streak)
            total_score += points

            streak_text = f"Streak: {streak}"
            multiplier = get_streak_multiplier(streak)
            if multiplier > 1.0:
                streak_text += f" ({multiplier}x)"

            if is_exact:
                print(f"{GREEN}Correct!{RESET} +{points} pts | {streak_text}\n")
            else:
                print(
                    f"{GREEN}Close enough!{RESET} The answer is {problem.answer}. "
                    f"+{points} pts | {streak_text}\n"
                )
            correct_count += 1
            results_so_far.append(True)
        else:
            streak = 0
            print(
                f"{RED}Nope!{RESET} {problem.display()} = {problem.answer} "
                f"| Streak reset\n"
            )
            results_so_far.append(False)

        # Record result
        problems_results.append(
            ProblemResult(
                problem=problem.display(),
                correct_answer=problem.answer,
                given_answer=answer,
                is_correct=is_correct,
                time_seconds=elapsed,
                points=(
                    calculate_score(elapsed, is_correct, streak) if is_correct else 0
                ),
            )
        )

    return LevelResult(
        level_number=level.number,
        level_name=level.name,
        total_score=total_score,
        correct_count=correct_count,
        total_problems=num_problems,
        best_streak=best_streak,
        total_time_seconds=total_time,
        problems=problems_results,
    )


def display_level_summary(result: LevelResult) -> None:
    """Display the summary after completing a level."""
    print(f"\n{'─' * 40}")
    print("Level Complete!")
    print(f"{'─' * 40}")
    print(f"Score: {result.total_score}")
    print(f"Correct: {result.correct_count}/{result.total_problems}")
    print(f"Best Streak: {result.best_streak}")
    print(f"Time: {result.total_time_seconds:.1f}s")
    print(f"{'─' * 40}\n")


def run_boss_level(level: Level, input_handler: InputHandler) -> LevelResult:
    """Run a boss level with time pressure.

    Args:
        level: The boss level configuration (must have time_limit set)
        input_handler: Handler for getting user input

    Returns:
        LevelResult with all statistics
    """
    if level.time_limit is None:
        raise ValueError("Boss level must have a time_limit")

    time_limit = level.time_limit
    num_problems = len(level.problems)

    print(f"\n{YELLOW}{'⚡' * 20}{RESET}")
    print(f"   ⏱️  BOSS BATTLE: {time_limit} seconds!")
    print(f"{YELLOW}{'⚡' * 20}{RESET}\n")

    problems_results: list[ProblemResult] = []
    results_so_far: list[bool] = []
    total_score = 0
    correct_count = 0
    streak = 0
    best_streak = 0

    boss_start = time.time()
    total_time = 0.0
    timed_out = False

    for i, problem in enumerate(level.problems):
        # Check time remaining
        elapsed_total = time.time() - boss_start
        time_remaining = time_limit - elapsed_total

        if time_remaining <= 0:
            timed_out = True
            print(f"\n{RED}⏱️  TIME'S UP!{RESET}\n")
            break

        # Display progress with timer
        done = " ".join(
            f"{GREEN}●{RESET}" if ok else f"{RED}●{RESET}" for ok in results_so_far
        )
        current = "◉"
        remaining_dots = " ".join("○" for _ in range(num_problems - i - 1))
        parts = [p for p in [done, current, remaining_dots] if p]

        # Color timer based on time remaining
        if time_remaining > 30:
            timer_color = GREEN
        elif time_remaining > 10:
            timer_color = YELLOW
        else:
            timer_color = RED

        print(f"   {timer_color}⏱️  {time_remaining:.0f}s remaining{RESET}")
        print(" ".join(parts))
        print(f"  {problem.display()} = _\n")

        # Get answer with timing
        start_time = time.time()
        answer, raw_input = input_handler.get_answer(
            prompt="🎤 ", expected=problem.answer
        )
        elapsed = time.time() - start_time
        total_time += elapsed

        # Check if we ran out of time during input
        if time.time() - boss_start > time_limit:
            timed_out = True
            print(f"\n{RED}⏱️  TIME'S UP!{RESET}\n")
            # Still record this last answer
            is_correct = is_fuzzy_match(answer, problem.answer)
            if is_correct:
                correct_count += 1
                results_so_far.append(True)
            else:
                results_so_far.append(False)
            problems_results.append(
                ProblemResult(
                    problem=problem.display(),
                    correct_answer=problem.answer,
                    given_answer=answer,
                    is_correct=is_correct,
                    time_seconds=elapsed,
                    points=0,
                )
            )
            break

        # Check answer (with fuzzy matching)
        is_correct = is_fuzzy_match(answer, problem.answer)
        is_exact = answer == problem.answer

        if is_correct:
            streak += 1
            best_streak = max(best_streak, streak)
            points = calculate_score(elapsed, is_correct, streak)
            total_score += points

            if is_exact:
                print(f"{GREEN}✓{RESET} +{points} pts\n")
            else:
                print(f"{GREEN}✓{RESET} (={problem.answer}) +{points} pts\n")
            correct_count += 1
            results_so_far.append(True)
        else:
            streak = 0
            print(f"{RED}✗{RESET} {problem.display()} = {problem.answer}\n")
            results_so_far.append(False)

        # Record result
        problems_results.append(
            ProblemResult(
                problem=problem.display(),
                correct_answer=problem.answer,
                given_answer=answer,
                is_correct=is_correct,
                time_seconds=elapsed,
                points=(
                    calculate_score(elapsed, is_correct, streak) if is_correct else 0
                ),
            )
        )

    # Calculate total time (capped at time limit)
    actual_total = time.time() - boss_start
    total_time = min(actual_total, float(time_limit))

    # Show completion status
    if not timed_out and correct_count == num_problems:
        print(f"\n{GREEN}{'⭐' * 20}{RESET}")
        print("   PERFECT BOSS VICTORY!")
        print(f"{GREEN}{'⭐' * 20}{RESET}\n")
    elif not timed_out:
        print(f"\n{YELLOW}Boss defeated!{RESET}\n")
    else:
        print(f"\n{RED}The boss got away...{RESET}")
        print("Try again to beat the timer!\n")

    return LevelResult(
        level_number=level.number,
        level_name=level.name,
        total_score=total_score,
        correct_count=correct_count,
        total_problems=num_problems,
        best_streak=best_streak,
        total_time_seconds=total_time,
        problems=problems_results,
    )
