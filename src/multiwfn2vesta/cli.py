"""Unified command-line entry point for maintained multiwfn2vesta workflows."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
import sys

from . import (
    abacus_molden,
    abacus_mulliken,
    aim_igmh_vesta,
    aim_vesta,
    cube_arith,
    cube_preset,
    cube_vesta,
    molden_check,
    multiwfn_atom_table,
    multiwfn_aim,
    multiwfn_grid,
    multiwfn_igmh,
    multiwfn_iri,
    surface_extrema_vesta,
)
from .executables import discovery_report


COMMANDS: Dict[str, Tuple[str, str]] = {
    "discover": ("Find Multiwfn and VESTA executables", "executables"),
    "abacus-molden": ("Generate and validate ABACUS Molden files", "abacus_molden"),
    "molden-check": ("Check Molden sections before Multiwfn workflows", "molden_check"),
    "cube-vesta": ("Create a VESTA file from cube data", "cube_vesta"),
    "cube-preset": ("Create a VESTA file from cube data using an analysis preset", "cube_preset"),
    "surface-extrema": ("Overlay Multiwfn surfanalysis.pdb extrema on VESTA", "surface_extrema_vesta"),
    "cube-arith": ("Combine compatible cube files, then optionally prepare VESTA", "cube_arith"),
    "iri-run": ("Run Multiwfn IRI/RDG cube generation, then prepare VESTA", "multiwfn_iri"),
    "igmh-run": ("Run Multiwfn IGMH cube generation, then prepare VESTA", "multiwfn_igmh"),
    "igm-run": ("Run Multiwfn IGM cube generation, then prepare VESTA", "multiwfn_igmh"),
    "migm-run": ("Run Multiwfn mIGM cube generation, then prepare VESTA", "multiwfn_igmh"),
    "grid-run": ("Run Multiwfn real-space function cube generation, then prepare VESTA", "multiwfn_grid"),
    "abacus-mulliken-color": ("Color VESTA atoms from ABACUS mulliken.txt", "abacus_mulliken"),
    "multiwfn-atom-color": ("Color VESTA atoms from a Multiwfn atom scalar table", "multiwfn_atom_table"),
    "aim-run": ("Run Multiwfn AIM on a wavefunction file, then convert PDB to VESTA", "multiwfn_aim"),
    "aim-pdb": ("Convert Multiwfn paths.pdb/CPs.pdb to atoms-only VESTA", "aim_vesta"),
    "aim-igmh": ("Style/render a saved AIM+IGMH VESTA overlay", "aim_igmh_vesta"),
}


ALIASES = {
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
    "multiwfn-grid": "grid-run",
    "scalar-cube-run": "grid-run",
    "function-cube": "grid-run",
    "mulliken-color": "abacus-mulliken-color",
    "atom-color": "abacus-mulliken-color",
    "multiwfn-table-color": "multiwfn-atom-color",
    "atom-table-color": "multiwfn-atom-color",
    "multiwfn-aim": "aim-run",
    "aim-vesta": "aim-pdb",
    "igmh": "aim-igmh",
}


def print_help() -> None:
    print(
        """multiwfn2vesta - maintained workflow launcher

Usage:
  multiwfn2vesta
      Start the interactive workflow chooser.

  multiwfn2vesta <command> [options]
      Run a scriptable workflow.

Commands:
  discover   Find Multiwfn and VESTA executables from env/PATH/workspace.
  abacus-molden
             Generate ABACUS LCAO Molden with latest ABACUS Multiwfn interface.
  molden-check
             Check Molden sections before Multiwfn workflows.
  cube-vesta
             Create a VESTA isosurface file from one cube and optional texture cube.
  cube-preset
             Apply an analysis preset before creating a VESTA cube file.
  surface-extrema
             Overlay Multiwfn surfanalysis.pdb extrema on an existing VESTA file.
  cube-arith
             Combine compatible cube files for density differences, Fukui, or dual descriptor.
  iri-run    Run Multiwfn IRI/RDG cube generation and prepare a VESTA mapped surface.
  igmh-run   Run Multiwfn IGMH cube generation and prepare a VESTA mapped surface.
  igm-run    Run Multiwfn IGM cube generation and prepare a VESTA mapped surface.
  migm-run   Run Multiwfn mIGM cube generation and prepare a VESTA mapped surface.
  grid-run   Run Multiwfn real-space function cube generation and prepare VESTA.
  abacus-mulliken-color
             Color VESTA atoms from ABACUS mulliken.txt charge/magnetism.
  multiwfn-atom-color
             Color VESTA atoms from a Multiwfn-style atom scalar table.
  aim-run    Run Multiwfn AIM on a wavefunction file, then convert to VESTA.
  aim-pdb    Convert Multiwfn paths.pdb/CPs.pdb to atoms-only VESTA.
  aim-igmh   Style a saved AIM+IGMH VESTA overlay, optionally render views.

Aliases:
  where, env  Aliases for discover.
  molden, abacus-multiwfn-molden
             Aliases for abacus-molden.
  cube       Alias for cube-vesta.
  preset, analysis-cube
             Aliases for cube-preset.
  surf-extrema, surfanalysis-vesta
             Aliases for surface-extrema.
  cube-math, density-diff, fukui-cube
             Aliases for cube-arith.
  multiwfn-iri, rdg-run
             Aliases for iri-run.
  multiwfn-igmh, multiwfn-igmh-run
             Aliases for igmh-run.
  multiwfn-igm, multiwfn-igm-run
             Aliases for igm-run.
  multiwfn-migm, multiwfn-migm-run
             Aliases for migm-run.
  multiwfn-grid, scalar-cube-run, function-cube
             Aliases for grid-run.
  multiwfn-table-color, atom-table-color
             Aliases for multiwfn-atom-color.
  atom-color  Backward-compatible alias for abacus-mulliken-color.
  aim-vesta  Alias for aim-pdb.
  igmh       Alias for aim-igmh.

Examples:
  multiwfn2vesta discover
  multiwfn2vesta abacus-molden abacus_calc ABACUS_Multiwfn.molden
  multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus
  multiwfn2vesta cube-vesta density.cub cube_products --isosurface 0.01
  multiwfn2vesta cube-preset orbital orbital.cub cube_products
  multiwfn2vesta surface-extrema input.vesta surfanalysis.pdb output.vesta --surface-cube density.cub
  multiwfn2vesta cube-arith products --operation dual-descriptor --anion-cube anion.cub --neutral-cube neutral.cub --cation-cube cation.cub
  multiwfn2vesta iri-run input.molden iri_products --timeout 300
  multiwfn2vesta igmh-run input.molden igmh_products --fragment 1-48 --fragment 49-60
  multiwfn2vesta igm-run input.molden igm_products --fragment 1-48 --fragment 49-60
  multiwfn2vesta grid-run input.molden grid_products --function density
  multiwfn2vesta abacus-mulliken-color input.vesta mulliken.txt colored.vesta
  multiwfn2vesta multiwfn-atom-color input.vesta atom_values.csv colored.vesta --value-column charge
  multiwfn2vesta aim-run input.molden aim_out
  multiwfn2vesta aim-pdb paths.pdb aim_atoms_only.vesta --cps-pdb CPs.pdb
  multiwfn2vesta aim-igmh overlay.vesta products --label-bcp-sites

Use `multiwfn2vesta <command> --help` for workflow-specific options.
"""
    )


def _prompt(label: str, default: Optional[str] = None, required: bool = False) -> str:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        value = input(f"{label}{suffix}: ").strip()
        if not value and default is not None:
            return default
        if value or not required:
            return value
        print("This value is required.")


def _yes_no(label: str, default: bool = False) -> bool:
    default_text = "Y/n" if default else "y/N"
    while True:
        value = input(f"{label} [{default_text}]: ").strip().lower()
        if not value:
            return default
        if value in {"y", "yes", "1", "true"}:
            return True
        if value in {"n", "no", "0", "false"}:
            return False
        print("Please answer y or n.")


def _default_output_dir(input_path: str, suffix: str) -> str:
    path = Path(input_path).expanduser()
    if path.name:
        return str(path.parent / suffix)
    return suffix


def interactive_aim_pdb() -> int:
    print("\nAIM PDB -> atoms-only VESTA")
    paths_pdb = _prompt("paths.pdb", required=True)
    output_vesta = _prompt("output .vesta", default=str(Path(paths_pdb).with_name("aim_atoms_only.vesta")))
    argv: List[str] = [paths_pdb, output_vesta]

    cps_pdb = _prompt("CPs.pdb (empty to skip)")
    if cps_pdb:
        argv.extend(["--cps-pdb", cps_pdb])

    title = _prompt("title", default="Multiwfn AIM paths")
    if title:
        argv.extend(["--title", title])

    cube = _prompt("cube file for cube-frame shift (empty to skip)")
    if cube:
        argv.extend(["--cube-frame-from-cube", cube])

    return aim_vesta.main(argv)


def interactive_aim_run() -> int:
    print("\nWavefunction -> Multiwfn AIM -> atoms-only VESTA")
    wavefunction = _prompt("wavefunction file (.molden/.fch/.wfn/etc.)", required=True)
    output_dir = _prompt("output directory", default=_default_output_dir(wavefunction, "multiwfn_aim"))
    argv: List[str] = [wavefunction, output_dir]

    multiwfn = _prompt("Multiwfn executable or directory (empty for auto-discovery)")
    if multiwfn:
        argv.extend(["--multiwfn", multiwfn])

    nthreads = _prompt("Multiwfn -nt threads (empty for default)")
    if nthreads:
        argv.extend(["--nthreads", nthreads])

    timeout = _prompt("timeout seconds (empty for no timeout)")
    if timeout:
        argv.extend(["--timeout", timeout])

    commands_file = _prompt("custom Multiwfn AIM command file (empty for default)")
    if commands_file:
        argv.extend(["--commands-file", commands_file])

    if _yes_no("skip atoms-only VESTA conversion", default=False):
        argv.append("--no-vesta")

    cube = _prompt("cube file for cube-frame shift during VESTA conversion (empty to skip)")
    if cube:
        argv.extend(["--cube-frame-from-cube", cube])

    return multiwfn_aim.main(argv)


def interactive_abacus_molden() -> int:
    print("\nABACUS calculation -> Multiwfn Molden")
    calc_dir = _prompt("ABACUS calculation directory", required=True)
    output_molden = _prompt("output Molden file", default=str(Path(calc_dir).resolve() / "ABACUS_Multiwfn.molden"))
    argv: List[str] = [calc_dir, output_molden]

    repo = _prompt("ABACUS git checkout (empty for workspace default)")
    if repo:
        argv.extend(["--abacus-repo", repo])

    git_ref = _prompt("ABACUS git ref", default="origin/develop")
    argv.extend(["--git-ref", git_ref])

    if _yes_no("git fetch origin develop before exporting molden.py", default=False):
        argv.append("--fetch")

    ngto = _prompt("number of fitted GTOs", default="7")
    argv.extend(["--ngto", ngto])

    rel_r = _prompt("relative cutoff radius", default="2")
    argv.extend(["--rel-r", rel_r])

    if not _yes_no("write [Nval]", default=True):
        argv.extend(["--with-Nval", "false"])

    if _yes_no("write [Pseudo]", default=False):
        argv.extend(["--with-pseudo", "true"])

    timeout = _prompt("timeout seconds (empty for no timeout)")
    if timeout:
        argv.extend(["--timeout", timeout])

    if _yes_no("skip molden-check --abacus", default=False):
        argv.append("--no-check")

    return abacus_molden.main(argv)


def interactive_aim_igmh() -> int:
    print("\nAIM+IGMH VESTA overlay styling")
    input_vesta = _prompt("input overlay .vesta", required=True)
    output_dir = _prompt("output directory", default=_default_output_dir(input_vesta, "aim_igmh_products"))
    argv: List[str] = [input_vesta, output_dir]

    stem = _prompt("output stem (empty to use input stem)")
    if stem:
        argv.extend(["--stem", stem])

    if _yes_no("rename BCP sites to BCP1/BCP2 labels", default=False):
        argv.append("--label-bcp-sites")

    if _yes_no("render front/right/top PNGs now (VESTA may steal focus)", default=False):
        argv.append("--render-three-views")
        initial = _prompt("initial saved view", default="top")
        argv.extend(["--initial-view", initial])
        scale = _prompt("image scale", default="2")
        argv.extend(["--scale", scale])
        if not _yes_no("keep default top x -8 temporary tilt", default=True):
            argv.append("--no-default-top-tilt")
        if _yes_no("clean existing workspace VESTA processes before render", default=False):
            argv.append("--clean-before")

    return aim_igmh_vesta.main(argv)


def interactive_cube_vesta() -> int:
    print("\nCube -> VESTA isosurface")
    surface_cube = _prompt("surface cube", required=True)
    output_dir = _prompt("output directory", default=_default_output_dir(surface_cube, "cube_vesta_products"))
    argv: List[str] = [surface_cube, output_dir]

    texture_cube = _prompt("texture/color cube (empty to skip)")
    if texture_cube:
        argv.extend(["--texture-cube", texture_cube])

    isosurface = _prompt("isosurface value", default=str(cube_vesta.DEFAULT_ISOSURFACE))
    argv.extend(["--isosurface", isosurface])

    tex_range = _prompt("physical texture range, e.g. -0.04 0.04 (empty for default percentages)")
    if tex_range:
        parts = tex_range.split()
        if len(parts) == 2:
            argv.extend(["--tex-physical", parts[0], parts[1]])
        else:
            print("Texture range needs exactly two numbers.")
            return 2

    structure = _prompt("structure phase (auto/none/molecule/crystal)", default="auto")
    argv.extend(["--structure", structure])

    if _yes_no("copy cube files beside VESTA", default=True) is False:
        argv.append("--no-copy-cubes")

    return cube_vesta.main(argv)


def interactive_cube_preset() -> int:
    print("\nCube analysis preset -> VESTA isosurface")
    print("Presets: " + ", ".join(cube_preset.preset_names()))
    preset = _prompt("preset", default="density")
    surface_cube = _prompt("surface cube", required=True)
    output_dir = _prompt("output directory", default=_default_output_dir(surface_cube, "cube_preset_products"))
    argv: List[str] = [preset, surface_cube, output_dir]

    texture_cube = _prompt("texture/color cube (empty to skip)")
    if texture_cube:
        argv.extend(["--texture-cube", texture_cube])

    isosurface = _prompt("override isosurface value (empty for preset default)")
    if isosurface:
        argv.extend(["--isosurface", isosurface])

    tex_range = _prompt("override physical texture range, e.g. -0.04 0.04 (empty for preset default)")
    if tex_range:
        parts = tex_range.split()
        if len(parts) == 2:
            argv.extend(["--tex-physical", parts[0], parts[1]])
        else:
            print("Texture range needs exactly two numbers.")
            return 2

    structure = _prompt("structure phase (empty for preset default)")
    if structure:
        argv.extend(["--structure", structure])

    if _yes_no("copy cube files beside VESTA", default=True) is False:
        argv.append("--no-copy-cubes")

    return cube_preset.main(argv)


def interactive_surface_extrema() -> int:
    print("\nMultiwfn surfanalysis.pdb extrema -> VESTA overlay")
    input_vesta = _prompt("input .vesta", required=True)
    surfanalysis_pdb = _prompt("surfanalysis.pdb", required=True)
    output_vesta = _prompt("output .vesta", default=str(Path(input_vesta).with_name("surface_extrema_overlay.vesta")))
    surface_cube = _prompt("surface/density cube used for coordinate alignment", required=True)
    argv: List[str] = [input_vesta, surfanalysis_pdb, output_vesta, "--surface-cube", surface_cube]

    selection = _prompt("selection (all/maxima/minima)", default="all")
    argv.extend(["--selection", selection])

    radius = _prompt("extrema radius (empty for default)")
    if radius:
        argv.extend(["--radius", radius])

    if _yes_no("show extrema labels", default=False):
        argv.append("--label-extrema")

    if _yes_no("keep existing COMPS setting", default=False):
        argv.append("--keep-comps")

    return surface_extrema_vesta.main(argv)


def interactive_cube_arith() -> int:
    print("\nCube arithmetic -> cube / VESTA")
    output_dir = _prompt("output directory", default="cube_arith_products")
    argv: List[str] = [output_dir]
    operation = _prompt(
        "operation (linear/density-difference/fukui-plus/fukui-minus/dual-descriptor)",
        default="linear",
    )
    argv.extend(["--operation", operation])
    if operation == "linear":
        while True:
            term = _prompt("term as COEFF CUBE (empty when done)", required=False)
            if not term:
                break
            parts = term.split(maxsplit=1)
            if len(parts) != 2:
                print("Each term needs a coefficient and a cube path.")
                return 2
            argv.extend(["--term", parts[0], parts[1]])
    elif operation in {"difference", "density-difference"}:
        plus_cube = _prompt("plus cube", required=True)
        minus_cube = _prompt("minus cube", required=True)
        argv.extend(["--plus-cube", plus_cube, "--minus-cube", minus_cube])
    else:
        neutral_cube = _prompt("neutral N cube", required=True)
        argv.extend(["--neutral-cube", neutral_cube])
        if operation in {"fukui-plus", "dual-descriptor"}:
            anion_cube = _prompt("anion N+1 cube", required=True)
            argv.extend(["--anion-cube", anion_cube])
        if operation in {"fukui-minus", "dual-descriptor"}:
            cation_cube = _prompt("cation N-1 cube", required=True)
            argv.extend(["--cation-cube", cation_cube])

    stem = _prompt("output stem (empty for operation default)")
    if stem:
        argv.extend(["--stem", stem])

    if _yes_no("skip VESTA generation", default=False):
        argv.append("--no-vesta")
    else:
        preset = _prompt("VESTA cube preset (auto/density/signed/...)", default="auto")
        argv.extend(["--preset", preset])
        isosurface = _prompt("override isosurface value (empty for preset default)")
        if isosurface:
            argv.extend(["--isosurface", isosurface])
        structure = _prompt("structure phase (auto/none/molecule/crystal)", default="auto")
        argv.extend(["--structure", structure])
        if _yes_no("copy output cube beside VESTA", default=True) is False:
            argv.append("--no-copy-cubes")

    return cube_arith.main(argv)


def interactive_iri_run() -> int:
    print("\nWavefunction -> Multiwfn IRI/RDG cubes -> VESTA")
    wavefunction = _prompt("wavefunction file (.molden/.fch/.wfn/etc.)", required=True)
    output_dir = _prompt("output directory", default=_default_output_dir(wavefunction, "multiwfn_iri"))
    argv: List[str] = [wavefunction, output_dir]

    multiwfn = _prompt("Multiwfn executable or directory (empty for auto-discovery)")
    if multiwfn:
        argv.extend(["--multiwfn", multiwfn])

    nthreads = _prompt("Multiwfn -nt threads (empty for default)")
    if nthreads:
        argv.extend(["--nthreads", nthreads])

    timeout = _prompt("timeout seconds (empty for no timeout)")
    if timeout:
        argv.extend(["--timeout", timeout])

    stem = _prompt("output stem (empty for wavefunction stem)")
    if stem:
        argv.extend(["--stem", stem])

    if _yes_no("skip VESTA generation", default=False):
        argv.append("--no-vesta")
    else:
        preset = _prompt("VESTA cube preset", default="iri")
        argv.extend(["--preset", preset])
        isosurface = _prompt("override isosurface value (empty for preset default)")
        if isosurface:
            argv.extend(["--isosurface", isosurface])
        tex_range = _prompt("override physical texture range, e.g. -0.04 0.04 (empty for preset default)")
        if tex_range:
            parts = tex_range.split()
            if len(parts) == 2:
                argv.extend(["--tex-physical", parts[0], parts[1]])
            else:
                print("Texture range needs exactly two numbers.")
                return 2

    return multiwfn_iri.main(argv)


def interactive_igmh_run() -> int:
    print("\nWavefunction -> Multiwfn IGM/IGMH cubes -> VESTA")
    wavefunction = _prompt("wavefunction file (.molden/.fch/.wfn/etc.)", required=True)
    output_dir = _prompt("output directory", default=_default_output_dir(wavefunction, "multiwfn_igmh"))
    argv: List[str] = [wavefunction, output_dir]

    method = _prompt("method (igmh/igm/migm)", default="igmh").lower()
    if method not in {"igmh", "igm", "migm"}:
        print("Method must be igmh, igm, or migm.")
        return 2
    argv.extend(["--method", method])
    if method in {"igm", "migm"}:
        sl2r_source = _prompt("sign(lambda2)rho source (actual/promolecular)", default="actual").lower()
        if sl2r_source not in {"actual", "promolecular"}:
            print("sign(lambda2)rho source must be actual or promolecular.")
            return 2
        argv.extend(["--sl2r-source", sl2r_source])

    while True:
        fragment = _prompt("fragment atom indices, e.g. 1-48 or c (empty when done)", required=False)
        if not fragment:
            break
        argv.extend(["--fragment", fragment])

    multiwfn = _prompt("Multiwfn executable or directory (empty for auto-discovery)")
    if multiwfn:
        argv.extend(["--multiwfn", multiwfn])

    nthreads = _prompt("Multiwfn -nt threads (empty for default)")
    if nthreads:
        argv.extend(["--nthreads", nthreads])

    timeout = _prompt("timeout seconds (empty for no timeout)")
    if timeout:
        argv.extend(["--timeout", timeout])

    stem = _prompt("output stem (empty for wavefunction stem)")
    if stem:
        argv.extend(["--stem", stem])

    grid_mode = _prompt("grid mode (low/medium/high/points/spacing/cube/pbc-cell)", default="points")
    argv.extend(["--grid-mode", grid_mode])
    if grid_mode == "points":
        grid_points = _prompt("grid points NX NY NZ", default="40 40 40")
        parts = grid_points.split()
        if len(parts) != 3:
            print("Grid points need exactly three integers.")
            return 2
        argv.extend(["--grid-points", parts[0], parts[1], parts[2]])
    elif grid_mode == "spacing":
        spacing = _prompt("grid spacing in Bohr", required=True)
        argv.extend(["--grid-spacing", spacing])
    elif grid_mode == "cube":
        reference_cube = _prompt("reference cube for grid", required=True)
        argv.extend(["--grid-cube", reference_cube])

    if _yes_no("skip VESTA generation", default=False):
        argv.append("--no-vesta")
    else:
        preset = _prompt("VESTA cube preset", default="igmh" if method == "igmh" else "igm")
        argv.extend(["--preset", preset])
        isosurface = _prompt("override isosurface value (empty for preset default)")
        if isosurface:
            argv.extend(["--isosurface", isosurface])
        tex_range = _prompt("override physical texture range, e.g. -0.05 0.05 (empty for preset default)")
        if tex_range:
            parts = tex_range.split()
            if len(parts) == 2:
                argv.extend(["--tex-physical", parts[0], parts[1]])
            else:
                print("Texture range needs exactly two numbers.")
                return 2

    return multiwfn_igmh.main(argv)


def interactive_grid_run() -> int:
    print("\nWavefunction -> Multiwfn real-space function cube -> VESTA")
    wavefunction = _prompt("wavefunction file (.molden/.fch/.wfn/etc.)", required=True)
    output_dir = _prompt("output directory", default=_default_output_dir(wavefunction, "multiwfn_grid"))
    argv: List[str] = [wavefunction, output_dir]

    orbital = _prompt("orbital index/label, or multiple space-separated labels for batch (empty to skip)")
    function_default = "orbital" if orbital else "density"
    function_name = _prompt(
        "function name/index (density/elf/lol/esp/orbital/...)",
        default=function_default,
    )
    if function_name:
        argv.extend(["--function", function_name])

    if orbital:
        orbitals = orbital.split()
        if len(orbitals) == 1:
            argv.extend(["--orbital", orbitals[0]])
        else:
            argv.append("--orbitals")
            argv.extend(orbitals)

    multiwfn = _prompt("Multiwfn executable or directory (empty for auto-discovery)")
    if multiwfn:
        argv.extend(["--multiwfn", multiwfn])

    nthreads = _prompt("Multiwfn -nt threads (empty for default)")
    if nthreads:
        argv.extend(["--nthreads", nthreads])

    timeout = _prompt("timeout seconds (empty for no timeout)")
    if timeout:
        argv.extend(["--timeout", timeout])

    stem = _prompt("output stem (empty for wavefunction stem)")
    if stem:
        argv.extend(["--stem", stem])

    grid_mode = _prompt("grid mode (low/medium/high/points/spacing/cube)", default="points")
    argv.extend(["--grid-mode", grid_mode])
    if grid_mode == "points":
        grid_points = _prompt("grid points NX NY NZ", default="40 40 40")
        parts = grid_points.split()
        if len(parts) != 3:
            print("Grid points need exactly three integers.")
            return 2
        argv.extend(["--grid-points", parts[0], parts[1], parts[2]])
    elif grid_mode == "spacing":
        spacing = _prompt("grid spacing in Bohr", required=True)
        argv.extend(["--grid-spacing", spacing])
    elif grid_mode == "cube":
        reference_cube = _prompt("reference cube for grid", required=True)
        argv.extend(["--grid-cube", reference_cube])

    if _yes_no("skip VESTA generation", default=False):
        argv.append("--no-vesta")
    else:
        preset = _prompt("VESTA cube preset (auto/density/signed/elf/lol)", default="auto")
        argv.extend(["--preset", preset])
        isosurface = _prompt("override isosurface value (empty for preset default)")
        if isosurface:
            argv.extend(["--isosurface", isosurface])
        structure = _prompt("structure phase (empty for preset default)")
        if structure:
            argv.extend(["--structure", structure])
        if _yes_no("copy cube files beside VESTA", default=True) is False:
            argv.append("--no-copy-cubes")

    return multiwfn_grid.main(argv)


def interactive_abacus_mulliken_color() -> int:
    print("\nABACUS Mulliken -> VESTA atom colors")
    input_vesta = _prompt("input .vesta", required=True)
    mulliken_txt = _prompt("ABACUS mulliken.txt", required=True)
    output_vesta = _prompt("output .vesta", default=str(Path(input_vesta).with_name("mulliken_colored.vesta")))
    argv: List[str] = [input_vesta, mulliken_txt, output_vesta]

    prop = _prompt("property (charge/magnetism/magnetism-x/y/z/magnetism-norm)", default="charge")
    argv.extend(["--property", prop])

    step = _prompt("ionic step number (empty for last)")
    if step:
        argv.extend(["--step", step])

    scale = _prompt("fixed color range vmin vmax (empty for auto symmetric)")
    if scale:
        parts = scale.split()
        if len(parts) != 2:
            print("Color range needs exactly two numbers.")
            return 2
        argv.extend(["--vmin", parts[0], "--vmax", parts[1]])

    center = _prompt("color center", default="0.0")
    argv.extend(["--center", center])

    section_index = _prompt("VESTA structure section index", default="0")
    argv.extend(["--section-index", section_index])

    values_csv = _prompt("write selected values CSV (empty to skip)")
    if values_csv:
        argv.extend(["--write-values", values_csv])

    if _yes_no("allow partial atom values", default=False):
        argv.append("--non-strict")

    return abacus_mulliken.main(argv)


def interactive_multiwfn_atom_color() -> int:
    print("\nMultiwfn atom table -> VESTA atom colors")
    input_vesta = _prompt("input .vesta", required=True)
    atom_table = _prompt("atom scalar table (CSV/TSV/text)", required=True)
    output_vesta = _prompt("output .vesta", default=str(Path(input_vesta).with_name("atom_table_colored.vesta")))
    argv: List[str] = [input_vesta, atom_table, output_vesta]

    value_column = _prompt("value column name (empty to infer)")
    if value_column:
        argv.extend(["--value-column", value_column])

    key_column = _prompt("key column name for atom index/label (empty to infer)")
    if key_column:
        argv.extend(["--key-column", key_column])

    scale = _prompt("fixed color range vmin vmax (empty for auto symmetric)")
    if scale:
        parts = scale.split()
        if len(parts) != 2:
            print("Color range needs exactly two numbers.")
            return 2
        argv.extend(["--vmin", parts[0], "--vmax", parts[1]])

    center = _prompt("color center", default="0.0")
    argv.extend(["--center", center])

    section_index = _prompt("VESTA structure section index", default="0")
    argv.extend(["--section-index", section_index])

    values_csv = _prompt("write normalized values CSV (empty to skip)")
    if values_csv:
        argv.extend(["--write-values", values_csv])

    if _yes_no("allow partial atom values", default=False):
        argv.append("--non-strict")

    return multiwfn_atom_table.main(argv)


def interactive_main() -> int:
    print("multiwfn2vesta interactive launcher\n")
    print("0) Discover Multiwfn/VESTA executables")
    print("1) Wavefunction -> Multiwfn AIM -> atoms-only VESTA")
    print("2) AIM PDB -> atoms-only VESTA")
    print("3) AIM+IGMH overlay -> styled VESTA / optional three views")
    print("4) Check Molden file for Multiwfn/ABACUS use")
    print("5) Cube -> VESTA isosurface")
    print("6) Cube analysis preset -> VESTA isosurface")
    print("7) Wavefunction -> Multiwfn IRI/RDG cubes -> VESTA")
    print("8) ABACUS Mulliken -> VESTA atom colors")
    print("9) ABACUS calculation -> Multiwfn Molden")
    print("10) Wavefunction -> Multiwfn real-space function cube -> VESTA")
    print("11) Cube arithmetic -> density difference/Fukui/dual descriptor VESTA")
    print("12) Multiwfn atom table -> VESTA atom colors")
    print("13) surfanalysis.pdb extrema -> VESTA overlay")
    print("14) Wavefunction -> Multiwfn IGM/IGMH cubes -> VESTA")
    print("q) Quit")
    choice = _prompt("choice", default="3").lower()
    if choice in {"0", "discover", "where", "env"}:
        print(discovery_report())
        return 0
    if choice in {"1", "aim-run", "multiwfn-aim"}:
        return interactive_aim_run()
    if choice in {"2", "aim-pdb", "aim-vesta"}:
        return interactive_aim_pdb()
    if choice in {"3", "aim-igmh", "igmh"}:
        return interactive_aim_igmh()
    if choice in {"4", "molden-check", "check-molden"}:
        molden = _prompt("Molden file", required=True)
        argv: List[str] = [molden]
        if _yes_no("ABACUS pseudopotential Molden", default=True):
            argv.append("--abacus")
        return molden_check.main(argv)
    if choice in {"5", "cube-vesta", "cube"}:
        return interactive_cube_vesta()
    if choice in {"6", "cube-preset", "preset", "analysis-cube"}:
        return interactive_cube_preset()
    if choice in {"11", "cube-arith", "cube-math", "density-diff", "fukui-cube"}:
        return interactive_cube_arith()
    if choice in {"7", "iri-run", "multiwfn-iri", "rdg-run"}:
        return interactive_iri_run()
    if choice in {"14", "igmh-run", "multiwfn-igmh", "multiwfn-igmh-run", "igm-run", "migm-run"}:
        return interactive_igmh_run()
    if choice in {"8", "abacus-mulliken-color", "mulliken-color", "atom-color"}:
        return interactive_abacus_mulliken_color()
    if choice in {"9", "abacus-molden", "molden", "abacus-multiwfn-molden"}:
        return interactive_abacus_molden()
    if choice in {"10", "grid-run", "multiwfn-grid", "scalar-cube-run", "function-cube"}:
        return interactive_grid_run()
    if choice in {"12", "multiwfn-atom-color", "multiwfn-table-color", "atom-table-color"}:
        return interactive_multiwfn_atom_color()
    if choice in {"13", "surface-extrema", "surf-extrema", "surfanalysis-vesta"}:
        return interactive_surface_extrema()
    if choice in {"q", "quit", "exit"}:
        return 0
    print(f"Unknown choice: {choice}")
    return 2


def run_command(command: str, args: Sequence[str]) -> int:
    if command == "discover":
        print(discovery_report(), end="")
        return 0
    if command == "abacus-molden":
        return abacus_molden.main(args)
    if command == "molden-check":
        return molden_check.main(args)
    if command == "cube-vesta":
        return cube_vesta.main(args)
    if command == "cube-preset":
        return cube_preset.main(args)
    if command == "surface-extrema":
        return surface_extrema_vesta.main(args)
    if command == "cube-arith":
        return cube_arith.main(args)
    if command == "iri-run":
        return multiwfn_iri.main(args)
    if command == "igmh-run":
        return multiwfn_igmh.main(args)
    if command == "igm-run":
        return multiwfn_igmh.main_igm(args)
    if command == "migm-run":
        return multiwfn_igmh.main_migm(args)
    if command == "grid-run":
        return multiwfn_grid.main(args)
    if command == "abacus-mulliken-color":
        return abacus_mulliken.main(args)
    if command == "multiwfn-atom-color":
        return multiwfn_atom_table.main(args)
    if command == "aim-run":
        return multiwfn_aim.main(args)
    if command == "aim-pdb":
        return aim_vesta.main(args)
    if command == "aim-igmh":
        return aim_igmh_vesta.main(args)
    raise ValueError(f"Unknown command: {command}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        return interactive_main()
    if args[0] in {"-h", "--help", "help"}:
        print_help()
        return 0

    command = ALIASES.get(args[0], args[0])
    if command not in COMMANDS:
        print(f"Unknown command: {args[0]}\n", file=sys.stderr)
        print_help()
        return 2
    return run_command(command, args[1:])


if __name__ == "__main__":
    raise SystemExit(main())
