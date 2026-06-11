#!/usr/bin/env python3
"""Build a compact gallery showcase from committed VESTA-rendered PNGs."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Tuple

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GALLERY = ROOT / "docs" / "assets" / "gallery"
DEFAULT_OUTPUT = DEFAULT_GALLERY / "feature_closure_showcase.png"


PANELS: Tuple[Tuple[str, str, str], ...] = (
    ("ag111_benzene_igmh_aim_front.png", "Ag(111)+benzene", "IGMH + AIM periodic front view"),
    ("ag111_benzene_igmh_aim_top.png", "Ag(111)+benzene", "IGMH + AIM periodic top view"),
    ("gc_aim_overlay.png", "GC base pair", "AIM paths and BCP overlay"),
    ("cdcl_nvt_trajectory_frame.png", "Cd/Cl trajectory", "Reference-style VESTA frame"),
    ("benzene_aim_overlay.png", "Benzene", "Basic AIM overlay"),
    ("h2o_iri_aim_overlay.png", "H2O-HF", "IRI + AIM debug evidence"),
)


def _font(size: int) -> ImageFont.ImageFont:
    candidates = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def _fit(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
    width, height = size
    source = image.convert("RGB")
    scale = min(width / source.width, height / source.height)
    resized = source.resize((int(source.width * scale), int(source.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGB", size, (246, 247, 248))
    x = (width - resized.width) // 2
    y = (height - resized.height) // 2
    canvas.paste(resized, (x, y))
    return canvas


def build_showcase(
    gallery_dir: Path = DEFAULT_GALLERY,
    output: Path = DEFAULT_OUTPUT,
    panels: Iterable[Tuple[str, str, str]] = PANELS,
) -> Path:
    title_font = _font(36)
    subtitle_font = _font(20)
    label_font = _font(20)
    small_font = _font(14)
    margin = 28
    gap = 18
    card_w = 520
    card_h = 348
    image_h = 272
    columns = 3
    panel_list = list(panels)
    rows = (len(panel_list) + columns - 1) // columns
    width = margin * 2 + columns * card_w + (columns - 1) * gap
    header_h = 118
    height = margin + header_h + rows * card_h + (rows - 1) * gap + margin

    canvas = Image.new("RGB", (width, height), (238, 241, 244))
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (margin, margin),
        "multiwfn2vesta feature closure showcase",
        fill=(28, 36, 45),
        font=title_font,
    )
    draw.text(
        (margin, margin + 50),
        "Assembled only from committed real VESTA renders; missing features stay marked needs-render.",
        fill=(80, 88, 98),
        font=subtitle_font,
    )

    for index, (filename, label, caption) in enumerate(panel_list):
        row, col = divmod(index, columns)
        x = margin + col * (card_w + gap)
        y = margin + header_h + row * (card_h + gap)
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=8, fill=(255, 255, 255), outline=(212, 218, 226))
        path = gallery_dir / filename
        if not path.exists():
            draw.rectangle((x + 12, y + 12, x + card_w - 12, y + image_h), fill=(232, 236, 240))
            draw.text((x + 24, y + 120), f"missing: {filename}", fill=(120, 48, 48), font=label_font)
        else:
            image = _fit(Image.open(path), (card_w - 24, image_h - 12))
            canvas.paste(image, (x + 12, y + 12))
        text_y = y + image_h + 10
        draw.text((x + 18, text_y), label, fill=(31, 41, 55), font=label_font)
        draw.text((x + 18, text_y + 28), caption, fill=(91, 100, 112), font=small_font)

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gallery-dir", type=Path, default=DEFAULT_GALLERY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = build_showcase(args.gallery_dir, args.output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
