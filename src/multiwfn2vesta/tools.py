"""Human-facing stable tools built on top of maintained workflow commands."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from . import (
    abacus_esp_align,
    abacus_lr_to_multiwfn,
    abacus_mulliken,
    aim_igmh_vesta,
    aim_vesta,
    cube_preset,
    examples,
    multiwfn_atom_table,
    trajectory_frames,
    trajectory_video,
)
from .executables import discovery_report


Lang = str


@dataclass(frozen=True)
class ToolSpec:
    name: str
    command: str
    status: str
    summary_en: str
    summary_zh: str
    usage_en: str
    usage_zh: str
    notes_en: str = ""
    notes_zh: str = ""


STABLE_TOOLS: Tuple[ToolSpec, ...] = (
    ToolSpec(
        name="discover",
        command="discover",
        status="stable",
        summary_en="Find workspace-local Multiwfn and VESTA executables.",
        summary_zh="查找当前工作区可用的 Multiwfn 和 VESTA 可执行文件。",
        usage_en="multiwfn2vesta tools run discover",
        usage_zh="multiwfn2vesta tools run discover",
    ),
    ToolSpec(
        name="examples",
        command="examples",
        status="stable",
        summary_en="List curated examples, gallery assets, and readiness status.",
        summary_zh="列出已整理的算例、图库素材和功能闭环状态。",
        usage_en="multiwfn2vesta tools run examples -- --summary",
        usage_zh="multiwfn2vesta tools run examples -- --summary",
    ),
    ToolSpec(
        name="cube",
        command="cube-preset",
        status="stable",
        summary_en="Convert a cube into a VESTA file with a maintained display preset.",
        summary_zh="把 cube 文件按维护好的 preset 转成 VESTA 场景。",
        usage_en="multiwfn2vesta tools run cube -- density.cub products --preset density",
        usage_zh="multiwfn2vesta tools run cube -- density.cub products --preset density",
        notes_en="This forwards to cube-preset. Put the preset first when using the low-level command directly.",
        notes_zh="该工具转发到 cube-preset；直接用底层命令时 preset 需要放在最前面。",
    ),
    ToolSpec(
        name="esp-surface",
        command="esp-surface",
        status="stable",
        summary_en="Build a VESTA density-surface ESP coloring scene from ABACUS density and electrostatic-potential cubes.",
        summary_zh="从 ABACUS 电子密度 cube 和静电势 cube 生成真空归零 ESP 范德华表面染色 VESTA 场景。",
        usage_en=(
            "multiwfn2vesta tools run esp-surface -- chg.cube potes.cube products "
            "--axis z --tex-physical -0.08 0.08"
        ),
        usage_zh=(
            "multiwfn2vesta tools run esp-surface -- chg.cube potes.cube products "
            "--axis z --tex-physical -0.08 0.08"
        ),
        notes_en="Runs abacus-esp-align first, then cube-preset esp.",
        notes_zh="先执行 abacus-esp-align 真空归零，再执行 cube-preset esp。",
    ),
    ToolSpec(
        name="excitation-bridge",
        command="abacus-lr-to-multiwfn",
        status="stable",
        summary_en="Convert single-rank ABACUS LR-TDDFT amplitudes to Multiwfn plain excitation text.",
        summary_zh="把单 rank ABACUS LR-TDDFT 振幅转换成 Multiwfn 可读的 plain text 激发组态。",
        usage_en="multiwfn2vesta tools run excitation-bridge -- OUT.lr h2o_singlet.excit.txt --label singlet",
        usage_zh="multiwfn2vesta tools run excitation-bridge -- OUT.lr h2o_singlet.excit.txt --label singlet",
        notes_en="Only the tested Gamma/single-rank bridge is marked stable.",
        notes_zh="这里只把已测试的 Gamma/single-rank 桥接标为稳定。",
    ),
    ToolSpec(
        name="aim-pdb",
        command="aim-pdb",
        status="stable",
        summary_en="Convert Multiwfn AIM paths.pdb/CPs.pdb into atoms-only VESTA without fake bonds.",
        summary_zh="把 Multiwfn AIM 的 paths.pdb/CPs.pdb 转成 atoms-only VESTA，避免伪键。",
        usage_en="multiwfn2vesta tools run aim-pdb -- paths.pdb aim_atoms_only.vesta --cps-pdb CPs.pdb",
        usage_zh="multiwfn2vesta tools run aim-pdb -- paths.pdb aim_atoms_only.vesta --cps-pdb CPs.pdb",
    ),
    ToolSpec(
        name="aim-igmh",
        command="aim-igmh",
        status="stable",
        summary_en="Style a saved AIM+IGMH VESTA overlay; rendering remains explicit.",
        summary_zh="整理已保存的 AIM+IGMH VESTA 叠图；渲染仍需显式开启。",
        usage_en="multiwfn2vesta tools run aim-igmh -- overlay.vesta products --label-bcp-sites",
        usage_zh="multiwfn2vesta tools run aim-igmh -- overlay.vesta products --label-bcp-sites",
        notes_en="Avoids changing AIM coordinates; three-view rendering may still involve VESTA UI.",
        notes_zh="不移动 AIM 坐标；三视图渲染仍可能涉及 VESTA 界面。",
    ),
    ToolSpec(
        name="trajectory-frames",
        command="trajectory-frames",
        status="stable",
        summary_en="Convert XYZ/extXYZ trajectories to per-frame VESTA files without launching VESTA.",
        summary_zh="把 XYZ/extXYZ 轨迹转换成逐帧 VESTA 文件，不启动 VESTA。",
        usage_en=(
            "multiwfn2vesta tools run trajectory-frames -- traj.extxyz frames "
            "--reference-vesta saved.vesta --boundary -0.05 1.05 -0.05 1.05 -0.05 1.05"
        ),
        usage_zh=(
            "multiwfn2vesta tools run trajectory-frames -- traj.extxyz frames "
            "--reference-vesta saved.vesta --boundary -0.05 1.05 -0.05 1.05 -0.05 1.05"
        ),
    ),
    ToolSpec(
        name="trajectory-video",
        command="trajectory-video",
        status="stable",
        summary_en="Encode already rendered PNG trajectory frames into a high-bitrate MP4.",
        summary_zh="把已经渲染好的 PNG 轨迹帧编码成高码率 MP4。",
        usage_en="multiwfn2vesta tools run trajectory-video -- png_frames movie.mp4 --bitrate 20M --run",
        usage_zh="multiwfn2vesta tools run trajectory-video -- png_frames movie.mp4 --bitrate 20M --run",
        notes_en="Does not start VESTA; it only wraps ffmpeg frame encoding.",
        notes_zh="不会启动 VESTA；只负责 ffmpeg 帧序列编码。",
    ),
    ToolSpec(
        name="abacus-atom-color",
        command="abacus-mulliken-color",
        status="stable",
        summary_en="Color VESTA atoms from ABACUS Mulliken charge or magnetism tables.",
        summary_zh="按 ABACUS Mulliken 电荷或磁矩给 VESTA 原子着色。",
        usage_en="multiwfn2vesta tools run abacus-atom-color -- input.vesta mulliken.txt colored.vesta --property charge",
        usage_zh="multiwfn2vesta tools run abacus-atom-color -- input.vesta mulliken.txt colored.vesta --property charge",
    ),
    ToolSpec(
        name="atom-table-color",
        command="multiwfn-atom-color",
        status="stable",
        summary_en="Color VESTA atoms from a generic atom scalar table.",
        summary_zh="按通用原子标量表给 VESTA 原子着色。",
        usage_en="multiwfn2vesta tools run atom-table-color -- input.vesta atom_values.csv colored.vesta --value-column charge",
        usage_zh="multiwfn2vesta tools run atom-table-color -- input.vesta atom_values.csv colored.vesta --value-column charge",
    ),
)


TOOL_BY_NAME: Dict[str, ToolSpec] = {tool.name: tool for tool in STABLE_TOOLS}
TOOL_ALIASES: Dict[str, str] = {
    "esp": "esp-surface",
    "esp-vdw": "esp-surface",
    "lr": "excitation-bridge",
    "excitation": "excitation-bridge",
    "aim": "aim-pdb",
    "igmh": "aim-igmh",
    "frames": "trajectory-frames",
    "movie": "trajectory-video",
    "video": "trajectory-video",
    "mulliken-color": "abacus-atom-color",
    "atom-color": "atom-table-color",
}


def normalize_lang(lang: str) -> Lang:
    value = (lang or "en").lower()
    if value in {"zh", "cn", "中文", "chinese"}:
        return "zh"
    return "en"


def _text(en: str, zh: str, lang: Lang) -> str:
    return zh if normalize_lang(lang) == "zh" else en


def _strip_separator(args: Sequence[str]) -> List[str]:
    values = list(args)
    if values and values[0] == "--":
        return values[1:]
    return values


def list_tools(*, lang: Lang = "en", as_json: bool = False) -> None:
    lang = normalize_lang(lang)
    if as_json:
        payload = [
            {
                "name": tool.name,
                "command": tool.command,
                "status": tool.status,
                "summary": _text(tool.summary_en, tool.summary_zh, lang),
                "usage": _text(tool.usage_en, tool.usage_zh, lang),
                "notes": _text(tool.notes_en, tool.notes_zh, lang),
            }
            for tool in STABLE_TOOLS
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(_text("Stable multiwfn2vesta tools", "multiwfn2vesta 稳定工具", lang))
    print(_text("Only workflows with local tests or explicit user-accepted use are listed here.", "这里只列出已有本地测试或用户明确认可可用的流程。", lang))
    for index, tool in enumerate(STABLE_TOOLS, start=1):
        summary = _text(tool.summary_en, tool.summary_zh, lang)
        usage = _text(tool.usage_en, tool.usage_zh, lang)
        notes = _text(tool.notes_en, tool.notes_zh, lang)
        print(f"\n{index}. {tool.name} [{tool.status}]")
        print(f"   {summary}")
        print(f"   {usage}")
        if notes:
            print(f"   {notes}")


def _dispatch_low_level(command: str, args: Sequence[str]) -> int:
    argv = list(args)
    if command == "discover":
        print(discovery_report(), end="")
        return 0
    if command == "examples":
        return examples.main(argv)
    if command == "cube-preset":
        if "--preset" in argv:
            index = argv.index("--preset")
            if index + 1 >= len(argv):
                raise SystemExit("--preset requires a value")
            preset = argv[index + 1]
            del argv[index : index + 2]
            argv.insert(0, preset)
        return cube_preset.main(argv)
    if command == "abacus-lr-to-multiwfn":
        return abacus_lr_to_multiwfn.main(argv)
    if command == "aim-pdb":
        return aim_vesta.main(argv)
    if command == "aim-igmh":
        return aim_igmh_vesta.main(argv)
    if command == "trajectory-frames":
        return trajectory_frames.main(argv)
    if command == "trajectory-video":
        return trajectory_video.main(argv)
    if command == "abacus-mulliken-color":
        return abacus_mulliken.main(argv)
    if command == "multiwfn-atom-color":
        return multiwfn_atom_table.main(argv)
    raise SystemExit(f"Tool command is not wired: {command}")


def run_esp_surface(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="multiwfn2vesta tools run esp-surface",
        description="Align an ABACUS electrostatic-potential cube to vacuum zero and create an ESP-colored density surface VESTA file.",
    )
    parser.add_argument("density_cube", type=Path, help="ABACUS electron density cube, e.g. chg.cube")
    parser.add_argument("esp_cube", type=Path, help="ABACUS electrostatic potential cube, e.g. potes.cube")
    parser.add_argument("output_dir", type=Path, help="output workflow directory")
    parser.add_argument("--axis", choices=("x", "y", "z"), default="z", help="vacuum/slab normal axis")
    parser.add_argument("--vacuum-side", choices=("low", "high", "both"), default="high")
    parser.add_argument("--vacuum-fraction", type=float, default=0.1)
    parser.add_argument("--vacuum-start", type=int)
    parser.add_argument("--vacuum-end", type=int)
    parser.add_argument("--isosurface", type=float, default=0.001)
    parser.add_argument("--tex-physical", nargs=2, type=float, default=(-0.08, 0.08), metavar=("MIN", "MAX"))
    parser.add_argument("--tex-range-source", choices=("full-cube", "surface-band"), default="surface-band")
    parser.add_argument("--surface-band", type=float)
    parser.add_argument("--surface-nearest", type=int, default=1024)
    parser.add_argument("--structure", choices=("auto", "none", "molecule", "crystal"), default="crystal")
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--stem", default="esp_surface")
    parser.add_argument("--no-copy-cubes", action="store_true")
    args = parser.parse_args(list(argv))

    root = args.output_dir
    root.mkdir(parents=True, exist_ok=True)
    shifted_cube = root / f"{args.esp_cube.stem}_vacuum0.cube"
    profile_csv = root / f"{args.esp_cube.stem}_profile.csv"
    report_md = root / f"{args.esp_cube.stem}_alignment.md"
    vesta_dir = root / "vesta"

    alignment = abacus_esp_align.align_cube(
        args.esp_cube,
        shifted_cube,
        axis=args.axis,
        vacuum_side=args.vacuum_side,
        vacuum_fraction=args.vacuum_fraction,
        vacuum_start=args.vacuum_start,
        vacuum_end=args.vacuum_end,
        profile_csv=profile_csv,
        report_md=report_md,
    )
    vesta = cube_preset.run_preset(
        "esp",
        args.density_cube,
        vesta_dir,
        texture_cube=shifted_cube,
        stem=args.stem,
        isosurface=args.isosurface,
        tex_physical=args.tex_physical,
        tex_range_source=args.tex_range_source,
        surface_band=args.surface_band,
        surface_nearest=args.surface_nearest,
        structure=args.structure,
        boundary=args.boundary,
        copy_cubes=not args.no_copy_cubes,
    )

    print(f"shifted_cube: {alignment.output_cube}")
    print(f"profile_csv: {profile_csv}")
    print(f"alignment_report: {report_md}")
    print(f"vesta: {vesta.vesta_path}")
    if vesta.manifest_path is not None:
        print(f"vesta_recipe: {vesta.manifest_path}")
    return 0


def run_tool(name: str, args: Sequence[str]) -> int:
    canonical = TOOL_ALIASES.get(name, name)
    if canonical not in TOOL_BY_NAME:
        raise SystemExit(f"Unknown stable tool: {name}")
    tool = TOOL_BY_NAME[canonical]
    tool_args = _strip_separator(args)
    if tool.command == "esp-surface":
        return run_esp_surface(tool_args)
    return _dispatch_low_level(tool.command, tool_args)


def interactive(lang: Lang = "en") -> int:
    lang = normalize_lang(lang)
    list_tools(lang=lang, as_json=False)
    raw = input(_text("\nTool name or number", "\n工具名或编号", lang) + ": ").strip()
    if not raw:
        return 0
    if raw.isdigit():
        index = int(raw)
        if index < 1 or index > len(STABLE_TOOLS):
            print(_text("Invalid number.", "编号无效。", lang), file=sys.stderr)
            return 2
        name = STABLE_TOOLS[index - 1].name
    else:
        name = raw
    args_line = input(_text("Arguments for this tool", "该工具的参数", lang) + ": ").strip()
    return run_tool(name, shlex.split(args_line))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="List and run stable human-facing multiwfn2vesta tools.")
    parser.add_argument("--lang", choices=("en", "zh"), default="en", help="display language")
    parser.add_argument("--json", action="store_true", help="print tool list as JSON")
    subparsers = parser.add_subparsers(dest="action")

    list_parser = subparsers.add_parser("list", help="list stable tools")
    list_parser.add_argument("--lang", choices=("en", "zh"), default=None, dest="sub_lang")
    list_parser.add_argument("--json", action="store_true")

    run_parser = subparsers.add_parser("run", help="run a stable tool")
    run_parser.add_argument("tool")
    run_parser.add_argument("tool_args", nargs=argparse.REMAINDER)

    interactive_parser = subparsers.add_parser("interactive", help="interactive stable tool chooser")
    interactive_parser.add_argument("--lang", choices=("en", "zh"), default=None, dest="sub_lang")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.action == "run":
        return run_tool(args.tool, args.tool_args)
    if args.action == "interactive":
        return interactive(args.sub_lang or args.lang)
    if args.action == "list":
        list_tools(lang=args.sub_lang or args.lang, as_json=args.json)
        return 0
    list_tools(lang=args.lang, as_json=args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
