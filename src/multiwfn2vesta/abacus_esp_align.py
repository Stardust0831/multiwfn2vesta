"""Align ABACUS electrostatic-potential cube zero to a vacuum plateau."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, NamedTuple, Optional, Sequence, Tuple


AXIS_TO_INDEX = {"x": 0, "y": 1, "z": 2}


class CubeGrid(NamedTuple):
    natoms: int
    counts: Tuple[int, int, int]
    header: Tuple[str, ...]


class AlignmentResult(NamedTuple):
    output_cube: Path
    profile_path: Optional[Path]
    report_path: Optional[Path]
    axis: str
    vacuum_offset: float
    vacuum_start: int
    vacuum_end: int
    data_min_before: float
    data_max_before: float
    data_min_after: float
    data_max_after: float
    point_count: int


@dataclass(frozen=True)
class PlanarProfile:
    sums: List[float]
    counts: List[int]

    @property
    def means(self) -> List[float]:
        return [total / count if count else 0.0 for total, count in zip(self.sums, self.counts)]


def _read_cube_grid(path: Path) -> CubeGrid:
    with path.open(encoding="utf-8", errors="replace") as handle:
        header: List[str] = []
        for _ in range(2):
            line = handle.readline()
            if not line:
                raise ValueError(f"Cannot read cube comments from {path}")
            header.append(line)
        origin = handle.readline()
        if not origin:
            raise ValueError(f"Cannot read cube origin line from {path}")
        fields = origin.split()
        if len(fields) < 4:
            raise ValueError(f"Malformed cube origin line in {path}: {origin.rstrip()}")
        natoms = abs(int(fields[0]))
        header.append(origin)
        counts: List[int] = []
        for _ in range(3):
            line = handle.readline()
            if not line:
                raise ValueError(f"Cannot read cube grid line from {path}")
            fields = line.split()
            if len(fields) < 4:
                raise ValueError(f"Malformed cube grid line in {path}: {line.rstrip()}")
            counts.append(abs(int(fields[0])))
            header.append(line)
        for _ in range(natoms):
            line = handle.readline()
            if not line:
                raise ValueError(f"Cannot read cube atom block from {path}")
            header.append(line)
    return CubeGrid(natoms=natoms, counts=(counts[0], counts[1], counts[2]), header=tuple(header))


def _iter_cube_values(path: Path, header_lines: int) -> Iterable[float]:
    with path.open(encoding="utf-8", errors="replace") as handle:
        for _ in range(header_lines):
            skipped = handle.readline()
            if not skipped:
                raise ValueError(f"Cube ended before data block: {path}")
        for line in handle:
            for field in line.split():
                yield float(field)


def _flat_index_to_ijk(index: int, counts: Tuple[int, int, int]) -> Tuple[int, int, int]:
    nx, ny, nz = counts
    i = index // (ny * nz)
    rem = index - i * ny * nz
    j = rem // nz
    k = rem - j * nz
    return i, j, k


def planar_average(path: Path, axis: str = "z") -> Tuple[PlanarProfile, float, float, int]:
    grid = _read_cube_grid(path)
    axis_index = AXIS_TO_INDEX[axis]
    nplanes = grid.counts[axis_index]
    sums = [0.0 for _ in range(nplanes)]
    counts = [0 for _ in range(nplanes)]
    data_min: Optional[float] = None
    data_max: Optional[float] = None
    nvalues = 0

    for nvalues, value in enumerate(_iter_cube_values(path, len(grid.header)), start=1):
        plane = _flat_index_to_ijk(nvalues - 1, grid.counts)[axis_index]
        sums[plane] += value
        counts[plane] += 1
        data_min = value if data_min is None else min(data_min, value)
        data_max = value if data_max is None else max(data_max, value)

    expected = grid.counts[0] * grid.counts[1] * grid.counts[2]
    if nvalues != expected:
        raise ValueError(f"Cube data point count mismatch in {path}: got {nvalues}, expected {expected}")
    if data_min is None or data_max is None:
        raise ValueError(f"Cube has no data values: {path}")
    return PlanarProfile(sums=sums, counts=counts), data_min, data_max, nvalues


def _window_bounds(nplanes: int, side: str, fraction: float, start: Optional[int], end: Optional[int]) -> Tuple[int, int]:
    if start is not None or end is not None:
        if start is None or end is None:
            raise ValueError("Both --vacuum-start and --vacuum-end must be supplied when either is used")
        if start < 0 or end <= start or end > nplanes:
            raise ValueError(f"Invalid vacuum plane window [{start}, {end}) for {nplanes} planes")
        return start, end
    width = max(1, int(round(nplanes * fraction)))
    width = min(width, nplanes)
    if side == "low":
        return 0, width
    if side == "high":
        return nplanes - width, nplanes
    if side == "both":
        return -width, width
    raise ValueError(f"Unknown vacuum side: {side}")


def choose_vacuum_offset(
    means: Sequence[float],
    *,
    side: str = "high",
    fraction: float = 0.1,
    start: Optional[int] = None,
    end: Optional[int] = None,
) -> Tuple[float, int, int]:
    if not means:
        raise ValueError("Cannot choose vacuum offset from an empty planar profile")
    if fraction <= 0 or fraction > 1:
        raise ValueError("--vacuum-fraction must be in (0, 1]")
    nplanes = len(means)
    low, high = _window_bounds(nplanes, side, fraction, start, end)
    if low < 0:
        width = high
        selected = list(means[:width]) + list(means[nplanes - width :])
        start_out, end_out = 0, nplanes
    else:
        selected = list(means[low:high])
        start_out, end_out = low, high
    if not selected:
        raise ValueError("Selected vacuum plane window is empty")
    return sum(selected) / len(selected), start_out, end_out


def subtract_cube_constant(input_cube: Path, output_cube: Path, offset: float) -> Tuple[float, float, int]:
    grid = _read_cube_grid(input_cube)
    output_cube.parent.mkdir(parents=True, exist_ok=True)
    data_min: Optional[float] = None
    data_max: Optional[float] = None
    count = 0
    row: List[float] = []
    with output_cube.open("w", encoding="utf-8", newline="\n") as handle:
        for idx, line in enumerate(grid.header):
            if idx == 0:
                handle.write("Vacuum-zero aligned ABACUS electrostatic potential cube\n")
            elif idx == 1:
                handle.write(f"Original comment: {line.rstrip()} | subtracted offset {offset:.12E}\n")
            else:
                handle.write(line if line.endswith("\n") else line + "\n")
        for value in _iter_cube_values(input_cube, len(grid.header)):
            shifted = value - offset
            data_min = shifted if data_min is None else min(data_min, shifted)
            data_max = shifted if data_max is None else max(data_max, shifted)
            count += 1
            row.append(shifted)
            if len(row) == 6:
                handle.write("".join(f" {item:13.6E}" for item in row) + "\n")
                row = []
        if row:
            handle.write("".join(f" {item:13.6E}" for item in row) + "\n")
    expected = grid.counts[0] * grid.counts[1] * grid.counts[2]
    if count != expected:
        raise ValueError(f"Cube data point count mismatch in {input_cube}: got {count}, expected {expected}")
    if data_min is None or data_max is None:
        raise ValueError(f"No cube data values were written from {input_cube}")
    return data_min, data_max, count


def write_profile_csv(path: Path, means: Sequence[float], axis: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(f"plane_index,{axis}_plane_average\n")
        for index, value in enumerate(means):
            handle.write(f"{index},{value:.12E}\n")


def write_report(path: Path, result: AlignmentResult, input_cube: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# ABACUS ESP Vacuum Alignment Report",
        "",
        f"- input_cube: `{input_cube}`",
        f"- output_cube: `{result.output_cube}`",
        f"- axis: `{result.axis}`",
        f"- vacuum_plane_window: `{result.vacuum_start}:{result.vacuum_end}`",
        f"- subtracted_offset: `{result.vacuum_offset:.12E}`",
        f"- data_min_before: `{result.data_min_before:.12E}`",
        f"- data_max_before: `{result.data_max_before:.12E}`",
        f"- data_min_after: `{result.data_min_after:.12E}`",
        f"- data_max_after: `{result.data_max_after:.12E}`",
        f"- point_count: `{result.point_count}`",
        "",
        "The shifted cube is intended for ESP texture coloring.  For slab systems,",
        "choose the vacuum side/window from the flat region of the planar-average",
        "profile so the vacuum reference is approximately zero.",
        "",
    ]
    if result.profile_path is not None:
        lines.append(f"- planar_profile_csv: `{result.profile_path}`")
    path.write_text("\n".join(lines), encoding="utf-8")


def align_cube(
    input_cube: Path,
    output_cube: Path,
    *,
    axis: str = "z",
    vacuum_side: str = "high",
    vacuum_fraction: float = 0.1,
    vacuum_start: Optional[int] = None,
    vacuum_end: Optional[int] = None,
    profile_csv: Optional[Path] = None,
    report_md: Optional[Path] = None,
) -> AlignmentResult:
    axis = axis.lower()
    if axis not in AXIS_TO_INDEX:
        raise ValueError("--axis must be x, y, or z")
    profile, before_min, before_max, point_count = planar_average(input_cube, axis=axis)
    means = profile.means
    offset, start, end = choose_vacuum_offset(
        means,
        side=vacuum_side,
        fraction=vacuum_fraction,
        start=vacuum_start,
        end=vacuum_end,
    )
    after_min, after_max, written_count = subtract_cube_constant(input_cube, output_cube, offset)
    if written_count != point_count:
        raise ValueError("Internal point-count mismatch while writing shifted cube")
    if profile_csv is not None:
        write_profile_csv(profile_csv, means, axis)
    result = AlignmentResult(
        output_cube=output_cube,
        profile_path=profile_csv,
        report_path=report_md,
        axis=axis,
        vacuum_offset=offset,
        vacuum_start=start,
        vacuum_end=end,
        data_min_before=before_min,
        data_max_before=before_max,
        data_min_after=after_min,
        data_max_after=after_max,
        point_count=point_count,
    )
    if report_md is not None:
        write_report(report_md, result, input_cube)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Shift an ABACUS electrostatic-potential cube so the vacuum planar-average plateau is zero.",
    )
    parser.add_argument("input_cube", type=Path, help="ABACUS electrostatic potential cube, e.g. potes.cube")
    parser.add_argument("output_cube", type=Path, help="shifted output cube")
    parser.add_argument("--axis", choices=("x", "y", "z"), default="z", help="vacuum/slab normal axis")
    parser.add_argument(
        "--vacuum-side",
        choices=("low", "high", "both"),
        default="high",
        help="which side of the cell is vacuum when an explicit window is not supplied",
    )
    parser.add_argument(
        "--vacuum-fraction",
        type=float,
        default=0.1,
        help="fraction of planes used from the selected vacuum side",
    )
    parser.add_argument("--vacuum-start", type=int, help="explicit first vacuum plane index, inclusive")
    parser.add_argument("--vacuum-end", type=int, help="explicit last vacuum plane index, exclusive")
    parser.add_argument("--profile-csv", type=Path, help="write planar-average profile CSV")
    parser.add_argument("--report-md", type=Path, help="write markdown alignment report")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = align_cube(
            args.input_cube,
            args.output_cube,
            axis=args.axis,
            vacuum_side=args.vacuum_side,
            vacuum_fraction=args.vacuum_fraction,
            vacuum_start=args.vacuum_start,
            vacuum_end=args.vacuum_end,
            profile_csv=args.profile_csv,
            report_md=args.report_md,
        )
    except Exception as exc:  # pragma: no cover - CLI error path
        parser.error(str(exc))
    print(f"Wrote shifted cube: {result.output_cube}")
    print(f"Subtracted vacuum offset: {result.vacuum_offset:.12E}")
    print(f"Plane window: {result.vacuum_start}:{result.vacuum_end} along {result.axis}")
    print(f"Range before: {result.data_min_before:.6E} .. {result.data_max_before:.6E}")
    print(f"Range after:  {result.data_min_after:.6E} .. {result.data_max_after:.6E}")
    if result.profile_path is not None:
        print(f"Wrote planar profile: {result.profile_path}")
    if result.report_path is not None:
        print(f"Wrote report: {result.report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
