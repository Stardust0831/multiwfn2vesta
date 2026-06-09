"""Patch AIM overlay styles in VESTA multi-phase files.

This module is intended for VESTA files produced by importing an AIM
atoms-only phase over a real structure/cube phase.  It keeps AIM path sample
points as explicit sites, avoids AIM bonds by default, and can assign BCPs to
a distinct pseudo-element so they remain visible even when they coincide with
path sample points.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Sequence, Tuple


DEFAULT_PATH_ELEMENT = "Xe"
DEFAULT_BCP_ELEMENT = "Rn"
DEFAULT_PATH_RADIUS = 0.055
DEFAULT_BCP_RADIUS = 0.180
DEFAULT_PATH_RGB = (255, 230, 0)
DEFAULT_BCP_RGB = (255, 80, 0)

PHASE_HEADERS = {"CRYSTAL", "MOLECULE"}
TAIL_HEADERS = {"ATOMT", "SCENE", "HBOND", "STYLE"}


def _line_ending(reference: str, default: str) -> str:
    if reference.endswith("\r\n"):
        return "\r\n"
    if reference.endswith("\n"):
        return "\n"
    return default


def _is_path_label(label: str) -> bool:
    return label.startswith("P") and "_" in label


def _is_bcp_label(label: str) -> bool:
    return label.startswith("CP") and label.endswith("_N")


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
) -> str:
    r, g, b = rgb
    return (
        f"{index:4d} {label:>12s}  {radius:6.4f}"
        f" {r:3d} {g:3d} {b:3d} {r:3d} {g:3d} {b:3d} 204  0{newline}"
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
        if len(fields) >= 3 and (_is_path_label(fields[2]) or fields[2].startswith("CP")):
            return True
    return False


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
) -> str:
    """Return VESTA text with AIM path and BCP display styles patched.

    Path samples are never removed.  If a BCP sits exactly on top of a path
    point, the BCP is made distinguishable by its own element type and style.
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
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
