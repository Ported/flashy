#!/bin/bash
# Deploy Flutter web app to Cloudflare Pages
#
# Usage:
#   ./deploy-web.sh              # Build and deploy to production
#   ./deploy-web.sh --build-only # Just build to build/web (for CI)
#   ./deploy-web.sh --staging    # Build for staging (uses production API)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLUTTER_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WEB_DIR="$FLUTTER_DIR/../flashy/platforms/web"

cd "$FLUTTER_DIR"

BUILD_ONLY=false
STAGING=false

for arg in "$@"; do
    case $arg in
        --build-only)
            BUILD_ONLY=true
            ;;
        --staging)
            STAGING=true
            ;;
    esac
done

echo "🔨 Building Flutter web app..."

# Build Flutter web
if [[ "$STAGING" == true ]]; then
    echo "   (staging build - using production API)"
    flutter build web --release --dart-define=FLASHY_API_BASE_URL=https://flashycards.org
else
    echo "   (production build - same-origin API)"
    flutter build web --release
fi

DEPLOY_DIR="$FLUTTER_DIR/build/web"

echo "📦 Copying API functions and config..."
mkdir -p "$DEPLOY_DIR/functions/api"

# Copy Functions for API (only .ts files, not tests)
cp "$WEB_DIR/functions/_middleware.ts" "$DEPLOY_DIR/functions/" 2>/dev/null || true
cp "$WEB_DIR/functions/api/"*.ts "$DEPLOY_DIR/functions/api/" 2>/dev/null || true
# Remove test files from deploy
rm -f "$DEPLOY_DIR/functions/api/"*.test.ts 2>/dev/null || true

# Copy _headers for caching rules and wrangler.toml for D1 binding
cp "$WEB_DIR/_headers" "$DEPLOY_DIR/" 2>/dev/null || true
cp "$WEB_DIR/wrangler.toml" "$DEPLOY_DIR/" 2>/dev/null || true

echo "✅ Build complete: $DEPLOY_DIR"

if [[ "$BUILD_ONLY" == true ]]; then
    echo "📁 Contents:"
    find "$DEPLOY_DIR" -type f | sort | head -30
    echo "..."
    exit 0
fi

# Deploy
PROJECT_NAME="flashycards"
echo "🚀 Deploying to Cloudflare Pages ($PROJECT_NAME)..."
wrangler pages deploy "$DEPLOY_DIR" --project-name=$PROJECT_NAME --commit-dirty=true

echo "✅ Deployment complete!"
