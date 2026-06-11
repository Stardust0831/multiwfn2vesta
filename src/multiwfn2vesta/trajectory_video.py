"""Prepare or run high-bitrate videos from rendered trajectory PNG frames."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import List, NamedTuple, Optional, Sequence, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_FRAME_GLOB = "frame_*.png"
DEFAULT_FPS = 24.0
DEFAULT_BITRATE = "20M"
DEFAULT_CODEC = "libx264"
DEFAULT_PIX_FMT = "yuv420p"
DEFAULT_FRAME_ROLE = "nvt_first_png_frame"
DEFAULT_VIDEO_ROLE = "nvt_high_bitrate_video"


class TrajectoryVideoResult(NamedTuple):
    frames_dir: Path
    output: Path
    recipe_path: Path
    concat_file: Path
    frames: Tuple[Path, ...]
    command: Tuple[str, ...]
    returncode: Optional[int]
    success: bool
    ran_ffmpeg: bool


def _natural_key(path: Path) -> List[object]:
    parts = re.split(r"(\d+)", path.name)
    key: List[object] = []
    for part in parts:
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(part)
    return key


def collect_frames(frames_dir: Path, frame_glob: str = DEFAULT_FRAME_GLOB) -> Tuple[Path, ...]:
    frames_dir = Path(frames_dir).expanduser().resolve()
    if not frames_dir.is_dir():
        raise FileNotFoundError("Frame directory not found: {}".format(frames_dir))
    frames = tuple(sorted(frames_dir.glob(frame_glob), key=_natural_key))
    if not frames:
        raise FileNotFoundError("No frames matched {} in {}".format(frame_glob, frames_dir))
    return frames


def _concat_quote(path: Path) -> str:
    text = str(path.resolve())
    return "'" + text.replace("'", "'\\''") + "'"


def write_concat_file(frames: Sequence[Path], concat_file: Path) -> None:
    concat_file = Path(concat_file)
    concat_file.parent.mkdir(parents=True, exist_ok=True)
    lines = ["file {}".format(_concat_quote(frame)) for frame in frames]
    concat_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_ffmpeg_command(
    concat_file: Path,
    output: Path,
    *,
    ffmpeg: str = "ffmpeg",
    fps: float = DEFAULT_FPS,
    bitrate: Optional[str] = DEFAULT_BITRATE,
    crf: Optional[int] = None,
    codec: str = DEFAULT_CODEC,
    pix_fmt: str = DEFAULT_PIX_FMT,
    overwrite: bool = False,
    extra_args: Optional[Sequence[str]] = None,
) -> Tuple[str, ...]:
    if fps <= 0:
        raise ValueError("--fps must be positive")
    command: List[str] = [
        ffmpeg,
        "-y" if overwrite else "-n",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-r",
        _format_number(fps),
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(Path(concat_file)),
        "-an",
        "-c:v",
        codec,
    ]
    if crf is not None:
        command.extend(["-crf", str(int(crf))])
    elif bitrate:
        command.extend(["-b:v", str(bitrate)])
    if pix_fmt:
        command.extend(["-pix_fmt", pix_fmt])
    command.extend(extra_args or [])
    command.append(str(Path(output)))
    return tuple(command)


def _format_number(value: float) -> str:
    if float(value).is_integer():
        return str(int(value))
    return str(float(value))


def shell_command(command: Sequence[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in command)


def _project_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return (PROJECT_ROOT / path).resolve()


def _manifest_entries(manifest: dict, key: str) -> List[dict]:
    value = manifest.get(key, [])
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _manifest_path_for_role(manifest: dict, role: str) -> Optional[Path]:
    for group in ("workspace_smoke_evidence", "project_assets"):
        for item in _manifest_entries(manifest, group):
            if item.get("role") == role and item.get("path"):
                return _project_path(str(item["path"]))
    return None


def resolve_manifest_frames_dir(manifest_path: Path, frame_role: str = DEFAULT_FRAME_ROLE) -> Tuple[Path, dict]:
    manifest_path = Path(manifest_path).expanduser().resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    frame_path = _manifest_path_for_role(manifest, frame_role)
    if frame_path is None:
        raise ValueError("Manifest does not contain role {!r}".format(frame_role))
    if frame_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}:
        return frame_path.parent, manifest
    return frame_path, manifest


def _default_output(frames_dir: Path, manifest: Optional[dict], video_role: str) -> Path:
    if manifest is not None:
        video_path = _manifest_path_for_role(manifest, video_role)
        if video_path is not None:
            return video_path.with_name(video_path.stem + "_rebuilt" + video_path.suffix)
    parent = frames_dir.parent if frames_dir.name.lower() == "png" else frames_dir
    return parent / (parent.name + "_trajectory.mp4")


def render_recipe(
    result: TrajectoryVideoResult,
    *,
    frame_glob: str,
    fps: float,
    bitrate: Optional[str],
    crf: Optional[int],
    codec: str,
    pix_fmt: str,
    manifest_path: Optional[Path],
    frame_role: str,
    video_role: str,
) -> str:
    lines = [
        "# trajectory-video recipe",
        "",
        "- frames_dir: `{}`".format(result.frames_dir),
        "- frame_glob: `{}`".format(frame_glob),
        "- frame_count: `{}`".format(len(result.frames)),
        "- first_frame: `{}`".format(result.frames[0]),
        "- last_frame: `{}`".format(result.frames[-1]),
        "- output: `{}`".format(result.output),
        "- concat_file: `{}`".format(result.concat_file),
        "- fps: `{}`".format(_format_number(fps)),
        "- bitrate: `{}`".format(bitrate if bitrate is not None else ""),
        "- crf: `{}`".format(crf if crf is not None else ""),
        "- codec: `{}`".format(codec),
        "- pix_fmt: `{}`".format(pix_fmt),
        "- ran_ffmpeg: `{}`".format(result.ran_ffmpeg),
        "- returncode: `{}`".format(result.returncode),
        "- success: `{}`".format(result.success),
    ]
    if manifest_path is not None:
        lines.extend(
            [
                "- manifest: `{}`".format(manifest_path),
                "- manifest_frame_role: `{}`".format(frame_role),
                "- manifest_video_role: `{}`".format(video_role),
            ]
        )
    lines.extend(
        [
            "",
            "## ffmpeg command",
            "",
            "```bash",
            shell_command(result.command),
            "```",
            "",
            "## Notes",
            "",
            "- This command consumes already rendered PNG frames; it does not start VESTA.",
            "- Use `--run` only when ffmpeg should be executed immediately.",
            "- Large MP4 files should stay in the workspace smoke area unless explicitly promoted.",
        ]
    )
    return "\n".join(lines) + "\n"


def prepare_video(
    frames_dir: Optional[Path],
    output: Optional[Path],
    *,
    manifest_path: Optional[Path] = None,
    frame_role: str = DEFAULT_FRAME_ROLE,
    video_role: str = DEFAULT_VIDEO_ROLE,
    frame_glob: str = DEFAULT_FRAME_GLOB,
    fps: float = DEFAULT_FPS,
    bitrate: Optional[str] = DEFAULT_BITRATE,
    crf: Optional[int] = None,
    codec: str = DEFAULT_CODEC,
    pix_fmt: str = DEFAULT_PIX_FMT,
    ffmpeg: str = "ffmpeg",
    run: bool = False,
    overwrite: bool = False,
    recipe_path: Optional[Path] = None,
    concat_file: Optional[Path] = None,
    extra_ffmpeg_args: Optional[Sequence[str]] = None,
) -> TrajectoryVideoResult:
    manifest: Optional[dict] = None
    if manifest_path is not None:
        manifest_frames_dir, manifest = resolve_manifest_frames_dir(manifest_path, frame_role)
        if frames_dir is None:
            frames_dir = manifest_frames_dir
    if frames_dir is None:
        raise ValueError("frames_dir is required unless --manifest supplies a frame role")

    frames_dir = Path(frames_dir).expanduser().resolve()
    frames = collect_frames(frames_dir, frame_glob)
    output_path = Path(output).expanduser().resolve() if output is not None else _default_output(frames_dir, manifest, video_role)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if run and output_path.exists() and not overwrite:
        raise FileExistsError("Output exists; pass --overwrite to replace it: {}".format(output_path))

    concat_path = Path(concat_file).expanduser().resolve() if concat_file else output_path.with_name(output_path.stem + "_frames.txt")
    write_concat_file(frames, concat_path)
    command = build_ffmpeg_command(
        concat_path,
        output_path,
        ffmpeg=ffmpeg,
        fps=fps,
        bitrate=bitrate,
        crf=crf,
        codec=codec,
        pix_fmt=pix_fmt,
        overwrite=overwrite,
        extra_args=extra_ffmpeg_args,
    )

    returncode: Optional[int] = None
    success = True
    if run:
        completed = subprocess.run(command, check=False)
        returncode = completed.returncode
        success = returncode == 0 and output_path.exists()

    recipe = Path(recipe_path).expanduser().resolve() if recipe_path else output_path.with_name(output_path.stem + "_trajectory_video_recipe.md")
    recipe.parent.mkdir(parents=True, exist_ok=True)
    result = TrajectoryVideoResult(
        frames_dir=frames_dir,
        output=output_path,
        recipe_path=recipe,
        concat_file=concat_path,
        frames=tuple(frames),
        command=command,
        returncode=returncode,
        success=success,
        ran_ffmpeg=run,
    )
    recipe.write_text(
        render_recipe(
            result,
            frame_glob=frame_glob,
            fps=fps,
            bitrate=bitrate,
            crf=crf,
            codec=codec,
            pix_fmt=pix_fmt,
            manifest_path=manifest_path,
            frame_role=frame_role,
            video_role=video_role,
        ),
        encoding="utf-8",
    )
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create or prepare a high-bitrate MP4 from rendered VESTA trajectory PNG frames.",
    )
    parser.add_argument("frames_dir", nargs="?", type=Path, help="Directory containing rendered PNG frames")
    parser.add_argument("output", nargs="?", type=Path, help="Output MP4 path")
    parser.add_argument("--frames-dir", dest="frames_dir_option", type=Path, help="Explicit PNG frame directory")
    parser.add_argument("--output", dest="output_option", type=Path, help="Explicit output MP4 path")
    parser.add_argument("--manifest", type=Path, help="Example artifact manifest JSON; can supply the frame directory")
    parser.add_argument("--manifest-frame-role", default=DEFAULT_FRAME_ROLE, help="Manifest role used to find PNG frames")
    parser.add_argument("--manifest-video-role", default=DEFAULT_VIDEO_ROLE, help="Manifest role used for default output naming")
    parser.add_argument("--frame-glob", default=DEFAULT_FRAME_GLOB, help="Glob pattern inside frames_dir")
    parser.add_argument("--fps", type=float, default=DEFAULT_FPS)
    parser.add_argument("--bitrate", default=DEFAULT_BITRATE, help="Target video bitrate, ignored when --crf is set")
    parser.add_argument("--crf", type=int, help="Use CRF quality mode instead of fixed bitrate")
    parser.add_argument("--codec", default=DEFAULT_CODEC)
    parser.add_argument("--pix-fmt", default=DEFAULT_PIX_FMT)
    parser.add_argument("--ffmpeg", default="ffmpeg", help="ffmpeg executable")
    parser.add_argument("--run", action="store_true", help="Execute ffmpeg. Default only writes frame list and recipe.")
    parser.add_argument("--overwrite", action="store_true", help="Allow ffmpeg to overwrite output")
    parser.add_argument("--recipe", type=Path, help="Markdown recipe path")
    parser.add_argument("--concat-file", type=Path, help="ffmpeg concat input list path")
    parser.add_argument(
        "--extra-ffmpeg-arg",
        action="append",
        default=[],
        help="Additional single ffmpeg argument appended before the output path; repeat as needed.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = prepare_video(
            args.frames_dir_option or args.frames_dir,
            args.output_option or args.output,
            manifest_path=args.manifest,
            frame_role=args.manifest_frame_role,
            video_role=args.manifest_video_role,
            frame_glob=args.frame_glob,
            fps=args.fps,
            bitrate=args.bitrate,
            crf=args.crf,
            codec=args.codec,
            pix_fmt=args.pix_fmt,
            ffmpeg=args.ffmpeg,
            run=args.run,
            overwrite=args.overwrite,
            recipe_path=args.recipe,
            concat_file=args.concat_file,
            extra_ffmpeg_args=args.extra_ffmpeg_arg,
        )
    except Exception as exc:  # pragma: no cover - exercised via CLI smoke behavior
        print(str(exc), file=sys.stderr)
        return 2

    print(result.output)
    print(result.recipe_path)
    print(shell_command(result.command))
    if not result.ran_ffmpeg:
        print("Dry-run only; pass --run to execute ffmpeg.")
    if result.ran_ffmpeg and not result.success:
        return result.returncode or 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
