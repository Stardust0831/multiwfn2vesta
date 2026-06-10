"""Run Multiwfn domain analysis from an existing cube/grid file."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, NamedTuple, Optional, Sequence

from .cube_preset import run_preset
from .cube_vesta import CubeVestaResult
from .executables import ExecutableCandidate, find_multiwfn
from .multiwfn_aim import read_command_file


DOMAIN_OUTPUT_MISSING_CODE = 3
DOMAIN_PROCESSING_FAILED_CODE = 4


class MultiwfnDomainResult(NamedTuple):
    multiwfn: ExecutableCandidate
    cube: Path
    output_dir: Path
    raw_dir: Path
    criterion: str
    domain_index: int
    returncode: int
    cli_returncode: int
    success: bool
    command_file: Path
    stdout_log: Path
    stderr_log: Path
    raw_domain_cube: Path
    raw_domain_pdb: Path
    domain_cube: Optional[Path]
    domain_pdb: Optional[Path]
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


def _validate_criterion(criterion: str) -> str:
    text = str(criterion).strip()
    if len(text) < 2 or text[0] not in {"<", ">"}:
        raise ValueError("Domain criterion must start with '<' or '>', for example '<0.5' or '>0.001'")
    try:
        float(text[1:])
    except ValueError:
        raise ValueError(f"Cannot parse numeric domain criterion: {criterion}") from None
    return text


def build_domain_commands(criterion: str = "<0.5", domain_index: int = 1) -> List[str]:
    """Build the Multiwfn command stream for cube-grid domain export."""
    criterion_text = _validate_criterion(criterion)
    index = int(domain_index)
    if index < 1:
        raise ValueError("--domain-index must be a positive integer")
    return [
        "200",
        "14",
        "3",
        criterion_text,
        "-1",
        "10",
        str(index),
        "11",
        str(index),
        "0",
        "0",
        "q",
    ]


def _write_recipe(
    path: Path,
    *,
    result: Optional[MultiwfnDomainResult] = None,
    multiwfn: Optional[ExecutableCandidate] = None,
    cube: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    raw_dir: Optional[Path] = None,
    criterion: str = "<0.5",
    domain_index: int = 1,
    command_file: Optional[Path] = None,
    raw_domain_cube: Optional[Path] = None,
    raw_domain_pdb: Optional[Path] = None,
    domain_cube: Optional[Path] = None,
    domain_pdb: Optional[Path] = None,
    vesta_result: Optional[CubeVestaResult] = None,
    commands: Optional[Sequence[str]] = None,
    error: Optional[str] = None,
) -> None:
    if result is not None:
        multiwfn = result.multiwfn
        cube = result.cube
        output_dir = result.output_dir
        raw_dir = result.raw_dir
        criterion = result.criterion
        domain_index = result.domain_index
        command_file = result.command_file
        raw_domain_cube = result.raw_domain_cube
        raw_domain_pdb = result.raw_domain_pdb
        domain_cube = result.domain_cube
        domain_pdb = result.domain_pdb
        vesta_result = result.vesta_result
        error = result.error

    lines = [
        "# Multiwfn Domain Analysis Recipe",
        "",
        f"- multiwfn: `{multiwfn.path if multiwfn is not None else None}`",
        f"- cube: `{cube}`",
        f"- output_dir: `{output_dir}`",
        f"- raw_dir: `{raw_dir}`",
        f"- criterion: `{criterion}`",
        f"- domain_index: `{domain_index}`",
        f"- command_file: `{command_file}`",
        f"- raw_domain_cube: `{raw_domain_cube}`",
        f"- raw_domain_pdb: `{raw_domain_pdb}`",
        f"- domain_cube: `{domain_cube}`",
        f"- domain_pdb: `{domain_pdb}`",
        f"- vesta_file: `{vesta_result.vesta_path if vesta_result is not None else None}`",
        f"- vesta_recipe: `{vesta_result.manifest_path if vesta_result is not None else None}`",
        f"- error: `{error}`",
        "",
        "## Source Notes",
        "",
        "- Multiwfn main menu `200` enters `otherfunc2_main`; subfunction `14` is domain analysis.",
        "- Menu option `3` sets the domain definition, for example `<0.5` or `>0.001`.",
        "- The maintained runner starts from the input cube's current grid data in memory and sends `-1`.",
        "- Post-processing option `10` exports binary `domain.cub`; option `11` exports boundary grids as `domain.pdb`.",
        "- Multiwfn writes value `1` for grids inside the selected domain and `0` outside, so `cube-preset domain` uses isosurface `0.5`.",
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


def run_multiwfn_domain(
    cube: Path,
    output_dir: Path,
    *,
    criterion: str = "<0.5",
    domain_index: int = 1,
    multiwfn_path: Optional[str] = None,
    commands: Optional[Sequence[str]] = None,
    commands_file: Optional[Path] = None,
    timeout: Optional[int] = None,
    nthreads: Optional[int] = None,
    stem: Optional[str] = None,
    raw_dir: Optional[Path] = None,
    keep_raw_outputs: bool = True,
    make_vesta: bool = True,
    vesta_output_dir: Optional[Path] = None,
    preset: str = "domain",
    isosurface: Optional[float] = None,
    structure: Optional[str] = None,
    boundary: Optional[Sequence[float]] = None,
    copy_cubes: bool = True,
) -> MultiwfnDomainResult:
    candidate = find_multiwfn(multiwfn_path)
    if candidate is None:
        raise FileNotFoundError(
            "Cannot find Multiwfn. Set MULTIWFN_PATH/MULTIWFNPATH/MultiwfnPATH "
            "or add Multiwfn/Multiwfn_noGUI to PATH."
        )

    cube = Path(cube).expanduser().resolve()
    if not cube.exists():
        raise FileNotFoundError(f"Cube file not found: {cube}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if raw_dir is None:
        raw_dir = output_dir / "multiwfn_domain_raw"
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
        command_list = build_domain_commands(criterion=criterion, domain_index=domain_index)

    output_stem = stem or cube.stem
    command_file = output_dir / "multiwfn_domain_input.txt"
    stdout_log = output_dir / "multiwfn_domain.stdout.txt"
    stderr_log = output_dir / "multiwfn_domain.stderr.txt"
    recipe_path = output_dir / "multiwfn_domain_recipe.md"
    command_file.write_text(_command_text(command_list), encoding="utf-8")

    raw_domain_cube = raw_dir / "domain.cub"
    raw_domain_pdb = raw_dir / "domain.pdb"
    for stale in (raw_domain_cube, raw_domain_pdb):
        if stale.exists():
            stale.unlink()

    command = [str(candidate.path), str(cube)]
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
        error = f"Multiwfn domain run timed out after {timeout} seconds; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text(stdout_text, encoding="utf-8")
        stderr_log.write_text((stderr_text + "\n" if stderr_text else "") + error + "\n", encoding="utf-8")
        _write_recipe(
            recipe_path,
            multiwfn=candidate,
            cube=cube,
            output_dir=output_dir,
            raw_dir=raw_dir,
            criterion=criterion,
            domain_index=domain_index,
            command_file=command_file,
            raw_domain_cube=raw_domain_cube,
            raw_domain_pdb=raw_domain_pdb,
            commands=command_list,
            error=error,
        )
        return MultiwfnDomainResult(
            candidate,
            cube,
            output_dir,
            raw_dir,
            criterion,
            domain_index,
            DOMAIN_PROCESSING_FAILED_CODE,
            DOMAIN_PROCESSING_FAILED_CODE,
            False,
            command_file,
            stdout_log,
            stderr_log,
            raw_domain_cube,
            raw_domain_pdb,
            None,
            None,
            recipe_path,
            None,
            error,
        )
    except OSError as exc:
        error = f"Failed to launch Multiwfn domain run: {exc}; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text("", encoding="utf-8")
        stderr_log.write_text(error + "\n", encoding="utf-8")
        _write_recipe(
            recipe_path,
            multiwfn=candidate,
            cube=cube,
            output_dir=output_dir,
            raw_dir=raw_dir,
            criterion=criterion,
            domain_index=domain_index,
            command_file=command_file,
            raw_domain_cube=raw_domain_cube,
            raw_domain_pdb=raw_domain_pdb,
            commands=command_list,
            error=error,
        )
        return MultiwfnDomainResult(
            candidate,
            cube,
            output_dir,
            raw_dir,
            criterion,
            domain_index,
            DOMAIN_PROCESSING_FAILED_CODE,
            DOMAIN_PROCESSING_FAILED_CODE,
            False,
            command_file,
            stdout_log,
            stderr_log,
            raw_domain_cube,
            raw_domain_pdb,
            None,
            None,
            recipe_path,
            None,
            error,
        )

    stdout_log.write_text(completed.stdout or "", encoding="utf-8")
    stderr_log.write_text(completed.stderr or "", encoding="utf-8")

    error = None
    cli_returncode = completed.returncode
    domain_cube: Optional[Path] = None
    domain_pdb: Optional[Path] = None
    vesta_result: Optional[CubeVestaResult] = None

    if completed.returncode != 0:
        error = f"Multiwfn failed with return code {completed.returncode}; inspect {stdout_log} and {stderr_log}"
    else:
        missing = [str(path) for path in (raw_domain_cube, raw_domain_pdb) if not path.exists()]
        if missing:
            error = (
                "Multiwfn finished with return code 0, but required domain output is missing: "
                + ", ".join(missing)
            )
            cli_returncode = DOMAIN_OUTPUT_MISSING_CODE

    if completed.returncode == 0 and cli_returncode == 0:
        try:
            domain_cube = output_dir / f"{output_stem}_domain.cub"
            domain_pdb = output_dir / f"{output_stem}_domain.pdb"
            _copy_or_move(raw_domain_cube, domain_cube, move=not keep_raw_outputs)
            _copy_or_move(raw_domain_pdb, domain_pdb, move=not keep_raw_outputs)
        except Exception as exc:
            error = f"Failed to copy Multiwfn domain outputs: {exc}"
            cli_returncode = DOMAIN_PROCESSING_FAILED_CODE
            domain_cube = None
            domain_pdb = None

    if completed.returncode == 0 and cli_returncode == 0 and make_vesta and domain_cube is not None:
        try:
            vesta_result = run_preset(
                preset,
                domain_cube,
                Path(vesta_output_dir) if vesta_output_dir is not None else output_dir,
                stem=f"{output_stem}_domain",
                title=f"{output_stem} domain {domain_index}",
                isosurface=isosurface,
                structure=structure,
                boundary=boundary,
                copy_cubes=copy_cubes,
            )
        except Exception as exc:
            error = f"Failed to generate VESTA file from Multiwfn domain cube: {exc}"
            cli_returncode = DOMAIN_PROCESSING_FAILED_CODE
            vesta_result = None

    result = MultiwfnDomainResult(
        multiwfn=candidate,
        cube=cube,
        output_dir=output_dir,
        raw_dir=raw_dir,
        criterion=criterion,
        domain_index=domain_index,
        returncode=completed.returncode,
        cli_returncode=cli_returncode,
        success=cli_returncode == 0,
        command_file=command_file,
        stdout_log=stdout_log,
        stderr_log=stderr_log,
        raw_domain_cube=raw_domain_cube,
        raw_domain_pdb=raw_domain_pdb,
        domain_cube=domain_cube,
        domain_pdb=domain_pdb,
        recipe_path=recipe_path,
        vesta_result=vesta_result,
        error=error,
    )
    _write_recipe(recipe_path, result=result, commands=command_list)
    return result


def _float_six(values: Optional[Sequence[float]]) -> Optional[Sequence[float]]:
    if values is None:
        return None
    if len(values) != 6:
        raise ValueError("Boundary requires six values: xmin xmax ymin ymax zmin zmax")
    return [float(value) for value in values]


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="domain-run",
        description="Run Multiwfn domain analysis on an existing cube/grid file and prepare VESTA.",
        epilog=(
            "Default command stream: main function 200, subfunction 14, set criterion, "
            "yield domains from current grid data in memory, export domain.cub and "
            "domain.pdb for the selected domain, then cube-preset domain unless --no-vesta is used."
        ),
    )
    parser.add_argument("cube", type=Path, help="Cube/grid file accepted by Multiwfn, e.g. density.cub or ESP.cub")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--criterion", default="<0.5", help="Domain definition such as '<0.5' or '>0.001'")
    parser.add_argument("--domain-index", type=int, default=1, help="Domain index to export from Multiwfn post-processing")
    parser.add_argument("--multiwfn", "--multiwfn-path", dest="multiwfn_path")
    parser.add_argument("--commands-file", type=Path, help="Override the default Multiwfn domain command stream")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--nthreads", type=int)
    parser.add_argument("--stem")
    parser.add_argument("--raw-dir", type=Path)
    parser.add_argument("--no-vesta", action="store_true", help="Do not generate a VESTA file from domain.cub")
    parser.add_argument("--vesta-output-dir", type=Path)
    parser.add_argument("--preset", default="domain", help="cube-preset preset used for the exported domain cube")
    parser.add_argument("--isosurface", type=float, help="Override the preset isosurface; default domain preset is 0.5")
    parser.add_argument("--structure", choices=["auto", "none", "molecule", "crystal"])
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--no-copy-cubes", action="store_true")
    args = parser.parse_args(argv)

    try:
        result = run_multiwfn_domain(
            args.cube,
            args.output_dir,
            criterion=args.criterion,
            domain_index=args.domain_index,
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
            boundary=_float_six(args.boundary),
            copy_cubes=not args.no_copy_cubes,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(f"domain-run: {exc}", file=sys.stderr)
        return 2

    print(f"Multiwfn: {result.multiwfn.path}")
    print(f"returncode: {result.returncode}")
    if result.cli_returncode != result.returncode:
        print(f"cli_returncode: {result.cli_returncode}")
    print(result.command_file)
    print(result.stdout_log)
    print(result.stderr_log)
    if result.domain_cube is not None and result.domain_cube.exists():
        print(result.domain_cube)
    if result.domain_pdb is not None and result.domain_pdb.exists():
        print(result.domain_pdb)
    if result.vesta_result is not None:
        print(result.vesta_result.vesta_path)
        if result.vesta_result.manifest_path is not None:
            print(result.vesta_result.manifest_path)
    print(result.recipe_path)
    if result.error:
        print(f"ERROR: {result.error}", file=sys.stderr)
    return result.cli_returncode


if __name__ == "__main__":
    raise SystemExit(main())
