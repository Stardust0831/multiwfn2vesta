import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.executables import ExecutableCandidate
from multiwfn2vesta.multiwfn_aigm import (
    AIGM_OUTPUT_MISSING_CODE,
    build_aigm_commands,
    run_multiwfn_aigm,
    trajectory_looks_periodic,
)


SURFACE_CUBE = """surface one
surface two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
  0.0 0.002 0.006 0.010 0.012 0.020 0.030 0.040
"""


TEXTURE_CUBE = """texture one
texture two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -0.10 -0.05 -0.02 0.00 0.03 0.04 0.08 0.10
"""


class TestMultiwfnAigmRunner(unittest.TestCase):
    def make_candidate(self, root):
        fake_exe = Path(root) / "Multiwfn_noGUI"
        fake_exe.write_text("#!/bin/sh\n", encoding="utf-8")
        fake_exe.chmod(0o755)
        return ExecutableCandidate("Multiwfn_noGUI", fake_exe, "test", True, True)

    def test_build_aigm_command_stream_for_points_grid_and_frame_range(self):
        commands = build_aigm_commands(
            ["1-48", "49-60"],
            frame_range=(5, 25),
            grid_points=(12, 13, 14),
        )

        self.assertEqual(
            commands,
            ["20", "12", "2", "1-48", "49-60", "5,25", "4", "12,13,14", "3", "0", "0", "q"],
        )

    def test_build_amigm_command_stream_can_export_optional_products(self):
        commands = build_aigm_commands(
            ["1-48", "c"],
            method="amigm",
            grid_mode="spacing",
            grid_spacing=0.25,
            export_rdg=True,
            export_tfi=True,
            export_scatter=True,
        )

        self.assertEqual(
            commands,
            ["20", "-12", "2", "1-48", "c", "", "4", "0.25", "2", "3", "4", "5", "0", "0", "q"],
        )

    def test_build_aigm_rejects_single_fragment(self):
        with self.assertRaisesRegex(ValueError, "at least two"):
            build_aigm_commands(["1-3"])

    def test_build_aigm_rejects_invalid_frame_range(self):
        with self.assertRaisesRegex(ValueError, "END"):
            build_aigm_commands(["1", "2"], frame_range=(5, 4))

    def test_build_aigm_rejects_points_grid_for_periodic_trajectory(self):
        with self.assertRaisesRegex(ValueError, "periodic trajectories"):
            build_aigm_commands(["1", "2"], periodic=True, grid_mode="points")

    def test_build_aigm_allows_spacing_grid_for_periodic_trajectory(self):
        commands = build_aigm_commands(["1", "2"], periodic=True, grid_mode="spacing", grid_spacing=0.3)

        self.assertEqual(commands, ["20", "12", "2", "1", "2", "", "4", "0.3", "3", "0", "0", "q"])

    def test_detects_extended_xyz_lattice_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            trajectory = Path(tmp) / "traj.xyz"
            trajectory.write_text(
                '2\nLattice="10 0 0 0 10 0 0 0 10" Properties=species:S:1:pos:R:3 pbc="T T T"\n'
                "H 0 0 0\nH 0 0 1\n",
                encoding="utf-8",
            )

            self.assertTrue(trajectory_looks_periodic(trajectory))

    def test_run_multiwfn_aigm_rejects_detected_periodic_points_grid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trajectory = root / "traj.xyz"
            trajectory.write_text(
                '2\nLattice="10 0 0 0 10 0 0 0 10" Properties=species:S:1:pos:R:3\n'
                "H 0 0 0\nH 0 0 1\n",
                encoding="utf-8",
            )
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_aigm.find_multiwfn", return_value=candidate):
                with self.assertRaisesRegex(ValueError, "periodic trajectories"):
                    run_multiwfn_aigm(trajectory, root / "products", fragments=["1", "2"])

    def test_run_multiwfn_aigm_writes_cubes_recipe_and_vesta(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trajectory = root / "traj.xyz"
            trajectory.write_text("2\nframe\nH 0 0 0\nH 0 0 1\n", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "avgdg_inter.cub").write_text(SURFACE_CUBE, encoding="utf-8")
                (cwd / "avgsl2r.cub").write_text(TEXTURE_CUBE, encoding="utf-8")
                (cwd / "avgRDG.cub").write_text(SURFACE_CUBE, encoding="utf-8")
                (cwd / "thermflu.cub").write_text(TEXTURE_CUBE, encoding="utf-8")
                (cwd / "output.txt").write_text("scatter\n", encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="warn")

            with patch("multiwfn2vesta.multiwfn_aigm.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_aigm.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_aigm(
                        trajectory,
                        root / "products",
                        fragments=["1", "2"],
                        frame_range=(1, 2),
                        nthreads=2,
                        timeout=30,
                        stem="case",
                        method="amigm",
                        grid_mode="spacing",
                        grid_spacing=0.6,
                        export_rdg=True,
                        export_tfi=True,
                        export_scatter=True,
                        make_tfi_vesta=True,
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.cli_returncode, 0)
            self.assertEqual(mocked_run.call_args.args[0], [str(candidate.path), str(trajectory.resolve()), "-nt", "2"])
            self.assertEqual(mocked_run.call_args.kwargs["cwd"], str(root / "products" / "multiwfn_amigm_raw"))
            self.assertEqual(mocked_run.call_args.kwargs["timeout"], 30)
            self.assertEqual(mocked_run.call_args.kwargs["env"]["Multiwfnpath"], str(candidate.path.parent))
            self.assertEqual(
                result.command_file.read_text(encoding="utf-8"),
                "20\n-12\n2\n1\n2\n1,2\n4\n0.6\n2\n3\n4\n5\n0\n0\nq\n",
            )
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "ok")
            self.assertEqual(result.stderr_log.read_text(encoding="utf-8"), "warn")
            self.assertTrue(result.raw_avgdg_inter_cube.exists())
            self.assertTrue(result.raw_avgsl2r_cube.exists())
            self.assertEqual(result.avgdg_inter_cube.name, "case_avgdg_inter.cub")
            self.assertEqual(result.avgsl2r_cube.name, "case_avgsl2r.cub")
            self.assertEqual(result.avgRDG_cube.name, "case_avgRDG.cub")
            self.assertEqual(result.thermflu_cube.name, "case_thermflu.cub")
            self.assertEqual(result.output_txt.name, "case_multiwfn_amigm_output.txt")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(result.vesta_result.vesta_path.name, "case_amigm_cube.vesta")
            self.assertIsNotNone(result.tfi_vesta_result)
            self.assertEqual(result.tfi_vesta_result.vesta_path.name, "case_amigm_tfi_cube.vesta")
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `aigm`", manifest)
            self.assertIn("title: `case_avgdg_inter (amigm)`", manifest)
            tfi_manifest = result.tfi_vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `aigm-tfi`", tfi_manifest)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("method: `amigm`", recipe)
            self.assertIn("fragments: `1; 2`", recipe)
            self.assertIn("frame_range: `1 to 2`", recipe)
            self.assertIn("periodic: `False`", recipe)

    def test_run_multiwfn_aigm_reports_missing_required_cubes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trajectory = root / "traj.xyz"
            trajectory.write_text("2\nframe\nH 0 0 0\nH 0 0 1\n", encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_aigm.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_aigm.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(candidate.path)], 0, stdout="ok", stderr=""),
                ):
                    result = run_multiwfn_aigm(trajectory, root / "products", fragments=["1", "2"])

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, AIGM_OUTPUT_MISSING_CODE)
            self.assertIn("required aigm cube output is missing", result.error or "")
            self.assertIsNone(result.avgdg_inter_cube)
            self.assertIsNone(result.avgsl2r_cube)
            self.assertIsNone(result.vesta_result)

    def test_run_multiwfn_aigm_rejects_tfi_vesta_without_tfi_cube(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trajectory = root / "traj.xyz"
            trajectory.write_text("2\nframe\nH 0 0 0\nH 0 0 1\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "requires --export-tfi"):
                run_multiwfn_aigm(
                    trajectory,
                    root / "products",
                    fragments=["1", "2"],
                    make_tfi_vesta=True,
                )

    def test_main_reports_fragment_errors_without_traceback(self):
        stderr = io.StringIO()
        candidate = self.make_candidate(Path(tempfile.mkdtemp()))
        with tempfile.TemporaryDirectory() as tmp:
            trajectory = Path(tmp) / "traj.xyz"
            trajectory.write_text("2\nframe\nH 0 0 0\nH 0 0 1\n", encoding="utf-8")
            with patch("multiwfn2vesta.multiwfn_aigm.find_multiwfn", return_value=candidate):
                with patch("sys.stderr", stderr):
                    code = __import__("multiwfn2vesta.multiwfn_aigm", fromlist=["main"]).main(
                        [str(trajectory), str(Path(tmp) / "products"), "--fragment", "1"]
                    )

        self.assertEqual(code, 2)
        self.assertIn("aigm-run:", stderr.getvalue())
        self.assertIn("at least two", stderr.getvalue())

    def test_main_amigm_rejects_method_override(self):
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = __import__("multiwfn2vesta.multiwfn_aigm", fromlist=["main_amigm"]).main_amigm(
                ["traj.xyz", "products", "--method", "aigm"]
            )

        self.assertEqual(code, 2)
        self.assertIn("amigm-run:", stderr.getvalue())
        self.assertIn("--method is fixed", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
