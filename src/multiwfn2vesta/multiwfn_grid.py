"""Run Multiwfn real-space function grid/cube generation."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

from .cube_preset import run_preset
from .cube_vesta import CubeVestaResult
from .executables import ExecutableCandidate, find_multiwfn
from .multiwfn_aim import read_command_file


GRID_OUTPUT_MISSING_CODE = 3
GRID_PROCESSING_FAILED_CODE = 4


@dataclass(frozen=True)
class GridFunction:
    name: str
    index: int
    output_filename: str
    preset: str
    aliases: Tuple[str, ...] = ()
    requires_orbital: bool = False
    mapped_preset: Optional[str] = None


GRID_FUNCTIONS: Tuple[GridFunction, ...] = (
    GridFunction("density", 1, "density.cub", "density", ("rho", "electron-density", "charge-density")),
    GridFunction("gradient", 2, "gradient.cub", "density", ("rho-gradient", "grad-rho")),
    GridFunction("laplacian", 3, "laplacian.cub", "laplacian", ("lap", "laplacian-rho")),
    GridFunction("orbital", 4, "MOvalue.cub", "signed", ("mo", "wavefunction", "mo-value"), True),
    GridFunction("spin-density", 5, "spindensity.cub", "spin-density", ("spin", "spindensity")),
    GridFunction(
        "hamiltonian-ked",
        6,
        "K(r).cub",
        "hamiltonian-ked",
        ("k-r", "k(r)", "kinetic-k", "hamiltonian-kinetic-density"),
    ),
    GridFunction(
        "lagrangian-ked",
        7,
        "G(r).cub",
        "lagrangian-ked",
        ("g-r", "g(r)", "kinetic-g", "lagrangian-kinetic-density"),
    ),
    GridFunction("nuclear-esp", 8, "nucleiesp.cub", "signed", ("nuc-esp", "nuclear-potential"), mapped_preset="esp"),
    GridFunction("elf", 9, "ELF.cub", "elf", ("electron-localization-function",)),
    GridFunction("lol", 10, "LOL.cub", "lol", ("localized-orbital-locator",)),
    GridFunction("esp", 12, "totesp.cub", "signed", ("mep", "total-esp", "electrostatic-potential"), mapped_preset="esp"),
    GridFunction("rdg", 13, "RDG.cub", "rdg-scalar", ("reduced-density-gradient",)),
    GridFunction("promolecular-rdg", 14, "RDGprodens.cub", "promolecular-rdg", ("rdg-pro", "prodens-rdg")),
    GridFunction("signlambda2rho", 15, "signlambda2rho.cub", "signed", ("sl2r", "sign-lambda2-rho"), mapped_preset="iri"),
    GridFunction(
        "promolecular-signlambda2rho",
        16,
        "signlambda2rhoprodens.cub",
        "signed",
        ("prodens-signlambda2rho", "promolecular-sl2r", "sl2r-pro"),
        mapped_preset="iri",
    ),
    GridFunction(
        "alie",
        18,
        "avglocion.cub",
        "density",
        ("average-local-ionization-energy", "avglocion"),
        mapped_preset="alie",
    ),
    GridFunction("delta-g", 22, "Delta_g.cub", "density", ("deltag", "delta_g")),
    GridFunction("iri", 24, "IRI.cub", "density", ("interaction-region-indicator",)),
    GridFunction("vdw-potential", 25, "vdWpot.cub", "signed", ("vdw", "vdwpot"), mapped_preset="vdw-map"),
    GridFunction("orbital-density", 44, "orbdens.cub", "orbital-density", ("orbdens", "mo-density"), True),
)


FUNCTION_BY_NAME: Dict[str, GridFunction] = {}
FUNCTION_BY_INDEX: Dict[int, GridFunction] = {}
for _function in GRID_FUNCTIONS:
    FUNCTION_BY_NAME[_function.name] = _function
    FUNCTION_BY_INDEX[_function.index] = _function
    for _alias in _function.aliases:
        FUNCTION_BY_NAME[_alias] = _function


class MultiwfnGridResult(NamedTuple):
    multiwfn: ExecutableCandidate
    wavefunction: Path
    output_dir: Path
    raw_dir: Path
    function: GridFunction
    returncode: int
    cli_returncode: int
    success: bool
    command_file: Path
    stdout_log: Path
    stderr_log: Path
    raw_cube: Path
    cube: Optional[Path]
    recipe_path: Path
    vesta_result: Optional[CubeVestaResult]
    error: Optional[str]
    surface_cube: Optional[Path]
    mapped_preset: Optional[str]


class MultiwfnGridBatchResult(NamedTuple):
    wavefunction: Path
    output_dir: Path
    function: GridFunction
    orbitals: Tuple[str, ...]
    results: Tuple[MultiwfnGridResult, ...]
    recipe_path: Path
    success: bool
    cli_returncode: int


def available_functions_text() -> str:
    lines = ["Available Multiwfn grid functions:", ""]
    for function in GRID_FUNCTIONS:
        aliases = f" (aliases: {', '.join(function.aliases)})" if function.aliases else ""
        orbital = "; requires --orbital" if function.requires_orbital else ""
        mapped = f"; mapped preset with --surface-cube: {function.mapped_preset}" if function.mapped_preset else ""
        lines.append(
            f"- {function.name}{aliases}: index={function.index}, "
            f"Multiwfn output={function.output_filename}, preset={function.preset}{orbital}{mapped}"
        )
    return "\n".join(lines) + "\n"


def resolve_grid_function(function: Optional[str], function_index: Optional[int] = None) -> GridFunction:
    if function_index is not None:
        known = FUNCTION_BY_INDEX.get(function_index)
        if known is not None:
            return known
        return GridFunction(f"function-{function_index}", function_index, "griddata.cub", "density")

    key = (function or "density").strip().lower()
    try:
        return FUNCTION_BY_NAME[key]
    except KeyError:
        try:
            index = int(key)
        except ValueError:
            known = ", ".join(sorted(FUNCTION_BY_NAME))
            raise ValueError(f"Unknown Multiwfn grid function: {function}. Known names/aliases: {known}")
        return resolve_grid_function(None, index)


def mapped_surface_preset(function: GridFunction, preset: str = "auto") -> str:
    if preset == "auto":
        return function.mapped_preset or "surface-map"
    return preset


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


def _safe_orbital_label(orbital: str) -> str:
    safe = []
    for char in str(orbital).strip():
        if char.isalnum() or char in {"-", "_"}:
            safe.append(char)
        elif char == "+":
            safe.append("plus")
        else:
            safe.append("_")
    label = "".join(safe).strip("_")
    return label or "orbital"


def build_grid_commands(
    function: GridFunction,
    *,
    orbital: Optional[str] = None,
    grid_mode: str = "points",
    grid_points: Sequence[int] = (40, 40, 40),
    grid_spacing: Optional[float] = None,
    grid_cube: Optional[Path] = None,
    grid_extension: Optional[float] = None,
    pbc_origin: Optional[Sequence[float]] = None,
    pbc_lengths: Optional[Sequence[float]] = None,
) -> List[str]:
    commands: List[str] = ["5", str(function.index)]
    if function.requires_orbital:
        if not orbital:
            raise ValueError(f"Multiwfn function `{function.name}` requires --orbital")
        commands.append(str(orbital))
    elif orbital:
        raise ValueError("--orbital is only valid for orbital and orbital-density functions")

    mode = grid_mode.lower()
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

    commands.extend(["2", "0", "q"])
    return commands


def _write_recipe(
    path: Path,
    *,
    result: Optional[MultiwfnGridResult] = None,
    multiwfn: Optional[ExecutableCandidate] = None,
    wavefunction: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    raw_dir: Optional[Path] = None,
    function: Optional[GridFunction] = None,
    command_file: Optional[Path] = None,
    raw_cube: Optional[Path] = None,
    cube: Optional[Path] = None,
    vesta_result: Optional[CubeVestaResult] = None,
    surface_cube: Optional[Path] = None,
    mapped_preset: Optional[str] = None,
    error: Optional[str] = None,
) -> None:
    if result is not None:
        multiwfn = result.multiwfn
        wavefunction = result.wavefunction
        output_dir = result.output_dir
        raw_dir = result.raw_dir
        function = result.function
        command_file = result.command_file
        raw_cube = result.raw_cube
        cube = result.cube
        vesta_result = result.vesta_result
        error = result.error
        surface_cube = result.surface_cube
        mapped_preset = result.mapped_preset

    lines = [
        "# Multiwfn Grid Run Recipe",
        "",
        f"- multiwfn: `{multiwfn.path if multiwfn is not None else None}`",
        f"- wavefunction: `{wavefunction}`",
        f"- output_dir: `{output_dir}`",
        f"- raw_dir: `{raw_dir}`",
    ]
    if function is not None:
        lines.extend(
            [
                f"- function_name: `{function.name}`",
                f"- function_index: `{function.index}`",
                f"- multiwfn_default_cube: `{function.output_filename}`",
                f"- auto_vesta_preset: `{function.preset}`",
            ]
        )
    lines.extend(
        [
            f"- command_file: `{command_file}`",
            f"- raw_cube: `{raw_cube}`",
            f"- processed_cube: `{cube}`",
            f"- surface_cube_for_texture_map: `{surface_cube}`",
            f"- mapped_vesta_preset: `{mapped_preset}`",
            f"- vesta_file: `{vesta_result.vesta_path if vesta_result is not None else None}`",
            f"- vesta_recipe: `{vesta_result.manifest_path if vesta_result is not None else None}`",
            f"- error: `{error}`",
            "",
            "## Source Notes",
            "",
            "- Multiwfn main menu `5` calls `study3dim` for real-space function grid data.",
            "- In the `study3dim` post-processing menu, option `2` exports the current grid to a Gaussian cube file.",
            "- The default cube filename is determined by the selected real-space function index in Multiwfn source `0123dim.f90`.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_batch_recipe(path: Path, result: MultiwfnGridBatchResult) -> None:
    failed = [item for item in result.results if not item.success]
    skipped = max(0, len(result.orbitals) - len(result.results))
    lines = [
        "# Multiwfn Grid Batch Recipe",
        "",
        f"- wavefunction: `{result.wavefunction}`",
        f"- output_dir: `{result.output_dir}`",
        f"- function_name: `{result.function.name}`",
        f"- function_index: `{result.function.index}`",
        f"- orbitals: `{', '.join(result.orbitals)}`",
        f"- success: `{result.success}`",
        f"- cli_returncode: `{result.cli_returncode}`",
        f"- completed_runs: `{len(result.results)}`",
        f"- failed_runs: `{len(failed)}`",
        f"- skipped_runs: `{skipped}`",
        "",
        "## Runs",
        "",
    ]
    for index, requested_orbital in enumerate(result.orbitals, start=1):
        safe_label = _safe_orbital_label(requested_orbital)
        run_name = f"{index:03d}_{result.function.name}_{safe_label}"
        item = result.results[index - 1] if index <= len(result.results) else None
        status = "skipped"
        if item is not None:
            status = "success" if item.success else "failed"
        lines.extend(
            [
                f"### {run_name}",
                "",
                f"- requested_orbital: `{requested_orbital}`",
                f"- safe_label: `{safe_label}`",
                f"- status: `{status}`",
            ]
        )
        if item is None:
            lines.extend(
                [
                    f"- output_dir: `{result.output_dir / run_name}`",
                    "- raw_dir: `None`",
                    "- command_file: `None`",
                    "- stdout_log: `None`",
                    "- stderr_log: `None`",
                    "- raw_cube: `None`",
                    "- processed_cube: `None`",
                    "- vesta_file: `None`",
                    "- error: `not run yet or skipped after an earlier failure`",
                    "",
                ]
            )
            continue
        lines.extend(
            [
                f"- output_dir: `{item.output_dir}`",
                f"- raw_dir: `{item.raw_dir}`",
                f"- command_file: `{item.command_file}`",
                f"- stdout_log: `{item.stdout_log}`",
                f"- stderr_log: `{item.stderr_log}`",
                f"- raw_cube: `{item.raw_cube}`",
                f"- processed_cube: `{item.cube}`",
                f"- vesta_file: `"
                f"{item.vesta_result.vesta_path if item.vesta_result is not None else None}`",
                f"- error: `{item.error}`",
                "",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_multiwfn_grid(
    wavefunction: Path,
    output_dir: Path,
    *,
    function_name: Optional[str] = "density",
    function_index: Optional[int] = None,
    orbital: Optional[str] = None,
    multiwfn_path: Optional[str] = None,
    commands: Optional[Sequence[str]] = None,
    commands_file: Optional[Path] = None,
    expected_cube: Optional[Path] = None,
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
    keep_raw_cube: bool = True,
    make_vesta: bool = True,
    vesta_output_dir: Optional[Path] = None,
    surface_cube: Optional[Path] = None,
    preset: str = "auto",
    isosurface: Optional[float] = None,
    structure: Optional[str] = None,
    boundary: Optional[Sequence[float]] = None,
    copy_cubes: bool = True,
) -> MultiwfnGridResult:
    function = resolve_grid_function(function_name, function_index)
    candidate = find_multiwfn(multiwfn_path)
    if candidate is None:
        raise FileNotFoundError(
            "Cannot find Multiwfn. Set MULTIWFN_PATH/MULTIWFNPATH/MultiwfnPATH "
            "or add Multiwfn/Multiwfn_noGUI to PATH."
        )

    wavefunction = Path(wavefunction).expanduser().resolve()
    if not wavefunction.exists():
        raise FileNotFoundError(f"Wavefunction file not found: {wavefunction}")
    mapped_surface_cube: Optional[Path] = None
    if surface_cube is not None:
        mapped_surface_cube = Path(surface_cube).expanduser().resolve()
        if not mapped_surface_cube.exists():
            raise FileNotFoundError(f"Surface cube file not found: {mapped_surface_cube}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if raw_dir is None:
        raw_dir = output_dir / "multiwfn_grid_raw"
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
        command_list = build_grid_commands(
            function,
            orbital=orbital,
            grid_mode=grid_mode,
            grid_points=grid_points,
            grid_spacing=grid_spacing,
            grid_cube=grid_cube,
            grid_extension=grid_extension,
            pbc_origin=pbc_origin,
            pbc_lengths=pbc_lengths,
        )

    command_file = output_dir / "multiwfn_grid_input.txt"
    stdout_log = output_dir / "multiwfn_grid.stdout.txt"
    stderr_log = output_dir / "multiwfn_grid.stderr.txt"
    recipe_path = output_dir / "multiwfn_grid_recipe.md"
    command_file.write_text(_command_text(command_list), encoding="utf-8")

    if expected_cube is not None:
        expected_cube_path = Path(expected_cube)
        raw_cube = expected_cube_path if expected_cube_path.is_absolute() else raw_dir / expected_cube_path
    else:
        raw_cube = raw_dir / function.output_filename
    if raw_cube.exists():
        raw_cube.unlink()

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
        error = f"Multiwfn grid run timed out after {timeout} seconds; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text(stdout_text, encoding="utf-8")
        stderr_log.write_text((stderr_text + "\n" if stderr_text else "") + error + "\n", encoding="utf-8")
        _write_recipe(
            recipe_path,
            multiwfn=candidate,
            wavefunction=wavefunction,
            output_dir=output_dir,
            raw_dir=raw_dir,
            function=function,
            command_file=command_file,
            raw_cube=raw_cube,
            surface_cube=mapped_surface_cube,
            mapped_preset=mapped_surface_preset(function, preset) if mapped_surface_cube is not None else None,
            error=error,
        )
        return MultiwfnGridResult(
            candidate,
            wavefunction,
            output_dir,
            raw_dir,
            function,
            GRID_PROCESSING_FAILED_CODE,
            GRID_PROCESSING_FAILED_CODE,
            False,
            command_file,
            stdout_log,
            stderr_log,
            raw_cube,
            None,
            recipe_path,
            None,
            error,
            mapped_surface_cube,
            mapped_surface_preset(function, preset) if mapped_surface_cube is not None else None,
        )
    except OSError as exc:
        error = f"Failed to launch Multiwfn grid run: {exc}; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text("", encoding="utf-8")
        stderr_log.write_text(error + "\n", encoding="utf-8")
        _write_recipe(
            recipe_path,
            multiwfn=candidate,
            wavefunction=wavefunction,
            output_dir=output_dir,
            raw_dir=raw_dir,
            function=function,
            command_file=command_file,
            raw_cube=raw_cube,
            surface_cube=mapped_surface_cube,
            mapped_preset=mapped_surface_preset(function, preset) if mapped_surface_cube is not None else None,
            error=error,
        )
        return MultiwfnGridResult(
            candidate,
            wavefunction,
            output_dir,
            raw_dir,
            function,
            GRID_PROCESSING_FAILED_CODE,
            GRID_PROCESSING_FAILED_CODE,
            False,
            command_file,
            stdout_log,
            stderr_log,
            raw_cube,
            None,
            recipe_path,
            None,
            error,
            mapped_surface_cube,
            mapped_surface_preset(function, preset) if mapped_surface_cube is not None else None,
        )

    stdout_log.write_text(completed.stdout or "", encoding="utf-8")
    stderr_log.write_text(completed.stderr or "", encoding="utf-8")

    error = None
    cli_returncode = completed.returncode
    cube: Optional[Path] = None
    vesta_result: Optional[CubeVestaResult] = None

    if completed.returncode != 0:
        error = f"Multiwfn failed with return code {completed.returncode}; inspect {stdout_log} and {stderr_log}"
    elif not raw_cube.exists():
        error = (
            "Multiwfn finished with return code 0, but expected grid cube output "
            f"`{raw_cube}` was not generated"
        )
        cli_returncode = GRID_OUTPUT_MISSING_CODE

    if completed.returncode == 0 and cli_returncode == 0:
        try:
            cube = output_dir / f"{output_stem}_{function.name}.cub"
            _copy_or_move(raw_cube, cube, move=not keep_raw_cube)
        except Exception as exc:
            error = f"Failed to copy Multiwfn grid cube: {exc}"
            cli_returncode = GRID_PROCESSING_FAILED_CODE
            cube = None

    if completed.returncode == 0 and cli_returncode == 0 and make_vesta and cube is not None:
        try:
            if mapped_surface_cube is not None:
                preset_name = mapped_surface_preset(function, preset)
                vesta_result = run_preset(
                    preset_name,
                    mapped_surface_cube,
                    Path(vesta_output_dir) if vesta_output_dir is not None else output_dir,
                    texture_cube=cube,
                    stem=f"{output_stem}_{function.name}_{preset_name}",
                    title=f"{mapped_surface_cube.stem} colored by {function.name}",
                    isosurface=isosurface,
                    structure=structure,
                    boundary=boundary,
                    copy_cubes=copy_cubes,
                )
            else:
                preset_name = function.preset if preset == "auto" else preset
                vesta_result = run_preset(
                    preset_name,
                    cube,
                    Path(vesta_output_dir) if vesta_output_dir is not None else output_dir,
                    stem=f"{output_stem}_{function.name}_{preset_name}",
                    isosurface=isosurface,
                    structure=structure,
                    boundary=boundary,
                    copy_cubes=copy_cubes,
                )
        except Exception as exc:
            error = f"Failed to generate VESTA file from Multiwfn grid cube: {exc}"
            cli_returncode = GRID_PROCESSING_FAILED_CODE
            vesta_result = None

    result = MultiwfnGridResult(
        multiwfn=candidate,
        wavefunction=wavefunction,
        output_dir=output_dir,
        raw_dir=raw_dir,
        function=function,
        returncode=completed.returncode,
        cli_returncode=cli_returncode,
        success=cli_returncode == 0,
        command_file=command_file,
        stdout_log=stdout_log,
        stderr_log=stderr_log,
        raw_cube=raw_cube,
        cube=cube,
        recipe_path=recipe_path,
        vesta_result=vesta_result,
        error=error,
        surface_cube=mapped_surface_cube,
        mapped_preset=mapped_surface_preset(function, preset) if mapped_surface_cube is not None else None,
    )
    _write_recipe(recipe_path, result=result)
    return result


def run_multiwfn_grid_batch(
    wavefunction: Path,
    output_dir: Path,
    *,
    orbitals: Sequence[str],
    function_name: Optional[str] = "orbital",
    function_index: Optional[int] = None,
    multiwfn_path: Optional[str] = None,
    timeout: Optional[int] = None,
    nthreads: Optional[int] = None,
    stem: Optional[str] = None,
    grid_mode: str = "points",
    grid_points: Sequence[int] = (40, 40, 40),
    grid_spacing: Optional[float] = None,
    grid_cube: Optional[Path] = None,
    grid_extension: Optional[float] = None,
    pbc_origin: Optional[Sequence[float]] = None,
    pbc_lengths: Optional[Sequence[float]] = None,
    keep_raw_cube: bool = True,
    make_vesta: bool = True,
    vesta_output_dir: Optional[Path] = None,
    preset: str = "auto",
    isosurface: Optional[float] = None,
    structure: Optional[str] = None,
    boundary: Optional[Sequence[float]] = None,
    copy_cubes: bool = True,
    keep_going: bool = False,
) -> MultiwfnGridBatchResult:
    function = resolve_grid_function(function_name, function_index)
    if not function.requires_orbital:
        raise ValueError(
            "Batch orbital export requires an orbital function such as "
            "`orbital` or `orbital-density`"
        )
    normalized_orbitals = tuple(
        str(orbital).strip() for orbital in orbitals if str(orbital).strip()
    )
    if not normalized_orbitals:
        raise ValueError("At least one orbital is required for batch orbital export")

    wavefunction = Path(wavefunction).expanduser().resolve()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    batch_stem = stem or wavefunction.stem
    recipe_path = output_dir / "multiwfn_grid_batch_recipe.md"

    results: List[MultiwfnGridResult] = []

    def current_result() -> MultiwfnGridBatchResult:
        success = len(results) == len(normalized_orbitals) and all(
            item.success for item in results
        )
        cli_returncode = 0 if success else next(
            (item.cli_returncode for item in results if not item.success),
            GRID_PROCESSING_FAILED_CODE,
        )
        return MultiwfnGridBatchResult(
            wavefunction=wavefunction,
            output_dir=output_dir,
            function=function,
            orbitals=normalized_orbitals,
            results=tuple(results),
            recipe_path=recipe_path,
            success=success,
            cli_returncode=cli_returncode,
        )

    _write_batch_recipe(recipe_path, current_result())
    for index, orbital in enumerate(normalized_orbitals, start=1):
        safe = _safe_orbital_label(orbital)
        run_dir = output_dir / f"{index:03d}_{function.name}_{safe}"
        sub_vesta_output_dir = None
        if vesta_output_dir is not None:
            sub_vesta_output_dir = Path(vesta_output_dir) / run_dir.name
        result = run_multiwfn_grid(
            wavefunction,
            run_dir,
            function_name=function.name,
            orbital=orbital,
            multiwfn_path=multiwfn_path,
            timeout=timeout,
            nthreads=nthreads,
            stem=f"{batch_stem}_{safe}",
            grid_mode=grid_mode,
            grid_points=grid_points,
            grid_spacing=grid_spacing,
            grid_cube=grid_cube,
            grid_extension=grid_extension,
            pbc_origin=pbc_origin,
            pbc_lengths=pbc_lengths,
            keep_raw_cube=keep_raw_cube,
            make_vesta=make_vesta,
            vesta_output_dir=sub_vesta_output_dir,
            preset=preset,
            isosurface=isosurface,
            structure=structure,
            boundary=boundary,
            copy_cubes=copy_cubes,
        )
        results.append(result)
        _write_batch_recipe(recipe_path, current_result())
        if not result.success and not keep_going:
            break

    batch_result = current_result()
    _write_batch_recipe(recipe_path, batch_result)
    return batch_result


def _int_triple(values: Optional[Sequence[int]]) -> Tuple[int, int, int]:
    if values is None:
        return 40, 40, 40
    if len(values) != 3:
        raise ValueError("Expected exactly three grid point counts")
    return int(values[0]), int(values[1]), int(values[2])


def _float_triple(values: Optional[Sequence[float]]) -> Optional[Tuple[float, float, float]]:
    if values is None:
        return None
    if len(values) != 3:
        raise ValueError("Expected exactly three values")
    return float(values[0]), float(values[1]), float(values[2])


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run Multiwfn main-function-5 real-space grid generation and optionally prepare VESTA output.",
        epilog=(
            "Default command stream: main menu 5, selected function, grid setup, post-processing option 2, "
            "return to main menu, quit. Use --list-functions to see function aliases and default cube names."
        ),
    )
    parser.add_argument("wavefunction", type=Path, nargs="?", help="Wavefunction file accepted by Multiwfn")
    parser.add_argument("output_dir", type=Path, nargs="?")
    parser.add_argument(
        "--function",
        help=(
            "Function name/alias or numeric Multiwfn function index; defaults "
            "to density, or orbital when --orbitals is used"
        ),
    )
    parser.add_argument(
        "--function-index",
        type=int,
        help="Explicit numeric Multiwfn real-space function index",
    )
    parser.add_argument("--orbital", help="Orbital index/label for orbital or orbital-density functions")
    parser.add_argument(
        "--orbitals",
        nargs="+",
        help="Batch orbital labels/indices for orbital or orbital-density functions",
    )
    parser.add_argument(
        "--keep-going",
        action="store_true",
        help="Continue batch orbital export after a failed orbital",
    )
    parser.add_argument("--list-functions", action="store_true")
    parser.add_argument("--multiwfn", "--multiwfn-path", dest="multiwfn_path")
    parser.add_argument("--commands-file", type=Path, help="Override the generated Multiwfn command stream")
    parser.add_argument(
        "--expected-cube",
        type=Path,
        help="Expected cube name/path when using a custom command stream",
    )
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--nthreads", type=int)
    parser.add_argument("--stem")
    parser.add_argument("--raw-dir", type=Path)
    parser.add_argument(
        "--grid-mode",
        choices=["low", "medium", "high", "points", "spacing", "cube", "pbc-cell"],
        default="points",
    )
    parser.add_argument(
        "--grid-points",
        nargs=3,
        type=int,
        metavar=("NX", "NY", "NZ"),
        default=(40, 40, 40),
    )
    parser.add_argument("--grid-spacing", type=float)
    parser.add_argument("--grid-cube", type=Path)
    parser.add_argument(
        "--grid-extension",
        type=float,
        help="Non-PBC extension distance in Bohr before selecting grid mode",
    )
    parser.add_argument("--pbc-origin", nargs=3, type=float, metavar=("X", "Y", "Z"))
    parser.add_argument("--pbc-lengths", nargs=3, type=float, metavar=("A", "B", "C"))
    parser.add_argument("--move-raw-cube", action="store_true")
    parser.add_argument("--no-vesta", action="store_true")
    parser.add_argument("--vesta-output-dir", type=Path)
    parser.add_argument(
        "--surface-cube",
        type=Path,
        help=(
            "Use the generated grid cube as a texture on this surface cube. "
            "With --preset auto, ESP/ALIE/vdW/sign(lambda2)rho functions choose a mapped-surface preset."
        ),
    )
    parser.add_argument("--preset", default="auto", help="Cube preset for VESTA output; default auto from function")
    parser.add_argument("--isosurface", type=float)
    parser.add_argument("--structure", choices=["auto", "none", "molecule", "crystal"])
    parser.add_argument(
        "--boundary",
        nargs=6,
        type=float,
        metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"),
    )
    parser.add_argument("--no-copy-cubes", action="store_true")
    args = parser.parse_args(argv)

    if args.list_functions:
        print(available_functions_text(), end="")
        return 0
    if args.wavefunction is None or args.output_dir is None:
        parser.error("wavefunction and output_dir are required unless --list-functions is used")

    try:
        if args.orbitals:
            if args.orbital:
                raise ValueError("--orbital and --orbitals cannot be used together")
            if args.commands_file is not None or args.expected_cube is not None:
                raise ValueError(
                    "--commands-file and --expected-cube are not supported "
                    "with --orbitals"
                )
            if args.raw_dir is not None:
                raise ValueError("--raw-dir is not supported with --orbitals")
            if args.surface_cube is not None:
                raise ValueError("--surface-cube is not supported with --orbitals")
            result = run_multiwfn_grid_batch(
                args.wavefunction,
                args.output_dir,
                orbitals=args.orbitals,
                function_name=args.function or "orbital",
                function_index=args.function_index,
                multiwfn_path=args.multiwfn_path,
                timeout=args.timeout,
                nthreads=args.nthreads,
                stem=args.stem,
                grid_mode=args.grid_mode,
                grid_points=_int_triple(args.grid_points),
                grid_spacing=args.grid_spacing,
                grid_cube=args.grid_cube,
                grid_extension=args.grid_extension,
                pbc_origin=_float_triple(args.pbc_origin),
                pbc_lengths=_float_triple(args.pbc_lengths),
                keep_raw_cube=not args.move_raw_cube,
                make_vesta=not args.no_vesta,
                vesta_output_dir=args.vesta_output_dir,
                preset=args.preset,
                isosurface=args.isosurface,
                structure=args.structure,
                boundary=args.boundary,
                copy_cubes=not args.no_copy_cubes,
                keep_going=args.keep_going,
            )
            print(result.recipe_path)
            for item in result.results:
                print(item.output_dir)
                if item.cube is not None and item.cube.exists():
                    print(item.cube)
                if item.vesta_result is not None:
                    print(item.vesta_result.vesta_path)
                if item.error:
                    print(f"ERROR: {item.error}", file=sys.stderr)
            return result.cli_returncode

        if args.keep_going:
            raise ValueError("--keep-going is only supported with --orbitals")

        result = run_multiwfn_grid(
            args.wavefunction,
            args.output_dir,
            function_name=args.function or "density",
            function_index=args.function_index,
            orbital=args.orbital,
            multiwfn_path=args.multiwfn_path,
            commands_file=args.commands_file,
            expected_cube=args.expected_cube,
            timeout=args.timeout,
            nthreads=args.nthreads,
            stem=args.stem,
            raw_dir=args.raw_dir,
            grid_mode=args.grid_mode,
            grid_points=_int_triple(args.grid_points),
            grid_spacing=args.grid_spacing,
            grid_cube=args.grid_cube,
            grid_extension=args.grid_extension,
            pbc_origin=_float_triple(args.pbc_origin),
            pbc_lengths=_float_triple(args.pbc_lengths),
            keep_raw_cube=not args.move_raw_cube,
            make_vesta=not args.no_vesta,
            vesta_output_dir=args.vesta_output_dir,
            surface_cube=args.surface_cube,
            preset=args.preset,
            isosurface=args.isosurface,
            structure=args.structure,
            boundary=args.boundary,
            copy_cubes=not args.no_copy_cubes,
        )
    except (FileNotFoundError, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"grid-run: {exc}", file=sys.stderr)
        return 2

    print(f"Multiwfn: {result.multiwfn.path}")
    print(f"returncode: {result.returncode}")
    if result.cli_returncode != result.returncode:
        print(f"cli_returncode: {result.cli_returncode}")
    print(result.command_file)
    print(result.stdout_log)
    print(result.stderr_log)
    print(result.raw_dir)
    if result.raw_cube.exists():
        print(result.raw_cube)
    if result.cube is not None and result.cube.exists():
        print(result.cube)
    print(result.recipe_path)
    if result.vesta_result is not None:
        print(result.vesta_result.vesta_path)
        if result.vesta_result.manifest_path is not None:
            print(result.vesta_result.manifest_path)
    if result.error:
        print(f"ERROR: {result.error}", file=sys.stderr)
    return result.cli_returncode


if __name__ == "__main__":
    raise SystemExit(main())
