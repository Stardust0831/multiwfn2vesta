import tempfile
import unittest
from pathlib import Path

from multiwfn2vesta.cube_vesta import (
    BOHR_TO_ANGSTROM,
    _read_cube_summary,
    _structure_mode,
    run_workflow,
)


MOLECULE_CUBE = """comment one
comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
  0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7
"""


SIGNED_CUBE = """signed comment one
signed comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -0.3 -0.2 -0.1 0.0 0.1 0.2 0.3 0.4
"""


TEXTURE_CUBE = """texture one
texture two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -0.10 -0.05 0.0 0.05 0.10 0.15 0.20 0.30
"""


PERIODIC_CUBE = """periodic
cell
    2     0.000000     0.000000     0.000000
    2     1.000000     0.000000     0.000000
    2     0.000000     1.000000     0.000000
    2     0.000000     0.000000     1.000000
    8     8.000000     0.000000     0.000000     0.000000
    1     1.000000     1.000000     1.000000     1.000000
  0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7
"""


BAD_GRID_TEXTURE = """bad texture
bad grid
    1    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    3     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
  0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.1
"""


ZERO_SPAN_TEXTURE = """zero texture
zero span
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
  0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1
"""


class TestCubeVesta(unittest.TestCase):
    def write_tmp(self, root, name, text):
        path = Path(root) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_single_cube_generates_vesta_with_sections_off_and_structure_phase(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "surface.cub", MOLECULE_CUBE)

            result = run_workflow(cube, root / "products", isosurface=0.3, stem="case")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("IMPORT_DENSITY 1", text)
            self.assertIn("+1.000000 surface.cub", text)
            self.assertNotIn("IMPORT_TEXTURE", text)
            self.assertIn("SURFS   0  1  1", text)
            self.assertIn("SECTS   0  0", text)
            self.assertIn("ISURF\n  1   1        0.3", text)
            self.assertIn("\nMOLECULE\n", text)
            self.assertIn(" O1", text)
            self.assertIn(" H1", text)
            self.assertIn("structure_phase: `molecule`", manifest)
            self.assertTrue((root / "products" / "surface.cub").exists())

    def test_texture_cube_uses_import_texture_and_percent_tex3p_not_physical_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface = self.write_tmp(root, "surface.cub", MOLECULE_CUBE)
            texture = self.write_tmp(root, "texture.cub", TEXTURE_CUBE)

            result = run_workflow(
                surface,
                root / "products",
                texture_cube=texture,
                isosurface=0.2,
                tex_physical=(-0.05, 0.05),
                stem="colored",
            )

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("IMPORT_TEXTURE", text)
            self.assertIn("+1.000000 texture.cub", text)
            self.assertIn("TEX3P\n  1  1.25000E-01  3.75000E-01", text)
            self.assertNotIn(" -5.00000E-02  5.00000E-02", text)
            self.assertIn("tex_physical_range: `-0.05` to `0.05`", manifest)
            self.assertTrue((root / "products" / "surface.cub").exists())
            self.assertTrue((root / "products" / "texture.cub").exists())

    def test_surface_band_texture_scaling_uses_near_isosurface_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface = self.write_tmp(root, "surface.cub", MOLECULE_CUBE)
            texture = self.write_tmp(root, "texture.cub", TEXTURE_CUBE)

            result = run_workflow(
                surface,
                root / "products",
                texture_cube=texture,
                isosurface=0.2,
                tex_physical=(-0.05, 0.05),
                tex_range_source="surface-band",
                surface_band=0.11,
                stem="surface_band",
            )

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("TEX3P\n  1  0.00000E+00  1.00000E+00", text)
            self.assertIn("tex_reference_source: `surface-band`", manifest)
            self.assertIn("tex_reference_range: `-0.05` to `0.05`", manifest)
            self.assertIn("tex_reference_sample_count: `3`", manifest)
            self.assertIn("surface_band: `0.11`", manifest)

    def test_surface_band_texture_scaling_falls_back_to_nearest_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface = self.write_tmp(root, "surface.cub", MOLECULE_CUBE)
            texture = self.write_tmp(root, "texture.cub", TEXTURE_CUBE)

            result = run_workflow(
                surface,
                root / "products",
                texture_cube=texture,
                isosurface=0.2,
                tex_physical=(-0.05, 0.05),
                tex_range_source="surface-band",
                surface_band=0.0,
                surface_nearest=4,
                stem="nearest",
            )

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("TEX3P\n  1  3.33333E-01  1.00000E+00", text)
            self.assertIn("tex_reference_source: `surface-nearest`", manifest)
            self.assertIn("tex_reference_range: `-0.1` to `0.05`", manifest)
            self.assertIn("tex_reference_sample_count: `4`", manifest)
            self.assertIn("surface_nearest_fallback: `true`", manifest)

    def test_same_basename_surface_and_texture_cubes_do_not_overwrite_each_other(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface = self.write_tmp(root, "surface/same.cub", MOLECULE_CUBE)
            texture = self.write_tmp(root, "texture/same.cub", TEXTURE_CUBE)

            result = run_workflow(
                surface,
                root / "products",
                texture_cube=texture,
                isosurface=0.2,
                stem="same_name",
            )

            text = result.vesta_path.read_text(encoding="utf-8")
            copied_surface = root / "products" / "same.cub"
            copied_texture = root / "products" / "same_texture.cub"

            self.assertIn("+1.000000 same.cub", text)
            self.assertIn("+1.000000 same_texture.cub", text)
            self.assertEqual(copied_surface.read_text(encoding="utf-8"), MOLECULE_CUBE)
            self.assertEqual(copied_texture.read_text(encoding="utf-8"), TEXTURE_CUBE)
            self.assertEqual([destination.name for _, destination in result.copied_cubes], ["same.cub", "same_texture.cub"])

    def test_tex_physical_requires_texture_cube(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "surface.cub", MOLECULE_CUBE)

            with self.assertRaisesRegex(ValueError, "texture cube is required"):
                run_workflow(cube, root / "products", isosurface=0.2, tex_physical=(-0.1, 0.1))

    def test_tex_physical_rejects_zero_span_texture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface = self.write_tmp(root, "surface.cub", MOLECULE_CUBE)
            texture = self.write_tmp(root, "zero_texture.cub", ZERO_SPAN_TEXTURE)

            with self.assertRaisesRegex(ValueError, "zero-span texture"):
                run_workflow(
                    surface,
                    root / "products",
                    texture_cube=texture,
                    isosurface=0.2,
                    tex_physical=(-0.1, 0.1),
                )

    def test_rejects_incompatible_texture_grid_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface = self.write_tmp(root, "surface.cub", MOLECULE_CUBE)
            texture = self.write_tmp(root, "bad_texture.cub", BAD_GRID_TEXTURE)

            with self.assertRaisesRegex(ValueError, "not compatible"):
                run_workflow(surface, root / "products", texture_cube=texture, isosurface=0.2)

    def test_auto_structure_uses_crystal_for_origin_zero_fractional_atoms(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "periodic.cub", PERIODIC_CUBE)
            summary = _read_cube_summary(cube)

            self.assertEqual(_structure_mode(summary, "auto"), "crystal")

            result = run_workflow(cube, root / "products", isosurface=0.2, stem="periodic")
            text = result.vesta_path.read_text(encoding="utf-8")

        self.assertEqual(text.count("\nCRYSTAL\n"), 2)
        self.assertNotIn("\nMOLECULE\n", text)
        self.assertIn("0.500000   0.500000   0.500000    1a     1", text)

    def test_cube_units_auto_and_angstrom_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "surface.cub", MOLECULE_CUBE)

            auto_summary = _read_cube_summary(cube)
            angstrom_summary = _read_cube_summary(cube, cube_units="angstrom")

        self.assertEqual(auto_summary.unit, "bohr")
        self.assertAlmostEqual(auto_summary.unit_scale, BOHR_TO_ANGSTROM)
        self.assertEqual(angstrom_summary.unit, "angstrom")
        self.assertAlmostEqual(angstrom_summary.unit_scale, 1.0)

    def test_rejects_isosurface_outside_data_range(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "surface.cub", MOLECULE_CUBE)

            with self.assertRaisesRegex(ValueError, "outside surface cube data range"):
                run_workflow(cube, root / "products", isosurface=2.0)

    def test_signed_surface_mode_writes_positive_and_negative_isurfs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "signed.cub", SIGNED_CUBE)

            result = run_workflow(
                cube,
                root / "products",
                isosurface=0.2,
                surface_mode="signed",
                stem="signed",
            )

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.2 255 255\s+0 127 255\n  1   1\s+-0\.2\s+0\s+80 255 127 255")
            self.assertIn("surface_mode: `signed`", manifest)
            self.assertIn("isosurface_levels: `0.2, -0.2`", manifest)

    def test_signed_surface_requires_nonzero_level(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "signed.cub", SIGNED_CUBE)

            with self.assertRaisesRegex(ValueError, "non-zero"):
                run_workflow(cube, root / "products", isosurface=0.0, surface_mode="signed")

    def test_signed_surface_checks_negative_level_range(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "surface.cub", MOLECULE_CUBE)

            with self.assertRaisesRegex(ValueError, r"level\(s\).*-0\.2.*outside surface cube data range"):
                run_workflow(cube, root / "products", isosurface=0.2, surface_mode="signed")


if __name__ == "__main__":
    unittest.main()
