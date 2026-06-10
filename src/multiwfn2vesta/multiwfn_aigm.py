"""Run Multiwfn aIGM/amIGM trajectory-average cube generation."""

from __future__ import annotations

import argparse
import datetime as _datetime
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, NamedTuple, Optional, Sequence, Tuple

from .cube_preset import run_preset
from .cube_vesta import CubeVestaResult
from .executables import ExecutableCandidate, find_multiwfn
from .multiwfn_aim import read_command_file


AIGM_OUTPUT_MISSING_CODE = 3
AIGM_PROCESSING_FAILED_CODE = 4

AIGM_METHOD_MENU = {
    "aigm": "12",
    "amigm": "-12",
}

AIGM_METHOD_ALIASES = {
    "aigm": "aigm",
    "average-igm": "aigm",
    "averaged-igm": "aigm",
    "avg-igm": "aigm",
    "amigm": "amigm",
    "average-migm": "amigm",
    "averaged-migm": "amigm",
    "avg-migm": "amigm",
}


PERIODIC_POINTS_ERROR = (
    "--grid-mode points is unsafe for periodic trajectories: Multiwfn's PBC "
    "grid option 4 reads a spacing value instead of NX,NY,NZ. Use "
    "--grid-mode spacing --grid-spacing VALUE or --grid-mode pbc-cell."
)


class MultiwfnAigmResult(NamedTuple):
    multiwfn: ExecutableCandidate
    trajectory: Path
    output_dir: Path
    raw_dir: Path
    fragments: Tuple[str, ...]
    frame_range: Optional[Tuple[int, int]]
    returncode: int
    cli_returncode: int
    success: bool
    command_file: Path
    stdout_log: Path
    stderr_log: Path
    recipe_path: Path
    raw_avgdg_inter_cube: Path
    raw_avgsl2r_cube: Path
    avgdg_inter_cube: Optional[Path]
    avgsl2r_cube: Optional[Path]
    avgRDG_cube: Optional[Path]
    thermflu_cube: Optional[Path]
    output_txt: Optional[Path]
    vesta_result: Optional[CubeVestaResult]
    tfi_vesta_result: Optional[CubeVestaResult]
    error: Optional[str]


def _command_text(commands: Sequence[str]) -> str:
    return "\n".join(commands) + "\n"


def _run_environment(candidate: ExecutableCandidate) -> dict:
    env = dict(os.environ)
    env["Multiwfnpath"] = str(candidate.path.parent)
    env["MULTIWFNPATH"] = str(candidate.path.parent)
    env["MultiwfnPATH"] = str(candidate.path.parent)
    return env


def _timeout_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _copy_or_move(source: Path, destination: Path, *, move: bool = False) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination.unlink()
    if move:
        shutil.move(str(source), str(destination))
    else:
        shutil.copy2(source, destination)


def _format_int_triple(values: Sequence[int]) -> str:
    if len(values) != 3:
        raise ValueError("Expected three grid point counts")
    return "{},{},{}".format(int(values[0]), int(values[1]), int(values[2]))


def _format_float_triple(values: Optional[Sequence[float]]) -> str:
    if values is None:
        return ""
    if len(values) != 3:
        raise ValueError("Expected three values")
    return "{},{},{}".format(float(values[0]), float(values[1]), float(values[2]))


def _append_error(current: Optional[str], new: str) -> str:
    if not current:
        return new
    return current + " | " + new


def trajectory_looks_periodic(path: Path) -> bool:
    """Lightly detect common trajectory cell markers before building a PBC grid stream."""
    try:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")[:131072].lower()
    except OSError:
        return False
    return any(marker in text for marker in ("lattice=", " pbc=", "\npbc=", "cryst1"))


def _check_periodic_grid_mode(periodic: bool, grid_mode: str) -> None:
    if periodic and grid_mode.lower() == "points":
        raise ValueError(PERIODIC_POINTS_ERROR)


def normalize_aigm_method(method: str) -> str:
    key = str(method).strip().lower()
    if key not in AIGM_METHOD_ALIASES:
        raise ValueError("Unknown averaged IGM method: {}".format(method))
    return AIGM_METHOD_ALIASES[key]


def normalize_frame_range(frame_range: Optional[Sequence[int]]) -> Optional[Tuple[int, int]]:
    if frame_range is None:
        return None
    if len(frame_range) != 2:
        raise ValueError("--frame-range requires START END")
    start, end = int(frame_range[0]), int(frame_range[1])
    if start < 1:
        raise ValueError("Frame index starts from 1")
    if end < start:
        raise ValueError("--frame-range END must be greater than or equal to START")
    return start, end


def build_aigm_commands(
    fragments: Sequence[str],
    *,
    method: str = "aigm",
    frame_range: Optional[Sequence[int]] = None,
    periodic: bool = False,
    grid_mode: str = "points",
    grid_points: Sequence[int] = (40, 40, 40),
    grid_spacing: Optional[float] = None,
    grid_cube: Optional[Path] = None,
    grid_extension: Optional[float] = None,
    pbc_origin: Optional[Sequence[float]] = None,
    pbc_lengths: Optional[Sequence[float]] = None,
    export_rdg: bool = False,
    export_tfi: bool = False,
    export_scatter: bool = False,
) -> List[str]:
    method_key = normalize_aigm_method(method)
    frame_tuple = normalize_frame_range(frame_range)
    fragment_list = [str(fragment).strip() for fragment in fragments if str(fragment).strip()]
    if len(fragment_list) < 2:
        raise ValueError("aIGM/amIGM runner requires at least two --fragment entries")

    commands: List[str] = ["20", AIGM_METHOD_MENU[method_key], str(len(fragment_list))]
    commands.extend(fragment_list)
    commands.append("" if frame_tuple is None else "{},{}".format(frame_tuple[0], frame_tuple[1]))

    mode = grid_mode.lower()
    _check_periodic_grid_mode(periodic, mode)
    if grid_extension is not None and mode in {"low", "medium", "high", "points", "spacing", "cube"}:
        commands.extend(["-10", str(float(grid_extension))])

    if mode == "low":
        commands.append("1")
    elif mode == "medium":
        commands.append("2")
    elif mode == "high":
        commands.append("3")
    elif mode == "points":
        commands.extend(["4", _format_int_triple(grid_points)])
    elif mode == "spacing":
        if grid_spacing is None:
            raise ValueError("--grid-spacing is required when --grid-mode spacing is used")
        commands.extend(["4", str(float(grid_spacing))])
    elif mode == "cube":
        if grid_cube is None:
            raise ValueError("--grid-cube is required when --grid-mode cube is used")
        commands.extend(["8", str(Path(grid_cube).expanduser().resolve())])
    elif mode == "pbc-cell":
        commands.append("9")
        commands.append(_format_float_triple(pbc_origin))
        commands.append(_format_float_triple(pbc_lengths))
        commands.append("" if grid_spacing is None else str(float(grid_spacing)))
    else:
        raise ValueError("Unknown grid mode: {}".format(grid_mode))

    if export_scatter:
        commands.append("2")
    commands.append("3")
    if export_rdg:
        commands.append("4")
    if export_tfi:
        commands.append("5")
    commands.extend(["0", "0", "q"])
    return commands


def _write_recipe(
    path: Path,
    *,
    trajectory: Path,
    raw_dir: Path,
    method: str,
    fragments: Sequence[str],
    frame_range: Optional[Tuple[int, int]],
    commands: Sequence[str],
    grid_mode: str,
    periodic: bool,
    grid_points: Sequence[int],
    grid_spacing: Optional[float],
    grid_cube: Optional[Path],
    avgdg_inter_cube: Optional[Path],
    avgsl2r_cube: Optional[Path],
    avgRDG_cube: Optional[Path],
    thermflu_cube: Optional[Path],
    output_txt: Optional[Path],
    vesta_result: Optional[CubeVestaResult],
    tfi_vesta_result: Optional[CubeVestaResult],
    error: Optional[str],
) -> None:
    frame_text = "all" if frame_range is None else "{} to {}".format(frame_range[0], frame_range[1])
    lines = [
        "# Multiwfn aIGM/amIGM Recipe",
        "",
        "## Generated",
        "",
        f"- time: `{_datetime.datetime.now().isoformat(timespec='seconds')}`",
        f"- trajectory: `{trajectory}`",
        f"- raw_dir: `{raw_dir}`",
        f"- method: `{method}`",
        f"- fragments: `{'; '.join(fragments)}`",
        f"- frame_range: `{frame_text}`",
        f"- grid_mode: `{grid_mode}`",
        f"- periodic: `{periodic}`",
        f"- grid_points: `{_format_int_triple(grid_points)}`",
        f"- grid_spacing: `{grid_spacing}`",
        f"- grid_cube: `{grid_cube}`",
        "",
        "## Multiwfn Command Stream",
        "",
        "```text",
        *_command_text(commands).rstrip().splitlines(),
        "```",
        "",
        "## Outputs",
        "",
        f"- avgdg_inter_cube: `{avgdg_inter_cube}`",
        f"- avgsl2r_cube: `{avgsl2r_cube}`",
        f"- avgRDG_cube: `{avgRDG_cube}`",
        f"- thermflu_cube: `{thermflu_cube}`",
        f"- output_txt: `{output_txt}`",
        f"- vesta_file: `{vesta_result.vesta_path if vesta_result is not None else None}`",
        f"- tfi_vesta_file: `{tfi_vesta_result.vesta_path if tfi_vesta_result is not None else None}`",
    ]
    if vesta_result is not None and vesta_result.manifest_path is not None:
        lines.append(f"- vesta_recipe: `{vesta_result.manifest_path}`")
    if tfi_vesta_result is not None and tfi_vesta_result.manifest_path is not None:
        lines.append(f"- tfi_vesta_recipe: `{tfi_vesta_result.manifest_path}`")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Multiwfn aIGM/amIGM is a trajectory-average weak-interaction workflow.",
            "- The maintained VESTA surface uses `avgdg_inter.cub` colored by `avgsl2r.cub`.",
            "- `thermflu.cub` is only exported when TFI output was explicitly requested.",
        ]
    )
    if error:
        lines.extend(["", "## Error", "", f"- `{error}`"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_multiwfn_aigm(
    trajectory: Path,
    output_dir: Path,
    *,
    method: str = "aigm",
    fragments: Optional[Sequence[str]] = None,
    frame_range: Optional[Sequence[int]] = None,
    multiwfn_path: Optional[str] = None,
    commands: Optional[Sequence[str]] = None,
    commands_file: Optional[Path] = None,
    timeout: Optional[int] = None,
    nthreads: Optional[int] = None,
    stem: Optional[str] = None,
    raw_dir: Optional[Path] = None,
    periodic: Optional[bool] = None,
    grid_mode: str = "points",
    grid_points: Sequence[int] = (40, 40, 40),
    grid_spacing: Optional[float] = None,
    grid_cube: Optional[Path] = None,
    grid_extension: Optional[float] = None,
    pbc_origin: Optional[Sequence[float]] = None,
    pbc_lengths: Optional[Sequence[float]] = None,
    export_rdg: bool = False,
    export_tfi: bool = False,
    export_scatter: bool = False,
    make_vesta: bool = True,
    make_tfi_vesta: bool = False,
    vesta_output_dir: Optional[Path] = None,
    preset: Optional[str] = None,
    tfi_preset: Optional[str] = None,
    isosurface: Optional[float] = None,
    tex_physical: Optional[Tuple[float, float]] = None,
    tfi_tex_physical: Optional[Tuple[float, float]] = None,
    structure: Optional[str] = None,
    boundary: Optional[Sequence[float]] = None,
    copy_cubes: bool = True,
) -> MultiwfnAigmResult:
    method_key = normalize_aigm_method(method)
    frame_tuple = normalize_frame_range(frame_range)
    effective_preset = preset or "aigm"
    effective_tfi_preset = tfi_preset or "aigm-tfi"
    if make_tfi_vesta and not export_tfi:
        raise ValueError("--tfi-vesta requires --export-tfi")
    if make_tfi_vesta and not make_vesta:
        raise ValueError("--tfi-vesta cannot be combined with --no-vesta")

    candidate = find_multiwfn(multiwfn_path)
    if candidate is None:
        raise FileNotFoundError(
            "Cannot find Multiwfn. Set MULTIWFN_PATH/MULTIWFNPATH/MultiwfnPATH "
            "or add Multiwfn/Multiwfn_noGUI to PATH."
        )

    trajectory = Path(trajectory).expanduser().resolve()
    if not trajectory.exists():
        raise FileNotFoundError("Trajectory file not found: {}".format(trajectory))
    effective_periodic = trajectory_looks_periodic(trajectory) if periodic is None else bool(periodic)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if raw_dir is None:
        raw_dir = output_dir / f"multiwfn_{method_key}_raw"
    else:
        raw_dir = Path(raw_dir)
        if not raw_dir.is_absolute():
            raw_dir = output_dir / raw_dir
    raw_dir.mkdir(parents=True, exist_ok=True)

    fragment_tuple = tuple(str(fragment).strip() for fragment in (fragments or ()) if str(fragment).strip())
    if commands_file is not None:
        command_list = read_command_file(commands_file)
    elif commands is not None:
        command_list = list(commands)
    else:
        command_list = build_aigm_commands(
            fragment_tuple,
            method=method_key,
            frame_range=frame_tuple,
            periodic=effective_periodic,
            grid_mode=grid_mode,
            grid_points=grid_points,
            grid_spacing=grid_spacing,
            grid_cube=grid_cube,
            grid_extension=grid_extension,
            pbc_origin=pbc_origin,
            pbc_lengths=pbc_lengths,
            export_rdg=export_rdg,
            export_tfi=export_tfi,
            export_scatter=export_scatter,
        )

    output_stem = stem or trajectory.stem
    run_prefix = f"multiwfn_{method_key}"
    command_file = output_dir / f"{run_prefix}_input.txt"
    stdout_log = output_dir / f"{run_prefix}.stdout.txt"
    stderr_log = output_dir / f"{run_prefix}.stderr.txt"
    recipe_path = output_dir / f"{run_prefix}_recipe.md"
    command_file.write_text(_command_text(command_list), encoding="utf-8")

    raw_avgdg_inter = raw_dir / "avgdg_inter.cub"
    raw_avgsl2r = raw_dir / "avgsl2r.cub"
    raw_avgRDG = raw_dir / "avgRDG.cub"
    raw_thermflu = raw_dir / "thermflu.cub"
    raw_output_txt = raw_dir / "output.txt"
    for stale in (raw_avgdg_inter, raw_avgsl2r, raw_avgRDG, raw_thermflu, raw_output_txt):
        if stale.exists():
            stale.unlink()

    command = [str(candidate.path), str(trajectory)]
    if nthreads is not None and nthreads > 1:
        command.extend(["-nt", str(nthreads)])

    try:
        completed = subprocess.run(
            command,
            input=_command_text(command_list),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(raw_dir),
            env=_run_environment(candidate),
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        stdout_text = _timeout_text(getattr(exc, "stdout", None) or getattr(exc, "output", None))
        stderr_text = _timeout_text(getattr(exc, "stderr", None))
        error = f"Multiwfn {method_key} run timed out after {timeout} seconds; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text(stdout_text, encoding="utf-8")
        stderr_log.write_text((stderr_text + "\n" if stderr_text else "") + error + "\n", encoding="utf-8")
        _write_recipe(
            recipe_path,
            trajectory=trajectory,
            raw_dir=raw_dir,
            method=method_key,
            fragments=fragment_tuple,
            frame_range=frame_tuple,
            commands=command_list,
            grid_mode=grid_mode,
            periodic=effective_periodic,
            grid_points=grid_points,
            grid_spacing=grid_spacing,
            grid_cube=grid_cube,
            avgdg_inter_cube=None,
            avgsl2r_cube=None,
            avgRDG_cube=None,
            thermflu_cube=None,
            output_txt=None,
            vesta_result=None,
            tfi_vesta_result=None,
            error=error,
        )
        return MultiwfnAigmResult(
            candidate,
            trajectory,
            output_dir,
            raw_dir,
            fragment_tuple,
            frame_tuple,
            AIGM_PROCESSING_FAILED_CODE,
            AIGM_PROCESSING_FAILED_CODE,
            False,
            command_file,
            stdout_log,
            stderr_log,
            recipe_path,
            raw_avgdg_inter,
            raw_avgsl2r,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            error,
        )
    except OSError as exc:
        error = f"Failed to launch Multiwfn {method_key} run: {exc}; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text("", encoding="utf-8")
        stderr_log.write_text(error + "\n", encoding="utf-8")
        _write_recipe(
            recipe_path,
            trajectory=trajectory,
            raw_dir=raw_dir,
            method=method_key,
            fragments=fragment_tuple,
            frame_range=frame_tuple,
            commands=command_list,
            grid_mode=grid_mode,
            periodic=effective_periodic,
            grid_points=grid_points,
            grid_spacing=grid_spacing,
            grid_cube=grid_cube,
            avgdg_inter_cube=None,
            avgsl2r_cube=None,
            avgRDG_cube=None,
            thermflu_cube=None,
            output_txt=None,
            vesta_result=None,
            tfi_vesta_result=None,
            error=error,
        )
        return MultiwfnAigmResult(
            candidate,
            trajectory,
            output_dir,
            raw_dir,
            fragment_tuple,
            frame_tuple,
            AIGM_PROCESSING_FAILED_CODE,
            AIGM_PROCESSING_FAILED_CODE,
            False,
            command_file,
            stdout_log,
            stderr_log,
            recipe_path,
            raw_avgdg_inter,
            raw_avgsl2r,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            error,
        )

    stdout_log.write_text(completed.stdout or "", encoding="utf-8")
    stderr_log.write_text(completed.stderr or "", encoding="utf-8")

    error = None
    cli_returncode = completed.returncode
    avgdg_inter_cube: Optional[Path] = None
    avgsl2r_cube: Optional[Path] = None
    avgRDG_cube: Optional[Path] = None
    thermflu_cube: Optional[Path] = None
    output_txt: Optional[Path] = None
    vesta_result: Optional[CubeVestaResult] = None
    tfi_vesta_result: Optional[CubeVestaResult] = None

    required_missing = []
    if completed.returncode != 0:
        error = "Multiwfn failed with return code {}; inspect {} and {}".format(
            completed.returncode, stdout_log, stderr_log
        )
    else:
        required_missing = [str(path) for path in (raw_avgdg_inter, raw_avgsl2r) if not path.exists()]
        if required_missing:
            error = "Multiwfn finished with return code 0, but required {} cube output is missing: {}".format(
                method_key,
                ", ".join(required_missing),
            )
            cli_returncode = AIGM_OUTPUT_MISSING_CODE

    if completed.returncode == 0 and not required_missing:
        try:
            avgdg_inter_cube = output_dir / f"{output_stem}_avgdg_inter.cub"
            avgsl2r_cube = output_dir / f"{output_stem}_avgsl2r.cub"
            _copy_or_move(raw_avgdg_inter, avgdg_inter_cube)
            _copy_or_move(raw_avgsl2r, avgsl2r_cube)
            optional_missing = []
            if export_rdg:
                if raw_avgRDG.exists():
                    avgRDG_cube = output_dir / f"{output_stem}_avgRDG.cub"
                    _copy_or_move(raw_avgRDG, avgRDG_cube)
                else:
                    optional_missing.append(str(raw_avgRDG))
            if export_tfi:
                if raw_thermflu.exists():
                    thermflu_cube = output_dir / f"{output_stem}_thermflu.cub"
                    _copy_or_move(raw_thermflu, thermflu_cube)
                else:
                    optional_missing.append(str(raw_thermflu))
            if export_scatter:
                if raw_output_txt.exists():
                    output_txt = output_dir / f"{output_stem}_{run_prefix}_output.txt"
                    _copy_or_move(raw_output_txt, output_txt)
                else:
                    optional_missing.append(str(raw_output_txt))
            if optional_missing:
                error = _append_error(
                    error,
                    "Multiwfn finished with return code 0, but requested optional output is missing: {}".format(
                        ", ".join(optional_missing)
                    ),
                )
                cli_returncode = AIGM_OUTPUT_MISSING_CODE
        except Exception as exc:
            error = _append_error(error, "Failed to process Multiwfn {} cubes: {}".format(method_key, exc))
            cli_returncode = AIGM_PROCESSING_FAILED_CODE
            avgdg_inter_cube = None
            avgsl2r_cube = None
            avgRDG_cube = None
            thermflu_cube = None
            output_txt = None

    if completed.returncode == 0 and avgdg_inter_cube is not None and avgsl2r_cube is not None and make_vesta:
        try:
            vesta_result = run_preset(
                effective_preset,
                avgdg_inter_cube,
                Path(vesta_output_dir) if vesta_output_dir is not None else output_dir,
                texture_cube=avgsl2r_cube,
                stem=f"{output_stem}_{method_key}",
                title=f"{avgdg_inter_cube.stem} ({method_key})",
                isosurface=isosurface,
                tex_physical=tex_physical,
                structure=structure,
                boundary=boundary,
                copy_cubes=copy_cubes,
            )
        except Exception as exc:
            error = _append_error(error, "Failed to generate VESTA file from Multiwfn {} cubes: {}".format(method_key, exc))
            cli_returncode = AIGM_PROCESSING_FAILED_CODE
            vesta_result = None

    if (
        completed.returncode == 0
        and make_vesta
        and make_tfi_vesta
        and avgdg_inter_cube is not None
        and thermflu_cube is not None
    ):
        try:
            tfi_vesta_result = run_preset(
                effective_tfi_preset,
                avgdg_inter_cube,
                Path(vesta_output_dir) if vesta_output_dir is not None else output_dir,
                texture_cube=thermflu_cube,
                stem=f"{output_stem}_{method_key}_tfi",
                title=f"{avgdg_inter_cube.stem} ({method_key} TFI)",
                isosurface=isosurface,
                tex_physical=tfi_tex_physical,
                structure=structure,
                boundary=boundary,
                copy_cubes=copy_cubes,
            )
        except Exception as exc:
            error = _append_error(error, "Failed to generate TFI VESTA file from Multiwfn {} cubes: {}".format(method_key, exc))
            cli_returncode = AIGM_PROCESSING_FAILED_CODE
            tfi_vesta_result = None

    _write_recipe(
        recipe_path,
        trajectory=trajectory,
        raw_dir=raw_dir,
        method=method_key,
        fragments=fragment_tuple,
        frame_range=frame_tuple,
        commands=command_list,
        grid_mode=grid_mode,
        periodic=effective_periodic,
        grid_points=grid_points,
        grid_spacing=grid_spacing,
        grid_cube=grid_cube,
        avgdg_inter_cube=avgdg_inter_cube,
        avgsl2r_cube=avgsl2r_cube,
        avgRDG_cube=avgRDG_cube,
        thermflu_cube=thermflu_cube,
        output_txt=output_txt,
        vesta_result=vesta_result,
        tfi_vesta_result=tfi_vesta_result,
        error=error,
    )

    return MultiwfnAigmResult(
        multiwfn=candidate,
        trajectory=trajectory,
        output_dir=output_dir,
        raw_dir=raw_dir,
        fragments=fragment_tuple,
        frame_range=frame_tuple,
        returncode=completed.returncode,
        cli_returncode=cli_returncode,
        success=cli_returncode == 0,
        command_file=command_file,
        stdout_log=stdout_log,
        stderr_log=stderr_log,
        recipe_path=recipe_path,
        raw_avgdg_inter_cube=raw_avgdg_inter,
        raw_avgsl2r_cube=raw_avgsl2r,
        avgdg_inter_cube=avgdg_inter_cube,
        avgsl2r_cube=avgsl2r_cube,
        avgRDG_cube=avgRDG_cube,
        thermflu_cube=thermflu_cube,
        output_txt=output_txt,
        vesta_result=vesta_result,
        tfi_vesta_result=tfi_vesta_result,
        error=error,
    )


def _float_pair(values: Optional[Sequence[float]]) -> Optional[Tuple[float, float]]:
    if values is None:
        return None
    if len(values) != 2:
        raise ValueError("Expected exactly two values")
    return float(values[0]), float(values[1])


def _has_method_override(args: Sequence[str]) -> bool:
    return any(arg == "--method" or arg.startswith("--method=") for arg in args)


def main(
    argv: Optional[Sequence[str]] = None,
    *,
    program_name: str = "aigm-run",
    fixed_method: Optional[str] = None,
) -> int:
    method_default = normalize_aigm_method(fixed_method) if fixed_method is not None else "aigm"
    parser = argparse.ArgumentParser(
        prog=program_name,
        description="Run Multiwfn aIGM or amIGM trajectory-average cube generation and optionally prepare VESTA.",
        epilog=(
            "Default command stream: main function 20, method option 12/-12, fragments, frame range, "
            "grid selection, post-processing option 3 to export avgdg_inter.cub and avgsl2r.cub, "
            "then cube-preset aigm unless --no-vesta is used."
        ),
    )
    parser.add_argument("trajectory", type=Path, help="Trajectory file accepted by Multiwfn, typically XYZ trajectory")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--fragment", action="append", help="Atom indices for one fragment, e.g. 1-48 or c; repeat")
    if fixed_method is None:
        parser.add_argument("--method", choices=["aigm", "amigm"], default=method_default, help="Averaged IGM method to run")
    else:
        parser.set_defaults(method=method_default)
    parser.add_argument("--frame-range", nargs=2, type=int, metavar=("START", "END"), help="Frame range; omit for all frames")
    parser.add_argument("--multiwfn", "--multiwfn-path", dest="multiwfn_path")
    parser.add_argument("--commands-file", type=Path, help="Override the generated Multiwfn aIGM/amIGM command stream")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--nthreads", type=int)
    parser.add_argument("--stem")
    parser.add_argument("--raw-dir", type=Path)
    periodic_group = parser.add_mutually_exclusive_group()
    periodic_group.add_argument(
        "--periodic",
        dest="periodic",
        action="store_true",
        help="Treat the trajectory as periodic and reject grid modes unsafe for Multiwfn PBC prompts.",
    )
    periodic_group.add_argument(
        "--nonperiodic",
        dest="periodic",
        action="store_false",
        help="Treat the trajectory as non-periodic even if common cell markers are present.",
    )
    parser.set_defaults(periodic=None)
    parser.add_argument(
        "--grid-mode",
        choices=["low", "medium", "high", "points", "spacing", "cube", "pbc-cell"],
        default="points",
        help="Grid selection mode passed to Multiwfn setgrid. Periodic trajectories need spacing or pbc-cell.",
    )
    parser.add_argument("--grid-points", nargs=3, type=int, default=(40, 40, 40), metavar=("NX", "NY", "NZ"))
    parser.add_argument("--grid-spacing", type=float)
    parser.add_argument("--grid-cube", type=Path)
    parser.add_argument("--grid-extension", type=float)
    parser.add_argument("--pbc-origin", nargs=3, type=float, metavar=("X", "Y", "Z"))
    parser.add_argument("--pbc-lengths", nargs=3, type=float, metavar=("LX", "LY", "LZ"))
    parser.add_argument("--export-rdg", action="store_true", help="Also export avgRDG.cub from the post-processing menu")
    parser.add_argument("--export-tfi", action="store_true", help="Also compute/export thermflu.cub")
    parser.add_argument("--export-scatter", action="store_true", help="Also export output.txt scatter data")
    parser.add_argument("--no-vesta", action="store_true")
    parser.add_argument("--tfi-vesta", action="store_true", help="When --export-tfi is used, also write a TFI-colored VESTA file")
    parser.add_argument("--vesta-output-dir", type=Path)
    parser.add_argument("--preset", help="Cube preset for VESTA output; default is aigm")
    parser.add_argument("--tfi-preset", help="Cube preset for --tfi-vesta; default is aigm-tfi")
    parser.add_argument("--isosurface", type=float)
    parser.add_argument("--tex-physical", nargs=2, type=float, metavar=("MIN", "MAX"))
    parser.add_argument("--tfi-tex-physical", nargs=2, type=float, metavar=("MIN", "MAX"))
    parser.add_argument("--structure", choices=["auto", "none", "molecule", "crystal"])
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--no-copy-cubes", action="store_true")
    args = parser.parse_args(argv)

    try:
        tex_physical = _float_pair(args.tex_physical)
        tfi_tex_physical = _float_pair(args.tfi_tex_physical)
        result = run_multiwfn_aigm(
            args.trajectory,
            args.output_dir,
            method=args.method,
            fragments=args.fragment,
            frame_range=args.frame_range,
            multiwfn_path=args.multiwfn_path,
            commands_file=args.commands_file,
            timeout=args.timeout,
            nthreads=args.nthreads,
            stem=args.stem,
            raw_dir=args.raw_dir,
            periodic=args.periodic,
            grid_mode=args.grid_mode,
            grid_points=args.grid_points,
            grid_spacing=args.grid_spacing,
            grid_cube=args.grid_cube,
            grid_extension=args.grid_extension,
            pbc_origin=args.pbc_origin,
            pbc_lengths=args.pbc_lengths,
            export_rdg=args.export_rdg,
            export_tfi=args.export_tfi,
            export_scatter=args.export_scatter,
            make_vesta=not args.no_vesta,
            make_tfi_vesta=args.tfi_vesta,
            vesta_output_dir=args.vesta_output_dir,
            preset=args.preset,
            tfi_preset=args.tfi_preset,
            isosurface=args.isosurface,
            tex_physical=tex_physical,
            tfi_tex_physical=tfi_tex_physical,
            structure=args.structure,
            boundary=args.boundary,
            copy_cubes=not args.no_copy_cubes,
        )
    except (FileNotFoundError, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"{program_name}: {exc}", file=sys.stderr)
        return 2

    print("Multiwfn: {}".format(result.multiwfn.path))
    print("method: {}".format(normalize_aigm_method(args.method)))
    print("returncode: {}".format(result.returncode))
    if result.cli_returncode != result.returncode:
        print("cli_returncode: {}".format(result.cli_returncode))
    print(result.command_file)
    print(result.stdout_log)
    print(result.stderr_log)
    print(result.raw_dir)
    print(result.recipe_path)
    for path in (result.avgdg_inter_cube, result.avgsl2r_cube, result.avgRDG_cube, result.thermflu_cube, result.output_txt):
        if path is not None and path.exists():
            print(path)
    if result.vesta_result is not None:
        print(result.vesta_result.vesta_path)
        if result.vesta_result.manifest_path is not None:
            print(result.vesta_result.manifest_path)
    if result.tfi_vesta_result is not None:
        print(result.tfi_vesta_result.vesta_path)
        if result.tfi_vesta_result.manifest_path is not None:
            print(result.tfi_vesta_result.manifest_path)
    if result.error:
        print("ERROR: {}".format(result.error), file=sys.stderr)
    return result.cli_returncode


def main_fixed_method(method: str, argv: Optional[Sequence[str]] = None, *, program_name: Optional[str] = None) -> int:
    method_key = normalize_aigm_method(method)
    label = program_name or f"{method_key}-run"
    args = list(sys.argv[1:] if argv is None else argv)
    if _has_method_override(args):
        print(
            f"{label}: --method is fixed by this command; use aigm-run --method {method_key} "
            "or another explicit averaged method when you need the generic runner.",
            file=sys.stderr,
        )
        return 2
    return main(args, program_name=label, fixed_method=method_key)


def main_aigm(argv: Optional[Sequence[str]] = None) -> int:
    return main_fixed_method("aigm", argv, program_name="aigm-run")


def main_amigm(argv: Optional[Sequence[str]] = None) -> int:
    return main_fixed_method("amigm", argv, program_name="amigm-run")


if __name__ == "__main__":
    raise SystemExit(main())
