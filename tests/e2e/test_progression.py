"""Tests for level progression - completing levels and unlocking next."""

import re

from playwright.sync_api import Page, expect


def create_player_and_go_to_world_map(page: Page, player_name: str) -> None:
    """Helper to create player and navigate to world map."""
    page.get_by_role("button", name="New Player").click()
    page.locator("#new-player-name").fill(player_name)
    page.get_by_role("button", name="Create").click()

    # Navigate through intro screens
    page.locator("#intro-screen").click()
    page.wait_for_selector("#world-intro-screen.active")
    page.locator("#world-intro-screen").click()
    page.wait_for_selector("#world-map-screen.active")


def test_level_1_is_unlocked_for_new_player(app_page: Page) -> None:
    """Level 1 should be unlocked for a new player."""
    create_player_and_go_to_world_map(app_page, "NewPlayer1")

    # First level should be clickable (not locked)
    # Note: levels are displayed 10 to 1, so level 1 is last in the DOM
    first_level = app_page.locator(".level-item").last
    expect(first_level).not_to_have_class(re.compile("locked"))


def test_level_2_is_locked_for_new_player(app_page: Page) -> None:
    """Level 2 should be locked until level 1 is completed."""
    create_player_and_go_to_world_map(app_page, "NewPlayer2")

    # Second level should be locked
    # Note: levels are displayed 10 to 1, so level 2 is second-to-last
    second_level = app_page.locator(".level-item").nth(-2)
    expect(second_level).to_have_class(re.compile("locked"))


def test_completing_level_unlocks_next(app_page: Page) -> None:
    """Completing a level with 2+ stars should unlock the next level."""
    create_player_and_go_to_world_map(app_page, "ProgressPlayer")

    # Start level 1 (last in list since levels are displayed 10 to 1)
    app_page.locator(".level-item").last.click()
    app_page.wait_for_selector("#gameplay-screen.active")

    # Use F9 cheat to pass with 3 stars
    app_page.keyboard.press("F9")
    app_page.wait_for_selector("#result-screen.active")

    # Click continue to go back to world map
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Level 2 should now be unlocked (second-to-last in DOM)
    second_level = app_page.locator(".level-item").nth(-2)
    expect(second_level).not_to_have_class(re.compile("locked"))


def test_failing_level_does_not_unlock_next(app_page: Page) -> None:
    """Failing a level (1 star) should not unlock the next level."""
    create_player_and_go_to_world_map(app_page, "FailPlayer")

    # Start level 1 (last in list since levels are displayed 10 to 1)
    app_page.locator(".level-item").last.click()
    app_page.wait_for_selector("#gameplay-screen.active")

    # Use F10 cheat to fail
    app_page.keyboard.press("F10")
    app_page.wait_for_selector("#result-screen.active")

    # Click continue to go back to world map
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Level 2 should still be locked (second-to-last in DOM)
    second_level = app_page.locator(".level-item").nth(-2)
    expect(second_level).to_have_class(re.compile("locked"))


def test_stars_are_displayed_on_world_map(app_page: Page) -> None:
    """Completed levels should show stars on the world map."""
    create_player_and_go_to_world_map(app_page, "StarPlayer")

    # Complete level 1 (last in list since levels are displayed 10 to 1)
    app_page.locator(".level-item").last.click()
    app_page.wait_for_selector("#gameplay-screen.active")
    app_page.keyboard.press("F9")
    app_page.wait_for_selector("#result-screen.active")
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # First level should show stars (last in DOM)
    first_level = app_page.locator(".level-item").last
    stars_display = first_level.locator(".level-stars")
    # Should have star characters (⭐ emoji, not ★)
    expect(stars_display).to_contain_text("⭐")


def test_result_screen_shows_stars(app_page: Page) -> None:
    """Result screen should show star rating."""
    create_player_and_go_to_world_map(app_page, "ResultPlayer")

    # Complete level 1 (last in list since levels are displayed 10 to 1)
    app_page.locator(".level-item").last.click()
    app_page.wait_for_selector("#gameplay-screen.active")
    app_page.keyboard.press("F9")
    app_page.wait_for_selector("#result-screen.active")

    # Should show stars (⭐ emoji)
    stars = app_page.locator("#result-stars")
    expect(stars).to_be_visible()
    expect(stars).to_contain_text("⭐")


def test_replay_button_restarts_level(app_page: Page) -> None:
    """Clicking Replay should restart the same level."""
    create_player_and_go_to_world_map(app_page, "ReplayPlayer")

    # Complete level 1 (last in list since levels are displayed 10 to 1)
    app_page.locator(".level-item").last.click()
    app_page.wait_for_selector("#gameplay-screen.active")
    app_page.keyboard.press("F9")
    app_page.wait_for_selector("#result-screen.active")

    # Click Replay
    app_page.get_by_role("button", name="Replay").click()

    # Should be back in gameplay
    expect(app_page.locator("#gameplay-screen")).to_have_class(re.compile("active"))


def test_progress_persists_after_returning_to_player_select(app_page: Page) -> None:
    """Player progress should persist when re-selecting the player."""
    create_player_and_go_to_world_map(app_page, "PersistPlayer")

    # Complete level 1 (last in list since levels are displayed 10 to 1)
    app_page.locator(".level-item").last.click()
    app_page.wait_for_selector("#gameplay-screen.active")
    app_page.keyboard.press("F9")
    app_page.wait_for_selector("#result-screen.active")
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Go back to player select
    app_page.get_by_role("button", name="Back").click()
    app_page.wait_for_selector("#player-select-screen.active")

    # Re-select the player
    app_page.locator("#player-list li").filter(has_text="PersistPlayer").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Level 2 should still be unlocked (second-to-last in DOM)
    second_level = app_page.locator(".level-item").nth(-2)
    expect(second_level).not_to_have_class(re.compile("locked"))


def test_full_game_playthrough_to_completion(app_page: Page) -> None:
    """Play through all 40 levels (4 worlds x 10 levels) to reach the game complete screen."""
    create_player_and_go_to_world_map(app_page, "FullPlaythrough")

    # Play through all 4 worlds
    for world in range(1, 5):
        for level_in_world in range(1, 11):
            # Click level
            app_page.locator(".level-item").nth(-level_in_world).click()

            # Before level 6: friend meet screen
            if level_in_world == 6:
                app_page.wait_for_selector("#friend-meet-screen.active")
                app_page.locator("#friend-meet-screen").click()

            # Before level 10: boss intro screen
            if level_in_world == 10:
                app_page.wait_for_selector("#boss-intro-screen.active")
                app_page.locator("#boss-intro-screen").click()

            # Play the level
            app_page.wait_for_selector("#gameplay-screen.active")
            app_page.keyboard.press("F9")
            app_page.wait_for_selector("#result-screen.active")
            app_page.get_by_role("button", name="Continue").click()

            # After level 10: boss victory screen
            if level_in_world == 10:
                app_page.wait_for_selector("#boss-victory-screen.active")
                app_page.locator("#boss-victory-screen").click()

                if world < 4:
                    # World intro for next world
                    app_page.wait_for_selector("#world-intro-screen.active")
                    app_page.locator("#world-intro-screen").click()

            # Back to world map (except after final boss)
            if not (world == 4 and level_in_world == 10):
                app_page.wait_for_selector("#world-map-screen.active")

    # Final screen: Game Complete - Flashy goes home!
    app_page.wait_for_selector("#game-complete-screen.active")
    expect(app_page.locator("#game-complete-screen")).to_contain_text("Flashy find the way home")
