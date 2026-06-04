"""Convert Multiwfn AIM path/CP PDB files to an atoms-only VESTA file."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple


BOHR_TO_ANGSTROM = 0.529177210903


@dataclass
class PdbPoint:
    serial: int
    name: str
    resname: str
    chain: str
    resseq: int
    x: float
    y: float
    z: float
    element: str


@dataclass
class AimSite:
    label: str
    element: str
    x: float
    y: float
    z: float
    radius: float
    color: Tuple[int, int, int]
    kind: str
    group_index: int
    point_index: int


def _safe_int(text: str, default: int = 0) -> int:
    text = text.strip()
    if not text:
        return default
    try:
        return int(text)
    except ValueError:
        return default


def _parse_pdb_atom_line(line: str) -> Optional[PdbPoint]:
    record = line[:6].strip()
    if record not in {"ATOM", "HETATM"}:
        return None

    try:
        return PdbPoint(
            serial=_safe_int(line[6:11]),
            name=line[12:16].strip() or "X",
            resname=line[17:20].strip(),
            chain=line[21:22].strip(),
            resseq=_safe_int(line[22:26]),
            x=float(line[30:38]),
            y=float(line[38:46]),
            z=float(line[46:54]),
            element=(line[76:78].strip() or line[12:16].strip()[:2] or "C").title(),
        )
    except (ValueError, IndexError):
        fields = line.split()
        xyz = None
        for start in (6, 5, 3):
            if len(fields) >= start + 3:
                try:
                    xyz = (float(fields[start]), float(fields[start + 1]), float(fields[start + 2]))
                    break
                except ValueError:
                    pass
        if xyz is None:
            raise ValueError(f"Cannot parse PDB coordinate line: {line.rstrip()}") from None
        element = fields[-1] if fields[-1].isalpha() else fields[2]
        return PdbPoint(
            serial=_safe_int(fields[1]),
            name=fields[2],
            resname=fields[3] if len(fields) > 6 else "",
            chain=fields[4][0] if len(fields) > 6 else "",
            resseq=_safe_int(fields[5] if len(fields) > 6 else "0"),
            x=xyz[0],
            y=xyz[1],
            z=xyz[2],
            element=element.title(),
        )


def read_pdb_points(path: Path) -> Tuple[List[PdbPoint], Optional[Tuple[float, float, float, float, float, float]]]:
    points: List[PdbPoint] = []
    cell = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("CRYST1"):
            try:
                cell = (
                    float(line[6:15]),
                    float(line[15:24]),
                    float(line[24:33]),
                    float(line[33:40]),
                    float(line[40:47]),
                    float(line[47:54]),
                )
            except ValueError:
                cell = None
            continue
        point = _parse_pdb_atom_line(line)
        if point is not None:
            points.append(point)
    return points, cell


def _bounding_cell(
    sites: Sequence[AimSite],
    pdb_cell: Optional[Tuple[float, float, float, float, float, float]],
    margin: float,
) -> Tuple[Tuple[float, float, float, float, float, float], Tuple[float, float, float]]:
    if pdb_cell is not None:
        return pdb_cell, (0.0, 0.0, 0.0)
    if not sites:
        raise ValueError("Cannot build VESTA file without at least one AIM point")

    xs = [site.x for site in sites]
    ys = [site.y for site in sites]
    zs = [site.z for site in sites]
    minx, maxx = min(xs) - margin, max(xs) + margin
    miny, maxy = min(ys) - margin, max(ys) + margin
    minz, maxz = min(zs) - margin, max(zs) + margin
    a = max(maxx - minx, 1.0)
    b = max(maxy - miny, 1.0)
    c = max(maxz - minz, 1.0)
    return (a, b, c, 90.0, 90.0, 90.0), (minx, miny, minz)


def paths_to_sites(points: Iterable[PdbPoint], radius: float = 0.06) -> List[AimSite]:
    per_path_counts = {}
    sites: List[AimSite] = []
    for point in points:
        path_index = point.resseq or 1
        per_path_counts[path_index] = per_path_counts.get(path_index, 0) + 1
        point_index = per_path_counts[path_index]
        sites.append(
            AimSite(
                label=f"P{path_index:04d}_{point_index:04d}",
                element="C",
                x=point.x,
                y=point.y,
                z=point.z,
                radius=radius,
                color=(245, 166, 35),
                kind="path",
                group_index=path_index,
                point_index=point_index,
            )
        )
    return sites


def cps_to_sites(points: Iterable[PdbPoint], radius: float = 0.14) -> List[AimSite]:
    cp_colors = {
        "C": (145, 92, 182),
        "N": (255, 148, 36),
        "O": (245, 220, 64),
        "F": (78, 170, 82),
    }
    sites: List[AimSite] = []
    for index, point in enumerate(points, start=1):
        cp_code = (point.element or point.name or "C").upper()
        sites.append(
            AimSite(
                label=f"CP{index:04d}_{cp_code}",
                element=cp_code if cp_code in {"C", "N", "O", "F"} else "C",
                x=point.x,
                y=point.y,
                z=point.z,
                radius=radius,
                color=cp_colors.get(cp_code, (180, 180, 180)),
                kind="cp",
                group_index=point.resseq,
                point_index=index,
            )
        )
    return sites


def _lattice_components(cell: Tuple[float, float, float, float, float, float]) -> Tuple[float, float, float, float, float, float]:
    a, b, c, alpha, beta, gamma = cell
    alpha_r = math.radians(alpha)
    beta_r = math.radians(beta)
    gamma_r = math.radians(gamma)
    sin_gamma = math.sin(gamma_r)
    if abs(sin_gamma) < 1e-12:
        raise ValueError("Invalid cell: gamma angle produces a singular lattice")

    ax = a
    bx = b * math.cos(gamma_r)
    by = b * sin_gamma
    cx = c * math.cos(beta_r)
    cy = c * (math.cos(alpha_r) - math.cos(beta_r) * math.cos(gamma_r)) / sin_gamma
    cz2 = c * c - cx * cx - cy * cy
    if cz2 <= 0:
        raise ValueError("Invalid cell: angles produce a non-positive c-axis height")
    return ax, bx, by, cx, cy, math.sqrt(cz2)


def _frac(site: AimSite, cell: Tuple[float, float, float, float, float, float], origin: Tuple[float, float, float]) -> Tuple[float, float, float]:
    ax, bx, by, cx, cy, cz = _lattice_components(cell)
    ox, oy, oz = origin
    x = site.x - ox
    y = site.y - oy
    z = site.z - oz
    fz = z / cz
    fy = (y - fz * cy) / by
    fx = (x - fy * bx - fz * cx) / ax
    return fx, fy, fz


def render_atoms_only_vesta(
    sites: Sequence[AimSite],
    *,
    title: str = "Multiwfn AIM paths",
    pdb_cell: Optional[Tuple[float, float, float, float, float, float]] = None,
    margin: float = 2.0,
) -> str:
    cell, origin = _bounding_cell(sites, pdb_cell, margin)
    a, b, c, alpha, beta, gamma = cell

    lines: List[str] = [
        "#VESTA_FORMAT_VERSION 3.5.4",
        "",
        "",
        "CRYSTAL",
        "",
        "TITLE",
        title,
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
        " 1.000000  0.000000  0.000000  1.000000  0.000000  0.000000",
        " 0.000000  0.000000  1.000000  0.000000  0.000000  1.000000",
        "LMATRIX",
        " 1.000000  0.000000  0.000000  0.000000",
        " 0.000000  1.000000  0.000000  0.000000",
        " 0.000000  0.000000  1.000000  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        " 0.000000  0.000000  0.000000",
        "CELLP",
        f" {a:9.6f} {b:9.6f} {c:9.6f} {alpha:10.6f} {beta:10.6f} {gamma:10.6f}",
        "  0.000000   0.000000   0.000000   0.000000   0.000000   0.000000",
        "STRUC",
    ]

    for index, site in enumerate(sites, start=1):
        fx, fy, fz = _frac(site, cell, origin)
        lines.append(
            f"{index:4d}  {site.element:<2s}        {site.label:<12s} 1.0000"
            f" {fx:10.6f} {fy:10.6f} {fz:10.6f}    1a     1"
        )
        lines.append("                            0.000000   0.000000   0.000000  0.00")
    lines.extend(["  0 0 0 0 0 0 0", "THERI 1"])

    for index, site in enumerate(sites, start=1):
        lines.append(f"{index:4d} {site.label:>12s} -0.000000")
    lines.extend(
        [
            "  0 0 0",
            "SHAPE",
            "  0       0       0       0   0.000000  0   192   192   192   192",
            "BOUND",
            "       0        1         0        1         0        1",
            "  0   0   0   0  0",
            "SBOND",
            "  0 0 0 0",
            "SITET",
        ]
    )

    for index, site in enumerate(sites, start=1):
        r, g, bcol = site.color
        lines.append(
            f"{index:4d} {site.label:>12s} {site.radius:7.4f}"
            f" {r:3d} {g:3d} {bcol:3d} {r:3d} {g:3d} {bcol:3d} 204  0"
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
            "ATOMT",
            "  1          C  0.0600 245 166  35 245 166  35 204",
            "  2          N  0.1400 255 148  36 255 148  36 204",
            "  3          O  0.1400 245 220  64 245 220  64 204",
            "  4          F  0.1400  78 170  82  78 170  82 204",
            "  0 0 0 0 0 0",
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
            "DISPF 37753794",
            "MODEL   0  1  0",
            "SURFS   0  1  1",
            "SECTS  32  1",
            "FORMS   0  1",
            "ATOMS   0  0  1",
            "BONDS   0",
            "POLYS   0",
            "VECTS 1.000000",
            "BKGRC",
            " 255 255 255",
            "DPTHQ 1 -0.5000  3.5000",
        ]
    )
    return "\n".join(lines) + "\n"


def convert_aim_pdb_to_vesta(
    paths_pdb: Path,
    output_vesta: Path,
    *,
    cps_pdb: Optional[Path] = None,
    title: str = "Multiwfn AIM paths",
    margin: float = 2.0,
) -> None:
    path_points, path_cell = read_pdb_points(paths_pdb)
    sites = paths_to_sites(path_points)
    cell = path_cell

    if cps_pdb is not None:
        cp_points, cp_cell = read_pdb_points(cps_pdb)
        sites.extend(cps_to_sites(cp_points))
        cell = cell or cp_cell

    output_vesta.write_text(
        render_atoms_only_vesta(sites, title=title, pdb_cell=cell, margin=margin),
        encoding="utf-8",
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Convert Multiwfn AIM paths.pdb to atoms-only VESTA.")
    parser.add_argument("paths_pdb", type=Path)
    parser.add_argument("output_vesta", type=Path)
    parser.add_argument("--cps-pdb", type=Path)
    parser.add_argument("--title", default="Multiwfn AIM paths")
    parser.add_argument("--margin", type=float, default=2.0)
    args = parser.parse_args(argv)

    convert_aim_pdb_to_vesta(
        args.paths_pdb,
        args.output_vesta,
        cps_pdb=args.cps_pdb,
        title=args.title,
        margin=args.margin,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
