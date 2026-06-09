import unittest

from multiwfn2vesta.vesta_aim_overlay_style import patch_aim_overlay_style_text


SAMPLE = """\
#VESTA_FORMAT_VERSION 3.5.4
CRYSTAL
TITLE
base
STRUC
   1  C         C1           1.0000   0.100000   0.200000   0.300000    1a     1
                            0.000000   0.000000   0.000000  0.00
  0 0 0 0 0 0 0
SBOND
  0 0 0 0
SITET
   1           C1  0.7700 128  73  41 128  73  41 204  0
  0 0 0 0 0 0
CRYSTAL
TITLE
aim
STRUC
   1  C         P0001_0001   1.0000   0.426201   0.426125   0.514607    1a     1
                            0.000000   0.000000   0.000000  0.00
   2  N         CP0001_N     1.0000   0.426201   0.426125   0.514607    1a     1
                            0.000000   0.000000   0.000000  0.00
  0 0 0 0 0 0 0
THERI 1
   1   P0001_0001 -0.000000
   2     CP0001_N -0.000000
  0 0 0
SHAPE
  0       0       0       0   0.000000  0   192   192   192   192
BOUND
     0        1         0        1         0        1
  0   0   0   0  0
SBOND
  1    Xe    Xe    0.00000    0.02200  0  1  1  0  1  0.220  2.000 255 230   0
  0 0 0 0
SITET
   1   P0001_0001  0.0550 255 230   0 255 230   0 204  0
   2     CP0001_N  0.0700 255 128   0 255 128   0 204  0
  0 0 0 0 0 0
ATOMT
  1          C  0.7700 128  73  41 128  73  41 204
  2          N  0.0700 255 128   0 255 128   0 204
  3         Xe  0.0550 255 230   0 255 230   0 204
  0 0 0 0 0 0
STYLE
BONDS   1
"""


class TestVestaAimOverlayStyle(unittest.TestCase):
    def test_patch_keeps_path_point_and_assigns_bcp_pseudo_element(self):
        patched = patch_aim_overlay_style_text(
            SAMPLE,
            path_element="Xe",
            bcp_element="Rn",
            bcp_radius=0.180,
            path_rgb=(255, 230, 0),
            bcp_rgb=(255, 80, 0),
        )

        self.assertIn("  Xe        P0001_0001", patched)
        self.assertIn("  Rn        CP0001_N", patched)
        self.assertIn("P0001_0001  0.0600 255 230   0 255 230   0 204", patched)
        self.assertIn("CP0001_N  0.1800 255  80   0 255  80   0 204", patched)
        self.assertIn("  3         Xe  0.0600 255 230   0 255 230   0 204", patched)
        self.assertIn("  4         Rn  0.1800 255  80   0 255  80   0 204", patched)
        self.assertIn("BONDS   1", patched)
        self.assertEqual(patched.count("  Xe        P0001_0001"), 1)
        self.assertIn("P0001_0001 -0.000000", patched)

    def test_patch_clears_aim_sbond_without_touching_base_sbond(self):
        patched = patch_aim_overlay_style_text(SAMPLE)

        self.assertNotIn("0.02200", patched)
        self.assertEqual(patched.count("SBOND"), 2)
        self.assertGreaterEqual(patched.count("  0 0 0 0"), 2)

    def test_split_bcp_phase_keeps_paths_and_moves_bcp_to_final_phase(self):
        patched = patch_aim_overlay_style_text(
            SAMPLE,
            path_element="Xe",
            bcp_element="Rn",
            path_radius=0.020,
            bcp_radius=0.350,
            split_bcp_phase=True,
        )

        self.assertEqual(patched.count("CRYSTAL"), 3)
        self.assertEqual(patched.count("  Xe        P0001_0001"), 1)
        self.assertEqual(patched.count("  Rn        CP0001_N"), 1)
        self.assertLess(patched.index("  Xe        P0001_0001"), patched.index("  Rn        CP0001_N"))
        self.assertIn("AIM BCP final overlay phase", patched)
        self.assertIn("CP0001_N  0.3500 255  80   0 255  80   0 204", patched)
        self.assertNotIn("P0001_0001  0.3500", patched)

    def test_split_bcp_phase_is_idempotent_for_already_split_file(self):
        once = patch_aim_overlay_style_text(SAMPLE, split_bcp_phase=True)
        twice = patch_aim_overlay_style_text(once, split_bcp_phase=True)

        self.assertEqual(twice.count("CRYSTAL"), 3)
        self.assertEqual(twice.count("  Xe        P0001_0001"), 1)
        self.assertEqual(twice.count("  Rn        CP0001_N"), 1)

    def test_label_bcp_sites_uses_short_site_labels(self):
        patched = patch_aim_overlay_style_text(
            SAMPLE,
            bcp_element="Rn",
            split_bcp_phase=True,
            label_bcp_sites=True,
            label_font_size=18,
            label_offset=0.650,
        )

        self.assertIn("  Rn        BCP1", patched)
        self.assertIn("   1         BCP1 -0.000000", patched)
        self.assertIn("   1         BCP1  0.1800 255  80   0 255  80   0 204  1", patched)
        self.assertIn("LABEL 1    18  0.650 0", patched)
        self.assertNotIn("  Rn        CP0001_N", patched)
        self.assertNotIn("CP0001_N  0.1800", patched)

    def test_label_bcp_sites_remains_style_patchable(self):
        once = patch_aim_overlay_style_text(SAMPLE, bcp_element="Rn", label_bcp_sites=True)
        twice = patch_aim_overlay_style_text(once, bcp_element="Rn", label_bcp_sites=True)

        self.assertEqual(twice.count("  Rn        BCP1"), 1)
        self.assertIn("BCP1  0.1800 255  80   0 255  80   0 204", twice)

    def test_label_bcp_sites_inserts_label_style_inside_style_block(self):
        sample_without_label = SAMPLE.replace("STYLE\nBONDS   1\n", "STYLE\nBONDS   1\nBKGRC\n 255 255 255\n")
        patched = patch_aim_overlay_style_text(
            sample_without_label,
            bcp_element="Rn",
            label_bcp_sites=True,
            label_mode=1,
            label_font_size=24,
        )

        self.assertIn("BONDS   1\nLABEL 1    24  1.000 0\nBKGRC", patched)
        self.assertTrue(patched.rstrip().endswith("255 255 255"))


if __name__ == "__main__":
    unittest.main()
