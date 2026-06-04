"""Patch per-site VESTA atom colors from scalar values.

VESTA evidence in this project does not show a native atom scalar-colormap
field.  This module implements the reliable route: resolve values to RGB in
Python and write those colors into the ``SITET`` rows.
"""

from __future__ import annotations

import argparse
import csv
import io
from collections.abc import Mapping as MappingABC
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

from .vesta_parser import VestaSection, parse_vesta_text


RGB = Tuple[int, int, int]
ValueKey = Union[int, str]

DEFAULT_NEGATIVE_COLOR: RGB = (49, 130, 189)
DEFAULT_CENTER_COLOR: RGB = (247, 247, 247)
DEFAULT_POSITIVE_COLOR: RGB = (203, 24, 29)


@dataclass
class VestaStructureSite:
    index: int
    element: str
    label: str


@dataclass
class VestaSiteStyle:
    index: int
    label: str
    radius_text: str
    tail_fields: List[str]
    newline: str


@dataclass
class VestaAtomTypeStyle:
    element: str
    radius_text: str
    alpha_text: str


def _line_ending(line: str, default: str = "\n") -> str:
    if line.endswith("\r\n"):
        return "\r\n"
    if line.endswith("\n"):
        return "\n"
    return default


def _safe_int(text: str) -> Optional[int]:
    try:
        return int(text)
    except ValueError:
        return None


def _is_sentinel(line: str) -> bool:
    fields = line.split()
    return bool(fields and fields[0] == "0")


def parse_structure_sites(section: VestaSection) -> List[VestaStructureSite]:
    """Parse site index/element/label records from a VESTA ``STRUC`` section."""

    sites: List[VestaStructureSite] = []
    for line in section.body_lines:
        fields = line.split()
        if not fields:
            continue
        index = _safe_int(fields[0])
        if index is None:
            continue
        if index == 0:
            break
        if len(fields) < 3:
            raise ValueError(f"Cannot parse STRUC site line: {line.rstrip()}")
        sites.append(VestaStructureSite(index=index, element=fields[1], label=fields[2]))
    return sites


def parse_sitet_style_line(line: str) -> Optional[VestaSiteStyle]:
    """Parse one non-sentinel ``SITET`` line enough to preserve radius/tail."""

    fields = line.split()
    if not fields:
        return None
    index = _safe_int(fields[0])
    if index is None:
        return None
    if index == 0:
        return None
    if len(fields) < 10:
        raise ValueError(f"Cannot parse SITET style line: {line.rstrip()}")
    return VestaSiteStyle(
        index=index,
        label=fields[1],
        radius_text=fields[2],
        tail_fields=fields[9:],
        newline=_line_ending(line),
    )


def parse_atom_type_styles(section: VestaSection) -> Dict[str, VestaAtomTypeStyle]:
    """Parse enough of ``ATOMT`` to reuse element radii for new ``SITET`` rows."""

    styles: Dict[str, VestaAtomTypeStyle] = {}
    for line in section.body_lines:
        fields = line.split()
        if not fields:
            continue
        index = _safe_int(fields[0])
        if index is None:
            continue
        if index == 0:
            break
        if len(fields) < 10:
            continue
        styles[fields[1]] = VestaAtomTypeStyle(
            element=fields[1],
            radius_text=fields[2],
            alpha_text=fields[9],
        )
    return styles


def _format_sitet_line(style: VestaSiteStyle, color: RGB) -> str:
    r, g, b = color
    tail = " ".join(style.tail_fields) if style.tail_fields else "204 0"
    return (
        f"{style.index:4d} {style.label:>12s} {style.radius_text:>7s}"
        f" {r:3d} {g:3d} {b:3d} {r:3d} {g:3d} {b:3d} {tail}"
        f"{style.newline}"
    )


def _interpolate_rgb(left: RGB, right: RGB, t: float) -> RGB:
    t = max(0.0, min(1.0, t))
    return tuple(int(round(left[i] + (right[i] - left[i]) * t)) for i in range(3))  # type: ignore[return-value]


def blue_white_red(
    value: float,
    *,
    vmin: float,
    vmax: float,
    center: float = 0.0,
    negative_color: RGB = DEFAULT_NEGATIVE_COLOR,
    center_color: RGB = DEFAULT_CENTER_COLOR,
    positive_color: RGB = DEFAULT_POSITIVE_COLOR,
) -> RGB:
    """Map a scalar to a blue-white-red diverging color.

    Values below ``center`` interpolate from blue to white.  Values above
    ``center`` interpolate from white to red.  Values outside the range clamp.
    """

    if vmin >= vmax:
        raise ValueError("vmin must be smaller than vmax")
    if not (vmin <= center <= vmax):
        raise ValueError("center must be between vmin and vmax")

    value = max(vmin, min(vmax, value))
    if value <= center:
        if center == vmin:
            return center_color
        return _interpolate_rgb(negative_color, center_color, (value - vmin) / (center - vmin))
    if center == vmax:
        return center_color
    return _interpolate_rgb(center_color, positive_color, (value - center) / (vmax - center))


def _auto_range(values: Sequence[float], vmin: Optional[float], vmax: Optional[float], center: float) -> Tuple[float, float]:
    if not values:
        raise ValueError("No scalar values were provided")
    data_min = min(values)
    data_max = max(values)
    if vmin is not None and vmax is not None:
        return vmin, vmax
    if vmin is not None:
        return vmin, data_max if vmax is None else vmax
    if vmax is not None:
        return data_min if vmin is None else vmin, vmax

    span = max(abs(data_min - center), abs(data_max - center))
    if span == 0:
        span = 1.0
    return center - span, center + span


def _values_for_sites(
    sites: Sequence[VestaStructureSite],
    values: Union[Sequence[float], Mapping[ValueKey, float]],
    *,
    strict: bool,
) -> Dict[int, float]:
    by_index: Dict[int, float] = {}
    if isinstance(values, MappingABC):
        for site in sites:
            if site.label in values:
                by_index[site.index] = float(values[site.label])
            elif site.index in values:
                by_index[site.index] = float(values[site.index])
            elif str(site.index) in values:
                by_index[site.index] = float(values[str(site.index)])
            elif strict:
                raise ValueError(f"Missing scalar value for site {site.index} {site.label}")
        return by_index

    if strict and len(values) != len(sites):
        raise ValueError(f"Expected {len(sites)} ordered values, got {len(values)}")
    for site, value in zip(sites, values):
        by_index[site.index] = float(value)
    return by_index


def _find_terminator(body_lines: Sequence[str]) -> int:
    for index, line in enumerate(body_lines):
        if _is_sentinel(line):
            return index
    raise ValueError("SITET section has no sentinel terminator")


def patch_vesta_atom_colors_text(
    text: str,
    values: Union[Sequence[float], Mapping[ValueKey, float]],
    *,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    center: float = 0.0,
    section_index: int = 0,
    strict: bool = True,
) -> str:
    """Return VESTA text with per-site RGB colors patched in ``SITET``.

    ``values`` may be an ordered sequence matching the ``STRUC`` site order, or
    a mapping keyed by site label and/or one-based site index.  Other VESTA
    sections are serialized through the lossless parser unchanged.
    """

    document = parse_vesta_text(text)
    struc_sections = document.sections_named("STRUC")
    sitet_sections = document.sections_named("SITET")
    if section_index < 0:
        raise ValueError("section_index must be non-negative")
    if section_index >= len(struc_sections):
        raise ValueError(f"STRUC section index {section_index} is out of range")
    if section_index >= len(sitet_sections):
        raise ValueError(f"SITET section index {section_index} is out of range")

    sites = parse_structure_sites(struc_sections[section_index])
    value_by_index = _values_for_sites(sites, values, strict=strict)
    scale_values = list(value_by_index.values())
    effective_vmin, effective_vmax = _auto_range(scale_values, vmin, vmax, center)
    colors = {
        site_index: blue_white_red(value, vmin=effective_vmin, vmax=effective_vmax, center=center)
        for site_index, value in value_by_index.items()
    }

    sitet = sitet_sections[section_index]
    atomt_sections = document.sections_named("ATOMT")
    atom_type_styles = parse_atom_type_styles(atomt_sections[-1]) if atomt_sections else {}
    terminator = _find_terminator(sitet.body_lines)
    default_newline = "\r\n" if "\r\n" in text else "\n"
    existing_lines = sitet.body_lines[:terminator]
    terminator_and_after = sitet.body_lines[terminator:]
    existing_styles: List[VestaSiteStyle] = []
    for line in existing_lines:
        style = parse_sitet_style_line(line)
        if style is not None:
            existing_styles.append(style)

    style_by_index = {style.index: style for style in existing_styles}
    style_by_label = {style.label: style for style in existing_styles}
    site_by_index = {site.index: site for site in sites}

    rewritten: List[str] = []
    seen = set()
    for line in existing_lines:
        style = parse_sitet_style_line(line)
        if style is None:
            rewritten.append(line)
            continue
        color = colors.get(style.index)
        if color is None:
            rewritten.append(line)
            continue
        rewritten.append(_format_sitet_line(style, color))
        seen.add(style.index)

    for site in sites:
        if site.index in seen or site.index not in colors:
            continue
        template = style_by_index.get(site.index) or style_by_label.get(site.label)
        if template is None:
            atom_type = atom_type_styles.get(site.element)
            template = VestaSiteStyle(
                index=site.index,
                label=site.label,
                radius_text=atom_type.radius_text if atom_type is not None else "0.5000",
                tail_fields=[atom_type.alpha_text if atom_type is not None else "204", "0"],
                newline=default_newline,
            )
        rewritten.append(_format_sitet_line(template, colors[site.index]))

    # Touch site_by_index so mismatched style indices are easy to diagnose while
    # keeping unrelated SITET rows intact.
    unknown_colored = [index for index in colors if index not in site_by_index]
    if unknown_colored:
        raise ValueError(f"Scalar values target unknown site indices: {unknown_colored}")

    sitet.replace_body(rewritten + list(terminator_and_after))
    return document.text()


def patch_vesta_atom_colors_file(
    input_vesta: Path,
    values: Union[Sequence[float], Mapping[ValueKey, float]],
    output_vesta: Path,
    *,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    center: float = 0.0,
    section_index: int = 0,
    strict: bool = True,
    encoding: str = "utf-8",
) -> None:
    with input_vesta.open(encoding=encoding, errors="replace", newline="") as handle:
        text = handle.read()
    patched = patch_vesta_atom_colors_text(
        text,
        values,
        vmin=vmin,
        vmax=vmax,
        center=center,
        section_index=section_index,
        strict=strict,
    )
    with output_vesta.open("w", encoding=encoding, newline="") as handle:
        handle.write(patched)


def _split_whitespace_rows(text: str) -> List[List[str]]:
    rows: List[List[str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        rows.append(line.split())
    return rows


def _read_delimited_rows(text: str) -> List[List[str]]:
    content = "\n".join(line for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#"))
    if not content.strip():
        return []
    if "," not in content and "\t" not in content:
        return _split_whitespace_rows(content)
    sample = content[:2048]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t")
    except csv.Error:
        dialect = csv.excel_tab if "\t" in content else csv.excel
    reader = csv.reader(io.StringIO(content), dialect)
    return [[cell.strip() for cell in row] for row in reader if any(cell.strip() for cell in row)]


def _normalized(text: str) -> str:
    return text.strip().lower().replace("-", "_")


def _looks_like_header(row: Sequence[str]) -> bool:
    names = {_normalized(cell) for cell in row}
    known = {
        "index",
        "id",
        "site_index",
        "atom_index",
        "label",
        "site",
        "atom",
        "name",
        "value",
        "scalar",
        "charge",
        "q",
    }
    return bool(names & known)


def _find_column(header: Sequence[str], candidates: Iterable[str]) -> Optional[int]:
    normalized = [_normalized(cell) for cell in header]
    for candidate in candidates:
        if candidate in normalized:
            return normalized.index(candidate)
    return None


def read_site_values_table(path: Path) -> Union[List[float], Dict[ValueKey, float]]:
    """Read scalar values from a simple CSV/TSV/whitespace table.

    Supported forms:

    - one value per row, no header: ordered values;
    - ``label,value`` or ``index,value`` rows, with or without a header;
    - headers named like ``label``, ``site``, ``index``, ``value``, ``charge``.
    """

    rows = _read_delimited_rows(path.read_text(encoding="utf-8", errors="replace"))
    if not rows:
        raise ValueError(f"No scalar values found in {path}")

    if _looks_like_header(rows[0]):
        header = rows[0]
        data = rows[1:]
        value_col = _find_column(header, ("value", "scalar", "charge", "q"))
        label_col = _find_column(header, ("label", "site", "atom", "name"))
        index_col = _find_column(header, ("index", "id", "site_index", "atom_index"))
        if value_col is None:
            raise ValueError("Value table header must contain value/scalar/charge/q")
        if label_col is None and index_col is None:
            return [float(row[value_col]) for row in data]
        values: Dict[ValueKey, float] = {}
        for row in data:
            if value_col >= len(row):
                raise ValueError(f"Missing value column in row: {row}")
            value = float(row[value_col])
            if label_col is not None and label_col < len(row) and row[label_col]:
                values[row[label_col]] = value
            elif index_col is not None and index_col < len(row) and row[index_col]:
                values[int(row[index_col])] = value
            else:
                raise ValueError(f"Missing site key in row: {row}")
        return values

    if len(rows[0]) == 1:
        return [float(row[0]) for row in rows]

    values = {}
    for row in rows:
        if len(row) < 2:
            raise ValueError(f"Expected at least two columns in keyed value row: {row}")
        key_text = row[0]
        key_int = _safe_int(key_text)
        key: ValueKey = key_int if key_int is not None else key_text
        values[key] = float(row[1])
    return values


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Patch VESTA SITET atom RGB colors from per-site scalar values.")
    parser.add_argument("input_vesta", type=Path)
    parser.add_argument("values_table", type=Path, help="CSV/TSV/whitespace values table")
    parser.add_argument("output_vesta", type=Path)
    parser.add_argument("--vmin", type=float, default=None)
    parser.add_argument("--vmax", type=float, default=None)
    parser.add_argument("--center", type=float, default=0.0)
    parser.add_argument("--section-index", type=int, default=0, help="Zero-based STRUC/SITET section index")
    parser.add_argument("--non-strict", action="store_true", help="Allow partial values and leave other sites unchanged")
    args = parser.parse_args(argv)

    values = read_site_values_table(args.values_table)
    patch_vesta_atom_colors_file(
        args.input_vesta,
        values,
        args.output_vesta,
        vmin=args.vmin,
        vmax=args.vmax,
        center=args.center,
        section_index=args.section_index,
        strict=not args.non_strict,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
