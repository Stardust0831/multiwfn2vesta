#!/usr/bin/env python3
"""Export front/right/top images from one VESTA input using VESTA CLI rotation.

The maintained path opens one source `.vesta` once, exports the current camera
as `front`, rotates the same VESTA graphics area, flushes the screen, then
exports `right` and `top`.  It does not write view-specific `.vesta` files.

`--mode scene-copies` is retained only as a compatibility/diagnostic fallback
for environments where the native `-rotate_*` commands cannot be used.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from add_single_view_compass import add_compass


SCENES = {
    # Compatibility fallback only.  The default export mode uses VESTA CLI
    # -rotate_* commands instead of these matrices.
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

SEQUENCES = {
    # The input file opens in a front-like camera.
    "front": [
        ("front", []),
        ("right", [("-rotate_y", "-90")]),
        ("top", [("-rotate_y", "90"), ("-rotate_x", "-90")]),
    ],
    # The input file opens in a top/surface-normal camera, as in the current
    # Ag(111)+benzene IGMH+AIM saved overlay.
    "top": [
        ("top", []),
        ("right", [("-rotate_y", "-90")]),
        ("front", [("-rotate_y", "90"), ("-rotate_x", "-90")]),
    ],
}

PRINT_ORDER = ["front", "right", "top"]

VIEW_CHOICES = sorted({view for sequence in SEQUENCES.values() for view, _ in sequence})

INITIAL_VIEW_CHOICES = sorted(SEQUENCES)


def selected_sequence(initial_view: str, views: list[str]) -> list[tuple[str, list[tuple[str, str]]]]:
    wanted = set(views)
    sequence = SEQUENCES[initial_view]
    last_index = max(idx for idx, (view, _) in enumerate(sequence) if view in wanted)
    return sequence[: last_index + 1]


def ordered_paths(paths: dict[str, Path]) -> list[tuple[str, Path]]:
    return [(view, paths[view]) for view in PRINT_ORDER if view in paths]


def rotate_command(axis: str) -> str:
    return {"x": "-rotate_x", "y": "-rotate_y", "z": "-rotate_z"}[axis]


def parse_extra_rotations(raw_values: list[list[str]] | None) -> dict[str, list[tuple[str, str]]]:
    rotations: dict[str, list[tuple[str, str]]] = {}
    for raw in raw_values or []:
        view, axis, degrees = raw
        if view not in VIEW_CHOICES:
            raise SystemExit(f"Unsupported view for --extra-rotate: {view}")
        if axis not in {"x", "y", "z"}:
            raise SystemExit(f"Unsupported axis for --extra-rotate: {axis}")
        try:
            float(degrees)
        except ValueError as exc:
            raise SystemExit(f"Invalid angle for --extra-rotate: {degrees}") from exc
        rotations.setdefault(view, []).append((rotate_command(axis), degrees))
    return rotations


def inverse_rotations(rotations: list[tuple[str, str]]) -> list[tuple[str, str]]:
    inverse: list[tuple[str, str]] = []
    for command, degrees in reversed(rotations):
        if degrees.startswith("-"):
            inverse.append((command, degrees[1:]))
        else:
            inverse.append((command, "-" + degrees))
    return inverse


def append_rotations(command: list[str], rotations: list[tuple[str, str]]) -> None:
    for rotate_cmd, angle in rotations:
        command.extend([rotate_cmd, angle, "-flush"])


def windows_path(path: Path) -> str:
    result = subprocess.run(
        ["wslpath", "-w", str(path.resolve())],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def cmd_arg(text: str) -> str:
    if any(ch.isspace() for ch in text):
        return '"' + text.replace('"', '\\"') + '"'
    return text


def vesta_command(vesta_dir: Path, args: list[str]) -> str:
    return "cd /d %s && VESTA.exe %s" % (
        cmd_arg(windows_path(vesta_dir)),
        " ".join(args),
    )


def run_windows_vesta(vesta_dir: Path, args: list[str], timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    command = vesta_command(vesta_dir, args)
    return subprocess.run(
        ["timeout", str(timeout_seconds) + "s", "/mnt/c/WINDOWS/system32/cmd.exe", "/C", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def cleanup_workspace_vesta() -> None:
    powershell = Path("/mnt/c/WINDOWS/system32/WindowsPowerShell/v1.0/powershell.exe")
    if not powershell.exists():
        return
    root_win = windows_path(Path(__file__).resolve().parents[2])
    pattern = "*" + root_win.rstrip("\\") + "*"
    script = (
        "Get-CimInstance Win32_Process | "
        "Where-Object { $_.Name -eq 'VESTA.exe' -and "
        "$_.CommandLine -like '" + pattern.replace("'", "''") + "' } | "
        "ForEach-Object { Stop-Process -Id $_.ProcessId -Force "
        "-ErrorAction SilentlyContinue }"
    )
    subprocess.run([str(powershell), "-NoProfile", "-Command", script], check=False)


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


def prepare_render_input(source: Path, out_dir: Path, stem: str, comps: str) -> Path:
    text = source.read_text(encoding="utf-8", errors="replace")
    copy_relative_cubes(text, source.parent, out_dir)
    patched = patch_comps(text, comps)
    if patched == text and source.parent.resolve() == out_dir.resolve():
        return source
    render_input = out_dir / f"{stem}_render_input.vesta"
    render_input.write_text(patched, encoding="utf-8")
    return render_input


def export_with_cli_rotation(args: argparse.Namespace) -> list[Path]:
    source = Path(args.input_vesta)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = args.stem or source.stem
    render_input = prepare_render_input(source, out_dir, stem, args.comps)
    sequence = selected_sequence(args.initial_view, args.views)
    wanted_views = set(args.views)
    output_paths = {
        view: out_dir / f"{stem}_{view}{args.render_suffix}"
        for view, _ in sequence
        if view in wanted_views
    }
    extra_rotations = parse_extra_rotations(args.extra_rotate)

    command: list[str] = ["-open", cmd_arg(windows_path(render_input))]
    for view, rotations in sequence:
        append_rotations(command, rotations)
        if view not in output_paths:
            continue
        view_extra = extra_rotations.get(view, [])
        append_rotations(command, view_extra)
        command.extend(["-export_img", f"scale={args.scale}", cmd_arg(windows_path(output_paths[view])), "-flush"])
        append_rotations(command, inverse_rotations(view_extra))
    command.append("-close")

    if args.clean_before:
        cleanup_workspace_vesta()
    result = run_windows_vesta(Path(args.vesta_dir), command, args.timeout)
    if args.clean_after:
        cleanup_workspace_vesta()

    missing = [path for path in output_paths.values() if not path.exists()]
    if missing:
        print(result.stdout[-4000:])
        raise SystemExit("VESTA did not produce: " + ", ".join(str(path) for path in missing))

    for view, path in ordered_paths(output_paths):
        if args.add_compass:
            add_compass(path, view, None)
        print(path)
    return [path for _, path in ordered_paths(output_paths)]


def export_scene_copies(args: argparse.Namespace) -> list[Path]:
    source = Path(args.input_vesta)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8", errors="replace")
    copy_relative_cubes(text, source.parent, out_dir)
    text = patch_comps(text, args.comps)
    stem = args.stem or source.stem
    outputs: list[Path] = []

    for view in args.views:
        view_path = out_dir / f"{stem}_{view}.vesta"
        view_path.write_text(replace_scene(text, SCENES[view]), encoding="utf-8")
        outputs.append(view_path)
        print(view_path)
        if args.render_command:
            png_path = out_dir / f"{stem}_{view}{args.render_suffix}"
            command = args.render_command.format(input=view_path, output=png_path, view=view)
            subprocess.run(command, shell=True, check=True)
            if args.add_compass:
                add_compass(png_path, view, None)
            outputs.append(png_path)
            print(png_path)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_vesta")
    parser.add_argument("output_dir")
    parser.add_argument("--stem", help="Output filename stem. Default: input stem")
    parser.add_argument("--views", nargs="+", choices=VIEW_CHOICES, default=["front", "right", "top"])
    parser.add_argument(
        "--initial-view",
        choices=INITIAL_VIEW_CHOICES,
        default="front",
        help="View represented by the input file's current camera before CLI rotations.",
    )
    parser.add_argument("--comps", choices=["off", "on", "keep"], default="off")
    parser.add_argument("--scale", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--vesta-dir", default="tools/VESTA-win64")
    parser.add_argument("--render-suffix", default=".png")
    parser.add_argument("--add-compass", action="store_true", help="Add one compass after rendering")
    parser.add_argument("--clean-before", action="store_true")
    parser.add_argument("--clean-after", action="store_true", default=True)
    parser.add_argument("--no-clean-after", action="store_false", dest="clean_after")
    parser.add_argument(
        "--extra-rotate",
        action="append",
        nargs=3,
        metavar=("VIEW", "AXIS", "DEGREES"),
        help=(
            "Apply a temporary per-view rotation before export, then undo it. "
            "Example: --extra-rotate top x -8"
        ),
    )
    parser.add_argument(
        "--mode",
        choices=["cli-rotate", "scene-copies"],
        default="cli-rotate",
        help="Default opens one source once and uses VESTA -rotate_* before each export.",
    )
    parser.add_argument(
        "--render-command",
        help=(
            "Compatibility mode only: shell command template using {input}, {output}, and {view}. "
            "Example: 'python3 project/scripts/render_vesta_nofocus.py {input} {output}'"
        ),
    )
    args = parser.parse_args()

    if args.mode == "scene-copies":
        export_scene_copies(args)
    else:
        if args.render_command:
            raise SystemExit("--render-command is only valid with --mode scene-copies")
        export_with_cli_rotation(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
