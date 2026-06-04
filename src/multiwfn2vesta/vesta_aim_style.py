"""Patch VESTA style tables needed by Multiwfn AIM overlay phases."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple


AimAtomType = Tuple[float, Tuple[int, int, int]]

AIM_ATOM_TYPES: Dict[str, AimAtomType] = {
    "C": (0.0200, (120, 120, 120)),
    "N": (0.0700, (255, 128, 0)),
    "O": (0.0700, (255, 255, 0)),
    "F": (0.0700, (0, 255, 0)),
}


def _line_ending(reference_line: str, default: str) -> str:
    if reference_line.endswith("\r\n"):
        return "\r\n"
    if reference_line.endswith("\n"):
        return "\n"
    return default


def _format_atomt_line(index: int, element: str, radius: float, color: Tuple[int, int, int], newline: str) -> str:
    r, g, b = color
    return (
        f"{index:3d} {element:>10s} {radius:7.4f}"
        f" {r:3d} {g:3d} {b:3d} {r:3d} {g:3d} {b:3d} 204"
        f"{newline}"
    )


def _find_atomt_sections(lines: List[str]) -> List[Tuple[int, int]]:
    sections: List[Tuple[int, int]] = []
    start = None
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "ATOMT":
            start = index
            continue
        if start is not None and stripped == "0 0 0 0 0 0":
            sections.append((start, index))
            start = None
    return sections


def _existing_atomt_elements(lines: Iterable[str]) -> Tuple[Set[str], int]:
    elements: Set[str] = set()
    max_index = 0
    for line in lines:
        fields = line.split()
        if len(fields) < 2:
            continue
        try:
            max_index = max(max_index, int(fields[0]))
        except ValueError:
            continue
        elements.add(fields[1])
    return elements, max_index


def inject_aim_atom_types_text(text: str) -> str:
    """Add missing AIM pseudo atom types to the last VESTA ATOMT section.

    VESTA keeps only one global ``ATOMT`` table when saving multi-phase files.
    If a molecular base phase is opened first, VESTA may drop the AIM phase's
    C/N/O/F atom-type rows even though its per-site ``SITET`` rows remain.  The
    missing rows can make AIM path/CP colors fall back to unrelated defaults.
    """

    default_newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines(keepends=True)
    sections = _find_atomt_sections(lines)
    if not sections:
        raise ValueError("No ATOMT section found in VESTA text")

    start, terminator = sections[-1]
    existing, max_index = _existing_atomt_elements(lines[start + 1 : terminator])
    additions: List[str] = []
    newline = _line_ending(lines[terminator], default_newline)
    next_index = max_index + 1
    for element, (radius, color) in AIM_ATOM_TYPES.items():
        if element in existing:
            continue
        additions.append(_format_atomt_line(next_index, element, radius, color, newline))
        next_index += 1

    if not additions:
        return text
    return "".join(lines[:terminator] + additions + lines[terminator:])


def inject_aim_atom_types_file(input_vesta: Path, output_vesta: Path) -> None:
    text = input_vesta.read_text(encoding="utf-8", errors="replace")
    output_vesta.write_text(inject_aim_atom_types_text(text), encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Patch VESTA ATOMT rows needed by AIM overlay phases.")
    parser.add_argument("input_vesta", type=Path)
    parser.add_argument("output_vesta", type=Path)
    args = parser.parse_args(argv)

    inject_aim_atom_types_file(args.input_vesta, args.output_vesta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
