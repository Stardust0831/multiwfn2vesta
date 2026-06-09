"""Run Multiwfn AIM topology analysis and convert its PDB output."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, NamedTuple, Optional, Sequence

from .aim_vesta import convert_aim_pdb_to_vesta
from .executables import ExecutableCandidate, find_multiwfn


AIM_OUTPUT_MISSING_CODE = 3

DEFAULT_AIM_COMMANDS = [
    "2",
    "2",
    "3",
    "4",
    "5",
    "8",
    "-4",
    "6",
    "0",
    "-5",
    "6",
    "0",
    "7",
    "-1",
    "-10",
    "100",
    "2",
    "1",
    "mol.pdb",
    "0",
    "q",
]


class MultiwfnAimResult(NamedTuple):
    multiwfn: ExecutableCandidate
    wavefunction: Path
    output_dir: Path
    returncode: int
    paths_pdb: Path
    cps_pdb: Path
    mol_pdb: Path
    output_vesta: Optional[Path]
    stdout_log: Path
    stderr_log: Path
    command_file: Path
    success: bool
    cli_returncode: int
    error: Optional[str]


def read_command_file(path: Path) -> List[str]:
    # Blank lines can be meaningful in Multiwfn command streams because they
    # accept the current prompt's default value.  Preserve them as Enter.
    return [line.strip() for line in path.read_text(encoding="utf-8", errors="replace").splitlines()]


def _command_text(commands: Sequence[str]) -> str:
    return "\n".join(commands) + "\n"


def _run_environment(candidate: ExecutableCandidate) -> dict:
    env = dict(os.environ)
    # Multiwfn source reads Multiwfnpath; older project scripts used the other
    # spellings, so keep all three in sync for compatibility.
    env["Multiwfnpath"] = str(candidate.path.parent)
    env["MULTIWFNPATH"] = str(candidate.path.parent)
    env["MultiwfnPATH"] = str(candidate.path.parent)
    return env


def run_multiwfn_aim(
    wavefunction: Path,
    output_dir: Path,
    *,
    multiwfn_path: Optional[str] = None,
    commands: Optional[Sequence[str]] = None,
    commands_file: Optional[Path] = None,
    timeout: Optional[int] = None,
    nthreads: Optional[int] = None,
    convert_vesta: bool = True,
    output_vesta: Optional[Path] = None,
    cube_frame_from_cube: Optional[Path] = None,
    require_paths: bool = True,
) -> MultiwfnAimResult:
    candidate = find_multiwfn(multiwfn_path)
    if candidate is None:
        raise FileNotFoundError(
            "Cannot find Multiwfn. Set MULTIWFN_PATH/MULTIWFNPATH/MultiwfnPATH "
            "or add Multiwfn/Multiwfn_noGUI to PATH."
        )

    wavefunction = Path(wavefunction).expanduser().resolve()
    if not wavefunction.exists():
        raise FileNotFoundError("Wavefunction file not found: {}".format(wavefunction))

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if commands_file is not None:
        command_list = read_command_file(commands_file)
    elif commands is not None:
        command_list = list(commands)
    else:
        command_list = list(DEFAULT_AIM_COMMANDS)

    command_file = output_dir / "multiwfn_aim_input.txt"
    stdout_log = output_dir / "multiwfn.stdout.txt"
    stderr_log = output_dir / "multiwfn.stderr.txt"
    command_file.write_text(_command_text(command_list), encoding="utf-8")

    command = [str(candidate.path), str(wavefunction)]
    if nthreads is not None and nthreads > 1:
        command.extend(["-nt", str(nthreads)])

    completed = subprocess.run(
        command,
        input=_command_text(command_list),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(output_dir),
        env=_run_environment(candidate),
        timeout=timeout,
    )
    stdout_log.write_text(completed.stdout or "", encoding="utf-8")
    stderr_log.write_text(completed.stderr or "", encoding="utf-8")

    paths_pdb = output_dir / "paths.pdb"
    cps_pdb = output_dir / "CPs.pdb"
    mol_pdb = output_dir / "mol.pdb"
    vesta_path = Path(output_vesta) if output_vesta else output_dir / "aim_atoms_only.vesta"
    if output_vesta is not None and not vesta_path.is_absolute():
        vesta_path = output_dir / vesta_path

    error = None
    cli_returncode = completed.returncode
    if completed.returncode == 0 and require_paths and not paths_pdb.exists():
        error = (
            "Multiwfn finished with return code 0, but AIM output `paths.pdb` "
            "was not generated in {}. Check {} and {}."
        ).format(output_dir, stdout_log, stderr_log)
        cli_returncode = AIM_OUTPUT_MISSING_CODE

    if completed.returncode == 0 and cli_returncode == 0 and convert_vesta and paths_pdb.exists():
        convert_aim_pdb_to_vesta(
            paths_pdb,
            vesta_path,
            cps_pdb=cps_pdb if cps_pdb.exists() else None,
            title="Multiwfn AIM paths and CPs",
            cube_frame_from_cube=cube_frame_from_cube,
        )
    else:
        vesta_path = None

    return MultiwfnAimResult(
        multiwfn=candidate,
        wavefunction=wavefunction,
        output_dir=output_dir,
        returncode=completed.returncode,
        paths_pdb=paths_pdb,
        cps_pdb=cps_pdb,
        mol_pdb=mol_pdb,
        output_vesta=vesta_path,
        stdout_log=stdout_log,
        stderr_log=stderr_log,
        command_file=command_file,
        success=cli_returncode == 0,
        cli_returncode=cli_returncode,
        error=error,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run Multiwfn AIM analysis on a wavefunction file and optionally convert paths/CPs to VESTA.",
        epilog=(
            "Default outputs in output_dir: multiwfn_aim_input.txt, multiwfn.stdout.txt, "
            "multiwfn.stderr.txt, paths.pdb, CPs.pdb, mol.pdb, and aim_atoms_only.vesta. "
            "Multiwfn is discovered from --multiwfn, MULTIWFN_PATH/MULTIWFNPATH/"
            "Multiwfnpath/MultiwfnPATH, workspace tools, then PATH. VESTA is not "
            "launched by this command; use aim-igmh --render-three-views for explicit "
            "VESTA rendering."
        ),
    )
    parser.add_argument("wavefunction", type=Path, help="Wavefunction file accepted by Multiwfn, e.g. .molden/.fch/.wfn")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--multiwfn", "--multiwfn-path", dest="multiwfn_path")
    parser.add_argument("--commands-file", type=Path, help="Override the default Multiwfn AIM command stream")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--nthreads", type=int)
    parser.add_argument("--no-vesta", action="store_true", help="Do not convert paths.pdb/CPs.pdb to VESTA")
    parser.add_argument("--output-vesta", type=Path)
    parser.add_argument("--cube-frame-from-cube", type=Path)
    parser.add_argument(
        "--allow-missing-paths",
        action="store_true",
        help="Return Multiwfn's own return code even if paths.pdb is not generated.",
    )
    args = parser.parse_args(argv)

    result = run_multiwfn_aim(
        args.wavefunction,
        args.output_dir,
        multiwfn_path=args.multiwfn_path,
        commands_file=args.commands_file,
        timeout=args.timeout,
        nthreads=args.nthreads,
        convert_vesta=not args.no_vesta,
        output_vesta=args.output_vesta,
        cube_frame_from_cube=args.cube_frame_from_cube,
        require_paths=not args.allow_missing_paths,
    )

    print("Multiwfn: {}".format(result.multiwfn.path))
    print("returncode: {}".format(result.returncode))
    if result.cli_returncode != result.returncode:
        print("cli_returncode: {}".format(result.cli_returncode))
    print(result.command_file)
    print(result.stdout_log)
    print(result.stderr_log)
    if result.paths_pdb.exists():
        print(result.paths_pdb)
    if result.cps_pdb.exists():
        print(result.cps_pdb)
    if result.mol_pdb.exists():
        print(result.mol_pdb)
    if result.output_vesta is not None and result.output_vesta.exists():
        print(result.output_vesta)
    if result.error:
        print("ERROR: {}".format(result.error), file=sys.stderr)
    return result.cli_returncode


if __name__ == "__main__":
    raise SystemExit(main())
