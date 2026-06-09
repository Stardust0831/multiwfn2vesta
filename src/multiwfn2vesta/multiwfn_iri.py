"""Run Multiwfn IRI/RDG cube generation and prepare VESTA files."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, NamedTuple, Optional, Sequence, Tuple

from .cub import IRI_COLOR_LOWER, IRI_POSITIVE_SCALE, process_iri_color_cube
from .cube_preset import run_preset
from .cube_vesta import CubeVestaResult
from .executables import ExecutableCandidate, find_multiwfn
from .multiwfn_aim import read_command_file


IRI_OUTPUT_MISSING_CODE = 3
IRI_PROCESSING_FAILED_CODE = 4

DEFAULT_IRI_COMMANDS = [
    "20",
    "4",
    "4",
    "0.13",
    "3",
    "2",
    "0",
    "0",
    "q",
]


class MultiwfnIriResult(NamedTuple):
    multiwfn: ExecutableCandidate
    wavefunction: Path
    output_dir: Path
    raw_dir: Path
    returncode: int
    cli_returncode: int
    success: bool
    command_file: Path
    stdout_log: Path
    stderr_log: Path
    raw_color_cube: Path
    raw_surface_cube: Path
    color_cube: Optional[Path]
    surface_cube: Optional[Path]
    multiwfn_output_txt: Optional[Path]
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


def _copy_or_move(source: Path, destination: Path, *, move: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination.unlink()
    if move:
        shutil.move(str(source), str(destination))
    else:
        shutil.copy2(source, destination)


def run_multiwfn_iri(
    wavefunction: Path,
    output_dir: Path,
    *,
    multiwfn_path: Optional[str] = None,
    commands: Optional[Sequence[str]] = None,
    commands_file: Optional[Path] = None,
    timeout: Optional[int] = None,
    nthreads: Optional[int] = None,
    stem: Optional[str] = None,
    raw_dir: Optional[Path] = None,
    color_lower: float = IRI_COLOR_LOWER,
    color_upper: Optional[float] = None,
    color_positive_scale: float = IRI_POSITIVE_SCALE,
    strict_cube: bool = True,
    keep_raw_surface: bool = True,
    make_vesta: bool = True,
    vesta_output_dir: Optional[Path] = None,
    preset: str = "iri",
    isosurface: Optional[float] = None,
    tex_physical: Optional[Tuple[float, float]] = None,
    surface_band: Optional[float] = None,
    surface_nearest: int = 1024,
    structure: Optional[str] = None,
    boundary: Optional[Sequence[float]] = None,
    copy_cubes: bool = True,
) -> MultiwfnIriResult:
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
        raw_dir = output_dir / "multiwfn_iri_raw"
    else:
        raw_dir = Path(raw_dir)
        if not raw_dir.is_absolute():
            raw_dir = output_dir / raw_dir
    raw_dir.mkdir(parents=True, exist_ok=True)

    output_stem = stem or wavefunction.stem
    if commands_file is not None:
        command_list = read_command_file(commands_file)
    elif commands is not None:
        command_list = list(commands)
    else:
        command_list = list(DEFAULT_IRI_COMMANDS)

    command_file = output_dir / "multiwfn_iri_input.txt"
    stdout_log = output_dir / "multiwfn_iri.stdout.txt"
    stderr_log = output_dir / "multiwfn_iri.stderr.txt"
    command_file.write_text(_command_text(command_list), encoding="utf-8")

    raw_color_cube = raw_dir / "func1.cub"
    raw_surface_cube = raw_dir / "func2.cub"
    raw_output_txt = raw_dir / "output.txt"
    for stale in (raw_color_cube, raw_surface_cube, raw_output_txt):
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
        error = f"Multiwfn IRI run timed out after {timeout} seconds; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text(stdout_text, encoding="utf-8")
        stderr_log.write_text((stderr_text + "\n" if stderr_text else "") + error + "\n", encoding="utf-8")
        return MultiwfnIriResult(
            multiwfn=candidate,
            wavefunction=wavefunction,
            output_dir=output_dir,
            raw_dir=raw_dir,
            returncode=IRI_PROCESSING_FAILED_CODE,
            cli_returncode=IRI_PROCESSING_FAILED_CODE,
            success=False,
            command_file=command_file,
            stdout_log=stdout_log,
            stderr_log=stderr_log,
            raw_color_cube=raw_color_cube,
            raw_surface_cube=raw_surface_cube,
            color_cube=None,
            surface_cube=None,
            multiwfn_output_txt=None,
            vesta_result=None,
            error=error,
        )
    except OSError as exc:
        error = f"Failed to launch Multiwfn IRI run: {exc}; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text("", encoding="utf-8")
        stderr_log.write_text(error + "\n", encoding="utf-8")
        return MultiwfnIriResult(
            multiwfn=candidate,
            wavefunction=wavefunction,
            output_dir=output_dir,
            raw_dir=raw_dir,
            returncode=IRI_PROCESSING_FAILED_CODE,
            cli_returncode=IRI_PROCESSING_FAILED_CODE,
            success=False,
            command_file=command_file,
            stdout_log=stdout_log,
            stderr_log=stderr_log,
            raw_color_cube=raw_color_cube,
            raw_surface_cube=raw_surface_cube,
            color_cube=None,
            surface_cube=None,
            multiwfn_output_txt=None,
            vesta_result=None,
            error=error,
        )
    stdout_log.write_text(completed.stdout or "", encoding="utf-8")
    stderr_log.write_text(completed.stderr or "", encoding="utf-8")

    error = None
    cli_returncode = completed.returncode
    color_cube: Optional[Path] = None
    surface_cube: Optional[Path] = None
    multiwfn_output_txt: Optional[Path] = None
    vesta_result: Optional[CubeVestaResult] = None

    if completed.returncode != 0:
        error = "Multiwfn failed with return code {}; inspect {} and {}".format(
            completed.returncode, stdout_log, stderr_log
        )
    elif completed.returncode == 0:
        missing = [str(path) for path in (raw_color_cube, raw_surface_cube) if not path.exists()]
        if missing:
            error = "Multiwfn finished with return code 0, but required IRI cube output is missing: {}".format(
                ", ".join(missing)
            )
            cli_returncode = IRI_OUTPUT_MISSING_CODE

    if completed.returncode == 0 and cli_returncode == 0:
        try:
            color_cube = output_dir / f"{output_stem}_IRI1.cub"
            surface_cube = output_dir / f"{output_stem}_IRI2.cub"
            process_iri_color_cube(
                raw_color_cube,
                color_cube,
                lower=color_lower,
                upper=color_upper,
                positive_scale=color_positive_scale,
                strict=strict_cube,
            )
            _copy_or_move(raw_surface_cube, surface_cube, move=not keep_raw_surface)
            if raw_output_txt.exists():
                multiwfn_output_txt = output_dir / f"{output_stem}_multiwfn_iri_output.txt"
                _copy_or_move(raw_output_txt, multiwfn_output_txt, move=False)
        except Exception as exc:
            error = "Failed to process Multiwfn IRI cubes: {}".format(exc)
            cli_returncode = IRI_PROCESSING_FAILED_CODE
            color_cube = None
            surface_cube = None

    if completed.returncode == 0 and cli_returncode == 0 and make_vesta and surface_cube is not None and color_cube is not None:
        try:
            vesta_result = run_preset(
                preset,
                surface_cube,
                Path(vesta_output_dir) if vesta_output_dir is not None else output_dir,
                texture_cube=color_cube,
                stem=f"{output_stem}_{preset}",
                isosurface=isosurface,
                tex_physical=tex_physical,
                surface_band=surface_band,
                surface_nearest=surface_nearest,
                structure=structure,
                boundary=boundary,
                copy_cubes=copy_cubes,
            )
        except Exception as exc:
            error = "Failed to generate VESTA file from IRI cubes: {}".format(exc)
            cli_returncode = IRI_PROCESSING_FAILED_CODE
            vesta_result = None

    return MultiwfnIriResult(
        multiwfn=candidate,
        wavefunction=wavefunction,
        output_dir=output_dir,
        raw_dir=raw_dir,
        returncode=completed.returncode,
        cli_returncode=cli_returncode,
        success=cli_returncode == 0,
        command_file=command_file,
        stdout_log=stdout_log,
        stderr_log=stderr_log,
        raw_color_cube=raw_color_cube,
        raw_surface_cube=raw_surface_cube,
        color_cube=color_cube,
        surface_cube=surface_cube,
        multiwfn_output_txt=multiwfn_output_txt,
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
        description="Run Multiwfn IRI/RDG cube generation and optionally prepare a VESTA mapped-surface file.",
        epilog=(
            "Default outputs in output_dir: multiwfn_iri_input.txt, multiwfn_iri.stdout.txt, "
            "multiwfn_iri.stderr.txt, <stem>_IRI1.cub, <stem>_IRI2.cub, and a cube-preset "
            "VESTA file unless --no-vesta is used."
        ),
    )
    parser.add_argument("wavefunction", type=Path, help="Wavefunction file accepted by Multiwfn, e.g. .molden/.fch/.wfn")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--multiwfn", "--multiwfn-path", dest="multiwfn_path")
    parser.add_argument("--commands-file", type=Path, help="Override the default Multiwfn IRI command stream")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--nthreads", type=int)
    parser.add_argument("--stem")
    parser.add_argument("--raw-dir", type=Path)
    parser.add_argument("--color-lower", type=float, default=IRI_COLOR_LOWER)
    parser.add_argument("--color-upper", type=float)
    parser.add_argument("--color-positive-scale", type=float, default=IRI_POSITIVE_SCALE)
    parser.add_argument("--non-strict-cube", action="store_true")
    parser.add_argument("--move-raw-surface", action="store_true", help="Move func2.cub instead of copying it")
    parser.add_argument("--no-vesta", action="store_true")
    parser.add_argument("--vesta-output-dir", type=Path)
    parser.add_argument("--preset", default="iri", help="Cube preset name or alias for VESTA output, default: iri")
    parser.add_argument("--isosurface", type=float)
    parser.add_argument("--tex-physical", nargs=2, type=float, metavar=("MIN", "MAX"))
    parser.add_argument("--surface-band", type=float)
    parser.add_argument("--surface-nearest", type=int, default=1024)
    parser.add_argument("--structure", choices=["auto", "none", "molecule", "crystal"])
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--no-copy-cubes", action="store_true")
    args = parser.parse_args(argv)

    try:
        tex_physical = _float_pair(args.tex_physical)
        result = run_multiwfn_iri(
            args.wavefunction,
            args.output_dir,
            multiwfn_path=args.multiwfn_path,
            commands_file=args.commands_file,
            timeout=args.timeout,
            nthreads=args.nthreads,
            stem=args.stem,
            raw_dir=args.raw_dir,
            color_lower=args.color_lower,
            color_upper=args.color_upper,
            color_positive_scale=args.color_positive_scale,
            strict_cube=not args.non_strict_cube,
            keep_raw_surface=not args.move_raw_surface,
            make_vesta=not args.no_vesta,
            vesta_output_dir=args.vesta_output_dir,
            preset=args.preset,
            isosurface=args.isosurface,
            tex_physical=tex_physical,
            surface_band=args.surface_band,
            surface_nearest=args.surface_nearest,
            structure=args.structure,
            boundary=args.boundary,
            copy_cubes=not args.no_copy_cubes,
        )
    except (FileNotFoundError, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"iri-run: {exc}", file=sys.stderr)
        return 2

    print("Multiwfn: {}".format(result.multiwfn.path))
    print("returncode: {}".format(result.returncode))
    if result.cli_returncode != result.returncode:
        print("cli_returncode: {}".format(result.cli_returncode))
    print(result.command_file)
    print(result.stdout_log)
    print(result.stderr_log)
    print(result.raw_dir)
    if result.color_cube is not None and result.color_cube.exists():
        print(result.color_cube)
    if result.surface_cube is not None and result.surface_cube.exists():
        print(result.surface_cube)
    if result.multiwfn_output_txt is not None and result.multiwfn_output_txt.exists():
        print(result.multiwfn_output_txt)
    if result.vesta_result is not None:
        print(result.vesta_result.vesta_path)
        if result.vesta_result.manifest_path is not None:
            print(result.vesta_result.manifest_path)
    if result.error:
        print("ERROR: {}".format(result.error), file=sys.stderr)
    return result.cli_returncode


if __name__ == "__main__":
    raise SystemExit(main())
