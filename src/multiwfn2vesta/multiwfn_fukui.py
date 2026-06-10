"""Run Multiwfn density cubes for Fukui and dual-descriptor maps."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

from . import cube_arith, multiwfn_grid


FUKUI_PROCESSING_FAILED_CODE = 4
FUKUI_OPERATIONS: Tuple[str, ...] = ("fukui-plus", "fukui-minus", "dual-descriptor")


class MultiwfnFukuiResult(NamedTuple):
    output_dir: Path
    operations: Tuple[str, ...]
    grid_results: Dict[str, multiwfn_grid.MultiwfnGridResult]
    arithmetic_results: Dict[str, cube_arith.CubeArithmeticResult]
    recipe_path: Path
    success: bool
    cli_returncode: int
    error: Optional[str]


def _operation_token(operation: str) -> str:
    return operation.strip().lower().replace("_", "-")


def normalize_operations(operations: Optional[Sequence[str]]) -> Tuple[str, ...]:
    raw = list(operations or ["all"])
    normalized: List[str] = []
    for item in raw:
        token = _operation_token(item)
        if token == "all":
            if len(raw) > 1:
                raise ValueError("`all` cannot be combined with explicit Fukui operations")
            return FUKUI_OPERATIONS
        if token not in FUKUI_OPERATIONS:
            known = ", ".join(("all",) + FUKUI_OPERATIONS)
            raise ValueError(f"Unknown Fukui operation: {item}. Known operations: {known}")
        if token not in normalized:
            normalized.append(token)
    if not normalized:
        raise ValueError("At least one Fukui operation is required")
    return tuple(normalized)


def _required_states(operations: Sequence[str]) -> Tuple[str, ...]:
    states = ["neutral"]
    if any(operation in {"fukui-plus", "dual-descriptor"} for operation in operations):
        states.append("anion")
    if any(operation in {"fukui-minus", "dual-descriptor"} for operation in operations):
        states.append("cation")
    return tuple(states)


def _operation_stem(stem: Optional[str], operation: str) -> str:
    operation_name = operation.replace("-", "_")
    return f"{stem}_{operation_name}" if stem else operation_name


def _state_stem(stem: Optional[str], state: str) -> str:
    return f"{stem}_{state}" if stem else state


def _write_recipe(path: Path, result: MultiwfnFukuiResult) -> None:
    lines = [
        "# Multiwfn Fukui/Dual Descriptor Run Recipe",
        "",
        f"- output_dir: `{result.output_dir}`",
        f"- operations: `{', '.join(result.operations)}`",
        f"- success: `{result.success}`",
        f"- cli_returncode: `{result.cli_returncode}`",
        f"- error: `{result.error}`",
        "",
        "## Caveats",
        "",
        "- This workflow is intended for finite systems with comparable geometries and compatible grids.",
        "- Charged periodic supercells can be physically delicate; inspect the chemistry before interpreting the map.",
        "- The neutral density cube is generated first and reused as the reference grid for charged-state density cubes.",
        "",
        "## Density Grid Runs",
        "",
    ]
    for state in ("neutral", "anion", "cation"):
        grid_result = result.grid_results.get(state)
        if grid_result is None:
            continue
        lines.extend(
            [
                f"### {state}",
                "",
                f"- wavefunction: `{grid_result.wavefunction}`",
                f"- output_dir: `{grid_result.output_dir}`",
                f"- command_file: `{grid_result.command_file}`",
                f"- stdout_log: `{grid_result.stdout_log}`",
                f"- stderr_log: `{grid_result.stderr_log}`",
                f"- density_cube: `{grid_result.cube}`",
                f"- success: `{grid_result.success}`",
                f"- cli_returncode: `{grid_result.cli_returncode}`",
                f"- error: `{grid_result.error}`",
                "",
            ]
        )
    lines.extend(["## Cube Arithmetic", ""])
    for operation in result.operations:
        arithmetic = result.arithmetic_results.get(operation)
        lines.extend([f"### {operation}", ""])
        if arithmetic is None:
            lines.extend(["- status: `not generated`", ""])
            continue
        lines.extend(
            [
                f"- output_cube: `{arithmetic.output_cube}`",
                f"- recipe: `{arithmetic.recipe_path}`",
                f"- data_range: `{arithmetic.data_min}` to `{arithmetic.data_max}`",
                f"- vesta_file: `{arithmetic.vesta_result.vesta_path if arithmetic.vesta_result is not None else None}`",
                f"- vesta_recipe: `{arithmetic.vesta_result.manifest_path if arithmetic.vesta_result is not None else None}`",
                "",
            ]
        )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _fail_result(
    output_dir: Path,
    operations: Tuple[str, ...],
    grid_results: Dict[str, multiwfn_grid.MultiwfnGridResult],
    arithmetic_results: Dict[str, cube_arith.CubeArithmeticResult],
    recipe_path: Path,
    *,
    error: str,
    cli_returncode: int = FUKUI_PROCESSING_FAILED_CODE,
) -> MultiwfnFukuiResult:
    result = MultiwfnFukuiResult(
        output_dir,
        operations,
        grid_results,
        arithmetic_results,
        recipe_path,
        False,
        cli_returncode,
        error,
    )
    _write_recipe(recipe_path, result)
    return result


def run_multiwfn_fukui(
    output_dir: Path,
    *,
    neutral: Path,
    anion: Optional[Path] = None,
    cation: Optional[Path] = None,
    operations: Optional[Sequence[str]] = None,
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
    state_vesta: bool = False,
    no_vesta: bool = False,
    preset: str = "auto",
    isosurface: Optional[float] = None,
    structure: str = "auto",
    boundary: Optional[Sequence[float]] = None,
    cube_units: str = "auto",
    strict_atoms: bool = True,
    tolerance: float = 1.0e-6,
    copy_cubes: bool = True,
) -> MultiwfnFukuiResult:
    selected_operations = normalize_operations(operations)
    required_states = _required_states(selected_operations)
    state_paths: Dict[str, Optional[Path]] = {
        "neutral": Path(neutral),
        "anion": Path(anion) if anion is not None else None,
        "cation": Path(cation) if cation is not None else None,
    }
    for state in required_states:
        if state_paths[state] is None:
            raise ValueError(f"Operation(s) {', '.join(selected_operations)} require --{state}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    recipe_path = output_dir / "multiwfn_fukui_recipe.md"
    grid_results: Dict[str, multiwfn_grid.MultiwfnGridResult] = {}
    arithmetic_results: Dict[str, cube_arith.CubeArithmeticResult] = {}

    try:
        neutral_result = multiwfn_grid.run_multiwfn_grid(
            state_paths["neutral"],  # type: ignore[arg-type]
            output_dir / "neutral_density",
            function_name="density",
            multiwfn_path=multiwfn_path,
            timeout=timeout,
            nthreads=nthreads,
            stem=_state_stem(stem, "neutral"),
            grid_mode=grid_mode,
            grid_points=grid_points,
            grid_spacing=grid_spacing,
            grid_cube=grid_cube,
            grid_extension=grid_extension,
            pbc_origin=pbc_origin,
            pbc_lengths=pbc_lengths,
            make_vesta=state_vesta,
            preset="density",
            copy_cubes=copy_cubes,
        )
    except (FileNotFoundError, ValueError) as exc:
        return _fail_result(
            output_dir,
            selected_operations,
            grid_results,
            arithmetic_results,
            recipe_path,
            error=f"Neutral density grid generation failed: {exc}",
        )
    grid_results["neutral"] = neutral_result
    if not neutral_result.success or neutral_result.cube is None:
        return _fail_result(
            output_dir,
            selected_operations,
            grid_results,
            arithmetic_results,
            recipe_path,
            error="Neutral density grid generation failed",
            cli_returncode=neutral_result.cli_returncode or FUKUI_PROCESSING_FAILED_CODE,
        )

    for state in ("anion", "cation"):
        if state not in required_states:
            continue
        try:
            state_result = multiwfn_grid.run_multiwfn_grid(
                state_paths[state],  # type: ignore[arg-type]
                output_dir / f"{state}_density",
                function_name="density",
                multiwfn_path=multiwfn_path,
                timeout=timeout,
                nthreads=nthreads,
                stem=_state_stem(stem, state),
                grid_mode="cube",
                grid_cube=neutral_result.cube,
                make_vesta=state_vesta,
                preset="density",
                copy_cubes=copy_cubes,
            )
        except (FileNotFoundError, ValueError) as exc:
            return _fail_result(
                output_dir,
                selected_operations,
                grid_results,
                arithmetic_results,
                recipe_path,
                error=f"{state.capitalize()} density grid generation failed: {exc}",
            )
        grid_results[state] = state_result
        if not state_result.success or state_result.cube is None:
            return _fail_result(
                output_dir,
                selected_operations,
                grid_results,
                arithmetic_results,
                recipe_path,
                error=f"{state.capitalize()} density grid generation failed",
                cli_returncode=state_result.cli_returncode or FUKUI_PROCESSING_FAILED_CODE,
            )

    for operation in selected_operations:
        operation_dir = output_dir / operation.replace("-", "_")
        operation_stem = _operation_stem(stem, operation)
        terms = ()
        try:
            terms = cube_arith.terms_for_operation(
                operation,
                neutral_cube=grid_results["neutral"].cube,
                anion_cube=grid_results.get("anion").cube if "anion" in grid_results else None,
                cation_cube=grid_results.get("cation").cube if "cation" in grid_results else None,
            )
            arithmetic_results[operation] = cube_arith.run_workflow(
                operation_dir,
                terms=terms,
                operation=operation,
                stem=operation_stem,
                no_vesta=no_vesta,
                preset=preset,
                isosurface=isosurface,
                structure=structure,
                boundary=boundary,
                cube_units=cube_units,
                strict_atoms=strict_atoms,
                tolerance=tolerance,
                copy_cubes=copy_cubes,
            )
        except ValueError as exc:
            if not no_vesta and terms:
                try:
                    arithmetic_results[operation] = cube_arith.run_workflow(
                        operation_dir,
                        terms=terms,
                        operation=operation,
                        stem=operation_stem,
                        no_vesta=True,
                        preset=preset,
                        isosurface=isosurface,
                        structure=structure,
                        boundary=boundary,
                        cube_units=cube_units,
                        strict_atoms=strict_atoms,
                        tolerance=tolerance,
                        copy_cubes=copy_cubes,
                    )
                    return _fail_result(
                        output_dir,
                        selected_operations,
                        grid_results,
                        arithmetic_results,
                        recipe_path,
                        error=(
                            f"VESTA generation failed for {operation}: {exc}. "
                            "The cube-only arithmetic output was regenerated and recorded."
                        ),
                    )
                except ValueError:
                    pass
            return _fail_result(
                output_dir,
                selected_operations,
                grid_results,
                arithmetic_results,
                recipe_path,
                error=f"Cube arithmetic failed for {operation}: {exc}",
            )

    result = MultiwfnFukuiResult(
        output_dir,
        selected_operations,
        grid_results,
        arithmetic_results,
        recipe_path,
        True,
        0,
        None,
    )
    _write_recipe(recipe_path, result)
    return result


def _float_three(values: Optional[Sequence[float]]) -> Optional[Tuple[float, float, float]]:
    if values is None:
        return None
    if len(values) != 3:
        raise ValueError("Expected exactly three values")
    return float(values[0]), float(values[1]), float(values[2])


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="fukui-run",
        description="Generate density cubes from charged-state wavefunctions, then build Fukui/dual-descriptor cubes.",
        epilog=(
            "The neutral density cube is generated first and reused as the grid reference for "
            "charged-state density cubes. Intended for finite systems; charged periodic cells "
            "need careful physical treatment."
        ),
    )
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--neutral", type=Path, required=True, help="Neutral N-electron wavefunction")
    parser.add_argument("--anion", type=Path, help="N+1 wavefunction required for fukui-plus/dual-descriptor")
    parser.add_argument("--cation", type=Path, help="N-1 wavefunction required for fukui-minus/dual-descriptor")
    parser.add_argument(
        "--operation",
        action="append",
        choices=("all",) + FUKUI_OPERATIONS,
        help="Operation to build; repeatable. Default: all",
    )
    parser.add_argument("--multiwfn", "--multiwfn-path", dest="multiwfn_path")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--nthreads", type=int)
    parser.add_argument("--stem")
    parser.add_argument("--grid-mode", choices=["low", "medium", "high", "points", "spacing", "cube", "pbc-cell"], default="points")
    parser.add_argument("--grid-points", nargs=3, type=int, default=(40, 40, 40), metavar=("NX", "NY", "NZ"))
    parser.add_argument("--grid-spacing", type=float)
    parser.add_argument("--grid-cube", type=Path, help="Reference cube for the neutral density grid")
    parser.add_argument("--grid-extension", type=float)
    parser.add_argument("--pbc-origin", nargs=3, type=float, metavar=("X", "Y", "Z"))
    parser.add_argument("--pbc-lengths", nargs=3, type=float, metavar=("A", "B", "C"))
    parser.add_argument("--state-vesta", action="store_true", help="Also write VESTA density files for each state")
    parser.add_argument("--no-vesta", action="store_true", help="Do not write VESTA for Fukui/dual cubes")
    parser.add_argument("--preset", default="auto", help="Cube preset for Fukui/dual VESTA output; auto uses cube-arith defaults")
    parser.add_argument("--isosurface", type=float)
    parser.add_argument("--structure", choices=["auto", "none", "molecule", "crystal"], default="auto")
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--cube-units", choices=["auto", "bohr", "angstrom"], default="auto")
    parser.add_argument("--no-strict-atoms", action="store_true")
    parser.add_argument("--tolerance", type=float, default=1.0e-6)
    parser.add_argument("--no-copy-cubes", action="store_true")
    args = parser.parse_args(argv)

    try:
        result = run_multiwfn_fukui(
            args.output_dir,
            neutral=args.neutral,
            anion=args.anion,
            cation=args.cation,
            operations=args.operation,
            multiwfn_path=args.multiwfn_path,
            timeout=args.timeout,
            nthreads=args.nthreads,
            stem=args.stem,
            grid_mode=args.grid_mode,
            grid_points=args.grid_points,
            grid_spacing=args.grid_spacing,
            grid_cube=args.grid_cube,
            grid_extension=args.grid_extension,
            pbc_origin=_float_three(args.pbc_origin),
            pbc_lengths=_float_three(args.pbc_lengths),
            state_vesta=args.state_vesta,
            no_vesta=args.no_vesta,
            preset=args.preset,
            isosurface=args.isosurface,
            structure=args.structure,
            boundary=args.boundary,
            cube_units=args.cube_units,
            strict_atoms=not args.no_strict_atoms,
            tolerance=args.tolerance,
            copy_cubes=not args.no_copy_cubes,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(f"fukui-run: {exc}", file=sys.stderr)
        return 2

    print(result.recipe_path)
    for state in ("neutral", "anion", "cation"):
        grid_result = result.grid_results.get(state)
        if grid_result is not None and grid_result.cube is not None:
            print(grid_result.cube)
    for operation in result.operations:
        arithmetic = result.arithmetic_results.get(operation)
        if arithmetic is None:
            continue
        print(arithmetic.output_cube)
        print(arithmetic.recipe_path)
        if arithmetic.vesta_result is not None:
            print(arithmetic.vesta_result.vesta_path)
            if arithmetic.vesta_result.manifest_path is not None:
                print(arithmetic.vesta_result.manifest_path)
    if result.error:
        print(f"ERROR: {result.error}", file=sys.stderr)
    return result.cli_returncode


if __name__ == "__main__":
    raise SystemExit(main())
