#!/bin/bash
# Start local development server with Cloudflare D1 support and live reload

PORT=8765
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WEB_DIR="$SCRIPT_DIR/../flashy/platforms/web"

# Kill any existing process on the port
if lsof -i :$PORT > /dev/null 2>&1; then
    echo "Killing existing process on port $PORT..."
    kill $(lsof -t -i :$PORT) 2>/dev/null
    sleep 1
fi

# Kill any existing live reload server
if lsof -i :35729 > /dev/null 2>&1; then
    echo "Killing existing live reload server..."
    kill $(lsof -t -i :35729) 2>/dev/null
    sleep 1
fi

# Get local IP for mobile testing
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")

echo "Starting wrangler pages dev + live reload..."
echo ""
echo "Local:  http://localhost:$PORT"
echo "Mobile: http://$LOCAL_IP:$PORT"
echo ""

# Start wrangler in background
cd "$WEB_DIR"
wrangler pages dev . --port $PORT --ip 0.0.0.0 &
WRANGLER_PID=$!

# Wait for server to be ready
echo "Waiting for server to start..."
for i in {1..30}; do
    if curl -s http://localhost:$PORT > /dev/null 2>&1; then
        break
    fi
    sleep 0.5
done

# Initialize the D1 database
echo "Initializing D1 database..."
curl -s -X POST http://localhost:$PORT/api/init | cat
echo ""

# Start the watch script for live reload
cd "$SCRIPT_DIR/.."
poetry run python scripts/watch.py &
WATCH_PID=$!

echo ""
echo "Ready! Live reload enabled. Press Ctrl+C to stop."

# Cleanup function
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $WRANGLER_PID 2>/dev/null
    kill $WATCH_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for either process to exit
wait $WRANGLER_PID $WATCH_PID
