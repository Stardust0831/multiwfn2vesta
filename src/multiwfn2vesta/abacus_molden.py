"""Run the latest ABACUS Molden converter and validate the output."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

from .molden_check import MoldenCheckResult, check_molden_file, format_report


ABACUS_MOLDEN_FAILED = 2
ABACUS_MOLDEN_CHECK_FAILED = 1

MOLDEN_SCRIPT_PATH = "interfaces/Multiwfn_interface/molden.py"
REQUIRED_CONVERTER_MODULES = ("numpy", "scipy", "matplotlib")


@dataclass
class AbacusMoldenSource:
    script_path: Path
    origin: str
    repo: Optional[Path]
    git_ref: Optional[str]
    commit: Optional[str]
    commit_date: Optional[str]
    source_path: str
    sha256: str


@dataclass
class AbacusMoldenResult:
    calc_dir: Path
    output_molden: Path
    source: AbacusMoldenSource
    command: List[str]
    returncode: int
    stdout_log: Path
    stderr_log: Path
    recipe: Path
    check_result: Optional[MoldenCheckResult]
    success: bool
    cli_returncode: int
    error: Optional[str] = None


def _workspace_root() -> Path:
    return Path(__file__).resolve().parents[3]


def default_abacus_repo() -> Path:
    return _workspace_root() / "downloads" / "abacus_latest_molden" / "abacus-develop"


def _run_text(command: Sequence[str], *, cwd: Optional[Path] = None) -> str:
    completed = subprocess.run(
        list(command),
        cwd=str(cwd) if cwd is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    return completed.stdout.strip()


def _run_raw_text(command: Sequence[str], *, cwd: Optional[Path] = None) -> str:
    completed = subprocess.run(
        list(command),
        cwd=str(cwd) if cwd is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    return completed.stdout


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def _timeout_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def check_python_modules(python_executable: str, modules: Sequence[str]) -> List[str]:
    code = (
        "import importlib, sys\n"
        f"modules = {list(modules)!r}\n"
        "missing = []\n"
        "for module in modules:\n"
        "    try:\n"
        "        importlib.import_module(module)\n"
        "    except Exception:\n"
        "        missing.append(module)\n"
        "if missing:\n"
        "    print(','.join(missing))\n"
        "    sys.exit(1)\n"
    )
    completed = subprocess.run(
        [python_executable, "-c", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode == 0:
        return []
    stdout = (completed.stdout or "").strip()
    if stdout:
        return [item.strip() for item in stdout.split(",") if item.strip()]
    return list(modules)


def _copy_explicit_script(script: Path, destination: Path) -> AbacusMoldenSource:
    script = script.expanduser().resolve()
    if not script.exists():
        raise FileNotFoundError(f"ABACUS Molden script not found: {script}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    content = script.read_text(encoding="utf-8", errors="replace")
    destination.write_text(content, encoding="utf-8")
    destination.chmod(0o755)
    return AbacusMoldenSource(
        script_path=destination,
        origin="file",
        repo=None,
        git_ref=None,
        commit=None,
        commit_date=None,
        source_path=str(script),
        sha256=_sha256_text(content),
    )


def _export_git_script(
    repo: Path,
    git_ref: str,
    destination: Path,
    *,
    source_path: str = MOLDEN_SCRIPT_PATH,
    fetch: bool = False,
) -> AbacusMoldenSource:
    repo = repo.expanduser().resolve()
    if not repo.exists():
        raise FileNotFoundError(f"ABACUS repository not found: {repo}")
    if fetch:
        subprocess.run(["git", "fetch", "origin", "develop"], cwd=str(repo), check=True)

    commit = _run_text(["git", "rev-parse", git_ref], cwd=repo)
    commit_date = _run_text(["git", "show", "-s", "--format=%cI", git_ref], cwd=repo)
    content = _run_raw_text(["git", "show", f"{git_ref}:{source_path}"], cwd=repo)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    destination.chmod(0o755)
    return AbacusMoldenSource(
        script_path=destination,
        origin="git",
        repo=repo,
        git_ref=git_ref,
        commit=commit,
        commit_date=commit_date,
        source_path=source_path,
        sha256=_sha256_text(content),
    )


def prepare_molden_script(
    *,
    output_molden: Path,
    script: Optional[Path] = None,
    abacus_repo: Optional[Path] = None,
    git_ref: str = "origin/develop",
    source_path: str = MOLDEN_SCRIPT_PATH,
    fetch: bool = False,
) -> AbacusMoldenSource:
    script_copy = output_molden.with_name(f"{output_molden.stem}_abacus_molden.py")
    if script is not None:
        return _copy_explicit_script(script, script_copy)
    return _export_git_script(
        abacus_repo or default_abacus_repo(),
        git_ref,
        script_copy,
        source_path=source_path,
        fetch=fetch,
    )


def write_recipe(result: AbacusMoldenResult) -> None:
    source = result.source
    lines = [
        "# ABACUS Molden Recipe",
        "",
        f"- calc_dir: `{result.calc_dir}`",
        f"- output_molden: `{result.output_molden}`",
        f"- source_origin: `{source.origin}`",
        f"- source_path: `{source.source_path}`",
        f"- script_copy: `{source.script_path}`",
        f"- script_sha256: `{source.sha256}`",
    ]
    if source.repo is not None:
        lines.append(f"- abacus_repo: `{source.repo}`")
    if source.git_ref is not None:
        lines.append(f"- git_ref: `{source.git_ref}`")
    if source.commit is not None:
        lines.append(f"- commit: `{source.commit}`")
    if source.commit_date is not None:
        lines.append(f"- commit_date: `{source.commit_date}`")
    lines.extend(
        [
            f"- returncode: `{result.returncode}`",
            f"- cli_returncode: `{result.cli_returncode}`",
            f"- stdout_log: `{result.stdout_log}`",
            f"- stderr_log: `{result.stderr_log}`",
            "",
            "## Command",
            "",
            "```bash",
            " ".join(result.command),
            "```",
            "",
        ]
    )
    if result.error is not None:
        lines.extend(["## Error", "", result.error, ""])
    if result.check_result is not None:
        lines.extend(["## Molden Check", "", "```text", format_report(result.check_result, abacus=True).rstrip(), "```", ""])
    result.recipe.write_text("\n".join(lines), encoding="utf-8")


def run_abacus_molden(
    calc_dir: Path,
    output_molden: Path,
    *,
    script: Optional[Path] = None,
    abacus_repo: Optional[Path] = None,
    git_ref: str = "origin/develop",
    source_path: str = MOLDEN_SCRIPT_PATH,
    fetch: bool = False,
    python_executable: Optional[str] = None,
    ndigits: int = 3,
    ngto: int = 7,
    rel_r: str = "2",
    with_cell: bool = True,
    with_nval: bool = True,
    with_pseudo: bool = False,
    timeout: Optional[int] = None,
    check_output: bool = True,
    check_dependencies: bool = True,
) -> AbacusMoldenResult:
    calc_dir = calc_dir.expanduser().resolve()
    if not calc_dir.exists():
        raise FileNotFoundError(f"ABACUS calculation directory not found: {calc_dir}")
    output_molden = output_molden.expanduser().resolve()
    output_molden.parent.mkdir(parents=True, exist_ok=True)

    source = prepare_molden_script(
        output_molden=output_molden,
        script=script,
        abacus_repo=abacus_repo,
        git_ref=git_ref,
        source_path=source_path,
        fetch=fetch,
    )

    stdout_log = output_molden.with_name(f"{output_molden.stem}_abacus_molden.stdout.txt")
    stderr_log = output_molden.with_name(f"{output_molden.stem}_abacus_molden.stderr.txt")
    recipe = output_molden.with_name(f"{output_molden.stem}_abacus_molden_recipe.md")
    python_cmd = python_executable or sys.executable
    command = [
        python_cmd,
        str(source.script_path),
        "-f",
        str(calc_dir),
        "-o",
        str(output_molden),
        "-n",
        str(ndigits),
        "-g",
        str(ngto),
        "-r",
        rel_r,
        "--with-cell",
        _bool_text(with_cell),
        "--with-Nval",
        _bool_text(with_nval),
        "--with-pseudo",
        _bool_text(with_pseudo),
    ]

    if check_dependencies:
        missing_modules = check_python_modules(python_cmd, REQUIRED_CONVERTER_MODULES)
        if missing_modules:
            error = (
                "ABACUS molden.py Python dependency preflight failed for "
                f"{python_cmd}: missing {', '.join(missing_modules)}. "
                "Use --python to select an environment with numpy, scipy, and matplotlib, "
                "or pass --no-dependency-check if you intentionally want to skip this preflight."
            )
            stdout_log.write_text("", encoding="utf-8")
            stderr_log.write_text(error + "\n", encoding="utf-8")
            result = AbacusMoldenResult(
                calc_dir=calc_dir,
                output_molden=output_molden,
                source=source,
                command=command,
                returncode=ABACUS_MOLDEN_FAILED,
                stdout_log=stdout_log,
                stderr_log=stderr_log,
                recipe=recipe,
                check_result=None,
                success=False,
                cli_returncode=ABACUS_MOLDEN_FAILED,
                error=error,
            )
            write_recipe(result)
            return result

    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(output_molden.parent),
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        stdout_text = _timeout_text(getattr(exc, "stdout", None) or getattr(exc, "output", None))
        stderr_text = _timeout_text(getattr(exc, "stderr", None))
        error = f"ABACUS molden.py timed out after {timeout} seconds; inspect {stdout_log} and {stderr_log}"
        stdout_log.write_text(stdout_text, encoding="utf-8")
        stderr_log.write_text((stderr_text + "\n" if stderr_text else "") + error + "\n", encoding="utf-8")
        result = AbacusMoldenResult(
            calc_dir=calc_dir,
            output_molden=output_molden,
            source=source,
            command=command,
            returncode=ABACUS_MOLDEN_FAILED,
            stdout_log=stdout_log,
            stderr_log=stderr_log,
            recipe=recipe,
            check_result=None,
            success=False,
            cli_returncode=ABACUS_MOLDEN_FAILED,
            error=error,
        )
        write_recipe(result)
        return result
    stdout_log.write_text(completed.stdout or "", encoding="utf-8")
    stderr_log.write_text(completed.stderr or "", encoding="utf-8")

    check_result: Optional[MoldenCheckResult] = None
    error: Optional[str] = None
    cli_returncode = completed.returncode if completed.returncode != 0 else 0
    if completed.returncode == 0:
        if not output_molden.exists():
            error = f"ABACUS molden.py returned 0 but did not write output Molden file: {output_molden}"
            cli_returncode = ABACUS_MOLDEN_CHECK_FAILED
        elif check_output:
            check_result = check_molden_file(output_molden, abacus=True)
            if not check_result.ok:
                cli_returncode = ABACUS_MOLDEN_CHECK_FAILED
    elif completed.returncode != 0:
        cli_returncode = completed.returncode or ABACUS_MOLDEN_FAILED
        error = f"ABACUS molden.py failed with return code {completed.returncode}; inspect {stdout_log} and {stderr_log}"

    result = AbacusMoldenResult(
        calc_dir=calc_dir,
        output_molden=output_molden,
        source=source,
        command=command,
        returncode=completed.returncode,
        stdout_log=stdout_log,
        stderr_log=stderr_log,
        recipe=recipe,
        check_result=check_result,
        success=cli_returncode == 0,
        cli_returncode=cli_returncode,
        error=error,
    )
    write_recipe(result)
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate an ABACUS LCAO Molden file with the latest ABACUS Multiwfn interface and validate it.",
        epilog=(
            "The default source is downloads/abacus_latest_molden/abacus-develop "
            "at git ref origin/develop, path interfaces/Multiwfn_interface/molden.py. "
            "The generated Molden is checked with molden-check --abacus unless --no-check is used."
        ),
    )
    parser.add_argument("calc_dir", type=Path, help="ABACUS calculation directory containing INPUT, KPT, STRU, and OUT.<suffix>")
    parser.add_argument("output_molden", type=Path, help="Output Molden path; it is passed to ABACUS as an absolute -o path")
    parser.add_argument("--script", type=Path, help="Explicit molden.py script; skips git export")
    parser.add_argument("--abacus-repo", type=Path, default=default_abacus_repo(), help="ABACUS develop checkout")
    parser.add_argument("--git-ref", default="origin/develop", help="Git ref to export the converter from")
    parser.add_argument("--source-path", default=MOLDEN_SCRIPT_PATH, help="Path to molden.py inside the ABACUS git tree")
    parser.add_argument("--fetch", action="store_true", help="Run git fetch origin develop before exporting --git-ref")
    parser.add_argument("--python", dest="python_executable", help="Python executable used to run molden.py")
    parser.add_argument("-n", "--ndigits", type=int, default=3)
    parser.add_argument("-g", "--ngto", type=int, default=7)
    parser.add_argument("-r", "--rel-r", default="2", help="Relative cutoff radius; ABACUS accepts comma-separated multi-start values")
    parser.add_argument("--with-cell", choices=("true", "false"), default="true")
    parser.add_argument("--with-Nval", dest="with_nval", choices=("true", "false"), default="true")
    parser.add_argument("--with-pseudo", choices=("true", "false"), default="false")
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--no-dependency-check", action="store_true", help="Skip the numpy/scipy/matplotlib Python preflight for ABACUS molden.py")
    parser.add_argument("--no-check", action="store_true", help="Do not run molden-check --abacus after conversion")
    args = parser.parse_args(argv)

    def as_bool(text: str) -> bool:
        return text == "true"

    try:
        result = run_abacus_molden(
            args.calc_dir,
            args.output_molden,
            script=args.script,
            abacus_repo=args.abacus_repo,
            git_ref=args.git_ref,
            source_path=args.source_path,
            fetch=args.fetch,
            python_executable=args.python_executable,
            ndigits=args.ndigits,
            ngto=args.ngto,
            rel_r=args.rel_r,
            with_cell=as_bool(args.with_cell),
            with_nval=as_bool(args.with_nval),
            with_pseudo=as_bool(args.with_pseudo),
            timeout=args.timeout,
            check_output=not args.no_check,
            check_dependencies=not args.no_dependency_check,
        )
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"abacus-molden: {exc}", file=sys.stderr)
        return ABACUS_MOLDEN_FAILED

    print(f"ABACUS Molden script: {result.source.script_path}")
    if result.source.commit:
        print(f"ABACUS commit: {result.source.commit}")
    print(f"returncode: {result.returncode}")
    if result.cli_returncode != result.returncode:
        print(f"cli_returncode: {result.cli_returncode}")
    print(result.output_molden)
    print(result.stdout_log)
    print(result.stderr_log)
    print(result.recipe)
    if result.error:
        print(f"ERROR: {result.error}", file=sys.stderr)
    if result.check_result is not None:
        print(format_report(result.check_result, abacus=True), end="")
    return result.cli_returncode


if __name__ == "__main__":
    raise SystemExit(main())
