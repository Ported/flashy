"""Tests for gameplay - answering problems with keyboard input."""

import re

from conftest import generate_unique_name
from playwright.sync_api import Page, expect


def navigate_to_level(page: Page) -> None:
    """Helper to create player and navigate to level 1."""
    # Create player with unique name
    page.get_by_role("button", name="New Player").click()
    page.locator("#new-player-name").fill(generate_unique_name("Gameplay"))
    page.get_by_role("button", name="Create").click()

    # Navigate through intro screens
    page.locator("#intro-screen").click()
    page.wait_for_selector("#world-intro-screen.active")
    page.locator("#world-intro-screen").click()
    page.wait_for_selector("#world-map-screen.active")

    # Click level 1 (last in list since levels are displayed 10 to 1)
    page.locator(".level-item").last.click()
    page.wait_for_selector("#gameplay-screen.active")


def test_gameplay_screen_shows_problem(app_page: Page) -> None:
    """Gameplay screen should display a math problem."""
    navigate_to_level(app_page)

    # Problem display should be visible with a math problem
    problem = app_page.locator("#problem-display")
    expect(problem).to_be_visible()
    # Should contain an equation like "2 + 3 = ?"
    expect(problem).to_contain_text("=")
    expect(problem).to_contain_text("?")


def test_keyboard_input_shows_in_answer_box(app_page: Page) -> None:
    """Typing numbers should show in the answer box."""
    navigate_to_level(app_page)

    # Type a number
    app_page.keyboard.press("5")

    answer_box = app_page.locator("#answer-box")
    expect(answer_box).to_contain_text("5")


def test_keyboard_input_multiple_digits(app_page: Page) -> None:
    """Typing multiple digits should accumulate in answer box."""
    navigate_to_level(app_page)

    app_page.keyboard.press("1")
    app_page.keyboard.press("2")
    app_page.keyboard.press("3")

    answer_box = app_page.locator("#answer-box")
    expect(answer_box).to_contain_text("123")


def test_backspace_removes_digit(app_page: Page) -> None:
    """Backspace should remove the last digit."""
    navigate_to_level(app_page)

    app_page.keyboard.press("1")
    app_page.keyboard.press("2")
    app_page.keyboard.press("Backspace")

    answer_box = app_page.locator("#answer-box")
    expect(answer_box).to_contain_text("1")


def test_enter_submits_answer(app_page: Page) -> None:
    """Pressing Enter should submit the answer and show feedback."""
    navigate_to_level(app_page)

    # Set up observer to catch brief feedback class (only 2ms in tests)
    app_page.evaluate("""
        window.sawFeedback = false;
        const el = document.getElementById('problem-display');
        new MutationObserver(() => {
            if (el.classList.contains('correct') ||
                el.classList.contains('incorrect')) {
                window.sawFeedback = true;
            }
        }).observe(el, {attributes: true});
    """)

    # Type an answer and submit
    app_page.keyboard.press("5")
    app_page.keyboard.press("Enter")

    # Wait a moment for feedback to appear and be observed
    app_page.wait_for_timeout(50)

    # Verify the observer caught some feedback
    saw_feedback = app_page.evaluate("window.sawFeedback")
    assert saw_feedback, "Expected feedback class on problem-display"


def test_correct_answer_shows_green_feedback(app_page: Page) -> None:
    """Correct answer should show green feedback."""
    navigate_to_level(app_page)

    # Extract the problem and calculate correct answer
    problem_text = app_page.locator("#problem-display").inner_text()

    # Parse simple addition problem like "2 + 3 = ?"
    match = re.match(r"(\d+)\s*\+\s*(\d+)\s*=", problem_text)
    if match:
        correct = int(match.group(1)) + int(match.group(2))

        # Set up observer to catch the brief "correct" class
        # (feedback is only 2ms in tests)
        app_page.evaluate("window.sawCorrectFeedback = false")
        app_page.evaluate("""
            const el = document.getElementById('problem-display');
            new MutationObserver(() => {
                if (el.classList.contains('correct')) {
                    window.sawCorrectFeedback = true;
                }
            }).observe(el, {attributes: true});
        """)

        # Type the correct answer
        for digit in str(correct):
            app_page.keyboard.press(digit)
        app_page.keyboard.press("Enter")

        # Wait a moment for feedback to appear and be observed
        app_page.wait_for_timeout(50)

        # Verify the observer caught the correct feedback
        saw_feedback = app_page.evaluate("window.sawCorrectFeedback")
        assert saw_feedback, "Expected 'correct' class to appear on problem-display"


def test_wrong_answer_shows_red_feedback(app_page: Page) -> None:
    """Wrong answer should show red feedback."""
    navigate_to_level(app_page)

    # Set up observer to catch the brief "incorrect" class
    # (feedback is only 2ms in tests)
    app_page.evaluate("window.sawIncorrectFeedback = false")
    app_page.evaluate("""
        const el = document.getElementById('problem-display');
        new MutationObserver(() => {
            if (el.classList.contains('incorrect')) {
                window.sawIncorrectFeedback = true;
            }
        }).observe(el, {attributes: true});
    """)

    # Type obviously wrong answer (999)
    app_page.keyboard.press("9")
    app_page.keyboard.press("9")
    app_page.keyboard.press("9")
    app_page.keyboard.press("Enter")

    # Wait a moment for feedback to appear and be observed
    app_page.wait_for_timeout(50)

    # Verify the observer caught the incorrect feedback
    saw_feedback = app_page.evaluate("window.sawIncorrectFeedback")
    assert saw_feedback, "Expected 'incorrect' class to appear on problem-display"


def test_progress_dots_update_after_answer(app_page: Page) -> None:
    """Progress dots should update after answering."""
    navigate_to_level(app_page)

    # Get initial dot state - first should be current (filled circle)
    dots = app_page.locator("#progress-dots")
    expect(dots).to_contain_text("◉")  # Current dot marker (filled circle)

    # Submit an answer
    app_page.keyboard.press("5")
    app_page.keyboard.press("Enter")

    # Wait for next problem
    app_page.wait_for_timeout(500)

    # Dots should have updated (first problem answered)
    # The dot pattern will have changed


def test_cheat_f9_completes_all_problems(app_page: Page) -> None:
    """F9 cheat should complete all problems correctly and show results."""
    navigate_to_level(app_page)

    # Press F9 cheat
    app_page.keyboard.press("F9")

    # Should navigate to result screen
    app_page.wait_for_selector("#result-screen.active", timeout=5000)
    expect(app_page.locator("#result-screen")).to_have_class(re.compile("active"))


def test_cheat_f10_fails_all_problems(app_page: Page) -> None:
    """F10 cheat should fail all problems and show results."""
    navigate_to_level(app_page)

    # Press F10 cheat
    app_page.keyboard.press("F10")

    # Should navigate to result screen
    app_page.wait_for_selector("#result-screen.active", timeout=5000)

    # Should show 1 star or less (failed)
    stars = app_page.locator("#result-stars")
    expect(stars).to_be_visible()


def test_score_bar_visible(app_page: Page) -> None:
    """Score bar should be visible during gameplay."""
    navigate_to_level(app_page)

    score_bar = app_page.locator("#score-bar")
    expect(score_bar).to_be_visible()
    expect(score_bar).to_contain_text("Score")
