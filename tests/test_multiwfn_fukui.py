import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.cube_vesta import _iter_cube_data_values
from multiwfn2vesta.executables import ExecutableCandidate
from multiwfn2vesta.multiwfn_fukui import (
    FUKUI_PROCESSING_FAILED_CODE,
    main,
    normalize_operations,
    run_multiwfn_fukui,
)


def cube_text(values):
    return """density comment one
density comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
{data}
""".format(data="".join(" {0:.6f}".format(value) for value in values))


NEUTRAL_CUBE = cube_text([1, 2, 3, 4, 5, 6, 7, 8])
ANION_CUBE = cube_text([2, 3, 4, 5, 6, 7, 8, 9])
CATION_CUBE = cube_text([0, 1, 2, 3, 4, 5, 6, 7])


class TestMultiwfnFukuiRunner(unittest.TestCase):
    def make_candidate(self, root):
        fake_exe = Path(root) / "Multiwfn_noGUI"
        fake_exe.write_text("#!/bin/sh\n", encoding="utf-8")
        fake_exe.chmod(0o755)
        return ExecutableCandidate("Multiwfn_noGUI", fake_exe, "test", True, True)

    def read_values(self, path):
        return list(_iter_cube_data_values(Path(path)))

    def test_normalize_operations(self):
        self.assertEqual(
            normalize_operations(None),
            ("fukui-plus", "fukui-minus", "dual-descriptor"),
        )
        self.assertEqual(
            normalize_operations(["fukui_plus", "fukui-plus", "dual-descriptor"]),
            ("fukui-plus", "dual-descriptor"),
        )
        with self.assertRaisesRegex(ValueError, "cannot be combined"):
            normalize_operations(["all", "fukui-plus"])

    def test_run_multiwfn_fukui_generates_density_cubes_and_arithmetic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            neutral = root / "neutral.molden"
            anion = root / "anion.molden"
            cation = root / "cation.molden"
            for path in (neutral, anion, cation):
                path.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                wavefunction_name = Path(command[1]).name
                cube = {
                    "neutral.molden": NEUTRAL_CUBE,
                    "anion.molden": ANION_CUBE,
                    "cation.molden": CATION_CUBE,
                }[wavefunction_name]
                Path(kwargs["cwd"], "density.cub").write_text(cube, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout=wavefunction_name, stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_fukui(
                        root / "products",
                        neutral=neutral,
                        anion=anion,
                        cation=cation,
                        operations=["all"],
                        stem="case",
                        grid_points=(6, 7, 8),
                        no_vesta=True,
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.cli_returncode, 0)
            self.assertEqual(mocked_run.call_count, 3)
            self.assertEqual(result.operations, ("fukui-plus", "fukui-minus", "dual-descriptor"))

            neutral_grid = result.grid_results["neutral"]
            anion_grid = result.grid_results["anion"]
            cation_grid = result.grid_results["cation"]
            self.assertEqual(neutral_grid.cube.name, "case_neutral_density.cub")
            self.assertEqual(anion_grid.cube.name, "case_anion_density.cub")
            self.assertEqual(cation_grid.cube.name, "case_cation_density.cub")
            self.assertEqual(
                neutral_grid.command_file.read_text(encoding="utf-8"),
                "5\n1\n4\n6,7,8\n2\n0\nq\n",
            )
            self.assertIn(str(neutral_grid.cube), anion_grid.command_file.read_text(encoding="utf-8"))
            self.assertIn(str(neutral_grid.cube), cation_grid.command_file.read_text(encoding="utf-8"))

            fplus = result.arithmetic_results["fukui-plus"]
            fminus = result.arithmetic_results["fukui-minus"]
            dual = result.arithmetic_results["dual-descriptor"]
            self.assertEqual(self.read_values(fplus.output_cube), [1.0] * 8)
            self.assertEqual(self.read_values(fminus.output_cube), [1.0] * 8)
            self.assertEqual(self.read_values(dual.output_cube), [0.0] * 8)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("neutral density cube is generated first", recipe)
            self.assertIn("fukui-plus", recipe)
            self.assertIn("dual-descriptor", recipe)

    def test_run_multiwfn_fukui_requires_needed_charged_states(self):
        with tempfile.TemporaryDirectory() as tmp:
            neutral = Path(tmp) / "neutral.molden"
            neutral.write_text("wavefunction", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "require --anion"):
                run_multiwfn_fukui(
                    Path(tmp) / "products",
                    neutral=neutral,
                    operations=["fukui-plus"],
                )

    def test_run_multiwfn_fukui_stops_after_failed_grid_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            neutral = root / "neutral.molden"
            anion = root / "anion.molden"
            neutral.write_text("wavefunction", encoding="utf-8")
            anion.write_text("wavefunction", encoding="utf-8")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=None):
                result = run_multiwfn_fukui(
                    root / "products",
                    neutral=neutral,
                    anion=anion,
                    operations=["fukui-plus"],
                )

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, FUKUI_PROCESSING_FAILED_CODE)
            self.assertIn("Neutral density grid generation failed", result.error or "")
            self.assertTrue(result.recipe_path.exists())

    def test_run_multiwfn_fukui_records_cube_when_vesta_generation_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            neutral = root / "neutral.molden"
            anion = root / "anion.molden"
            for path in (neutral, anion):
                path.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                wavefunction_name = Path(command[1]).name
                cube = {
                    "neutral.molden": NEUTRAL_CUBE,
                    "anion.molden": ANION_CUBE,
                }[wavefunction_name]
                Path(kwargs["cwd"], "density.cub").write_text(cube, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout=wavefunction_name, stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    with patch("multiwfn2vesta.cube_arith.run_preset", side_effect=ValueError("bad isosurface")):
                        result = run_multiwfn_fukui(
                            root / "products",
                            neutral=neutral,
                            anion=anion,
                            operations=["fukui-plus"],
                        )

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, FUKUI_PROCESSING_FAILED_CODE)
            self.assertIn("VESTA generation failed for fukui-plus", result.error or "")
            arithmetic = result.arithmetic_results["fukui-plus"]
            self.assertTrue(arithmetic.output_cube.exists())
            self.assertIsNone(arithmetic.vesta_result)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("output_cube", recipe)
            self.assertIn("fukui_plus.cub", recipe)
            self.assertNotIn("status: `not generated`", recipe)

    def test_main_reports_missing_state_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            neutral = Path(tmp) / "neutral.molden"
            neutral.write_text("wavefunction", encoding="utf-8")
            stderr = io.StringIO()

            with patch("sys.stderr", stderr):
                code = main(
                    [
                        str(Path(tmp) / "products"),
                        "--operation",
                        "fukui-plus",
                        "--neutral",
                        str(neutral),
                    ]
                )

            self.assertEqual(code, 2)
            self.assertIn("fukui-run:", stderr.getvalue())
            self.assertIn("require --anion", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
