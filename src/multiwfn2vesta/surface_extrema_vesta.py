"""Overlay Multiwfn molecular-surface extrema on generated VESTA files."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, NamedTuple, Optional, Sequence, Tuple

from . import cube_vesta


RGB = Tuple[int, int, int]
Vector3 = Tuple[float, float, float]

DEFAULT_EXTREMA_RADIUS = 0.10
DEFAULT_MAXIMA_RGB: RGB = (255, 0, 0)
DEFAULT_MINIMA_RGB: RGB = (0, 0, 255)


@dataclass(frozen=True)
class SurfaceExtremum:
    serial: int
    kind: str
    source_element: str
    x: float
    y: float
    z: float
    value: Optional[float]
    label: str


class SurfaceExtremaPdb(NamedTuple):
    extrema: List[SurfaceExtremum]
    cell: Optional[Tuple[float, float, float, float, float, float]]
    value_unit: Optional[str]


class SurfaceExtremaOverlayResult(NamedTuple):
    vesta_path: Path
    extrema_count: int
    maxima_count: int
    minima_count: int
    selection: str
    value_unit: Optional[str]


def _safe_int(text: str, default: int = 0) -> int:
    text = text.strip()
    if not text:
        return default
    try:
        return int(text)
    except ValueError:
        return default


def _safe_float(text: str) -> Optional[float]:
    text = text.strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _parse_cryst1(line: str) -> Optional[Tuple[float, float, float, float, float, float]]:
    try:
        return (
            float(line[6:15]),
            float(line[15:24]),
            float(line[24:33]),
            float(line[33:40]),
            float(line[40:47]),
            float(line[47:54]),
        )
    except ValueError:
        return None


def _unit_from_remark(line: str) -> Optional[str]:
    lowered = line.lower()
    if "b-factor" not in lowered:
        return None
    if "kcal/mol" in lowered:
        return "kcal/mol"
    if "ev" in lowered:
        return "eV"
    if "a.u." in lowered or "au" in lowered:
        return "a.u."
    return None


def _parse_surface_atom_line(line: str) -> Optional[Tuple[int, str, Vector3, Optional[float]]]:
    record = line[:6].strip()
    if record not in {"ATOM", "HETATM"}:
        return None

    serial = _safe_int(line[6:11])
    element = (line[76:78].strip() or line[12:16].strip()[:2] or "").title()
    value = _safe_float(line[60:66]) if len(line) >= 66 else None
    try:
        x = float(line[30:38])
        y = float(line[38:46])
        z = float(line[46:54])
        return serial, element, (x, y, z), value
    except (ValueError, IndexError):
        pass

    fields = line.split()
    xyz = None
    xyz_start = -1
    for start in (6, 5, 3):
        if len(fields) >= start + 3:
            try:
                xyz = (float(fields[start]), float(fields[start + 1]), float(fields[start + 2]))
                xyz_start = start
                break
            except ValueError:
                pass
    if xyz is None:
        raise ValueError(f"Cannot parse surfanalysis PDB coordinate line: {line.rstrip()}") from None

    if not element:
        element = (fields[-1] if fields[-1].isalpha() else fields[2]).title()
    if value is None and xyz_start + 4 < len(fields):
        value = _safe_float(fields[xyz_start + 4])
    return _safe_int(fields[1]), element, xyz, value


def read_surfanalysis_pdb(path: Path) -> SurfaceExtremaPdb:
    """Read Multiwfn ``surfanalysis.pdb`` extrema.

    Multiwfn writes surface maxima as carbon records and minima as oxygen
    records.  The PDB B-factor field stores the mapped function value when
    Multiwfn has one available.
    """
    path = Path(path)
    extrema: List[SurfaceExtremum] = []
    cell = None
    value_unit = None
    maxima = 0
    minima = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("CRYST1"):
            cell = _parse_cryst1(line)
            continue
        if line.startswith("REMARK"):
            value_unit = _unit_from_remark(line) or value_unit
        parsed = _parse_surface_atom_line(line)
        if parsed is None:
            continue
        serial, element, coords, value = parsed
        code = element.upper()
        if code == "C":
            maxima += 1
            kind = "maximum"
            label = f"MAX{maxima:04d}"
        elif code == "O":
            minima += 1
            kind = "minimum"
            label = f"MIN{minima:04d}"
        else:
            continue
        extrema.append(
            SurfaceExtremum(
                serial=serial,
                kind=kind,
                source_element=code,
                x=coords[0],
                y=coords[1],
                z=coords[2],
                value=value,
                label=label,
            )
        )
    return SurfaceExtremaPdb(extrema=extrema, cell=cell, value_unit=value_unit)


def select_extrema(extrema: Sequence[SurfaceExtremum], selection: str) -> List[SurfaceExtremum]:
    if selection == "all":
        return list(extrema)
    if selection == "maxima":
        return [item for item in extrema if item.kind == "maximum"]
    if selection == "minima":
        return [item for item in extrema if item.kind == "minimum"]
    raise ValueError(f"Unknown surface extrema selection: {selection}")


def _validate_rgb(values: Sequence[int], label: str) -> RGB:
    if len(values) != 3:
        raise ValueError(f"{label} RGB requires exactly three values")
    rgb = tuple(int(value) for value in values)
    if any(value < 0 or value > 255 for value in rgb):
        raise ValueError(f"{label} RGB values must be in 0..255")
    return rgb  # type: ignore[return-value]


def _extrema_structure_mode(summary: cube_vesta.CubeSummary, requested: str) -> str:
    if requested != "auto":
        return requested
    return "crystal" if cube_vesta._structure_mode(summary, "auto") == "crystal" else "molecule"


def _site_coords(
    extremum: SurfaceExtremum,
    summary: cube_vesta.CubeSummary,
    mode: str,
) -> Vector3:
    origin = tuple(value * summary.unit_scale for value in summary.origin)
    cart = (extremum.x - origin[0], extremum.y - origin[1], extremum.z - origin[2])
    if mode == "crystal":
        return cube_vesta._cart_to_frac(cart, cube_vesta._cell_vectors(summary))
    return cart


def _format_sitet_line(
    index: int,
    label: str,
    radius: float,
    rgb: RGB,
    show_label: bool,
) -> str:
    r, g, b = rgb
    return (
        f"{index:4d} {label:>12s} {radius:7.4f}"
        f" {r:3d} {g:3d} {b:3d} {r:3d} {g:3d} {b:3d} 204  {1 if show_label else 0}"
    )


def _format_atomt_line(index: int, element: str, radius: float, rgb: RGB) -> str:
    r, g, b = rgb
    return f"{index:3d} {element:>10s} {radius:7.4f} {r:3d} {g:3d} {b:3d} {r:3d} {g:3d} {b:3d} 204"


def render_surface_extrema_phase(
    summary: cube_vesta.CubeSummary,
    extrema: Sequence[SurfaceExtremum],
    *,
    title: str = "Multiwfn surface extrema",
    structure: str = "auto",
    boundary: Tuple[float, float, float, float, float, float] = (0.0, 1.0, 0.0, 1.0, 0.0, 1.0),
    radius: float = DEFAULT_EXTREMA_RADIUS,
    maxima_rgb: RGB = DEFAULT_MAXIMA_RGB,
    minima_rgb: RGB = DEFAULT_MINIMA_RGB,
    maxima_element: str = "C",
    minima_element: str = "O",
    label_extrema: bool = False,
) -> str:
    if not extrema:
        raise ValueError("No selected surface extrema to render")
    if radius <= 0:
        raise ValueError("Surface extrema radius must be positive")

    mode = _extrema_structure_mode(summary, structure)
    structure_kind = "CRYSTAL" if mode == "crystal" else "MOLECULE"
    cell_line = (
        cube_vesta._format_cell_line(summary)
        if mode == "crystal"
        else "  1.000000   1.000000   1.000000  90.000000  90.000000  90.000000"
    )
    suffix = "    1a     1" if mode == "crystal" else "    1        -"
    lines = ["", ""]
    lines.extend(
        cube_vesta._phase_common_lines(
            summary,
            title=title,
            structure_kind=structure_kind,
            cell_line=cell_line,
        )
    )
    lines.append("STRUC")
    for index, extremum in enumerate(extrema, start=1):
        x, y, z = _site_coords(extremum, summary, mode)
        element = maxima_element if extremum.kind == "maximum" else minima_element
        lines.append(
            f"{index:4d}  {element:<2s}        {extremum.label:<12s} 1.0000"
            f" {x:10.6f} {y:10.6f} {z:10.6f}{suffix}"
        )
        lines.append("                            0.000000   0.000000   0.000000  0.00")
    lines.extend(["  0 0 0 0 0 0 0", "THERI 1"])
    for index, extremum in enumerate(extrema, start=1):
        lines.append(f"{index:4d} {extremum.label:>12s} -0.000000")
    lines.extend(
        [
            "  0 0 0",
            "SHAPE",
            "  0       0       0       0   0.000000  0   192   192   192   192",
            "BOUND",
            f" {boundary[0]:7.3f} {boundary[1]:7.3f} {boundary[2]:7.3f} {boundary[3]:7.3f} {boundary[4]:7.3f} {boundary[5]:7.3f}",
            "  0   0   0   0  0",
            "QCORIG",
            "        0         0         0",
            "SBOND",
            "  0 0 0 0",
            "SITET",
        ]
    )
    for index, extremum in enumerate(extrema, start=1):
        rgb = maxima_rgb if extremum.kind == "maximum" else minima_rgb
        lines.append(_format_sitet_line(index, extremum.label, radius, rgb, label_extrema))
    lines.extend(
        [
            "  0 0 0 0 0 0",
            "VECTR",
            " 0 0 0 0 0",
            "VECTT",
            " 0 0 0 0 0",
            "SPLAN",
            "  0   0   0   0",
            "LBLAT",
            " -1",
            "LBLSP",
            " -1",
            "DLATM",
            " -1",
            "DLBND",
            " -1",
            "DLPLY",
            " -1",
            "PLN2D",
            "  0   0   0   0",
            "ATOMT",
            _format_atomt_line(1, maxima_element, radius, maxima_rgb),
            _format_atomt_line(2, minima_element, radius, minima_rgb),
            "  0 0 0 0 0 0",
        ]
    )
    return "\n".join(lines) + "\n"


def _insert_before_scene(vesta_text: str, phase_text: str) -> str:
    lines = vesta_text.splitlines(keepends=True)
    phase_lines = phase_text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.strip() == "SCENE":
            lines[index:index] = phase_lines
            return "".join(lines)
    if not vesta_text.endswith("\n"):
        vesta_text += "\n"
    return vesta_text + phase_text


def _patch_comps(vesta_text: str, enabled: bool) -> str:
    target = f"COMPS {1 if enabled else 0}\n"
    lines = vesta_text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.strip().startswith("COMPS"):
            newline = "\r\n" if line.endswith("\r\n") else "\n"
            lines[index] = target.rstrip("\n") + newline
            return "".join(lines)
    return vesta_text


def overlay_surface_extrema_text(
    vesta_text: str,
    summary: cube_vesta.CubeSummary,
    extrema_pdb: SurfaceExtremaPdb,
    *,
    selection: str = "all",
    title: str = "Multiwfn surface extrema",
    structure: str = "auto",
    boundary: Tuple[float, float, float, float, float, float] = (0.0, 1.0, 0.0, 1.0, 0.0, 1.0),
    radius: float = DEFAULT_EXTREMA_RADIUS,
    maxima_rgb: RGB = DEFAULT_MAXIMA_RGB,
    minima_rgb: RGB = DEFAULT_MINIMA_RGB,
    maxima_element: str = "C",
    minima_element: str = "O",
    label_extrema: bool = False,
    set_comps_off: bool = True,
) -> Tuple[str, SurfaceExtremaOverlayResult]:
    selected = select_extrema(extrema_pdb.extrema, selection)
    if not selected:
        raise ValueError(f"No surface extrema matched selection `{selection}`")
    phase = render_surface_extrema_phase(
        summary,
        selected,
        title=title,
        structure=structure,
        boundary=boundary,
        radius=radius,
        maxima_rgb=maxima_rgb,
        minima_rgb=minima_rgb,
        maxima_element=maxima_element,
        minima_element=minima_element,
        label_extrema=label_extrema,
    )
    text = _insert_before_scene(vesta_text, phase)
    if set_comps_off:
        text = _patch_comps(text, enabled=False)
    return text, SurfaceExtremaOverlayResult(
        vesta_path=Path(),
        extrema_count=len(selected),
        maxima_count=sum(1 for item in selected if item.kind == "maximum"),
        minima_count=sum(1 for item in selected if item.kind == "minimum"),
        selection=selection,
        value_unit=extrema_pdb.value_unit,
    )


def overlay_surface_extrema_file(
    input_vesta: Path,
    surfanalysis_pdb: Path,
    output_vesta: Path,
    *,
    surface_cube: Path,
    selection: str = "all",
    title: str = "Multiwfn surface extrema",
    structure: str = "auto",
    boundary: Tuple[float, float, float, float, float, float] = (0.0, 1.0, 0.0, 1.0, 0.0, 1.0),
    radius: float = DEFAULT_EXTREMA_RADIUS,
    maxima_rgb: RGB = DEFAULT_MAXIMA_RGB,
    minima_rgb: RGB = DEFAULT_MINIMA_RGB,
    maxima_element: str = "C",
    minima_element: str = "O",
    label_extrema: bool = False,
    set_comps_off: bool = True,
    cube_units: str = "auto",
    strict: bool = True,
) -> SurfaceExtremaOverlayResult:
    input_vesta = Path(input_vesta)
    output_vesta = Path(output_vesta)
    summary = cube_vesta._read_cube_summary(Path(surface_cube), cube_units=cube_units, strict=strict)
    extrema_pdb = read_surfanalysis_pdb(Path(surfanalysis_pdb))
    text, result = overlay_surface_extrema_text(
        input_vesta.read_text(encoding="utf-8", errors="replace"),
        summary,
        extrema_pdb,
        selection=selection,
        title=title,
        structure=structure,
        boundary=boundary,
        radius=radius,
        maxima_rgb=maxima_rgb,
        minima_rgb=minima_rgb,
        maxima_element=maxima_element,
        minima_element=minima_element,
        label_extrema=label_extrema,
        set_comps_off=set_comps_off,
    )
    output_vesta.parent.mkdir(parents=True, exist_ok=True)
    output_vesta.write_text(text, encoding="utf-8")
    return SurfaceExtremaOverlayResult(
        vesta_path=output_vesta,
        extrema_count=result.extrema_count,
        maxima_count=result.maxima_count,
        minima_count=result.minima_count,
        selection=result.selection,
        value_unit=result.value_unit,
    )


def append_overlay_manifest(
    manifest: Path,
    *,
    surfanalysis_pdb: Path,
    result: SurfaceExtremaOverlayResult,
    radius: float,
    maxima_rgb: RGB,
    minima_rgb: RGB,
    label_extrema: bool,
    set_comps_off: bool,
) -> None:
    text = manifest.read_text(encoding="utf-8")
    lines = [
        "",
        "## Surface Extrema Overlay",
        "",
        f"- surfanalysis_pdb: `{surfanalysis_pdb}`",
        f"- selection: `{result.selection}`",
        f"- extrema_count: `{result.extrema_count}`",
        f"- maxima_count: `{result.maxima_count}`",
        f"- minima_count: `{result.minima_count}`",
        f"- value_unit: `{result.value_unit}`",
        f"- radius: `{radius}`",
        f"- maxima_rgb: `{maxima_rgb[0]} {maxima_rgb[1]} {maxima_rgb[2]}`",
        f"- minima_rgb: `{minima_rgb[0]} {minima_rgb[1]} {minima_rgb[2]}`",
        f"- label_extrema: `{str(label_extrema).lower()}`",
        f"- set_comps_off: `{str(set_comps_off).lower()}`",
        "- source_convention: `Multiwfn surfanalysis.pdb uses C for surface maxima and O for surface minima`",
    ]
    manifest.write_text(text.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


def _float_six(values: Optional[Sequence[float]]) -> Tuple[float, float, float, float, float, float]:
    if values is None:
        return 0.0, 1.0, 0.0, 1.0, 0.0, 1.0
    if len(values) != 6:
        raise ValueError("Boundary requires six values")
    return tuple(float(value) for value in values)  # type: ignore[return-value]


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Insert Multiwfn surfanalysis.pdb surface extrema into an existing VESTA file."
    )
    parser.add_argument("input_vesta", type=Path)
    parser.add_argument("surfanalysis_pdb", type=Path)
    parser.add_argument("output_vesta", type=Path)
    parser.add_argument("--surface-cube", type=Path, required=True, help="Surface/density cube used to align coordinates")
    parser.add_argument("--selection", choices=["all", "maxima", "minima"], default="all")
    parser.add_argument("--title", default="Multiwfn surface extrema")
    parser.add_argument("--structure", choices=["auto", "molecule", "crystal"], default="auto")
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--radius", type=float, default=DEFAULT_EXTREMA_RADIUS)
    parser.add_argument("--maxima-rgb", nargs=3, type=int, default=DEFAULT_MAXIMA_RGB)
    parser.add_argument("--minima-rgb", nargs=3, type=int, default=DEFAULT_MINIMA_RGB)
    parser.add_argument("--maxima-element", default="C")
    parser.add_argument("--minima-element", default="O")
    parser.add_argument("--label-extrema", action="store_true")
    parser.add_argument("--keep-comps", action="store_true", help="Do not force COMPS 0 after adding an extra phase")
    parser.add_argument("--cube-units", choices=["auto", "bohr", "angstrom"], default="auto")
    parser.add_argument("--non-strict-cube", action="store_true")
    args = parser.parse_args(argv)

    try:
        result = overlay_surface_extrema_file(
            args.input_vesta,
            args.surfanalysis_pdb,
            args.output_vesta,
            surface_cube=args.surface_cube,
            selection=args.selection,
            title=args.title,
            structure=args.structure,
            boundary=_float_six(args.boundary),
            radius=args.radius,
            maxima_rgb=_validate_rgb(args.maxima_rgb, "maxima"),
            minima_rgb=_validate_rgb(args.minima_rgb, "minima"),
            maxima_element=args.maxima_element,
            minima_element=args.minima_element,
            label_extrema=args.label_extrema,
            set_comps_off=not args.keep_comps,
            cube_units=args.cube_units,
            strict=not args.non_strict_cube,
        )
    except ValueError as exc:
        print(f"surface-extrema: {exc}")
        return 2

    print(result.vesta_path)
    print(f"extrema {result.extrema_count} maxima {result.maxima_count} minima {result.minima_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
