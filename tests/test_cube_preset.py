import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.cube_preset import (
    format_preset_list,
    main,
    resolve_preset,
    run_preset,
)


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


TEXTURE_CUBE = """texture one
texture two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -0.10 -0.05 -0.02 0.00 0.03 0.04 0.08 0.10
"""


ALIE_TEXTURE_CUBE = """alie one
alie two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
  0.30 0.31 0.32 0.33 0.34 0.35 0.36 0.38
"""


class TestCubePreset(unittest.TestCase):
    def write_tmp(self, root, name, text):
        path = Path(root) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_resolve_preset_accepts_orbital_alias(self):
        preset = resolve_preset("orbital")
        self.assertEqual(preset.name, "signed")
        self.assertEqual(preset.surface_mode, "signed")

    def test_format_preset_list_mentions_main_routes(self):
        text = format_preset_list()
        self.assertIn("density", text)
        self.assertIn("signed", text)
        self.assertIn("iri", text)
        self.assertIn("esp", text)
        self.assertIn("alie", text)
        self.assertIn("surface-map", text)
        self.assertIn("vdw-map", text)

    def test_orbital_alias_writes_signed_surfaces_and_preset_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "orbital.cub", SIGNED_CUBE)

            result = run_preset("orbital", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("ISURF", text)
            self.assertRegex(text, r"ISURF\n  1   1\s+0\.02 255 255\s+0 127 255\n  1   1\s+-0\.02\s+0\s+80 255 127 255")
            self.assertIn("canonical_preset: `signed`", manifest)
            self.assertIn("requested_preset: `orbital`", manifest)
            self.assertIn("effective_surface_mode: `signed`", manifest)

    def test_iri_preset_requires_texture_cube(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface = self.write_tmp(root, "iri2.cub", SURFACE_CUBE)

            with self.assertRaisesRegex(ValueError, "requires --texture-cube"):
                run_preset("iri", surface, root / "products")

    def test_iri_preset_uses_surface_band_texture_scaling(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface = self.write_tmp(root, "iri2.cub", SURFACE_CUBE)
            texture = self.write_tmp(root, "iri1.cub", TEXTURE_CUBE)

            result = run_preset("rdg", surface, root / "products", texture_cube=texture, surface_band=0.25)

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("IMPORT_TEXTURE", text)
            self.assertIn("TEX3P", text)
            self.assertIn("tex_reference_source: `surface-band`", manifest)
            self.assertIn("preset_tex_physical: `-0.04` to `0.04`", manifest)
            self.assertIn("effective_tex_physical: `-0.04` to `0.04`", manifest)
            self.assertIn("canonical_preset: `iri`", manifest)
            self.assertIn("requested_preset: `rdg`", manifest)

    def test_alie_preset_uses_multiwfn_surface_map_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            density = self.write_tmp(root, "density.cub", SURFACE_CUBE)
            alie = self.write_tmp(root, "avglocion.cub", ALIE_TEXTURE_CUBE)

            result = run_preset(
                "average-local-ionization-energy",
                density,
                root / "products",
                texture_cube=alie,
            )

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("IMPORT_TEXTURE", text)
            self.assertIn("TEX3P", text)
            self.assertIn("canonical_preset: `alie`", manifest)
            self.assertIn("requested_preset: `average-local-ionization-energy`", manifest)
            self.assertIn("effective_isosurface: `0.0005`", manifest)
            self.assertIn("preset_tex_physical: `0.32` to `0.36`", manifest)
            self.assertIn("tex_reference_source: `full-cube`", manifest)

    def test_surface_map_preset_tracks_molsurfmap_template_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            density = self.write_tmp(root, "density.cub", SURFACE_CUBE)
            mapped = self.write_tmp(root, "mapped.cub", TEXTURE_CUBE)

            result = run_preset("molsurfmap", density, root / "products", texture_cube=mapped)

            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("canonical_preset: `surface-map`", manifest)
            self.assertIn("effective_isosurface: `0.01`", manifest)
            self.assertIn("preset_tex_physical: `0.0` to `0.002`", manifest)

    def test_vdw_surface_preset_records_vmd_default_range(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            density = self.write_tmp(root, "density.cub", SURFACE_CUBE)
            vdw = self.write_tmp(root, "vdW.cub", TEXTURE_CUBE)

            result = run_preset("vdw-surface", density, root / "products", texture_cube=vdw)

            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("canonical_preset: `vdw-map`", manifest)
            self.assertIn("effective_isosurface: `0.0001`", manifest)
            self.assertIn("preset_tex_physical: `-0.3` to `0.3`", manifest)

    def test_tex_percent_manifest_records_explicit_percent_scaling(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface = self.write_tmp(root, "iri2.cub", SURFACE_CUBE)
            texture = self.write_tmp(root, "iri1.cub", TEXTURE_CUBE)

            result = run_preset("rdg", surface, root / "products", texture_cube=texture, tex_percent=(10.0, 90.0))

            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("effective_tex_range_source: `explicit-percent`", manifest)
            self.assertIn("effective_tex_percent: `10.0` to `90.0`", manifest)
            self.assertIn("physical texture scaling was not applied", manifest)

    def test_main_lists_presets(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = main(["--list-presets"])

        self.assertEqual(code, 0)
        self.assertIn("Available cube presets", output.getvalue())

    def test_main_reports_missing_texture_for_iri(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface = self.write_tmp(root, "iri2.cub", SURFACE_CUBE)
            output = io.StringIO()

            with patch("sys.stdout", output):
                code = main(["iri", str(surface), str(root / "products")])

            self.assertEqual(code, 2)
            self.assertIn("requires --texture-cube", output.getvalue())


if __name__ == "__main__":
    unittest.main()
