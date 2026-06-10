"""Run Multiwfn IGMH cube generation and prepare VESTA files."""

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


IGMH_OUTPUT_MISSING_CODE = 3
IGMH_PROCESSING_FAILED_CODE = 4


class MultiwfnIgmhResult(NamedTuple):
    multiwfn: ExecutableCandidate
    wavefunction: Path
    output_dir: Path
    raw_dir: Path
    fragments: Tuple[str, ...]
    returncode: int
    cli_returncode: int
    success: bool
    command_file: Path
    stdout_log: Path
    stderr_log: Path
    recipe_path: Path
    raw_dg_inter_cube: Path
    raw_sl2r_cube: Path
    dg_inter_cube: Optional[Path]
    sl2r_cube: Optional[Path]
    dg_intra_cube: Optional[Path]
    dg_cube: Optional[Path]
    output_txt: Optional[Path]
    vesta_result: Optional[CubeVestaResult]
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


def wavefunction_has_molden_cell(path: Path, *, max_lines: int = 2000) -> bool:
    """Return True when a text wavefunction looks like a periodic Molden file."""
    try:
        with Path(path).open("r", encoding="utf-8", errors="ignore") as handle:
            for line_number, line in enumerate(handle):
                if line_number >= max_lines:
                    break
                if line.strip().lower() == "[cell]":
                    return True
    except OSError:
        return False
    return False


def build_igmh_commands(
    fragments: Sequence[str],
    *,
    grid_mode: str = "points",
    grid_points: Sequence[int] = (40, 40, 40),
    grid_spacing: Optional[float] = None,
    grid_cube: Optional[Path] = None,
    grid_extension: Optional[float] = None,
    pbc_origin: Optional[Sequence[float]] = None,
    pbc_lengths: Optional[Sequence[float]] = None,
    periodic: bool = False,
) -> List[str]:
    fragment_list = [str(fragment).strip() for fragment in fragments if str(fragment).strip()]
    if len(fragment_list) < 2:
        raise ValueError("IGMH runner requires at least two --fragment entries for interfragment analysis")

    commands: List[str] = ["20", "11", str(len(fragment_list))]
    commands.extend(fragment_list)

    mode = grid_mode.lower()
    if periodic and mode == "points":
        raise ValueError(
            "--grid-mode points is unsafe for periodic Molden/[Cell] inputs: "
            "Multiwfn's PBC grid option 4 reads a spacing value instead of NX,NY,NZ. "
            "Use --grid-mode spacing --grid-spacing VALUE or --grid-mode pbc-cell."
        )
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
        raise ValueError(f"Unknown grid mode: {grid_mode}")

    commands.extend(["3", "0", "0", "q"])
    return commands


def _write_recipe(
    path: Path,
    *,
    wavefunction: Path,
    raw_dir: Path,
    fragments: Sequence[str],
    commands: Sequence[str],
    grid_mode: str,
    grid_points: Sequence[int],
    grid_spacing: Optional[float],
    grid_cube: Optional[Path],
    dg_inter_cube: Optional[Path],
    sl2r_cube: Optional[Path],
    dg_intra_cube: Optional[Path],
    dg_cube: Optional[Path],
    vesta_result: Optional[CubeVestaResult],
    error: Optional[str],
) -> None:
    lines = [
        "# Multiwfn IGMH Recipe",
        "",
        "## Generated",
        "",
        f"- time: `{_datetime.datetime.now().isoformat(timespec='seconds')}`",
        f"- wavefunction: `{wavefunction}`",
        f"- raw_dir: `{raw_dir}`",
        f"- fragments: `{'; '.join(fragments)}`",
        f"- grid_mode: `{grid_mode}`",
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
        f"- dg_inter_cube: `{dg_inter_cube}`",
        f"- sl2r_cube: `{sl2r_cube}`",
        f"- dg_intra_cube: `{dg_intra_cube}`",
        f"- dg_cube: `{dg_cube}`",
        f"- vesta_file: `{vesta_result.vesta_path if vesta_result is not None else None}`",
    ]
    if vesta_result is not None and vesta_result.manifest_path is not None:
        lines.append(f"- vesta_recipe: `{vesta_result.manifest_path}`")
    if error:
        lines.extend(["", "## Error", "", f"- `{error}`"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_multiwfn_igmh(
    wavefunction: Path,
    output_dir: Path,
    *,
    fragments: Optional[Sequence[str]] = None,
    multiwfn_path: Optional[str] = None,
    commands: Optional[Sequence[str]] = None,
    commands_file: Optional[Path] = None,
    timeout: Optional[int] = None,
    nthreads: Optional[int] = None,
    stem: Optional[str] = None,
    raw_dir: Optional[Path] = None,
    grid_mode: str = "points",
    grid_points: Sequence[int] = (40, 40, 40),
    grid_spacing: Optional[float] = None,
    grid_cube: Optional[Path] = None,
    grid_extension: Optional[float] = None,
    pbc_origin: Optional[Sequence[float]] = None,
    pbc_lengths: Optional[Sequence[float]] = None,
    make_vesta: bool = True,
    vesta_output_dir: Optional[Path] = None,
    preset: str = "igmh",
    isosurface: Optional[float] = None,
    tex_physical: Optional[Tuple[float, float]] = None,
    structure: Optional[str] = None,
    boundary: Optional[Sequence[float]] = None,
    copy_cubes: bool = True,
) -> MultiwfnIgmhResult:
    candidate = find_multiwfn(multiwfn_path)
    if candidate is None:
        raise FileNotFoundError(
            "Cannot find Multiwfn. Set MULTIWFN_PATH/MULTIWFNPATH/MultiwfnPATH "
            "or add Multiwfn/Multiwfn_noGUI to PATH."
        )

    wavefunction = Path(wavefunction).expanduser().resolve()
    if not wavefunction.exists():
        raise FileNotFoundError("Wavefunction file not found: {}".format(wavefunction))

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if raw_dir is None:
        raw_dir = output_dir / "multiwfn_igmh_raw"
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
        command_list = build_igmh_commands(
            fragment_tuple,
            grid_mode=grid_mode,
            grid_points=grid_points,
            grid_spacing=grid_spacing,
            grid_cube=grid_cube,
            grid_extension=grid_extension,
            pbc_origin=pbc_origin,
            pbc_lengths=pbc_lengths,
            periodic=wavefunction_has_molden_cell(wavefunction),
        )

    output_stem = stem or wavefunction.stem
    command_file = output_dir / "multiwfn_igmh_input.txt"
    stdout_log = output_dir / "multiwfn_igmh.stdout.txt"
    stderr_log = output_dir / "multiwfn_igmh.stderr.txt"
    recipe_path = output_dir / "multiwfn_igmh_recipe.md"
    command_file.write_text(_command_text(command_list), encoding="utf-8")

    raw_dg_inter = raw_dir / "dg_inter.cub"
    raw_sl2r = raw_dir / "sl2r.cub"
    raw_dg_intra = raw_dir / "dg_intra.cub"
    raw_dg = raw_dir / "dg.cub"
    raw_output_txt = raw_dir / "output.txt"
    for stale in (raw_dg_inter, raw_sl2r, raw_dg_intra, raw_dg, raw_output_txt):
        if stale.exists():
            stale.unlink()

    command = [str(candidate.path), str(wavefunction)]
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
        error = f"Multiwfn IGMH run timed out after {timeout} seconds; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text(stdout_text, encoding="utf-8")
        stderr_log.write_text((stderr_text + "\n" if stderr_text else "") + error + "\n", encoding="utf-8")
        _write_recipe(
            recipe_path,
            wavefunction=wavefunction,
            raw_dir=raw_dir,
            fragments=fragment_tuple,
            commands=command_list,
            grid_mode=grid_mode,
            grid_points=grid_points,
            grid_spacing=grid_spacing,
            grid_cube=grid_cube,
            dg_inter_cube=None,
            sl2r_cube=None,
            dg_intra_cube=None,
            dg_cube=None,
            vesta_result=None,
            error=error,
        )
        return MultiwfnIgmhResult(
            candidate,
            wavefunction,
            output_dir,
            raw_dir,
            fragment_tuple,
            IGMH_PROCESSING_FAILED_CODE,
            IGMH_PROCESSING_FAILED_CODE,
            False,
            command_file,
            stdout_log,
            stderr_log,
            recipe_path,
            raw_dg_inter,
            raw_sl2r,
            None,
            None,
            None,
            None,
            None,
            None,
            error,
        )
    except OSError as exc:
        error = f"Failed to launch Multiwfn IGMH run: {exc}; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text("", encoding="utf-8")
        stderr_log.write_text(error + "\n", encoding="utf-8")
        _write_recipe(
            recipe_path,
            wavefunction=wavefunction,
            raw_dir=raw_dir,
            fragments=fragment_tuple,
            commands=command_list,
            grid_mode=grid_mode,
            grid_points=grid_points,
            grid_spacing=grid_spacing,
            grid_cube=grid_cube,
            dg_inter_cube=None,
            sl2r_cube=None,
            dg_intra_cube=None,
            dg_cube=None,
            vesta_result=None,
            error=error,
        )
        return MultiwfnIgmhResult(
            candidate,
            wavefunction,
            output_dir,
            raw_dir,
            fragment_tuple,
            IGMH_PROCESSING_FAILED_CODE,
            IGMH_PROCESSING_FAILED_CODE,
            False,
            command_file,
            stdout_log,
            stderr_log,
            recipe_path,
            raw_dg_inter,
            raw_sl2r,
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
    dg_inter_cube: Optional[Path] = None
    sl2r_cube: Optional[Path] = None
    dg_intra_cube: Optional[Path] = None
    dg_cube: Optional[Path] = None
    output_txt: Optional[Path] = None
    vesta_result: Optional[CubeVestaResult] = None

    if completed.returncode != 0:
        error = "Multiwfn failed with return code {}; inspect {} and {}".format(
            completed.returncode, stdout_log, stderr_log
        )
    else:
        missing = [str(path) for path in (raw_dg_inter, raw_sl2r) if not path.exists()]
        if missing:
            error = "Multiwfn finished with return code 0, but required IGMH cube output is missing: {}".format(
                ", ".join(missing)
            )
            cli_returncode = IGMH_OUTPUT_MISSING_CODE

    if completed.returncode == 0 and cli_returncode == 0:
        try:
            dg_inter_cube = output_dir / f"{output_stem}_dg_inter.cub"
            sl2r_cube = output_dir / f"{output_stem}_sl2r.cub"
            _copy_or_move(raw_dg_inter, dg_inter_cube)
            _copy_or_move(raw_sl2r, sl2r_cube)
            if raw_dg_intra.exists():
                dg_intra_cube = output_dir / f"{output_stem}_dg_intra.cub"
                _copy_or_move(raw_dg_intra, dg_intra_cube)
            if raw_dg.exists():
                dg_cube = output_dir / f"{output_stem}_dg.cub"
                _copy_or_move(raw_dg, dg_cube)
            if raw_output_txt.exists():
                output_txt = output_dir / f"{output_stem}_multiwfn_igmh_output.txt"
                _copy_or_move(raw_output_txt, output_txt)
        except Exception as exc:
            error = "Failed to process Multiwfn IGMH cubes: {}".format(exc)
            cli_returncode = IGMH_PROCESSING_FAILED_CODE
            dg_inter_cube = None
            sl2r_cube = None
            dg_intra_cube = None
            dg_cube = None
            output_txt = None

    if completed.returncode == 0 and cli_returncode == 0 and make_vesta and dg_inter_cube is not None and sl2r_cube is not None:
        try:
            vesta_result = run_preset(
                preset,
                dg_inter_cube,
                Path(vesta_output_dir) if vesta_output_dir is not None else output_dir,
                texture_cube=sl2r_cube,
                stem=f"{output_stem}_{preset}",
                isosurface=isosurface,
                tex_physical=tex_physical,
                structure=structure,
                boundary=boundary,
                copy_cubes=copy_cubes,
            )
        except Exception as exc:
            error = "Failed to generate VESTA file from IGMH cubes: {}".format(exc)
            cli_returncode = IGMH_PROCESSING_FAILED_CODE
            vesta_result = None

    _write_recipe(
        recipe_path,
        wavefunction=wavefunction,
        raw_dir=raw_dir,
        fragments=fragment_tuple,
        commands=command_list,
        grid_mode=grid_mode,
        grid_points=grid_points,
        grid_spacing=grid_spacing,
        grid_cube=grid_cube,
        dg_inter_cube=dg_inter_cube,
        sl2r_cube=sl2r_cube,
        dg_intra_cube=dg_intra_cube,
        dg_cube=dg_cube,
        vesta_result=vesta_result,
        error=error,
    )

    return MultiwfnIgmhResult(
        multiwfn=candidate,
        wavefunction=wavefunction,
        output_dir=output_dir,
        raw_dir=raw_dir,
        fragments=fragment_tuple,
        returncode=completed.returncode,
        cli_returncode=cli_returncode,
        success=cli_returncode == 0,
        command_file=command_file,
        stdout_log=stdout_log,
        stderr_log=stderr_log,
        recipe_path=recipe_path,
        raw_dg_inter_cube=raw_dg_inter,
        raw_sl2r_cube=raw_sl2r,
        dg_inter_cube=dg_inter_cube,
        sl2r_cube=sl2r_cube,
        dg_intra_cube=dg_intra_cube,
        dg_cube=dg_cube,
        output_txt=output_txt,
        vesta_result=vesta_result,
        error=error,
    )


def _float_pair(values: Optional[Sequence[float]]) -> Optional[Tuple[float, float]]:
    if values is None:
        return None
    if len(values) != 2:
        raise ValueError("Expected exactly two values")
    return float(values[0]), float(values[1])


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run Multiwfn IGMH cube generation and optionally prepare a VESTA mapped-surface file.",
        epilog=(
            "Default command stream: main function 20, IGMH option 11, user fragments, "
            "grid selection, post-processing option 3 to export sl2r.cub and dg_inter.cub, "
            "then cube-preset igmh unless --no-vesta is used."
        ),
    )
    parser.add_argument("wavefunction", type=Path, help="Wavefunction file accepted by Multiwfn, e.g. .molden/.fch/.wfn")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--fragment", action="append", help="Atom indices for one fragment, e.g. 1-48 or 49-60; repeat")
    parser.add_argument("--multiwfn", "--multiwfn-path", dest="multiwfn_path")
    parser.add_argument("--commands-file", type=Path, help="Override the generated Multiwfn IGMH command stream")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--nthreads", type=int)
    parser.add_argument("--stem")
    parser.add_argument("--raw-dir", type=Path)
    parser.add_argument(
        "--grid-mode",
        choices=["low", "medium", "high", "points", "spacing", "cube", "pbc-cell"],
        default="points",
        help="Grid selection mode. Default points is for finite non-PBC inputs; periodic [Cell] inputs need spacing or pbc-cell.",
    )
    parser.add_argument("--grid-points", nargs=3, type=int, default=(40, 40, 40), metavar=("NX", "NY", "NZ"))
    parser.add_argument("--grid-spacing", type=float)
    parser.add_argument("--grid-cube", type=Path)
    parser.add_argument("--grid-extension", type=float)
    parser.add_argument("--pbc-origin", nargs=3, type=float, metavar=("X", "Y", "Z"))
    parser.add_argument("--pbc-lengths", nargs=3, type=float, metavar=("LX", "LY", "LZ"))
    parser.add_argument("--no-vesta", action="store_true")
    parser.add_argument("--vesta-output-dir", type=Path)
    parser.add_argument("--preset", default="igmh", help="Cube preset name or alias for VESTA output, default: igmh")
    parser.add_argument("--isosurface", type=float)
    parser.add_argument("--tex-physical", nargs=2, type=float, metavar=("MIN", "MAX"))
    parser.add_argument("--structure", choices=["auto", "none", "molecule", "crystal"])
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--no-copy-cubes", action="store_true")
    args = parser.parse_args(argv)

    try:
        tex_physical = _float_pair(args.tex_physical)
        result = run_multiwfn_igmh(
            args.wavefunction,
            args.output_dir,
            fragments=args.fragment,
            multiwfn_path=args.multiwfn_path,
            commands_file=args.commands_file,
            timeout=args.timeout,
            nthreads=args.nthreads,
            stem=args.stem,
            raw_dir=args.raw_dir,
            grid_mode=args.grid_mode,
            grid_points=args.grid_points,
            grid_spacing=args.grid_spacing,
            grid_cube=args.grid_cube,
            grid_extension=args.grid_extension,
            pbc_origin=args.pbc_origin,
            pbc_lengths=args.pbc_lengths,
            make_vesta=not args.no_vesta,
            vesta_output_dir=args.vesta_output_dir,
            preset=args.preset,
            isosurface=args.isosurface,
            tex_physical=tex_physical,
            structure=args.structure,
            boundary=args.boundary,
            copy_cubes=not args.no_copy_cubes,
        )
    except (FileNotFoundError, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"igmh-run: {exc}", file=sys.stderr)
        return 2

    print("Multiwfn: {}".format(result.multiwfn.path))
    print("returncode: {}".format(result.returncode))
    if result.cli_returncode != result.returncode:
        print("cli_returncode: {}".format(result.cli_returncode))
    print(result.command_file)
    print(result.stdout_log)
    print(result.stderr_log)
    print(result.raw_dir)
    print(result.recipe_path)
    for path in (result.dg_inter_cube, result.sl2r_cube, result.dg_intra_cube, result.dg_cube, result.output_txt):
        if path is not None and path.exists():
            print(path)
    if result.vesta_result is not None:
        print(result.vesta_result.vesta_path)
        if result.vesta_result.manifest_path is not None:
            print(result.vesta_result.manifest_path)
    if result.error:
        print("ERROR: {}".format(result.error), file=sys.stderr)
    return result.cli_returncode


if __name__ == "__main__":
    raise SystemExit(main())
