import io
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.abacus_esp_align import align_cube, main, planar_average
from multiwfn2vesta.cube_vesta import _iter_cube_data_values


ESP_CUBE = """test cube
potential
    1     0.000000     0.000000     0.000000
    2     1.000000     0.000000     0.000000
    2     0.000000     1.000000     0.000000
    2     0.000000     0.000000     1.000000
    1     1.000000     0.000000     0.000000     0.000000
  1.0 3.0 2.0 4.0 3.0 5.0 4.0 6.0
"""


class TestAbacusEspAlign(unittest.TestCase):
    def write_tmp(self, root, name, text):
        path = Path(root) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def read_values(self, path):
        return list(_iter_cube_data_values(Path(path)))

    def test_planar_average_uses_cube_z_inner_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            cube = self.write_tmp(tmp, "esp.cube", ESP_CUBE)
            profile, data_min, data_max, count = planar_average(cube, axis="z")

            self.assertEqual(profile.counts, [4, 4])
            self.assertEqual(profile.means, [2.5, 4.5])
            self.assertEqual(data_min, 1.0)
            self.assertEqual(data_max, 6.0)
            self.assertEqual(count, 8)

    def test_committed_sample_esp_alignment_matches_expected_outputs(self):
        source = Path(__file__).resolve().parents[1] / "examples" / "cof_direct_cube_suite" / "sample_esp"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sample_esp"
            shutil.copytree(source, root)
            out = root / "potes_demo_vacuum0.cube"
            profile_csv = root / "potes_demo_profile.csv"
            report_md = root / "potes_demo_alignment.md"
            expected_cube = out.read_text(encoding="utf-8")
            expected_profile = profile_csv.read_text(encoding="utf-8")

            result = align_cube(
                root / "potes_demo.cube",
                out,
                axis="z",
                vacuum_side="high",
                vacuum_fraction=0.5,
                profile_csv=profile_csv,
                report_md=report_md,
            )

            self.assertEqual(result.vacuum_offset, 4.5)
            self.assertEqual(result.vacuum_start, 1)
            self.assertEqual(result.vacuum_end, 2)
            self.assertEqual(out.read_text(encoding="utf-8"), expected_cube)
            self.assertEqual(profile_csv.read_text(encoding="utf-8"), expected_profile)
            self.assertIn("subtracted_offset: `4.500000000000E+00`", report_md.read_text(encoding="utf-8"))

    def test_align_cube_subtracts_high_vacuum_plateau(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "esp.cube", ESP_CUBE)
            out = root / "esp_vacuum0.cube"
            profile_csv = root / "profile.csv"
            report_md = root / "report.md"

            result = align_cube(
                cube,
                out,
                axis="z",
                vacuum_side="high",
                vacuum_fraction=0.5,
                profile_csv=profile_csv,
                report_md=report_md,
            )

            self.assertEqual(result.vacuum_offset, 4.5)
            self.assertEqual(result.vacuum_start, 1)
            self.assertEqual(result.vacuum_end, 2)
            self.assertEqual(result.data_min_after, -3.5)
            self.assertEqual(result.data_max_after, 1.5)
            self.assertEqual(self.read_values(out), [-3.5, -1.5, -2.5, -0.5, -1.5, 0.5, -0.5, 1.5])
            self.assertIn("plane_index,z_plane_average", profile_csv.read_text(encoding="utf-8"))
            self.assertIn("subtracted_offset", report_md.read_text(encoding="utf-8"))

    def test_main_reports_alignment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "esp.cube", ESP_CUBE)
            out = root / "shifted.cube"
            stdout = io.StringIO()

            with patch("sys.stdout", stdout):
                exit_code = main([str(cube), str(out), "--axis", "z", "--vacuum-side", "high", "--vacuum-fraction", "0.5"])

            self.assertEqual(exit_code, 0)
            self.assertTrue(out.exists())
            self.assertIn("Subtracted vacuum offset: 4.500000000000E+00", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
