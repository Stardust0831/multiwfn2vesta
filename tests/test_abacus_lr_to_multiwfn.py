import tempfile
import unittest
from pathlib import Path

from multiwfn2vesta.abacus_lr_to_multiwfn import (
    RY_TO_EV,
    convert_abacus_lr_to_multiwfn,
    infer_lr_dimensions,
    parse_abacus_lr,
)


class TestAbacusLrToMultiwfn(unittest.TestCase):
    def test_convert_singlet_files_to_multiwfn_plain_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out_dir = root / "OUT.lr"
            out_dir.mkdir()
            (out_dir / "Excitation_Energy_singlet.dat").write_text("1.0 2.0\n", encoding="utf-8")
            (out_dir / "Excitation_Amplitude_singlet_0.dat").write_text(
                "0.5 0.0 -0.25 0.1\n"
                "0.0 0.2 0.3 -0.4\n",
                encoding="utf-8",
            )
            output = root / "h2o_singlet.excit.txt"

            result = convert_abacus_lr_to_multiwfn(
                root,
                output,
                label="singlet",
                nocc=2,
                nvirt=2,
                coeff_threshold=0.15,
                coefficient_scale=1.0,
            )

            self.assertEqual(len(result.states), 2)
            self.assertEqual(result.nocc, 2)
            self.assertEqual(result.nvirt, 2)
            self.assertIn("explicit nocc,nvirt", result.dimension_source)
            self.assertEqual(result.coefficient_scale, 1.0)
            self.assertEqual(result.skipped_coefficients, 3)
            text = output.read_text(encoding="utf-8")
            self.assertIn(f"Excited State 1  1{RY_TO_EV:12.6f}", text)
            self.assertIn("     1 ->     3    0.500000", text)
            self.assertIn("     2 ->     3   -0.250000", text)
            self.assertIn("     1 ->     4    0.200000", text)
            self.assertIn("     2 ->     4   -0.400000", text)
            self.assertIn("0.500000\n     2 ->     3", text)
            self.assertIn("-0.250000\n\n Excited State 2", text)
            self.assertTrue(output.with_suffix(output.suffix + ".recipe.md").exists())

    def test_triplet_label_sets_multiplicity_three(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Excitation_Energy_triplet.dat").write_text("3.0\n", encoding="utf-8")
            (root / "Excitation_Amplitude_triplet_0.dat").write_text("0.7 0.1\n", encoding="utf-8")

            states, _energy, _amp, _skipped = parse_abacus_lr(
                root,
                label="triplet",
                nocc=1,
                nvirt=2,
                coefficient_scale=1.0,
            )

            self.assertEqual(states[0].multiplicity, 3)
            self.assertEqual(states[0].transitions[0].occ, 1)
            self.assertAlmostEqual(states[0].transitions[0].coeff, 0.7)
            self.assertEqual(states[0].transitions[0].virt, 2)
            self.assertEqual(states[0].transitions[1].virt, 3)

    def test_infers_dimensions_from_input_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out_dir = root / "OUT.lr"
            out_dir.mkdir()
            (root / "INPUT").write_text("nocc 2\nnvirt 2\n", encoding="utf-8")
            (out_dir / "Excitation_Energy_singlet.dat").write_text("1.0\n", encoding="utf-8")
            (out_dir / "Excitation_Amplitude_singlet_0.dat").write_text("0.1 0.2 0.3 0.4\n", encoding="utf-8")
            output = root / "inferred.excit.txt"

            result = convert_abacus_lr_to_multiwfn(root, output, label="singlet")

            self.assertEqual(result.nocc, 2)
            self.assertEqual(result.nvirt, 2)
            self.assertAlmostEqual(result.coefficient_scale, 2**-0.5)
            self.assertEqual(len(result.states[0].transitions), 4)
            self.assertTrue(result.dimension_source.endswith("INPUT"))
            recipe = output.with_suffix(output.suffix + ".recipe.md").read_text(encoding="utf-8")
            self.assertIn("- nocc: `2`", recipe)
            self.assertIn("- nvirt: `2`", recipe)

    def test_running_log_dimensions_take_precedence_over_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out_dir = root / "OUT.lr"
            out_dir.mkdir()
            (root / "INPUT").write_text("nocc 99\nnvirt 99\n", encoding="utf-8")
            (out_dir / "running_lr.log").write_text(
                "number of occupied bands: 1\nnumber of virtual bands: 2\n",
                encoding="utf-8",
            )

            nocc, nvirt, source = infer_lr_dimensions(root)

            self.assertEqual((nocc, nvirt), (1, 2))
            self.assertTrue(source.endswith("running_lr.log"))

    def test_missing_dimensions_gives_actionable_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Excitation_Energy_singlet.dat").write_text("1.0\n", encoding="utf-8")
            (root / "Excitation_Amplitude_singlet_0.dat").write_text("0.1 0.2\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "pass --nocc and --nvirt explicitly"):
                convert_abacus_lr_to_multiwfn(root, root / "missing.excit.txt", label="singlet")

    def test_rejects_inconsistent_dimensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Excitation_Energy_singlet.dat").write_text("1.0\n", encoding="utf-8")
            (root / "Excitation_Amplitude_singlet_0.dat").write_text("0.1 0.2 0.3\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "not divisible"):
                parse_abacus_lr(root, label="singlet", nocc=2, nvirt=2)

    def test_rejects_multiple_rank_files_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Excitation_Energy_singlet.dat").write_text("1.0\n", encoding="utf-8")
            (root / "Excitation_Amplitude_singlet_0.dat").write_text("0.1 0.2\n", encoding="utf-8")
            (root / "Excitation_Amplitude_singlet_1.dat").write_text("0.3 0.4\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Multiple ABACUS amplitude rank files"):
                parse_abacus_lr(root, label="singlet", nocc=1, nvirt=2)


if __name__ == "__main__":
    unittest.main()
