"""Unified command-line entry point for maintained multiwfn2vesta workflows."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
import sys

from . import aim_igmh_vesta, aim_vesta


COMMANDS: Dict[str, Tuple[str, str]] = {
    "aim-pdb": ("Convert Multiwfn paths.pdb/CPs.pdb to atoms-only VESTA", "aim_vesta"),
    "aim-igmh": ("Style/render a saved AIM+IGMH VESTA overlay", "aim_igmh_vesta"),
}


ALIASES = {
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
  aim-pdb    Convert Multiwfn paths.pdb/CPs.pdb to atoms-only VESTA.
  aim-igmh   Style a saved AIM+IGMH VESTA overlay, optionally render views.

Aliases:
  aim-vesta  Alias for aim-pdb.
  igmh       Alias for aim-igmh.

Examples:
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


def interactive_main() -> int:
    print("multiwfn2vesta interactive launcher\n")
    print("1) AIM PDB -> atoms-only VESTA")
    print("2) AIM+IGMH overlay -> styled VESTA / optional three views")
    print("q) Quit")
    choice = _prompt("choice", default="2").lower()
    if choice in {"1", "aim-pdb", "aim-vesta"}:
        return interactive_aim_pdb()
    if choice in {"2", "aim-igmh", "igmh"}:
        return interactive_aim_igmh()
    if choice in {"q", "quit", "exit"}:
        return 0
    print(f"Unknown choice: {choice}")
    return 2


def run_command(command: str, args: Sequence[str]) -> int:
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
