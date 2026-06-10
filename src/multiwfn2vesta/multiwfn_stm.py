"""Run Multiwfn STM/LDOS cube generation and prepare VESTA files."""

from __future__ import annotations

import argparse
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


STM_OUTPUT_MISSING_CODE = 3
STM_PROCESSING_FAILED_CODE = 4


class MultiwfnStmResult(NamedTuple):
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
    raw_stm_cube: Path
    stm_cube: Optional[Path]
    recipe_path: Path
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


def _format_float_pair(values: Optional[Sequence[float]]) -> str:
    if values is None:
        return ""
    if len(values) != 2:
        raise ValueError("Expected two range values")
    return "{},{}".format(float(values[0]), float(values[1]))


def build_stm_commands(
    *,
    bias: Optional[float] = None,
    fermi: Optional[float] = None,
    grid_points: Sequence[int] = (80, 80, 40),
    x_range: Optional[Sequence[float]] = None,
    y_range: Optional[Sequence[float]] = None,
    z_range: Optional[Sequence[float]] = None,
    prepare_fermi_temperature: Optional[float] = None,
) -> List[str]:
    """Build the Multiwfn command stream for constant-current STM.cub export."""
    commands: List[str] = ["300"]
    if prepare_fermi_temperature is not None:
        commands.extend(["9", str(float(prepare_fermi_temperature)), "q"])

    commands.extend(["4", "1"])
    if bias is not None:
        commands.extend(["2", str(float(bias))])
    if fermi is not None:
        commands.extend(["3", str(float(fermi))])

    commands.extend(["4", _format_int_triple(grid_points)])
    if x_range is not None:
        commands.extend(["5", _format_float_pair(x_range)])
    if y_range is not None:
        commands.extend(["6", _format_float_pair(y_range)])
    if z_range is not None:
        commands.extend(["7", _format_float_pair(z_range)])

    commands.extend(["0", "2", "0", "-1", "0", "q"])
    return commands


def _write_recipe(
    path: Path,
    *,
    result: Optional[MultiwfnStmResult] = None,
    multiwfn: Optional[ExecutableCandidate] = None,
    wavefunction: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    raw_dir: Optional[Path] = None,
    command_file: Optional[Path] = None,
    raw_stm_cube: Optional[Path] = None,
    stm_cube: Optional[Path] = None,
    vesta_result: Optional[CubeVestaResult] = None,
    bias: Optional[float] = None,
    fermi: Optional[float] = None,
    grid_points: Sequence[int] = (80, 80, 40),
    x_range: Optional[Sequence[float]] = None,
    y_range: Optional[Sequence[float]] = None,
    z_range: Optional[Sequence[float]] = None,
    prepare_fermi_temperature: Optional[float] = None,
    commands: Optional[Sequence[str]] = None,
    error: Optional[str] = None,
) -> None:
    if result is not None:
        multiwfn = result.multiwfn
        wavefunction = result.wavefunction
        output_dir = result.output_dir
        raw_dir = result.raw_dir
        command_file = result.command_file
        raw_stm_cube = result.raw_stm_cube
        stm_cube = result.stm_cube
        vesta_result = result.vesta_result
        error = result.error

    lines = [
        "# Multiwfn STM/LDOS Run Recipe",
        "",
        f"- multiwfn: `{multiwfn.path if multiwfn is not None else None}`",
        f"- wavefunction: `{wavefunction}`",
        f"- output_dir: `{output_dir}`",
        f"- raw_dir: `{raw_dir}`",
        f"- command_file: `{command_file}`",
        f"- mode: `constant-current STM cube`",
        f"- bias_V: `{bias}`",
        f"- fermi_eV: `{fermi}`",
        f"- prepare_fermi_temperature_K: `{prepare_fermi_temperature}`",
        f"- grid_points: `{_format_int_triple(grid_points)}`",
        f"- x_range_Angstrom: `{_format_float_pair(x_range) if x_range is not None else None}`",
        f"- y_range_Angstrom: `{_format_float_pair(y_range) if y_range is not None else None}`",
        f"- z_range_Angstrom: `{_format_float_pair(z_range) if z_range is not None else None}`",
        f"- raw_stm_cube: `{raw_stm_cube}`",
        f"- processed_stm_cube: `{stm_cube}`",
        f"- vesta_file: `{vesta_result.vesta_path if vesta_result is not None else None}`",
        f"- vesta_recipe: `{vesta_result.manifest_path if vesta_result is not None else None}`",
        f"- error: `{error}`",
        "",
        "## Source Notes",
        "",
        "- Multiwfn main menu `300` enters `otherfunc3_main`; subfunction `4` is STM simulation.",
        "- STM mode defaults to constant-distance, so the maintained stream sends menu option `1` to switch to constant-current.",
        "- Constant-current post-processing menu option `2` exports the current grid as `STM.cub` in the working directory.",
        "- Multiwfn requires wavefunction inputs with GTF/GTO information for this function.",
    ]
    if commands is not None:
        lines.extend(
            [
                "",
                "## Multiwfn Command Stream",
                "",
                "```text",
                *_command_text(commands).rstrip().splitlines(),
                "```",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_multiwfn_stm(
    wavefunction: Path,
    output_dir: Path,
    *,
    bias: Optional[float] = None,
    fermi: Optional[float] = None,
    grid_points: Sequence[int] = (80, 80, 40),
    x_range: Optional[Sequence[float]] = None,
    y_range: Optional[Sequence[float]] = None,
    z_range: Optional[Sequence[float]] = None,
    prepare_fermi_temperature: Optional[float] = None,
    multiwfn_path: Optional[str] = None,
    commands: Optional[Sequence[str]] = None,
    commands_file: Optional[Path] = None,
    timeout: Optional[int] = None,
    nthreads: Optional[int] = None,
    stem: Optional[str] = None,
    raw_dir: Optional[Path] = None,
    keep_raw_cube: bool = True,
    make_vesta: bool = True,
    vesta_output_dir: Optional[Path] = None,
    preset: str = "stm",
    isosurface: Optional[float] = None,
    structure: Optional[str] = None,
    boundary: Optional[Sequence[float]] = None,
    copy_cubes: bool = True,
) -> MultiwfnStmResult:
    candidate = find_multiwfn(multiwfn_path)
    if candidate is None:
        raise FileNotFoundError(
            "Cannot find Multiwfn. Set MULTIWFN_PATH/MULTIWFNPATH/MultiwfnPATH "
            "or add Multiwfn/Multiwfn_noGUI to PATH."
        )

    wavefunction = Path(wavefunction).expanduser().resolve()
    if not wavefunction.exists():
        raise FileNotFoundError(f"Wavefunction file not found: {wavefunction}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if raw_dir is None:
        raw_dir = output_dir / "multiwfn_stm_raw"
    else:
        raw_dir = Path(raw_dir)
        if not raw_dir.is_absolute():
            raw_dir = output_dir / raw_dir
    raw_dir.mkdir(parents=True, exist_ok=True)

    if commands_file is not None:
        command_list = read_command_file(commands_file)
    elif commands is not None:
        command_list = list(commands)
    else:
        command_list = build_stm_commands(
            bias=bias,
            fermi=fermi,
            grid_points=grid_points,
            x_range=x_range,
            y_range=y_range,
            z_range=z_range,
            prepare_fermi_temperature=prepare_fermi_temperature,
        )

    output_stem = stem or wavefunction.stem
    command_file = output_dir / "multiwfn_stm_input.txt"
    stdout_log = output_dir / "multiwfn_stm.stdout.txt"
    stderr_log = output_dir / "multiwfn_stm.stderr.txt"
    recipe_path = output_dir / "multiwfn_stm_recipe.md"
    command_file.write_text(_command_text(command_list), encoding="utf-8")

    raw_stm_cube = raw_dir / "STM.cub"
    if raw_stm_cube.exists():
        raw_stm_cube.unlink()

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
        error = f"Multiwfn STM run timed out after {timeout} seconds; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text(stdout_text, encoding="utf-8")
        stderr_log.write_text((stderr_text + "\n" if stderr_text else "") + error + "\n", encoding="utf-8")
        _write_recipe(
            recipe_path,
            multiwfn=candidate,
            wavefunction=wavefunction,
            output_dir=output_dir,
            raw_dir=raw_dir,
            command_file=command_file,
            raw_stm_cube=raw_stm_cube,
            bias=bias,
            fermi=fermi,
            grid_points=grid_points,
            x_range=x_range,
            y_range=y_range,
            z_range=z_range,
            prepare_fermi_temperature=prepare_fermi_temperature,
            commands=command_list,
            error=error,
        )
        return MultiwfnStmResult(
            candidate,
            wavefunction,
            output_dir,
            raw_dir,
            STM_PROCESSING_FAILED_CODE,
            STM_PROCESSING_FAILED_CODE,
            False,
            command_file,
            stdout_log,
            stderr_log,
            raw_stm_cube,
            None,
            recipe_path,
            None,
            error,
        )
    except OSError as exc:
        error = f"Failed to launch Multiwfn STM run: {exc}; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text("", encoding="utf-8")
        stderr_log.write_text(error + "\n", encoding="utf-8")
        _write_recipe(
            recipe_path,
            multiwfn=candidate,
            wavefunction=wavefunction,
            output_dir=output_dir,
            raw_dir=raw_dir,
            command_file=command_file,
            raw_stm_cube=raw_stm_cube,
            bias=bias,
            fermi=fermi,
            grid_points=grid_points,
            x_range=x_range,
            y_range=y_range,
            z_range=z_range,
            prepare_fermi_temperature=prepare_fermi_temperature,
            commands=command_list,
            error=error,
        )
        return MultiwfnStmResult(
            candidate,
            wavefunction,
            output_dir,
            raw_dir,
            STM_PROCESSING_FAILED_CODE,
            STM_PROCESSING_FAILED_CODE,
            False,
            command_file,
            stdout_log,
            stderr_log,
            raw_stm_cube,
            None,
            recipe_path,
            None,
            error,
        )

    stdout_log.write_text(completed.stdout or "", encoding="utf-8")
    stderr_log.write_text(completed.stderr or "", encoding="utf-8")

    error = None
    cli_returncode = completed.returncode
    stm_cube: Optional[Path] = None
    vesta_result: Optional[CubeVestaResult] = None

    if completed.returncode != 0:
        error = f"Multiwfn failed with return code {completed.returncode}; inspect {stdout_log} and {stderr_log}"
    elif not raw_stm_cube.exists():
        error = (
            "Multiwfn finished with return code 0, but expected STM cube output "
            f"`{raw_stm_cube}` was not generated"
        )
        cli_returncode = STM_OUTPUT_MISSING_CODE

    if completed.returncode == 0 and cli_returncode == 0:
        try:
            stm_cube = output_dir / f"{output_stem}_stm.cub"
            _copy_or_move(raw_stm_cube, stm_cube, move=not keep_raw_cube)
        except Exception as exc:
            error = f"Failed to copy Multiwfn STM cube: {exc}"
            cli_returncode = STM_PROCESSING_FAILED_CODE
            stm_cube = None

    if completed.returncode == 0 and cli_returncode == 0 and make_vesta and stm_cube is not None:
        try:
            vesta_result = run_preset(
                preset,
                stm_cube,
                Path(vesta_output_dir) if vesta_output_dir is not None else output_dir,
                stem=f"{output_stem}_stm",
                title=f"{output_stem} STM/LDOS",
                isosurface=isosurface,
                structure=structure,
                boundary=boundary,
                copy_cubes=copy_cubes,
            )
        except Exception as exc:
            error = f"Failed to generate VESTA file from Multiwfn STM cube: {exc}"
            cli_returncode = STM_PROCESSING_FAILED_CODE
            vesta_result = None

    result = MultiwfnStmResult(
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
        raw_stm_cube=raw_stm_cube,
        stm_cube=stm_cube,
        recipe_path=recipe_path,
        vesta_result=vesta_result,
        error=error,
    )
    _write_recipe(
        recipe_path,
        result=result,
        bias=bias,
        fermi=fermi,
        grid_points=grid_points,
        x_range=x_range,
        y_range=y_range,
        z_range=z_range,
        prepare_fermi_temperature=prepare_fermi_temperature,
        commands=command_list,
    )
    return result


def _float_pair(values: Optional[Sequence[float]]) -> Optional[Tuple[float, float]]:
    if values is None:
        return None
    if len(values) != 2:
        raise ValueError("Expected exactly two values")
    return float(values[0]), float(values[1])


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="stm-run",
        description="Run Multiwfn constant-current STM/LDOS cube generation and optionally prepare a VESTA file.",
        epilog=(
            "Default command stream: main function 300, subfunction 4, toggle to constant-current, "
            "set grid points/ranges, calculate, export STM.cub, then cube-preset stm unless --no-vesta is used."
        ),
    )
    parser.add_argument("wavefunction", type=Path, help="Wavefunction file accepted by Multiwfn and containing GTF/GTO information")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--bias", type=float, help="Bias voltage in V")
    parser.add_argument("--fermi", type=float, help="Fermi energy in eV")
    parser.add_argument(
        "--prepare-fermi-temperature",
        type=float,
        help="Run Multiwfn 300 -> 9 first at this temperature in K to prepare integer/Aufbau occupations",
    )
    parser.add_argument("--grid-points", nargs=3, type=int, default=(80, 80, 40), metavar=("NX", "NY", "NZ"))
    parser.add_argument("--x-range", nargs=2, type=float, metavar=("MIN", "MAX"), help="X range in Angstrom")
    parser.add_argument("--y-range", nargs=2, type=float, metavar=("MIN", "MAX"), help="Y range in Angstrom")
    parser.add_argument("--z-range", nargs=2, type=float, metavar=("MIN", "MAX"), help="Z range in Angstrom")
    parser.add_argument("--multiwfn", "--multiwfn-path", dest="multiwfn_path")
    parser.add_argument("--commands-file", type=Path, help="Override the generated Multiwfn STM command stream")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--nthreads", type=int)
    parser.add_argument("--stem")
    parser.add_argument("--raw-dir", type=Path)
    parser.add_argument("--no-vesta", action="store_true")
    parser.add_argument("--vesta-output-dir", type=Path)
    parser.add_argument("--preset", default="stm", help="Cube preset name or alias for VESTA output")
    parser.add_argument("--isosurface", type=float)
    parser.add_argument("--structure", choices=["auto", "none", "molecule", "crystal"])
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--no-copy-cubes", action="store_true")
    args = parser.parse_args(argv)

    try:
        result = run_multiwfn_stm(
            args.wavefunction,
            args.output_dir,
            bias=args.bias,
            fermi=args.fermi,
            grid_points=args.grid_points,
            x_range=_float_pair(args.x_range),
            y_range=_float_pair(args.y_range),
            z_range=_float_pair(args.z_range),
            prepare_fermi_temperature=args.prepare_fermi_temperature,
            multiwfn_path=args.multiwfn_path,
            commands_file=args.commands_file,
            timeout=args.timeout,
            nthreads=args.nthreads,
            stem=args.stem,
            raw_dir=args.raw_dir,
            make_vesta=not args.no_vesta,
            vesta_output_dir=args.vesta_output_dir,
            preset=args.preset,
            isosurface=args.isosurface,
            structure=args.structure,
            boundary=args.boundary,
            copy_cubes=not args.no_copy_cubes,
        )
    except (FileNotFoundError, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"stm-run: {exc}", file=sys.stderr)
        return 2

    print(f"Multiwfn: {result.multiwfn.path}")
    print(f"returncode: {result.returncode}")
    if result.cli_returncode != result.returncode:
        print(f"cli_returncode: {result.cli_returncode}")
    print(result.command_file)
    print(result.stdout_log)
    print(result.stderr_log)
    print(result.raw_dir)
    print(result.recipe_path)
    if result.stm_cube is not None and result.stm_cube.exists():
        print(result.stm_cube)
    if result.vesta_result is not None:
        print(result.vesta_result.vesta_path)
        if result.vesta_result.manifest_path is not None:
            print(result.vesta_result.manifest_path)
    if result.error:
        print(f"ERROR: {result.error}", file=sys.stderr)
    return result.cli_returncode


if __name__ == "__main__":
    raise SystemExit(main())
