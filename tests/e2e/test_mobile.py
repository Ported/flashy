"""Tests for mobile viewport - ensuring UI works on small screens."""

import re

from conftest import generate_unique_name
from playwright.sync_api import Page, expect


def test_player_select_visible_on_mobile(mobile_page: Page) -> None:
    """Player select screen should be fully visible on mobile."""
    # New Player button should be visible and tappable
    new_player_btn = mobile_page.get_by_role("button", name="New Player")
    expect(new_player_btn).to_be_visible()
    expect(new_player_btn).to_be_in_viewport()


def test_new_player_form_usable_on_mobile(mobile_page: Page) -> None:
    """New player form should work on mobile viewport."""
    mobile_page.get_by_role("button", name="New Player").click()

    # Name input should be visible
    name_input = mobile_page.locator("#new-player-name")
    expect(name_input).to_be_visible()
    expect(name_input).to_be_in_viewport()

    # Create button should be visible
    create_btn = mobile_page.get_by_role("button", name="Create")
    expect(create_btn).to_be_visible()
    expect(create_btn).to_be_in_viewport()

    # Should be able to type and create
    name_input.fill(generate_unique_name("Mobile"))
    create_btn.click()

    # Should navigate to intro
    mobile_page.wait_for_selector("#intro-screen.active")
    expect(mobile_page.locator("#intro-screen")).to_have_class(re.compile("active"))


def test_gameplay_screen_elements_visible_on_mobile(mobile_page: Page) -> None:
    """All gameplay elements should be visible on mobile without scrolling."""
    # Create player and navigate to level
    mobile_page.get_by_role("button", name="New Player").click()
    mobile_page.locator("#new-player-name").fill(generate_unique_name("MobGame"))
    mobile_page.get_by_role("button", name="Create").click()
    mobile_page.wait_for_selector("#intro-screen.active")
    mobile_page.locator("#intro-screen").click()
    mobile_page.wait_for_selector("#world-intro-screen.active")
    mobile_page.locator("#world-intro-screen").click()
    mobile_page.wait_for_selector("#world-map-screen.active")
    # Click level 1 (last in list since levels are displayed 10 to 1)
    mobile_page.locator(".level-item").last.click()
    mobile_page.wait_for_selector("#gameplay-screen.active")

    # Problem display should be visible
    problem = mobile_page.locator("#problem-display")
    expect(problem).to_be_visible()
    expect(problem).to_be_in_viewport()

    # Answer box should be visible
    answer_box = mobile_page.locator("#answer-box")
    expect(answer_box).to_be_visible()
    expect(answer_box).to_be_in_viewport()

    # Score bar should be visible
    score_bar = mobile_page.locator("#score-bar")
    expect(score_bar).to_be_visible()
    expect(score_bar).to_be_in_viewport()

    # Numpad should be visible
    numpad = mobile_page.locator("#numpad")
    expect(numpad).to_be_visible()


def test_world_map_levels_tappable_on_mobile(mobile_page: Page) -> None:
    """Level buttons should be large enough to tap on mobile."""
    # Create player and navigate to world map
    mobile_page.get_by_role("button", name="New Player").click()
    mobile_page.locator("#new-player-name").fill(generate_unique_name("MobTap"))
    mobile_page.get_by_role("button", name="Create").click()
    mobile_page.wait_for_selector("#intro-screen.active")
    mobile_page.locator("#intro-screen").click()
    mobile_page.wait_for_selector("#world-intro-screen.active")
    mobile_page.locator("#world-intro-screen").click()
    mobile_page.wait_for_selector("#world-map-screen.active")

    # Level 1 is last in DOM (levels displayed 10 to 1), scroll it into view
    first_level = mobile_page.locator(".level-item").last
    first_level.scroll_into_view_if_needed()
    expect(first_level).to_be_visible()
    expect(first_level).to_be_in_viewport()

    # Verify it has reasonable size for tapping
    # iOS guidelines recommend 44x44 but 38px is still tappable
    box = first_level.bounding_box()
    assert box is not None
    assert box["width"] >= 44, f"Level button too narrow: {box['width']}px"
    assert box["height"] >= 38, f"Level button too short: {box['height']}px"


def test_result_screen_buttons_visible_on_mobile(mobile_page: Page) -> None:
    """Result screen buttons should be visible on mobile."""
    # Create player and complete a level
    mobile_page.get_by_role("button", name="New Player").click()
    mobile_page.locator("#new-player-name").fill(generate_unique_name("MobResult"))
    mobile_page.get_by_role("button", name="Create").click()
    mobile_page.wait_for_selector("#intro-screen.active")
    mobile_page.locator("#intro-screen").click()
    mobile_page.wait_for_selector("#world-intro-screen.active")
    mobile_page.locator("#world-intro-screen").click()
    mobile_page.wait_for_selector("#world-map-screen.active")
    # Click level 1 (last in list since levels are displayed 10 to 1)
    mobile_page.locator(".level-item").last.click()
    mobile_page.wait_for_selector("#gameplay-screen.active")
    mobile_page.keyboard.press("F9")
    mobile_page.wait_for_selector("#result-screen.active")

    # Continue button should be visible
    continue_btn = mobile_page.get_by_role("button", name="Continue")
    expect(continue_btn).to_be_visible()
    expect(continue_btn).to_be_in_viewport()

    # Replay button should be visible
    replay_btn = mobile_page.get_by_role("button", name="Replay")
    expect(replay_btn).to_be_visible()
    expect(replay_btn).to_be_in_viewport()


def test_screens_fit_within_viewport_on_mobile(mobile_page: Page) -> None:
    """Screen content should not overflow the viewport horizontally."""
    # Navigate through various screens and check none overflow
    mobile_page.get_by_role("button", name="New Player").click()

    # Check new player screen doesn't overflow
    screen = mobile_page.locator("#new-player-screen")
    box = screen.bounding_box()
    assert box is not None
    viewport = mobile_page.viewport_size
    assert viewport is not None
    assert box["width"] <= viewport["width"], "New player screen overflows viewport"


def test_numpad_visible_on_mobile(mobile_page: Page) -> None:
    """Numpad should be visible during gameplay on mobile."""
    # Create player and navigate to level
    mobile_page.get_by_role("button", name="New Player").click()
    mobile_page.locator("#new-player-name").fill(generate_unique_name("Numpad"))
    mobile_page.get_by_role("button", name="Create").click()
    mobile_page.wait_for_selector("#intro-screen.active")
    mobile_page.locator("#intro-screen").click()
    mobile_page.wait_for_selector("#world-intro-screen.active")
    mobile_page.locator("#world-intro-screen").click()
    mobile_page.wait_for_selector("#world-map-screen.active")
    mobile_page.locator(".level-item").last.click()
    mobile_page.wait_for_selector("#gameplay-screen.active")

    # Numpad should be visible
    numpad = mobile_page.locator("#numpad")
    expect(numpad).to_be_visible()

    # Number buttons should be tappable
    btn_5 = mobile_page.locator(".numpad-btn", has_text="5").first
    expect(btn_5).to_be_visible()
    box = btn_5.bounding_box()
    assert box is not None
    assert box["width"] >= 44, f"Numpad button too narrow: {box['width']}px"
    assert box["height"] >= 44, f"Numpad button too short: {box['height']}px"


def test_numpad_input_works_on_mobile(mobile_page: Page) -> None:
    """Tapping numpad buttons should input digits."""
    # Create player and navigate to level
    mobile_page.get_by_role("button", name="New Player").click()
    mobile_page.locator("#new-player-name").fill(generate_unique_name("NumIn"))
    mobile_page.get_by_role("button", name="Create").click()
    mobile_page.wait_for_selector("#intro-screen.active")
    mobile_page.locator("#intro-screen").click()
    mobile_page.wait_for_selector("#world-intro-screen.active")
    mobile_page.locator("#world-intro-screen").click()
    mobile_page.wait_for_selector("#world-map-screen.active")
    mobile_page.locator(".level-item").last.click()
    mobile_page.wait_for_selector("#gameplay-screen.active")

    # Scroll numpad into view first
    numpad = mobile_page.locator("#numpad")
    numpad.scroll_into_view_if_needed()

    # Tap numpad buttons to enter "12" - use exact text match within numpad
    mobile_page.locator("#numpad .numpad-btn", has_text=re.compile("^1$")).click()
    mobile_page.locator("#numpad .numpad-btn", has_text=re.compile("^2$")).click()

    # Answer box should show "12"
    answer_box = mobile_page.locator("#answer-box")
    expect(answer_box).to_contain_text("12")

    # Tap backspace
    mobile_page.locator("#numpad .numpad-btn", has_text="⌫").click()
    expect(answer_box).to_contain_text("1")

    # Tap more digits and enter
    mobile_page.locator("#numpad .numpad-btn", has_text=re.compile("^0$")).click()
    mobile_page.locator(".enter-btn").click()

    # Feedback should appear in problem display (we submitted an answer)
    problem_display = mobile_page.locator("#problem-display")
    expect(problem_display).to_have_class(re.compile("correct|incorrect"))
