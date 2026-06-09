"""Reusable AIM+IGMH VESTA overlay workflow.

The high-level workflow starts from a VESTA file that already contains the
periodic structure/IGMH cube phase and an imported AIM path/critical-point
phase.  It applies the maintained AIM display style, copies relative cube
dependencies beside the product, writes a markdown recipe manifest, and can
optionally call the existing one-session VESTA three-view renderer.
"""

from __future__ import annotations

import argparse
import datetime as _datetime
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, NamedTuple, Optional, Sequence, Tuple

from .vesta_aim_overlay_style import (
    DEFAULT_BCP_ELEMENT,
    DEFAULT_BCP_RADIUS,
    DEFAULT_BCP_RGB,
    DEFAULT_PATH_ELEMENT,
    DEFAULT_PATH_RADIUS,
    DEFAULT_PATH_RGB,
    patch_aim_overlay_style_text,
)


DEFAULT_EXTRA_ROTATIONS: Tuple[Tuple[str, str, str], ...] = (("top", "x", "-8"),)
DEFAULT_RENDER_VIEWS: Tuple[str, ...] = ("front", "right", "top")


class CubeReference(NamedTuple):
    kind: str
    raw_path: str
    source_path: Path
    destination_path: Optional[Path]
    is_relative: bool
    exists: bool
    copied: bool


class WorkflowResult(NamedTuple):
    styled_vesta: Path
    manifest: Optional[Path]
    cube_references: List[CubeReference]
    render_command: Optional[List[str]]


def _project_dir() -> Path:
    return Path(__file__).resolve().parents[2]


def _workspace_root() -> Path:
    return _project_dir().parent


def _is_windows_absolute(path_text: str) -> bool:
    return (
        len(path_text) >= 3
        and path_text[1] == ":"
        and path_text[2] in {"/", "\\"}
    ) or path_text.startswith("\\\\")


def _is_absolute_path(path_text: str) -> bool:
    return Path(path_text).is_absolute() or _is_windows_absolute(path_text)


def _safe_relative_destination(raw_path: str, output_dir: Path) -> Path:
    relative = Path(raw_path)
    if any(part == ".." for part in relative.parts):
        return output_dir / relative.name
    return output_dir / relative


def collect_cube_references(text: str, source_dir: Path, output_dir: Path) -> List[CubeReference]:
    """Collect VESTA density/texture cube references from `.vesta` text."""

    refs: List[CubeReference] = []
    lines = text.splitlines()
    for idx, line in enumerate(lines[:-1]):
        fields = line.strip().split()
        if not fields or fields[0] not in {"IMPORT_DENSITY", "IMPORT_TEXTURE"}:
            continue
        next_fields = lines[idx + 1].strip().split()
        if len(next_fields) < 2:
            continue
        raw_path = next_fields[-1].strip('"')
        is_relative = not _is_absolute_path(raw_path)
        source_path = source_dir / raw_path if is_relative else Path(raw_path)
        destination = _safe_relative_destination(raw_path, output_dir) if is_relative else None
        refs.append(
            CubeReference(
                kind=fields[0],
                raw_path=raw_path,
                source_path=source_path,
                destination_path=destination,
                is_relative=is_relative,
                exists=source_path.exists(),
                copied=False,
            )
        )
    return refs


def copy_relative_cubes(
    text: str,
    source_dir: Path,
    output_dir: Path,
    *,
    enabled: bool = True,
) -> List[CubeReference]:
    """Copy relative cube references beside the generated VESTA file."""

    refs = []
    for ref in collect_cube_references(text, source_dir, output_dir):
        copied = False
        if enabled and ref.is_relative and ref.exists and ref.destination_path is not None:
            if ref.source_path.resolve() != ref.destination_path.resolve():
                ref.destination_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ref.source_path, ref.destination_path)
                copied = True
        refs.append(ref._replace(copied=copied))
    return refs


def _rgb_tuple(values: Sequence[int]) -> Tuple[int, int, int]:
    if len(values) != 3:
        raise ValueError("RGB options require exactly three integers")
    return int(values[0]), int(values[1]), int(values[2])


def _format_rgb(rgb: Tuple[int, int, int]) -> str:
    return "%d %d %d" % rgb


def _format_command(command: Sequence[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in command)


def compass_to_comps(compass: str, explicit_comps: Optional[str]) -> str:
    if explicit_comps:
        return explicit_comps
    return {
        "post": "off",
        "none": "off",
        "native": "on",
        "keep": "keep",
    }[compass]


def build_three_view_command(
    styled_vesta: Path,
    output_dir: Path,
    *,
    stem: str,
    views: Sequence[str] = DEFAULT_RENDER_VIEWS,
    initial_view: str = "top",
    extra_rotate: Sequence[Tuple[str, str, str]] = DEFAULT_EXTRA_ROTATIONS,
    compass: str = "post",
    comps: Optional[str] = None,
    scale: int = 2,
    timeout: int = 240,
    vesta_dir: str = "tools/VESTA-win64",
    render_suffix: str = ".png",
    clean_before: bool = False,
    clean_after: bool = True,
    mode: str = "cli-rotate",
) -> List[str]:
    """Build the script command for the maintained one-session renderer."""

    script = _project_dir() / "scripts" / "vesta_three_views.py"
    command = [
        sys.executable,
        str(script),
        str(styled_vesta),
        str(output_dir),
        "--stem",
        stem,
        "--views",
    ]
    command.extend(str(view) for view in views)
    command.extend(
        [
            "--initial-view",
            initial_view,
            "--comps",
            compass_to_comps(compass, comps),
            "--scale",
            str(scale),
            "--timeout",
            str(timeout),
            "--vesta-dir",
            vesta_dir,
            "--render-suffix",
            render_suffix,
            "--mode",
            mode,
        ]
    )
    for view, axis, degrees in extra_rotate:
        command.extend(["--extra-rotate", view, axis, str(degrees)])
    if compass == "post":
        command.append("--add-compass")
    if clean_before:
        command.append("--clean-before")
    if clean_after:
        command.append("--clean-after")
    else:
        command.append("--no-clean-after")
    return command


def render_manifest_text(
    *,
    input_vesta: Path,
    styled_vesta: Path,
    output_dir: Path,
    style_options: dict,
    cube_references: Sequence[CubeReference],
    render_command: Optional[Sequence[str]],
    render_requested: bool,
    generated_at: Optional[str] = None,
) -> str:
    generated_at = generated_at or _datetime.datetime.now().isoformat(timespec="seconds")
    lines = [
        "# AIM+IGMH VESTA Recipe",
        "",
        "## Generated",
        "",
        "- time: `%s`" % generated_at,
        "- input_vesta: `%s`" % input_vesta,
        "- output_dir: `%s`" % output_dir,
        "- styled_vesta: `%s`" % styled_vesta,
        "",
        "## AIM Overlay Style",
        "",
        "- path_element: `%s`" % style_options["path_element"],
        "- path_radius: `%.4f`" % style_options["path_radius"],
        "- path_rgb: `%s`" % _format_rgb(style_options["path_rgb"]),
        "- bcp_element: `%s`" % style_options["bcp_element"],
        "- bcp_radius: `%.4f`" % style_options["bcp_radius"],
        "- bcp_rgb: `%s`" % _format_rgb(style_options["bcp_rgb"]),
        "- clear_aim_sbond: `%s`" % style_options["clear_aim_sbond"],
        "- keep_structure_bonds: `%s`" % style_options["keep_structure_bonds"],
        "- split_bcp_phase: `%s`" % style_options["split_bcp_phase"],
        "- label_bcp_sites: `%s`" % style_options["label_bcp_sites"],
        "- bcp_label_prefix: `%s`" % style_options["bcp_label_prefix"],
        "- label_mode: `%s`" % style_options["label_mode"],
        "- label_font_size: `%s`" % style_options["label_font_size"],
        "- label_offset: `%s`" % style_options["label_offset"],
        "- label_mark: `%s`" % style_options["label_mark"],
        "",
        "## Cube Dependencies",
        "",
    ]
    if cube_references:
        lines.append("| kind | raw path | source exists | copied | destination |")
        lines.append("| --- | --- | --- | --- | --- |")
        for ref in cube_references:
            lines.append(
                "| `%s` | `%s` | `%s` | `%s` | `%s` |"
                % (
                    ref.kind,
                    ref.raw_path,
                    ref.exists,
                    ref.copied,
                    ref.destination_path or "",
                )
            )
    else:
        lines.append("- No `IMPORT_DENSITY` or `IMPORT_TEXTURE` cube references found.")

    lines.extend(
        [
            "",
            "## Rendering",
            "",
            "- render_requested: `%s`" % render_requested,
        ]
    )
    if render_command:
        lines.extend(["", "```bash", _format_command(render_command), "```"])
    else:
        lines.append("- render_command: not generated")

    lines.extend(
        [
            "",
            "## Workflow Notes",
            "",
            "- AIM path samples are preserved; the workflow does not delete points that overlap BCPs.",
            "- AIM and BCP coordinates are not moved; remaining visibility problems should be solved by camera/style.",
            "- Structure bonds are kept by default, while AIM-phase `SBOND` is cleared by default.",
            "- The maintained three-view render path opens one `.vesta` once and uses VESTA CLI rotations.",
        ]
    )
    return "\n".join(lines) + "\n"


def run_workflow(
    input_vesta: Path,
    output_dir: Path,
    *,
    stem: Optional[str] = None,
    output_vesta: Optional[Path] = None,
    manifest: Optional[Path] = None,
    write_manifest: bool = True,
    copy_cubes: bool = True,
    strict_cubes: bool = False,
    path_element: str = DEFAULT_PATH_ELEMENT,
    bcp_element: str = DEFAULT_BCP_ELEMENT,
    path_radius: float = DEFAULT_PATH_RADIUS,
    bcp_radius: float = DEFAULT_BCP_RADIUS,
    path_rgb: Tuple[int, int, int] = DEFAULT_PATH_RGB,
    bcp_rgb: Tuple[int, int, int] = DEFAULT_BCP_RGB,
    clear_aim_sbond: bool = True,
    keep_structure_bonds: bool = True,
    split_bcp_phase: bool = True,
    label_bcp_sites: bool = False,
    bcp_label_prefix: str = "BCP",
    label_mode: int = 1,
    label_font_size: float = 12,
    label_offset: float = 1.000,
    label_mark: int = 0,
    render_three_views: bool = False,
    views: Sequence[str] = DEFAULT_RENDER_VIEWS,
    initial_view: str = "top",
    extra_rotate: Sequence[Tuple[str, str, str]] = DEFAULT_EXTRA_ROTATIONS,
    compass: str = "post",
    comps: Optional[str] = None,
    scale: int = 2,
    timeout: int = 240,
    vesta_dir: str = "tools/VESTA-win64",
    render_suffix: str = ".png",
    clean_before: bool = False,
    clean_after: bool = True,
    mode: str = "cli-rotate",
) -> WorkflowResult:
    input_vesta = Path(input_vesta)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = stem or input_vesta.stem
    styled_vesta = Path(output_vesta) if output_vesta else output_dir / f"{stem}_styled.vesta"

    source_text = input_vesta.read_text(encoding="utf-8", errors="replace")
    style_options = {
        "path_element": path_element,
        "bcp_element": bcp_element,
        "path_radius": path_radius,
        "bcp_radius": bcp_radius,
        "path_rgb": path_rgb,
        "bcp_rgb": bcp_rgb,
        "clear_aim_sbond": clear_aim_sbond,
        "keep_structure_bonds": keep_structure_bonds,
        "split_bcp_phase": split_bcp_phase,
        "label_bcp_sites": label_bcp_sites,
        "bcp_label_prefix": bcp_label_prefix,
        "label_mode": label_mode,
        "label_font_size": label_font_size,
        "label_offset": label_offset,
        "label_mark": label_mark,
    }
    patched = patch_aim_overlay_style_text(source_text, **style_options)
    styled_vesta.parent.mkdir(parents=True, exist_ok=True)
    styled_vesta.write_text(patched, encoding="utf-8")

    cube_refs = copy_relative_cubes(source_text, input_vesta.parent, styled_vesta.parent, enabled=copy_cubes)
    missing_relative = [ref.raw_path for ref in cube_refs if ref.is_relative and not ref.exists]
    if strict_cubes and missing_relative:
        raise FileNotFoundError("Missing relative cube references: " + ", ".join(missing_relative))

    render_command = None
    if render_three_views:
        render_command = build_three_view_command(
            styled_vesta,
            output_dir,
            stem=stem,
            views=views,
            initial_view=initial_view,
            extra_rotate=extra_rotate,
            compass=compass,
            comps=comps,
            scale=scale,
            timeout=timeout,
            vesta_dir=vesta_dir,
            render_suffix=render_suffix,
            clean_before=clean_before,
            clean_after=clean_after,
            mode=mode,
        )
        subprocess.run(render_command, check=True, cwd=str(_workspace_root()))

    manifest_path = Path(manifest) if manifest else output_dir / f"{stem}_aim_igmh_recipe.md"
    if write_manifest:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            render_manifest_text(
                input_vesta=input_vesta,
                styled_vesta=styled_vesta,
                output_dir=output_dir,
                style_options=style_options,
                cube_references=cube_refs,
                render_command=render_command,
                render_requested=render_three_views,
            ),
            encoding="utf-8",
        )
    else:
        manifest_path = None

    return WorkflowResult(
        styled_vesta=styled_vesta,
        manifest=manifest_path,
        cube_references=cube_refs,
        render_command=render_command,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Apply the maintained AIM+IGMH VESTA overlay style and optionally export three views."
    )
    parser.add_argument("input_vesta", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--stem", help="Output filename stem. Default: input stem")
    parser.add_argument("--output-vesta", type=Path, help="Styled VESTA output path")
    parser.add_argument("--manifest", type=Path, help="Markdown recipe path")
    parser.add_argument("--no-manifest", action="store_true")
    parser.add_argument("--no-copy-cubes", action="store_true")
    parser.add_argument("--strict-cubes", action="store_true", help="Fail if a referenced relative cube is missing")
    parser.add_argument("--path-element", default=DEFAULT_PATH_ELEMENT)
    parser.add_argument("--bcp-element", default=DEFAULT_BCP_ELEMENT)
    parser.add_argument("--path-radius", type=float, default=DEFAULT_PATH_RADIUS)
    parser.add_argument("--bcp-radius", type=float, default=DEFAULT_BCP_RADIUS)
    parser.add_argument("--path-rgb", nargs=3, type=int, default=DEFAULT_PATH_RGB)
    parser.add_argument("--bcp-rgb", nargs=3, type=int, default=DEFAULT_BCP_RGB)
    parser.add_argument("--keep-aim-sbond", action="store_true")
    parser.add_argument("--structure-bonds-off", action="store_true")
    parser.add_argument("--no-split-bcp-phase", action="store_true")
    parser.add_argument("--label-bcp-sites", action="store_true")
    parser.add_argument("--bcp-label-prefix", default="BCP")
    parser.add_argument("--label-mode", type=int, default=1)
    parser.add_argument("--label-font-size", type=float, default=12)
    parser.add_argument("--label-offset", type=float, default=1.000)
    parser.add_argument("--label-mark", type=int, default=0)
    parser.add_argument("--render-three-views", "--render", action="store_true")
    parser.add_argument("--views", nargs="+", default=list(DEFAULT_RENDER_VIEWS))
    parser.add_argument("--initial-view", choices=["front", "top"], default="top")
    parser.add_argument(
        "--extra-rotate",
        action="append",
        nargs=3,
        metavar=("VIEW", "AXIS", "DEGREES"),
        help="Extra temporary camera rotation passed to the three-view renderer",
    )
    parser.add_argument(
        "--no-default-top-tilt",
        action="store_true",
        help="Do not add the current Ag interface default `--extra-rotate top x -8`",
    )
    parser.add_argument("--compass", choices=["post", "none", "native", "keep"], default="post")
    parser.add_argument("--comps", choices=["off", "on", "keep"], help="Override renderer COMPS mode")
    parser.add_argument("--scale", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--vesta-dir", default="tools/VESTA-win64")
    parser.add_argument("--render-suffix", default=".png")
    parser.add_argument("--clean-before", action="store_true")
    parser.add_argument("--no-clean-after", action="store_true")
    parser.add_argument(
        "--mode",
        choices=["cli-rotate", "scene-copies"],
        default="cli-rotate",
        help="Keep the default `cli-rotate` for one-source/one-session three-view rendering.",
    )
    args = parser.parse_args(argv)

    extra_rotate: List[Tuple[str, str, str]] = []
    if not args.no_default_top_tilt:
        extra_rotate.extend(DEFAULT_EXTRA_ROTATIONS)
    if args.extra_rotate:
        extra_rotate.extend((view, axis, degrees) for view, axis, degrees in args.extra_rotate)

    result = run_workflow(
        args.input_vesta,
        args.output_dir,
        stem=args.stem,
        output_vesta=args.output_vesta,
        manifest=args.manifest,
        write_manifest=not args.no_manifest,
        copy_cubes=not args.no_copy_cubes,
        strict_cubes=args.strict_cubes,
        path_element=args.path_element,
        bcp_element=args.bcp_element,
        path_radius=args.path_radius,
        bcp_radius=args.bcp_radius,
        path_rgb=_rgb_tuple(args.path_rgb),
        bcp_rgb=_rgb_tuple(args.bcp_rgb),
        clear_aim_sbond=not args.keep_aim_sbond,
        keep_structure_bonds=not args.structure_bonds_off,
        split_bcp_phase=not args.no_split_bcp_phase,
        label_bcp_sites=args.label_bcp_sites,
        bcp_label_prefix=args.bcp_label_prefix,
        label_mode=args.label_mode,
        label_font_size=args.label_font_size,
        label_offset=args.label_offset,
        label_mark=args.label_mark,
        render_three_views=args.render_three_views,
        views=args.views,
        initial_view=args.initial_view,
        extra_rotate=extra_rotate,
        compass=args.compass,
        comps=args.comps,
        scale=args.scale,
        timeout=args.timeout,
        vesta_dir=args.vesta_dir,
        render_suffix=args.render_suffix,
        clean_before=args.clean_before,
        clean_after=not args.no_clean_after,
        mode=args.mode,
    )
    print(result.styled_vesta)
    if result.manifest:
        print(result.manifest)
    if result.render_command:
        print(_format_command(result.render_command))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
