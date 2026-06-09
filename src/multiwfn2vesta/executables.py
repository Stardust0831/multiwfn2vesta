"""Executable discovery helpers for Multiwfn and VESTA."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from typing import Iterable, List, NamedTuple, Optional, Sequence


class ExecutableCandidate(NamedTuple):
    name: str
    path: Path
    source: str
    exists: bool
    executable: bool


MULTIWFN_ENV_VARS = (
    "MULTIWFN_PATH",
    "MULTIWFNPATH",
    "MultiwfnPATH",
    "MultiwfnPath",
    "Multiwfnpath",
    "MULTIWFN_EXECUTABLE",
)

VESTA_ENV_VARS = (
    "VESTA_PATH",
    "VESTA_DIR",
    "VESTAPATH",
    "VestaPATH",
    "Vestapath",
    "VESTA_EXECUTABLE",
)

MULTIWFN_NAMES = ("Multiwfn_noGUI", "Multiwfn", "Multiwfn.exe")
VESTA_NAMES = ("VESTA.exe", "VESTA")


def project_dir() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_root() -> Path:
    return project_dir().parent


def _is_executable(path: Path) -> bool:
    return path.is_file() and os.access(str(path), os.X_OK)


def _candidate(name: str, path: Path, source: str) -> ExecutableCandidate:
    return ExecutableCandidate(
        name=name,
        path=path,
        source=source,
        exists=path.exists(),
        executable=_is_executable(path),
    )


def _looks_like_windows_path(value: str) -> bool:
    return (len(value) >= 3 and value[1] == ":" and value[2] in {"/", "\\"}) or value.startswith("\\\\")


def _normalize_user_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute() and not _looks_like_windows_path(value):
        return path.resolve()
    return path


def _dedupe(candidates: Iterable[ExecutableCandidate]) -> List[ExecutableCandidate]:
    seen = set()
    out: List[ExecutableCandidate] = []
    for candidate in candidates:
        key = str(candidate.path)
        if key in seen:
            continue
        seen.add(key)
        out.append(candidate)
    return out


def _from_value(value: str, names: Sequence[str], source: str) -> List[ExecutableCandidate]:
    if not value:
        return []
    path = _normalize_user_path(value)
    candidates: List[ExecutableCandidate] = []
    if path.is_dir():
        for name in names:
            candidates.append(_candidate(name, path / name, source))
    else:
        candidates.append(_candidate(path.name, path, source))
    return candidates


def _from_env(env_names: Sequence[str], names: Sequence[str]) -> List[ExecutableCandidate]:
    candidates: List[ExecutableCandidate] = []
    for env_name in env_names:
        value = os.environ.get(env_name)
        if value:
            candidates.extend(_from_value(value, names, "env:" + env_name))
    return candidates


def _from_path(names: Sequence[str]) -> List[ExecutableCandidate]:
    candidates: List[ExecutableCandidate] = []
    for name in names:
        resolved = shutil.which(name)
        if resolved:
            candidates.append(_candidate(name, Path(resolved), "PATH"))
    return candidates


def _workspace_multiwfn_candidates() -> List[ExecutableCandidate]:
    root = workspace_root()
    return [
        _candidate(
            "Multiwfn_noGUI",
            root / "tools" / "Multiwfn_2026.6.2_bin_Linux_noGUI" / "Multiwfn_noGUI",
            "workspace",
        ),
        _candidate(
            "Multiwfn",
            root / "tools" / "Multiwfn_2026.6.2_bin_Linux" / "Multiwfn",
            "workspace",
        ),
        _candidate(
            "Multiwfn.exe",
            root / "tools" / "Multiwfn_2026.6.2_bin_Win64" / "Multiwfn.exe",
            "workspace",
        ),
    ]


def _workspace_vesta_candidates() -> List[ExecutableCandidate]:
    root = workspace_root()
    return [
        _candidate("VESTA.exe", root / "tools" / "VESTA-win64" / "VESTA.exe", "workspace"),
        _candidate("VESTA", root / "tools" / "VESTA-gtk3-x86_64" / "VESTA", "workspace"),
    ]


def multiwfn_candidates(explicit: Optional[str] = None) -> List[ExecutableCandidate]:
    candidates: List[ExecutableCandidate] = []
    if explicit:
        candidates.extend(_from_value(explicit, MULTIWFN_NAMES, "explicit"))
    candidates.extend(_from_env(MULTIWFN_ENV_VARS, MULTIWFN_NAMES))
    # Prefer the workspace noGUI binary before arbitrary PATH hits.  This avoids
    # accidentally selecting a Windows GUI binary from a WSL PATH.
    candidates.extend(_workspace_multiwfn_candidates())
    candidates.extend(_from_path(MULTIWFN_NAMES))
    return _dedupe(candidates)


def vesta_candidates(explicit: Optional[str] = None) -> List[ExecutableCandidate]:
    candidates: List[ExecutableCandidate] = []
    if explicit:
        candidates.extend(_from_value(explicit, VESTA_NAMES, "explicit"))
    candidates.extend(_from_env(VESTA_ENV_VARS, VESTA_NAMES))
    candidates.extend(_workspace_vesta_candidates())
    candidates.extend(_from_path(VESTA_NAMES))
    return _dedupe(candidates)


def find_multiwfn(explicit: Optional[str] = None) -> Optional[ExecutableCandidate]:
    for candidate in multiwfn_candidates(explicit):
        if candidate.executable:
            return candidate
    return None


def find_vesta(explicit: Optional[str] = None) -> Optional[ExecutableCandidate]:
    for candidate in vesta_candidates(explicit):
        if candidate.executable or candidate.exists:
            return candidate
    return None


def vesta_windows_dir(explicit: Optional[str] = None) -> Optional[Path]:
    for candidate in vesta_candidates(explicit):
        path = candidate.path
        if path.is_dir() and (path / "VESTA.exe").exists():
            return path
        if path.name.lower() == "vesta.exe" and path.exists():
            return path.parent
    return None


def discovery_report() -> str:
    lines = ["# Executable discovery", "", "## Multiwfn", ""]
    selected_multiwfn = find_multiwfn()
    if selected_multiwfn is not None:
        lines.append("- selected: `{}` from `{}`".format(selected_multiwfn.path, selected_multiwfn.source))
    else:
        lines.append("- selected: not found")
    lines.append("")
    for candidate in multiwfn_candidates():
        lines.append(
            "- `{}` from `{}` exists={} executable={}".format(
                candidate.path, candidate.source, candidate.exists, candidate.executable
            )
        )
    lines.extend(["", "## VESTA", ""])
    selected_vesta = find_vesta()
    if selected_vesta is not None:
        lines.append("- selected: `{}` from `{}`".format(selected_vesta.path, selected_vesta.source))
    else:
        lines.append("- selected: not found")
    windows_dir = vesta_windows_dir()
    if windows_dir is not None:
        lines.append("- windows_cli_dir: `{}`".format(windows_dir))
    lines.append("")
    for candidate in vesta_candidates():
        lines.append(
            "- `{}` from `{}` exists={} executable={}".format(
                candidate.path, candidate.source, candidate.exists, candidate.executable
            )
        )
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"-h", "--help", "help"}:
        print(
            "Usage: multiwfn2vesta-discover\n\n"
            "Reports Multiwfn and VESTA executable candidates from explicit project "
            "defaults, environment variables, PATH, and workspace-local tools."
        )
        return 0
    if args:
        print("discover does not accept positional arguments: {}".format(" ".join(args)), file=sys.stderr)
        return 2
    print(discovery_report(), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
