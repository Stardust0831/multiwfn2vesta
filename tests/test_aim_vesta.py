import tempfile
import unittest
from pathlib import Path

from multiwfn2vesta.aim_vesta import convert_aim_pdb_to_vesta, read_pdb_points
from multiwfn2vesta.vesta_aim_style import inject_aim_atom_types_text
from multiwfn2vesta.vesta_parser import parse_vesta_text


PATHS_PDB = """\
HETATM    1  C   PTH A   1       0.000   0.000   0.000  1.00  0.00           C
HETATM    2  C   PTH A   1       0.100   0.000   0.000  1.00  0.00           C
TER
HETATM    3  C   PTH A   2       1.000   1.000   0.000  1.00  0.00           C
TER
"""

SKEWED_CELL_PATHS_PDB = """\
CRYST1   10.000   10.000   10.000  90.00  90.00  60.00
HETATM    1  C   PTH A   1       5.000   8.660   0.000  1.00  0.00           C
TER
"""

CP_PDB = """\
REMARK   C=(3,-3) N=(3,-1) O=(3,+1) F=(3,+3)
HETATM    1  C   CPS A   1       0.000   0.000   0.119  1.00  0.00           C
HETATM    2  N   CPS A   1       0.000   0.603  -0.360  1.00  0.00           N
HETATM    3  O   CPS A   1       0.000   0.000   0.000  1.00  0.00           O
HETATM    4  F   CPS A   1       0.000   0.000   1.000  1.00  0.00           F
"""

NONPERIODIC_PATHS_PDB = """\
HETATM    1  C   PTH A   1      -0.500   0.603  -0.360  1.00  0.00           C
TER
"""


class TestAimVesta(unittest.TestCase):
    def test_read_pdb_points_preserves_path_residue_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "paths.pdb"
            path.write_text(PATHS_PDB, encoding="utf-8")

            points, cell = read_pdb_points(path)

        self.assertIsNone(cell)
        self.assertEqual([point.resseq for point in points], [1, 1, 2])
        self.assertEqual([(point.x, point.y, point.z) for point in points][1], (0.1, 0.0, 0.0))

    def test_read_pdb_points_accepts_loose_split_coordinates(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "loose_paths.pdb"
            path.write_text("HETATM 4 CP 2.250 1.000 0.350\n", encoding="utf-8")

            points, _ = read_pdb_points(path)

        self.assertEqual(len(points), 1)
        self.assertEqual((points[0].x, points[0].y, points[0].z), (2.25, 1.0, 0.35))

    def test_convert_paths_to_vesta_disables_bonds_and_writes_sites(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = Path(tmp) / "paths.pdb"
            output = Path(tmp) / "paths.vesta"
            paths.write_text(PATHS_PDB, encoding="utf-8")

            convert_aim_pdb_to_vesta(paths, output, title="AIM test")
            text = output.read_text(encoding="utf-8")
            document = parse_vesta_text(text)

        self.assertIn("TITLE\nAIM test\n", text)
        self.assertEqual(document.section("SBOND").nonblank_body_lines, ["  0 0 0 0\n"])
        self.assertEqual(document.section("BONDS").args, ["0"])
        self.assertNotIn("BONDS   1\n", text)
        self.assertNotIn(" C     C ", text)
        self.assertIn("P0001_0001", text)
        self.assertIn("P0001_0002", text)
        self.assertIn("P0002_0001", text)
        self.assertEqual(text.count("  0 0 0 0 0 0 0"), 1)

    def test_nonperiodic_paths_write_molecule_with_raw_cartesian_coordinates(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = Path(tmp) / "paths.pdb"
            output = Path(tmp) / "paths.vesta"
            paths.write_text(NONPERIODIC_PATHS_PDB, encoding="utf-8")

            convert_aim_pdb_to_vesta(paths, output)
            text = output.read_text(encoding="utf-8")

        self.assertIn("\nMOLECULE\n", text)
        self.assertNotIn("\nCRYSTAL\n", text)
        self.assertRegex(text, r"\s+1\.000000\s+1\.000000\s+1\.000000\s+90\.000000\s+90\.000000\s+90\.000000")
        site_line = next(line for line in text.splitlines() if "P0001_0001" in line and "1.0000" in line)
        fields = site_line.split()
        self.assertEqual(fields[-2:], ["1", "-"])
        self.assertAlmostEqual(float(fields[4]), -0.5, places=3)
        self.assertAlmostEqual(float(fields[5]), 0.603, places=3)
        self.assertAlmostEqual(float(fields[6]), -0.36, places=3)

    def test_convert_with_cps_writes_bcp_labels_and_styles(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = Path(tmp) / "paths.pdb"
            cps = Path(tmp) / "CPs.pdb"
            output = Path(tmp) / "aim.vesta"
            paths.write_text(PATHS_PDB, encoding="utf-8")
            cps.write_text(CP_PDB, encoding="utf-8")

            convert_aim_pdb_to_vesta(paths, output, cps_pdb=cps)
            text = output.read_text(encoding="utf-8")

        self.assertIn("CP0001_C", text)
        self.assertIn("CP0002_N", text)
        self.assertIn("  N         CP0002_N", text)
        self.assertRegex(text, r"P0001_0001\s+0\.0400\s+120\s+120\s+120")
        self.assertRegex(text, r"CP0001_C\s+0\.2000\s+184\s+0\s+184")
        self.assertRegex(text, r"CP0002_N\s+0\.3200\s+255\s+128\s+0")
        self.assertRegex(text, r"CP0003_O\s+0\.2000\s+255\s+255\s+0")
        self.assertRegex(text, r"CP0004_F\s+0\.2000\s+0\s+255\s+0")

    def test_convert_with_skewed_cryst1_uses_lattice_coordinates(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = Path(tmp) / "skewed_paths.pdb"
            output = Path(tmp) / "skewed.vesta"
            paths.write_text(SKEWED_CELL_PATHS_PDB, encoding="utf-8")

            convert_aim_pdb_to_vesta(paths, output)
            text = output.read_text(encoding="utf-8")

        self.assertIn(" 10.000000 10.000000 10.000000  90.000000  90.000000  60.000000", text)
        site_line = next(line for line in text.splitlines() if "P0001_0001" in line and "1.0000" in line)
        fields = site_line.split()
        self.assertAlmostEqual(float(fields[4]), 0.0, places=3)
        self.assertAlmostEqual(float(fields[5]), 1.0, places=3)
        self.assertAlmostEqual(float(fields[6]), 0.0, places=3)

    def test_inject_aim_atom_types_adds_missing_global_atomt_rows(self):
        text = """\
ATOMT
  1          O  0.2600 254   3   0 254   3   0 204
  2          H  0.1600 255 204 204 255 204 204 204
  0 0 0 0 0 0
"""

        patched = inject_aim_atom_types_text(text)

        self.assertIn("  3          C  0.0400 120 120 120 120 120 120 204", patched)
        self.assertIn("  4          N  0.3200 255 128   0 255 128   0 204", patched)
        self.assertIn("  5          F  0.2000   0 255   0   0 255   0 204", patched)
        self.assertEqual(patched.count("          O "), 1)


if __name__ == "__main__":
    unittest.main()
