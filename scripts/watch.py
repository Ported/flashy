#!/usr/bin/env python3
"""Watch for changes and auto-rebuild the web version with live reload.

Usage:
    poetry run python scripts/watch.py
"""

import asyncio
import subprocess
import sys
from pathlib import Path

# Files/folders to watch
WATCH_PATHS = [
    Path("flashy/core"),
    Path("flashy/platforms/web/index.html"),
]

BUILD_SCRIPT = Path("flashy/platforms/web/build.py")
RELOAD_PORT = 35729

# Connected WebSocket clients
clients: set[asyncio.Queue[str]] = set()


def get_mtimes() -> dict[Path, float]:
    """Get modification times for all watched files."""
    mtimes = {}
    for watch_path in WATCH_PATHS:
        if watch_path.is_file():
            mtimes[watch_path] = watch_path.stat().st_mtime
        elif watch_path.is_dir():
            for f in watch_path.rglob("*.py"):
                mtimes[f] = f.stat().st_mtime
    return mtimes


def build() -> bool:
    """Run the build script. Returns True on success."""
    print("\n🔨 Building...", flush=True)
    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT)],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("✅ Build complete!", flush=True)
        return True
    else:
        print(f"❌ Build failed:\n{result.stderr}", flush=True)
        return False


async def notify_clients() -> None:
    """Send reload signal to all connected browsers."""
    if clients:
        print(f"🔄 Reloading {len(clients)} browser(s)...", flush=True)
        for queue in clients:
            await queue.put("reload")


async def handle_client(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    """Handle SSE client connection."""
    queue: asyncio.Queue[str] = asyncio.Queue()
    clients.add(queue)
    print(f"🌐 Browser connected (total: {len(clients)})")

    try:
        # Send SSE headers
        writer.write(b"HTTP/1.1 200 OK\r\n")
        writer.write(b"Content-Type: text/event-stream\r\n")
        writer.write(b"Cache-Control: no-cache\r\n")
        writer.write(b"Access-Control-Allow-Origin: *\r\n")
        writer.write(b"Connection: keep-alive\r\n\r\n")
        await writer.drain()

        while True:
            msg = await queue.get()
            writer.write(f"data: {msg}\n\n".encode())
            await writer.drain()
    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        clients.discard(queue)
        print(f"🌐 Browser disconnected (total: {len(clients)})")
        writer.close()


async def watch_files() -> None:
    """Watch for file changes and rebuild."""
    last_mtimes = get_mtimes()
    build()  # Initial build

    while True:
        await asyncio.sleep(0.5)
        current_mtimes = get_mtimes()

        changed = []
        for path, mtime in current_mtimes.items():
            if path not in last_mtimes or last_mtimes[path] != mtime:
                changed.append(path)

        if changed:
            for p in changed:
                print(f"📝 Changed: {p}")
            if build():
                await notify_clients()
            last_mtimes = current_mtimes


async def main() -> None:
    print("👀 Watching for changes with live reload...")
    print("   - flashy/core/*.py")
    print("   - flashy/platforms/web/index.html")
    print(f"\n🔌 Live reload server on port {RELOAD_PORT}")
    print("   (Browser will auto-refresh on changes)\n")

    server = await asyncio.start_server(handle_client, "localhost", RELOAD_PORT)

    async with server:
        await asyncio.gather(
            server.serve_forever(),
            watch_files(),
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Stopped watching.")
