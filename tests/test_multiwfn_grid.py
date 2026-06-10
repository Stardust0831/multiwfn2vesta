import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.executables import ExecutableCandidate
from multiwfn2vesta.multiwfn_grid import (
    GRID_OUTPUT_MISSING_CODE,
    GRID_PROCESSING_FAILED_CODE,
    available_functions_text,
    build_grid_commands,
    resolve_grid_function,
    run_multiwfn_grid,
)


DENSITY_CUBE = """density comment one
density comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.00 0.02 0.04 0.06 0.08 0.10 0.12 0.14
"""


class TestMultiwfnGridRunner(unittest.TestCase):
    def make_candidate(self, root):
        fake_exe = Path(root) / "Multiwfn_noGUI"
        fake_exe.write_text("#!/bin/sh\n", encoding="utf-8")
        fake_exe.chmod(0o755)
        return ExecutableCandidate("Multiwfn_noGUI", fake_exe, "test", True, True)

    def test_available_functions_and_alias_resolution(self):
        text = available_functions_text()
        self.assertIn("density", text)
        self.assertIn("orbital", text)
        self.assertIn("requires --orbital", text)
        self.assertEqual(resolve_grid_function("rho").name, "density")
        self.assertEqual(resolve_grid_function("12").name, "esp")
        self.assertEqual(resolve_grid_function(None, 9).name, "elf")
        custom = resolve_grid_function(None, 99)
        self.assertEqual(custom.index, 99)
        self.assertEqual(custom.output_filename, "griddata.cub")

    def test_build_density_points_command_stream(self):
        function = resolve_grid_function("density")
        commands = build_grid_commands(function, grid_points=(12, 13, 14))
        self.assertEqual(commands, ["5", "1", "4", "12,13,14", "2", "0", "q"])

    def test_build_orbital_command_requires_orbital_selector(self):
        function = resolve_grid_function("orbital")
        with self.assertRaises(ValueError):
            build_grid_commands(function)
        self.assertEqual(
            build_grid_commands(function, orbital="h", grid_mode="low"),
            ["5", "4", "h", "1", "2", "0", "q"],
        )

    def test_build_reference_cube_grid_command_stream(self):
        function = resolve_grid_function("elf")
        with tempfile.TemporaryDirectory() as tmp:
            ref = Path(tmp) / "ref.cub"
            ref.write_text(DENSITY_CUBE, encoding="utf-8")
            commands = build_grid_commands(function, grid_mode="cube", grid_cube=ref)

        self.assertEqual(commands[:3], ["5", "9", "8"])
        self.assertTrue(commands[3].endswith("ref.cub"))
        self.assertEqual(commands[-3:], ["2", "0", "q"])

    def test_run_multiwfn_grid_writes_cube_vesta_and_recipe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "density.cub").write_text(DENSITY_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="warn")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        nthreads=2,
                        timeout=30,
                        stem="case",
                        grid_points=(12, 12, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.cli_returncode, 0)
            self.assertEqual(mocked_run.call_args.args[0], [str(candidate.path), str(wavefunction.resolve()), "-nt", "2"])
            self.assertEqual(mocked_run.call_args.kwargs["timeout"], 30)
            self.assertEqual(mocked_run.call_args.kwargs["env"]["Multiwfnpath"], str(candidate.path.parent))
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n1\n4\n12,12,12\n2\n0\nq\n")
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "ok")
            self.assertEqual(result.stderr_log.read_text(encoding="utf-8"), "warn")
            self.assertTrue(result.raw_cube.exists())
            self.assertTrue(result.cube.exists())
            self.assertEqual(result.cube.name, "case_density.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertTrue(result.vesta_result.vesta_path.exists())
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_index: `1`", recipe)
            self.assertIn("auto_vesta_preset: `density`", recipe)

    def test_run_multiwfn_grid_can_skip_vesta_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                Path(kwargs["cwd"], "density.cub").write_text(DENSITY_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(wavefunction, root / "products", make_vesta=False)

            self.assertTrue(result.success)
            self.assertTrue(result.cube.exists())
            self.assertIsNone(result.vesta_result)

    def test_run_multiwfn_grid_expected_cube_keeps_relative_subdirectory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                nested = Path(kwargs["cwd"]) / "nested"
                nested.mkdir()
                (nested / "custom.cub").write_text(DENSITY_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        commands=["5", "1", "0", "q"],
                        expected_cube=Path("nested/custom.cub"),
                        make_vesta=False,
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.raw_cube, root / "products" / "multiwfn_grid_raw" / "nested" / "custom.cub")
            self.assertTrue(result.cube.exists())

    def test_run_multiwfn_grid_reports_missing_cube(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_grid.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(candidate.path)], 0, stdout="ok", stderr=""),
                ):
                    result = run_multiwfn_grid(wavefunction, root / "products")

        self.assertFalse(result.success)
        self.assertEqual(result.cli_returncode, GRID_OUTPUT_MISSING_CODE)
        self.assertIn("expected grid cube output", result.error or "")
        self.assertIsNone(result.cube)
        self.assertIsNone(result.vesta_result)

    def test_run_multiwfn_grid_records_nonzero_multiwfn_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_grid.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(candidate.path)], 7, stdout="bad", stderr="failed"),
                ):
                    result = run_multiwfn_grid(wavefunction, root / "products")

            self.assertFalse(result.success)
            self.assertEqual(result.returncode, 7)
            self.assertEqual(result.cli_returncode, 7)
            self.assertIn("return code 7", result.error or "")
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "bad")
            self.assertEqual(result.stderr_log.read_text(encoding="utf-8"), "failed")

    def test_run_multiwfn_grid_timeout_writes_partial_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                raise subprocess.TimeoutExpired(command, timeout=5, output="partial stdout", stderr="partial stderr")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(wavefunction, root / "products", timeout=5)

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, GRID_PROCESSING_FAILED_CODE)
            self.assertIn("timed out after 5 seconds", result.error or "")
            self.assertIn("partial stdout", result.stdout_log.read_text(encoding="utf-8"))
            self.assertIn("partial stderr", result.stderr_log.read_text(encoding="utf-8"))
            self.assertIn("timed out", result.recipe_path.read_text(encoding="utf-8"))

    def test_run_multiwfn_grid_launch_error_writes_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=OSError("boom")):
                    result = run_multiwfn_grid(wavefunction, root / "products")

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, GRID_PROCESSING_FAILED_CODE)
            self.assertIn("Failed to launch", result.error or "")
            self.assertIn("boom", result.stderr_log.read_text(encoding="utf-8"))

    def test_run_multiwfn_grid_requires_wavefunction(self):
        candidate = self.make_candidate(Path(tempfile.mkdtemp()))
        with tempfile.TemporaryDirectory() as tmp:
            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with self.assertRaises(FileNotFoundError):
                    run_multiwfn_grid(Path(tmp) / "missing.fch", Path(tmp) / "products")

    def test_main_reports_discovery_errors_without_traceback(self):
        stderr = io.StringIO()
        with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=None):
            with patch("sys.stderr", stderr):
                code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                    ["missing.fch", "products"]
                )

        self.assertEqual(code, 2)
        self.assertIn("Cannot find Multiwfn", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
