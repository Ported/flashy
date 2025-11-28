#!/bin/bash
# Deploy Flashy web platform to Cloudflare Pages
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔨 Building flashy_core.py..."
python build.py

echo "🚀 Deploying to Cloudflare Pages..."
wrangler pages deploy . --project-name=flashycards --commit-dirty=true

echo "✅ Deployment complete!"
