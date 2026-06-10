import tempfile
import unittest
from pathlib import Path

from multiwfn2vesta.cube_vesta import BOHR_TO_ANGSTROM, run_workflow
from multiwfn2vesta.surface_extrema_vesta import (
    overlay_surface_extrema_file,
    read_surfanalysis_pdb,
)


SURFACE_CUBE = """surface one
surface two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
  0.0 0.4 0.8 1.0 1.1 1.2 1.6 2.0
"""


SURFANALYSIS_PDB = """\
REMARK   Unit of B-factor field (ALIE) is eV
REMARK   Carbon: Surface maximum    Oxygen: surface minimum
HETATM    1  C   MOL A   1       0.000   0.529   0.265  1.00  2.50           C
HETATM    1  O   MOL A   1       0.500   1.000   0.000  1.00 -1.25           O
END
"""


class TestSurfaceExtremaVesta(unittest.TestCase):
    def write_tmp(self, root, name, text):
        path = Path(root) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_read_surfanalysis_pdb_maps_carbon_and_oxygen_extrema(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdb = self.write_tmp(tmp, "surfanalysis.pdb", SURFANALYSIS_PDB)

            parsed = read_surfanalysis_pdb(pdb)

        self.assertEqual(parsed.value_unit, "eV")
        self.assertEqual([item.kind for item in parsed.extrema], ["maximum", "minimum"])
        self.assertEqual([item.label for item in parsed.extrema], ["MAX0001", "MIN0001"])
        self.assertEqual([item.source_element for item in parsed.extrema], ["C", "O"])
        self.assertAlmostEqual(parsed.extrema[0].value, 2.50)
        self.assertAlmostEqual(parsed.extrema[1].value, -1.25)

    def test_overlay_extrema_inserts_phase_with_cube_origin_shift_and_no_comps(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "density.cub", SURFACE_CUBE)
            pdb = self.write_tmp(root, "surfanalysis.pdb", SURFANALYSIS_PDB)
            base = run_workflow(cube, root / "products", isosurface=0.8, stem="surface")
            output = root / "products" / "surface_extrema.vesta"

            result = overlay_surface_extrema_file(
                base.vesta_path,
                pdb,
                output,
                surface_cube=cube,
                selection="all",
                label_extrema=True,
            )
            text = output.read_text(encoding="utf-8")

        self.assertEqual(result.extrema_count, 2)
        self.assertEqual(result.maxima_count, 1)
        self.assertEqual(result.minima_count, 1)
        self.assertIn("Multiwfn surface extrema", text)
        self.assertIn("MAX0001", text)
        self.assertIn("MIN0001", text)
        self.assertIn("COMPS 0", text)
        self.assertRegex(text, r"MAX0001\s+0\.1000\s+255\s+0\s+0")
        self.assertRegex(text, r"MIN0001\s+0\.1000\s+0\s+0\s+255")
        max_line = next(line for line in text.splitlines() if "MAX0001" in line and "1.0000" in line)
        fields = max_line.split()
        self.assertAlmostEqual(float(fields[4]), BOHR_TO_ANGSTROM, places=5)
        self.assertAlmostEqual(float(fields[5]), 0.529 + 2.0 * BOHR_TO_ANGSTROM, places=5)
        self.assertAlmostEqual(float(fields[6]), 0.265 - 0.5 * BOHR_TO_ANGSTROM, places=5)

    def test_overlay_selection_can_keep_only_minima(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "density.cub", SURFACE_CUBE)
            pdb = self.write_tmp(root, "surfanalysis.pdb", SURFANALYSIS_PDB)
            base = run_workflow(cube, root / "products", isosurface=0.8, stem="surface")
            output = root / "products" / "surface_minima.vesta"

            result = overlay_surface_extrema_file(
                base.vesta_path,
                pdb,
                output,
                surface_cube=cube,
                selection="minima",
            )
            text = output.read_text(encoding="utf-8")

        self.assertEqual(result.extrema_count, 1)
        self.assertEqual(result.maxima_count, 0)
        self.assertEqual(result.minima_count, 1)
        self.assertNotIn("MAX0001", text)
        self.assertIn("MIN0001", text)


if __name__ == "__main__":
    unittest.main()
