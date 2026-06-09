"""Sanity checks for Molden files before Multiwfn workflows."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple


CHECK_FAILED = 1

SECTION_RE = re.compile(r"^\s*\[([^\]]+)\]\s*(.*)$")
FLOAT_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][-+]?\d+)?")


class MoldenSection(NamedTuple):
    name: str
    key: str
    line_number: int
    suffix: str


class MoldenCheckResult(NamedTuple):
    path: Path
    sections: List[MoldenSection]
    atoms_count: int
    mo_count: int
    nval_entries: List[Tuple[str, float]]
    cell_numeric_rows: int
    errors: List[str]
    warnings: List[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def _section_key(name: str) -> str:
    return " ".join(name.strip().lower().split())


def _section_map(sections: Sequence[MoldenSection]) -> Dict[str, List[MoldenSection]]:
    mapping: Dict[str, List[MoldenSection]] = {}
    for section in sections:
        mapping.setdefault(section.key, []).append(section)
    return mapping


def _parse_float(value: str) -> float:
    return float(value.replace("D", "E").replace("d", "e"))


def _split_sections(lines: Sequence[str]) -> Tuple[List[MoldenSection], Dict[str, List[str]]]:
    sections: List[MoldenSection] = []
    contents: Dict[str, List[str]] = {}
    current_key: Optional[str] = None
    for line_number, line in enumerate(lines, start=1):
        match = SECTION_RE.match(line)
        if match:
            name = match.group(1).strip()
            key = _section_key(name)
            sections.append(MoldenSection(name=name, key=key, line_number=line_number, suffix=match.group(2).strip()))
            contents.setdefault(key, [])
            current_key = key
            continue
        if current_key is not None:
            contents[current_key].append(line.rstrip("\n"))
    return sections, contents


def _count_atoms(atom_lines: Sequence[str]) -> int:
    count = 0
    for line in atom_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.split()
        if len(parts) >= 6 and parts[0][0].isalpha():
            count += 1
    return count


def _count_mos(mo_lines: Sequence[str]) -> int:
    markers = {"sym=": 0, "ene=": 0, "occup=": 0}
    for line in mo_lines:
        stripped = line.strip().lower()
        for marker in markers:
            if stripped.startswith(marker):
                markers[marker] += 1
    return max(markers.values())


def _parse_nval(nval_lines: Sequence[str]) -> List[Tuple[str, float]]:
    entries: List[Tuple[str, float]] = []
    for line in nval_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.split()
        if len(parts) < 2:
            continue
        try:
            entries.append((parts[0], _parse_float(parts[1])))
        except ValueError:
            continue
    return entries


def _count_cell_numeric_rows(cell_lines: Sequence[str]) -> int:
    rows = 0
    for line in cell_lines:
        if len(FLOAT_RE.findall(line)) >= 3:
            rows += 1
    return rows


def check_molden_file(
    path: Path,
    *,
    abacus: bool = False,
    require_cell: bool = False,
    require_nval: bool = False,
) -> MoldenCheckResult:
    """Inspect a Molden file for sections needed by Multiwfn workflows."""
    path = Path(path).expanduser()
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    sections, contents = _split_sections(lines)
    mapping = _section_map(sections)

    effective_require_cell = require_cell or abacus
    effective_require_nval = require_nval or abacus
    errors: List[str] = []
    warnings: List[str] = []

    for section in ("atoms", "gto", "mo"):
        if section not in mapping:
            errors.append(f"Missing required [{section.upper() if section != 'gto' else 'GTO'}] section")

    if "molden format" not in mapping:
        warnings.append("Missing [Molden Format] header; Multiwfn may still read some files, but this is not a standard Molden header")

    if effective_require_cell and "cell" not in mapping:
        errors.append("Missing [Cell] section required for ABACUS/periodic workflows")

    if effective_require_nval and "nval" not in mapping:
        errors.append("Missing [Nval] section required for ABACUS pseudopotential workflows")

    atoms_count = _count_atoms(contents.get("atoms", []))
    if "atoms" in mapping and atoms_count == 0:
        errors.append("[Atoms] section is present but no atom records were recognized")

    mo_count = _count_mos(contents.get("mo", []))
    if "mo" in mapping and mo_count == 0:
        errors.append("[MO] section is present but no orbital block markers were recognized")

    nval_entries = _parse_nval(contents.get("nval", []))
    if "nval" in mapping and not nval_entries:
        errors.append("[Nval] section is present but no element/value entries were recognized")

    cell_numeric_rows = _count_cell_numeric_rows(contents.get("cell", []))
    if "cell" in mapping and cell_numeric_rows == 0:
        errors.append("[Cell] section is present but no numeric cell rows were recognized")
    elif "cell" in mapping and cell_numeric_rows not in (1, 3):
        warnings.append(
            f"[Cell] contains {cell_numeric_rows} numeric rows; expected either one parameter row or three vector rows"
        )

    if abacus:
        warnings.append(
            "ABACUS Molden should come from latest interfaces/Multiwfn_interface/molden.py; "
            "only LCAO nspin=1/2 Gamma/single-k workflows are currently supported"
        )

    return MoldenCheckResult(
        path=path,
        sections=sections,
        atoms_count=atoms_count,
        mo_count=mo_count,
        nval_entries=nval_entries,
        cell_numeric_rows=cell_numeric_rows,
        errors=errors,
        warnings=warnings,
    )


def format_report(result: MoldenCheckResult, *, abacus: bool = False) -> str:
    section_text = ", ".join(f"[{section.name}]@{section.line_number}" for section in result.sections)
    if not section_text:
        section_text = "(none)"

    lines = [
        f"Molden file: {result.path}",
        f"Mode: {'ABACUS pseudopotential' if abacus else 'generic'}",
        f"Sections: {section_text}",
        f"Atoms: {result.atoms_count}",
        f"MO blocks: {result.mo_count}",
        f"Nval entries: {len(result.nval_entries)}",
        f"Cell numeric rows: {result.cell_numeric_rows}",
    ]
    if result.nval_entries:
        entries = ", ".join(f"{elem}={value:g}" for elem, value in result.nval_entries)
        lines.append(f"Nval detail: {entries}")
    if result.warnings:
        lines.append("Warnings:")
        lines.extend(f"- {warning}" for warning in result.warnings)
    if result.errors:
        lines.append("Errors:")
        lines.extend(f"- {error}" for error in result.errors)
    lines.append("Result: OK" if result.ok else "Result: FAILED")
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check whether a Molden file has the sections needed for Multiwfn workflows.",
        epilog=(
            "Use --abacus for ABACUS pseudopotential Molden files. It requires "
            "[Cell] and [Nval], matching the latest ABACUS Multiwfn interface "
            "recommendation."
        ),
    )
    parser.add_argument("molden", type=Path)
    parser.add_argument("--abacus", action="store_true", help="Require ABACUS-specific [Cell] and [Nval] sections")
    parser.add_argument("--require-cell", action="store_true", help="Require [Cell] even outside --abacus mode")
    parser.add_argument("--require-nval", action="store_true", help="Require [Nval] even outside --abacus mode")
    args = parser.parse_args(argv)

    try:
        result = check_molden_file(
            args.molden,
            abacus=args.abacus,
            require_cell=args.require_cell,
            require_nval=args.require_nval,
        )
    except FileNotFoundError as exc:
        print(f"molden-check: {exc}", file=sys.stderr)
        return CHECK_FAILED

    print(format_report(result, abacus=args.abacus), end="")
    return 0 if result.ok else CHECK_FAILED


if __name__ == "__main__":
    raise SystemExit(main())
