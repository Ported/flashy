#!/bin/bash
# Generate app icons from SVG for all platforms
# Requires: rsvg-convert (librsvg), magick (ImageMagick)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLUTTER_DIR="$(dirname "$SCRIPT_DIR")"
SVG_SOURCE="/Users/greg/git/flashy-v2/flashy-icon.svg"

echo "Generating icons from: $SVG_SOURCE"

# Create temp directory for intermediate files
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Generate a master 1024x1024 PNG first
echo "Creating master 1024x1024 PNG..."
rsvg-convert -w 1024 -h 1024 "$SVG_SOURCE" -o "$TEMP_DIR/icon-1024.png"

# Function to resize PNG
resize_png() {
    local size=$1
    local output=$2
    magick "$TEMP_DIR/icon-1024.png" -resize "${size}x${size}" "$output"
    echo "  Created: $output (${size}x${size})"
}

# ============================================================
# Web icons
# ============================================================
echo ""
echo "=== Web Icons ==="
WEB_DIR="$FLUTTER_DIR/web"

resize_png 16 "$WEB_DIR/favicon.png"
resize_png 192 "$WEB_DIR/icons/Icon-192.png"
resize_png 512 "$WEB_DIR/icons/Icon-512.png"
resize_png 192 "$WEB_DIR/icons/Icon-maskable-192.png"
resize_png 512 "$WEB_DIR/icons/Icon-maskable-512.png"

# ============================================================
# Android icons
# ============================================================
echo ""
echo "=== Android Icons ==="
ANDROID_DIR="$FLUTTER_DIR/android/app/src/main/res"

resize_png 48 "$ANDROID_DIR/mipmap-mdpi/ic_launcher.png"
resize_png 72 "$ANDROID_DIR/mipmap-hdpi/ic_launcher.png"
resize_png 96 "$ANDROID_DIR/mipmap-xhdpi/ic_launcher.png"
resize_png 144 "$ANDROID_DIR/mipmap-xxhdpi/ic_launcher.png"
resize_png 192 "$ANDROID_DIR/mipmap-xxxhdpi/ic_launcher.png"

# ============================================================
# iOS icons
# ============================================================
echo ""
echo "=== iOS Icons ==="
IOS_DIR="$FLUTTER_DIR/ios/Runner/Assets.xcassets/AppIcon.appiconset"

resize_png 20 "$IOS_DIR/Icon-App-20x20@1x.png"
resize_png 40 "$IOS_DIR/Icon-App-20x20@2x.png"
resize_png 60 "$IOS_DIR/Icon-App-20x20@3x.png"
resize_png 29 "$IOS_DIR/Icon-App-29x29@1x.png"
resize_png 58 "$IOS_DIR/Icon-App-29x29@2x.png"
resize_png 87 "$IOS_DIR/Icon-App-29x29@3x.png"
resize_png 40 "$IOS_DIR/Icon-App-40x40@1x.png"
resize_png 80 "$IOS_DIR/Icon-App-40x40@2x.png"
resize_png 120 "$IOS_DIR/Icon-App-40x40@3x.png"
resize_png 60 "$IOS_DIR/Icon-App-60x60@2x.png"
resize_png 180 "$IOS_DIR/Icon-App-60x60@3x.png"
resize_png 76 "$IOS_DIR/Icon-App-76x76@1x.png"
resize_png 152 "$IOS_DIR/Icon-App-76x76@2x.png"
resize_png 167 "$IOS_DIR/Icon-App-83.5x83.5@2x.png"
resize_png 1024 "$IOS_DIR/Icon-App-1024x1024@1x.png"

# ============================================================
# macOS icons
# ============================================================
echo ""
echo "=== macOS Icons ==="
MACOS_DIR="$FLUTTER_DIR/macos/Runner/Assets.xcassets/AppIcon.appiconset"

resize_png 16 "$MACOS_DIR/app_icon_16.png"
resize_png 32 "$MACOS_DIR/app_icon_32.png"
resize_png 64 "$MACOS_DIR/app_icon_64.png"
resize_png 128 "$MACOS_DIR/app_icon_128.png"
resize_png 256 "$MACOS_DIR/app_icon_256.png"
resize_png 512 "$MACOS_DIR/app_icon_512.png"
resize_png 1024 "$MACOS_DIR/app_icon_1024.png"

# ============================================================
# Windows icon (.ico)
# ============================================================
echo ""
echo "=== Windows Icon ==="
WINDOWS_DIR="$FLUTTER_DIR/windows/runner/resources"

# Create multiple sizes for ICO file
magick "$TEMP_DIR/icon-1024.png" \
    \( -clone 0 -resize 16x16 \) \
    \( -clone 0 -resize 32x32 \) \
    \( -clone 0 -resize 48x48 \) \
    \( -clone 0 -resize 64x64 \) \
    \( -clone 0 -resize 128x128 \) \
    \( -clone 0 -resize 256x256 \) \
    -delete 0 \
    "$WINDOWS_DIR/app_icon.ico"
echo "  Created: $WINDOWS_DIR/app_icon.ico"

echo ""
echo "Done! All icons generated successfully."
