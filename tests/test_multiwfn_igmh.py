import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.executables import ExecutableCandidate
from multiwfn2vesta.multiwfn_igmh import (
    IGMH_OUTPUT_MISSING_CODE,
    build_igmh_commands,
    run_multiwfn_igmh,
    wavefunction_has_molden_cell,
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


class TestMultiwfnIgmhRunner(unittest.TestCase):
    def make_candidate(self, root):
        fake_exe = Path(root) / "Multiwfn_noGUI"
        fake_exe.write_text("#!/bin/sh\n", encoding="utf-8")
        fake_exe.chmod(0o755)
        return ExecutableCandidate("Multiwfn_noGUI", fake_exe, "test", True, True)

    def test_build_igmh_command_stream_for_points_grid(self):
        commands = build_igmh_commands(["1-48", "49-60"], grid_points=(12, 13, 14))

        self.assertEqual(commands, ["20", "11", "2", "1-48", "49-60", "4", "12,13,14", "3", "0", "0", "q"])

    def test_build_igmh_command_stream_for_spacing_grid_with_complement(self):
        commands = build_igmh_commands(["1-48", "c"], grid_mode="spacing", grid_spacing=0.6)

        self.assertEqual(commands, ["20", "11", "2", "1-48", "c", "4", "0.6", "3", "0", "0", "q"])

    def test_build_igm_command_stream_uses_actual_density_prompt(self):
        commands = build_igmh_commands(
            ["1-48", "49-60"],
            method="igm",
            sl2r_source="actual",
            grid_mode="medium",
        )

        self.assertEqual(commands, ["20", "10", "2", "1-48", "49-60", "1", "2", "3", "0", "0", "q"])

    def test_build_migm_command_stream_can_use_promolecular_sl2r(self):
        commands = build_igmh_commands(
            ["1-48", "c"],
            method="migm",
            sl2r_source="promolecular",
            grid_mode="spacing",
            grid_spacing=0.25,
        )

        self.assertEqual(commands, ["20", "-10", "2", "1-48", "c", "2", "4", "0.25", "3", "0", "0", "q"])

    def test_igmh_rejects_promolecular_sl2r_source(self):
        with self.assertRaisesRegex(ValueError, "IGMH always uses actual"):
            build_igmh_commands(["1-48", "c"], method="igmh", sl2r_source="promolecular")

    def test_build_igmh_rejects_points_grid_for_periodic_inputs(self):
        with self.assertRaisesRegex(ValueError, "periodic Molden"):
            build_igmh_commands(["1-48", "c"], grid_mode="points", periodic=True)

    def test_build_igmh_command_stream_for_pbc_cell_grid(self):
        commands = build_igmh_commands(
            ["1-48", "c"],
            grid_mode="pbc-cell",
            grid_spacing=0.25,
            pbc_origin=(0.0, 0.0, 0.0),
            pbc_lengths=(10.0, 11.0, 12.0),
            periodic=True,
        )

        self.assertEqual(
            commands,
            ["20", "11", "2", "1-48", "c", "9", "0.0,0.0,0.0", "10.0,11.0,12.0", "0.25", "3", "0", "0", "q"],
        )

    def test_build_igmh_requires_two_fragments(self):
        with self.assertRaisesRegex(ValueError, "at least two"):
            build_igmh_commands(["1-3"])

    def test_wavefunction_has_molden_cell_detects_periodic_molden(self):
        with tempfile.TemporaryDirectory() as tmp:
            molden = Path(tmp) / "periodic.molden"
            molden.write_text("[Molden Format]\n[Cell]\n1 0 0\n", encoding="utf-8")

            self.assertTrue(wavefunction_has_molden_cell(molden))

    def test_run_multiwfn_igmh_writes_cubes_recipe_and_vesta(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "case.molden"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "dg_inter.cub").write_text(SURFACE_CUBE, encoding="utf-8")
                (cwd / "sl2r.cub").write_text(TEXTURE_CUBE, encoding="utf-8")
                (cwd / "dg_intra.cub").write_text(SURFACE_CUBE, encoding="utf-8")
                (cwd / "dg.cub").write_text(SURFACE_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="warn")

            with patch("multiwfn2vesta.multiwfn_igmh.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_igmh.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_igmh(
                        wavefunction,
                        root / "products",
                        fragments=["1-3", "4-6"],
                        nthreads=2,
                        timeout=30,
                        stem="case",
                        method="igm",
                        sl2r_source="actual",
                        grid_mode="spacing",
                        grid_spacing=0.6,
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.cli_returncode, 0)
            self.assertEqual(mocked_run.call_args.args[0], [str(candidate.path), str(wavefunction.resolve()), "-nt", "2"])
            self.assertEqual(mocked_run.call_args.kwargs["cwd"], str(root / "products" / "multiwfn_igm_raw"))
            self.assertEqual(mocked_run.call_args.kwargs["timeout"], 30)
            self.assertEqual(mocked_run.call_args.kwargs["env"]["Multiwfnpath"], str(candidate.path.parent))
            self.assertEqual(
                result.command_file.read_text(encoding="utf-8"),
                "20\n10\n2\n1-3\n4-6\n1\n4\n0.6\n3\n0\n0\nq\n",
            )
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "ok")
            self.assertEqual(result.stderr_log.read_text(encoding="utf-8"), "warn")
            self.assertTrue(result.raw_dg_inter_cube.exists())
            self.assertTrue(result.raw_sl2r_cube.exists())
            self.assertEqual(result.dg_inter_cube.name, "case_dg_inter.cub")
            self.assertEqual(result.sl2r_cube.name, "case_sl2r.cub")
            self.assertEqual(result.dg_intra_cube.name, "case_dg_intra.cub")
            self.assertEqual(result.dg_cube.name, "case_dg.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertTrue(result.vesta_result.vesta_path.exists())
            self.assertEqual(result.vesta_result.vesta_path.name, "case_igm_cube.vesta")
            self.assertIn("IMPORT_TEXTURE", result.vesta_result.vesta_path.read_text(encoding="utf-8"))
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `igmh`", manifest)
            self.assertIn("title: `case_dg_inter (igm)`", manifest)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("method: `igm`", recipe)
            self.assertIn("sl2r_source: `actual`", recipe)
            self.assertIn("fragments: `1-3; 4-6`", recipe)
            self.assertIn("grid_spacing: `0.6`", recipe)

    def test_run_multiwfn_igmh_reports_missing_required_cubes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "case.molden"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_igmh.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_igmh.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(candidate.path)], 0, stdout="ok", stderr=""),
                ):
                    result = run_multiwfn_igmh(wavefunction, root / "products", fragments=["1", "2"])

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, IGMH_OUTPUT_MISSING_CODE)
            self.assertIn("required IGMH cube output is missing", result.error or "")
            self.assertIsNone(result.dg_inter_cube)
            self.assertIsNone(result.sl2r_cube)
            self.assertIsNone(result.vesta_result)

    def test_run_multiwfn_igmh_can_skip_vesta_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "case.molden"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "dg_inter.cub").write_text(SURFACE_CUBE, encoding="utf-8")
                (cwd / "sl2r.cub").write_text(TEXTURE_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            with patch("multiwfn2vesta.multiwfn_igmh.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_igmh.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_igmh(wavefunction, root / "products", fragments=["1", "2"], make_vesta=False)

            self.assertTrue(result.success)
            self.assertTrue(result.dg_inter_cube.exists())
            self.assertTrue(result.sl2r_cube.exists())
            self.assertIsNone(result.vesta_result)

    def test_main_reports_fragment_errors_without_traceback(self):
        stderr = io.StringIO()
        candidate = self.make_candidate(Path(tempfile.mkdtemp()))
        with tempfile.TemporaryDirectory() as tmp:
            wavefunction = Path(tmp) / "case.molden"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            with patch("multiwfn2vesta.multiwfn_igmh.find_multiwfn", return_value=candidate):
                with patch("sys.stderr", stderr):
                    code = __import__("multiwfn2vesta.multiwfn_igmh", fromlist=["main"]).main(
                        [str(wavefunction), str(Path(tmp) / "products"), "--fragment", "1"]
                    )

        self.assertEqual(code, 2)
        self.assertIn("igmh-run:", stderr.getvalue())
        self.assertIn("at least two", stderr.getvalue())

    def test_main_igm_rejects_method_override(self):
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = __import__("multiwfn2vesta.multiwfn_igmh", fromlist=["main_igm"]).main_igm(
                ["input.molden", "products", "--method", "igmh"]
            )

        self.assertEqual(code, 2)
        self.assertIn("igm-run:", stderr.getvalue())
        self.assertIn("--method is fixed", stderr.getvalue())

    def test_main_rejects_points_grid_for_periodic_molden_before_launching_multiwfn(self):
        stderr = io.StringIO()
        candidate = self.make_candidate(Path(tempfile.mkdtemp()))
        with tempfile.TemporaryDirectory() as tmp:
            wavefunction = Path(tmp) / "periodic.molden"
            wavefunction.write_text("[Molden Format]\n[Cell]\n1 0 0\n0 1 0\n0 0 1\n", encoding="utf-8")
            with patch("multiwfn2vesta.multiwfn_igmh.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_igmh.subprocess.run") as mocked_run:
                    with patch("sys.stderr", stderr):
                        code = __import__("multiwfn2vesta.multiwfn_igmh", fromlist=["main"]).main(
                            [
                                str(wavefunction),
                                str(Path(tmp) / "products"),
                                "--fragment",
                                "1",
                                "--fragment",
                                "2",
                            ]
                        )

            self.assertFalse(mocked_run.called)

        self.assertEqual(code, 2)
        self.assertIn("periodic Molden", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
