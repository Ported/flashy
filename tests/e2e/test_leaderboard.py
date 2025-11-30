"""Tests for leaderboard functionality."""

import re

from conftest import navigate_to_player_select
from playwright.sync_api import Page, expect


def create_player(page: Page, player_name: str) -> None:
    """Helper to create a new player."""
    page.get_by_role("button", name="New Player").click()
    page.locator("#new-player-name").fill(player_name)
    page.get_by_role("button", name="Create").click()


def navigate_to_world_map(page: Page, player_name: str) -> None:
    """Create player and navigate through intro to world map."""
    create_player(page, player_name)

    # Navigate through intro screens
    page.locator("#intro-screen").click()
    page.wait_for_selector("#world-intro-screen.active")
    page.locator("#world-intro-screen").click()
    page.wait_for_selector("#world-map-screen.active")


def complete_level_with_cheats(page: Page) -> None:
    """Complete current level using F9 cheat key."""
    page.wait_for_selector("#gameplay-screen.active")
    page.keyboard.press("F9")  # Cheat: pass all problems
    page.wait_for_selector("#result-screen.active")


def test_player_registration_reserves_name(app_page: Page) -> None:
    """Creating a player should register their name on the leaderboard."""
    navigate_to_world_map(app_page, "LeaderTest1")

    # Open leaderboard
    app_page.get_by_role("button", name="Leaderboard").click()
    app_page.wait_for_selector("#leaderboard-screen.active")

    # Player should appear (with 0 score initially)
    expect(app_page.locator("#leaderboard-list")).to_contain_text("LeaderTest1")


def test_duplicate_name_rejected(app_page: Page) -> None:
    """Trying to register an already-taken name should show error."""
    # First player
    navigate_to_world_map(app_page, "UniqueName")

    # Go back and clear local storage to simulate different browser
    app_page.get_by_role("button", name="Back").click()
    app_page.wait_for_selector("#player-select-screen.active")
    app_page.evaluate("localStorage.clear()")
    app_page.reload()
    navigate_to_player_select(app_page)

    # Try to create player with same name (already registered on leaderboard)
    app_page.get_by_role("button", name="New Player").click()
    app_page.locator("#new-player-name").fill("UniqueName")
    app_page.get_by_role("button", name="Create").click()

    # Should show error from leaderboard API
    error = app_page.locator("#new-player-error")
    expect(error).to_contain_text("already taken")

    # Should still be on new player screen
    expect(app_page.locator("#new-player-screen")).to_have_class(re.compile("active"))


def test_score_syncs_after_level_complete(app_page: Page) -> None:
    """Completing a level should sync score to leaderboard."""
    navigate_to_world_map(app_page, "ScoreSync")

    # Start level 1
    app_page.locator(".level-item").last.click()
    complete_level_with_cheats(app_page)

    # Result screen should show rank (wait for async sync to complete)
    rank_el = app_page.locator("#result-rank")
    expect(rank_el).not_to_contain_text("Updating")  # Wait for sync to finish
    expect(rank_el).to_contain_text("#")

    # Continue to world map
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Check leaderboard shows score > 0
    app_page.get_by_role("button", name="Leaderboard").click()
    app_page.wait_for_selector("#leaderboard-screen.active")

    # Find our player's entry and verify score is not 0
    leaderboard = app_page.locator("#leaderboard-list")
    expect(leaderboard).to_contain_text("ScoreSync")
    # Score should be visible (pts suffix)
    expect(leaderboard).to_contain_text("pts")


def test_leaderboard_shows_rankings(app_page: Page) -> None:
    """Leaderboard should show players ranked by score."""
    navigate_to_world_map(app_page, "RankTest")

    # Open leaderboard
    app_page.get_by_role("button", name="Leaderboard").click()
    app_page.wait_for_selector("#leaderboard-screen.active")

    # Should show rank numbers
    expect(app_page.locator("#leaderboard-list")).to_contain_text("#1")


def test_leaderboard_back_returns_to_world_map(app_page: Page) -> None:
    """Clicking Back on leaderboard should return to world map."""
    navigate_to_world_map(app_page, "BackTest")

    # Open leaderboard
    app_page.get_by_role("button", name="Leaderboard").click()
    app_page.wait_for_selector("#leaderboard-screen.active")

    # Click back
    app_page.locator("#btn-leaderboard-back").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Should be back on world map
    expect(app_page.locator("#world-map-screen")).to_have_class(re.compile("active"))


def test_current_player_highlighted_on_leaderboard(app_page: Page) -> None:
    """Current player's entry should be highlighted on leaderboard."""
    navigate_to_world_map(app_page, "HighlightMe")

    # Complete a level to get a score
    app_page.locator(".level-item").last.click()
    complete_level_with_cheats(app_page)
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Open leaderboard
    app_page.get_by_role("button", name="Leaderboard").click()
    app_page.wait_for_selector("#leaderboard-screen.active")

    # Our entry should have the current-player class
    our_entry = app_page.locator(".leaderboard-entry.current-player")
    expect(our_entry).to_be_visible()
    expect(our_entry).to_contain_text("HighlightMe")


def get_leaderboard_score(page: Page, player_name: str) -> int:
    """Extract a player's score from the leaderboard."""
    page.get_by_role("button", name="Leaderboard").click()
    page.wait_for_selector("#leaderboard-screen.active")

    # Find entry and extract score
    entry = page.locator(f".leaderboard-entry:has-text('{player_name}')")
    score_text = entry.locator(".leaderboard-score").text_content()
    # Parse "2700 pts" -> 2700
    score = int(score_text.replace("pts", "").strip()) if score_text else 0

    page.locator("#btn-leaderboard-back").click()
    page.wait_for_selector("#world-map-screen.active")
    return score


def test_replay_with_lower_score_keeps_best(app_page: Page) -> None:
    """Replaying a level with lower score shouldn't change leaderboard total."""
    navigate_to_world_map(app_page, "ReplayTest")

    # Complete level 1 with cheats (perfect score)
    app_page.locator(".level-item").last.click()
    complete_level_with_cheats(app_page)
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Get score after first completion
    score_after_first = get_leaderboard_score(app_page, "ReplayTest")
    assert score_after_first > 0

    # Replay the same level (click level 1 again)
    app_page.locator(".level-item").last.click()
    app_page.wait_for_selector("#gameplay-screen.active")

    # This time, answer wrong to get a lower score
    # Press wrong number then enter
    app_page.keyboard.type("99999")
    app_page.keyboard.press("Enter")
    # Wait for feedback to complete before using cheat
    app_page.wait_for_timeout(100)
    # Use F9 to finish remaining problems
    app_page.keyboard.press("F9")
    app_page.wait_for_selector("#result-screen.active")
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Get score after replay - should be same (best score kept)
    score_after_replay = get_leaderboard_score(app_page, "ReplayTest")
    assert score_after_replay == score_after_first


def test_replay_with_higher_score_updates_total(app_page: Page) -> None:
    """Replaying a level with higher score should update leaderboard total."""
    navigate_to_world_map(app_page, "ImproveTest")

    # Complete level 1 with a bad score first (answer wrong)
    app_page.locator(".level-item").last.click()
    app_page.wait_for_selector("#gameplay-screen.active")
    app_page.keyboard.type("99999")
    app_page.keyboard.press("Enter")
    # Wait for feedback to complete before using cheat
    app_page.wait_for_timeout(100)
    app_page.keyboard.press("F9")  # Finish rest with cheats
    app_page.wait_for_selector("#result-screen.active")
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Get score after first (bad) completion
    score_after_bad = get_leaderboard_score(app_page, "ImproveTest")

    # Replay with perfect score using cheats
    app_page.locator(".level-item").last.click()
    complete_level_with_cheats(app_page)
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Get score after good completion - should be higher
    score_after_good = get_leaderboard_score(app_page, "ImproveTest")
    assert score_after_good > score_after_bad
