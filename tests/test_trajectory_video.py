import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from multiwfn2vesta import trajectory_video


class TestTrajectoryVideo(unittest.TestCase):
    def _write_frames(self, frames_dir: Path) -> None:
        frames_dir.mkdir(parents=True, exist_ok=True)
        for name in ("frame_0010.png", "frame_0002.png", "frame_0001.png"):
            (frames_dir / name).write_text(name, encoding="utf-8")

    def test_collect_frames_uses_natural_sort(self):
        with tempfile.TemporaryDirectory() as tmp:
            frames_dir = Path(tmp) / "png"
            self._write_frames(frames_dir)

            frames = trajectory_video.collect_frames(frames_dir)

        self.assertEqual([frame.name for frame in frames], ["frame_0001.png", "frame_0002.png", "frame_0010.png"])

    def test_prepare_video_writes_concat_list_recipe_and_dry_run_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            frames_dir = Path(tmp) / "png"
            self._write_frames(frames_dir)
            output = Path(tmp) / "movie.mp4"

            result = trajectory_video.prepare_video(frames_dir, output, fps=30, bitrate="40M")

            self.assertFalse(output.exists())
            self.assertFalse(result.ran_ffmpeg)
            self.assertTrue(result.success)
            self.assertEqual(result.frames[0].name, "frame_0001.png")
            self.assertEqual(result.frames[-1].name, "frame_0010.png")
            concat_text = result.concat_file.read_text(encoding="utf-8")
            self.assertIn("frame_0001.png", concat_text)
            self.assertIn("frame_0010.png", concat_text)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("frame_count: `3`", recipe)
            self.assertIn("-b:v 40M", recipe)
            self.assertIn("ffmpeg", result.command[0])

    def test_manifest_can_supply_frame_directory_and_default_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            manifest_path = project_root / "examples" / "cdcl" / "artifact_manifest.json"
            frames_dir = Path(tmp) / "smoke" / "traj" / "png"
            self._write_frames(frames_dir)
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(
                json.dumps(
                    {
                        "workspace_smoke_evidence": [
                            {"role": "nvt_first_png_frame", "path": "../smoke/traj/png/frame_0001.png"},
                            {"role": "nvt_high_bitrate_video", "path": "../smoke/traj/traj_hq20m.mp4"},
                        ]
                    }
                ),
                encoding="utf-8",
            )

            with patch("multiwfn2vesta.trajectory_video.PROJECT_ROOT", project_root):
                result = trajectory_video.prepare_video(None, None, manifest_path=manifest_path)

            self.assertEqual(result.frames_dir, frames_dir.resolve())
            self.assertEqual(result.output.name, "traj_hq20m_rebuilt.mp4")
            self.assertTrue(result.recipe_path.exists())

    def test_run_refuses_existing_output_without_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            frames_dir = Path(tmp) / "png"
            self._write_frames(frames_dir)
            output = Path(tmp) / "movie.mp4"
            output.write_text("old", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                trajectory_video.prepare_video(frames_dir, output, run=True)

    def test_cli_dry_run_prints_recipe_and_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            frames_dir = Path(tmp) / "png"
            self._write_frames(frames_dir)
            output = Path(tmp) / "movie.mp4"
            stdout = io.StringIO()

            with patch("sys.stdout", stdout):
                code = trajectory_video.main([str(frames_dir), str(output), "--fps", "12"])

            self.assertEqual(code, 0)
            text = stdout.getvalue()
            self.assertIn(str(output.resolve()), text)
            self.assertIn("Dry-run only", text)
            self.assertIn("-r 12", text)

    def test_cli_manifest_accepts_explicit_output_option(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            manifest_path = project_root / "examples" / "cdcl" / "artifact_manifest.json"
            frames_dir = Path(tmp) / "smoke" / "traj" / "png"
            self._write_frames(frames_dir)
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(
                json.dumps(
                    {
                        "workspace_smoke_evidence": [
                            {"role": "nvt_first_png_frame", "path": "../smoke/traj/png/frame_0001.png"}
                        ]
                    }
                ),
                encoding="utf-8",
            )
            output = Path(tmp) / "out" / "movie.mp4"
            stdout = io.StringIO()

            with patch("multiwfn2vesta.trajectory_video.PROJECT_ROOT", project_root), patch("sys.stdout", stdout):
                code = trajectory_video.main(["--manifest", str(manifest_path), "--output", str(output)])

            self.assertEqual(code, 0)
            self.assertIn(str(output.resolve()), stdout.getvalue())
            self.assertTrue(output.with_name("movie_trajectory_video_recipe.md").exists())

    def test_cli_reports_missing_frames(self):
        with tempfile.TemporaryDirectory() as tmp:
            stderr = io.StringIO()
            with patch("sys.stderr", stderr):
                code = trajectory_video.main([str(Path(tmp) / "missing"), str(Path(tmp) / "movie.mp4")])

            self.assertEqual(code, 2)
            self.assertIn("Frame directory not found", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
