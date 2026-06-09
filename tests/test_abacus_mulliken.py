import tempfile
import unittest
from pathlib import Path

from multiwfn2vesta.abacus_mulliken import (
    color_vesta_from_mulliken,
    mulliken_values_by_index,
    parse_abacus_mulliken_text,
    select_mulliken_step,
)


SAMPLE_VESTA = """#VESTA_FORMAT_VERSION 3.5.4

CRYSTAL

TITLE
test

STRUC
   1  Fe        Fe1          1.0000   0.000000   0.000000   0.000000    1a     1
                            0.000000   0.000000   0.000000  0.00
   2  Fe        Fe2          1.0000   0.500000   0.500000   0.500000    1a     1
                            0.000000   0.000000   0.000000  0.00
  0 0 0 0 0 0 0
SITET
   1          Fe1  1.0000 200 200 200 200 200 200 204  0
   2          Fe2  1.0000 200 200 200 200 200 200 204  0
  0 0 0 0 0 0
ATOMT
  1         Fe  1.0000 180 180 180 180 180 180 204
  0 0 0 0 0 0
STYLE
BONDS   0
"""


NSPIN1_MULLIKEN = """ --- Ionic Step 1 ---
 Total charge 2
 Decomposed Mulliken population analysis for each atom

 ------------------
 Atom 1 is H
 ------------------
       sum lmz    1.0000

 total charge    on atom 1     1.0000

 ------------------
 Atom 2 is H
 ------------------
       sum lmz    1.0000

 total charge    on atom 2     1.0000
"""


NSPIN2_MULLIKEN_TWO_STEPS = """ --- Ionic Step 1 ---
 Total charge 32
 Total charge of spin1 16
 Total charge of spin2 16

 ------------------
 Atom 1 is Fe
 ------------------
       sum lmz    9.9000    6.1000   16.0000    3.8000

 total charge    on atom 1    16.0000
 total magnetism on atom 1     3.8000

 ------------------
 Atom 2 is Fe
 ------------------
       sum lmz    6.1000    9.9000   16.0000   -3.8000

 total charge    on atom 2    16.0000
 total magnetism on atom 2    -3.8000

 --- Ionic Step 2 ---
 Total charge 32
 Total charge of spin1 16
 Total charge of spin2 16

 ------------------
 Atom 1 is Fe
 ------------------
       sum lmz   10.0000    6.0000   16.0000    4.0000

 total charge    on atom 1    16.5000
 total magnetism on atom 1     4.0000

 ------------------
 Atom 2 is Fe
 ------------------
       sum lmz    6.0000   10.0000   16.0000   -4.0000

 total charge    on atom 2    15.5000
 total magnetism on atom 2    -4.0000
"""


NSPIN4_MULLIKEN = """ --- Ionic Step 1 ---
 Total charge 32

 ------------------
 Atom 1 is Fe
 ------------------
       sum lmz   16.0000    1.1970   -0.1000    0.2000

 total charge    on atom 1    16.0000
 total magnetism on atom 1     1.1970    -0.1000     0.2000

 ------------------
 Atom 2 is Fe
 ------------------
       sum lmz   16.0000   -1.1970    0.1000   -0.2000

 total charge    on atom 2    16.0000
 total magnetism on atom 2    -1.1970     0.1000    -0.2000
"""


THREE_ATOM_MULLIKEN = """ --- Ionic Step 1 ---
 Total charge 3

 ------------------
 Atom 1 is Fe
 ------------------
 total charge    on atom 1     1.0000

 ------------------
 Atom 2 is Fe
 ------------------
 total charge    on atom 2     1.0000

 ------------------
 Atom 3 is Fe
 ------------------
 total charge    on atom 3     1.0000
"""


LEGACY_MULLIKEN = """STEP: 0
CALCULATE THE MULLIkEN ANALYSIS FOR EACH ATOM
0                 Zeta of Si                        Spin 1
Total Charge on atom:  Si                   4
1                 Zeta of Si                        Spin 1
Total Charge on atom:  Si                   3.5
"""


class TestAbacusMulliken(unittest.TestCase):
    def test_parse_nspin1_charges(self):
        steps = parse_abacus_mulliken_text(NSPIN1_MULLIKEN)

        self.assertEqual(len(steps), 1)
        self.assertEqual([atom.index for atom in steps[0].atoms], [1, 2])
        self.assertEqual([atom.label for atom in steps[0].atoms], ["H", "H"])
        self.assertEqual(mulliken_values_by_index(steps[0], "charge"), {1: 1.0, 2: 1.0})

    def test_selects_last_step_by_default_and_reads_spin2_magnetism(self):
        steps = parse_abacus_mulliken_text(NSPIN2_MULLIKEN_TWO_STEPS)
        selected = select_mulliken_step(steps)

        self.assertEqual(selected.step, 2)
        self.assertEqual(mulliken_values_by_index(selected, "charge"), {1: 16.5, 2: 15.5})
        self.assertEqual(mulliken_values_by_index(selected, "magnetism"), {1: 4.0, 2: -4.0})

        with self.assertRaisesRegex(ValueError, "magnetism-z requires nspin=4"):
            mulliken_values_by_index(selected, "magnetism-z")

    def test_can_select_exact_step(self):
        steps = parse_abacus_mulliken_text(NSPIN2_MULLIKEN_TWO_STEPS)

        selected = select_mulliken_step(steps, step=1)

        self.assertEqual(selected.step, 1)
        self.assertEqual(mulliken_values_by_index(selected, "magnetism"), {1: 3.8, 2: -3.8})

    def test_parse_nspin4_vector_magnetism_components_and_norm(self):
        step = parse_abacus_mulliken_text(NSPIN4_MULLIKEN)[0]

        self.assertEqual(mulliken_values_by_index(step, "magnetism-x"), {1: 1.197, 2: -1.197})
        self.assertEqual(mulliken_values_by_index(step, "magnetism-y"), {1: -0.1, 2: 0.1})
        self.assertEqual(mulliken_values_by_index(step, "magnetism-z"), {1: 0.2, 2: -0.2})
        self.assertAlmostEqual(mulliken_values_by_index(step, "magnetism-norm")[1], (1.197**2 + 0.1**2 + 0.2**2) ** 0.5)

        with self.assertRaisesRegex(ValueError, "Vector Mulliken magnetism"):
            mulliken_values_by_index(step, "magnetism")

    def test_parses_legacy_documentation_format(self):
        step = parse_abacus_mulliken_text(LEGACY_MULLIKEN)[0]

        self.assertEqual(step.step, 0)
        self.assertEqual(mulliken_values_by_index(step, "charge"), {1: 4.0, 2: 3.5})

    def test_color_vesta_from_mulliken_patches_by_atom_index_and_writes_values_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_vesta = root / "input.vesta"
            mulliken = root / "mulliken.txt"
            output_vesta = root / "colored.vesta"
            values_csv = root / "values.csv"
            input_vesta.write_text(SAMPLE_VESTA, encoding="utf-8")
            mulliken.write_text(NSPIN2_MULLIKEN_TWO_STEPS, encoding="utf-8")

            selected = color_vesta_from_mulliken(
                input_vesta,
                mulliken,
                output_vesta,
                property_name="magnetism",
                vmin=-4.0,
                vmax=4.0,
                values_csv=values_csv,
            )

            text = output_vesta.read_text(encoding="utf-8")
            csv_text = values_csv.read_text(encoding="utf-8")

            self.assertEqual(selected.step, 2)
            self.assertIn("   1          Fe1  1.0000 203  24  29 203  24  29 204 0\n", text)
            self.assertIn("   2          Fe2  1.0000  49 130 189  49 130 189 204 0\n", text)
            self.assertIn("index,label,value,charge,magnetism_x,magnetism_y,magnetism_z", csv_text)
            self.assertIn("1,Fe,4,16.5,4", csv_text)
            self.assertIn("2,Fe,-4,15.5,-4", csv_text)

    def test_strict_coloring_rejects_surplus_mulliken_atoms(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_vesta = root / "input.vesta"
            mulliken = root / "mulliken.txt"
            output_vesta = root / "colored.vesta"
            input_vesta.write_text(SAMPLE_VESTA, encoding="utf-8")
            mulliken.write_text(THREE_ATOM_MULLIKEN, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "requires VESTA STRUC site indices"):
                color_vesta_from_mulliken(input_vesta, mulliken, output_vesta)

            self.assertFalse(output_vesta.exists())


if __name__ == "__main__":
    unittest.main()
