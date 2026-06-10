"""Color VESTA atoms from generic Multiwfn-style atom scalar tables."""

from __future__ import annotations

import argparse
import csv
import io
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union

from .vesta_atom_coloring import ValueKey, parse_structure_sites, patch_vesta_atom_colors_file
from .vesta_parser import parse_vesta_text


INDEX_ALIASES = (
    "index",
    "idx",
    "id",
    "no",
    "num",
    "number",
    "serial",
    "site",
    "site_index",
    "atom_index",
    "atom",
    "atoms",
    "atomid",
    "atom_id",
    "iatom",
    "iatm",
)
INDEX_ALIAS_SET = set(INDEX_ALIASES)

LABEL_ALIASES = (
    "label",
    "name",
    "atom_label",
    "site_label",
    "atom_name",
    "site_name",
    "element",
    "elem",
    "symbol",
)
LABEL_ALIAS_SET = set(LABEL_ALIASES)

VALUE_ALIASES = (
    "value",
    "scalar",
    "charge",
    "q",
    "population",
    "pop",
    "mulliken",
    "hirshfeld",
    "adch",
    "cm5",
    "fukui",
    "fukui_plus",
    "fukui_minus",
    "dual",
    "contribution",
    "weight",
    "percent",
)
VALUE_ALIAS_SET = set(VALUE_ALIASES)
HEADER_HINTS = INDEX_ALIAS_SET | LABEL_ALIAS_SET | VALUE_ALIAS_SET | {"atom", "atoms"}


@dataclass
class AtomScalarTable:
    """Parsed atom scalar values ready for VESTA site coloring."""

    values: Union[List[float], Dict[ValueKey, float]]
    rows: List[Tuple[Optional[int], Optional[str], float]]
    key_mode: str
    value_column: Optional[str] = None
    key_column: Optional[str] = None

    def value_count(self) -> int:
        return len(self.rows)


def _normalize_name(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def _safe_int(text: str) -> Optional[int]:
    try:
        if re.fullmatch(r"[-+]?\d+", text.strip()):
            return int(text)
    except ValueError:
        return None
    return None


def _safe_float(text: str) -> Optional[float]:
    try:
        return float(text)
    except ValueError:
        return None


def _is_float_text(text: str) -> bool:
    return _safe_float(text) is not None


def _strip_inline_comment(line: str) -> str:
    stripped = line.lstrip()
    if stripped.startswith("#"):
        return ""
    # Keep hashes inside CSV fields out of scope; Multiwfn text tables use
    # comments/separators rather than quoted comment characters.
    return line.split("#", 1)[0].strip()


def _split_whitespace_rows(text: str) -> List[List[str]]:
    rows: List[List[str]] = []
    for raw_line in text.splitlines():
        line = _strip_inline_comment(raw_line)
        if not line:
            continue
        if re.fullmatch(r"[-=*_ ]+", line):
            continue
        rows.append(line.split())
    return rows


def _read_rows(text: str) -> List[List[str]]:
    cleaned_lines: List[str] = []
    for raw_line in text.splitlines():
        line = _strip_inline_comment(raw_line)
        if not line:
            continue
        if re.fullmatch(r"[-=*_ ,\t]+", line):
            continue
        cleaned_lines.append(line)
    content = "\n".join(cleaned_lines)
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


def _looks_like_header(row: Sequence[str]) -> bool:
    normalized = [_normalize_name(cell) for cell in row]
    if any(name in HEADER_HINTS for name in normalized):
        return True
    return not any(_is_float_text(cell) for cell in row)


def _find_named_column(header: Sequence[str], names: Iterable[str], requested: Optional[str] = None) -> Optional[int]:
    normalized = [_normalize_name(cell) for cell in header]
    if requested:
        target = _normalize_name(requested)
        if target in normalized:
            return normalized.index(target)
        raise ValueError(f"Column {requested!r} was not found in table header: {', '.join(header)}")
    for name in names:
        if name in normalized:
            return normalized.index(name)
    return None


def _find_value_column(header: Sequence[str], requested: Optional[str] = None) -> Optional[int]:
    normalized = [_normalize_name(cell) for cell in header]
    if requested:
        target = _normalize_name(requested)
        if target in normalized:
            return normalized.index(target)
        raise ValueError(f"Column {requested!r} was not found in table header: {', '.join(header)}")

    matches = [index for index, name in enumerate(normalized) if name in VALUE_ALIAS_SET]
    if len(matches) > 1:
        columns = ", ".join(header[index] for index in matches)
        raise ValueError(
            "Multiple possible value columns were found "
            f"({columns}); pass --value-column to choose one."
        )
    if matches:
        return matches[0]
    return None


def _last_numeric_column(rows: Sequence[Sequence[str]], *, skip: Iterable[int] = ()) -> int:
    if not rows:
        raise ValueError("No data rows were found")
    skip_set = set(skip)
    max_cols = max(len(row) for row in rows)
    candidates: List[int] = []
    for column in range(max_cols):
        if column in skip_set:
            continue
        ok = True
        seen = False
        for row in rows:
            if column >= len(row) or not row[column]:
                ok = False
                break
            if _safe_float(row[column]) is None:
                ok = False
                break
            seen = True
        if ok and seen:
            candidates.append(column)
    if not candidates:
        raise ValueError("Could not infer a numeric value column; pass --value-column")
    return candidates[-1]


def _row_cell(row: Sequence[str], column: int, role: str) -> str:
    if column >= len(row):
        raise ValueError(f"Missing {role} column in row: {row}")
    value = row[column].strip()
    if not value:
        raise ValueError(f"Empty {role} column in row: {row}")
    return value


def _parse_headered_table(
    header: Sequence[str],
    data: Sequence[Sequence[str]],
    *,
    value_column: Optional[str],
    key_column: Optional[str],
) -> AtomScalarTable:
    if not data:
        raise ValueError("Atom scalar table has a header but no data rows")
    value_col = _find_value_column(header, requested=value_column)
    key_col: Optional[int] = None
    label_col = _find_named_column(header, LABEL_ALIASES)
    key_kind = "ordered"
    if key_column:
        key_col = _find_named_column(header, set(header), requested=key_column)
        normalized_key = _normalize_name(header[key_col])
        key_kind = "index" if normalized_key in INDEX_ALIAS_SET else "label"
    else:
        index_col = _find_named_column(header, INDEX_ALIASES)
        if index_col is not None:
            key_col = index_col
            key_kind = "index"
        elif label_col is not None:
            key_col = label_col
            key_kind = "label"
    if value_col is None:
        skip = [column for column in [key_col] if column is not None]
        value_col = _last_numeric_column(data, skip=skip)

    rows: List[Tuple[Optional[int], Optional[str], float]] = []
    values: Union[List[float], Dict[ValueKey, float]]
    if key_col is None:
        ordered: List[float] = []
        for row in data:
            value = float(_row_cell(row, value_col, "value"))
            ordered.append(value)
            rows.append((None, None, value))
        values = ordered
    else:
        mapped: Dict[ValueKey, float] = {}
        for row in data:
            key_text = _row_cell(row, key_col, "key")
            value = float(_row_cell(row, value_col, "value"))
            if key_kind == "index":
                index = _safe_int(key_text)
                if index is None:
                    raise ValueError(f"Expected integer atom index, got {key_text!r}")
                mapped[index] = value
                label = row[label_col] if label_col is not None and label_col < len(row) and row[label_col] else None
                rows.append((index, label, value))
            else:
                mapped[key_text] = value
                rows.append((None, key_text, value))
        values = mapped
    return AtomScalarTable(
        values=values,
        rows=rows,
        key_mode=key_kind,
        value_column=header[value_col] if value_col < len(header) else str(value_col),
        key_column=header[key_col] if key_col is not None and key_col < len(header) else None,
    )


def _parse_unheadered_table(
    rows_in: Sequence[Sequence[str]],
    *,
    value_column: Optional[str],
    key_column: Optional[str],
) -> AtomScalarTable:
    if value_column is not None or key_column is not None:
        raise ValueError("--value-column/--key-column require a header row")
    if not rows_in:
        raise ValueError("No atom scalar table rows were found")
    if all(len(row) == 1 for row in rows_in):
        ordered = [float(row[0]) for row in rows_in]
        return AtomScalarTable(
            values=ordered,
            rows=[(None, None, value) for value in ordered],
            key_mode="ordered",
        )

    if all(len(row) >= 2 for row in rows_in):
        mapped: Dict[ValueKey, float] = {}
        parsed_rows: List[Tuple[Optional[int], Optional[str], float]] = []
        first_column_indices = [_safe_int(row[0]) for row in rows_in]
        if all(index is not None for index in first_column_indices):
            value_col = 1 if all(len(row) == 2 for row in rows_in) else _last_numeric_column(rows_in, skip=[0])
            for row, index in zip(rows_in, first_column_indices):
                assert index is not None
                value = float(_row_cell(row, value_col, "value"))
                mapped[index] = value
                label = row[1] if value_col != 1 and len(row) > 1 else None
                parsed_rows.append((index, label, value))
            return AtomScalarTable(values=mapped, rows=parsed_rows, key_mode="index")

        if all(_safe_int(row[0]) is None for row in rows_in):
            value_col = 1 if all(len(row) == 2 for row in rows_in) else _last_numeric_column(rows_in, skip=[0])
            for row in rows_in:
                label = row[0]
                value = float(_row_cell(row, value_col, "value"))
                mapped[label] = value
                parsed_rows.append((None, label, value))
            return AtomScalarTable(values=mapped, rows=parsed_rows, key_mode="label")

    raise ValueError("Could not infer atom scalar table shape; add a header row and use --value-column")


def parse_multiwfn_atom_table_text(
    text: str,
    *,
    value_column: Optional[str] = None,
    key_column: Optional[str] = None,
) -> AtomScalarTable:
    """Parse Multiwfn-style per-atom scalar values.

    This intentionally accepts generic atom tables rather than one brittle
    Multiwfn menu transcript.  Multiwfn output copied to CSV/TSV/whitespace
    text, or hand-prepared atom scalar tables, can be keyed by atom index,
    keyed by VESTA site label, or ordered in VESTA ``STRUC`` order.
    """

    rows = _read_rows(text)
    if not rows:
        raise ValueError("No atom scalar values were found")
    if _looks_like_header(rows[0]):
        return _parse_headered_table(
            rows[0],
            rows[1:],
            value_column=value_column,
            key_column=key_column,
        )
    return _parse_unheadered_table(rows, value_column=value_column, key_column=key_column)


def read_multiwfn_atom_table(
    path: Path,
    *,
    value_column: Optional[str] = None,
    key_column: Optional[str] = None,
) -> AtomScalarTable:
    return parse_multiwfn_atom_table_text(
        path.read_text(encoding="utf-8", errors="replace"),
        value_column=value_column,
        key_column=key_column,
    )


def _read_vesta_site_count(input_vesta: Path, section_index: int) -> int:
    document = parse_vesta_text(input_vesta.read_text(encoding="utf-8", errors="replace"))
    struc_sections = document.sections_named("STRUC")
    if section_index < 0:
        raise ValueError("section_index must be non-negative")
    if section_index >= len(struc_sections):
        raise ValueError(f"STRUC section index {section_index} is out of range")
    return len(parse_structure_sites(struc_sections[section_index]))


def _read_vesta_site_keys(input_vesta: Path, section_index: int) -> Tuple[List[int], List[str]]:
    document = parse_vesta_text(input_vesta.read_text(encoding="utf-8", errors="replace"))
    struc_sections = document.sections_named("STRUC")
    if section_index < 0:
        raise ValueError("section_index must be non-negative")
    if section_index >= len(struc_sections):
        raise ValueError(f"STRUC section index {section_index} is out of range")
    sites = parse_structure_sites(struc_sections[section_index])
    return [site.index for site in sites], [site.label for site in sites]


def _format_list(items: Sequence[object], limit: int = 12) -> str:
    shown = ", ".join(str(item) for item in items[:limit])
    if len(items) > limit:
        shown += f", ... ({len(items)} total)"
    return f"[{shown}]"


def _duplicates(items: Sequence[object]) -> List[object]:
    seen = set()
    duplicates: List[object] = []
    for item in items:
        if item in seen and item not in duplicates:
            duplicates.append(item)
        seen.add(item)
    return duplicates


def validate_table_for_vesta(input_vesta: Path, table: AtomScalarTable, section_index: int) -> None:
    """Require strict atom tables to match the selected VESTA structure."""

    site_indices, site_labels = _read_vesta_site_keys(input_vesta, section_index)
    if table.key_mode == "ordered":
        site_count = len(site_indices)
        if table.value_count() != site_count:
            raise ValueError(
                "Strict Multiwfn atom table coloring requires ordered table length "
                f"to match VESTA STRUC site count; section {section_index} has "
                f"{site_count} sites, table has {table.value_count()} rows. "
                "Use --non-strict only if intentionally coloring the first subset."
            )
        return

    if table.key_mode == "index":
        table_indices = [index for index, _label, _value in table.rows if index is not None]
        duplicate_indices = _duplicates(table_indices)
        if duplicate_indices:
            raise ValueError(f"Strict Multiwfn atom table coloring found duplicate atom indices: {_format_list(duplicate_indices)}")
        missing = sorted(set(site_indices) - set(table_indices))
        surplus = sorted(set(table_indices) - set(site_indices))
        if missing or surplus:
            raise ValueError(
                "Strict Multiwfn atom table coloring requires table atom indices "
                "to match VESTA STRUC site indices exactly; "
                f"VESTA section {section_index} has {_format_list(site_indices)}, "
                f"table has {_format_list(table_indices)}; "
                f"missing {_format_list(missing)}, surplus {_format_list(surplus)}. "
                "Use --non-strict only if intentionally coloring a subset."
            )
        return

    if table.key_mode == "label":
        table_labels = [label for _index, label, _value in table.rows if label is not None]
        duplicate_labels = _duplicates(table_labels)
        if duplicate_labels:
            raise ValueError(f"Strict Multiwfn atom table coloring found duplicate labels: {_format_list(duplicate_labels)}")
        missing = sorted(set(site_labels) - set(table_labels))
        surplus = sorted(set(table_labels) - set(site_labels))
        if missing or surplus:
            raise ValueError(
                "Strict Multiwfn atom table coloring requires table labels "
                "to match VESTA STRUC site labels exactly; "
                f"VESTA section {section_index} has {_format_list(site_labels)}, "
                f"table has {_format_list(table_labels)}; "
                f"missing {_format_list(missing)}, surplus {_format_list(surplus)}. "
                "Use --non-strict only if intentionally coloring a subset."
            )
        return

    raise ValueError(f"Unknown atom table key mode: {table.key_mode}")


def validate_ordered_table_for_vesta(input_vesta: Path, table: AtomScalarTable, section_index: int) -> None:
    """Backward-compatible wrapper for older callers."""

    if table.key_mode == "ordered":
        site_count = _read_vesta_site_count(input_vesta, section_index)
        if table.value_count() != site_count:
            raise ValueError(
                "Strict Multiwfn atom table coloring requires ordered table length "
                f"to match VESTA STRUC site count; section {section_index} has "
                f"{site_count} sites, table has {table.value_count()} rows. "
                "Use --non-strict only if intentionally coloring the first subset."
            )


def write_values_csv(path: Path, table: AtomScalarTable) -> None:
    lines = ["index,label,value\n"]
    for index, label, value in table.rows:
        lines.append(
            "%s,%s,%.12g\n"
            % (
                "" if index is None else index,
                "" if label is None else label,
                value,
            )
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines), encoding="utf-8")


def color_vesta_from_multiwfn_atom_table(
    input_vesta: Path,
    atom_table: Path,
    output_vesta: Path,
    *,
    value_column: Optional[str] = None,
    key_column: Optional[str] = None,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    center: float = 0.0,
    section_index: int = 0,
    strict: bool = True,
    values_csv: Optional[Path] = None,
) -> AtomScalarTable:
    table = read_multiwfn_atom_table(atom_table, value_column=value_column, key_column=key_column)
    if strict:
        validate_table_for_vesta(input_vesta, table, section_index)
    patch_vesta_atom_colors_file(
        input_vesta,
        table.values,
        output_vesta,
        vmin=vmin,
        vmax=vmax,
        center=center,
        section_index=section_index,
        strict=strict,
    )
    if values_csv is not None:
        write_values_csv(values_csv, table)
    return table


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Color VESTA atoms from a generic Multiwfn-style atom scalar table."
    )
    parser.add_argument("input_vesta", type=Path)
    parser.add_argument("atom_table", type=Path, help="CSV/TSV/whitespace atom scalar table")
    parser.add_argument("output_vesta", type=Path)
    parser.add_argument("--value-column", help="Header column containing the scalar value")
    parser.add_argument("--key-column", help="Header column containing VESTA site label or one-based atom index")
    parser.add_argument("--vmin", type=float, default=None)
    parser.add_argument("--vmax", type=float, default=None)
    parser.add_argument("--center", type=float, default=0.0)
    parser.add_argument("--section-index", type=int, default=0, help="Zero-based STRUC/SITET section index")
    parser.add_argument("--non-strict", action="store_true", help="Allow partial values and leave other sites unchanged")
    parser.add_argument("--write-values", type=Path, help="Optional normalized CSV file with parsed values")
    args = parser.parse_args(argv)

    table = color_vesta_from_multiwfn_atom_table(
        args.input_vesta,
        args.atom_table,
        args.output_vesta,
        value_column=args.value_column,
        key_column=args.key_column,
        vmin=args.vmin,
        vmax=args.vmax,
        center=args.center,
        section_index=args.section_index,
        strict=not args.non_strict,
        values_csv=args.write_values,
    )
    print(args.output_vesta)
    print(f"colored {table.value_count()} atom values from {args.atom_table} ({table.key_mode})")
    if args.write_values is not None:
        print(args.write_values)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
