#!/bin/bash
# Deploy Flashy web platform to Cloudflare Pages
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔨 Building flashy_core.py..."
python build.py

echo "📦 Preparing deployment directory..."
DEPLOY_DIR=$(mktemp -d)
trap "rm -rf $DEPLOY_DIR" EXIT

# Copy only the files needed for deployment
cp index.html "$DEPLOY_DIR/"
cp flashy_core.py "$DEPLOY_DIR/"
cp favicon.svg "$DEPLOY_DIR/"
cp _headers "$DEPLOY_DIR/"

# Copy optimized assets (not originals)
mkdir -p "$DEPLOY_DIR/assets/backgrounds"
cp assets/backgrounds/*.webp "$DEPLOY_DIR/assets/backgrounds/"

# Copy Functions for API
cp -r functions "$DEPLOY_DIR/" 2>/dev/null || true

echo "🚀 Deploying to Cloudflare Pages..."
wrangler pages deploy "$DEPLOY_DIR" --project-name=flashycards --commit-dirty=true

echo "✅ Deployment complete!"
