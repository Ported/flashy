#!/usr/bin/env python3
"""Process original artwork into web-optimized background images.

Usage:
    poetry run python scripts/process_assets.py

Input: assets/originals/world-{N}-{name}.{png,jpg,heic}
Output: assets/backgrounds/world-{N}-{name}.webp

Processing:
1. Keep full height, center-crop width to square (1:1) if wider
2. Resize to max 1080px height
3. Convert to WebP with quality 80 (good balance of size/quality)

The originals are never modified.
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Run: poetry add pillow")
    sys.exit(1)

# Register HEIC support (for iPhone photos)
try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
except ImportError:
    print("Note: pillow-heif not installed. HEIC files won't be supported.")
    print("      Run: poetry add pillow-heif")

ASSETS_DIR = Path(__file__).parent.parent / "assets"
ORIGINALS_DIR = ASSETS_DIR / "originals"
BACKGROUNDS_DIR = ASSETS_DIR / "backgrounds"

# Target: square aspect ratio (1:1) - works well with CSS background-size: cover
# Only crops width, never height
TARGET_RATIO = 1.0

# Max output height (width will match based on aspect ratio)
MAX_HEIGHT = 1080

# WebP quality (0-100, higher = better quality, larger file)
WEBP_QUALITY = 80


def center_crop_width_only(img: Image.Image, target_ratio: float) -> Image.Image:
    """Center crop width to target aspect ratio. Never crops height."""
    width, height = img.size
    current_ratio = width / height

    if current_ratio > target_ratio:
        # Image is wider than target, crop width from both sides
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        return img.crop((left, 0, left + new_width, height))
    else:
        # Image is square or taller than target - keep as-is
        return img


def process_image(input_path: Path, output_path: Path) -> None:
    """Process a single image: crop, resize, convert to WebP."""
    print(f"Processing: {input_path.name}")

    # Open and convert to RGB (WebP doesn't support all modes)
    with Image.open(input_path) as img:
        # Handle EXIF rotation metadata (common in phone photos)
        try:
            from PIL import ImageOps

            img = ImageOps.exif_transpose(img)  # type: ignore[assignment]
        except Exception:
            pass

        # Convert to RGB
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")

        original_size = img.size
        print(f"  Original: {original_size[0]}x{original_size[1]}")

        # Center crop width only (preserve full height)
        img = center_crop_width_only(img, TARGET_RATIO)
        print(f"  After crop: {img.size[0]}x{img.size[1]}")

        # Resize if taller than max height
        if img.size[1] > MAX_HEIGHT:
            # Calculate new width to maintain aspect ratio
            scale = MAX_HEIGHT / img.size[1]
            new_width = int(img.size[0] * scale)
            img = img.resize((new_width, MAX_HEIGHT), Image.Resampling.LANCZOS)
            print(f"  After resize: {img.size[0]}x{img.size[1]}")

        # Save as WebP
        img.save(output_path, "WEBP", quality=WEBP_QUALITY)

        # Report size
        size_kb = output_path.stat().st_size / 1024
        print(f"  Output: {output_path.name} ({size_kb:.1f} KB)")


def main() -> int:
    """Process all world background originals."""
    # Ensure output directory exists
    BACKGROUNDS_DIR.mkdir(parents=True, exist_ok=True)

    # Find all world background originals (case-insensitive extensions)
    patterns = [
        "world-*.png", "world-*.PNG",
        "world-*.jpg", "world-*.JPG",
        "world-*.jpeg", "world-*.JPEG",
        "world-*.heic", "world-*.HEIC",
    ]
    originals: list[Path] = []
    for pattern in patterns:
        originals.extend(ORIGINALS_DIR.glob(pattern))

    if not originals:
        print(f"No world-*.{{png,jpg,heic}} files found in {ORIGINALS_DIR}")
        print("Expected files like: world-1-addition-alps.png")
        return 1

    print(f"Found {len(originals)} original(s) to process\n")

    for original in sorted(originals):
        # Output filename: same name but .webp extension
        output_name = original.stem + ".webp"
        output_path = BACKGROUNDS_DIR / output_name
        process_image(original, output_path)
        print()

    print("Done! Processed backgrounds are in assets/backgrounds/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
