import tempfile
import unittest
from pathlib import Path

from multiwfn2vesta.vesta_atom_coloring import (
    blue_white_red,
    patch_vesta_atom_colors_text,
    read_site_values_table,
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


class TestVestaAtomColoring(unittest.TestCase):
    def test_blue_white_red_maps_negative_center_positive(self):
        self.assertEqual(blue_white_red(-1.0, vmin=-1.0, vmax=1.0), (49, 130, 189))
        self.assertEqual(blue_white_red(0.0, vmin=-1.0, vmax=1.0), (247, 247, 247))
        self.assertEqual(blue_white_red(1.0, vmin=-1.0, vmax=1.0), (203, 24, 29))

    def test_patch_ordered_values_updates_sitet_rgb_only(self):
        patched = patch_vesta_atom_colors_text(SAMPLE_VESTA, [-1.0, 0.0, 1.0], vmin=-1.0, vmax=1.0)

        self.assertIn("   1           H1  0.3200  49 130 189  49 130 189 204 0\n", patched)
        self.assertIn("   2           O1  0.7400 247 247 247 247 247 247 204 0\n", patched)
        self.assertIn("   3           H2  0.3200 203  24  29 203  24  29 204 0\n", patched)
        self.assertIn("  1          H  0.3200 255 255 255 255 255 255 204\n", patched)
        self.assertIn("BONDS   0\n", patched)

    def test_patch_label_values_with_auto_symmetric_range(self):
        patched = patch_vesta_atom_colors_text(SAMPLE_VESTA, {"H1": -0.3, "O1": 0.0, "H2": 0.3})

        self.assertIn(" 49 130 189  49 130 189", patched)
        self.assertIn("247 247 247 247 247 247", patched)
        self.assertIn("203  24  29 203  24  29", patched)

    def test_patch_index_values_can_be_partial_when_non_strict(self):
        patched = patch_vesta_atom_colors_text(
            SAMPLE_VESTA,
            {2: 1.0},
            vmin=-1.0,
            vmax=1.0,
            strict=False,
        )

        self.assertIn("   1           H1  0.3200 200 200 200 200 200 200 204  0\n", patched)
        self.assertIn("   2           O1  0.7400 203  24  29 203  24  29 204 0\n", patched)

    def test_patch_adds_missing_sitet_rows_from_atomt_radius(self):
        text = SAMPLE_VESTA.replace(
            "   3           H2  0.3200 200 200 200 200 200 200 204  0\n",
            "",
        )

        patched = patch_vesta_atom_colors_text(text, [-1.0, 0.0, 1.0], vmin=-1.0, vmax=1.0)

        self.assertIn("   3           H2  0.3200 203  24  29 203  24  29 204 0\n", patched)

    def test_strict_ordered_values_require_all_sites(self):
        with self.assertRaisesRegex(ValueError, "Expected 3 ordered values"):
            patch_vesta_atom_colors_text(SAMPLE_VESTA, [0.1, 0.2])

    def test_read_values_table_supports_one_column_and_keyed_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            one_col = Path(tmp) / "ordered.txt"
            one_col.write_text("-0.1\n0.0\n0.1\n", encoding="utf-8")
            self.assertEqual(read_site_values_table(one_col), [-0.1, 0.0, 0.1])

            keyed = Path(tmp) / "charges.csv"
            keyed.write_text("label,charge\nH1,-0.2\nO1,0.4\n", encoding="utf-8")
            self.assertEqual(read_site_values_table(keyed), {"H1": -0.2, "O1": 0.4})

            indexed = Path(tmp) / "charges.tsv"
            indexed.write_text("index\tvalue\n1\t-0.2\n2\t0.4\n", encoding="utf-8")
            self.assertEqual(read_site_values_table(indexed), {1: -0.2, 2: 0.4})


if __name__ == "__main__":
    unittest.main()
