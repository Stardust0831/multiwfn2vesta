"""Convert ABACUS LR-TDDFT amplitudes to Multiwfn plain excitation text."""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence


ABACUS_LR_CONVERT_FAILED = 2

RY_TO_EV = 13.605693122994


@dataclass
class Transition:
    occ: int
    virt: int
    coeff: float


@dataclass
class ExcitedState:
    index: int
    multiplicity: int
    energy_ev: float
    transitions: List[Transition]


@dataclass
class ConversionResult:
    label: str
    energy_file: Path
    amplitude_file: Path
    output_file: Path
    nocc: int
    nvirt: int
    dimension_source: str
    coefficient_scale: float
    states: List[ExcitedState]
    skipped_coefficients: int
    recipe_file: Optional[Path]


def _read_numbers(path: Path) -> List[float]:
    text = path.read_text(encoding="utf-8", errors="replace")
    numbers: List[float] = []
    for token in text.split():
        try:
            numbers.append(float(token))
        except ValueError as exc:
            raise ValueError(f"Non-numeric token in {path}: {token!r}") from exc
    return numbers


def _label_multiplicity(label: str, default: int) -> int:
    normalized = label.lower()
    if normalized == "singlet":
        return 1
    if normalized == "triplet":
        return 3
    return default


def _candidate_files(calc_dir: Path, label: str, rank: int) -> tuple[Path, Path]:
    out_dirs = [calc_dir]
    out_dirs.extend(sorted(path for path in calc_dir.glob("OUT.*") if path.is_dir()))
    for directory in out_dirs:
        energy = directory / f"Excitation_Energy_{label}.dat"
        amplitude = directory / f"Excitation_Amplitude_{label}_{rank}.dat"
        if energy.exists() and amplitude.exists():
            return energy, amplitude
    return calc_dir / f"Excitation_Energy_{label}.dat", calc_dir / f"Excitation_Amplitude_{label}_{rank}.dat"


def _candidate_dirs(calc_dir: Path) -> List[Path]:
    dirs = [calc_dir]
    if calc_dir.name.startswith("OUT.") and calc_dir.parent.exists():
        dirs.append(calc_dir.parent)
    dirs.extend(sorted(path for path in calc_dir.glob("OUT.*") if path.is_dir()))
    unique: List[Path] = []
    seen = set()
    for directory in dirs:
        resolved = directory.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(directory)
    return unique


def _find_rank_files(calc_dir: Path, label: str) -> List[Path]:
    found: List[Path] = []
    pattern = re.compile(rf"^Excitation_Amplitude_{re.escape(label)}_(\d+)\.dat$")
    for directory in _candidate_dirs(calc_dir):
        found.extend(path for path in directory.iterdir() if path.is_file() and pattern.match(path.name))
    return sorted(found)


def _parse_input_dimensions(path: Path) -> tuple[Optional[int], Optional[int]]:
    nocc: Optional[int] = None
    nvirt: Optional[int] = None
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        key = parts[0].lower()
        if key == "nocc":
            nocc = int(parts[1])
        elif key == "nvirt":
            nvirt = int(parts[1])
    return nocc, nvirt


def _parse_running_dimensions(path: Path) -> tuple[Optional[int], Optional[int]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    nocc_match = re.search(r"number of occupied bands:\s*(\d+)", text, re.IGNORECASE)
    nvirt_match = re.search(r"number of virtual bands:\s*(\d+)", text, re.IGNORECASE)
    nocc = int(nocc_match.group(1)) if nocc_match else None
    nvirt = int(nvirt_match.group(1)) if nvirt_match else None
    return nocc, nvirt


def infer_lr_dimensions(calc_dir: Path) -> tuple[Optional[int], Optional[int], str]:
    """Infer ABACUS LR particle-hole dimensions from running logs or INPUT files."""
    calc_dir = calc_dir.expanduser().resolve()
    running_candidates: List[Path] = []
    input_candidates: List[Path] = []
    for directory in _candidate_dirs(calc_dir):
        running_candidates.extend(sorted(directory.glob("running*.log")))
        running_candidates.extend(sorted(directory.glob("*.log")))
        for name in ("INPUT", "INPUT.lr", "INPUT.scf"):
            path = directory / name
            if path.is_file():
                input_candidates.append(path)

    seen = set()
    for path in running_candidates:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        nocc, nvirt = _parse_running_dimensions(path)
        if nocc is not None and nvirt is not None:
            return nocc, nvirt, str(path)

    seen.clear()
    for path in input_candidates:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        nocc, nvirt = _parse_input_dimensions(path)
        if nocc is not None and nvirt is not None:
            return nocc, nvirt, str(path)

    return None, None, "not inferred"


def _resolve_dimensions(calc_dir: Path, nocc: Optional[int], nvirt: Optional[int]) -> tuple[int, int, str]:
    inferred_nocc, inferred_nvirt, source = infer_lr_dimensions(calc_dir)
    resolved_nocc = nocc if nocc is not None else inferred_nocc
    resolved_nvirt = nvirt if nvirt is not None else inferred_nvirt
    if resolved_nocc is None or resolved_nvirt is None:
        raise ValueError(
            "nocc and nvirt are required but could not be inferred from ABACUS "
            "running logs or INPUT files; pass --nocc and --nvirt explicitly."
        )
    if resolved_nocc <= 0 or resolved_nvirt <= 0:
        raise ValueError("nocc and nvirt must be positive")
    explicit = []
    if nocc is not None:
        explicit.append("nocc")
    if nvirt is not None:
        explicit.append("nvirt")
    if explicit:
        suffix = f"; inferred fallback {source}" if source != "not inferred" else ""
        return resolved_nocc, resolved_nvirt, "explicit " + ",".join(explicit) + suffix
    return resolved_nocc, resolved_nvirt, source


def parse_abacus_lr(
    calc_dir: Path,
    *,
    label: str = "singlet",
    nocc: Optional[int] = None,
    nvirt: Optional[int] = None,
    rank: int = 0,
    multiplicity: Optional[int] = None,
    energy_unit: str = "ry",
    coeff_threshold: float = 0.0,
    coefficient_scale: float = 0.7071067811865475,
    strict_single_rank: bool = True,
) -> tuple[List[ExcitedState], Path, Path, int]:
    calc_dir = calc_dir.expanduser().resolve()
    if not calc_dir.exists():
        raise FileNotFoundError(f"ABACUS LR directory not found: {calc_dir}")
    nocc, nvirt, _dimension_source = _resolve_dimensions(calc_dir, nocc, nvirt)

    if strict_single_rank:
        rank_files = _find_rank_files(calc_dir, label)
        rank_ids = sorted({int(path.stem.rsplit("_", 1)[1]) for path in rank_files})
        if rank_ids and rank_ids != [rank]:
            raise ValueError(
                "Multiple ABACUS amplitude rank files were found. "
                "The first converter version only supports single-rank outputs because "
                "distributed LR amplitudes need BLACS/Parallel_2D gather metadata. "
                f"Found ranks: {rank_ids}"
            )

    energy_file, amplitude_file = _candidate_files(calc_dir, label, rank)
    if not energy_file.exists():
        raise FileNotFoundError(f"ABACUS LR energy file not found: {energy_file}")
    if not amplitude_file.exists():
        raise FileNotFoundError(f"ABACUS LR amplitude file not found: {amplitude_file}")

    energies = _read_numbers(energy_file)
    amplitudes = _read_numbers(amplitude_file)
    pair_count = nocc * nvirt
    if pair_count == 0:
        raise ValueError("nocc*nvirt must be positive")
    if len(amplitudes) % pair_count != 0:
        raise ValueError(
            f"Amplitude count {len(amplitudes)} is not divisible by nocc*nvirt={pair_count}; "
            "check --nocc/--nvirt and ensure this is a single-rank Gamma-only output."
        )
    nstates = len(amplitudes) // pair_count
    if len(energies) != nstates:
        raise ValueError(
            f"Energy count {len(energies)} does not match amplitude-derived state count {nstates}"
        )

    if energy_unit == "ry":
        energies_ev = [energy * RY_TO_EV for energy in energies]
    elif energy_unit == "ev":
        energies_ev = energies
    else:
        raise ValueError(f"Unsupported energy unit: {energy_unit}")
    if coefficient_scale <= 0:
        raise ValueError("coefficient_scale must be positive")

    mult = _label_multiplicity(label, multiplicity if multiplicity is not None else 1)
    states: List[ExcitedState] = []
    skipped = 0
    for state_index in range(nstates):
        transitions: List[Transition] = []
        offset = state_index * pair_count
        for pair_index in range(pair_count):
            coeff = amplitudes[offset + pair_index] * coefficient_scale
            if abs(coeff) < coeff_threshold:
                skipped += 1
                continue
            iocc = pair_index // nvirt
            ivirt = pair_index % nvirt
            transitions.append(Transition(occ=iocc + 1, virt=nocc + ivirt + 1, coeff=coeff))
        states.append(
            ExcitedState(
                index=state_index + 1,
                multiplicity=mult,
                energy_ev=energies_ev[state_index],
                transitions=transitions,
            )
        )
    return states, energy_file, amplitude_file, skipped


def write_multiwfn_excitation(states: Sequence[ExcitedState], output: Path) -> None:
    lines: List[str] = []
    for state in states:
        lines.append(f" Excited State {state.index}{state.multiplicity:3d}{state.energy_ev:12.6f}")
        for transition in state.transitions:
            lines.append(f"{transition.occ:6d} ->{transition.virt:6d}{transition.coeff:12.6f}")
        lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_recipe(result: ConversionResult) -> None:
    if result.recipe_file is None:
        return
    result.recipe_file.parent.mkdir(parents=True, exist_ok=True)
    base_dir = result.recipe_file.parent

    def fmt_path(path: Path) -> str:
        try:
            return os.path.relpath(path, base_dir)
        except ValueError:
            return str(path)

    def fmt_source(source: str) -> str:
        if source == "not inferred" or source.startswith("explicit "):
            return source
        return fmt_path(Path(source))

    lines = [
        "# ABACUS LR-TDDFT To Multiwfn Excitation Recipe",
        "",
        f"- label: `{result.label}`",
        f"- energy_file: `{fmt_path(result.energy_file)}`",
        f"- amplitude_file: `{fmt_path(result.amplitude_file)}`",
        f"- output_file: `{fmt_path(result.output_file)}`",
        f"- nocc: `{result.nocc}`",
        f"- nvirt: `{result.nvirt}`",
        f"- dimension_source: `{fmt_source(result.dimension_source)}`",
        f"- coefficient_scale: `{result.coefficient_scale}`",
        f"- states: `{len(result.states)}`",
        f"- skipped_coefficients: `{result.skipped_coefficients}`",
        "",
        "## Format",
        "",
        "ABACUS amplitude pair index is interpreted as `iocc * nvirt + ivirt`, matching",
        "`source_lcao/module_lr/lr_spectrum.cpp`. Multiwfn MO indices are 1-based, so",
        "the exporter writes `iocc + 1 -> nocc + ivirt + 1`.",
        "A blank line is inserted after every excited state because Multiwfn's plain-text",
        "parser uses the blank line to terminate that state's transition list.",
        "ABACUS LR amplitudes are scaled by `coefficient_scale` before writing. The default",
        "`1/sqrt(2)` matches Multiwfn's closed-shell TDDFT normalization convention, where",
        "the sum of squared excitation coefficients is expected to be about 0.5.",
        "",
    ]
    result.recipe_file.write_text("\n".join(lines), encoding="utf-8")


def convert_abacus_lr_to_multiwfn(
    calc_dir: Path,
    output: Path,
    *,
    label: str = "singlet",
    nocc: Optional[int] = None,
    nvirt: Optional[int] = None,
    rank: int = 0,
    multiplicity: Optional[int] = None,
    energy_unit: str = "ry",
    coeff_threshold: float = 0.0,
    coefficient_scale: float = 0.7071067811865475,
    strict_single_rank: bool = True,
    recipe: Optional[Path] = None,
) -> ConversionResult:
    calc_dir = calc_dir.expanduser().resolve()
    resolved_nocc, resolved_nvirt, dimension_source = _resolve_dimensions(calc_dir, nocc, nvirt)
    states, energy_file, amplitude_file, skipped = parse_abacus_lr(
        calc_dir,
        label=label,
        nocc=resolved_nocc,
        nvirt=resolved_nvirt,
        rank=rank,
        multiplicity=multiplicity,
        energy_unit=energy_unit,
        coeff_threshold=coeff_threshold,
        coefficient_scale=coefficient_scale,
        strict_single_rank=strict_single_rank,
    )
    output = output.expanduser().resolve()
    write_multiwfn_excitation(states, output)
    recipe_file = recipe.expanduser().resolve() if recipe is not None else output.with_suffix(output.suffix + ".recipe.md")
    result = ConversionResult(
        label=label,
        energy_file=energy_file,
        amplitude_file=amplitude_file,
        output_file=output,
        nocc=resolved_nocc,
        nvirt=resolved_nvirt,
        dimension_source=dimension_source,
        coefficient_scale=coefficient_scale,
        states=states,
        skipped_coefficients=skipped,
        recipe_file=recipe_file,
    )
    write_recipe(result)
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert single-rank ABACUS LR-TDDFT amplitudes to Multiwfn plain excitation text.",
        epilog=(
            "The first version supports Gamma-only/single-rank ABACUS LR outputs. "
            "nocc/nvirt are inferred from ABACUS running logs or INPUT files when possible; "
            "pass --nocc/--nvirt explicitly to override inference."
        ),
    )
    parser.add_argument("calc_dir", type=Path, help="Directory containing OUT.* or direct Excitation_Energy/Amplitude files")
    parser.add_argument("output", type=Path, help="Output Multiwfn plain excitation text")
    parser.add_argument("--label", default="singlet", help="ABACUS label, e.g. singlet, triplet, openshell")
    parser.add_argument("--nocc", type=int, help="Number of occupied orbitals in the LR particle-hole basis; inferred when omitted")
    parser.add_argument("--nvirt", type=int, help="Number of virtual orbitals in the LR particle-hole basis; inferred when omitted")
    parser.add_argument("--rank", type=int, default=0, help="ABACUS amplitude rank suffix to read")
    parser.add_argument("--multiplicity", type=int, help="Override Multiwfn multiplicity; singlet=1 and triplet=3 by default")
    parser.add_argument("--energy-unit", choices=("ry", "ev"), default="ry", help="Unit of Excitation_Energy file")
    parser.add_argument("--coeff-threshold", type=float, default=0.0, help="Drop coefficients with abs(coeff) below this value")
    parser.add_argument(
        "--coefficient-scale",
        type=float,
        default=0.7071067811865475,
        help="Scale applied to ABACUS LR amplitudes before writing; default 1/sqrt(2) matches Multiwfn closed-shell TDDFT normalization",
    )
    parser.add_argument("--allow-multiple-rank-files", action="store_true", help="Do not fail when other rank files are present")
    parser.add_argument("--recipe", type=Path, help="Markdown recipe path; default is <output>.recipe.md")
    args = parser.parse_args(argv)

    try:
        result = convert_abacus_lr_to_multiwfn(
            args.calc_dir,
            args.output,
            label=args.label,
            nocc=args.nocc,
            nvirt=args.nvirt,
            rank=args.rank,
            multiplicity=args.multiplicity,
            energy_unit=args.energy_unit,
            coeff_threshold=args.coeff_threshold,
            coefficient_scale=args.coefficient_scale,
            strict_single_rank=not args.allow_multiple_rank_files,
            recipe=args.recipe,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"abacus-lr-to-multiwfn: {exc}", file=sys.stderr)
        return ABACUS_LR_CONVERT_FAILED

    print(result.output_file)
    print(result.recipe_file)
    print(f"nocc: {result.nocc}")
    print(f"nvirt: {result.nvirt}")
    print(f"dimension_source: {result.dimension_source}")
    print(f"coefficient_scale: {result.coefficient_scale}")
    print(f"states: {len(result.states)}")
    print(f"skipped_coefficients: {result.skipped_coefficients}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
