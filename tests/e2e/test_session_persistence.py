"""Tests for session persistence and token-based account recovery."""

import re

from conftest import generate_unique_name, navigate_to_player_select
from playwright.sync_api import BrowserContext, Page, expect


def test_session_persists_after_page_reload(app_page: Page) -> None:
    """Player should remain logged in after page reload."""
    # Create a new player
    player_name = generate_unique_name("Persist")
    app_page.get_by_role("button", name="New Player").click()
    app_page.locator("#new-player-name").fill(player_name)
    app_page.get_by_role("button", name="Create").click()

    # Navigate through intro screens to world map
    app_page.wait_for_selector("#intro-screen.active")
    app_page.locator("#intro-screen").click()
    app_page.wait_for_selector("#world-intro-screen.active")
    app_page.locator("#world-intro-screen").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Reload the page
    app_page.reload()

    # Should go directly to world map (not welcome screen)
    app_page.wait_for_selector("#world-map-screen.active", timeout=60000)
    expect(app_page.locator("#world-map-screen")).to_have_class(re.compile("active"))

    # Verify it's the same player
    expect(app_page.locator("#world-map-player")).to_contain_text(player_name)


def test_session_persists_in_new_tab(
    shared_context: BrowserContext, web_server: str
) -> None:
    """Player should remain logged in when opening a new tab."""
    # Create first page and player
    page1 = shared_context.new_page()
    page1.goto(web_server)
    page1.evaluate("localStorage.clear()")
    page1.reload()
    page1.wait_for_selector("#welcome-screen.active", timeout=60000)
    page1.click("text=Play")
    page1.wait_for_selector("#player-select-screen.active")

    player_name = generate_unique_name("NewTab")
    page1.get_by_role("button", name="New Player").click()
    page1.locator("#new-player-name").fill(player_name)
    page1.get_by_role("button", name="Create").click()

    # Navigate to world map
    page1.wait_for_selector("#intro-screen.active")
    page1.locator("#intro-screen").click()
    page1.wait_for_selector("#world-intro-screen.active")
    page1.locator("#world-intro-screen").click()
    page1.wait_for_selector("#world-map-screen.active")

    # Open a new tab (same browser context = same localStorage)
    page2 = shared_context.new_page()
    page2.goto(web_server)

    # Should go directly to world map with same player
    page2.wait_for_selector("#world-map-screen.active", timeout=60000)
    expect(page2.locator("#world-map-player")).to_contain_text(player_name)

    page1.close()
    page2.close()


def test_token_recovers_account_after_progress_cleared(app_page: Page) -> None:
    """Player account should be recoverable if progress is cleared but token remains."""
    # Create a new player
    player_name = generate_unique_name("Recover")
    app_page.get_by_role("button", name="New Player").click()
    app_page.locator("#new-player-name").fill(player_name)
    app_page.get_by_role("button", name="Create").click()

    # Navigate to world map
    app_page.wait_for_selector("#intro-screen.active")
    app_page.locator("#intro-screen").click()
    app_page.wait_for_selector("#world-intro-screen.active")
    app_page.locator("#world-intro-screen").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Simulate partial data loss: clear progress but keep token
    app_page.evaluate(
        """(playerName) => {
        // Keep only the token, clear everything else
        const keys = [];
        for (let i = 0; i < localStorage.length; i++) {
            keys.push(localStorage.key(i));
        }
        keys.forEach(key => {
            if (!key.startsWith('flashy_token_')) {
                localStorage.removeItem(key);
            }
        });
    }""",
        player_name,
    )

    # Reload the page
    app_page.reload()

    # Should show welcome screen (no current player set)
    app_page.wait_for_selector("#welcome-screen.active", timeout=60000)
    app_page.click("text=Play")
    app_page.wait_for_selector("#player-select-screen.active")

    # Player should still appear in the list (recovered from token)
    player_item = app_page.locator("#player-list li").filter(has_text=player_name)
    expect(player_item).to_be_visible(timeout=5000)

    # Should be able to select and play as that player
    # Since recovered player has no progress, they'll see intro screen first
    player_item.click()
    app_page.wait_for_selector("#intro-screen.active", timeout=5000)

    # Click through intro to get to world map
    app_page.locator("#intro-screen").click()
    app_page.wait_for_selector("#world-intro-screen.active")
    app_page.locator("#world-intro-screen").click()
    app_page.wait_for_selector("#world-map-screen.active")
    expect(app_page.locator("#world-map-player")).to_contain_text(player_name)


def test_token_recovers_account_with_progress(app_page: Page) -> None:
    """Player account with progress should be fully recoverable from token."""
    # Create a new player
    player_name = generate_unique_name("RecoverProg")
    app_page.get_by_role("button", name="New Player").click()
    app_page.locator("#new-player-name").fill(player_name)
    app_page.get_by_role("button", name="Create").click()

    # Navigate to world map
    app_page.wait_for_selector("#intro-screen.active")
    app_page.locator("#intro-screen").click()
    app_page.wait_for_selector("#world-intro-screen.active")
    app_page.locator("#world-intro-screen").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Complete level 1 to get some progress
    app_page.locator(".level-item").last.click()
    app_page.wait_for_selector("#gameplay-screen.active")
    app_page.keyboard.press("F9")  # Cheat to pass
    app_page.wait_for_selector("#result-screen.active")
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Simulate clearing current player but keeping token AND progress data
    # This simulates a partial corruption where only the session is lost
    app_page.evaluate(
        """() => {
        localStorage.removeItem('flashy_current_player');
        localStorage.removeItem('flashy_current_world');
    }"""
    )

    # Reload the page
    app_page.reload()

    # Should show welcome screen (no current player set)
    app_page.wait_for_selector("#welcome-screen.active", timeout=60000)
    app_page.click("text=Play")
    app_page.wait_for_selector("#player-select-screen.active")

    # Player should appear with Level 2 progress preserved
    player_item = app_page.locator("#player-list li").filter(has_text=player_name)
    expect(player_item).to_be_visible()
    expect(player_item).to_contain_text("Level 2")

    # Selecting should go directly to world map (has progress)
    player_item.click()
    app_page.wait_for_selector("#world-map-screen.active", timeout=5000)
    expect(app_page.locator("#world-map-player")).to_contain_text(player_name)


def test_back_button_switches_player_without_logout(app_page: Page) -> None:
    """Back button should switch players but keep all tokens intact."""
    # Create first player
    player1 = generate_unique_name("Player1")
    app_page.get_by_role("button", name="New Player").click()
    app_page.locator("#new-player-name").fill(player1)
    app_page.get_by_role("button", name="Create").click()

    # Navigate to world map
    app_page.wait_for_selector("#intro-screen.active")
    app_page.locator("#intro-screen").click()
    app_page.wait_for_selector("#world-intro-screen.active")
    app_page.locator("#world-intro-screen").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Complete level 1 so player1 has progress (required for direct world map access)
    app_page.locator(".level-item").last.click()
    app_page.wait_for_selector("#gameplay-screen.active")
    app_page.keyboard.press("F9")  # Cheat to pass
    app_page.wait_for_selector("#result-screen.active")
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Go back to player select
    app_page.get_by_role("button", name="Back").click()
    app_page.wait_for_selector("#player-select-screen.active")

    # Create second player
    player2 = generate_unique_name("Player2")
    app_page.get_by_role("button", name="New Player").click()
    app_page.locator("#new-player-name").fill(player2)
    app_page.get_by_role("button", name="Create").click()

    # Navigate to world map
    app_page.wait_for_selector("#intro-screen.active")
    app_page.locator("#intro-screen").click()
    app_page.wait_for_selector("#world-intro-screen.active")
    app_page.locator("#world-intro-screen").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Go back and verify both players are in the list
    app_page.get_by_role("button", name="Back").click()
    app_page.wait_for_selector("#player-select-screen.active")

    expect(app_page.locator("#player-list li").filter(has_text=player1)).to_be_visible()
    expect(app_page.locator("#player-list li").filter(has_text=player2)).to_be_visible()

    # Select first player - should go directly to world map (has progress)
    app_page.locator("#player-list li").filter(has_text=player1).click()
    app_page.wait_for_selector("#world-map-screen.active")
    expect(app_page.locator("#world-map-player")).to_contain_text(player1)


def test_progress_preserved_after_switching_players(app_page: Page) -> None:
    """Player progress should be preserved when switching between players."""
    # Create first player and complete a level
    player1 = generate_unique_name("Progress1")
    app_page.get_by_role("button", name="New Player").click()
    app_page.locator("#new-player-name").fill(player1)
    app_page.get_by_role("button", name="Create").click()

    app_page.wait_for_selector("#intro-screen.active")
    app_page.locator("#intro-screen").click()
    app_page.wait_for_selector("#world-intro-screen.active")
    app_page.locator("#world-intro-screen").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Complete level 1
    app_page.locator(".level-item").last.click()
    app_page.wait_for_selector("#gameplay-screen.active")
    app_page.keyboard.press("F9")  # Cheat to pass
    app_page.wait_for_selector("#result-screen.active")
    app_page.get_by_role("button", name="Continue").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Go back and create second player
    app_page.get_by_role("button", name="Back").click()
    app_page.wait_for_selector("#player-select-screen.active")

    player2 = generate_unique_name("Progress2")
    app_page.get_by_role("button", name="New Player").click()
    app_page.locator("#new-player-name").fill(player2)
    app_page.get_by_role("button", name="Create").click()

    app_page.wait_for_selector("#intro-screen.active")
    app_page.locator("#intro-screen").click()
    app_page.wait_for_selector("#world-intro-screen.active")
    app_page.locator("#world-intro-screen").click()
    app_page.wait_for_selector("#world-map-screen.active")

    # Go back and select first player again
    app_page.get_by_role("button", name="Back").click()
    app_page.wait_for_selector("#player-select-screen.active")

    # First player should show Level 2 (completed level 1)
    player1_item = app_page.locator("#player-list li").filter(has_text=player1)
    expect(player1_item).to_contain_text("Level 2")

    # Second player should show Level 1 (no progress)
    player2_item = app_page.locator("#player-list li").filter(has_text=player2)
    expect(player2_item).to_contain_text("Level 1")
