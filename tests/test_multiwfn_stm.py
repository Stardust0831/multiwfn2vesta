import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.executables import ExecutableCandidate
from multiwfn2vesta.multiwfn_stm import (
    STM_OUTPUT_MISSING_CODE,
    build_stm_commands,
    run_multiwfn_stm,
)


STM_CUBE = """STM comment one
STM comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.0000 0.0005 0.0010 0.0020 0.0040 0.0080 0.0120 0.0150
"""


class TestMultiwfnStmRunner(unittest.TestCase):
    def make_candidate(self, root):
        fake_exe = Path(root) / "Multiwfn_noGUI"
        fake_exe.write_text("#!/bin/sh\n", encoding="utf-8")
        fake_exe.chmod(0o755)
        return ExecutableCandidate("Multiwfn_noGUI", fake_exe, "test", True, True)

    def test_build_default_constant_current_command_stream(self):
        commands = build_stm_commands(grid_points=(10, 10, 6))

        self.assertEqual(commands, ["300", "4", "1", "4", "10,10,6", "0", "2", "0", "-1", "0", "q"])

    def test_build_command_stream_with_bias_fermi_ranges_and_prepare_fermi(self):
        commands = build_stm_commands(
            bias=-1.0,
            fermi=-4.8,
            grid_points=(12, 13, 14),
            x_range=(-6.0, 6.0),
            y_range=(-5.0, 5.0),
            z_range=(2.0, 8.0),
            prepare_fermi_temperature=298.15,
        )

        self.assertEqual(
            commands,
            [
                "300",
                "9",
                "298.15",
                "q",
                "4",
                "1",
                "2",
                "-1.0",
                "3",
                "-4.8",
                "4",
                "12,13,14",
                "5",
                "-6.0,6.0",
                "6",
                "-5.0,5.0",
                "7",
                "2.0,8.0",
                "0",
                "2",
                "0",
                "-1",
                "0",
                "q",
            ],
        )

    def test_run_multiwfn_stm_writes_cube_vesta_and_recipe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "STM.cub").write_text(STM_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="warn")

            with patch("multiwfn2vesta.multiwfn_stm.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_stm.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_stm(
                        wavefunction,
                        root / "products",
                        nthreads=2,
                        timeout=30,
                        stem="case",
                        grid_points=(10, 10, 6),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.cli_returncode, 0)
            self.assertEqual(mocked_run.call_args.args[0], [str(candidate.path), str(wavefunction.resolve()), "-nt", "2"])
            self.assertEqual(mocked_run.call_args.kwargs["cwd"], str(root / "products" / "multiwfn_stm_raw"))
            self.assertEqual(mocked_run.call_args.kwargs["timeout"], 30)
            self.assertEqual(mocked_run.call_args.kwargs["env"]["Multiwfnpath"], str(candidate.path.parent))
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "300\n4\n1\n4\n10,10,6\n0\n2\n0\n-1\n0\nq\n")
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "ok")
            self.assertEqual(result.stderr_log.read_text(encoding="utf-8"), "warn")
            self.assertTrue(result.raw_stm_cube.exists())
            self.assertTrue(result.stm_cube.exists())
            self.assertEqual(result.stm_cube.name, "case_stm.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(result.vesta_result.vesta_path.name, "case_stm_cube.vesta")
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `stm`", manifest)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("mode: `constant-current STM cube`", recipe)
            self.assertIn("grid_points: `10,10,6`", recipe)

    def test_run_multiwfn_stm_can_skip_vesta_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                Path(kwargs["cwd"], "STM.cub").write_text(STM_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            with patch("multiwfn2vesta.multiwfn_stm.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_stm.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_stm(wavefunction, root / "products", make_vesta=False)

            self.assertTrue(result.success)
            self.assertTrue(result.stm_cube.exists())
            self.assertIsNone(result.vesta_result)

    def test_run_multiwfn_stm_reports_missing_cube(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_stm.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_stm.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(candidate.path)], 0, stdout="ok", stderr=""),
                ):
                    result = run_multiwfn_stm(wavefunction, root / "products")

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, STM_OUTPUT_MISSING_CODE)
            self.assertIn("expected STM cube output", result.error or "")
            self.assertIsNone(result.stm_cube)
            self.assertIsNone(result.vesta_result)

    def test_main_reports_missing_wavefunction_without_traceback(self):
        stderr = io.StringIO()
        candidate = self.make_candidate(Path(tempfile.mkdtemp()))
        with tempfile.TemporaryDirectory() as tmp:
            with patch("multiwfn2vesta.multiwfn_stm.find_multiwfn", return_value=candidate):
                with patch("sys.stderr", stderr):
                    code = __import__("multiwfn2vesta.multiwfn_stm", fromlist=["main"]).main(
                        [str(Path(tmp) / "missing.fch"), str(Path(tmp) / "products")]
                    )

        self.assertEqual(code, 2)
        self.assertIn("stm-run:", stderr.getvalue())
        self.assertIn("Wavefunction file not found", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
