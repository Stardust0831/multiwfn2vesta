import tempfile
import unittest
from pathlib import Path

import numpy as np

from multiwfn2vesta.cub import (
    process_iri_color_cube,
    transform_iri_color_values,
    vesta_percent_range_for_values,
)


class TestIriCubeProcessing(unittest.TestCase):
    def test_transform_iri_color_values_keeps_upper_tail_for_vesta_percent_scaling(self):
        values = np.array([-0.10, -0.03, 0.00, 0.01, 0.03, 0.10])

        transformed = transform_iri_color_values(values)

        np.testing.assert_allclose(
            transformed,
            np.array([-0.04, -0.03, 0.00, 0.02, 0.06, 0.20]),
        )

    def test_transform_iri_color_values_can_reproduce_old_upper_clip(self):
        values = np.array([-0.10, -0.03, 0.00, 0.01, 0.03, 0.10])

        transformed = transform_iri_color_values(values, upper=0.04)

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
                np.array([-0.04, -0.03, 0.00, 0.02, 0.06, 0.20]),
            )
            written = output_cube.read_text(encoding="utf-8")
            self.assertIn("comment one", written)
            self.assertIn("comment two", written)
            self.assertIn("    1     0.000000     0.000000     0.000000", written)
            self.assertIn("  -4.00000E-02", written)
            self.assertIn("   2.00000E-01", written)

    def test_vesta_percent_range_for_values_maps_physical_targets_to_percentages(self):
        sampled_values = np.array([-0.04, -0.0334954])

        lower, upper = vesta_percent_range_for_values(
            sampled_values,
            target_lower=-0.04,
            target_upper=0.04,
        )

        self.assertAlmostEqual(lower, 0.0, places=12)
        self.assertAlmostEqual(upper, 12.298988408203426, places=12)

    def test_vesta_percent_range_rejects_degenerate_values(self):
        with self.assertRaisesRegex(ValueError, "zero-span"):
            vesta_percent_range_for_values(np.array([0.1, 0.1]))

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
