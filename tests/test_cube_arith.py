import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.cube_arith import (
    CubeTerm,
    combine_cubes,
    main,
    run_workflow,
    terms_for_operation,
)
from multiwfn2vesta.cube_vesta import _iter_cube_data_values


BASE_CUBE = """base comment one
base comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
  1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0
"""


DELTA_CUBE = """delta comment one
delta comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
  0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0
"""


THIRD_CUBE = """third comment one
third comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
  2.0 2.0 2.0 2.0 2.0 2.0 2.0 2.0
"""


BAD_GRID_CUBE = """bad grid
bad grid
    2    -1.000000    -2.000000     0.500000
    1     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
  0.0 0.1 0.2 0.3
"""


BAD_ATOMS_CUBE = """bad atoms
bad atoms
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    6     6.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
  0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0
"""


ANGSTROM_UNIT_CUBE = """angstrom unit
angstrom unit
    2    -1.000000    -2.000000     0.500000
   -2     0.500000     0.000000     0.000000
   -2     0.000000     0.500000     0.000000
   -2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
  0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0
"""


class TestCubeArithmetic(unittest.TestCase):
    def write_tmp(self, root, name, text):
        path = Path(root) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def read_values(self, path):
        return list(_iter_cube_data_values(Path(path)))

    def test_combine_cubes_writes_linear_combination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = self.write_tmp(root, "base.cub", BASE_CUBE)
            delta = self.write_tmp(root, "delta.cub", DELTA_CUBE)
            out = root / "products" / "linear.cub"

            data_min, data_max, count = combine_cubes(
                [CubeTerm(1.0, base), CubeTerm(-2.0, delta)],
                out,
                comment1="custom one",
                comment2="custom two",
            )

            self.assertEqual(count, 8)
            self.assertEqual(data_min, 0.0)
            self.assertEqual(data_max, 0.0)
            text = out.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("custom one\ncustom two\n"))
            self.assertEqual(self.read_values(out), [0.0] * 8)

    def test_terms_for_common_fukui_operations(self):
        neutral = Path("neutral.cub")
        anion = Path("anion.cub")
        cation = Path("cation.cub")
        alpha = Path("alpha.cub")
        beta = Path("beta.cub")

        self.assertEqual(
            terms_for_operation("fukui-plus", neutral_cube=neutral, anion_cube=anion),
            (CubeTerm(1.0, anion), CubeTerm(-1.0, neutral)),
        )
        self.assertEqual(
            terms_for_operation("fukui-minus", neutral_cube=neutral, cation_cube=cation),
            (CubeTerm(1.0, neutral), CubeTerm(-1.0, cation)),
        )
        self.assertEqual(
            terms_for_operation("dual-descriptor", neutral_cube=neutral, anion_cube=anion, cation_cube=cation),
            (CubeTerm(1.0, anion), CubeTerm(-2.0, neutral), CubeTerm(1.0, cation)),
        )
        self.assertEqual(
            terms_for_operation("spin-density", plus_cube=alpha, minus_cube=beta),
            (CubeTerm(1.0, alpha), CubeTerm(-1.0, beta)),
        )

    def test_run_workflow_writes_cube_recipe_and_signed_vesta(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plus = self.write_tmp(root, "plus.cub", BASE_CUBE)
            minus = self.write_tmp(root, "minus.cub", THIRD_CUBE)

            result = run_workflow(
                root / "products",
                operation="density-difference",
                terms=(CubeTerm(1.0, plus), CubeTerm(-1.5, minus)),
                stem="diff",
                isosurface=0.2,
            )

            self.assertEqual(result.data_count, 8)
            self.assertEqual(result.data_min, -2.0)
            self.assertEqual(result.data_max, 5.0)
            self.assertTrue(result.output_cube.exists())
            self.assertTrue(result.recipe_path.exists())
            self.assertIsNotNone(result.vesta_result)
            vesta_text = result.vesta_result.vesta_path.read_text(encoding="utf-8")
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("diff.cub", vesta_text)
            self.assertIn("ISURF", vesta_text)
            self.assertIn("density-difference", recipe)
            self.assertIn("`1.0` *", recipe)
            self.assertIn("`-1.5` *", recipe)

    def test_run_workflow_can_skip_vesta(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = self.write_tmp(root, "base.cub", BASE_CUBE)
            delta = self.write_tmp(root, "delta.cub", DELTA_CUBE)

            result = run_workflow(
                root / "products",
                terms=(CubeTerm(1.0, base), CubeTerm(-1.0, delta)),
                no_vesta=True,
            )

            self.assertTrue(result.output_cube.exists())
            self.assertIsNone(result.vesta_result)
            self.assertIn("vesta_file: `None`", result.recipe_path.read_text(encoding="utf-8"))

    def test_fukui_plus_auto_preset_uses_density_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            neutral = self.write_tmp(root, "neutral.cub", DELTA_CUBE)
            anion = self.write_tmp(root, "anion.cub", BASE_CUBE)

            result = run_workflow(
                root / "products",
                operation="fukui-plus",
                terms=terms_for_operation("fukui-plus", neutral_cube=neutral, anion_cube=anion),
                stem="fplus",
                isosurface=0.6,
            )

            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(result.vesta_result.vesta_path.name, "fplus_density_cube.vesta")
            text = result.vesta_result.vesta_path.read_text(encoding="utf-8")
            self.assertIn("ISURF\n  1   1        0.6", text)
            self.assertNotIn("      -0.6", text)

    def test_spin_density_auto_preset_uses_spin_density_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            alpha = self.write_tmp(root, "alpha_density.cub", BASE_CUBE)
            beta = self.write_tmp(root, "beta_density.cub", THIRD_CUBE)

            result = run_workflow(
                root / "products",
                operation="spin-density",
                terms=terms_for_operation("spin-density", plus_cube=alpha, minus_cube=beta),
                stem="spin_density",
            )

            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(result.output_cube.name, "spin_density.cub")
            self.assertEqual(result.vesta_result.vesta_path.name, "spin_density_spin-density_cube.vesta")
            self.assertEqual(self.read_values(result.output_cube), [-1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
            text = result.vesta_result.vesta_path.read_text(encoding="utf-8")
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertRegex(
                text,
                r"ISURF\n  1   1\s+0\.02\s+255\s+80\s+80\s+145\s+255\n  1   1\s+-0\.02\s+70\s+130\s+255\s+145\s+255",
            )
            self.assertIn("canonical_preset: `spin-density`", manifest)
            self.assertIn("requested_preset: `spin-density`", manifest)
            self.assertIn("alpha-minus-beta spin density", manifest)

    def test_rejects_incompatible_grid_and_atoms(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = self.write_tmp(root, "base.cub", BASE_CUBE)
            bad_grid = self.write_tmp(root, "bad_grid.cub", BAD_GRID_CUBE)
            bad_atoms = self.write_tmp(root, "bad_atoms.cub", BAD_ATOMS_CUBE)

            with self.assertRaisesRegex(ValueError, "grid is not compatible"):
                combine_cubes([CubeTerm(1.0, base), CubeTerm(1.0, bad_grid)], root / "bad_grid_out.cub")
            with self.assertRaisesRegex(ValueError, "atom list is not compatible"):
                combine_cubes([CubeTerm(1.0, base), CubeTerm(1.0, bad_atoms)], root / "bad_atoms_out.cub")

            combine_cubes(
                [CubeTerm(1.0, base), CubeTerm(1.0, bad_atoms)],
                root / "non_strict_atoms.cub",
                strict_atoms=False,
            )

    def test_rejects_mixed_cube_unit_conventions_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = self.write_tmp(root, "base.cub", BASE_CUBE)
            angstrom = self.write_tmp(root, "angstrom.cub", ANGSTROM_UNIT_CUBE)

            with self.assertRaisesRegex(ValueError, "unit convention is not compatible"):
                combine_cubes([CubeTerm(1.0, base), CubeTerm(1.0, angstrom)], root / "mixed_units.cub")

            combine_cubes(
                [CubeTerm(1.0, base), CubeTerm(1.0, angstrom)],
                root / "forced_angstrom.cub",
                cube_units="angstrom",
            )

    def test_rejects_output_overwriting_input_cube(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = self.write_tmp(root, "base.cub", BASE_CUBE)
            delta = self.write_tmp(root, "delta.cub", DELTA_CUBE)

            with self.assertRaisesRegex(ValueError, "overwrite an input cube"):
                combine_cubes([CubeTerm(1.0, base), CubeTerm(-1.0, delta)], base)

    def test_main_runs_dual_descriptor_and_reports_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            neutral = self.write_tmp(root, "neutral.cub", BASE_CUBE)
            anion = self.write_tmp(root, "anion.cub", DELTA_CUBE)
            cation = self.write_tmp(root, "cation.cub", THIRD_CUBE)
            output = io.StringIO()

            with patch("sys.stdout", output):
                code = main(
                    [
                        str(root / "products"),
                        "--operation",
                        "dual-descriptor",
                        "--anion-cube",
                        str(anion),
                        "--neutral-cube",
                        str(neutral),
                        "--cation-cube",
                        str(cation),
                        "--stem",
                        "dual",
                        "--no-vesta",
                    ]
                )

            self.assertEqual(code, 0)
            self.assertTrue((root / "products" / "dual.cub").exists())
            self.assertIn("dual.cub", output.getvalue())
            self.assertEqual(self.read_values(root / "products" / "dual.cub"), [2.0 - 1.5 * i for i in range(1, 9)])

    def test_main_runs_spin_density_and_reports_vesta_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            alpha = self.write_tmp(root, "alpha.cub", BASE_CUBE)
            beta = self.write_tmp(root, "beta.cub", THIRD_CUBE)
            output = io.StringIO()

            with patch("sys.stdout", output):
                code = main(
                    [
                        str(root / "products"),
                        "--operation",
                        "spin-density",
                        "--plus-cube",
                        str(alpha),
                        "--minus-cube",
                        str(beta),
                        "--stem",
                        "spin",
                    ]
                )

            self.assertEqual(code, 0)
            self.assertTrue((root / "products" / "spin.cub").exists())
            self.assertTrue((root / "products" / "spin_spin-density_cube.vesta").exists())
            self.assertIn("spin_spin-density_cube.vesta", output.getvalue())

    def test_main_reports_missing_terms(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = main(["products", "--operation", "linear"])

        self.assertEqual(code, 2)
        self.assertIn("At least one cube term is required", output.getvalue())


if __name__ == "__main__":
    unittest.main()
