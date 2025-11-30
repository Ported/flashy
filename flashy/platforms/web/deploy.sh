#!/bin/bash
# Deploy Flashy web platform to Cloudflare Pages
#
# Usage:
#   ./deploy.sh              # Build and deploy
#   ./deploy.sh --build-only # Just build to dist/ (for CI)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

BUILD_ONLY=false
if [[ "$1" == "--build-only" ]]; then
    BUILD_ONLY=true
fi

echo "🔨 Building flashy_core.py..."
python build.py

echo "📦 Preparing deployment directory..."
DEPLOY_DIR="$SCRIPT_DIR/dist"
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR/assets/backgrounds" "$DEPLOY_DIR/functions/api"

# Copy only the files needed for deployment
cp index.html "$DEPLOY_DIR/"
cp flashy_core.py "$DEPLOY_DIR/"
cp favicon.svg "$DEPLOY_DIR/"
cp _headers "$DEPLOY_DIR/"

# Copy optimized assets (not originals)
cp assets/backgrounds/*.webp "$DEPLOY_DIR/assets/backgrounds/"

# Copy Functions for API (only .ts files, not tests or node_modules)
cp functions/api/*.ts "$DEPLOY_DIR/functions/api/" 2>/dev/null || true
# Remove test files from deploy
rm -f "$DEPLOY_DIR/functions/api/"*.test.ts 2>/dev/null || true

echo "✅ Build complete: $DEPLOY_DIR"

if [[ "$BUILD_ONLY" == true ]]; then
    echo "📁 Contents:"
    find "$DEPLOY_DIR" -type f | sort
    exit 0
fi

echo "🚀 Deploying to Cloudflare Pages..."
wrangler pages deploy "$DEPLOY_DIR" --project-name=flashycards --commit-dirty=true

echo "✅ Deployment complete!"
