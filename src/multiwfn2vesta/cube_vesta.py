"""Generate VESTA files for scalar cube visualization."""

from __future__ import annotations

import argparse
import datetime as _datetime
import heapq
import math
import shutil
from dataclasses import dataclass
from itertools import zip_longest
from pathlib import Path
from typing import Dict, Iterator, List, NamedTuple, Optional, Sequence, Tuple


BOHR_TO_ANGSTROM = 0.529177210903
DEFAULT_ISOSURFACE = 0.01
DEFAULT_TEX_PERCENT_RANGE = (0.0, 1.0)

RGB = Tuple[int, int, int]
Vector3 = Tuple[float, float, float]


PERIODIC_SYMBOLS = [
    "",
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
]

ELEMENT_STYLES: Dict[str, Tuple[float, RGB]] = {
    "H": (0.4600, (255, 204, 204)),
    "B": (0.8300, (255, 181, 181)),
    "C": (0.7700, (128, 73, 41)),
    "N": (0.7000, (48, 80, 248)),
    "O": (0.7400, (254, 3, 0)),
    "F": (0.6400, (176, 185, 230)),
    "P": (1.1000, (255, 128, 0)),
    "S": (1.0400, (255, 255, 48)),
    "Cl": (0.9900, (31, 240, 31)),
    "Br": (1.1400, (166, 41, 41)),
    "I": (1.3300, (148, 0, 148)),
    "Ag": (1.4400, (183, 187, 189)),
}
DEFAULT_ELEMENT_STYLE = (0.7000, (180, 180, 180))


class CubeAtom(NamedTuple):
    atomic_number: int
    charge: float
    coords: Vector3


class CubeGridAxis(NamedTuple):
    count: int
    raw_count: int
    step: Vector3


class CubeSummary(NamedTuple):
    path: Path
    comment1: str
    comment2: str
    natoms: int
    origin: Vector3
    axes: Tuple[CubeGridAxis, CubeGridAxis, CubeGridAxis]
    atoms: List[CubeAtom]
    data_count: int
    expected_count: int
    data_min: Optional[float]
    data_max: Optional[float]
    unit: str
    unit_scale: float


class CubeVestaResult(NamedTuple):
    vesta_path: Path
    manifest_path: Optional[Path]
    copied_cubes: List[Tuple[Path, Path]]


class TextureReferenceRange(NamedTuple):
    source: str
    data_min: float
    data_max: float
    sample_count: int
    surface_band: Optional[float]
    nearest_fallback: bool


class IsosurfaceSpec(NamedTuple):
    level: float
    rgb: RGB


@dataclass
class StructureSite:
    index: int
    element: str
    label: str
    coords: Vector3
    radius: float
    rgb: RGB


def _parse_float(text: str) -> float:
    return float(text.replace("D", "E").replace("d", "e"))


def _vsub(left: Vector3, right: Vector3) -> Vector3:
    return left[0] - right[0], left[1] - right[1], left[2] - right[2]


def _vscale(vector: Vector3, scale: float) -> Vector3:
    return vector[0] * scale, vector[1] * scale, vector[2] * scale


def _vdot(left: Vector3, right: Vector3) -> float:
    return left[0] * right[0] + left[1] * right[1] + left[2] * right[2]


def _vcross(left: Vector3, right: Vector3) -> Vector3:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def _vnorm(vector: Vector3) -> float:
    return math.sqrt(_vdot(vector, vector))


def _angle(left: Vector3, right: Vector3) -> float:
    denom = _vnorm(left) * _vnorm(right)
    if denom == 0:
        raise ValueError("Cannot compute an angle from a zero-length cube cell vector")
    value = max(-1.0, min(1.0, _vdot(left, right) / denom))
    return math.degrees(math.acos(value))


def _det(a: Vector3, b: Vector3, c: Vector3) -> float:
    return _vdot(a, _vcross(b, c))


def _cart_to_frac(cart: Vector3, cell_vectors: Tuple[Vector3, Vector3, Vector3]) -> Vector3:
    a, b, c = cell_vectors
    determinant = _det(a, b, c)
    if abs(determinant) < 1e-12:
        raise ValueError("Cannot convert coordinates with a singular cube cell")
    fx = _det(cart, b, c) / determinant
    fy = _det(a, cart, c) / determinant
    fz = _det(a, b, cart) / determinant
    return fx, fy, fz


def _cell_vectors(summary: CubeSummary) -> Tuple[Vector3, Vector3, Vector3]:
    return tuple(_vscale(axis.step, axis.count * summary.unit_scale) for axis in summary.axes)  # type: ignore[return-value]


def _cell_parameters(summary: CubeSummary) -> Tuple[float, float, float, float, float, float]:
    a_vec, b_vec, c_vec = _cell_vectors(summary)
    a = _vnorm(a_vec)
    b = _vnorm(b_vec)
    c = _vnorm(c_vec)
    alpha = _angle(b_vec, c_vec)
    beta = _angle(a_vec, c_vec)
    gamma = _angle(a_vec, b_vec)
    return a, b, c, alpha, beta, gamma


def _cube_unit(axes: Sequence[CubeGridAxis], requested: str) -> Tuple[str, float]:
    if requested == "bohr":
        return "bohr", BOHR_TO_ANGSTROM
    if requested == "angstrom":
        return "angstrom", 1.0
    if any(axis.raw_count < 0 for axis in axes):
        return "angstrom", 1.0
    return "bohr", BOHR_TO_ANGSTROM


def _read_cube_summary(path: Path, *, cube_units: str = "auto", strict: bool = True) -> CubeSummary:
    path = Path(path)
    with path.open(encoding="utf-8", errors="replace") as handle:
        comment1 = handle.readline().rstrip("\n")
        comment2 = handle.readline().rstrip("\n")
        origin_line = handle.readline().split()
        if len(origin_line) < 4:
            raise ValueError(f"Cannot parse cube origin line in {path}")
        natoms = int(origin_line[0])
        origin = tuple(_parse_float(value) for value in origin_line[1:4])  # type: ignore[assignment]

        axes: List[CubeGridAxis] = []
        for _ in range(3):
            fields = handle.readline().split()
            if len(fields) < 4:
                raise ValueError(f"Cannot parse cube grid line in {path}")
            raw_count = int(fields[0])
            axes.append(
                CubeGridAxis(
                    count=abs(raw_count),
                    raw_count=raw_count,
                    step=tuple(_parse_float(value) for value in fields[1:4]),  # type: ignore[arg-type]
                )
            )

        atoms: List[CubeAtom] = []
        for _ in range(abs(natoms)):
            fields = handle.readline().split()
            if len(fields) < 5:
                raise ValueError(f"Cannot parse cube atom line in {path}")
            atoms.append(
                CubeAtom(
                    atomic_number=int(float(fields[0])),
                    charge=_parse_float(fields[1]),
                    coords=tuple(_parse_float(value) for value in fields[2:5]),  # type: ignore[arg-type]
                )
            )

        expected = axes[0].count * axes[1].count * axes[2].count
        data_count = 0
        data_min: Optional[float] = None
        data_max: Optional[float] = None
        for line in handle:
            for field in line.split():
                value = _parse_float(field)
                data_count += 1
                data_min = value if data_min is None else min(data_min, value)
                data_max = value if data_max is None else max(data_max, value)

    if strict and data_count != expected:
        raise ValueError(f"Cube data point count mismatch in {path}: got {data_count}, expected {expected}")
    unit, unit_scale = _cube_unit(axes, cube_units)
    return CubeSummary(
        path=path,
        comment1=comment1,
        comment2=comment2,
        natoms=natoms,
        origin=origin,
        axes=(axes[0], axes[1], axes[2]),
        atoms=atoms,
        data_count=data_count,
        expected_count=expected,
        data_min=data_min,
        data_max=data_max,
        unit=unit,
        unit_scale=unit_scale,
    )


def _iter_cube_data_values(path: Path) -> Iterator[float]:
    path = Path(path)
    with path.open(encoding="utf-8", errors="replace") as handle:
        handle.readline()
        handle.readline()
        origin_line = handle.readline().split()
        if len(origin_line) < 4:
            raise ValueError(f"Cannot parse cube origin line in {path}")
        natoms = abs(int(origin_line[0]))
        for _ in range(3 + natoms):
            handle.readline()
        for line in handle:
            for field in line.split():
                yield _parse_float(field)


def _symbol(atomic_number: int) -> str:
    if 0 < atomic_number < len(PERIODIC_SYMBOLS):
        return PERIODIC_SYMBOLS[atomic_number]
    return "X"


def _element_style(element: str) -> Tuple[float, RGB]:
    return ELEMENT_STYLES.get(element, DEFAULT_ELEMENT_STYLE)


def _structure_mode(summary: CubeSummary, requested: str) -> str:
    if requested != "auto":
        return requested
    if not summary.atoms:
        return "none"
    origin_abs = max(abs(value) for value in summary.origin)
    if origin_abs > 1.0e-8:
        return "molecule"
    cell_vectors = _cell_vectors(summary)
    for atom in summary.atoms:
        cart = _vscale(_vsub(atom.coords, summary.origin), summary.unit_scale)
        frac = _cart_to_frac(cart, cell_vectors)
        if any(value < -1.0e-5 or value > 1.00001 for value in frac):
            return "molecule"
    return "crystal"


def _structure_sites(summary: CubeSummary, mode: str) -> List[StructureSite]:
    sites: List[StructureSite] = []
    labels: Dict[str, int] = {}
    cell_vectors = _cell_vectors(summary)
    for index, atom in enumerate(summary.atoms, start=1):
        element = _symbol(atom.atomic_number)
        labels[element] = labels.get(element, 0) + 1
        label = f"{element}{labels[element]}"
        radius, rgb = _element_style(element)
        shifted = _vscale(_vsub(atom.coords, summary.origin), summary.unit_scale)
        coords = _cart_to_frac(shifted, cell_vectors) if mode == "crystal" else shifted
        sites.append(StructureSite(index=index, element=element, label=label, coords=coords, radius=radius, rgb=rgb))
    return sites


def _format_path_for_vesta(path_text: str) -> str:
    normalized = path_text.replace("\\", "/")
    if any(char.isspace() for char in normalized):
        return '"%s"' % normalized.replace('"', '\\"')
    return normalized


def _compatible_grid(left: CubeSummary, right: CubeSummary, tolerance: float = 1.0e-6) -> bool:
    if [axis.count for axis in left.axes] != [axis.count for axis in right.axes]:
        return False
    for lvalue, rvalue in zip(left.origin, right.origin):
        if abs(lvalue - rvalue) > tolerance:
            return False
    for laxis, raxis in zip(left.axes, right.axes):
        for lvalue, rvalue in zip(laxis.step, raxis.step):
            if abs(lvalue - rvalue) > tolerance:
                return False
    return True


def _percent_range_for_minmax(
    value_min: float,
    value_max: float,
    *,
    target_lower: float,
    target_upper: float,
) -> Tuple[float, float]:
    span = value_max - value_min
    if span == 0:
        raise ValueError("Cannot compute VESTA percentage range from zero-span texture values")
    return (target_lower - value_min) / span, (target_upper - value_min) / span


def _validate_rgb(values: Sequence[int], label: str) -> RGB:
    if len(values) != 3:
        raise ValueError(f"{label} requires exactly three RGB values")
    rgb = tuple(int(value) for value in values)
    if any(value < 0 or value > 255 for value in rgb):
        raise ValueError(f"{label} RGB values must be in 0..255")
    return rgb  # type: ignore[return-value]


def _validate_opacity(values: Sequence[int]) -> Tuple[int, int]:
    if len(values) != 2:
        raise ValueError("Surface opacity requires exactly two values")
    opacity = tuple(int(value) for value in values)
    if any(value < 0 or value > 255 for value in opacity):
        raise ValueError("Surface opacity values must be in 0..255")
    return opacity  # type: ignore[return-value]


def _surface_specs(
    *,
    isosurface: float,
    surface_mode: str,
    positive_rgb: RGB,
    negative_rgb: RGB,
) -> List[IsosurfaceSpec]:
    if surface_mode == "single":
        return [IsosurfaceSpec(isosurface, positive_rgb)]
    if surface_mode == "signed":
        level = abs(isosurface)
        if level == 0:
            raise ValueError("Signed surface mode requires a non-zero isosurface magnitude")
        return [
            IsosurfaceSpec(level, positive_rgb),
            IsosurfaceSpec(-level, negative_rgb),
        ]
    raise ValueError(f"Unknown surface mode: {surface_mode}")


def _format_isurf_lines(specs: Sequence[IsosurfaceSpec], opacity: Tuple[int, int]) -> List[str]:
    lines = ["ISURF"]
    for spec in specs:
        r, g, b = spec.rgb
        lines.append(f"  1   1 {spec.level:10.5g} {r:3d} {g:3d} {b:3d} {opacity[0]:3d} {opacity[1]:3d}")
    lines.append("  0   0   0   0")
    return lines


def _default_surface_band(summary: CubeSummary, isosurface: float) -> float:
    if summary.data_min is None or summary.data_max is None:
        return max(abs(isosurface) * 0.02, 1.0e-8)
    span = summary.data_max - summary.data_min
    return max(abs(isosurface) * 0.02, abs(span) * 0.005, 1.0e-8)


def _surface_sampled_texture_reference_range(
    surface_summary: CubeSummary,
    texture_summary: CubeSummary,
    *,
    isosurface: float,
    surface_band: Optional[float] = None,
    nearest_count: int = 1024,
) -> TextureReferenceRange:
    if nearest_count <= 0:
        raise ValueError("surface nearest fallback count must be positive")
    band = _default_surface_band(surface_summary, isosurface) if surface_band is None else float(surface_band)
    if band < 0:
        raise ValueError("surface band must be non-negative")

    sentinel = object()
    sampled_count = 0
    sampled_min: Optional[float] = None
    sampled_max: Optional[float] = None
    nearest_heap: List[Tuple[float, int, float]] = []
    total = 0

    for index, (surface_value, texture_value) in enumerate(
        zip_longest(_iter_cube_data_values(surface_summary.path), _iter_cube_data_values(texture_summary.path), fillvalue=sentinel)
    ):
        if surface_value is sentinel or texture_value is sentinel:
            raise ValueError("Surface and texture cube data lengths differ during surface sampling")
        surface_float = float(surface_value)
        texture_float = float(texture_value)
        total += 1
        distance = abs(surface_float - isosurface)
        if distance <= band:
            sampled_count += 1
            sampled_min = texture_float if sampled_min is None else min(sampled_min, texture_float)
            sampled_max = texture_float if sampled_max is None else max(sampled_max, texture_float)
        if len(nearest_heap) < nearest_count:
            heapq.heappush(nearest_heap, (-distance, index, texture_float))
        elif distance < -nearest_heap[0][0]:
            heapq.heapreplace(nearest_heap, (-distance, index, texture_float))

    if total != surface_summary.expected_count or total != texture_summary.expected_count:
        raise ValueError(
            "Cube data point count mismatch during surface sampling: got %d, expected %d/%d"
            % (total, surface_summary.expected_count, texture_summary.expected_count)
        )

    if sampled_count > 0 and sampled_min is not None and sampled_max is not None and sampled_min != sampled_max:
        return TextureReferenceRange("surface-band", sampled_min, sampled_max, sampled_count, band, False)

    if not nearest_heap:
        raise ValueError("No texture values are available for surface-sampled texture scaling")
    nearest_values = [item[2] for item in nearest_heap]
    return TextureReferenceRange(
        "surface-nearest",
        min(nearest_values),
        max(nearest_values),
        len(nearest_values),
        band,
        True,
    )


def _format_cell_line(summary: CubeSummary) -> str:
    a, b, c, alpha, beta, gamma = _cell_parameters(summary)
    return f" {a:9.6f} {b:9.6f} {c:9.6f} {alpha:10.6f} {beta:10.6f} {gamma:10.6f}"


def _phase_common_lines(summary: CubeSummary, *, title: str, structure_kind: str, cell_line: str) -> List[str]:
    a, _, c, _, _, _ = _cell_parameters(summary)
    return [
        structure_kind,
        "",
        "TITLE",
        f" {title}",
        "",
        "GROUP",
        "1 1 P 1",
        "SYMOP",
        " 0.000000  0.000000  0.000000  1  0  0   0  1  0   0  0  1   1",
        " -1.0 -1.0 -1.0  0 0 0  0 0 0  0 0 0",
        "TRANM 0",
        " 0.000000  0.000000  0.000000  1  0  0   0  1  0   0  0  1",
        "LTRANSL",
        " -1",
        " 0.000000  0.000000  0.000000  0.000000  0.000000  0.000000",
        "LORIENT",
        " -1   0   0   0   0",
        f" 1.000000  0.000000  0.000000 {a:9.6f}  0.000000  0.000000",
        f" 0.000000  0.000000  1.000000  0.000000  0.000000 {c:9.6f}",
        "LMATRIX",
        " 1.000000  0.000000  0.000000  0.000000",
        " 0.000000  1.000000  0.000000  0.000000",
        " 0.000000  0.000000  1.000000  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        " 0.000000  0.000000  0.000000",
        "PHASON",
        " 1.000000  0.000000  0.000000",
        " 0.000000  1.000000  0.000000",
        " 0.000000  0.000000  1.000000",
        "CELLP",
        cell_line,
        "  0.000000   0.000000   0.000000   0.000000   0.000000   0.000000",
    ]


def _density_phase_lines(
    summary: CubeSummary,
    *,
    title: str,
    density_path_text: str,
    texture_path_text: Optional[str],
    boundary: Tuple[float, float, float, float, float, float],
) -> List[str]:
    lines = _phase_common_lines(
        summary,
        title=title,
        structure_kind="CRYSTAL",
        cell_line=_format_cell_line(summary),
    )
    insert_at = lines.index("GROUP")
    imports = [
        "IMPORT_DENSITY 1",
        f"+1.000000 {_format_path_for_vesta(density_path_text)}",
    ]
    if texture_path_text:
        imports.extend(
            [
                "",
                "IMPORT_TEXTURE",
                f"+1.000000 {_format_path_for_vesta(texture_path_text)}",
            ]
        )
    lines[insert_at:insert_at] = imports + [""]
    lines.extend(_empty_phase_tail(boundary))
    return lines


def _empty_phase_tail(boundary: Tuple[float, float, float, float, float, float]) -> List[str]:
    return [
        "STRUC",
        "  0 0 0 0 0 0 0",
        "THERI 1",
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
    ]


def _structure_phase_lines(
    summary: CubeSummary,
    *,
    mode: str,
    title: str,
    boundary: Tuple[float, float, float, float, float, float],
) -> List[str]:
    if mode == "none":
        return []
    structure_kind = "CRYSTAL" if mode == "crystal" else "MOLECULE"
    if mode == "crystal":
        cell_line = _format_cell_line(summary)
        suffix = "    1a     1"
    else:
        cell_line = "  1.000000   1.000000   1.000000  90.000000  90.000000  90.000000"
        suffix = "    1        -"
    sites = _structure_sites(summary, mode)
    lines = ["", ""]
    lines.extend(_phase_common_lines(summary, title=title, structure_kind=structure_kind, cell_line=cell_line))
    lines.append("STRUC")
    for site in sites:
        x, y, z = site.coords
        lines.append(
            f"{site.index:4d}  {site.element:<2s}        {site.label:<12s} 1.0000"
            f" {x:10.6f} {y:10.6f} {z:10.6f}{suffix}"
        )
        lines.append("                            0.000000   0.000000   0.000000  0.00")
    lines.extend(["  0 0 0 0 0 0 0", "THERI 1"])
    for site in sites:
        lines.append(f"{site.index:4d} {site.label:>12s} -0.000000")
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
    for site in sites:
        r, g, b = site.rgb
        lines.append(
            f"{site.index:4d} {site.label:>12s} {site.radius:7.4f}"
            f" {r:3d} {g:3d} {b:3d} {r:3d} {g:3d} {b:3d} 204  0"
        )
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
        ]
    )
    unique_elements: List[str] = []
    for site in sites:
        if site.element not in unique_elements:
            unique_elements.append(site.element)
    for index, element in enumerate(unique_elements, start=1):
        radius, rgb = _element_style(element)
        r, g, b = rgb
        lines.append(f"{index:3d} {element:>10s} {radius:7.4f} {r:3d} {g:3d} {b:3d} {r:3d} {g:3d} {b:3d} 204")
    lines.extend(["  0 0 0 0 0 0"])
    return lines


def render_cube_vesta_text(
    summary: CubeSummary,
    *,
    density_path_text: str,
    texture_path_text: Optional[str] = None,
    title: str = "Cube visualization",
    isosurface: float = DEFAULT_ISOSURFACE,
    surface_mode: str = "single",
    positive_rgb: RGB = (255, 255, 0),
    negative_rgb: RGB = (0, 80, 255),
    surface_opacity: Tuple[int, int] = (127, 255),
    tex_percent_range: Tuple[float, float] = DEFAULT_TEX_PERCENT_RANGE,
    structure: str = "auto",
    boundary: Tuple[float, float, float, float, float, float] = (0.0, 1.0, 0.0, 1.0, 0.0, 1.0),
    sections: str = "off",
    show_structure_bonds: bool = True,
) -> str:
    structure_mode = _structure_mode(summary, structure)
    density_title = title
    lines: List[str] = [
        "#VESTA_FORMAT_VERSION 3.5.4",
        "",
        "",
    ]
    lines.extend(
        _density_phase_lines(
            summary,
            title=density_title,
            density_path_text=density_path_text,
            texture_path_text=texture_path_text,
            boundary=boundary,
        )
    )
    lines.extend(
        _structure_phase_lines(
            summary,
            mode=structure_mode,
            title=f"{title} structure",
            boundary=boundary,
        )
    )

    sects_line = "SECTS   0  0" if sections == "off" else "SECTS  32  1"
    tex_min, tex_max = tex_percent_range
    isurf_lines = _format_isurf_lines(
        _surface_specs(
            isosurface=isosurface,
            surface_mode=surface_mode,
            positive_rgb=positive_rgb,
            negative_rgb=negative_rgb,
        ),
        surface_opacity,
    )
    lines.extend(
        [
            "SCENE",
            " 1.000000  0.000000  0.000000  0.000000",
            " 0.000000  1.000000  0.000000  0.000000",
            " 0.000000  0.000000  1.000000  0.000000",
            " 0.000000  0.000000  0.000000  1.000000",
            "  0.000   0.000",
            "  0.000",
            "  1.000",
            "HBOND 0 2",
            "",
            "STYLE",
            "DISPF 37753666",
            "MODEL   0  1  0",
            "SURFS   0  1  1",
            sects_line,
            "FORMS   0  1",
            "ATOMS   0  0  1",
            f"BONDS   {1 if show_structure_bonds else 0}",
            "POLYS   1",
            "VECTS 1.000000",
            "FORMP",
            "  1  1.0   0   0   0",
            "ATOMP",
            " 24  24   0  50  2.0   0",
            "BONDP",
            "  1  16  0.250  2.000 127 127 127",
            "POLYP",
            " 204 1  1.000 180 180 180",
            *isurf_lines,
            "TEX3P",
            f"  1 {tex_min:12.5E} {tex_max:12.5E}",
            "SECTP",
            "  1  0.00000E+00  1.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00",
            "CONTR",
            " 0.1 -1 1 1 10 -1 2 5",
            " 2 1 2 1",
            "   0   0   0",
            "HKLPP",
            " 192 1  1.000 255   0 255",
            "UCOLP",
            "   0   1  1.000   0   0   0",
            "COMPS 1",
            "LABEL 1    12  1.000 0",
            "PROJT 0  0.962",
            "BKGRC",
            " 255 255 255",
            "DPTHQ 1 -0.5000  3.5000",
            "SECCL 0",
            "",
            "TEXCL 0",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def _copy_cube(
    source: Path,
    output_dir: Path,
    *,
    enabled: bool,
    used_names: Optional[Dict[str, Path]] = None,
    role: str = "cube",
) -> Tuple[str, Optional[Tuple[Path, Path]]]:
    source = Path(source)
    if not enabled:
        return str(source), None
    used_names = used_names if used_names is not None else {}
    resolved_source = source.resolve()
    destination_name = source.name
    if destination_name in used_names and used_names[destination_name] != resolved_source:
        stem = source.stem or "cube"
        suffix = source.suffix
        candidate_stem = f"{stem}_{role}"
        counter = 1
        while True:
            suffix_counter = "" if counter == 1 else f"_{counter}"
            candidate_name = f"{candidate_stem}{suffix_counter}{suffix}"
            if candidate_name not in used_names or used_names[candidate_name] == resolved_source:
                destination_name = candidate_name
                break
            counter += 1
    destination = output_dir / destination_name
    already_reserved = destination_name in used_names and used_names[destination_name] == resolved_source
    used_names[destination_name] = resolved_source
    if resolved_source != destination.resolve():
        if already_reserved and destination.exists():
            return destination.name, None
        shutil.copy2(source, destination)
        return destination.name, (source, destination)
    return destination.name, None


def _texture_percent_range(
    texture_summary: Optional[CubeSummary],
    *,
    surface_summary: Optional[CubeSummary] = None,
    isosurface: float = DEFAULT_ISOSURFACE,
    tex_percent: Optional[Tuple[float, float]],
    tex_physical: Optional[Tuple[float, float]],
    tex_range_source: str = "full-cube",
    surface_band: Optional[float] = None,
    surface_nearest: int = 1024,
) -> Tuple[Tuple[float, float], Optional[TextureReferenceRange]]:
    if tex_percent is not None and tex_physical is not None:
        raise ValueError("Use either tex_percent or tex_physical, not both")
    if tex_percent is not None:
        return tex_percent, None
    if tex_physical is not None:
        if texture_summary is None or texture_summary.data_min is None or texture_summary.data_max is None:
            raise ValueError("A texture cube is required to convert physical texture values to VESTA percentages")
        if tex_range_source == "surface-band":
            if surface_summary is None:
                raise ValueError("A surface cube is required for surface-sampled texture scaling")
            reference = _surface_sampled_texture_reference_range(
                surface_summary,
                texture_summary,
                isosurface=isosurface,
                surface_band=surface_band,
                nearest_count=surface_nearest,
            )
        elif tex_range_source == "full-cube":
            reference = TextureReferenceRange(
                "full-cube",
                texture_summary.data_min,
                texture_summary.data_max,
                texture_summary.data_count,
                None,
                False,
            )
        else:
            raise ValueError(f"Unknown texture range source: {tex_range_source}")
        return _percent_range_for_minmax(
            reference.data_min,
            reference.data_max,
            target_lower=tex_physical[0],
            target_upper=tex_physical[1],
        ), reference
    return DEFAULT_TEX_PERCENT_RANGE, None


def _manifest_text(
    *,
    result_vesta: Path,
    surface_summary: CubeSummary,
    texture_summary: Optional[CubeSummary],
    copied_cubes: Sequence[Tuple[Path, Path]],
    title: str,
    isosurface: float,
    tex_percent_range: Tuple[float, float],
    tex_physical: Optional[Tuple[float, float]],
    tex_reference_range: Optional[TextureReferenceRange],
    surface_mode: str,
    isosurface_specs: Sequence[IsosurfaceSpec],
    structure_mode: str,
    sections: str,
    generated_at: Optional[str] = None,
) -> str:
    generated_at = generated_at or _datetime.datetime.now().isoformat(timespec="seconds")
    lines = [
        "# Cube VESTA Recipe",
        "",
        "## Generated",
        "",
        f"- time: `{generated_at}`",
        f"- output_vesta: `{result_vesta}`",
        f"- title: `{title}`",
        "",
        "## Surface Cube",
        "",
        f"- path: `{surface_summary.path}`",
        f"- unit: `{surface_summary.unit}`",
        f"- atoms: `{len(surface_summary.atoms)}`",
        f"- grid: `{surface_summary.axes[0].count} x {surface_summary.axes[1].count} x {surface_summary.axes[2].count}`",
        f"- data_range: `{surface_summary.data_min}` to `{surface_summary.data_max}`",
        f"- isosurface: `{isosurface}`",
        f"- surface_mode: `{surface_mode}`",
        "- isosurface_levels: `%s`"
        % ", ".join(str(spec.level) for spec in isosurface_specs),
        "",
        "## Texture Cube",
        "",
    ]
    if texture_summary is None:
        lines.append("- texture_cube: not used")
    else:
        lines.extend(
            [
                f"- path: `{texture_summary.path}`",
                f"- data_range: `{texture_summary.data_min}` to `{texture_summary.data_max}`",
                f"- tex_percent_range: `{tex_percent_range[0]}` to `{tex_percent_range[1]}`",
            ]
        )
        if tex_physical is not None:
            lines.append(
                "- tex_physical_range: `%s` to `%s` converted from selected texture reference range"
                % (tex_physical[0], tex_physical[1])
            )
        if tex_reference_range is not None:
            lines.extend(
                [
                    f"- tex_reference_source: `{tex_reference_range.source}`",
                    f"- tex_reference_range: `{tex_reference_range.data_min}` to `{tex_reference_range.data_max}`",
                    f"- tex_reference_sample_count: `{tex_reference_range.sample_count}`",
                ]
            )
            if tex_reference_range.surface_band is not None:
                lines.append(f"- surface_band: `{tex_reference_range.surface_band}`")
            if tex_reference_range.nearest_fallback:
                lines.append("- surface_nearest_fallback: `true`")
    lines.extend(
        [
            "",
            "## VESTA Fields",
            "",
            "- `IMPORT_DENSITY 1` is used for the surface cube.",
            "- `IMPORT_TEXTURE` is used only when a texture cube is supplied.",
            f"- `SECTS` mode: `{sections}`.",
            "- `TEX3P` stores VESTA percentage/normalized values, not direct physical scalar values.",
            f"- structure_phase: `{structure_mode}`.",
            "",
            "## Copied Cubes",
            "",
        ]
    )
    if copied_cubes:
        for source, destination in copied_cubes:
            lines.append(f"- `{source}` -> `{destination}`")
    else:
        lines.append("- No cube files copied.")
    return "\n".join(lines) + "\n"


def run_workflow(
    surface_cube: Path,
    output_dir: Path,
    *,
    texture_cube: Optional[Path] = None,
    stem: Optional[str] = None,
    output_vesta: Optional[Path] = None,
    manifest: Optional[Path] = None,
    write_manifest: bool = True,
    title: Optional[str] = None,
    isosurface: float = DEFAULT_ISOSURFACE,
    surface_mode: str = "single",
    positive_rgb: RGB = (255, 255, 0),
    negative_rgb: RGB = (0, 80, 255),
    surface_opacity: Tuple[int, int] = (127, 255),
    tex_percent: Optional[Tuple[float, float]] = None,
    tex_physical: Optional[Tuple[float, float]] = None,
    tex_range_source: str = "full-cube",
    surface_band: Optional[float] = None,
    surface_nearest: int = 1024,
    cube_units: str = "auto",
    structure: str = "auto",
    boundary: Tuple[float, float, float, float, float, float] = (0.0, 1.0, 0.0, 1.0, 0.0, 1.0),
    sections: str = "off",
    copy_cubes: bool = True,
    strict: bool = True,
    strict_compatible: bool = True,
    show_structure_bonds: bool = True,
) -> CubeVestaResult:
    surface_cube = Path(surface_cube)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = stem or surface_cube.stem
    output_vesta = Path(output_vesta) if output_vesta else output_dir / f"{stem}_cube.vesta"
    manifest_path = Path(manifest) if manifest else output_dir / f"{stem}_cube_vesta_recipe.md"
    title = title or surface_cube.stem
    output_vesta.parent.mkdir(parents=True, exist_ok=True)

    surface_summary = _read_cube_summary(surface_cube, cube_units=cube_units, strict=strict)
    texture_summary = None
    if texture_cube is not None:
        texture_summary = _read_cube_summary(Path(texture_cube), cube_units=cube_units, strict=strict)
        if strict_compatible and not _compatible_grid(surface_summary, texture_summary):
            raise ValueError("Texture cube grid is not compatible with the surface cube")

    isosurface_specs = _surface_specs(
        isosurface=isosurface,
        surface_mode=surface_mode,
        positive_rgb=positive_rgb,
        negative_rgb=negative_rgb,
    )
    if surface_summary.data_min is not None and surface_summary.data_max is not None:
        outside_levels = [
            spec.level
            for spec in isosurface_specs
            if spec.level < surface_summary.data_min or spec.level > surface_summary.data_max
        ]
        if outside_levels:
            raise ValueError(
                "Isosurface level(s) %s outside surface cube data range %.6g..%.6g"
                % (", ".join("%.6g" % level for level in outside_levels), surface_summary.data_min, surface_summary.data_max)
            )

    tex_range, tex_reference_range = _texture_percent_range(
        texture_summary,
        surface_summary=surface_summary,
        isosurface=isosurface,
        tex_percent=tex_percent,
        tex_physical=tex_physical,
        tex_range_source=tex_range_source,
        surface_band=surface_band,
        surface_nearest=surface_nearest,
    )
    copied: List[Tuple[Path, Path]] = []
    used_cube_names: Dict[str, Path] = {}
    density_path_text, density_copy = _copy_cube(
        surface_cube,
        output_vesta.parent,
        enabled=copy_cubes,
        used_names=used_cube_names,
        role="surface",
    )
    if density_copy is not None:
        copied.append(density_copy)
    texture_path_text = None
    if texture_cube is not None:
        texture_path_text, texture_copy = _copy_cube(
            Path(texture_cube),
            output_vesta.parent,
            enabled=copy_cubes,
            used_names=used_cube_names,
            role="texture",
        )
        if texture_copy is not None:
            copied.append(texture_copy)

    structure_mode = _structure_mode(surface_summary, structure)
    output_vesta.write_text(
        render_cube_vesta_text(
            surface_summary,
            density_path_text=density_path_text,
            texture_path_text=texture_path_text,
            title=title,
            isosurface=isosurface,
            surface_mode=surface_mode,
            positive_rgb=positive_rgb,
            negative_rgb=negative_rgb,
            surface_opacity=surface_opacity,
            tex_percent_range=tex_range,
            structure=structure,
            boundary=boundary,
            sections=sections,
            show_structure_bonds=show_structure_bonds,
        ),
        encoding="utf-8",
    )
    if write_manifest:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            _manifest_text(
                result_vesta=output_vesta,
                surface_summary=surface_summary,
                texture_summary=texture_summary,
                copied_cubes=copied,
                title=title,
                isosurface=isosurface,
                tex_percent_range=tex_range,
                tex_physical=tex_physical,
                tex_reference_range=tex_reference_range,
                surface_mode=surface_mode,
                isosurface_specs=isosurface_specs,
                structure_mode=structure_mode,
                sections=sections,
            ),
            encoding="utf-8",
        )
    else:
        manifest_path = None
    return CubeVestaResult(vesta_path=output_vesta, manifest_path=manifest_path, copied_cubes=copied)


def _float_pair(values: Optional[Sequence[float]]) -> Optional[Tuple[float, float]]:
    if values is None:
        return None
    if len(values) != 2:
        raise ValueError("Expected exactly two values")
    return float(values[0]), float(values[1])


def _float_six(values: Optional[Sequence[float]]) -> Tuple[float, float, float, float, float, float]:
    if values is None:
        return 0.0, 1.0, 0.0, 1.0, 0.0, 1.0
    if len(values) != 6:
        raise ValueError("Boundary requires six values: xmin xmax ymin ymax zmin zmax")
    return tuple(float(value) for value in values)  # type: ignore[return-value]


def _rgb_arg(values: Sequence[int], label: str) -> RGB:
    return _validate_rgb(values, label)


def _opacity_arg(values: Sequence[int]) -> Tuple[int, int]:
    return _validate_opacity(values)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create a VESTA file for a scalar cube, optionally with a texture/color cube."
    )
    parser.add_argument("surface_cube", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--texture-cube", type=Path)
    parser.add_argument("--stem")
    parser.add_argument("--output-vesta", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--no-manifest", action="store_true")
    parser.add_argument("--title")
    parser.add_argument("--isosurface", type=float, default=DEFAULT_ISOSURFACE)
    parser.add_argument("--surface-mode", choices=["single", "signed"], default="single")
    parser.add_argument("--positive-rgb", nargs=3, type=int, default=(255, 255, 0), metavar=("R", "G", "B"))
    parser.add_argument("--negative-rgb", nargs=3, type=int, default=(0, 80, 255), metavar=("R", "G", "B"))
    parser.add_argument("--surface-opacity", nargs=2, type=int, default=(127, 255), metavar=("O1", "O2"))
    parser.add_argument("--tex-percent", nargs=2, type=float, metavar=("MIN", "MAX"))
    parser.add_argument("--tex-physical", nargs=2, type=float, metavar=("MIN", "MAX"))
    parser.add_argument("--tex-range-source", choices=["full-cube", "surface-band"], default="full-cube")
    parser.add_argument("--surface-band", type=float, help="Surface scalar half-width for surface-band texture scaling")
    parser.add_argument("--surface-nearest", type=int, default=1024, help="Nearest grid-point fallback count")
    parser.add_argument("--cube-units", choices=["auto", "bohr", "angstrom"], default="auto")
    parser.add_argument("--structure", choices=["auto", "none", "molecule", "crystal"], default="auto")
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--sections", choices=["off", "keep"], default="off")
    parser.add_argument("--no-copy-cubes", action="store_true")
    parser.add_argument("--non-strict", action="store_true", help="Allow cube data count mismatch")
    parser.add_argument("--no-strict-compatible", action="store_true", help="Do not require texture grid to match surface grid")
    parser.add_argument("--structure-bonds-off", action="store_true")
    args = parser.parse_args(argv)

    result = run_workflow(
        args.surface_cube,
        args.output_dir,
        texture_cube=args.texture_cube,
        stem=args.stem,
        output_vesta=args.output_vesta,
        manifest=args.manifest,
        write_manifest=not args.no_manifest,
        title=args.title,
        isosurface=args.isosurface,
        surface_mode=args.surface_mode,
        positive_rgb=_rgb_arg(args.positive_rgb, "positive surface"),
        negative_rgb=_rgb_arg(args.negative_rgb, "negative surface"),
        surface_opacity=_opacity_arg(args.surface_opacity),
        tex_percent=_float_pair(args.tex_percent),
        tex_physical=_float_pair(args.tex_physical),
        tex_range_source=args.tex_range_source,
        surface_band=args.surface_band,
        surface_nearest=args.surface_nearest,
        cube_units=args.cube_units,
        structure=args.structure,
        boundary=_float_six(args.boundary),
        sections=args.sections,
        copy_cubes=not args.no_copy_cubes,
        strict=not args.non_strict,
        strict_compatible=not args.no_strict_compatible,
        show_structure_bonds=not args.structure_bonds_off,
    )
    print(result.vesta_path)
    if result.manifest_path is not None:
        print(result.manifest_path)
    if result.copied_cubes:
        for _, destination in result.copied_cubes:
            print(f"copied {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
