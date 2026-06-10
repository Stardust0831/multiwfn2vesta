"""Analysis-oriented presets for cube-to-VESTA workflows."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from . import cube_vesta, surface_extrema_vesta


RGB = Tuple[int, int, int]


@dataclass(frozen=True)
class CubePreset:
    name: str
    aliases: Tuple[str, ...]
    description: str
    surface_mode: str
    isosurface: float
    positive_rgb: RGB = (255, 255, 0)
    negative_rgb: RGB = (0, 80, 255)
    surface_opacity: Tuple[int, int] = (127, 255)
    tex_physical: Optional[Tuple[float, float]] = None
    tex_range_source: str = "full-cube"
    texture_required: bool = False
    structure: str = "auto"
    sections: str = "off"
    notes: str = ""


PRESETS: Tuple[CubePreset, ...] = (
    CubePreset(
        name="density",
        aliases=("rho", "charge-density", "scalar"),
        description="Single positive isosurface for density-like scalar cubes.",
        surface_mode="single",
        isosurface=0.01,
        positive_rgb=(255, 220, 80),
        notes="Use for ABACUS out_chg cubes or Multiwfn electron-density cubes.",
    ),
    CubePreset(
        name="signed",
        aliases=("orbital", "mo", "wavefunction", "abacus-wfc", "density-difference", "dual-descriptor"),
        description="Positive/negative isosurfaces for signed real scalar cubes.",
        surface_mode="signed",
        isosurface=0.02,
        notes="Use for molecular orbitals, real wavefunction cubes, density differences, or dual-descriptor cubes.",
    ),
    CubePreset(
        name="elf",
        aliases=("abacus-elf",),
        description="ELF localization isosurface.",
        surface_mode="single",
        isosurface=0.80,
        positive_rgb=(255, 190, 60),
        notes="Use for ABACUS out_elf cubes or Multiwfn ELF cubes; tune the isosurface for each system.",
    ),
    CubePreset(
        name="lol",
        aliases=(),
        description="LOL localization isosurface.",
        surface_mode="single",
        isosurface=0.50,
        positive_rgb=(120, 210, 120),
        notes="Use for Multiwfn LOL cubes; tune the isosurface for each system.",
    ),
    CubePreset(
        name="stm",
        aliases=("ldos", "stm-ldos", "tunneling-current"),
        description="Constant-current STM/LDOS tunneling-current isosurface.",
        surface_mode="single",
        isosurface=0.001,
        positive_rgb=(80, 210, 255),
        notes="Use for Multiwfn STM.cub exported by the constant-current STM workflow; tune the isosurface for each bias/system.",
    ),
    CubePreset(
        name="domain",
        aliases=("domain-cube", "domain-analysis", "binary-domain"),
        description="Binary Multiwfn domain.cub isosurface.",
        surface_mode="single",
        isosurface=0.5,
        positive_rgb=(255, 170, 0),
        surface_opacity=(160, 255),
        notes="Use for Multiwfn domain.cub from main function 200/14; values are 1 inside the selected domain and 0 outside.",
    ),
    CubePreset(
        name="iri",
        aliases=("rdg", "nci", "weak-interaction"),
        description="IRI/RDG/NCI surface colored by sign(lambda2)rho-like texture cube.",
        surface_mode="single",
        isosurface=1.0,
        tex_physical=(-0.04, 0.04),
        tex_range_source="surface-band",
        texture_required=True,
        notes="Use the IRI/RDG scalar as surface cube and sign(lambda2)rho-like cube as texture cube.",
    ),
    CubePreset(
        name="igmh",
        aliases=("igm", "igm-inter", "igmh-inter", "interfragment-igm", "interfragment-igmh"),
        description="IGM/IGMH interfragment delta-g surface colored by sign(lambda2)rho.",
        surface_mode="single",
        isosurface=0.01000,
        tex_physical=(-0.05, 0.05),
        texture_required=True,
        notes=(
            "Use Multiwfn dg_inter.cub as surface cube and sl2r.cub as texture cube; "
            "defaults follow the bundled IGM_inter.vmd template."
        ),
    ),
    CubePreset(
        name="igm-intra",
        aliases=("igmh-intra", "intrafragment-igm", "intrafragment-igmh"),
        description="IGM/IGMH intrafragment delta-g surface colored by sign(lambda2)rho.",
        surface_mode="single",
        isosurface=0.2000,
        tex_physical=(-0.05, 0.05),
        texture_required=True,
        notes=(
            "Use Multiwfn dg_intra.cub as surface cube and sl2r.cub as texture cube; "
            "defaults follow the bundled IGM_intra.vmd template."
        ),
    ),
    CubePreset(
        name="aigm",
        aliases=("average-igm", "averaged-igm", "avg-igm"),
        description="Averaged IGM delta-g surface colored by averaged sign(lambda2)rho.",
        surface_mode="single",
        isosurface=0.008,
        tex_physical=(-0.05, 0.05),
        texture_required=True,
        notes=(
            "Use Multiwfn avgdg_inter.cub as surface cube and avgsl2r.cub as texture cube; "
            "defaults follow the bundled aIGM.vmd template."
        ),
    ),
    CubePreset(
        name="aigm-tfi",
        aliases=("aigm-thermal-fluctuation-index", "tfi-igm", "aigm-tfi-map"),
        description="Averaged IGM delta-g surface colored by thermal fluctuation index.",
        surface_mode="single",
        isosurface=0.008,
        tex_physical=(0.0, 1.5),
        texture_required=True,
        notes=(
            "Use Multiwfn avgdg_inter.cub as surface cube and thermflu.cub as texture cube; "
            "defaults follow the bundled aIGM_TFI.vmd template."
        ),
    ),
    CubePreset(
        name="esp",
        aliases=("mep", "electrostatic-potential", "density-esp"),
        description="Density surface colored by electrostatic potential texture cube.",
        surface_mode="single",
        isosurface=0.001,
        texture_required=True,
        notes="Use density as surface cube and ESP/MEP/potential as texture cube; set --tex-physical for comparable figures.",
    ),
    CubePreset(
        name="surface-map",
        aliases=("molsurfmap", "mapped-surface", "density-surface-map"),
        description="Generic density surface colored by a compatible mapped-property cube.",
        surface_mode="single",
        isosurface=0.01,
        tex_physical=(0.0, 0.002),
        texture_required=True,
        notes=(
            "Use density/surface cube as the surface and a mapped-property cube as texture; "
            "defaults follow the bundled molsurfmap.vmd template."
        ),
    ),
    CubePreset(
        name="alie",
        aliases=("average-local-ionization-energy", "avglocion"),
        description="Density surface colored by Multiwfn average local ionization energy (ALIE).",
        surface_mode="single",
        isosurface=0.0005,
        tex_physical=(0.32, 0.36),
        texture_required=True,
        notes=(
            "Use Multiwfn density.cub as surface cube and avglocion.cub as texture cube; "
            "default color range follows the bundled ALIE.vmd example in a.u."
        ),
    ),
    CubePreset(
        name="lea",
        aliases=("local-electron-affinity",),
        description="Density surface colored by Multiwfn local electron affinity (LEA).",
        surface_mode="single",
        isosurface=0.01,
        tex_physical=(-0.8, -0.3),
        texture_required=True,
        notes=(
            "Use Multiwfn density.cub as surface cube and userfunc.cub as texture cube; "
            "default color range follows the bundled LEA VMD example in a.u."
        ),
    ),
    CubePreset(
        name="leae",
        aliases=("local-electron-attachment-energy",),
        description="Density surface colored by Multiwfn local electron attachment energy (LEAE).",
        surface_mode="single",
        isosurface=0.004,
        tex_physical=(-0.03, 0.0),
        texture_required=True,
        notes=(
            "Use Multiwfn density.cub as surface cube and userfunc.cub as texture cube; "
            "default color range follows the bundled LEAE VMD example in a.u."
        ),
    ),
    CubePreset(
        name="vdw-map",
        aliases=("vdw-surface", "vdw-density-surface", "vdw-potential-map"),
        description="Density surface colored by Multiwfn van der Waals potential.",
        surface_mode="single",
        isosurface=0.0001,
        tex_physical=(-0.3, 0.3),
        texture_required=True,
        notes=(
            "Use Multiwfn density.cub as surface cube and vdW.cub/vdWpot.cub as texture cube; "
            "default color range follows the bundled vdWpot.vmd example in kcal/mol."
        ),
    ),
)


PRESET_BY_NAME: Dict[str, CubePreset] = {}
for _preset in PRESETS:
    PRESET_BY_NAME[_preset.name] = _preset
    for _alias in _preset.aliases:
        PRESET_BY_NAME[_alias] = _preset


def preset_names() -> List[str]:
    return [preset.name for preset in PRESETS]


def resolve_preset(name: str) -> CubePreset:
    key = name.strip().lower()
    try:
        return PRESET_BY_NAME[key]
    except KeyError:
        known = ", ".join(sorted(PRESET_BY_NAME))
        raise ValueError(f"Unknown cube preset: {name}. Known presets/aliases: {known}")


def format_preset_list() -> str:
    lines = ["Available cube presets:", ""]
    for preset in PRESETS:
        alias_text = f" (aliases: {', '.join(preset.aliases)})" if preset.aliases else ""
        lines.append(f"- {preset.name}{alias_text}: {preset.description}")
        lines.append(f"  isosurface={preset.isosurface}, surface_mode={preset.surface_mode}")
        if preset.texture_required:
            lines.append("  requires --texture-cube")
        if preset.tex_physical is not None:
            lines.append(f"  tex_physical={preset.tex_physical[0]} {preset.tex_physical[1]}")
        if preset.notes:
            lines.append(f"  note: {preset.notes}")
    return "\n".join(lines) + "\n"


def default_surface_extrema_selection(preset: CubePreset) -> str:
    if preset.name in {"alie", "leae"}:
        return "minima"
    if preset.name == "lea":
        return "maxima"
    return "all"


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


def _rgb(values: Optional[Sequence[int]], default: RGB, label: str) -> RGB:
    if values is None:
        return default
    if len(values) != 3:
        raise ValueError(f"{label} RGB requires exactly three values")
    rgb = tuple(int(value) for value in values)
    if any(value < 0 or value > 255 for value in rgb):
        raise ValueError(f"{label} RGB values must be between 0 and 255")
    return rgb  # type: ignore[return-value]


def _opacity(values: Optional[Sequence[int]], default: Tuple[int, int]) -> Tuple[int, int]:
    if values is None:
        return default
    if len(values) != 2:
        raise ValueError("Surface opacity requires exactly two values")
    opacity = tuple(int(value) for value in values)
    if any(value < 0 or value > 255 for value in opacity):
        raise ValueError("Surface opacity values must be between 0 and 255")
    return opacity  # type: ignore[return-value]


def _append_preset_manifest(
    manifest: Path,
    *,
    requested_preset: str,
    preset: CubePreset,
    surface_cube: Path,
    texture_cube: Optional[Path],
    surface_mode: str,
    isosurface: float,
    tex_percent: Optional[Tuple[float, float]],
    tex_physical: Optional[Tuple[float, float]],
    tex_range_source: str,
) -> None:
    text = manifest.read_text(encoding="utf-8")
    lines = [
        "",
        "## Cube Preset",
        "",
        f"- requested_preset: `{requested_preset}`",
        f"- canonical_preset: `{preset.name}`",
        f"- description: `{preset.description}`",
        f"- surface_cube: `{surface_cube}`",
        f"- texture_cube: `{texture_cube}`" if texture_cube is not None else "- texture_cube: `None`",
        f"- preset_surface_mode: `{preset.surface_mode}`",
        f"- effective_surface_mode: `{surface_mode}`",
        f"- preset_isosurface: `{preset.isosurface}`",
        f"- effective_isosurface: `{isosurface}`",
        f"- texture_required: `{str(preset.texture_required).lower()}`",
        f"- preset_tex_range_source: `{preset.tex_range_source}`",
        f"- effective_tex_range_source: `{tex_range_source}`",
    ]
    if tex_percent is not None:
        lines.append(f"- effective_tex_percent: `{tex_percent[0]}` to `{tex_percent[1]}`")
        lines.append("- tex_range_note: `explicit --tex-percent was used; physical texture scaling was not applied`")
    if preset.tex_physical is not None:
        lines.append(f"- preset_tex_physical: `{preset.tex_physical[0]}` to `{preset.tex_physical[1]}`")
    if tex_physical is not None:
        lines.append(f"- effective_tex_physical: `{tex_physical[0]}` to `{tex_physical[1]}`")
    if preset.notes:
        lines.append(f"- notes: `{preset.notes}`")
    manifest.write_text(text.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


def run_preset(
    preset_name: str,
    surface_cube: Path,
    output_dir: Path,
    *,
    texture_cube: Optional[Path] = None,
    stem: Optional[str] = None,
    output_vesta: Optional[Path] = None,
    manifest: Optional[Path] = None,
    write_manifest: bool = True,
    title: Optional[str] = None,
    isosurface: Optional[float] = None,
    surface_mode: Optional[str] = None,
    positive_rgb: Optional[Sequence[int]] = None,
    negative_rgb: Optional[Sequence[int]] = None,
    surface_opacity: Optional[Sequence[int]] = None,
    tex_percent: Optional[Sequence[float]] = None,
    tex_physical: Optional[Sequence[float]] = None,
    tex_range_source: Optional[str] = None,
    surface_band: Optional[float] = None,
    surface_nearest: int = 1024,
    cube_units: str = "auto",
    structure: Optional[str] = None,
    boundary: Optional[Sequence[float]] = None,
    sections: Optional[str] = None,
    copy_cubes: bool = True,
    strict: bool = True,
    strict_compatible: bool = True,
    show_structure_bonds: bool = True,
    surfanalysis_pdb: Optional[Path] = None,
    surf_extrema: str = "auto",
    extrema_radius: float = surface_extrema_vesta.DEFAULT_EXTREMA_RADIUS,
    maxima_rgb: Optional[Sequence[int]] = None,
    minima_rgb: Optional[Sequence[int]] = None,
    label_extrema: bool = False,
    keep_comps: bool = False,
) -> cube_vesta.CubeVestaResult:
    surface_cube = Path(surface_cube)
    output_dir = Path(output_dir)
    texture_cube = Path(texture_cube) if texture_cube is not None else None
    surfanalysis_pdb = Path(surfanalysis_pdb) if surfanalysis_pdb is not None else None
    preset = resolve_preset(preset_name)
    if preset.texture_required and texture_cube is None:
        raise ValueError(f"Cube preset `{preset.name}` requires --texture-cube")

    effective_isosurface = preset.isosurface if isosurface is None else float(isosurface)
    effective_surface_mode = surface_mode or preset.surface_mode
    effective_tex_percent = _float_pair(tex_percent)
    effective_tex_physical = None if effective_tex_percent is not None else preset.tex_physical
    if tex_physical is not None:
        effective_tex_physical = _float_pair(tex_physical)
    backend_tex_range_source = tex_range_source or preset.tex_range_source
    manifest_tex_range_source = "explicit-percent" if effective_tex_percent is not None else backend_tex_range_source
    effective_title = title or f"{surface_cube.stem} ({preset.name})"
    effective_stem = stem or f"{surface_cube.stem}_{preset.name}"

    result = cube_vesta.run_workflow(
        surface_cube,
        output_dir,
        texture_cube=texture_cube,
        stem=effective_stem,
        output_vesta=output_vesta,
        manifest=manifest,
        write_manifest=write_manifest,
        title=effective_title,
        isosurface=effective_isosurface,
        surface_mode=effective_surface_mode,
        positive_rgb=_rgb(positive_rgb, preset.positive_rgb, "positive surface"),
        negative_rgb=_rgb(negative_rgb, preset.negative_rgb, "negative surface"),
        surface_opacity=_opacity(surface_opacity, preset.surface_opacity),
        tex_percent=effective_tex_percent,
        tex_physical=effective_tex_physical,
        tex_range_source=backend_tex_range_source,
        surface_band=surface_band,
        surface_nearest=surface_nearest,
        cube_units=cube_units,
        structure=structure or preset.structure,
        boundary=_float_six(boundary),
        sections=sections or preset.sections,
        copy_cubes=copy_cubes,
        strict=strict,
        strict_compatible=strict_compatible,
        show_structure_bonds=show_structure_bonds,
    )
    if result.manifest_path is not None:
        _append_preset_manifest(
            result.manifest_path,
            requested_preset=preset_name,
            preset=preset,
            surface_cube=surface_cube,
            texture_cube=texture_cube,
            surface_mode=effective_surface_mode,
            isosurface=effective_isosurface,
            tex_percent=effective_tex_percent,
            tex_physical=effective_tex_physical,
            tex_range_source=manifest_tex_range_source,
        )
    if surfanalysis_pdb is not None:
        selection = default_surface_extrema_selection(preset) if surf_extrema == "auto" else surf_extrema
        max_rgb = _rgb(maxima_rgb, surface_extrema_vesta.DEFAULT_MAXIMA_RGB, "surface maxima")
        min_rgb = _rgb(minima_rgb, surface_extrema_vesta.DEFAULT_MINIMA_RGB, "surface minima")
        overlay_structure = structure or preset.structure
        if overlay_structure == "none":
            overlay_structure = "auto"
        overlay = surface_extrema_vesta.overlay_surface_extrema_file(
            result.vesta_path,
            surfanalysis_pdb,
            result.vesta_path,
            surface_cube=surface_cube,
            selection=selection,
            title=f"{effective_title} surface extrema",
            structure=overlay_structure,
            boundary=_float_six(boundary),
            radius=extrema_radius,
            maxima_rgb=max_rgb,
            minima_rgb=min_rgb,
            label_extrema=label_extrema,
            set_comps_off=not keep_comps,
            cube_units=cube_units,
            strict=strict,
        )
        if result.manifest_path is not None:
            surface_extrema_vesta.append_overlay_manifest(
                result.manifest_path,
                surfanalysis_pdb=surfanalysis_pdb,
                result=overlay,
                radius=extrema_radius,
                maxima_rgb=max_rgb,
                minima_rgb=min_rgb,
                label_extrema=label_extrema,
                set_comps_off=not keep_comps,
            )
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create a VESTA file from a cube using an analysis-oriented preset."
    )
    parser.add_argument("preset", nargs="?", help="Preset name or alias; use --list-presets to inspect options")
    parser.add_argument("surface_cube", nargs="?", type=Path)
    parser.add_argument("output_dir", nargs="?", type=Path)
    parser.add_argument("--list-presets", action="store_true")
    parser.add_argument("--texture-cube", type=Path)
    parser.add_argument("--stem")
    parser.add_argument("--output-vesta", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--no-manifest", action="store_true")
    parser.add_argument("--title")
    parser.add_argument("--isosurface", type=float)
    parser.add_argument("--surface-mode", choices=["single", "signed"])
    parser.add_argument("--positive-rgb", nargs=3, type=int, metavar=("R", "G", "B"))
    parser.add_argument("--negative-rgb", nargs=3, type=int, metavar=("R", "G", "B"))
    parser.add_argument("--surface-opacity", nargs=2, type=int, metavar=("O1", "O2"))
    parser.add_argument("--tex-percent", nargs=2, type=float, metavar=("MIN", "MAX"))
    parser.add_argument("--tex-physical", nargs=2, type=float, metavar=("MIN", "MAX"))
    parser.add_argument("--tex-range-source", choices=["full-cube", "surface-band"])
    parser.add_argument("--surface-band", type=float)
    parser.add_argument("--surface-nearest", type=int, default=1024)
    parser.add_argument("--cube-units", choices=["auto", "bohr", "angstrom"], default="auto")
    parser.add_argument("--structure", choices=["auto", "none", "molecule", "crystal"])
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--sections", choices=["off", "keep"])
    parser.add_argument("--no-copy-cubes", action="store_true")
    parser.add_argument("--non-strict", action="store_true", help="Allow cube data count mismatch")
    parser.add_argument("--no-strict-compatible", action="store_true", help="Do not require texture grid to match surface grid")
    parser.add_argument("--structure-bonds-off", action="store_true")
    parser.add_argument("--surfanalysis-pdb", type=Path, help="Overlay Multiwfn surface extrema from surfanalysis.pdb")
    parser.add_argument("--surf-extrema", choices=["auto", "all", "maxima", "minima"], default="auto")
    parser.add_argument("--extrema-radius", type=float, default=surface_extrema_vesta.DEFAULT_EXTREMA_RADIUS)
    parser.add_argument("--maxima-rgb", nargs=3, type=int, metavar=("R", "G", "B"))
    parser.add_argument("--minima-rgb", nargs=3, type=int, metavar=("R", "G", "B"))
    parser.add_argument("--label-extrema", action="store_true")
    parser.add_argument("--keep-comps", action="store_true", help="Do not force COMPS 0 after adding extrema phase")
    args = parser.parse_args(argv)

    if args.list_presets:
        print(format_preset_list(), end="")
        return 0
    if args.preset is None or args.surface_cube is None or args.output_dir is None:
        parser.error("preset, surface_cube, and output_dir are required unless --list-presets is used")

    try:
        result = run_preset(
            args.preset,
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
            positive_rgb=args.positive_rgb,
            negative_rgb=args.negative_rgb,
            surface_opacity=args.surface_opacity,
            tex_percent=args.tex_percent,
            tex_physical=args.tex_physical,
            tex_range_source=args.tex_range_source,
            surface_band=args.surface_band,
            surface_nearest=args.surface_nearest,
            cube_units=args.cube_units,
            structure=args.structure,
            boundary=args.boundary,
            sections=args.sections,
            copy_cubes=not args.no_copy_cubes,
            strict=not args.non_strict,
            strict_compatible=not args.no_strict_compatible,
            show_structure_bonds=not args.structure_bonds_off,
            surfanalysis_pdb=args.surfanalysis_pdb,
            surf_extrema=args.surf_extrema,
            extrema_radius=args.extrema_radius,
            maxima_rgb=args.maxima_rgb,
            minima_rgb=args.minima_rgb,
            label_extrema=args.label_extrema,
            keep_comps=args.keep_comps,
        )
    except ValueError as exc:
        print(f"cube-preset: {exc}")
        return 2

    print(result.vesta_path)
    if result.manifest_path is not None:
        print(result.manifest_path)
    if result.copied_cubes:
        for _, destination in result.copied_cubes:
            print(f"copied {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
