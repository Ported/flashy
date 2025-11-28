"""Tests for player creation and selection flow."""

import re

from playwright.sync_api import Page, expect


def test_player_select_screen_shows_new_player_button(app_page: Page) -> None:
    """The player select screen should show a 'New Player' button."""
    new_player_btn = app_page.get_by_role("button", name="New Player")
    expect(new_player_btn).to_be_visible()


def test_create_new_player(app_page: Page) -> None:
    """Creating a new player should add them to the list."""
    # Click New Player button
    app_page.get_by_role("button", name="New Player").click()

    # Should show new player screen
    expect(app_page.locator("#new-player-screen")).to_have_class(re.compile("active"))

    # Enter player name
    app_page.locator("#new-player-name").fill("TestPlayer")

    # Click Create
    app_page.get_by_role("button", name="Create").click()

    # Should navigate to intro screen for new player
    expect(app_page.locator("#intro-screen")).to_have_class(re.compile("active"))


def test_create_player_empty_name_shows_error(app_page: Page) -> None:
    """Creating a player with empty name should show an error."""
    # Click New Player button
    app_page.get_by_role("button", name="New Player").click()

    # Leave name empty and click Create
    app_page.get_by_role("button", name="Create").click()

    # Should show error message
    error_msg = app_page.locator("#new-player-error")
    expect(error_msg).to_be_visible()
    expect(error_msg).to_contain_text("enter a name")


def test_create_duplicate_player_shows_error(app_page: Page) -> None:
    """Creating a player with a name that already exists should show an error."""
    # Create first player
    app_page.get_by_role("button", name="New Player").click()
    app_page.locator("#new-player-name").fill("DuplicateTest")
    app_page.get_by_role("button", name="Create").click()

    # Wait for intro, then go back to player select
    expect(app_page.locator("#intro-screen")).to_have_class(re.compile("active"))

    # Navigate through intro to world map, then back to player select
    # (clicking advances the intro)
    app_page.locator("#intro-screen").click()
    app_page.wait_for_selector("#world-intro-screen.active")
    app_page.locator("#world-intro-screen").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Click back button
    app_page.get_by_role("button", name="Back").click()
    app_page.wait_for_selector("#player-select-screen.active")

    # Try to create player with same name
    app_page.get_by_role("button", name="New Player").click()
    app_page.locator("#new-player-name").fill("DuplicateTest")
    app_page.get_by_role("button", name="Create").click()

    # Should show error
    error_msg = app_page.locator("#new-player-error")
    expect(error_msg).to_be_visible()
    expect(error_msg).to_contain_text("already exists")


def test_select_existing_player(app_page: Page) -> None:
    """Selecting a returning player (with progress) should go directly to world map."""
    # First create a player
    app_page.get_by_role("button", name="New Player").click()
    app_page.locator("#new-player-name").fill("ExistingPlayer")
    app_page.get_by_role("button", name="Create").click()

    # Navigate through intro screens
    app_page.locator("#intro-screen").click()
    app_page.wait_for_selector("#world-intro-screen.active")
    app_page.locator("#world-intro-screen").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Complete level 1 to unlock level 2 (required for "returning player" flow)
    # Note: levels are displayed 10 to 1, so level 1 is last in the DOM
    app_page.locator(".level-item").last.click()
    app_page.wait_for_selector("#gameplay-screen.active")
    app_page.keyboard.press("F9")  # Cheat to pass
    app_page.wait_for_selector("#result-screen.active")
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Go back to player select
    app_page.get_by_role("button", name="Back").click()
    app_page.wait_for_selector("#player-select-screen.active")

    # Now select the player - should go directly to world map (no intro)
    app_page.locator("#player-list li").filter(has_text="ExistingPlayer").click()

    # Should go directly to world map since they have progress
    app_page.wait_for_selector("#world-map-screen.active", timeout=5000)
    expect(app_page.locator("#world-map-screen")).to_have_class(re.compile("active"))


def test_cancel_new_player_returns_to_select(app_page: Page) -> None:
    """Clicking cancel on new player form should return to player select."""
    app_page.get_by_role("button", name="New Player").click()
    expect(app_page.locator("#new-player-screen")).to_have_class(re.compile("active"))

    app_page.get_by_role("button", name="Cancel").click()
    expect(app_page.locator("#player-select-screen")).to_have_class(
        re.compile("active")
    )
