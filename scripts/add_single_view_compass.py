#!/usr/bin/env python3
"""Add one screen-fixed, VESTA-like coordinate compass to exported PNGs."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


VIEWS = {
    "front": (("a", (220, 30, 30), (1.0, 0.0)), ("c", (35, 65, 220), (0.0, -1.0))),
    "right": (("b", (20, 170, 40), (1.0, 0.0)), ("c", (35, 65, 220), (0.0, -1.0))),
    "top": (("a", (220, 30, 30), (1.0, 0.0)), ("b", (20, 170, 40), (0.5, -0.85))),
}


def compass_font(size: int) -> ImageFont.ImageFont:
    for candidate in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def arrow(
    draw: ImageDraw.ImageDraw,
    origin: tuple[int, int],
    vector: tuple[float, float],
    color: tuple[int, int, int],
    label: str,
    length: int,
    width: int,
    font: ImageFont.ImageFont,
) -> None:
    ox, oy = origin
    vx, vy = vector
    norm = math.hypot(vx, vy)
    vx, vy = vx / norm, vy / norm
    ex = ox + int(vx * length)
    ey = oy + int(vy * length)
    draw.line((ox, oy, ex, ey), fill=color, width=width)
    head = max(12, width * 4)
    angle = math.atan2(vy, vx)
    points = [(ex, ey)]
    for delta in (0.48, -0.48):
        points.append(
            (
                ex - int(math.cos(angle + delta) * head),
                ey - int(math.sin(angle + delta) * head),
            )
        )
    draw.polygon(points, fill=color)
    label_x = ex + int(vx * 22) + int(-vy * 6)
    label_y = ey + int(vy * 22) + int(vx * 6) - 12
    draw.text((label_x, label_y), label, fill=(0, 0, 0), font=font)


def add_compass(path: Path, view: str, output: Path | None) -> None:
    image = Image.open(path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    width, height = image.size
    origin = (max(90, width // 12), height - max(90, height // 8))
    length = max(90, min(width, height) // 9)
    line_width = max(5, min(width, height) // 220)
    font = compass_font(max(18, min(width, height) // 65))
    clear_pad = max(34, line_width * 5)
    clear_box = (
        0,
        max(0, origin[1] - length - clear_pad),
        min(width, origin[0] + length + clear_pad * 2),
        height,
    )
    background = image.getpixel((0, 0))
    draw.rectangle(clear_box, fill=background)

    # Small origin sphere, matching VESTA's unobtrusive lower-left axis marker.
    r = line_width * 2
    draw.ellipse(
        (origin[0] - r, origin[1] - r, origin[0] + r, origin[1] + r),
        fill=(230, 230, 230),
        outline=(80, 80, 80),
    )
    for label, color, vector in VIEWS[view]:
        arrow(draw, origin, vector, color, label, length, line_width, font)
    image.convert("RGB").save(output or path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("png")
    parser.add_argument("--view", choices=sorted(VIEWS), required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    add_compass(Path(args.png), args.view, Path(args.output) if args.output else None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
