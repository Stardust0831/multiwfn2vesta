"""Curated example index for real multiwfn2vesta workflows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = PROJECT_ROOT.parent


DOCS = {
    "manual_zh": "docs/manual_zh.md",
    "gallery_zh": "docs/example_gallery_zh.md",
    "status_matrix_zh": "docs/example_status_matrix_zh.md",
    "examples_plan_zh": "examples/README_zh.md",
}


EXAMPLES: List[Dict[str, object]] = [
    {
        "id": "ag111_benzene_igmh_aim",
        "status": "ready",
        "priority": 1,
        "title": "Ag(111)+benzene IGMH+AIM three-view overlay",
        "system": "Ag(111)+benzene periodic slab",
        "route": "ABACUS LCAO Molden -> Multiwfn IGMH/AIM -> VESTA three views",
        "runbook": "examples/ag111_benzene_igmh_aim/README_zh.md",
        "gallery": [
            "docs/assets/gallery/ag111_benzene_igmh_aim_front.png",
            "docs/assets/gallery/ag111_benzene_igmh_aim_right.png",
            "docs/assets/gallery/ag111_benzene_igmh_aim_top.png",
        ],
        "smoke": [
            "../smoke/abacus_server_artifacts_20260606/ag111_benzene/ag111_benzene_lcao_cont3_nval.molden",
            "../smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/products/dg_inter.cub",
            "../smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/products/sl2r.cub",
            "../smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_cli_rotate_split_bcp_final_20260609/",
        ],
        "note": "Best current ABACUS-driven showcase; camera can still be tightened in a future render pass.",
        "next": "Promote the full command history and a tighter camera render into a formal reproducible example.",
    },
    {
        "id": "gc_aim",
        "status": "ready",
        "priority": 2,
        "title": "GC base-pair AIM paths and BCP overlay",
        "system": "GC base pair",
        "route": "Multiwfn AIM paths.pdb/CPs.pdb -> atoms-only VESTA overlay",
        "runbook": "examples/gc_aim/README_zh.md",
        "gallery": ["docs/assets/gallery/gc_aim_overlay.png"],
        "smoke": ["../smoke/20260605_sob445_more_aim_examples/gc/"],
        "note": "Preferred molecular AIM manual example because it has intermolecular hydrogen-bond topology.",
        "next": "Render a cleaner manual figure without duplicate axis clutter.",
    },
    {
        "id": "cdcl_trajectory_video",
        "status": "ready",
        "priority": 3,
        "title": "Cd/Cl trajectory frames and high-bitrate VESTA video",
        "system": "Cd/Cl ASE trajectory",
        "route": "ASE trajectory -> VESTA frames -> PNG sequence -> MP4",
        "runbook": "examples/cdcl_trajectory_video/README_zh.md",
        "gallery": [
            "docs/assets/gallery/cdcl_nvt_trajectory_frame.png",
            "docs/assets/gallery/cdcl_trajectory_frame.png",
        ],
        "smoke": [
            "../smoke/vesta_trajectory_video_1608/ase_nvt_refstyle_stride20_cdcl3p50/ase_nvt_refstyle_stride20_cdcl3p50_hq20m.mp4",
            "../smoke/vesta_trajectory_video_1608/ase_nvt_refstyle_stride20_cdcl3p50/png/frame_0001.png",
        ],
        "note": "Good trajectory/video evidence; the actual video is intentionally not committed because it is large.",
        "next": "Turn the frame patching and ffmpeg sequence into a maintained CLI.",
    },
    {
        "id": "benzene_aim",
        "status": "ready",
        "priority": 4,
        "title": "Benzene AIM basic overlay",
        "system": "benzene",
        "route": "Multiwfn AIM paths.pdb/CPs.pdb -> atoms-only VESTA overlay",
        "runbook": "examples/README_zh.md",
        "gallery": ["docs/assets/gallery/benzene_aim_overlay.png"],
        "smoke": ["../smoke/20260605_sob445_more_aim_examples/benzene/"],
        "note": "Small basic AIM example; GC is the better showcase.",
        "next": "Split into a dedicated runbook if this becomes a tutorial fixture.",
    },
    {
        "id": "h2o_hf_iri_aim_debug",
        "status": "needs-work",
        "priority": 5,
        "title": "H2O-HF IRI+AIM debug overlay",
        "system": "H2O-HF",
        "route": "IRI surface/texture cubes plus AIM overlay",
        "runbook": "examples/README_zh.md",
        "gallery": ["docs/assets/gallery/h2o_iri_aim_overlay.png"],
        "smoke": ["../smoke/20260605_iri_aim_h2o_hf/products/"],
        "note": "Useful evidence for cube-frame alignment and texture-range debugging, not a finished showcase.",
        "next": "Fix VESTA SURFS/SECTS/TEX3P styling and rerender a readable IRI+AIM figure.",
    },
    {
        "id": "phenanthrene_aim_view_fix",
        "status": "needs-work",
        "priority": 6,
        "title": "Phenanthrene AIM overlay needing a better view",
        "system": "phenanthrene",
        "route": "Multiwfn AIM paths.pdb/CPs.pdb -> VESTA overlay",
        "runbook": "examples/README_zh.md",
        "gallery": ["docs/assets/gallery/phenanthrene_aim_overlay.png"],
        "smoke": ["../smoke/20260605_sob445_more_aim_examples/phenanthrene/"],
        "note": "Rendered evidence exists, but the current camera is not good enough for the main manual.",
        "next": "Rerender with a planar or oblique view before promoting.",
    },
    {
        "id": "mulliken_coloring_toy",
        "status": "needs-work",
        "priority": 7,
        "title": "ABACUS Mulliken atom coloring smoke",
        "system": "two-atom Fe toy",
        "route": "ABACUS mulliken.txt -> VESTA SITET atom colors",
        "runbook": "examples/README_zh.md",
        "gallery": [],
        "smoke": ["../smoke/abacus_mulliken_color_smoke_20260610/"],
        "note": "Parser and VESTA color patching are proven, but this is not a chemical showcase.",
        "next": "Use a real magnetic or charged ABACUS system, add a PNG, legend, and color scale.",
    },
    {
        "id": "benzene_nics_vector_misc",
        "status": "misc",
        "priority": 8,
        "title": "Benzene NICS/vector VESTA prototype",
        "system": "benzene",
        "route": "VESTA vector/arrow style prototype",
        "runbook": "examples/README_zh.md",
        "gallery": ["docs/assets/gallery/benzene_nics_vector.png"],
        "smoke": ["../smoke/20260605_nics_vesta_vectors/"],
        "note": "Kept as miscellaneous vector-format evidence; not part of maintained main code for now.",
        "next": "Only revive after real NICS/current data are ready.",
    },
]


def _project_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return (PROJECT_ROOT / path).resolve()


def _display_path(path_text: str, absolute: bool = False) -> str:
    path = Path(path_text)
    if path.is_absolute():
        return str(path)
    base = PROJECT_ROOT
    resolved = (base / path).resolve()
    if absolute:
        return str(resolved)
    return path_text


def _iter_examples(status: str = "all") -> Iterable[Dict[str, object]]:
    for example in sorted(EXAMPLES, key=lambda item: int(item["priority"])):
        if status == "all" or example["status"] == status:
            yield example


def examples_for_json(status: str = "all", absolute: bool = False) -> List[Dict[str, object]]:
    records: List[Dict[str, object]] = []
    for example in _iter_examples(status):
        record = dict(example)
        for key in ("runbook",):
            record[key] = _display_path(str(record[key]), absolute=absolute)
        for key in ("gallery", "smoke"):
            record[key] = [_display_path(str(item), absolute=absolute) for item in record.get(key, [])]  # type: ignore[arg-type]
        records.append(record)
    return records


def _print_text(status: str = "all", absolute: bool = False) -> None:
    print("multiwfn2vesta curated examples\n")
    print("Docs:")
    for label, path in DOCS.items():
        print(f"  {label}: {_display_path(path, absolute=absolute)}")
    print()
    print("Examples:")
    for example in _iter_examples(status):
        print(f"- [{example['status']}] {example['id']}: {example['title']}")
        print(f"  system: {example['system']}")
        print(f"  route: {example['route']}")
        print(f"  runbook: {_display_path(str(example['runbook']), absolute=absolute)}")
        gallery = example.get("gallery") or []
        if gallery:
            print("  gallery:")
            for item in gallery:  # type: ignore[assignment]
                print(f"    - {_display_path(str(item), absolute=absolute)}")
        smoke = example.get("smoke") or []
        if smoke:
            print("  smoke evidence:")
            for item in smoke:  # type: ignore[assignment]
                print(f"    - {_display_path(str(item), absolute=absolute)}")
        print(f"  note: {example['note']}")
        print(f"  next: {example['next']}")
    print()
    print("Use --status ready, --status needs-work, or --status misc to filter.")
    print("Use --json for machine-readable output.")


def _verify_project_files(status: str = "all") -> int:
    missing: List[str] = []
    for path in DOCS.values():
        if not _project_path(path).exists():
            missing.append(path)
    for example in _iter_examples(status):
        runbook = str(example["runbook"])
        if not _project_path(runbook).exists():
            missing.append(runbook)
        for image in example.get("gallery", []):  # type: ignore[assignment]
            if not _project_path(str(image)).exists():
                missing.append(str(image))
    if missing:
        print("Missing project files:")
        for item in missing:
            print(f"- {item}")
        return 1
    print("Project example docs and gallery files are present.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List curated multiwfn2vesta examples and their documentation paths.",
    )
    parser.add_argument(
        "--status",
        choices=["all", "ready", "needs-work", "misc"],
        default="all",
        help="Filter examples by current documentation status.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--absolute", action="store_true", help="Print absolute paths.")
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Check that project-local runbooks and gallery assets exist.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.verify:
        return _verify_project_files(args.status)
    if args.json:
        print(json.dumps(examples_for_json(args.status, absolute=args.absolute), ensure_ascii=False, indent=2))
    else:
        _print_text(args.status, absolute=args.absolute)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
