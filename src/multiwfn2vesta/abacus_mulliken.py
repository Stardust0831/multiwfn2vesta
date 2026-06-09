"""Parse ABACUS Mulliken output and color VESTA atoms by per-atom values."""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

from .vesta_atom_coloring import parse_structure_sites, patch_vesta_atom_colors_file
from .vesta_parser import parse_vesta_text


FLOAT_RE = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?"

IONIC_STEP_RE = re.compile(r"^\s*---\s*Ionic\s+Step\s+(\d+)\s*---", re.IGNORECASE)
LEGACY_STEP_RE = re.compile(r"^\s*STEP:\s*(\d+)\s*$", re.IGNORECASE)
ATOM_RE = re.compile(r"^\s*Atom\s+(\d+)\s+is\s+(.+?)\s*$", re.IGNORECASE)
LEGACY_ATOM_RE = re.compile(r"^\s*(\d+)\s+Zeta\s+of\s+(\S+)", re.IGNORECASE)
CHARGE_RE = re.compile(rf"^\s*total\s+charge\s+on\s+atom\s+(\d+)\s+({FLOAT_RE})\s*$", re.IGNORECASE)
MAGNETISM_RE = re.compile(
    rf"^\s*total\s+magnetism\s+on\s+atom\s+(\d+)\s+(.+?)\s*$",
    re.IGNORECASE,
)
LEGACY_CHARGE_RE = re.compile(rf"^\s*Total\s+Charge\s+on\s+atom:\s+(\S+)\s+({FLOAT_RE})\s*$", re.IGNORECASE)
LEGACY_MAGNETISM_RE = re.compile(
    rf"^\s*Total\s+Magnetism\s+on\s+atom:\s+(\S+)\s+(.+?)\s*$",
    re.IGNORECASE,
)

PROPERTY_CHOICES = (
    "charge",
    "magnetism",
    "magnetism-x",
    "magnetism-y",
    "magnetism-z",
    "magnetism-norm",
)


@dataclass
class MullikenAtom:
    index: int
    label: str
    charge: Optional[float] = None
    magnetism: Tuple[float, ...] = ()


@dataclass
class MullikenStep:
    step: int
    atoms: List[MullikenAtom] = field(default_factory=list)

    def atom_by_index(self) -> Dict[int, MullikenAtom]:
        return {atom.index: atom for atom in self.atoms}


def _parse_float_tokens(text: str) -> Tuple[float, ...]:
    return tuple(float(match.group(0)) for match in re.finditer(FLOAT_RE, text))


def _get_or_create_atom(step: MullikenStep, index: int, label: Optional[str] = None) -> MullikenAtom:
    for atom in step.atoms:
        if atom.index == index:
            if label:
                atom.label = label
            return atom
    atom = MullikenAtom(index=index, label=label or f"Atom{index}")
    step.atoms.append(atom)
    step.atoms.sort(key=lambda item: item.index)
    return atom


def parse_abacus_mulliken_text(text: str) -> List[MullikenStep]:
    """Parse ABACUS ``mulliken.txt`` into ionic-step atom summaries.

    Current ABACUS ``origin/develop`` writes blocks headed by
    ``--- Ionic Step N ---`` and atom records like ``Atom 1 is Fe`` followed by
    ``total charge on atom`` and optional ``total magnetism on atom`` lines.
    The parser also accepts the older documentation form using ``STEP: N`` and
    ``Total Charge on atom: Fe ...``.
    """

    steps: List[MullikenStep] = []
    current_step: Optional[MullikenStep] = None
    current_atom: Optional[MullikenAtom] = None

    def ensure_step(step_number: int = 0) -> MullikenStep:
        nonlocal current_step
        if current_step is None:
            current_step = MullikenStep(step_number)
            steps.append(current_step)
        return current_step

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        match = IONIC_STEP_RE.match(line) or LEGACY_STEP_RE.match(line)
        if match:
            current_step = MullikenStep(int(match.group(1)))
            steps.append(current_step)
            current_atom = None
            continue

        match = ATOM_RE.match(line)
        if match:
            step = ensure_step()
            current_atom = _get_or_create_atom(step, int(match.group(1)), match.group(2).strip())
            continue

        match = LEGACY_ATOM_RE.match(line)
        if match:
            step = ensure_step()
            # Old documentation uses zero-based atom headers.
            current_atom = _get_or_create_atom(step, int(match.group(1)) + 1, match.group(2).strip())
            continue

        match = CHARGE_RE.match(line)
        if match:
            step = ensure_step()
            current_atom = _get_or_create_atom(step, int(match.group(1)))
            current_atom.charge = float(match.group(2))
            continue

        match = MAGNETISM_RE.match(line)
        if match:
            step = ensure_step()
            current_atom = _get_or_create_atom(step, int(match.group(1)))
            current_atom.magnetism = _parse_float_tokens(match.group(2))
            continue

        match = LEGACY_CHARGE_RE.match(line)
        if match:
            step = ensure_step()
            if current_atom is None:
                current_atom = _get_or_create_atom(step, len(step.atoms) + 1, match.group(1))
            current_atom.label = match.group(1)
            current_atom.charge = float(match.group(2))
            continue

        match = LEGACY_MAGNETISM_RE.match(line)
        if match:
            step = ensure_step()
            if current_atom is None:
                current_atom = _get_or_create_atom(step, len(step.atoms) + 1, match.group(1))
            current_atom.label = match.group(1)
            current_atom.magnetism = _parse_float_tokens(match.group(2))

    if not steps:
        raise ValueError("No ABACUS Mulliken steps were found")
    for step in steps:
        if not step.atoms:
            raise ValueError(f"Mulliken step {step.step} contains no atom summaries")
    return steps


def read_abacus_mulliken(path: Path) -> List[MullikenStep]:
    return parse_abacus_mulliken_text(path.read_text(encoding="utf-8", errors="replace"))


def select_mulliken_step(steps: Sequence[MullikenStep], step: Optional[int] = None) -> MullikenStep:
    if not steps:
        raise ValueError("No ABACUS Mulliken steps were provided")
    if step is None:
        return steps[-1]
    matches = [item for item in steps if item.step == step]
    if not matches:
        available = ", ".join(str(item.step) for item in steps)
        raise ValueError(f"Mulliken step {step} was not found; available steps: {available}")
    return matches[-1]


def mulliken_atom_value(atom: MullikenAtom, property_name: str) -> float:
    prop = property_name.replace("_", "-").lower()
    if prop == "charge":
        if atom.charge is None:
            raise ValueError(f"Atom {atom.index} has no Mulliken charge")
        return atom.charge

    if not atom.magnetism:
        raise ValueError(f"Atom {atom.index} has no Mulliken magnetism")
    if prop == "magnetism":
        if len(atom.magnetism) != 1:
            raise ValueError(
                "Vector Mulliken magnetism requires magnetism-x, magnetism-y, magnetism-z, or magnetism-norm"
            )
        return atom.magnetism[0]
    if prop == "magnetism-x":
        if len(atom.magnetism) < 3:
            raise ValueError("magnetism-x requires nspin=4 vector magnetism")
        return atom.magnetism[0]
    if prop == "magnetism-y":
        if len(atom.magnetism) < 3:
            raise ValueError("magnetism-y requires nspin=4 vector magnetism")
        return atom.magnetism[1]
    if prop == "magnetism-z":
        if len(atom.magnetism) < 3:
            raise ValueError("magnetism-z requires nspin=4 vector magnetism")
        return atom.magnetism[2]
    if prop == "magnetism-norm":
        return math.sqrt(sum(value * value for value in atom.magnetism))
    raise ValueError(f"Unknown Mulliken property: {property_name}")


def mulliken_values_by_index(step: MullikenStep, property_name: str) -> Dict[int, float]:
    return {atom.index: mulliken_atom_value(atom, property_name) for atom in step.atoms}


def _format_index_list(indices: Sequence[int], limit: int = 12) -> str:
    shown = ", ".join(str(index) for index in indices[:limit])
    if len(indices) > limit:
        shown += f", ... ({len(indices)} total)"
    return f"[{shown}]"


def _read_vesta_structure_indices(path: Path, section_index: int) -> List[int]:
    document = parse_vesta_text(path.read_text(encoding="utf-8", errors="replace"))
    struc_sections = document.sections_named("STRUC")
    if section_index < 0:
        raise ValueError("section_index must be non-negative")
    if section_index >= len(struc_sections):
        raise ValueError(f"STRUC section index {section_index} is out of range")
    return [site.index for site in parse_structure_sites(struc_sections[section_index])]


def validate_vesta_indices_for_mulliken(input_vesta: Path, step: MullikenStep, section_index: int) -> None:
    """Require the selected VESTA structure to match ABACUS atom indices.

    The generic atom-coloring backend intentionally accepts partial mappings,
    but ABACUS Mulliken output represents one ordered atom table.  In strict
    mode, silently ignoring surplus Mulliken atoms would usually mean the user
    selected the wrong VESTA file or structure section.
    """

    vesta_indices = _read_vesta_structure_indices(input_vesta, section_index)
    mulliken_indices = [atom.index for atom in step.atoms]
    if vesta_indices != mulliken_indices:
        raise ValueError(
            "Strict ABACUS Mulliken coloring requires VESTA STRUC site indices "
            "to match Mulliken atom indices exactly; "
            f"VESTA section {section_index} has {_format_index_list(vesta_indices)}, "
            f"Mulliken step {step.step} has {_format_index_list(mulliken_indices)}. "
            "Use --non-strict only if intentionally coloring a subset."
        )


def write_values_csv(path: Path, step: MullikenStep, values: Mapping[int, float]) -> None:
    lines = ["index,label,value,charge,magnetism_x,magnetism_y,magnetism_z\n"]
    for atom in step.atoms:
        magnetism = list(atom.magnetism)
        while len(magnetism) < 3:
            magnetism.append(float("nan"))
        lines.append(
            "%d,%s,%.12g,%s,%s,%s,%s\n"
            % (
                atom.index,
                atom.label,
                values[atom.index],
                "" if atom.charge is None else "%.12g" % atom.charge,
                "" if math.isnan(magnetism[0]) else "%.12g" % magnetism[0],
                "" if math.isnan(magnetism[1]) else "%.12g" % magnetism[1],
                "" if math.isnan(magnetism[2]) else "%.12g" % magnetism[2],
            )
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines), encoding="utf-8")


def color_vesta_from_mulliken(
    input_vesta: Path,
    mulliken_txt: Path,
    output_vesta: Path,
    *,
    property_name: str = "charge",
    step: Optional[int] = None,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    center: float = 0.0,
    section_index: int = 0,
    strict: bool = True,
    values_csv: Optional[Path] = None,
) -> MullikenStep:
    selected = select_mulliken_step(read_abacus_mulliken(mulliken_txt), step=step)
    if strict:
        validate_vesta_indices_for_mulliken(input_vesta, selected, section_index)
    values = mulliken_values_by_index(selected, property_name)
    patch_vesta_atom_colors_file(
        input_vesta,
        values,
        output_vesta,
        vmin=vmin,
        vmax=vmax,
        center=center,
        section_index=section_index,
        strict=strict,
    )
    if values_csv is not None:
        write_values_csv(values_csv, selected, values)
    return selected


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Color VESTA atoms from ABACUS mulliken.txt atom values.")
    parser.add_argument("input_vesta", type=Path)
    parser.add_argument("mulliken_txt", type=Path)
    parser.add_argument("output_vesta", type=Path)
    parser.add_argument("--property", choices=PROPERTY_CHOICES, default="charge")
    parser.add_argument("--step", type=int, help="Exact ABACUS ionic step number. Default: last step")
    parser.add_argument("--vmin", type=float, default=None)
    parser.add_argument("--vmax", type=float, default=None)
    parser.add_argument("--center", type=float, default=0.0)
    parser.add_argument("--section-index", type=int, default=0, help="Zero-based STRUC/SITET section index")
    parser.add_argument("--non-strict", action="store_true", help="Allow partial values and leave other sites unchanged")
    parser.add_argument("--write-values", type=Path, help="Optional CSV file with the selected per-atom values")
    args = parser.parse_args(argv)

    selected = color_vesta_from_mulliken(
        args.input_vesta,
        args.mulliken_txt,
        args.output_vesta,
        property_name=args.property,
        step=args.step,
        vmin=args.vmin,
        vmax=args.vmax,
        center=args.center,
        section_index=args.section_index,
        strict=not args.non_strict,
        values_csv=args.write_values,
    )
    print(args.output_vesta)
    print(f"colored {len(selected.atoms)} atoms from Mulliken step {selected.step}")
    if args.write_values is not None:
        print(args.write_values)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
