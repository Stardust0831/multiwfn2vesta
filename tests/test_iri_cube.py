import tempfile
import unittest
from pathlib import Path

import numpy as np

from multiwfn2vesta.cub import process_iri_color_cube, transform_iri_color_values


class TestIriCubeProcessing(unittest.TestCase):
    def test_transform_iri_color_values_matches_old_multiwfn_sequence(self):
        values = np.array([-0.10, -0.03, 0.00, 0.01, 0.03, 0.10])

        transformed = transform_iri_color_values(values)

        np.testing.assert_allclose(
            transformed,
            np.array([-0.04, -0.03, 0.00, 0.02, 0.04, 0.04]),
        )

    def test_process_iri_color_cube_preserves_header_and_remaps_values(self):
        cube_text = """comment one
comment two
    1     0.000000     0.000000     0.000000
    2     1.000000     0.000000     0.000000
    1     0.000000     1.000000     0.000000
    3     0.000000     0.000000     1.000000
    6     6.000000     0.000000     0.000000     0.000000
  -0.10000E+00 -0.30000E-01  0.00000E+00  0.10000E-01  0.30000E-01  0.10000E+00
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_cube = Path(tmpdir) / "func1.cub"
            output_cube = Path(tmpdir) / "mapped.cub"
            input_cube.write_text(cube_text, encoding="utf-8")

            transformed = process_iri_color_cube(input_cube, output_cube)

            self.assertTrue(output_cube.exists())
            np.testing.assert_allclose(
                transformed.reshape(-1),
                np.array([-0.04, -0.03, 0.00, 0.02, 0.04, 0.04]),
            )
            written = output_cube.read_text(encoding="utf-8")
            self.assertIn("comment one", written)
            self.assertIn("comment two", written)
            self.assertIn("    1     0.000000     0.000000     0.000000", written)
            self.assertIn("  -4.00000E-02", written)
            self.assertIn("   4.00000E-02", written)

    def test_process_iri_color_cube_rejects_truncated_cube_by_default(self):
        cube_text = """comment one
comment two
    1     0.000000     0.000000     0.000000
    2     1.000000     0.000000     0.000000
    1     0.000000     1.000000     0.000000
    3     0.000000     0.000000     1.000000
    6     6.000000     0.000000     0.000000     0.000000
  -0.10000E+00 -0.30000E-01  0.00000E+00
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_cube = Path(tmpdir) / "func1.cub"
            output_cube = Path(tmpdir) / "mapped.cub"
            input_cube.write_text(cube_text, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Cube data point count mismatch"):
                process_iri_color_cube(input_cube, output_cube)

            self.assertFalse(output_cube.exists())


if __name__ == "__main__":
    unittest.main()
