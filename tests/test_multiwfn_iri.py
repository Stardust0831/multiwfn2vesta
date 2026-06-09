import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.executables import ExecutableCandidate
from multiwfn2vesta.multiwfn_iri import DEFAULT_IRI_COMMANDS, run_multiwfn_iri


COLOR_CUBE = """color one
color two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    1     0.000000     0.500000     0.000000
    3     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -0.10 -0.03 0.00 0.01 0.03 0.10
"""


SURFACE_CUBE = """surface one
surface two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    1     0.000000     0.500000     0.000000
    3     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.20 0.80 1.00 1.05 1.20 1.60
"""


class TestMultiwfnIriRunner(unittest.TestCase):
    def make_candidate(self, root):
        fake_exe = Path(root) / "Multiwfn_noGUI"
        fake_exe.write_text("#!/bin/sh\n", encoding="utf-8")
        fake_exe.chmod(0o755)
        return ExecutableCandidate("Multiwfn_noGUI", fake_exe, "test", True, True)

    def test_run_multiwfn_iri_writes_processed_cubes_and_vesta(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "func1.cub").write_text(COLOR_CUBE, encoding="utf-8")
                (cwd / "func2.cub").write_text(SURFACE_CUBE, encoding="utf-8")
                (cwd / "output.txt").write_text("iri log", encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="warn")

            with patch("multiwfn2vesta.multiwfn_iri.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_iri.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_iri(
                        wavefunction,
                        root / "products",
                        nthreads=2,
                        timeout=30,
                        stem="case",
                        surface_band=0.25,
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.cli_returncode, 0)
            self.assertEqual(mocked_run.call_args.args[0], [str(candidate.path), str(wavefunction.resolve()), "-nt", "2"])
            self.assertEqual(mocked_run.call_args.kwargs["cwd"], str(root / "products" / "multiwfn_iri_raw"))
            self.assertEqual(mocked_run.call_args.kwargs["timeout"], 30)
            self.assertEqual(mocked_run.call_args.kwargs["env"]["Multiwfnpath"], str(candidate.path.parent))
            self.assertIn("\n".join(DEFAULT_IRI_COMMANDS[:3]), result.command_file.read_text(encoding="utf-8"))
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "ok")
            self.assertEqual(result.stderr_log.read_text(encoding="utf-8"), "warn")
            self.assertEqual(result.multiwfn_output_txt.read_text(encoding="utf-8"), "iri log")
            self.assertTrue(result.raw_color_cube.exists())
            self.assertTrue(result.raw_surface_cube.exists())
            self.assertTrue(result.color_cube.exists())
            self.assertTrue(result.surface_cube.exists())
            self.assertIn("-4.00000E-02", result.color_cube.read_text(encoding="utf-8"))
            self.assertIn("2.00000E-01", result.color_cube.read_text(encoding="utf-8"))
            self.assertIsNotNone(result.vesta_result)
            self.assertTrue(result.vesta_result.vesta_path.exists())
            self.assertIn("IMPORT_TEXTURE", result.vesta_result.vesta_path.read_text(encoding="utf-8"))
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `iri`", manifest)
            self.assertIn("tex_reference_source: `surface-band`", manifest)

    def test_run_multiwfn_iri_reports_missing_cubes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_iri.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_iri.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(candidate.path)], 0, stdout="ok", stderr=""),
                ):
                    result = run_multiwfn_iri(wavefunction, root / "products")

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, 3)
            self.assertIn("required IRI cube output is missing", result.error or "")
            self.assertIsNone(result.color_cube)
            self.assertIsNone(result.surface_cube)
            self.assertIsNone(result.vesta_result)

    def test_run_multiwfn_iri_can_skip_vesta_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "func1.cub").write_text(COLOR_CUBE, encoding="utf-8")
                (cwd / "func2.cub").write_text(SURFACE_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            with patch("multiwfn2vesta.multiwfn_iri.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_iri.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_iri(wavefunction, root / "products", make_vesta=False)

            self.assertTrue(result.success)
            self.assertTrue(result.color_cube.exists())
            self.assertTrue(result.surface_cube.exists())
            self.assertIsNone(result.vesta_result)

    def test_run_multiwfn_iri_records_nonzero_multiwfn_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_iri.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_iri.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(candidate.path)], 7, stdout="bad", stderr="failed"),
                ):
                    result = run_multiwfn_iri(wavefunction, root / "products")

            self.assertFalse(result.success)
            self.assertEqual(result.returncode, 7)
            self.assertEqual(result.cli_returncode, 7)
            self.assertIn("return code 7", result.error or "")
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "bad")
            self.assertEqual(result.stderr_log.read_text(encoding="utf-8"), "failed")
            self.assertIsNone(result.vesta_result)

    def test_run_multiwfn_iri_timeout_writes_partial_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                raise subprocess.TimeoutExpired(command, timeout=5, output="partial stdout", stderr="partial stderr")

            with patch("multiwfn2vesta.multiwfn_iri.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_iri.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_iri(wavefunction, root / "products", timeout=5)

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, 4)
            self.assertIn("timed out after 5 seconds", result.error or "")
            self.assertIn("partial stdout", result.stdout_log.read_text(encoding="utf-8"))
            self.assertIn("partial stderr", result.stderr_log.read_text(encoding="utf-8"))
            self.assertIsNone(result.color_cube)
            self.assertIsNone(result.surface_cube)
            self.assertIsNone(result.vesta_result)

    def test_run_multiwfn_iri_requires_wavefunction(self):
        candidate = self.make_candidate(Path(tempfile.mkdtemp()))
        with tempfile.TemporaryDirectory() as tmp:
            with patch("multiwfn2vesta.multiwfn_iri.find_multiwfn", return_value=candidate):
                with self.assertRaises(FileNotFoundError):
                    run_multiwfn_iri(Path(tmp) / "missing.fch", Path(tmp) / "products")

    def test_main_reports_discovery_errors_without_traceback(self):
        stderr = io.StringIO()
        with patch("multiwfn2vesta.multiwfn_iri.find_multiwfn", return_value=None):
            with patch("sys.stderr", stderr):
                code = __import__("multiwfn2vesta.multiwfn_iri", fromlist=["main"]).main(["missing.fch", "products"])

        self.assertEqual(code, 2)
        self.assertIn("Cannot find Multiwfn", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
