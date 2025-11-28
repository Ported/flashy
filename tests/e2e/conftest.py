"""E2E test fixtures for Playwright testing."""

import shutil
import signal
import subprocess
import sys
import time
import uuid
from collections.abc import Generator
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Page


def generate_unique_name(base: str = "Player") -> str:
    """Generate a unique player name using UUID suffix."""
    return f"{base}_{uuid.uuid4().hex[:8]}"

# Path to web platform files
WEB_DIR = Path(__file__).parent.parent.parent / "flashy" / "platforms" / "web"
BUILD_SCRIPT = WEB_DIR / "build.py"


def find_free_port() -> int:
    """Find a free port to use."""
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def web_server() -> Generator[str, None, None]:
    """Start wrangler pages dev to serve the app with D1 database.

    Rebuilds flashy_core.py before starting the server.
    """
    # Run build script to ensure flashy_core.py is up to date
    subprocess.run([sys.executable, str(BUILD_SCRIPT)], check=True, cwd=WEB_DIR.parent)

    # Find wrangler
    wrangler = shutil.which("wrangler")
    if not wrangler:
        # Try npx
        wrangler = "npx"
        wrangler_args = ["wrangler"]
    else:
        wrangler_args = []

    port = find_free_port()

    # Clear any existing test database for a fresh start
    e2e_state_dir = WEB_DIR / ".wrangler" / "state" / "e2e"
    if e2e_state_dir.exists():
        shutil.rmtree(e2e_state_dir)

    # Start wrangler pages dev with local D1
    # --local runs everything locally without needing Cloudflare auth
    # --persist keeps the D1 data in .wrangler/state
    process = subprocess.Popen(
        [
            wrangler,
            *wrangler_args,
            "pages",
            "dev",
            str(WEB_DIR),
            "--port",
            str(port),
            "--d1=DB",
            "--local",
            "--persist-to",
            str(e2e_state_dir),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=WEB_DIR,
    )

    # Wait for server to be ready
    url = f"http://localhost:{port}"
    max_wait = 30
    start = time.time()
    while time.time() - start < max_wait:
        try:
            import urllib.request

            urllib.request.urlopen(url, timeout=1)
            break
        except Exception:
            time.sleep(0.5)
    else:
        process.terminate()
        raise RuntimeError(f"Wrangler did not start within {max_wait}s")

    # Initialize the database schema via the init endpoint
    import urllib.request

    try:
        req = urllib.request.Request(f"{url}/api/init", method="POST")
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"Schema init warning: {e}")

    yield url

    # Cleanup
    process.send_signal(signal.SIGTERM)
    process.wait(timeout=5)


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


def pytest_configure(config: pytest.Config) -> None:
    """Set default Playwright timeouts to be much faster.

    The app is fast, so we don't need to wait 30 seconds for failures.
    """
    from playwright.sync_api import expect

    # Set default expect timeout to 2 seconds (instead of 5s)
    expect.set_options(timeout=2000)


@pytest.fixture(scope="session")
def shared_context(
    browser: "Browser", web_server: str  # type: ignore[name-defined]  # noqa: F821
) -> Generator[BrowserContext, None, None]:
    """Create a shared browser context that persists across all tests.

    This allows the browser cache (Pyodide, models) to be reused.
    """
    context = browser.new_context()
    # Set faster default timeout for actions (5s instead of 30s)
    context.set_default_timeout(5000)

    # Warm up the cache by loading the app once
    page = context.new_page()
    page.goto(web_server)
    page.wait_for_selector("#player-select-screen.active", timeout=120000)
    page.close()

    yield context

    context.close()


@pytest.fixture
def app_page(
    shared_context: BrowserContext, web_server: str
) -> Generator[Page, None, None]:
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
def mobile_page(
    shared_context: BrowserContext, web_server: str
) -> Generator[Page, None, None]:
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
