import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.aim_igmh_vesta import (
    build_three_view_command,
    collect_cube_references,
    compass_to_comps,
    run_workflow,
)


SAMPLE_OVERLAY = """\
#VESTA_FORMAT_VERSION 3.5.4
CRYSTAL
TITLE
base
IMPORT_DENSITY 1
+1.000000 dg_inter.cub
IMPORT_TEXTURE
+1.000000 sl2r.cub
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


class TestAimIgmhVestaWorkflow(unittest.TestCase):
    def test_collect_cube_references_finds_density_and_texture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            refs = collect_cube_references(SAMPLE_OVERLAY, root, root / "out")

        self.assertEqual([ref.kind for ref in refs], ["IMPORT_DENSITY", "IMPORT_TEXTURE"])
        self.assertEqual([ref.raw_path for ref in refs], ["dg_inter.cub", "sl2r.cub"])
        self.assertTrue(all(ref.is_relative for ref in refs))

    def test_run_workflow_styles_overlay_copies_cubes_and_writes_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "input.vesta"
            source.write_text(SAMPLE_OVERLAY, encoding="utf-8")
            (root / "dg_inter.cub").write_text("density", encoding="utf-8")
            (root / "sl2r.cub").write_text("texture", encoding="utf-8")

            result = run_workflow(source, root / "products", stem="ag_case")

            styled = result.styled_vesta.read_text(encoding="utf-8")
            manifest = result.manifest.read_text(encoding="utf-8")
            density_copied = (root / "products" / "dg_inter.cub").exists()
            texture_copied = (root / "products" / "sl2r.cub").exists()

            self.assertIn("  Xe        P0001_0001", styled)
            self.assertIn("  Rn        CP0001_N", styled)
            self.assertIn("P0001_0001  0.0600 255 230   0 255 230   0 204", styled)
            self.assertIn("CP0001_N  0.1800 255  80   0 255  80   0 204", styled)
            self.assertIn("AIM BCP final overlay phase", styled)
            self.assertNotIn("0.02200", styled)
            self.assertTrue(density_copied)
            self.assertTrue(texture_copied)
            self.assertIn("path_element: `Xe`", manifest)
            self.assertIn("split_bcp_phase: `True`", manifest)
            self.assertIn("render_requested: `False`", manifest)
            self.assertIn("does not delete points", manifest)

    def test_run_workflow_builds_render_command_only_when_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "input.vesta"
            source.write_text(SAMPLE_OVERLAY, encoding="utf-8")

            with patch("multiwfn2vesta.aim_igmh_vesta.subprocess.run") as mocked_run:
                result = run_workflow(
                    source,
                    root / "products",
                    stem="ag_case",
                    render_three_views=True,
                    label_bcp_sites=True,
                )

            command = result.render_command

        self.assertIsNotNone(command)
        self.assertEqual(mocked_run.call_count, 1)
        self.assertTrue(mocked_run.call_args.kwargs["cwd"].endswith("multiwfn2vesta"))
        self.assertEqual(command.count("--extra-rotate"), 1)
        self.assertIn("--add-compass", command)
        self.assertIn("--comps", command)
        self.assertIn("off", command)
        self.assertIn("--initial-view", command)
        self.assertIn("top", command)

    def test_build_three_view_command_keeps_one_session_renderer_contract(self):
        command = build_three_view_command(
            Path("styled.vesta"),
            Path("out"),
            stem="case",
            extra_rotate=(("top", "x", "-8"),),
        )

        self.assertIn("vesta_three_views.py", " ".join(command))
        self.assertNotIn("--mode scene-copies", " ".join(command))
        self.assertEqual(command.count("--extra-rotate"), 1)
        self.assertEqual(command[command.index("--mode") + 1], "cli-rotate")

    def test_compass_mode_maps_to_comps(self):
        self.assertEqual(compass_to_comps("post", None), "off")
        self.assertEqual(compass_to_comps("none", None), "off")
        self.assertEqual(compass_to_comps("native", None), "on")
        self.assertEqual(compass_to_comps("keep", None), "keep")
        self.assertEqual(compass_to_comps("post", "keep"), "keep")


if __name__ == "__main__":
    unittest.main()
