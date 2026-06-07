#!/usr/bin/env python3
"""Generate front/right/top VESTA view files from one input .vesta file.

Rendering is opt-in because local Windows VESTA automation has been confirmed
to steal desktop focus.  Use --render-command only when that interruption is
acceptable or when a non-activating renderer is available.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from add_single_view_compass import add_compass


SCENES = {
    # Screen convention: right/up are positive coordinates for the named plane.
    "front": [
        " 1.000000  0.000000  0.000000  0.000000",
        " 0.000000  0.000000  1.000000  0.000000",
        " 0.000000 -1.000000  0.000000  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        "  0.000   0.000",
        "  0.000",
        "  0.800",
    ],
    "right": [
        " 0.000000  1.000000  0.000000  0.000000",
        " 0.000000  0.000000  1.000000  0.000000",
        " 1.000000  0.000000  0.000000  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        "  0.000   0.000",
        "  0.000",
        "  0.800",
    ],
    "top": [
        " 1.000000  0.000000  0.000000  0.000000",
        " 0.000000  1.000000  0.000000  0.000000",
        " 0.000000  0.000000  1.000000  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        "  0.000   0.000",
        "  0.000",
        "  0.800",
    ],
}


def replace_scene(text: str, scene_lines: list[str]) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() == "SCENE":
            lines[idx + 1 : idx + 8] = scene_lines
            return "\n".join(lines) + "\n"
    raise SystemExit("No SCENE block found")


def patch_comps(text: str, mode: str) -> str:
    if mode == "keep":
        return text
    value = "1" if mode == "on" else "0"
    lines = text.splitlines()
    changed = False
    for idx, line in enumerate(lines):
        if line.strip().startswith("COMPS "):
            lines[idx] = f"COMPS {value}"
            changed = True
    if not changed:
        lines.append(f"COMPS {value}")
    return "\n".join(lines) + "\n"


def copy_relative_cubes(text: str, source_dir: Path, out_dir: Path) -> None:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() in {"IMPORT_DENSITY 1", "IMPORT_TEXTURE"} and idx + 1 < len(lines):
            fields = lines[idx + 1].split()
            if len(fields) >= 2:
                cube = Path(fields[-1])
                if not cube.is_absolute():
                    src = source_dir / cube
                    if src.exists():
                        shutil.copy2(src, out_dir / cube.name)


def render_view(command_template: str, input_path: Path, output_path: Path, view: str) -> None:
    command = command_template.format(input=input_path, output=output_path, view=view)
    subprocess.run(command, shell=True, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_vesta")
    parser.add_argument("output_dir")
    parser.add_argument("--stem", help="Output filename stem. Default: input stem")
    parser.add_argument("--views", nargs="+", choices=sorted(SCENES), default=["front", "right", "top"])
    parser.add_argument("--comps", choices=["off", "on", "keep"], default="off")
    parser.add_argument(
        "--render-command",
        help=(
            "Optional shell command template using {input}, {output}, and {view}. "
            "Example: 'python3 project/scripts/render_vesta_nofocus.py {input} {output}'"
        ),
    )
    parser.add_argument("--render-suffix", default=".png")
    parser.add_argument("--add-compass", action="store_true", help="Add one compass after rendering")
    args = parser.parse_args()

    source = Path(args.input_vesta)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8", errors="replace")
    copy_relative_cubes(text, source.parent, out_dir)
    text = patch_comps(text, args.comps)
    stem = args.stem or source.stem

    for view in args.views:
        view_path = out_dir / f"{stem}_{view}.vesta"
        view_path.write_text(replace_scene(text, SCENES[view]), encoding="utf-8")
        print(view_path)
        if args.render_command:
            png_path = out_dir / f"{stem}_{view}{args.render_suffix}"
            render_view(args.render_command, view_path, png_path, view)
            if args.add_compass:
                add_compass(png_path, view, None)
            print(png_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
