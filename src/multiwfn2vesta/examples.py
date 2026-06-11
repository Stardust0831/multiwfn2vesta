"""Curated example index for real multiwfn2vesta workflows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Dict, Iterable, List, Optional, Sequence, Set


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = PROJECT_ROOT.parent


DOCS = {
    "manual_zh": "docs/manual_zh.md",
    "gallery_zh": "docs/example_gallery_zh.md",
    "status_matrix_zh": "docs/example_status_matrix_zh.md",
    "feature_examples_zh": "docs/feature_examples_zh.md",
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
        "system": "Cd/Cl trajectory",
        "route": "XYZ/extXYZ trajectory -> VESTA frames -> PNG sequence -> MP4",
        "runbook": "examples/cdcl_trajectory_video/README_zh.md",
        "manifest": "examples/cdcl_trajectory_video/artifact_manifest.json",
        "gallery": [
            "docs/assets/gallery/cdcl_nvt_trajectory_frame.png",
            "docs/assets/gallery/cdcl_trajectory_frame.png",
        ],
        "smoke": [
            "../smoke/vesta_trajectory_video_1608/ase_nvt_refstyle_stride20_cdcl3p50/ase_nvt_refstyle_stride20_cdcl3p50_hq20m.mp4",
            "../smoke/vesta_trajectory_video_1608/ase_nvt_refstyle_stride20_cdcl3p50/png/frame_0001.png",
            "../smoke/vesta_trajectory_video_1608/ase_nvt_refstyle_stride20_cdcl3p50/patched/",
            "../smoke/vesta_trajectory_video_1608/ase_npt_refstyle_stride20/ase_npt_refstyle_stride20_hq20m.mp4",
        ],
        "note": "Good trajectory/video evidence; XYZ/extXYZ frame writing and MP4 encoding now have maintained wrappers.",
        "next": "Add direct ASE .traj reading and a non-focus-stealing VESTA PNG rendering layer.",
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


FEATURE_COVERAGE: List[Dict[str, object]] = [
    {
        "command": "discover",
        "feature": "Multiwfn/VESTA executable discovery",
        "status": "linked",
        "example": "Ag(111)+benzene and all local workflows",
        "system": "workspace-local executables",
        "runbook": "docs/manual_zh.md",
        "gallery": [],
        "next": "Add a short Chinese command-output fixture if screenshots become useful.",
    },
    {
        "command": "abacus-molden",
        "feature": "ABACUS LCAO Molden handoff",
        "status": "linked",
        "example": "ag111_benzene_igmh_aim",
        "system": "Ag(111)+benzene periodic slab",
        "runbook": "examples/ag111_benzene_igmh_aim/README_zh.md",
        "gallery": ["docs/assets/gallery/ag111_benzene_igmh_aim_front.png"],
        "next": "Promote the full ABACUS directory transcript into the runbook without committing large wavefunction files.",
    },
    {
        "command": "molden-check",
        "feature": "Molden structure and ABACUS [Nval] validation",
        "status": "linked",
        "example": "ag111_benzene_igmh_aim",
        "system": "Ag(111)+benzene ABACUS Molden",
        "runbook": "examples/ag111_benzene_igmh_aim/README_zh.md",
        "gallery": ["docs/assets/gallery/ag111_benzene_igmh_aim_front.png"],
        "next": "Record one successful check output block in the Chinese manual.",
    },
    {
        "command": "cube-vesta",
        "feature": "Generic cube to VESTA isosurface",
        "status": "linked",
        "example": "h2o_hf_iri_aim_debug",
        "system": "H2O-HF IRI surface cube",
        "runbook": "docs/example_gallery_zh.md",
        "gallery": ["docs/assets/gallery/h2o_iri_aim_overlay.png"],
        "next": "Render a cleaner standalone cube figure that is not tied to IRI debugging.",
    },
    {
        "command": "cube-preset",
        "feature": "Analysis presets for scalar/signed/mapped cube display",
        "status": "linked",
        "example": "ag111_benzene_igmh_aim; h2o_hf_iri_aim_debug",
        "system": "Ag(111)+benzene IGMH and H2O-HF IRI",
        "runbook": "docs/example_status_matrix_zh.md",
        "gallery": [
            "docs/assets/gallery/ag111_benzene_igmh_aim_front.png",
            "docs/assets/gallery/h2o_iri_aim_overlay.png",
        ],
        "next": "Add direct ABACUS cube examples for charge density, potential, ELF, and wavefunction norm.",
    },
    {
        "command": "surface-extrema",
        "feature": "Multiwfn surfanalysis extrema overlay",
        "status": "needs-render",
        "example": "planned ALIE/LEA surface extrema",
        "system": "polar aromatic molecule or adsorption interface",
        "runbook": "docs/skills/surface_extrema_vesta_skill.md",
        "gallery": [],
        "next": "Generate ALIE/LEA/LEAE surface extrema from a real molecule and render minima/maxima markers.",
    },
    {
        "command": "cube-arith",
        "feature": "Density difference, spin density, Fukui, and dual cube arithmetic",
        "status": "needs-example",
        "example": "planned Fukui/dual descriptor molecule",
        "system": "reactive aromatic or heteroatom-rich molecule with neutral/anion/cation states",
        "runbook": "docs/usage.md",
        "gallery": [],
        "next": "Prepare charged-state cubes and render Fukui+/Fukui-/dual maps.",
    },
    {
        "command": "iri-run",
        "feature": "IRI/RDG cube generation and VESTA mapped surface",
        "status": "needs-render",
        "example": "h2o_hf_iri_aim_debug",
        "system": "H2O-HF hydrogen-bond complex",
        "runbook": "docs/iri_vesta_coloring.md",
        "gallery": ["docs/assets/gallery/h2o_iri_aim_overlay.png"],
        "next": "Rerender with a clear IRI isosurface and validated texture range before marking ready.",
    },
    {
        "command": "igmh-run/igm-run/migm-run",
        "feature": "Fragment weak-interaction cubes",
        "status": "ready",
        "example": "ag111_benzene_igmh_aim",
        "system": "Ag(111)+benzene periodic slab",
        "runbook": "examples/ag111_benzene_igmh_aim/README_zh.md",
        "gallery": [
            "docs/assets/gallery/ag111_benzene_igmh_aim_front.png",
            "docs/assets/gallery/ag111_benzene_igmh_aim_right.png",
            "docs/assets/gallery/ag111_benzene_igmh_aim_top.png",
        ],
        "next": "Keep Ag(111)+benzene as the main periodic showcase; add a small molecular dimer for fast smoke reruns.",
    },
    {
        "command": "aigm-run/amigm-run",
        "feature": "Trajectory-average weak-interaction cubes",
        "status": "needs-example",
        "example": "planned short trajectory averaged IGM",
        "system": "Cd/Cl trajectory or Ag(111)+benzene AIMD excerpt",
        "runbook": "docs/usage.md",
        "gallery": [],
        "next": "Use a short real trajectory to generate averaged cubes and a VESTA mapped surface.",
    },
    {
        "command": "grid-run",
        "feature": "Multiwfn real-space scalar functions",
        "status": "needs-render",
        "example": "planned H2O/benzene/Ag(111)+benzene grid suite",
        "system": "H2O for density/KED/ESP, benzene for orbital/Fukui, Ag(111)+benzene for vdW/ESP",
        "runbook": "docs/feature_examples_zh.md",
        "gallery": [],
        "next": "Render one compact suite covering density/orbital/spin/KED/ELF/ESP/vdW/FOD/information-density groups.",
    },
    {
        "command": "grid-run --function rose/sedd",
        "feature": "Region of Slow Electrons and single exponential decay detector scalar fields",
        "status": "needs-render",
        "example": "planned benzene dimer or GC weak-interaction scalar comparison",
        "system": "benzene dimer, GC base pair, or another weak-interaction/aromatic system",
        "runbook": "docs/feature_examples_zh.md",
        "gallery": [],
        "next": "Use validated Molden input to generate RoSE and SEDD cubes, tune the default 0.5 isosurface, and render a paired figure.",
    },
    {
        "command": "fukui-run",
        "feature": "Charged-state Fukui and dual descriptor maps",
        "status": "needs-example",
        "example": "planned electrophilic/nucleophilic molecule",
        "system": "heteroatom-rich aromatic molecule with neutral, anion, and cation wavefunctions",
        "runbook": "docs/usage.md",
        "gallery": [],
        "next": "Compute aligned charged-state density cubes and render Fukui+/Fukui-/dual descriptor surfaces.",
    },
    {
        "command": "stm-run",
        "feature": "Constant-current STM/LDOS cube export",
        "status": "needs-render",
        "example": "planned surface or adsorbate STM",
        "system": "Ag(111)+benzene or a smaller aromatic molecule near a surface",
        "runbook": "docs/skills/multiwfn_stm_run_skill.md",
        "gallery": [],
        "next": "Choose a physically meaningful LDOS window and render the constant-current isosurface.",
    },
    {
        "command": "domain-run",
        "feature": "Cube domain extraction and binary domain display",
        "status": "needs-render",
        "example": "planned H2O density domain",
        "system": "H2O electron-density domain",
        "runbook": "docs/skills/multiwfn_domain_run_skill.md",
        "gallery": [],
        "next": "Render the domain cube and document the selected domain criterion.",
    },
    {
        "command": "abacus-mulliken-color",
        "feature": "ABACUS Mulliken charge/magnetism atom coloring",
        "status": "needs-render",
        "example": "planned charged or magnetic ABACUS system",
        "system": "magnetic oxide/metal cluster or charged adsorbate system",
        "runbook": "docs/vesta_atom_value_coloring.md",
        "gallery": [],
        "next": "Replace the toy Fe smoke with a real charge or spin-density coloring figure and legend.",
    },
    {
        "command": "multiwfn-atom-color",
        "feature": "Generic atom scalar table coloring",
        "status": "needs-render",
        "example": "planned Multiwfn charge/Fukui atom table",
        "system": "reactive molecule with atom charges or condensed Fukui values",
        "runbook": "docs/vesta_atom_value_coloring.md",
        "gallery": [],
        "next": "Connect a real Multiwfn population table and render a colored molecular structure.",
    },
    {
        "command": "aim-run",
        "feature": "Multiwfn AIM topology generation",
        "status": "ready",
        "example": "gc_aim",
        "system": "GC base pair",
        "runbook": "examples/gc_aim/README_zh.md",
        "gallery": ["docs/assets/gallery/gc_aim_overlay.png"],
        "next": "Use GC as the main hydrogen-bond topology tutorial and keep benzene as the basic check.",
    },
    {
        "command": "aim-pdb",
        "feature": "AIM paths.pdb/CPs.pdb atoms-only VESTA conversion",
        "status": "ready",
        "example": "gc_aim; benzene_aim",
        "system": "GC base pair and benzene",
        "runbook": "examples/gc_aim/README_zh.md",
        "gallery": [
            "docs/assets/gallery/gc_aim_overlay.png",
            "docs/assets/gallery/benzene_aim_overlay.png",
        ],
        "next": "Add a compact CP color/type legend to the manual.",
    },
    {
        "command": "aim-igmh",
        "feature": "Saved AIM+IGMH overlay styling and three-view rendering",
        "status": "ready",
        "example": "ag111_benzene_igmh_aim",
        "system": "Ag(111)+benzene periodic slab",
        "runbook": "examples/ag111_benzene_igmh_aim/README_zh.md",
        "gallery": [
            "docs/assets/gallery/ag111_benzene_igmh_aim_front.png",
            "docs/assets/gallery/ag111_benzene_igmh_aim_right.png",
            "docs/assets/gallery/ag111_benzene_igmh_aim_top.png",
        ],
        "next": "Continue improving non-focus-stealing rendering and camera presets.",
    },
    {
        "command": "trajectory-frames",
        "feature": "XYZ/extXYZ trajectory to VESTA frame files",
        "status": "ready",
        "example": "cdcl_trajectory_video",
        "system": "Cd/Cl NVT/NPT trajectory",
        "runbook": "examples/cdcl_trajectory_video/README_zh.md",
        "gallery": ["docs/assets/gallery/cdcl_nvt_trajectory_frame.png"],
        "next": "Add direct ASE .traj reading when a stable dependency policy is chosen.",
    },
    {
        "command": "trajectory-video",
        "feature": "Rendered PNG frame sequence to high-bitrate MP4",
        "status": "ready",
        "example": "cdcl_trajectory_video",
        "system": "Cd/Cl VESTA trajectory frames",
        "runbook": "examples/cdcl_trajectory_video/README_zh.md",
        "gallery": ["docs/assets/gallery/cdcl_nvt_trajectory_frame.png"],
        "next": "Add an optional VESTA PNG rendering layer that does not steal focus when possible.",
    },
    {
        "command": "examples",
        "feature": "Curated example, gallery, feature-coverage, and real-system discovery",
        "status": "ready",
        "example": "project example index",
        "system": "maintained real-system gallery",
        "runbook": "docs/feature_examples_zh.md",
        "gallery": ["docs/assets/gallery/current_feature_overview.png"],
        "next": "Keep the coverage table synchronized whenever a workflow gains or loses ready example status.",
    },
]


SYSTEM_RECOMMENDATIONS: List[Dict[str, object]] = [
    {
        "id": "ag111_benzene",
        "priority": 1,
        "title": "Ag(111)+benzene periodic adsorption slab",
        "value": "Best current end-to-end periodic showcase for ABACUS LCAO Molden, fragment weak interactions, AIM topology, vdW/ESP fields, and three-view VESTA figures.",
        "covers": [
            "abacus-molden",
            "molden-check",
            "igmh-run",
            "aim-run",
            "aim-igmh",
            "grid-run vdW/ESP",
        ],
        "example": "ag111_benzene_igmh_aim",
        "status": "ready-core; more scalar renders pending",
        "next": "Use the same validated Molden/cell to add vdW component, ESP, electric-field, and steric/SBL figures without changing the main showcase system.",
    },
    {
        "id": "gc_base_pair",
        "priority": 2,
        "title": "GC base pair",
        "value": "Compact molecular hydrogen-bond topology system with meaningful AIM BCPs and a natural target for IRI/RDG, ESP-on-density, and RoSE/SEDD paired figures.",
        "covers": ["aim-run", "aim-pdb", "iri-run", "grid-run rose/sedd", "surface-extrema"],
        "example": "gc_aim",
        "status": "ready AIM; IRI/grid renders pending",
        "next": "Promote GC from AIM-only to a paired AIM + weak-interaction scalar tutorial after a clean IRI/RoSE/SEDD render.",
    },
    {
        "id": "benzene_dimer",
        "priority": 3,
        "title": "Benzene dimer or substituted aromatic dimer",
        "value": "Small, interpretable dispersion/pi-stacking system for RDG/IRI/DORI/Delta-g, RoSE/SEDD, vdW potential, and orbital/Fukui demonstrations.",
        "covers": ["iri-run", "grid-run", "cube-preset", "cube-arith", "fukui-run"],
        "example": "planned_benzene_dimer_scalar_suite",
        "status": "recommended; not yet rendered",
        "next": "Prepare one validated Molden and reuse it for a compact scalar-field gallery instead of creating one toy per scalar.",
    },
    {
        "id": "h2o_hf_complex",
        "priority": 4,
        "title": "H2O-HF hydrogen-bond complex",
        "value": "Fast weak-interaction regression system; already useful for IRI texture range, section suppression, and AIM/cube alignment debugging.",
        "covers": ["iri-run", "aim-pdb", "cube-vesta", "cube-preset"],
        "example": "h2o_hf_iri_aim_debug",
        "status": "debug render only",
        "next": "Keep as a fast regression fixture, but do not use it as the main manual figure until IRI surface visibility is fixed.",
    },
    {
        "id": "cof_12000n2_monolayer",
        "priority": 5,
        "title": "COF_12000N2 monolayer with vacuum",
        "value": "Periodic porous 2D material candidate for ABACUS direct electron density, electrostatic potential, ELF/LOL, partial charge, and atom-coloring examples.",
        "covers": ["cube-vesta", "cube-preset", "grid-run ELF/ESP", "abacus-mulliken-color", "multiwfn-atom-color"],
        "example": "planned_cof_direct_cube_suite",
        "status": "recommended; calculation/render pending",
        "next": "Use a clean single-layer cell and commit only light runbooks/gallery PNGs, not full ABACUS wavefunction outputs.",
    },
    {
        "id": "open_shell_or_magnetic_system",
        "priority": 6,
        "title": "Open-shell molecule, magnetic oxide, or spin-polarized adsorbate",
        "value": "Needed for spin-density, alpha/beta density, spin-polarization, Mulliken magnetism coloring, and atom-table coloring figures.",
        "covers": ["grid-run spin", "cube-arith spin-density", "abacus-mulliken-color", "multiwfn-atom-color"],
        "example": "planned_spin_coloring_suite",
        "status": "missing real showcase",
        "next": "Replace the current toy Fe coloring smoke with a chemically meaningful spin or charge example plus a legend.",
    },
    {
        "id": "cdcl_trajectory",
        "priority": 7,
        "title": "Cd/Cl NVT/NPT trajectory",
        "value": "Best current video workflow system because it exercises extXYZ frames, reference VESTA style reuse, custom Cd-Cl bonding, Boundary, PNG sequence, and high-bitrate MP4.",
        "covers": ["trajectory-frames", "trajectory-video"],
        "example": "cdcl_trajectory_video",
        "status": "ready for frame/video layer",
        "next": "Add direct ASE .traj reading or a stable converter policy, then close the VESTA PNG render layer if focus stealing can be avoided.",
    },
]


COVERAGE_COMMAND_ALIASES: Dict[str, str] = {
    "where": "discover",
    "env": "discover",
    "molden": "abacus-molden",
    "abacus-multiwfn-molden": "abacus-molden",
    "check-molden": "molden-check",
    "abacus-molden-check": "molden-check",
    "cube": "cube-vesta",
    "preset": "cube-preset",
    "analysis-cube": "cube-preset",
    "surf-extrema": "surface-extrema",
    "surfanalysis-vesta": "surface-extrema",
    "cube-math": "cube-arith",
    "density-diff": "cube-arith",
    "fukui-cube": "cube-arith",
    "multiwfn-iri": "iri-run",
    "rdg-run": "iri-run",
    "multiwfn-igmh": "igmh-run",
    "multiwfn-igmh-run": "igmh-run",
    "multiwfn-igm": "igm-run",
    "multiwfn-igm-run": "igm-run",
    "multiwfn-migm": "migm-run",
    "multiwfn-migm-run": "migm-run",
    "multiwfn-aigm": "aigm-run",
    "multiwfn-aigm-run": "aigm-run",
    "averaged-igm-run": "aigm-run",
    "multiwfn-amigm": "amigm-run",
    "multiwfn-amigm-run": "amigm-run",
    "averaged-migm-run": "amigm-run",
    "multiwfn-grid": "grid-run",
    "scalar-cube-run": "grid-run",
    "function-cube": "grid-run",
    "multiwfn-fukui": "fukui-run",
    "multiwfn-fukui-run": "fukui-run",
    "dual-descriptor-run": "fukui-run",
    "multiwfn-stm": "stm-run",
    "multiwfn-stm-run": "stm-run",
    "ldos-run": "stm-run",
    "multiwfn-domain": "domain-run",
    "multiwfn-domain-run": "domain-run",
    "cube-domain": "domain-run",
    "mulliken-color": "abacus-mulliken-color",
    "atom-color": "abacus-mulliken-color",
    "multiwfn-table-color": "multiwfn-atom-color",
    "atom-table-color": "multiwfn-atom-color",
    "multiwfn-aim": "aim-run",
    "aim-vesta": "aim-pdb",
    "igmh": "aim-igmh",
    "traj-frames": "trajectory-frames",
    "xyz-vesta-frames": "trajectory-frames",
    "vesta-trajectory-frames": "trajectory-frames",
    "traj-video": "trajectory-video",
    "trajectory-mp4": "trajectory-video",
    "vesta-trajectory-video": "trajectory-video",
    "example": "examples",
    "gallery": "examples",
    "example-gallery": "examples",
}


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


def _known_ids() -> Set[str]:
    return {str(example["id"]) for example in EXAMPLES}


def _normalize_ids(ids: Optional[Sequence[str]]) -> Optional[Set[str]]:
    if not ids:
        return None
    selected: Set[str] = set()
    for item in ids:
        for part in item.split(","):
            value = part.strip()
            if value:
                selected.add(value)
    return selected or None


def _validate_ids(ids: Optional[Set[str]]) -> List[str]:
    if not ids:
        return []
    known = _known_ids()
    return sorted(item for item in ids if item not in known)


def _iter_examples(status: str = "all", ids: Optional[Set[str]] = None) -> Iterable[Dict[str, object]]:
    for example in sorted(EXAMPLES, key=lambda item: int(item["priority"])):
        if ids is not None and str(example["id"]) not in ids:
            continue
        if status == "all" or example["status"] == status:
            yield example


def examples_for_json(
    status: str = "all",
    absolute: bool = False,
    ids: Optional[Sequence[str]] = None,
) -> List[Dict[str, object]]:
    selected_ids = _normalize_ids(ids)
    records: List[Dict[str, object]] = []
    for example in _iter_examples(status, selected_ids):
        record = dict(example)
        for key in ("runbook", "manifest"):
            if key in record:
                record[key] = _display_path(str(record[key]), absolute=absolute)
        for key in ("gallery", "smoke"):
            record[key] = [_display_path(str(item), absolute=absolute) for item in record.get(key, [])]  # type: ignore[arg-type]
        records.append(record)
    return records


def _normalize_terms(values: Optional[Sequence[str]]) -> Optional[Set[str]]:
    if not values:
        return None
    terms: Set[str] = set()
    for item in values:
        for part in item.split(","):
            value = part.strip().lower()
            if value:
                terms.add(value)
    return terms or None


def _command_text_matches(term: str, command_text: str) -> bool:
    if term == command_text:
        return True
    command_parts = [part.strip() for part in command_text.replace("/", " ").split()]
    return term in command_parts or term in command_text


def _known_coverage_command_terms() -> Set[str]:
    terms = set(COVERAGE_COMMAND_ALIASES)
    for item in FEATURE_COVERAGE:
        command_text = str(item.get("command", "")).lower()
        terms.add(command_text)
        terms.update(part.strip() for part in command_text.replace("/", " ").split() if part.strip())
    return terms


def _coverage_matches_terms(record: Dict[str, object], terms: Optional[Set[str]]) -> bool:
    if not terms:
        return True
    command_text = str(record.get("command", "")).lower()
    keyword_text = " ".join(
        str(record.get(key, ""))
        for key in ("feature", "system", "next")
    ).lower()
    known_command_terms = _known_coverage_command_terms()
    for term in terms:
        canonical = COVERAGE_COMMAND_ALIASES.get(term)
        if canonical:
            if _command_text_matches(canonical, command_text):
                return True
            continue
        if term in known_command_terms:
            if _command_text_matches(term, command_text):
                return True
            continue
        if term in keyword_text:
            return True
    return False


def feature_coverage_for_json(
    status: str = "all",
    absolute: bool = False,
    needs_render: bool = False,
    commands: Optional[Sequence[str]] = None,
) -> List[Dict[str, object]]:
    command_terms = _normalize_terms(commands)
    records: List[Dict[str, object]] = []
    for item in FEATURE_COVERAGE:
        item_status = str(item["status"])
        if status != "all" and item_status != status:
            continue
        if needs_render and item_status not in {"needs-render", "needs-example"}:
            continue
        if not _coverage_matches_terms(item, command_terms):
            continue
        record = dict(item)
        record["runbook"] = _display_path(str(record["runbook"]), absolute=absolute)
        record["gallery"] = [_display_path(str(path), absolute=absolute) for path in record.get("gallery", [])]  # type: ignore[arg-type]
        records.append(record)
    return records


def gallery_for_json(
    status: str = "all",
    absolute: bool = False,
    ids: Optional[Sequence[str]] = None,
) -> List[Dict[str, object]]:
    selected_ids = _normalize_ids(ids)
    records: List[Dict[str, object]] = []
    for example in _iter_examples(status, selected_ids):
        for image in example.get("gallery", []):  # type: ignore[assignment]
            image_text = str(image)
            records.append(
                {
                    "example_id": example["id"],
                    "status": example["status"],
                    "title": example["title"],
                    "system": example["system"],
                    "image": _display_path(image_text, absolute=absolute),
                    "exists": _project_path(image_text).exists(),
                    "runbook": _display_path(str(example["runbook"]), absolute=absolute),
                    "note": example["note"],
                }
            )
    if selected_ids is None and status in {"all", "ready"}:
        image_text = "docs/assets/gallery/current_feature_overview.png"
        records.append(
            {
                "example_id": "examples",
                "status": "ready",
                "title": "Feature overview gallery",
                "system": "maintained real-system gallery",
                "image": _display_path(image_text, absolute=absolute),
                "exists": _project_path(image_text).exists(),
                "runbook": _display_path("docs/feature_examples_zh.md", absolute=absolute),
                "note": "Rendered overview assembled from committed gallery PNGs; not a separate scientific calculation.",
            }
        )
    return records


def systems_for_json() -> List[Dict[str, object]]:
    return [dict(item) for item in sorted(SYSTEM_RECOMMENDATIONS, key=lambda item: int(item["priority"]))]


def _print_text(status: str = "all", absolute: bool = False, ids: Optional[Set[str]] = None) -> None:
    print("multiwfn2vesta curated examples\n")
    print("Docs:")
    for label, path in DOCS.items():
        print(f"  {label}: {_display_path(path, absolute=absolute)}")
    print()
    print("Examples:")
    matched = False
    for example in _iter_examples(status, ids):
        matched = True
        print(f"- [{example['status']}] {example['id']}: {example['title']}")
        print(f"  system: {example['system']}")
        print(f"  route: {example['route']}")
        print(f"  runbook: {_display_path(str(example['runbook']), absolute=absolute)}")
        manifest = example.get("manifest")
        if manifest:
            print(f"  manifest: {_display_path(str(manifest), absolute=absolute)}")
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
    if not matched:
        print("  No examples match the selected filters.")
    print()
    print("Use --id EXAMPLE_ID and --status ready/needs-work/misc to filter.")
    print("Use --json for machine-readable output.")


def _print_coverage(
    status: str = "all",
    absolute: bool = False,
    needs_render: bool = False,
    commands: Optional[Sequence[str]] = None,
) -> None:
    records = feature_coverage_for_json(
        status=status,
        absolute=absolute,
        needs_render=needs_render,
        commands=commands,
    )
    print("multiwfn2vesta feature example coverage\n")
    print(f"Docs: {_display_path('docs/feature_examples_zh.md', absolute=absolute)}")
    if commands:
        print("Command filter: " + ", ".join(commands))
    print()
    if not records:
        print("No feature coverage records match the selected filters.")
        return
    for record in records:
        print(f"- [{record['status']}] {record['command']}: {record['feature']}")
        print(f"  example: {record['example']}")
        print(f"  system: {record['system']}")
        print(f"  runbook: {record['runbook']}")
        gallery = record.get("gallery") or []
        if gallery:
            print("  gallery:")
            for item in gallery:  # type: ignore[assignment]
                print(f"    - {item}")
        print(f"  next: {record['next']}")
    print()
    print("Status: ready means example + project gallery image; linked means covered through another ready workflow;")
    print("needs-render means workflow exists but needs a better project-local figure; needs-example means a real system is still missing.")


def _print_gallery(status: str = "all", absolute: bool = False, ids: Optional[Set[str]] = None) -> None:
    records = gallery_for_json(status=status, absolute=absolute, ids=sorted(ids) if ids else None)
    print("multiwfn2vesta rendered gallery assets\n")
    print(f"Docs: {_display_path('docs/example_gallery_zh.md', absolute=absolute)}")
    print()
    if not records:
        print("No gallery assets match the selected filters.")
        return
    for record in records:
        exists = "present" if record["exists"] else "missing"
        print(f"- [{record['status']}] {record['example_id']}: {record['title']}")
        print(f"  system: {record['system']}")
        print(f"  image: {record['image']} ({exists})")
        print(f"  runbook: {record['runbook']}")
        print(f"  note: {record['note']}")


def _print_systems() -> None:
    print("multiwfn2vesta recommended real systems\n")
    for item in systems_for_json():
        print(f"- {item['priority']}. {item['id']}: {item['title']}")
        print(f"  value: {item['value']}")
        print("  covers: " + ", ".join(str(value) for value in item["covers"]))  # type: ignore[index]
        print(f"  example: {item['example']}")
        print(f"  status: {item['status']}")
        print(f"  next: {item['next']}")


def _verify_project_files(status: str = "all", ids: Optional[Set[str]] = None) -> int:
    missing: List[str] = []
    for path in DOCS.values():
        if not _project_path(path).exists():
            missing.append(path)
    for example in _iter_examples(status, ids):
        runbook = str(example["runbook"])
        if not _project_path(runbook).exists():
            missing.append(runbook)
        manifest = example.get("manifest")
        if manifest and not _project_path(str(manifest)).exists():
            missing.append(str(manifest))
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


def _verify_smoke_files(status: str = "all", ids: Optional[Set[str]] = None) -> int:
    missing: List[str] = []
    checked = 0
    for example in _iter_examples(status, ids):
        for item in example.get("smoke", []):  # type: ignore[assignment]
            checked += 1
            path_text = str(item)
            if not _project_path(path_text).exists():
                missing.append(path_text)
    if missing:
        print("Missing smoke evidence:")
        for item in missing:
            print(f"- {item}")
        print()
        print("Smoke evidence is workspace-local and is not committed; rerun or restore the example smoke directory.")
        return 1
    print(f"Smoke evidence paths are present. checked={checked}")
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
    parser.add_argument(
        "--id",
        action="append",
        dest="ids",
        metavar="EXAMPLE_ID",
        help="Show or verify one example id. Can be repeated or comma-separated.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--absolute", action="store_true", help="Print absolute paths.")
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="List maintained commands/features with their recommended example systems and figure status.",
    )
    parser.add_argument(
        "--command",
        action="append",
        dest="commands",
        metavar="COMMAND_OR_TERM",
        help="Filter --coverage records by command, alias, or feature term. Implies --coverage.",
    )
    parser.add_argument(
        "--coverage-status",
        choices=["all", "ready", "linked", "needs-render", "needs-example", "misc"],
        default="all",
        help="Filter --coverage records by feature coverage status.",
    )
    parser.add_argument(
        "--needs-render",
        action="store_true",
        help="Shortcut for --coverage records that still need a real render or real example.",
    )
    parser.add_argument(
        "--gallery-assets",
        action="store_true",
        help="List project-local rendered PNG assets grouped by curated example.",
    )
    parser.add_argument(
        "--systems",
        action="store_true",
        help="List recommended real systems for closing examples instead of toy placeholders.",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Check that project-local runbooks and gallery assets exist.",
    )
    parser.add_argument(
        "--verify-smoke",
        action="store_true",
        help="Check workspace-local smoke evidence paths. These files are not committed.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    selected_ids = _normalize_ids(args.ids)
    unknown_ids = _validate_ids(selected_ids)
    if unknown_ids:
        print("Unknown example id(s): " + ", ".join(unknown_ids), file=sys.stderr)
        print("Known ids: " + ", ".join(sorted(_known_ids())), file=sys.stderr)
        return 2
    if args.verify or args.verify_smoke:
        exit_code = 0
        if args.verify:
            exit_code = max(exit_code, _verify_project_files(args.status, selected_ids))
        if args.verify_smoke:
            exit_code = max(exit_code, _verify_smoke_files(args.status, selected_ids))
        return exit_code
    if args.gallery_assets:
        if args.json:
            print(
                json.dumps(
                    gallery_for_json(args.status, absolute=args.absolute, ids=args.ids),
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            _print_gallery(args.status, absolute=args.absolute, ids=selected_ids)
        return 0
    if args.systems:
        if args.json:
            print(json.dumps(systems_for_json(), ensure_ascii=False, indent=2))
        else:
            _print_systems()
        return 0
    if args.coverage or args.needs_render or args.commands:
        if args.json:
            print(
                json.dumps(
                    feature_coverage_for_json(
                        args.coverage_status,
                        absolute=args.absolute,
                        needs_render=args.needs_render,
                        commands=args.commands,
                    ),
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            _print_coverage(
                args.coverage_status,
                absolute=args.absolute,
                needs_render=args.needs_render,
                commands=args.commands,
            )
        return 0
    if args.json:
        print(
            json.dumps(
                examples_for_json(args.status, absolute=args.absolute, ids=args.ids),
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        _print_text(args.status, absolute=args.absolute, ids=selected_ids)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
