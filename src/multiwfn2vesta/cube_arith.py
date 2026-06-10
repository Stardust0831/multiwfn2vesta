"""Linear arithmetic for compatible cube files."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import zip_longest
from pathlib import Path
from typing import List, NamedTuple, Optional, Sequence, Tuple

from . import cube_vesta
from .cube_preset import run_preset


DEFAULT_PRESET = "auto"


@dataclass(frozen=True)
class CubeTerm:
    coefficient: float
    cube: Path


class CubeArithmeticResult(NamedTuple):
    output_cube: Path
    recipe_path: Path
    terms: Tuple[CubeTerm, ...]
    data_min: float
    data_max: float
    data_count: int
    vesta_result: Optional[cube_vesta.CubeVestaResult]


def _read_cube_header(path: Path) -> List[str]:
    path = Path(path)
    with path.open(encoding="utf-8", errors="replace") as handle:
        header = [handle.readline(), handle.readline()]
        origin_line = handle.readline()
        if not origin_line:
            raise ValueError(f"Cannot parse cube origin line in {path}")
        fields = origin_line.split()
        if len(fields) < 4:
            raise ValueError(f"Cannot parse cube origin line in {path}")
        natoms = abs(int(fields[0]))
        header.append(origin_line)
        for _ in range(3 + natoms):
            line = handle.readline()
            if not line:
                raise ValueError(f"Cannot parse cube header in {path}")
            header.append(line)
    return header


def _atoms_compatible(
    left: cube_vesta.CubeSummary,
    right: cube_vesta.CubeSummary,
    *,
    tolerance: float,
) -> bool:
    if len(left.atoms) != len(right.atoms):
        return False
    for latom, ratom in zip(left.atoms, right.atoms):
        if latom.atomic_number != ratom.atomic_number:
            return False
        if abs(latom.charge - ratom.charge) > tolerance:
            return False
        for lvalue, rvalue in zip(latom.coords, ratom.coords):
            if abs(lvalue - rvalue) > tolerance:
                return False
    return True


def _units_compatible(
    left: cube_vesta.CubeSummary,
    right: cube_vesta.CubeSummary,
    *,
    tolerance: float,
) -> bool:
    if left.unit != right.unit:
        return False
    return abs(left.unit_scale - right.unit_scale) <= tolerance


def _validate_terms(terms: Sequence[CubeTerm]) -> Tuple[CubeTerm, ...]:
    normalized = tuple(CubeTerm(float(term.coefficient), Path(term.cube)) for term in terms)
    if not normalized:
        raise ValueError("At least one cube term is required")
    return normalized


def combine_cubes(
    terms: Sequence[CubeTerm],
    output_cube: Path,
    *,
    comment1: Optional[str] = None,
    comment2: Optional[str] = None,
    cube_units: str = "auto",
    strict: bool = True,
    strict_atoms: bool = True,
    tolerance: float = 1.0e-6,
) -> Tuple[float, float, int]:
    """Write a linear combination of compatible cube files.

    The first cube supplies the header, atoms, and grid.  Every subsequent
    cube must have the same grid, and by default the same atom list.
    """
    normalized = _validate_terms(terms)
    output_cube = Path(output_cube)
    resolved_output = output_cube.resolve()
    for term in normalized:
        if Path(term.cube).resolve() == resolved_output:
            raise ValueError(f"Output cube would overwrite an input cube: {term.cube}")
    output_cube.parent.mkdir(parents=True, exist_ok=True)

    summaries = [
        cube_vesta._read_cube_summary(term.cube, cube_units=cube_units, strict=strict)  # pylint: disable=protected-access
        for term in normalized
    ]
    reference = summaries[0]
    for summary in summaries[1:]:
        if not _units_compatible(reference, summary, tolerance=tolerance):
            raise ValueError(f"Cube unit convention is not compatible with reference: {summary.path}")
        if not cube_vesta._compatible_grid(reference, summary, tolerance=tolerance):  # pylint: disable=protected-access
            raise ValueError(f"Cube grid is not compatible with reference: {summary.path}")
        if strict_atoms and not _atoms_compatible(reference, summary, tolerance=tolerance):
            raise ValueError(f"Cube atom list is not compatible with reference: {summary.path}")

    header = _read_cube_header(normalized[0].cube)
    if comment1 is not None:
        header[0] = comment1.rstrip("\n") + "\n"
    if comment2 is not None:
        header[1] = comment2.rstrip("\n") + "\n"

    iterators = [cube_vesta._iter_cube_data_values(term.cube) for term in normalized]  # pylint: disable=protected-access
    sentinel = object()
    data_min: Optional[float] = None
    data_max: Optional[float] = None
    count = 0

    with output_cube.open("w", encoding="utf-8", newline="\n") as handle:
        for line in header:
            handle.write(line if line.endswith("\n") else line + "\n")
        row: List[float] = []
        for values in zip_longest(*iterators, fillvalue=sentinel):
            if any(value is sentinel for value in values):
                raise ValueError("Cube data lengths differ during arithmetic")
            combined = sum(term.coefficient * float(value) for term, value in zip(normalized, values))
            data_min = combined if data_min is None else min(data_min, combined)
            data_max = combined if data_max is None else max(data_max, combined)
            count += 1
            row.append(combined)
            if len(row) == 6:
                handle.write("".join(f" {value:13.6E}" for value in row) + "\n")
                row = []
        if row:
            handle.write("".join(f" {value:13.6E}" for value in row) + "\n")

    if count != reference.expected_count:
        raise ValueError(f"Cube data point count mismatch after arithmetic: got {count}, expected {reference.expected_count}")
    if data_min is None or data_max is None:
        raise ValueError("No cube data values were written")
    return data_min, data_max, count


def terms_for_operation(
    operation: str,
    *,
    neutral_cube: Optional[Path] = None,
    anion_cube: Optional[Path] = None,
    cation_cube: Optional[Path] = None,
    plus_cube: Optional[Path] = None,
    minus_cube: Optional[Path] = None,
) -> Tuple[CubeTerm, ...]:
    key = operation.strip().lower()
    if key == "linear":
        raise ValueError("The linear operation requires explicit --term entries")
    if key in {"difference", "density-difference", "spin-density"}:
        if plus_cube is None or minus_cube is None:
            raise ValueError(f"{key} requires --plus-cube and --minus-cube")
        return (CubeTerm(1.0, Path(plus_cube)), CubeTerm(-1.0, Path(minus_cube)))
    if key == "fukui-plus":
        if anion_cube is None or neutral_cube is None:
            raise ValueError("fukui-plus requires --anion-cube and --neutral-cube")
        return (CubeTerm(1.0, Path(anion_cube)), CubeTerm(-1.0, Path(neutral_cube)))
    if key == "fukui-minus":
        if neutral_cube is None or cation_cube is None:
            raise ValueError("fukui-minus requires --neutral-cube and --cation-cube")
        return (CubeTerm(1.0, Path(neutral_cube)), CubeTerm(-1.0, Path(cation_cube)))
    if key == "dual-descriptor":
        if anion_cube is None or neutral_cube is None or cation_cube is None:
            raise ValueError("dual-descriptor requires --anion-cube, --neutral-cube, and --cation-cube")
        return (
            CubeTerm(1.0, Path(anion_cube)),
            CubeTerm(-2.0, Path(neutral_cube)),
            CubeTerm(1.0, Path(cation_cube)),
        )
    raise ValueError(f"Unknown cube arithmetic operation: {operation}")


def _terms_from_cli(raw_terms: Optional[Sequence[Sequence[str]]]) -> Tuple[CubeTerm, ...]:
    if not raw_terms:
        return ()
    terms: List[CubeTerm] = []
    for coeff_text, cube_text in raw_terms:
        try:
            coefficient = float(coeff_text)
        except ValueError as exc:
            raise ValueError(f"Invalid cube coefficient: {coeff_text}") from exc
        terms.append(CubeTerm(coefficient, Path(cube_text)))
    return tuple(terms)


def _default_stem(operation: str, terms: Sequence[CubeTerm]) -> str:
    key = operation.strip().lower()
    if key != "linear":
        return key.replace("-", "_")
    if len(terms) == 1:
        return terms[0].cube.stem
    return "cube_linear_combination"


def _default_preset(operation: str) -> str:
    key = operation.strip().lower()
    if key in {"fukui-plus", "fukui-minus"}:
        return "density"
    if key == "spin-density":
        return "spin-density"
    return "signed"


def _write_recipe(
    path: Path,
    *,
    output_cube: Path,
    terms: Sequence[CubeTerm],
    operation: str,
    data_min: float,
    data_max: float,
    data_count: int,
    vesta_result: Optional[cube_vesta.CubeVestaResult],
) -> None:
    lines = [
        "# Cube Arithmetic Recipe",
        "",
        f"- operation: `{operation}`",
        f"- output_cube: `{output_cube}`",
        f"- data_count: `{data_count}`",
        f"- data_range: `{data_min}` to `{data_max}`",
        "",
        "## Terms",
        "",
    ]
    for index, term in enumerate(terms, start=1):
        lines.append(f"{index}. `{term.coefficient}` * `{term.cube}`")
    lines.extend(
        [
            "",
            "## VESTA",
            "",
            f"- vesta_file: `{vesta_result.vesta_path if vesta_result is not None else None}`",
            f"- vesta_recipe: `{vesta_result.manifest_path if vesta_result is not None else None}`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_workflow(
    output_dir: Path,
    *,
    terms: Sequence[CubeTerm],
    operation: str = "linear",
    stem: Optional[str] = None,
    output_cube: Optional[Path] = None,
    no_vesta: bool = False,
    preset: str = DEFAULT_PRESET,
    isosurface: Optional[float] = None,
    structure: str = "auto",
    boundary: Optional[Sequence[float]] = None,
    cube_units: str = "auto",
    strict: bool = True,
    strict_atoms: bool = True,
    tolerance: float = 1.0e-6,
    copy_cubes: bool = True,
) -> CubeArithmeticResult:
    normalized = _validate_terms(terms)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    effective_stem = stem or _default_stem(operation, normalized)
    if output_cube is None:
        cube_path = output_dir / f"{effective_stem}.cub"
    else:
        cube_path = Path(output_cube)
    if output_cube is not None and not cube_path.is_absolute():
        cube_path = output_dir / cube_path

    data_min, data_max, data_count = combine_cubes(
        normalized,
        cube_path,
        comment1=f"multiwfn2vesta cube-arith {operation}",
        comment2=" ".join(f"{term.coefficient}*{term.cube.name}" for term in normalized),
        cube_units=cube_units,
        strict=strict,
        strict_atoms=strict_atoms,
        tolerance=tolerance,
    )

    vesta_result: Optional[cube_vesta.CubeVestaResult] = None
    if not no_vesta:
        effective_preset = _default_preset(operation) if preset == "auto" else preset
        vesta_result = run_preset(
            effective_preset,
            cube_path,
            output_dir,
            stem=f"{effective_stem}_{effective_preset}",
            title=f"{effective_stem} ({operation})",
            isosurface=isosurface,
            structure=structure,
            boundary=boundary,
            cube_units=cube_units,
            copy_cubes=copy_cubes,
            strict=strict,
        )

    recipe_path = output_dir / f"{effective_stem}_cube_arith_recipe.md"
    _write_recipe(
        recipe_path,
        output_cube=cube_path,
        terms=normalized,
        operation=operation,
        data_min=data_min,
        data_max=data_max,
        data_count=data_count,
        vesta_result=vesta_result,
    )
    return CubeArithmeticResult(cube_path, recipe_path, normalized, data_min, data_max, data_count, vesta_result)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create a linear combination of compatible cube files and optionally prepare VESTA output."
    )
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--operation",
        choices=[
            "linear",
            "difference",
            "density-difference",
            "spin-density",
            "fukui-plus",
            "fukui-minus",
            "dual-descriptor",
        ],
        default="linear",
    )
    parser.add_argument("--term", nargs=2, action="append", metavar=("COEFF", "CUBE"))
    parser.add_argument("--plus-cube", type=Path, help="Positive/alpha/spin-up cube for density-difference or spin-density")
    parser.add_argument("--minus-cube", type=Path, help="Negative/beta/spin-down cube for density-difference or spin-density")
    parser.add_argument("--neutral-cube", type=Path, help="Neutral N-electron density cube for Fukui/dual descriptor")
    parser.add_argument("--anion-cube", type=Path, help="N+1 density cube for fukui-plus/dual descriptor")
    parser.add_argument("--cation-cube", type=Path, help="N-1 density cube for fukui-minus/dual descriptor")
    parser.add_argument("--stem")
    parser.add_argument("--output-cube", type=Path)
    parser.add_argument("--no-vesta", action="store_true")
    parser.add_argument(
        "--preset",
        default=DEFAULT_PRESET,
        help="Cube preset for VESTA output; auto uses density for fukui-plus/minus, spin-density for spin-density, and signed otherwise",
    )
    parser.add_argument("--isosurface", type=float)
    parser.add_argument("--structure", choices=["auto", "none", "molecule", "crystal"], default="auto")
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--cube-units", choices=["auto", "bohr", "angstrom"], default="auto")
    parser.add_argument("--non-strict", action="store_true", help="Allow cube data count mismatch while reading summaries")
    parser.add_argument("--no-strict-atoms", action="store_true", help="Only require grid compatibility, not identical atoms")
    parser.add_argument("--tolerance", type=float, default=1.0e-6)
    parser.add_argument("--no-copy-cubes", action="store_true")
    args = parser.parse_args(argv)

    try:
        explicit_terms = _terms_from_cli(args.term)
        if args.operation == "linear":
            terms = explicit_terms
        elif explicit_terms:
            raise ValueError("--term cannot be combined with a named --operation")
        else:
            terms = terms_for_operation(
                args.operation,
                neutral_cube=args.neutral_cube,
                anion_cube=args.anion_cube,
                cation_cube=args.cation_cube,
                plus_cube=args.plus_cube,
                minus_cube=args.minus_cube,
            )
        result = run_workflow(
            args.output_dir,
            terms=terms,
            operation=args.operation,
            stem=args.stem,
            output_cube=args.output_cube,
            no_vesta=args.no_vesta,
            preset=args.preset,
            isosurface=args.isosurface,
            structure=args.structure,
            boundary=args.boundary,
            cube_units=args.cube_units,
            strict=not args.non_strict,
            strict_atoms=not args.no_strict_atoms,
            tolerance=args.tolerance,
            copy_cubes=not args.no_copy_cubes,
        )
    except ValueError as exc:
        print(f"cube-arith: {exc}")
        return 2

    print(result.output_cube)
    print(result.recipe_path)
    if result.vesta_result is not None:
        print(result.vesta_result.vesta_path)
        if result.vesta_result.manifest_path is not None:
            print(result.vesta_result.manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
