"""Convert simple XYZ/extXYZ trajectories into per-frame VESTA structure files."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Tuple

from .cube_vesta import DEFAULT_ELEMENT_STYLE, ELEMENT_STYLES


Vector3 = Tuple[float, float, float]
CellVectors = Tuple[Vector3, Vector3, Vector3]
Boundary = Tuple[float, float, float, float, float, float]
RGB = Tuple[int, int, int]

DEFAULT_BOUNDARY: Boundary = (0.0, 1.0, 0.0, 1.0, 0.0, 1.0)
DEFAULT_BOND_RGB: RGB = (127, 127, 127)


class TrajectoryAtom(NamedTuple):
    element: str
    coords: Vector3


class TrajectoryFrame(NamedTuple):
    index: int
    comment: str
    atoms: Tuple[TrajectoryAtom, ...]
    lattice: Optional[CellVectors]


class BondRule(NamedTuple):
    element1: str
    element2: str
    distance_min: float
    distance_max: float


class TrajectoryFramesResult(NamedTuple):
    source: Path
    output_dir: Path
    frames_dir: Path
    manifest_path: Path
    recipe_path: Path
    frame_paths: Tuple[Path, ...]
    frame_indices: Tuple[int, ...]


def _parse_float(text: str) -> float:
    return float(text.replace("D", "E").replace("d", "e"))


def _vsub(left: Vector3, right: Vector3) -> Vector3:
    return left[0] - right[0], left[1] - right[1], left[2] - right[2]


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


def _det(a: Vector3, b: Vector3, c: Vector3) -> float:
    return _vdot(a, _vcross(b, c))


def _angle(left: Vector3, right: Vector3) -> float:
    denom = _vnorm(left) * _vnorm(right)
    if denom == 0:
        raise ValueError("Cannot compute a cell angle from a zero-length vector")
    value = max(-1.0, min(1.0, _vdot(left, right) / denom))
    return math.degrees(math.acos(value))


def _cell_parameters(vectors: CellVectors) -> Tuple[float, float, float, float, float, float]:
    a_vec, b_vec, c_vec = vectors
    a = _vnorm(a_vec)
    b = _vnorm(b_vec)
    c = _vnorm(c_vec)
    alpha = _angle(b_vec, c_vec)
    beta = _angle(a_vec, c_vec)
    gamma = _angle(a_vec, b_vec)
    return a, b, c, alpha, beta, gamma


def _cart_to_frac(cart: Vector3, vectors: CellVectors) -> Vector3:
    a, b, c = vectors
    determinant = _det(a, b, c)
    if abs(determinant) < 1.0e-12:
        raise ValueError("Cannot convert coordinates with a singular cell")
    fx = _det(cart, b, c) / determinant
    fy = _det(a, cart, c) / determinant
    fz = _det(a, b, cart) / determinant
    return fx, fy, fz


def _parse_lattice(comment: str) -> Optional[CellVectors]:
    match = re.search(r'Lattice="([^"]+)"', comment)
    if not match:
        return None
    values = [_parse_float(item) for item in match.group(1).split()]
    if len(values) != 9:
        raise ValueError("extXYZ Lattice must contain 9 numbers")
    return (
        (values[0], values[1], values[2]),
        (values[3], values[4], values[5]),
        (values[6], values[7], values[8]),
    )


def iter_xyz_frames(path: Path) -> Iterator[TrajectoryFrame]:
    path = Path(path)
    with path.open(encoding="utf-8", errors="replace") as handle:
        frame_index = 0
        while True:
            natoms_line = handle.readline()
            if not natoms_line:
                break
            if not natoms_line.strip():
                continue
            try:
                natoms = int(natoms_line.strip())
            except ValueError as exc:
                raise ValueError("Cannot parse XYZ atom count line: {}".format(natoms_line.rstrip())) from exc
            comment = handle.readline()
            if comment == "":
                raise ValueError("Unexpected EOF after XYZ atom count")
            atoms: List[TrajectoryAtom] = []
            for atom_index in range(natoms):
                line = handle.readline()
                if line == "":
                    raise ValueError("Unexpected EOF inside XYZ frame")
                fields = line.split()
                if len(fields) < 4:
                    raise ValueError("Cannot parse XYZ atom line {}: {}".format(atom_index + 1, line.rstrip()))
                atoms.append(
                    TrajectoryAtom(
                        element=_normalize_element(fields[0]),
                        coords=(_parse_float(fields[1]), _parse_float(fields[2]), _parse_float(fields[3])),
                    )
                )
            frame_index += 1
            yield TrajectoryFrame(
                index=frame_index,
                comment=comment.rstrip("\n"),
                atoms=tuple(atoms),
                lattice=_parse_lattice(comment),
            )


def _normalize_element(element: str) -> str:
    text = str(element).strip()
    if not text:
        raise ValueError("Empty element symbol")
    return text[0].upper() + text[1:].lower()


def _element_style(element: str) -> Tuple[float, RGB]:
    return ELEMENT_STYLES.get(element, DEFAULT_ELEMENT_STYLE)


def _labels_for_atoms(atoms: Sequence[TrajectoryAtom]) -> List[str]:
    counts: Dict[str, int] = {}
    labels: List[str] = []
    for atom in atoms:
        counts[atom.element] = counts.get(atom.element, 0) + 1
        labels.append("{}{}".format(atom.element, counts[atom.element]))
    return labels


def _phase_common_lines(title: str, structure_kind: str, cell_line: str, cell_vectors: Optional[CellVectors]) -> List[str]:
    if cell_vectors is not None:
        a, _, c, _, _, _ = _cell_parameters(cell_vectors)
    else:
        a, c = 1.0, 1.0
    return [
        structure_kind,
        "",
        "TITLE",
        " {}".format(title),
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


def _format_cell_line(cell_vectors: Optional[CellVectors]) -> str:
    if cell_vectors is None:
        return "  1.000000   1.000000   1.000000  90.000000  90.000000  90.000000"
    a, b, c, alpha, beta, gamma = _cell_parameters(cell_vectors)
    return f" {a:9.6f} {b:9.6f} {c:9.6f} {alpha:10.6f} {beta:10.6f} {gamma:10.6f}"


def _format_boundary(boundary: Boundary) -> str:
    return " {0:7.3f} {1:7.3f} {2:7.3f} {3:7.3f} {4:7.3f} {5:7.3f}".format(*boundary)


def _style_tail(show_bonds: bool, comps: bool = False) -> List[str]:
    return [
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
        "SECTS   0  0",
        "FORMS   0  1",
        "ATOMS   0  0  1",
        "BONDS   {}".format(1 if show_bonds else 0),
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
        "COMPS {}".format(1 if comps else 0),
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


def _tail_from_reference(reference_vesta: Optional[Path]) -> Optional[List[str]]:
    if reference_vesta is None:
        return None
    lines = Path(reference_vesta).read_text(encoding="utf-8", errors="replace").splitlines()
    for index, line in enumerate(lines):
        if line.strip() == "SCENE":
            return lines[index:]
    raise ValueError("Reference VESTA has no SCENE section: {}".format(reference_vesta))


def render_frame_vesta_text(
    frame: TrajectoryFrame,
    *,
    title: str,
    structure: str = "auto",
    boundary: Boundary = DEFAULT_BOUNDARY,
    bond_rules: Sequence[BondRule] = (),
    bond_radius: float = 0.25,
    bond_rgb: RGB = DEFAULT_BOND_RGB,
    reference_tail: Optional[Sequence[str]] = None,
    comps: bool = False,
) -> str:
    if structure not in {"auto", "molecule", "crystal"}:
        raise ValueError("structure must be auto, molecule, or crystal")
    cell_vectors = frame.lattice
    mode = "crystal" if (structure == "auto" and cell_vectors is not None) else structure
    if mode == "auto":
        mode = "molecule"
    if mode == "crystal" and cell_vectors is None:
        raise ValueError("Crystal trajectory frame requires extXYZ Lattice or --cell-vectors")

    structure_kind = "CRYSTAL" if mode == "crystal" else "MOLECULE"
    suffix = "    1a     1" if mode == "crystal" else "    1        -"
    labels = _labels_for_atoms(frame.atoms)
    lines: List[str] = ["#VESTA_FORMAT_VERSION 3.5.4", "", ""]
    lines.extend(_phase_common_lines(title, structure_kind, _format_cell_line(cell_vectors), cell_vectors))
    lines.append("STRUC")
    for index, (atom, label) in enumerate(zip(frame.atoms, labels), start=1):
        coords = _cart_to_frac(atom.coords, cell_vectors) if mode == "crystal" and cell_vectors is not None else atom.coords
        x, y, z = coords
        lines.append(
            f"{index:4d}  {atom.element:<2s}        {label:<12s} 1.0000"
            f" {x:10.6f} {y:10.6f} {z:10.6f}{suffix}"
        )
        lines.append("                            0.000000   0.000000   0.000000  0.00")
    lines.extend(["  0 0 0 0 0 0 0", "THERI 1"])
    for index, label in enumerate(labels, start=1):
        lines.append(f"{index:4d} {label:>12s} -0.000000")
    lines.extend(
        [
            "  0 0 0",
            "SHAPE",
            "  0       0       0       0   0.000000  0   192   192   192   192",
            "BOUND",
            _format_boundary(boundary),
            "  0   0   0   0  0",
            "QCORIG",
            "        0         0         0",
            "SBOND",
        ]
    )
    br, bg, bb = bond_rgb
    for index, rule in enumerate(bond_rules, start=1):
        lines.append(
            f"{index:4d} {rule.element1:<2s} {rule.element2:<2s}"
            f" {rule.distance_min:8.5f} {rule.distance_max:8.5f}"
            f"  0  1  1  0  {bond_radius:7.4f} {bond_radius:7.4f}"
            f" {br:3d} {bg:3d} {bb:3d}"
        )
    lines.extend(["  0 0 0 0", "SITET"])
    for index, (atom, label) in enumerate(zip(frame.atoms, labels), start=1):
        radius, rgb = _element_style(atom.element)
        r, g, b = rgb
        lines.append(
            f"{index:4d} {label:>12s} {radius:7.4f}"
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
    for atom in frame.atoms:
        if atom.element not in unique_elements:
            unique_elements.append(atom.element)
    for index, element in enumerate(unique_elements, start=1):
        radius, rgb = _element_style(element)
        r, g, b = rgb
        lines.append(f"{index:3d} {element:>10s} {radius:7.4f} {r:3d} {g:3d} {b:3d} {r:3d} {g:3d} {b:3d} 204")
    lines.append("  0 0 0 0 0 0")
    tail = list(reference_tail) if reference_tail is not None else _style_tail(show_bonds=bool(bond_rules), comps=comps)
    lines.extend(tail)
    return "\n".join(lines) + "\n"


def _selected_frames(
    frames: Iterable[TrajectoryFrame],
    *,
    start: int = 1,
    stop: Optional[int] = None,
    stride: int = 1,
) -> Iterator[TrajectoryFrame]:
    if start < 1:
        raise ValueError("--start must be at least 1")
    if stop is not None and stop < start:
        raise ValueError("--stop must be greater than or equal to --start")
    if stride < 1:
        raise ValueError("--stride must be at least 1")
    for frame in frames:
        if frame.index < start:
            continue
        if stop is not None and frame.index > stop:
            break
        if (frame.index - start) % stride == 0:
            yield frame


def _parse_boundary(values: Optional[Sequence[float]]) -> Boundary:
    if values is None:
        return DEFAULT_BOUNDARY
    if len(values) != 6:
        raise ValueError("--boundary requires six numbers")
    return tuple(float(value) for value in values)  # type: ignore[return-value]


def _parse_bonds(values: Optional[Sequence[Sequence[str]]]) -> Tuple[BondRule, ...]:
    rules: List[BondRule] = []
    for raw in values or []:
        if len(raw) != 4:
            raise ValueError("--bond requires ELEMENT1 ELEMENT2 MIN MAX")
        rules.append(BondRule(_normalize_element(raw[0]), _normalize_element(raw[1]), float(raw[2]), float(raw[3])))
    return tuple(rules)


def _parse_rgb(values: Optional[Sequence[int]]) -> RGB:
    if values is None:
        return DEFAULT_BOND_RGB
    if len(values) != 3:
        raise ValueError("--bond-rgb requires three integers")
    rgb = tuple(int(value) for value in values)
    if any(value < 0 or value > 255 for value in rgb):
        raise ValueError("--bond-rgb values must be in 0..255")
    return rgb  # type: ignore[return-value]


def _parse_cell_vectors(values: Optional[Sequence[float]]) -> Optional[CellVectors]:
    if values is None:
        return None
    if len(values) != 9:
        raise ValueError("--cell-vectors requires 9 numbers")
    numbers = [float(value) for value in values]
    return (
        (numbers[0], numbers[1], numbers[2]),
        (numbers[3], numbers[4], numbers[5]),
        (numbers[6], numbers[7], numbers[8]),
    )


def write_trajectory_frames(
    trajectory: Path,
    output_dir: Path,
    *,
    stem: str = "frame",
    start: int = 1,
    stop: Optional[int] = None,
    stride: int = 1,
    structure: str = "auto",
    boundary: Boundary = DEFAULT_BOUNDARY,
    bond_rules: Sequence[BondRule] = (),
    bond_radius: float = 0.25,
    bond_rgb: RGB = DEFAULT_BOND_RGB,
    reference_vesta: Optional[Path] = None,
    cell_vectors: Optional[CellVectors] = None,
    comps: bool = False,
) -> TrajectoryFramesResult:
    trajectory = Path(trajectory).expanduser().resolve()
    if not trajectory.exists():
        raise FileNotFoundError("Trajectory file not found: {}".format(trajectory))
    output_dir = Path(output_dir).expanduser().resolve()
    frames_dir = output_dir / "vesta"
    frames_dir.mkdir(parents=True, exist_ok=True)
    reference_tail = _tail_from_reference(reference_vesta)
    frame_paths: List[Path] = []
    frame_indices: List[int] = []
    for serial, frame in enumerate(_selected_frames(iter_xyz_frames(trajectory), start=start, stop=stop, stride=stride), start=1):
        effective_lattice = frame.lattice or cell_vectors
        effective_frame = TrajectoryFrame(frame.index, frame.comment, frame.atoms, effective_lattice)
        frame_path = frames_dir / f"{stem}_{serial:04d}.vesta"
        frame_path.write_text(
            render_frame_vesta_text(
                effective_frame,
                title=f"{trajectory.stem} frame {frame.index}",
                structure=structure,
                boundary=boundary,
                bond_rules=bond_rules,
                bond_radius=bond_radius,
                bond_rgb=bond_rgb,
                reference_tail=reference_tail,
                comps=comps,
            ),
            encoding="utf-8",
        )
        frame_paths.append(frame_path)
        frame_indices.append(frame.index)
    if not frame_paths:
        raise ValueError("No trajectory frames were selected")
    manifest_path = output_dir / f"{stem}_trajectory_frames_manifest.json"
    recipe_path = output_dir / f"{stem}_trajectory_frames_recipe.md"
    manifest = {
        "source": str(trajectory),
        "frames_dir": str(frames_dir),
        "frame_count": len(frame_paths),
        "frame_indices": frame_indices,
        "frames": [str(path) for path in frame_paths],
        "start": start,
        "stop": stop,
        "stride": stride,
        "structure": structure,
        "boundary": list(boundary),
        "bond_rules": [rule._asdict() for rule in bond_rules],
        "bond_radius": bond_radius,
        "bond_rgb": list(bond_rgb),
        "reference_vesta": str(Path(reference_vesta).resolve()) if reference_vesta else None,
        "cell_vectors": [list(vector) for vector in cell_vectors] if cell_vectors is not None else None,
        "comps": comps,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    recipe_path.write_text(_recipe_text(manifest_path, manifest), encoding="utf-8")
    return TrajectoryFramesResult(
        source=trajectory,
        output_dir=output_dir,
        frames_dir=frames_dir,
        manifest_path=manifest_path,
        recipe_path=recipe_path,
        frame_paths=tuple(frame_paths),
        frame_indices=tuple(frame_indices),
    )


def _recipe_text(manifest_path: Path, manifest: dict) -> str:
    lines = [
        "# trajectory-frames recipe",
        "",
        "- source: `{}`".format(manifest["source"]),
        "- frames_dir: `{}`".format(manifest["frames_dir"]),
        "- frame_count: `{}`".format(manifest["frame_count"]),
        "- frame_indices: `{}`".format(", ".join(str(item) for item in manifest["frame_indices"])),
        "- structure: `{}`".format(manifest["structure"]),
        "- boundary: `{}`".format(" ".join(str(item) for item in manifest["boundary"])),
        "- bond_rules: `{}`".format(
            "; ".join(
                "{element1}-{element2} {distance_min:g}-{distance_max:g}".format(**rule)
                for rule in manifest["bond_rules"]
            )
            or "none"
        ),
        "- bond_radius: `{}`".format(manifest["bond_radius"]),
        "- bond_rgb: `{}`".format(" ".join(str(item) for item in manifest["bond_rgb"])),
        "- reference_vesta: `{}`".format(manifest["reference_vesta"] or "none"),
        "- cell_vectors: `{}`".format(manifest["cell_vectors"] or "from extXYZ Lattice or none"),
        "- comps: `{}`".format("on" if manifest["comps"] else "off"),
        "- manifest: `{}`".format(manifest_path),
        "",
        "## Generated frame files",
        "",
        "The `.vesta` frame files are in `{}`.".format(manifest["frames_dir"]),
        "This command only writes VESTA structure files; it does not start VESTA and does not render PNG images.",
        "",
        "## Next steps",
        "",
        "1. Render these `.vesta` frames to a PNG directory using the maintained or manual VESTA rendering route.",
        "2. Encode the PNG frames with:",
        "",
        "```bash",
        "multiwfn2vesta trajectory-video png_frames trajectory.mp4 --fps 24 --bitrate 20M",
        "```",
        "",
        "ASE `.traj` reading and unattended VESTA PNG rendering are intentionally outside this command for now.",
    ]
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert XYZ/extXYZ trajectories into per-frame VESTA files.")
    parser.add_argument("trajectory", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--stem", default="frame")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--stop", type=int)
    parser.add_argument("--stride", type=int, default=1)
    parser.add_argument("--structure", choices=["auto", "molecule", "crystal"], default="auto")
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--bond", nargs=4, action="append", metavar=("E1", "E2", "MIN", "MAX"), help="Add a VESTA SBOND rule; repeat as needed")
    parser.add_argument("--bond-radius", type=float, default=0.25)
    parser.add_argument("--bond-rgb", nargs=3, type=int, metavar=("R", "G", "B"))
    parser.add_argument("--reference-vesta", type=Path, help="Reuse the SCENE/STYLE tail from a saved VESTA file")
    parser.add_argument("--cell-vectors", nargs=9, type=float, metavar=("A1X", "A1Y", "A1Z", "A2X", "A2Y", "A2Z", "A3X", "A3Y", "A3Z"))
    parser.add_argument("--comps", choices=["off", "on"], default="off", help="Show VESTA compass/axes in the default style tail")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = write_trajectory_frames(
            args.trajectory,
            args.output_dir,
            stem=args.stem,
            start=args.start,
            stop=args.stop,
            stride=args.stride,
            structure=args.structure,
            boundary=_parse_boundary(args.boundary),
            bond_rules=_parse_bonds(args.bond),
            bond_radius=args.bond_radius,
            bond_rgb=_parse_rgb(args.bond_rgb),
            reference_vesta=args.reference_vesta,
            cell_vectors=_parse_cell_vectors(args.cell_vectors),
            comps=args.comps == "on",
        )
    except Exception as exc:  # pragma: no cover - CLI smoke covers this path
        print(str(exc), file=sys.stderr)
        return 2
    print(result.frames_dir)
    print(result.manifest_path)
    print(result.recipe_path)
    print("frames={}".format(len(result.frame_paths)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
