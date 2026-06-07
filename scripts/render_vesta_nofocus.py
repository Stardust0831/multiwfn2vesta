#!/usr/bin/env python3
"""Render a VESTA image through Windows interop with a minimized window.

This is not a true headless renderer.  It is an isolated experiment for the
`vesta-nofocus-render` branch: start VESTA minimized through PowerShell, wait
for export, then clean only VESTA processes whose command line points at this
workspace.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


POWERSHELL = Path("/mnt/c/WINDOWS/system32/WindowsPowerShell/v1.0/powershell.exe")


def workspace_root() -> Path:
    return Path(__file__).resolve().parents[2]


def windows_path(path: Path) -> str:
    result = subprocess.run(
        ["wslpath", "-w", str(path)],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return result.stdout.strip()


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def cleanup_workspace_vesta(workspace_win: str) -> None:
    pattern = "*" + workspace_win.rstrip("\\") + "*"
    script = (
        "Get-CimInstance Win32_Process | "
        "Where-Object { $_.Name -eq 'VESTA.exe' -and "
        f"$_.CommandLine -like {ps_quote(pattern)} }} | "
        "ForEach-Object { Stop-Process -Id $_.ProcessId -Force "
        "-ErrorAction SilentlyContinue }"
    )
    subprocess.run([str(POWERSHELL), "-NoProfile", "-Command", script], check=False)


def render(args: argparse.Namespace) -> int:
    root = workspace_root()
    vesta = Path(args.vesta_exe) if args.vesta_exe else root / "tools" / "VESTA-win64" / "VESTA.exe"
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    vesta_win = windows_path(vesta)
    input_win = windows_path(input_path)
    output_win = windows_path(output_path)
    root_win = windows_path(root)
    timeout_ms = int(args.timeout * 1000)
    arguments = [
        "-open",
        input_win,
        "-export_img",
        f"scale={args.scale}",
        output_win,
        "-flush",
        "-close",
    ]
    ps_args = "@(" + ",".join(ps_quote(item) for item in arguments) + ")"
    script = f"""
$p = Start-Process -FilePath {ps_quote(vesta_win)} -ArgumentList {ps_args} -WindowStyle Minimized -PassThru
if (-not $p.WaitForExit({timeout_ms})) {{
  Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
  exit 124
}}
exit $p.ExitCode
"""
    if args.clean_before:
        cleanup_workspace_vesta(root_win)
    result = subprocess.run([str(POWERSHELL), "-NoProfile", "-Command", script], check=False)
    if args.clean_after:
        cleanup_workspace_vesta(root_win)
    if not output_path.exists():
        return result.returncode or 1
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--vesta-exe")
    parser.add_argument("--scale", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=220, help="Seconds before killing this VESTA process")
    parser.add_argument("--clean-before", action="store_true")
    parser.add_argument("--clean-after", action="store_true", default=True)
    args = parser.parse_args(argv[1:])
    return render(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
