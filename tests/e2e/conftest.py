"""E2E test fixtures for Playwright testing."""

import subprocess
import sys
import threading
import time
from collections.abc import Generator
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import TCPServer

import pytest
from playwright.sync_api import BrowserContext, Page

# Path to web platform files
WEB_DIR = Path(__file__).parent.parent.parent / "flashy" / "platforms" / "web"
BUILD_SCRIPT = WEB_DIR / "build.py"


class QuietHandler(SimpleHTTPRequestHandler):
    """HTTP handler that suppresses request logging."""

    def log_message(self, format: str, *args: object) -> None:
        pass  # Suppress logging


@pytest.fixture(scope="session")
def web_server() -> Generator[str, None, None]:
    """Start a local HTTP server serving the web platform files.

    Rebuilds flashy_core.py before starting the server.
    """
    # Run build script to ensure flashy_core.py is up to date
    subprocess.run([sys.executable, str(BUILD_SCRIPT)], check=True, cwd=WEB_DIR.parent)

    # Create server
    class Handler(QuietHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    # Use port 0 to get a random available port
    server = TCPServer(("", 0), Handler)
    port = server.server_address[1]

    # Start server in background thread
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    # Give server time to start
    time.sleep(0.5)

    yield f"http://localhost:{port}"

    # Cleanup
    server.shutdown()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """Configure browser context to keep cache between tests.

    This dramatically speeds up tests by caching Pyodide and model files.
    """
    return {
        **browser_context_args,
        # Keep browser cache warm across tests
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def shared_context(browser: "Browser", web_server: str) -> Generator[BrowserContext, None, None]:  # type: ignore[name-defined]  # noqa: F821
    """Create a shared browser context that persists across all tests.

    This allows the browser cache (Pyodide, models) to be reused.
    """
    context = browser.new_context()

    # Warm up the cache by loading the app once
    page = context.new_page()
    page.goto(web_server)
    page.wait_for_selector("#player-select-screen.active", timeout=120000)
    page.close()

    yield context

    context.close()


@pytest.fixture
def app_page(shared_context: BrowserContext, web_server: str) -> Generator[Page, None, None]:
    """Navigate to the app and wait for it to load.

    Uses shared context for cache, but clears localStorage for test isolation.
    """
    page = shared_context.new_page()
    page.goto(web_server)

    # Clear localStorage for test isolation (but keep browser cache!)
    page.evaluate("localStorage.clear()")
    page.reload()

    # Wait for app to be ready (loading screen disappears)
    # Should be fast now since Pyodide is cached
    page.wait_for_selector("#player-select-screen.active", timeout=60000)

    yield page

    page.close()


@pytest.fixture
def mobile_page(shared_context: BrowserContext, web_server: str) -> Generator[Page, None, None]:
    """Navigate to the app with mobile viewport (iPhone SE size)."""
    page = shared_context.new_page()
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(web_server)

    # Clear localStorage for test isolation
    page.evaluate("localStorage.clear()")
    page.reload()

    # Wait for app to be ready
    page.wait_for_selector("#player-select-screen.active", timeout=60000)

    yield page

    page.close()
