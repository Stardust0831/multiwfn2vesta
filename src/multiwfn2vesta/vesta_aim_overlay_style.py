"""Patch AIM overlay styles in VESTA multi-phase files.

This module is intended for VESTA files produced by importing an AIM
atoms-only phase over a real structure/cube phase.  It keeps AIM path sample
points as explicit sites, avoids AIM bonds by default, and can assign BCPs to
a distinct pseudo-element.  Optionally BCP sites can be moved into a final
dedicated phase so VESTA draws them after the path-point phase.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Sequence, Tuple


DEFAULT_PATH_ELEMENT = "Xe"
DEFAULT_BCP_ELEMENT = "Rn"
DEFAULT_PATH_RADIUS = 0.060
DEFAULT_BCP_RADIUS = 0.180
DEFAULT_PATH_RGB = (255, 230, 0)
DEFAULT_BCP_RGB = (255, 80, 0)

PHASE_HEADERS = {"CRYSTAL", "MOLECULE"}
TAIL_HEADERS = {"ATOMT", "SCENE", "HBOND", "STYLE"}
SECTION_HEADERS = {
    "STRUC",
    "THERI",
    "SHAPE",
    "BOUND",
    "SBOND",
    "SITET",
    "VECTR",
    "VECTT",
    "SPLAN",
    "LBLAT",
    "LBLSP",
    "DLATM",
    "DLBND",
    "DLPLY",
    "PLN2D",
    "ATOMT",
    "SCENE",
    "HBOND",
    "STYLE",
}


def _line_ending(reference: str, default: str) -> str:
    if reference.endswith("\r\n"):
        return "\r\n"
    if reference.endswith("\n"):
        return "\n"
    return default


def _is_path_label(label: str) -> bool:
    return label.startswith("P") and "_" in label


def _is_bcp_label(label: str) -> bool:
    return (label.startswith("CP") and label.endswith("_N")) or (
        label.startswith("BCP") and label[3:].isdigit()
    )


def _format_struc_line(
    index: int,
    element: str,
    label: str,
    occupancy: float,
    x: float,
    y: float,
    z: float,
    suffix: str,
    newline: str,
) -> str:
    return (
        f"{index:4d}  {element:<2s}        {label:<12s} {occupancy:6.4f}"
        f" {x:10.6f} {y:10.6f} {z:10.6f}{suffix}{newline}"
    )


def _format_sitet_line(
    index: int,
    label: str,
    radius: float,
    rgb: Tuple[int, int, int],
    newline: str,
    show_label: int = 0,
) -> str:
    r, g, b = rgb
    return (
        f"{index:4d} {label:>12s}  {radius:6.4f}"
        f" {r:3d} {g:3d} {b:3d} {r:3d} {g:3d} {b:3d} 204  {show_label:d}{newline}"
    )


def _format_atomt_line(
    index: int,
    element: str,
    radius: float,
    rgb: Tuple[int, int, int],
    newline: str,
) -> str:
    r, g, b = rgb
    return (
        f"{index:3d} {element:>10s} {radius:7.4f}"
        f" {r:3d} {g:3d} {b:3d} {r:3d} {g:3d} {b:3d} 204{newline}"
    )


def _format_theri_line(index: int, label: str, value: str, newline: str) -> str:
    return f"{index:4d} {label:>12s} {value}{newline}"


def _format_label_line(mode: int, font_size: float, offset: float, mark: int, newline: str) -> str:
    return f"LABEL {mode:d} {font_size:5g} {offset:6.3f} {mark:d}{newline}"


def _blank_displacement_line(newline: str) -> str:
    return f"                            0.000000   0.000000   0.000000  0.00{newline}"


def _phase_starts(lines: List[str]) -> List[int]:
    return [idx for idx, line in enumerate(lines) if line.strip() in PHASE_HEADERS]


def _global_tail_start(lines: List[str], phase_start: int) -> int:
    for idx in range(phase_start + 1, len(lines)):
        if lines[idx].strip() in TAIL_HEADERS:
            return idx
    return len(lines)


def _phase_contains_aim_labels(lines: List[str], start: int, end: int) -> bool:
    for line in lines[start:end]:
        fields = line.split()
        if len(fields) >= 3 and (_is_path_label(fields[2]) or _is_bcp_label(fields[2])):
            return True
    return False


def _phase_contains_path_and_bcp(lines: List[str], start: int, end: int) -> bool:
    has_path = False
    has_bcp = False
    for line in lines[start:end]:
        fields = line.split()
        if len(fields) >= 3:
            has_path = has_path or _is_path_label(fields[2])
            has_bcp = has_bcp or _is_bcp_label(fields[2])
    return has_path and has_bcp


def _aim_phase_ranges(lines: List[str]) -> List[Tuple[int, int]]:
    starts = _phase_starts(lines)
    ranges: List[Tuple[int, int]] = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else _global_tail_start(lines, start)
        if _phase_contains_aim_labels(lines, start, end):
            ranges.append((start, end))
    return ranges


def _patch_structure_and_sitet(
    lines: List[str],
    start: int,
    end: int,
    *,
    path_element: str,
    bcp_element: str,
    path_radius: float,
    bcp_radius: float,
    path_rgb: Tuple[int, int, int],
    bcp_rgb: Tuple[int, int, int],
    default_newline: str,
) -> List[str]:
    out = list(lines)
    for idx in range(start, end):
        fields = out[idx].split()
        newline = _line_ending(out[idx], default_newline)
        if len(fields) >= 9 and (_is_path_label(fields[2]) or _is_bcp_label(fields[2])):
            element = path_element if _is_path_label(fields[2]) else bcp_element
            suffix = "    1a     1" if fields[-1] != "-" else "    1        -"
            out[idx] = _format_struc_line(
                int(fields[0]),
                element,
                fields[2],
                float(fields[3]),
                float(fields[4]),
                float(fields[5]),
                float(fields[6]),
                suffix,
                newline,
            )
        elif len(fields) >= 11 and (_is_path_label(fields[1]) or _is_bcp_label(fields[1])):
            radius = path_radius if _is_path_label(fields[1]) else bcp_radius
            rgb = path_rgb if _is_path_label(fields[1]) else bcp_rgb
            out[idx] = _format_sitet_line(int(fields[0]), fields[1], radius, rgb, newline)
    return out


def _replace_sbond_with_empty(lines: List[str], start: int, end: int, default_newline: str) -> List[str]:
    sbond = -1
    for idx in range(start, end):
        if lines[idx].strip() == "SBOND":
            sbond = idx
            break
    if sbond < 0:
        return lines

    terminator = sbond + 1
    while terminator < len(lines):
        if lines[terminator].strip().startswith("0 0 0 0"):
            terminator += 1
            break
        terminator += 1
    newline = _line_ending(lines[sbond], default_newline)
    replacement = [f"SBOND{newline}", f"  0 0 0 0{newline}"]
    return lines[:sbond] + replacement + lines[terminator:]


def _patch_global_atomt(
    lines: List[str],
    *,
    path_element: str,
    bcp_element: str,
    path_radius: float,
    bcp_radius: float,
    path_rgb: Tuple[int, int, int],
    bcp_rgb: Tuple[int, int, int],
    default_newline: str,
) -> List[str]:
    atomt = -1
    for idx, line in enumerate(lines):
        if line.strip() == "ATOMT":
            atomt = idx
    if atomt < 0:
        return lines

    end = atomt + 1
    max_index = 0
    existing = set()
    while end < len(lines):
        if lines[end].strip() == "0 0 0 0 0 0":
            break
        fields = lines[end].split()
        if len(fields) >= 2:
            try:
                max_index = max(max_index, int(fields[0]))
                existing.add(fields[1])
            except ValueError:
                pass
        end += 1
    if end >= len(lines):
        return lines

    patched = list(lines)
    target_styles = {
        path_element: (path_radius, path_rgb),
        bcp_element: (bcp_radius, bcp_rgb),
    }
    for idx in range(atomt + 1, end):
        fields = patched[idx].split()
        if len(fields) >= 10 and fields[1] in target_styles:
            radius, rgb = target_styles[fields[1]]
            patched[idx] = _format_atomt_line(
                int(fields[0]),
                fields[1],
                radius,
                rgb,
                _line_ending(patched[idx], default_newline),
            )

    additions: List[str] = []
    newline = _line_ending(lines[end], default_newline)
    next_index = max_index + 1
    for element, (radius, rgb) in target_styles.items():
        if element in existing:
            continue
        additions.append(_format_atomt_line(next_index, element, radius, rgb, newline))
        next_index += 1
    return patched[:end] + additions + patched[end:]


def _patch_global_bonds(lines: List[str], enabled: bool) -> List[str]:
    out = list(lines)
    value = "1" if enabled else "0"
    for idx, line in enumerate(out):
        if line.strip().startswith("BONDS"):
            newline = _line_ending(line, "\n")
            out[idx] = f"BONDS   {value}{newline}"
    return out


def _patch_global_label_style(
    lines: List[str],
    *,
    mode: int,
    font_size: float,
    offset: float,
    mark: int,
    default_newline: str,
) -> List[str]:
    out = list(lines)
    changed = False
    for idx, line in enumerate(out):
        fields = line.split()
        if fields[:1] == ["LABEL"] and len(fields) >= 5:
            out[idx] = _format_label_line(mode, font_size, offset, mark, _line_ending(line, default_newline))
            changed = True
    if not changed:
        insert_at = len(out)
        in_style = False
        for idx, line in enumerate(out):
            stripped = line.strip()
            if stripped == "STYLE":
                in_style = True
            elif in_style and stripped.split()[0:1] in (["PROJT"], ["BKGRC"], ["DPTHQ"], ["LIGHT0"], ["LIGHT1"]):
                insert_at = idx
                break
        out.insert(insert_at, _format_label_line(mode, font_size, offset, mark, default_newline))
    return out


def _patch_bcp_site_labels(
    lines: List[str],
    *,
    prefix: str,
    default_newline: str,
) -> List[str]:
    out = list(lines)
    counter = 1
    for start, end in _aim_phase_ranges(out):
        label_map: dict[str, str] = {}
        for idx in range(start, end):
            fields = out[idx].split()
            if len(fields) < 9 or not _is_bcp_label(fields[2]):
                continue
            old_label = fields[2]
            new_label = f"{prefix}{counter}"
            counter += 1
            label_map[old_label] = new_label
            suffix = "    1a     1" if fields[-1] != "-" else "    1        -"
            out[idx] = _format_struc_line(
                int(fields[0]),
                fields[1],
                new_label,
                float(fields[3]),
                float(fields[4]),
                float(fields[5]),
                float(fields[6]),
                suffix,
                _line_ending(out[idx], default_newline),
            )

        if not label_map:
            continue

        for idx in range(start, end):
            fields = out[idx].split()
            if len(fields) >= 11 and fields[1] in label_map:
                try:
                    out[idx] = _format_sitet_line(
                        int(fields[0]),
                        label_map[fields[1]],
                        float(fields[2]),
                        (int(fields[3]), int(fields[4]), int(fields[5])),
                        _line_ending(out[idx], default_newline),
                        show_label=1,
                    )
                except ValueError:
                    pass
            elif len(fields) >= 3 and fields[1] in label_map:
                out[idx] = _format_theri_line(
                    int(fields[0]),
                    label_map[fields[1]],
                    fields[2],
                    _line_ending(out[idx], default_newline),
                )
    return out


def _find_section(lines: List[str], start: int, end: int, section: str) -> int:
    for idx in range(start, end):
        if lines[idx].strip().split()[0:1] == [section]:
            return idx
    return -1


def _find_sentinel(lines: List[str], start: int, end: int, prefix: str) -> int:
    for idx in range(start, end):
        if lines[idx].strip().startswith(prefix):
            return idx
    return -1


def _is_section_or_sentinel(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    first = stripped.split()[0]
    return first in SECTION_HEADERS or stripped.startswith("0 0 0")


def _replace_title_line(phase_header: List[str], title: str, default_newline: str) -> List[str]:
    out = list(phase_header)
    for idx, line in enumerate(out[:-1]):
        if line.strip() == "TITLE":
            title_idx = idx + 1
            while title_idx < len(out) and not out[title_idx].strip():
                title_idx += 1
            if title_idx < len(out):
                out[title_idx] = title + _line_ending(out[title_idx], default_newline)
            break
    return out


def _split_bcp_phase_once(
    lines: List[str],
    start: int,
    end: int,
    *,
    bcp_element: str,
    bcp_radius: float,
    bcp_rgb: Tuple[int, int, int],
    default_newline: str,
) -> List[str]:
    struc = _find_section(lines, start, end, "STRUC")
    theri = _find_section(lines, start, end, "THERI")
    shape = _find_section(lines, start, end, "SHAPE")
    sbond = _find_section(lines, start, end, "SBOND")
    sitet = _find_section(lines, start, end, "SITET")
    if min(struc, theri, shape, sbond, sitet) < 0:
        return lines

    struc_end = _find_sentinel(lines, struc + 1, end, "0 0 0 0 0 0 0")
    theri_end = _find_sentinel(lines, theri + 1, end, "0 0 0")
    sitet_end = _find_sentinel(lines, sitet + 1, end, "0 0 0 0 0 0")
    if min(struc_end, theri_end, sitet_end) < 0:
        return lines

    kept_struc: List[Tuple[str, str]] = []
    bcp_struc: List[Tuple[str, str]] = []
    idx = struc + 1
    while idx < struc_end:
        line = lines[idx]
        fields = line.split()
        if len(fields) >= 9 and (_is_path_label(fields[2]) or _is_bcp_label(fields[2])):
            newline = _line_ending(line, default_newline)
            disp = _blank_displacement_line(newline)
            next_idx = idx + 1
            if next_idx < struc_end and not _is_section_or_sentinel(lines[next_idx]):
                disp = lines[next_idx]
                next_idx += 1
            label = fields[2]
            suffix = "    1a     1" if fields[-1] != "-" else "    1        -"
            record = (
                fields[1],
                label,
                float(fields[3]),
                float(fields[4]),
                float(fields[5]),
                float(fields[6]),
                suffix,
                newline,
                disp,
            )
            if _is_bcp_label(label):
                bcp_struc.append(record)
            else:
                kept_struc.append(record)
            idx = next_idx
        else:
            kept_struc.append(("__RAW__", line, 0.0, 0.0, 0.0, 0.0, "", _line_ending(line, default_newline), ""))
            idx += 1

    if not bcp_struc:
        return lines

    kept_labels: List[str] = [record[1] for record in kept_struc if record[0] != "__RAW__"]
    bcp_labels: List[str] = [record[1] for record in bcp_struc]
    kept_index = {label: idx + 1 for idx, label in enumerate(kept_labels)}
    bcp_index = {label: idx + 1 for idx, label in enumerate(bcp_labels)}

    def render_struc(records: List[Tuple[str, str, float, float, float, float, str, str, str]], bcp: bool) -> List[str]:
        rendered: List[str] = []
        for record in records:
            element, label, occupancy, x, y, z, suffix, newline, disp = record
            if element == "__RAW__":
                rendered.append(label)
                continue
            index = bcp_index[label] if bcp else kept_index[label]
            rendered.append(
                _format_struc_line(
                    index,
                    bcp_element if bcp else element,
                    label,
                    occupancy,
                    x,
                    y,
                    z,
                    suffix,
                    newline,
                )
            )
            rendered.append(disp)
        return rendered

    def render_theri(labels: List[str], mapping: dict[str, int]) -> List[str]:
        values: dict[str, Tuple[str, str]] = {}
        for line in lines[theri + 1 : theri_end]:
            fields = line.split()
            if len(fields) >= 3:
                values[fields[1]] = (fields[2], _line_ending(line, default_newline))
        rendered: List[str] = []
        for label in labels:
            value, newline = values.get(label, ("-0.000000", default_newline))
            rendered.append(_format_theri_line(mapping[label], label, value, newline))
        return rendered

    def render_sitet(labels: List[str], mapping: dict[str, int], bcp: bool) -> List[str]:
        styles: dict[str, Tuple[float, Tuple[int, int, int], str]] = {}
        for line in lines[sitet + 1 : sitet_end]:
            fields = line.split()
            if len(fields) >= 6:
                try:
                    styles[fields[1]] = (
                        float(fields[2]),
                        (int(fields[3]), int(fields[4]), int(fields[5])),
                        _line_ending(line, default_newline),
                    )
                except ValueError:
                    pass
        rendered: List[str] = []
        for label in labels:
            radius, rgb, newline = styles.get(label, (bcp_radius, bcp_rgb, default_newline))
            if bcp:
                radius, rgb = bcp_radius, bcp_rgb
            rendered.append(_format_sitet_line(mapping[label], label, radius, rgb, newline))
        return rendered

    phase_header = lines[start : struc + 1]
    bcp_header = _replace_title_line(
        phase_header,
        "AIM BCP final overlay phase",
        default_newline,
    )
    struc_sentinel = lines[struc_end]
    theri_header = lines[theri]
    theri_sentinel = lines[theri_end]
    sitet_header = lines[sitet]
    sitet_sentinel = lines[sitet_end]

    original_phase = (
        phase_header
        + render_struc(kept_struc, False)
        + [struc_sentinel]
        + [theri_header]
        + render_theri(kept_labels, kept_index)
        + [theri_sentinel]
        + lines[shape:sbond]
        + [f"SBOND{_line_ending(lines[sbond], default_newline)}", f"  0 0 0 0{default_newline}"]
        + [sitet_header]
        + render_sitet(kept_labels, kept_index, False)
        + [sitet_sentinel]
        + lines[sitet_end + 1 : end]
    )
    bcp_phase = (
        bcp_header
        + render_struc(bcp_struc, True)
        + [struc_sentinel]
        + [theri_header]
        + render_theri(bcp_labels, bcp_index)
        + [theri_sentinel]
        + lines[shape:sbond]
        + [f"SBOND{_line_ending(lines[sbond], default_newline)}", f"  0 0 0 0{default_newline}"]
        + [sitet_header]
        + render_sitet(bcp_labels, bcp_index, True)
        + [sitet_sentinel]
        + lines[sitet_end + 1 : end]
    )
    return lines[:start] + original_phase + bcp_phase + lines[end:]


def _split_bcp_phases(
    lines: List[str],
    *,
    bcp_element: str,
    bcp_radius: float,
    bcp_rgb: Tuple[int, int, int],
    default_newline: str,
) -> List[str]:
    ranges = _aim_phase_ranges(lines)
    for start, end in reversed(ranges):
        if not _phase_contains_path_and_bcp(lines, start, end):
            continue
        lines = _split_bcp_phase_once(
            lines,
            start,
            end,
            bcp_element=bcp_element,
            bcp_radius=bcp_radius,
            bcp_rgb=bcp_rgb,
            default_newline=default_newline,
        )
    return lines


def patch_aim_overlay_style_text(
    text: str,
    *,
    path_element: str = DEFAULT_PATH_ELEMENT,
    bcp_element: str = DEFAULT_BCP_ELEMENT,
    path_radius: float = DEFAULT_PATH_RADIUS,
    bcp_radius: float = DEFAULT_BCP_RADIUS,
    path_rgb: Tuple[int, int, int] = DEFAULT_PATH_RGB,
    bcp_rgb: Tuple[int, int, int] = DEFAULT_BCP_RGB,
    clear_aim_sbond: bool = True,
    keep_structure_bonds: bool = True,
    split_bcp_phase: bool = False,
    label_bcp_sites: bool = False,
    bcp_label_prefix: str = "BCP",
    label_mode: int = 1,
    label_font_size: float = 12,
    label_offset: float = 1.000,
    label_mark: int = 0,
) -> str:
    """Return VESTA text with AIM path and BCP display styles patched.

    Path samples are never removed.  If a BCP sits exactly on top of a path
    point, the BCP is made distinguishable by its own element type and style.
    If ``label_bcp_sites`` is true, BCP site names are rewritten to concise
    labels such as ``BCP1`` and their per-site label flag is enabled.  VESTA's
    documented native label model can then display site names; no arbitrary
    text or non-empty ``LBLAT`` records are generated here.
    """

    default_newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines(keepends=True)
    ranges = _aim_phase_ranges(lines)
    if not ranges:
        raise ValueError("No AIM phase containing P*/CP* labels found")

    for start, end in reversed(ranges):
        lines = _patch_structure_and_sitet(
            lines,
            start,
            end,
            path_element=path_element,
            bcp_element=bcp_element,
            path_radius=path_radius,
            bcp_radius=bcp_radius,
            path_rgb=path_rgb,
            bcp_rgb=bcp_rgb,
            default_newline=default_newline,
        )
        if clear_aim_sbond:
            lines = _replace_sbond_with_empty(lines, start, end, default_newline)

    if split_bcp_phase:
        lines = _split_bcp_phases(
            lines,
            bcp_element=bcp_element,
            bcp_radius=bcp_radius,
            bcp_rgb=bcp_rgb,
            default_newline=default_newline,
        )

    if label_bcp_sites:
        lines = _patch_bcp_site_labels(
            lines,
            prefix=bcp_label_prefix,
            default_newline=default_newline,
        )
        lines = _patch_global_label_style(
            lines,
            mode=label_mode,
            font_size=label_font_size,
            offset=label_offset,
            mark=label_mark,
            default_newline=default_newline,
        )

    lines = _patch_global_atomt(
        lines,
        path_element=path_element,
        bcp_element=bcp_element,
        path_radius=path_radius,
        bcp_radius=bcp_radius,
        path_rgb=path_rgb,
        bcp_rgb=bcp_rgb,
        default_newline=default_newline,
    )
    lines = _patch_global_bonds(lines, keep_structure_bonds)
    return "".join(lines)


def patch_aim_overlay_style_file(input_vesta: Path, output_vesta: Path, **kwargs: object) -> None:
    text = input_vesta.read_text(encoding="utf-8", errors="replace")
    output_vesta.write_text(patch_aim_overlay_style_text(text, **kwargs), encoding="utf-8")


def _rgb_tuple(values: Sequence[int]) -> Tuple[int, int, int]:
    if len(values) != 3:
        raise ValueError("RGB values require exactly three integers")
    return int(values[0]), int(values[1]), int(values[2])


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Patch AIM overlay path/BCP styles in a VESTA file.")
    parser.add_argument("input_vesta", type=Path)
    parser.add_argument("output_vesta", type=Path)
    parser.add_argument("--path-element", default=DEFAULT_PATH_ELEMENT)
    parser.add_argument("--bcp-element", default=DEFAULT_BCP_ELEMENT)
    parser.add_argument("--path-radius", type=float, default=DEFAULT_PATH_RADIUS)
    parser.add_argument("--bcp-radius", type=float, default=DEFAULT_BCP_RADIUS)
    parser.add_argument("--path-rgb", nargs=3, type=int, default=DEFAULT_PATH_RGB)
    parser.add_argument("--bcp-rgb", nargs=3, type=int, default=DEFAULT_BCP_RGB)
    parser.add_argument("--keep-aim-sbond", action="store_true", help="Do not clear SBOND in AIM phases")
    parser.add_argument("--structure-bonds-off", action="store_true", help="Set global BONDS off")
    parser.add_argument(
        "--split-bcp-phase",
        action="store_true",
        help="Move BCP sites into a final dedicated phase while keeping all path samples",
    )
    parser.add_argument(
        "--label-bcp-sites",
        action="store_true",
        help="Rename BCP site labels to concise names and enable their native VESTA label flags",
    )
    parser.add_argument("--bcp-label-prefix", default="BCP")
    parser.add_argument("--label-mode", type=int, default=1)
    parser.add_argument("--label-font-size", type=float, default=12)
    parser.add_argument("--label-offset", type=float, default=1.000)
    parser.add_argument("--label-mark", type=int, default=0)
    args = parser.parse_args(argv)

    patch_aim_overlay_style_file(
        args.input_vesta,
        args.output_vesta,
        path_element=args.path_element,
        bcp_element=args.bcp_element,
        path_radius=args.path_radius,
        bcp_radius=args.bcp_radius,
        path_rgb=_rgb_tuple(args.path_rgb),
        bcp_rgb=_rgb_tuple(args.bcp_rgb),
        clear_aim_sbond=not args.keep_aim_sbond,
        keep_structure_bonds=not args.structure_bonds_off,
        split_bcp_phase=args.split_bcp_phase,
        label_bcp_sites=args.label_bcp_sites,
        bcp_label_prefix=args.bcp_label_prefix,
        label_mode=args.label_mode,
        label_font_size=args.label_font_size,
        label_offset=args.label_offset,
        label_mark=args.label_mark,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
