from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


RAMP = " .:-=+*#%@"


def image_data(channel: Image.Image):
    return channel.get_flattened_data() if hasattr(channel, "get_flattened_data") else channel.getdata()


def format_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def render_ascii(image: Image.Image, width: int, mode: str) -> str:
    rgba = image.convert("RGBA")
    src_w, src_h = rgba.size
    height = max(4, round(src_h / src_w * width * 0.45))
    small = rgba.resize((width, height), Image.Resampling.LANCZOS)

    if mode == "alpha":
        values = list(image_data(small.getchannel("A")))
    else:
        gray = small.convert("L")
        alpha = list(image_data(small.getchannel("A")))
        values = [v if a > 0 else 255 for v, a in zip(image_data(gray), alpha)]

    lines: list[str] = []
    for y in range(height):
        row = []
        for x in range(width):
            v = values[y * width + x]
            if mode == "gray":
                v = 255 - v
            row.append(RAMP[min(len(RAMP) - 1, v * (len(RAMP) - 1) // 255)])
        lines.append("".join(row).rstrip())
    return "\n".join(lines)


def inspect(path: Path, width: int, mode: str) -> str:
    image = Image.open(path).convert("RGBA")
    total = image.width * image.height
    alpha = list(image_data(image.getchannel("A")))
    visible = sum(1 for value in alpha if value > 0)
    near_black = 0
    for r, g, b, a in image_data(image):
        if a > 0 and r < 12 and g < 12 and b < 12:
            near_black += 1

    lines = [
        f"# {path.as_posix()}",
        f"size: {image.width}x{image.height}",
        f"alpha coverage: {format_pct(visible / total if total else 0)}",
        f"near-black visible: {format_pct(near_black / visible if visible else 0)}",
        f"bbox: {image.getbbox()}",
        f"mode: {mode}",
        "",
        render_ascii(image, width, mode),
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an image as terminal-readable ASCII for visual inspection.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--width", type=int, default=72)
    parser.add_argument("--mode", choices=("gray", "alpha"), default="gray")
    args = parser.parse_args()

    for index, path in enumerate(args.paths):
        if index:
            print("\n" + "=" * 80 + "\n")
        print(inspect(path, args.width, args.mode))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
