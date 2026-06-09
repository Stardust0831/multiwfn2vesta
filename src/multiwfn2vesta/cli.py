"""Unified command-line entry point for maintained multiwfn2vesta workflows."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
import sys

from . import abacus_molden, abacus_mulliken, aim_igmh_vesta, aim_vesta, cube_preset, cube_vesta, molden_check, multiwfn_aim
from .executables import discovery_report


COMMANDS: Dict[str, Tuple[str, str]] = {
    "discover": ("Find Multiwfn and VESTA executables", "executables"),
    "abacus-molden": ("Generate and validate ABACUS Molden files", "abacus_molden"),
    "molden-check": ("Check Molden sections before Multiwfn workflows", "molden_check"),
    "cube-vesta": ("Create a VESTA file from cube data", "cube_vesta"),
    "cube-preset": ("Create a VESTA file from cube data using an analysis preset", "cube_preset"),
    "abacus-mulliken-color": ("Color VESTA atoms from ABACUS mulliken.txt", "abacus_mulliken"),
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
    "mulliken-color": "abacus-mulliken-color",
    "atom-color": "abacus-mulliken-color",
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
  abacus-mulliken-color
             Color VESTA atoms from ABACUS mulliken.txt charge/magnetism.
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
  aim-vesta  Alias for aim-pdb.
  igmh       Alias for aim-igmh.

Examples:
  multiwfn2vesta discover
  multiwfn2vesta abacus-molden abacus_calc ABACUS_Multiwfn.molden
  multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus
  multiwfn2vesta cube-vesta density.cub cube_products --isosurface 0.01
  multiwfn2vesta cube-preset orbital orbital.cub cube_products
  multiwfn2vesta abacus-mulliken-color input.vesta mulliken.txt colored.vesta
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


def interactive_main() -> int:
    print("multiwfn2vesta interactive launcher\n")
    print("0) Discover Multiwfn/VESTA executables")
    print("1) Wavefunction -> Multiwfn AIM -> atoms-only VESTA")
    print("2) AIM PDB -> atoms-only VESTA")
    print("3) AIM+IGMH overlay -> styled VESTA / optional three views")
    print("4) Check Molden file for Multiwfn/ABACUS use")
    print("5) Cube -> VESTA isosurface")
    print("6) Cube analysis preset -> VESTA isosurface")
    print("7) ABACUS Mulliken -> VESTA atom colors")
    print("8) ABACUS calculation -> Multiwfn Molden")
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
    if choice in {"7", "abacus-mulliken-color", "mulliken-color", "atom-color"}:
        return interactive_abacus_mulliken_color()
    if choice in {"8", "abacus-molden", "molden", "abacus-multiwfn-molden"}:
        return interactive_abacus_molden()
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
    if command == "abacus-mulliken-color":
        return abacus_mulliken.main(args)
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
