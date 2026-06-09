import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.molden_check import check_molden_file, main


ABACUS_MOLDEN = """[Molden Format]
[Cell]
  4.0 0.0 0.0
  0.0 4.0 0.0
  0.0 0.0 12.0
[Atoms] AU
C 1 6 0.0 0.0 0.0
H 2 1 0.0 0.0 1.8
[Nval]
C 4
H 1
[GTO]
1 0
s 1 1.00
  1.0 1.0
[5D7F]
[MO]
 Sym= A1
 Ene= -0.500
 Spin= Alpha
 Occup= 2.000
  1 0.100
"""


GENERIC_MOLDEN = """[Molden Format]
[Atoms] AU
H 1 1 0.0 0.0 0.0
H 2 1 0.0 0.0 1.4
[GTO]
1 0
s 1 1.00
  1.0 1.0
[MO]
 Sym= A1
 Ene= -0.300
 Spin= Alpha
 Occup= 2.000
  1 0.200
"""


class TestMoldenCheck(unittest.TestCase):
    def write_tmp(self, text):
        tmp = tempfile.TemporaryDirectory()
        path = Path(tmp.name) / "input.molden"
        path.write_text(text, encoding="utf-8")
        self.addCleanup(tmp.cleanup)
        return path

    def test_abacus_molden_with_cell_and_nval_passes(self):
        path = self.write_tmp(ABACUS_MOLDEN)

        result = check_molden_file(path, abacus=True)

        self.assertTrue(result.ok)
        self.assertEqual(result.atoms_count, 2)
        self.assertEqual(result.mo_count, 1)
        self.assertEqual(result.cell_numeric_rows, 3)
        self.assertEqual(result.nval_entries, [("C", 4.0), ("H", 1.0)])

    def test_abacus_molden_requires_nval(self):
        path = self.write_tmp(ABACUS_MOLDEN.replace("[Nval]\nC 4\nH 1\n", ""))

        result = check_molden_file(path, abacus=True)

        self.assertFalse(result.ok)
        self.assertIn("Missing [Nval]", "\n".join(result.errors))

    def test_abacus_molden_without_sym_still_counts_mo_blocks(self):
        path = self.write_tmp(ABACUS_MOLDEN.replace(" Sym= A1\n", ""))

        result = check_molden_file(path, abacus=True)

        self.assertTrue(result.ok)
        self.assertEqual(result.mo_count, 1)

    def test_generic_molden_does_not_require_cell_or_nval(self):
        path = self.write_tmp(GENERIC_MOLDEN)

        result = check_molden_file(path)

        self.assertTrue(result.ok)
        self.assertEqual(result.atoms_count, 2)

    def test_main_returns_failure_for_abacus_missing_nval(self):
        path = self.write_tmp(GENERIC_MOLDEN)
        output = io.StringIO()

        with patch("sys.stdout", output):
            code = main([str(path), "--abacus"])

        self.assertEqual(code, 1)
        self.assertIn("Result: FAILED", output.getvalue())
        self.assertIn("Missing [Cell]", output.getvalue())
        self.assertIn("Missing [Nval]", output.getvalue())


if __name__ == "__main__":
    unittest.main()
