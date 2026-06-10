import tempfile
import unittest
from pathlib import Path

from multiwfn2vesta.multiwfn_atom_table import (
    color_vesta_from_multiwfn_atom_table,
    parse_multiwfn_atom_table_text,
)


SAMPLE_VESTA = """#VESTA_FORMAT_VERSION 3.5.4

CRYSTAL

TITLE
test

STRUC
   1  H         H1           1.0000   0.000000   0.000000   0.000000    1a     1
                            0.000000   0.000000   0.000000  0.00
   2  O         O1           1.0000   0.500000   0.500000   0.500000    1a     1
                            0.000000   0.000000   0.000000  0.00
   3  H         H2           1.0000   0.250000   0.250000   0.250000    1a     1
                            0.000000   0.000000   0.000000  0.00
  0 0 0 0 0 0 0
SITET
   1           H1  0.3200 200 200 200 200 200 200 204  0
   2           O1  0.7400 200 200 200 200 200 200 204  0
   3           H2  0.3200 200 200 200 200 200 200 204  0
  0 0 0 0 0 0
ATOMT
  1          H  0.3200 255 255 255 255 255 255 204
  2          O  0.7400 255   0   0 255   0   0 204
  0 0 0 0 0 0
STYLE
BONDS   0
"""


class TestMultiwfnAtomTable(unittest.TestCase):
    def test_parse_headered_multiwfn_like_whitespace_table(self):
        table = parse_multiwfn_atom_table_text(
            """
            Atom   Label   Mulliken_charge   Hirshfeld
            1      H1      0.25              0.10
            2      O1     -0.50             -0.20
            3      H2      0.25              0.10
            """,
            value_column="Mulliken_charge",
        )

        self.assertEqual(table.key_mode, "index")
        self.assertEqual(table.value_column, "Mulliken_charge")
        self.assertEqual(table.values, {1: 0.25, 2: -0.5, 3: 0.25})
        self.assertEqual(table.rows[0], (1, "H1", 0.25))

    def test_parse_headered_csv_with_explicit_label_key(self):
        table = parse_multiwfn_atom_table_text(
            "site_label,charge,fukui_plus\nH1,0.2,0.01\nO1,-0.4,0.08\nH2,0.2,0.01\n",
            value_column="fukui_plus",
            key_column="site_label",
        )

        self.assertEqual(table.key_mode, "label")
        self.assertEqual(table.key_column, "site_label")
        self.assertEqual(table.values, {"H1": 0.01, "O1": 0.08, "H2": 0.01})

    def test_multiple_candidate_value_columns_require_explicit_choice(self):
        with self.assertRaisesRegex(ValueError, "Multiple possible value columns"):
            parse_multiwfn_atom_table_text(
                "Atom Label Charge Fukui_plus\n1 H1 -0.2 0.01\n2 O1 0.4 0.08\n"
            )

    def test_parse_one_column_as_ordered_values(self):
        table = parse_multiwfn_atom_table_text("-0.2\n0.4\n-0.2\n")

        self.assertEqual(table.key_mode, "ordered")
        self.assertEqual(table.values, [-0.2, 0.4, -0.2])

    def test_parse_unheadered_index_label_value_table(self):
        table = parse_multiwfn_atom_table_text("1 H1 -0.2\n2 O1 0.4\n3 H2 -0.2\n")

        self.assertEqual(table.key_mode, "index")
        self.assertEqual(table.values, {1: -0.2, 2: 0.4, 3: -0.2})
        self.assertEqual(table.rows[0], (1, "H1", -0.2))

    def test_color_vesta_from_table_patches_by_index_and_writes_values_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_vesta = root / "input.vesta"
            table_path = root / "charges.txt"
            output_vesta = root / "colored.vesta"
            values_csv = root / "values.csv"
            input_vesta.write_text(SAMPLE_VESTA, encoding="utf-8")
            table_path.write_text(
                "Atom Label Charge\n1 H1 -0.5\n2 O1 0.0\n3 H2 0.5\n",
                encoding="utf-8",
            )

            table = color_vesta_from_multiwfn_atom_table(
                input_vesta,
                table_path,
                output_vesta,
                value_column="Charge",
                vmin=-0.5,
                vmax=0.5,
                values_csv=values_csv,
            )

            text = output_vesta.read_text(encoding="utf-8")
            csv_text = values_csv.read_text(encoding="utf-8")
            self.assertEqual(table.key_mode, "index")
            self.assertIn("   1           H1  0.3200  49 130 189  49 130 189 204 0\n", text)
            self.assertIn("   2           O1  0.7400 247 247 247 247 247 247 204 0\n", text)
            self.assertIn("   3           H2  0.3200 203  24  29 203  24  29 204 0\n", text)
            self.assertIn("index,label,value", csv_text)
            self.assertIn("1,H1,-0.5", csv_text)

    def test_strict_index_table_accepts_shuffled_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_vesta = root / "input.vesta"
            table_path = root / "charges.txt"
            output_vesta = root / "colored.vesta"
            input_vesta.write_text(SAMPLE_VESTA, encoding="utf-8")
            table_path.write_text("Atom Charge\n3 0.5\n1 -0.5\n2 0.0\n", encoding="utf-8")

            color_vesta_from_multiwfn_atom_table(
                input_vesta,
                table_path,
                output_vesta,
                value_column="Charge",
                vmin=-0.5,
                vmax=0.5,
            )

            text = output_vesta.read_text(encoding="utf-8")
            self.assertIn("   1           H1  0.3200  49 130 189  49 130 189 204 0\n", text)
            self.assertIn("   2           O1  0.7400 247 247 247 247 247 247 204 0\n", text)
            self.assertIn("   3           H2  0.3200 203  24  29 203  24  29 204 0\n", text)

    def test_strict_index_table_rejects_wrong_atom_indices(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_vesta = root / "input.vesta"
            table_path = root / "charges.txt"
            output_vesta = root / "colored.vesta"
            input_vesta.write_text(SAMPLE_VESTA, encoding="utf-8")
            table_path.write_text("Atom Charge\n1 -0.5\n3 0.0\n4 0.5\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "requires table atom indices"):
                color_vesta_from_multiwfn_atom_table(input_vesta, table_path, output_vesta)

            self.assertFalse(output_vesta.exists())

    def test_strict_index_table_rejects_duplicate_indices(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_vesta = root / "input.vesta"
            table_path = root / "charges.txt"
            output_vesta = root / "colored.vesta"
            input_vesta.write_text(SAMPLE_VESTA, encoding="utf-8")
            table_path.write_text("Atom Charge\n1 -0.5\n1 0.0\n3 0.5\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "duplicate atom indices"):
                color_vesta_from_multiwfn_atom_table(input_vesta, table_path, output_vesta)

    def test_strict_ordered_table_rejects_wrong_length(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_vesta = root / "input.vesta"
            table_path = root / "values.txt"
            output_vesta = root / "colored.vesta"
            input_vesta.write_text(SAMPLE_VESTA, encoding="utf-8")
            table_path.write_text("-0.5\n0.5\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "ordered table length"):
                color_vesta_from_multiwfn_atom_table(input_vesta, table_path, output_vesta)

    def test_missing_explicit_value_column_fails_stably(self):
        with self.assertRaisesRegex(ValueError, "Column 'not_here' was not found"):
            parse_multiwfn_atom_table_text("Atom Charge\n1 0.2\n", value_column="not_here")


if __name__ == "__main__":
    unittest.main()
