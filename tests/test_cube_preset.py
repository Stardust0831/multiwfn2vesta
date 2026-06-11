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


WIDE_SIGNED_CUBE = """wide signed comment one
wide signed comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -1.0 -0.8 -0.5 -0.1 0.1 0.5 0.8 1.0
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


VDW_POTENTIAL_CUBE = """vdw potential one
vdw potential two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -2.0 -1.2 -0.8 0.0 0.5 1.0 1.5 2.0
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


SURFANALYSIS_PDB = """\
REMARK   Unit of B-factor field (ALIE) is eV
REMARK   Carbon: Surface maximum    Oxygen: surface minimum
HETATM    1  C   MOL A   1       0.000   0.529   0.265  1.00  2.50           C
HETATM    1  O   MOL A   1       0.500   1.000   0.000  1.00 -1.25           O
END
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
        self.assertIn("gradient-norm", text)
        self.assertIn("signed", text)
        self.assertIn("spin-density", text)
        self.assertIn("spin-polarization", text)
        self.assertIn("orbital-density", text)
        self.assertIn("laplacian", text)
        self.assertIn("hamiltonian-ked", text)
        self.assertIn("lagrangian-ked", text)
        self.assertIn("potential", text)
        self.assertIn("vdw-potential", text)
        self.assertIn("partial-charge", text)
        self.assertIn("wavefunction-norm", text)
        self.assertIn("local-information-entropy", text)
        self.assertIn("electron-delocalization-range", text)
        self.assertIn("orbital-overlap-distance", text)
        self.assertIn("source-function", text)
        self.assertIn("user-function", text)
        self.assertIn("becke-weight", text)
        self.assertIn("hirshfeld-weight", text)
        self.assertIn("iri", text)
        self.assertIn("rdg-scalar", text)
        self.assertIn("promolecular-rdg", text)
        self.assertIn("promolecular-delta-g", text)
        self.assertIn("hirshfeld-delta-g", text)
        self.assertIn("iri-scalar", text)
        self.assertIn("dori-scalar", text)
        self.assertIn("stm", text)
        self.assertIn("domain", text)
        self.assertIn("basin", text)
        self.assertIn("basin-type", text)
        self.assertIn("igmh", text)
        self.assertIn("aigm", text)
        self.assertIn("esp", text)
        self.assertIn("dori", text)
        self.assertIn("alie", text)
        self.assertIn("surface-map", text)
        self.assertIn("vdw-map", text)

    def test_domain_preset_uses_binary_isosurface_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "domain.cub", """domain one
domain two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.0 0.0 0.0 1.0 1.0 1.0 0.0 0.0
""")

            result = run_preset("domain", cube, root / "products")

            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("canonical_preset: `domain`", manifest)
            self.assertIn("effective_isosurface: `0.5`", manifest)
            self.assertIn("Binary Multiwfn domain.cub isosurface", manifest)

    def test_basin_preset_uses_binary_isosurface_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "basin0001.cub", """basin one
basin two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.0 0.0 0.0 1.0 1.0 1.0 0.0 0.0
""")

            result = run_preset("binary-basin", cube, root / "products")

            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("canonical_preset: `basin`", manifest)
            self.assertIn("requested_preset: `binary-basin`", manifest)
            self.assertIn("effective_isosurface: `0.5`", manifest)
            self.assertIn("Binary Multiwfn basinNNNN.cub isosurface", manifest)

    def test_basin_preset_rejects_all_index_basin_cube_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "basin.cub", """basin all index
basin two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 1.0 1.0 2.0 2.0 3.0 3.0 0.0 0.0
""")

            with self.assertRaisesRegex(ValueError, "stores basin indices"):
                run_preset("basin", cube, root / "products")

    def test_basin_type_preset_uses_signed_synaptic_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "basinsyn.cub", """basin type one
basin type two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -1.0 -1.0 0.0 0.0 1.0 1.0 0.0 0.0
""")

            result = run_preset("basinsyn", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.5\s+255\s+180\s+40\s+145\s+255\n  1   1\s+-0\.5\s+80\s+160\s+255\s+145\s+255")
            self.assertIn("canonical_preset: `basin-type`", manifest)
            self.assertIn("effective_surface_mode: `signed`", manifest)
            self.assertIn("monosynaptic basin regions are -1", manifest)

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

    def test_gradient_norm_preset_writes_single_positive_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "gradient.cub", SURFACE_CUBE)

            result = run_preset("rho-gradient", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.05\s+120\s+210\s+255\s+145\s+255")
            self.assertNotRegex(text, r"\n  1   1\s+-0\.05")
            self.assertIn("canonical_preset: `gradient-norm`", manifest)
            self.assertIn("requested_preset: `rho-gradient`", manifest)
            self.assertIn("gradient.cub", manifest)
            self.assertIn("sur_value=0.05", manifest)

    def test_spin_density_preset_writes_signed_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "spindensity.cub", SIGNED_CUBE)

            result = run_preset("spindensity", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(
                text,
                r"ISURF\n  1   1\s+0\.02\s+255\s+80\s+80\s+145\s+255\n  1   1\s+-0\.02\s+70\s+130\s+255\s+145\s+255",
            )
            self.assertIn("canonical_preset: `spin-density`", manifest)
            self.assertIn("requested_preset: `spindensity`", manifest)
            self.assertIn("alpha-minus-beta spin density", manifest)
            self.assertIn("main-function-5 sur_value", manifest)

    def test_spin_polarization_preset_writes_signed_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "spindensity.cub", WIDE_SIGNED_CUBE)

            result = run_preset("spin-polarization", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(
                text,
                r"ISURF\n  1   1\s+0\.5\s+255\s+95\s+80\s+145\s+255\n  1   1\s+-0\.5\s+80\s+145\s+255\s+145\s+255",
            )
            self.assertIn("canonical_preset: `spin-polarization`", manifest)
            self.assertIn("dimensionless spin polarization parameter", manifest)
            self.assertIn("ipolarpara=1", manifest)

    def test_orbital_density_preset_writes_single_positive_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "orbdens.cub", SURFACE_CUBE)

            result = run_preset("orbdens", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.005\s+180\s+140\s+255\s+145\s+255")
            self.assertNotRegex(text, r"\n  1   1\s+-0\.005")
            self.assertIn("canonical_preset: `orbital-density`", manifest)
            self.assertIn("requested_preset: `orbdens`", manifest)
            self.assertIn("orbdens.cub", manifest)

    def test_laplacian_preset_writes_signed_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "laplacian.cub", SIGNED_CUBE)

            result = run_preset("laplacian-rho", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(
                text,
                r"ISURF\n  1   1\s+0\.05\s+255\s+165\s+40\s+125\s+255\n  1   1\s+-0\.05\s+60\s+130\s+255\s+125\s+255",
            )
            self.assertIn("canonical_preset: `laplacian`", manifest)
            self.assertIn("requested_preset: `laplacian-rho`", manifest)
            self.assertIn("laplacian.cub", manifest)

    def test_hamiltonian_ked_preset_writes_signed_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "K(r).cub", SIGNED_CUBE)

            result = run_preset("k(r)", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(
                text,
                r"ISURF\n  1   1\s+0\.01\s+255\s+195\s+55\s+130\s+255\n  1   1\s+-0\.01\s+80\s+110\s+255\s+130\s+255",
            )
            self.assertIn("canonical_preset: `hamiltonian-ked`", manifest)
            self.assertIn("requested_preset: `k(r)`", manifest)
            self.assertIn("K(r).cub", manifest)

    def test_lagrangian_ked_preset_writes_single_positive_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "G(r).cub", SURFACE_CUBE)

            result = run_preset("lagrangian-kinetic-density", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.01\s+90\s+210\s+150\s+145\s+255")
            self.assertNotRegex(text, r"\n  1   1\s+-0\.01")
            self.assertIn("canonical_preset: `lagrangian-ked`", manifest)
            self.assertIn("requested_preset: `lagrangian-kinetic-density`", manifest)
            self.assertIn("G(r).cub", manifest)

    def test_local_information_entropy_preset_writes_signed_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "infoentro.cub", SIGNED_CUBE)

            result = run_preset("infoentro", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(
                text,
                r"ISURF\n  1   1\s+0\.05\s+245\s+190\s+70\s+135\s+255\n  1   1\s+-0\.05\s+80\s+150\s+255\s+135\s+255",
            )
            self.assertIn("canonical_preset: `local-information-entropy`", manifest)
            self.assertIn("requested_preset: `infoentro`", manifest)
            self.assertIn("infoentro.cub", manifest)
            self.assertIn("-rho/N*ln(rho/N)", manifest)

    def test_source_function_preset_writes_signed_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "srcfunc.cub", SIGNED_CUBE)

            result = run_preset("srcfunc", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(
                text,
                r"ISURF\n  1   1\s+0\.05\s+255\s+210\s+80\s+135\s+255\n  1   1\s+-0\.05\s+70\s+130\s+255\s+135\s+255",
            )
            self.assertIn("canonical_preset: `source-function`", manifest)
            self.assertIn("requested_preset: `srcfunc`", manifest)
            self.assertIn("srcfunc.cub", manifest)
            self.assertIn("reference point", manifest)
            self.assertIn("srcfuncmode", manifest)
            self.assertIn("-set", manifest)
            self.assertIn("sur_value=0.05", manifest)

    def test_pair_function_preset_writes_signed_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "fermihole.cub", SIGNED_CUBE)

            result = run_preset("fermihole", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(
                text,
                r"ISURF\n  1   1\s+0\.05\s+255\s+185\s+90\s+135\s+255\n  1   1\s+-0\.05\s+85\s+145\s+255\s+135\s+255",
            )
            self.assertIn("canonical_preset: `pair-function`", manifest)
            self.assertIn("requested_preset: `fermihole`", manifest)
            self.assertIn("fermihole.cub", manifest)
            self.assertIn("reference point", manifest)
            self.assertIn("pairfunctype", manifest)
            self.assertIn("paircorrtype", manifest)
            self.assertIn("-set", manifest)

    def test_user_function_preset_writes_signed_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "userfunc.cub", SIGNED_CUBE)

            result = run_preset("userfunc", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(
                text,
                r"ISURF\n  1   1\s+0\.05\s+255\s+205\s+80\s+135\s+255\n  1   1\s+-0\.05\s+75\s+135\s+255\s+135\s+255",
            )
            self.assertIn("canonical_preset: `user-function`", manifest)
            self.assertIn("requested_preset: `userfunc`", manifest)
            self.assertIn("userfunc.cub", manifest)
            self.assertIn("iuserfunc", manifest)
            self.assertIn("LEA/LEAE", manifest)
            self.assertIn("system- and function-specific tuning", manifest)
            self.assertIn("-set", manifest)

    def test_electron_delocalization_range_preset_writes_single_positive_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "EDR.cub", SURFACE_CUBE)

            result = run_preset("edr", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.05\s+105\s+210\s+180\s+145\s+255")
            self.assertNotRegex(text, r"\n  1   1\s+-0\.05")
            self.assertNotIn("IMPORT_TEXTURE", text)
            self.assertIn("canonical_preset: `electron-delocalization-range`", manifest)
            self.assertIn("requested_preset: `edr`", manifest)
            self.assertIn("EDR.cub", manifest)
            self.assertIn("d in Bohr", manifest)
            self.assertIn("sur_value=0.05", manifest)

    def test_orbital_overlap_distance_preset_writes_single_positive_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "EDRDmax.cub", SURFACE_CUBE)

            result = run_preset("edrdmax", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.05\s+115\s+170\s+255\s+145\s+255")
            self.assertNotRegex(text, r"\n  1   1\s+-0\.05")
            self.assertNotIn("IMPORT_TEXTURE", text)
            self.assertIn("canonical_preset: `orbital-overlap-distance`", manifest)
            self.assertIn("requested_preset: `edrdmax`", manifest)
            self.assertIn("EDRDmax.cub", manifest)
            self.assertIn("default EDR exponent set 20, 2.50, 1.50", manifest)
            self.assertIn("sur_value=0.05", manifest)

    def test_becke_weight_preset_writes_single_positive_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "Becke.cub", SURFACE_CUBE)

            result = run_preset("becke", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.5\s+180\s+220\s+120\s+145\s+255")
            self.assertNotRegex(text, r"\n  1   1\s+-0\.5")
            self.assertNotIn("IMPORT_TEXTURE", text)
            self.assertIn("canonical_preset: `becke-weight`", manifest)
            self.assertIn("requested_preset: `becke`", manifest)
            self.assertIn("Becke.cub", manifest)
            self.assertIn("0..1", manifest)
            self.assertIn("I,0", manifest)

    def test_hirshfeld_weight_preset_writes_single_positive_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "Hirshfeld.cub", SURFACE_CUBE)

            result = run_preset("hirshfeld", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.5\s+120\s+205\s+170\s+145\s+255")
            self.assertNotRegex(text, r"\n  1   1\s+-0\.5")
            self.assertNotIn("IMPORT_TEXTURE", text)
            self.assertIn("canonical_preset: `hirshfeld-weight`", manifest)
            self.assertIn("requested_preset: `hirshfeld`", manifest)
            self.assertIn("Hirshfeld.cub", manifest)
            self.assertIn("0..1", manifest)
            self.assertIn("built-in atomic densities", manifest)

    def test_standalone_rdg_scalar_preset_keeps_iri_alias_available_for_texture_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "RDG.cub", SURFACE_CUBE)

            result = run_preset("rdg-cube", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.5\s+130\s+220\s+170\s+145\s+255")
            self.assertIn("canonical_preset: `rdg-scalar`", manifest)
            self.assertIn("requested_preset: `rdg-cube`", manifest)
            self.assertIn("For RDG/NCI surfaces colored by sign(lambda2)rho", manifest)

    def test_promolecular_rdg_scalar_preset_uses_multiwfn_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "RDGprodens.cub", SURFACE_CUBE)

            result = run_preset("rdg-pro", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.4\s+100\s+200\s+200\s+145\s+255")
            self.assertIn("canonical_preset: `promolecular-rdg`", manifest)
            self.assertIn("requested_preset: `rdg-pro`", manifest)
            self.assertIn("RDGprodens.cub", manifest)

    def test_promolecular_delta_g_preset_writes_single_positive_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "Delta_g.cub", SURFACE_CUBE)

            result = run_preset("deltag", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.05\s+255\s+185\s+70\s+145\s+255")
            self.assertNotRegex(text, r"\n  1   1\s+-0\.05")
            self.assertNotIn("IMPORT_TEXTURE", text)
            self.assertIn("canonical_preset: `promolecular-delta-g`", manifest)
            self.assertIn("requested_preset: `deltag`", manifest)
            self.assertIn("Delta_g.cub", manifest)
            self.assertIn("function 22", manifest)
            self.assertIn("distinct from IGM/IGMH fragment dg_inter.cub", manifest)
            self.assertIn("sur_value=0.05", manifest)

    def test_hirshfeld_delta_g_preset_writes_single_positive_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "griddata.cub", SURFACE_CUBE)

            result = run_preset("delta-g-hirshfeld", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.05\s+255\s+135\s+80\s+145\s+255")
            self.assertNotRegex(text, r"\n  1   1\s+-0\.05")
            self.assertNotIn("IMPORT_TEXTURE", text)
            self.assertIn("canonical_preset: `hirshfeld-delta-g`", manifest)
            self.assertIn("requested_preset: `delta-g-hirshfeld`", manifest)
            self.assertIn("griddata.cub", manifest)
            self.assertIn("function 23", manifest)
            self.assertIn("Hirshfeld partition", manifest)
            self.assertIn("fragment dg_inter.cub", manifest)

    def test_standalone_iri_scalar_preset_keeps_texture_route_available(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "IRI.cub", SURFACE_CUBE)

            result = run_preset("standalone-iri", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+1(?:\.0+)?\s+120\s+210\s+190\s+145\s+255")
            self.assertNotIn("IMPORT_TEXTURE", text)
            self.assertIn("canonical_preset: `iri-scalar`", manifest)
            self.assertIn("requested_preset: `standalone-iri`", manifest)
            self.assertIn("IRI.cub", manifest)
            self.assertIn("keep using preset `iri` with --texture-cube", manifest)

    def test_standalone_dori_scalar_preset_tracks_dorifill_isosurface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "userfunc.cub", SURFACE_CUBE)

            result = run_preset("standalone-dori", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.95\s+140\s+210\s+190\s+145\s+255")
            self.assertNotIn("IMPORT_TEXTURE", text)
            self.assertIn("canonical_preset: `dori-scalar`", manifest)
            self.assertIn("requested_preset: `standalone-dori`", manifest)
            self.assertIn("iuserfunc=20", manifest)
            self.assertIn("DORIfill.vmd", manifest)

    def test_abacus_direct_potential_preset_writes_signed_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "pot_es.cube", SIGNED_CUBE)

            result = run_preset("out-pot", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(
                text,
                r"ISURF\n  1   1\s+0\.05\s+255\s+90\s+60\s+120\s+255\n  1   1\s+-0\.05\s+60\s+120\s+255\s+120\s+255",
            )
            self.assertIn("canonical_preset: `potential`", manifest)
            self.assertIn("requested_preset: `out-pot`", manifest)
            self.assertIn("effective_surface_mode: `signed`", manifest)
            self.assertIn("direct ABACUS out_pot cubes", manifest)

    def test_vdw_potential_preset_writes_signed_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "vdWpot.cub", VDW_POTENTIAL_CUBE)

            result = run_preset("vdwpot", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(
                text,
                r"ISURF\n  1   1\s+1(?:\.0+)?\s+255\s+120\s+60\s+130\s+255\n  1   1\s+-1(?:\.0+)?\s+70\s+150\s+255\s+130\s+255",
            )
            self.assertNotIn("IMPORT_TEXTURE", text)
            self.assertIn("canonical_preset: `vdw-potential`", manifest)
            self.assertIn("requested_preset: `vdwpot`", manifest)
            self.assertIn("vdWpot.cub", manifest)
            self.assertIn("kcal/mol", manifest)
            self.assertIn("sur_value=1.0", manifest)
            self.assertIn("use preset `vdw-map`", manifest)

    def test_abacus_partial_charge_preset_writes_single_positive_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "pchg.cube", SURFACE_CUBE)

            result = run_preset("abacus-pchg", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.001\s+130\s+210\s+255\s+150\s+255")
            self.assertIn("canonical_preset: `partial-charge`", manifest)
            self.assertIn("requested_preset: `abacus-pchg`", manifest)
            self.assertIn("effective_surface_mode: `single`", manifest)
            self.assertIn("out_pchg partial charge cubes", manifest)

    def test_abacus_wavefunction_norm_preset_distinguishes_nonnegative_wfc(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "wfc_norm.cube", SURFACE_CUBE)

            result = run_preset("out-wfc-norm", cube, root / "products")

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.001\s+180\s+120\s+255\s+145\s+255")
            self.assertNotRegex(text, r"\n  1   1\s+-0\.001")
            self.assertIn("canonical_preset: `wavefunction-norm`", manifest)
            self.assertIn("requested_preset: `out-wfc-norm`", manifest)
            self.assertIn("effective_surface_mode: `single`", manifest)
            self.assertIn("out_wfc_norm", manifest)

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

    def test_dori_preset_tracks_bundled_dorifill_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface = self.write_tmp(root, "DORI.cub", SURFACE_CUBE)
            texture = self.write_tmp(root, "sl2r.cub", TEXTURE_CUBE)

            result = run_preset("dori-fill", surface, root / "products", texture_cube=texture, surface_band=0.25)

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertRegex(text, r"ISURF\n  1   1\s+0\.95")
            self.assertIn("IMPORT_TEXTURE", text)
            self.assertIn("TEX3P", text)
            self.assertIn("canonical_preset: `dori`", manifest)
            self.assertIn("requested_preset: `dori-fill`", manifest)
            self.assertIn("preset_tex_physical: `-0.04` to `0.02`", manifest)
            self.assertIn("effective_tex_physical: `-0.04` to `0.02`", manifest)
            self.assertIn("tex_reference_source: `surface-band`", manifest)
            self.assertIn("DORIfill.vmd", manifest)

    def test_stm_preset_accepts_ldos_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = self.write_tmp(root, "STM.cub", SURFACE_CUBE)

            result = run_preset("ldos", cube, root / "products")

            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("canonical_preset: `stm`", manifest)
            self.assertIn("requested_preset: `ldos`", manifest)
            self.assertIn("effective_isosurface: `0.001`", manifest)
            self.assertIn("Constant-current STM/LDOS", manifest)

    def test_igmh_alias_uses_multiwfn_igm_inter_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dg_inter = self.write_tmp(root, "dg_inter.cub", SURFACE_CUBE)
            sl2r = self.write_tmp(root, "sl2r.cub", TEXTURE_CUBE)

            result = run_preset("igm-inter", dg_inter, root / "products", texture_cube=sl2r)

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("IMPORT_TEXTURE", text)
            self.assertIn("canonical_preset: `igmh`", manifest)
            self.assertIn("requested_preset: `igm-inter`", manifest)
            self.assertIn("effective_isosurface: `0.01`", manifest)
            self.assertIn("preset_tex_physical: `-0.05` to `0.05`", manifest)
            self.assertIn("tex_reference_source: `full-cube`", manifest)
            self.assertIn("IGM_inter.vmd", manifest)

    def test_igm_intra_preset_tracks_template_isosurface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dg_intra = self.write_tmp(root, "dg_intra.cub", SURFACE_CUBE)
            sl2r = self.write_tmp(root, "sl2r.cub", TEXTURE_CUBE)

            result = run_preset("igmh-intra", dg_intra, root / "products", texture_cube=sl2r)

            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("canonical_preset: `igm-intra`", manifest)
            self.assertIn("effective_isosurface: `0.2`", manifest)
            self.assertIn("preset_tex_physical: `-0.05` to `0.05`", manifest)
            self.assertIn("IGM_intra.vmd", manifest)

    def test_aigm_presets_track_bundled_vmd_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            avgdg = self.write_tmp(root, "avgdg_inter.cub", SURFACE_CUBE)
            avgsl2r = self.write_tmp(root, "avgsl2r.cub", TEXTURE_CUBE)
            thermflu = self.write_tmp(root, "thermflu.cub", TEXTURE_CUBE)

            aigm = run_preset("average-igm", avgdg, root / "aigm_products", texture_cube=avgsl2r)
            tfi = run_preset("aigm-tfi", avgdg, root / "tfi_products", texture_cube=thermflu)

            aigm_manifest = aigm.manifest_path.read_text(encoding="utf-8")
            tfi_manifest = tfi.manifest_path.read_text(encoding="utf-8")

            self.assertIn("canonical_preset: `aigm`", aigm_manifest)
            self.assertIn("effective_isosurface: `0.008`", aigm_manifest)
            self.assertIn("preset_tex_physical: `-0.05` to `0.05`", aigm_manifest)
            self.assertIn("aIGM.vmd", aigm_manifest)
            self.assertIn("canonical_preset: `aigm-tfi`", tfi_manifest)
            self.assertIn("effective_isosurface: `0.008`", tfi_manifest)
            self.assertIn("preset_tex_physical: `0.0` to `1.5`", tfi_manifest)
            self.assertIn("aIGM_TFI.vmd", tfi_manifest)

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

    def test_alie_preset_auto_overlays_only_surface_minima(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            density = self.write_tmp(root, "density.cub", SURFACE_CUBE)
            alie = self.write_tmp(root, "avglocion.cub", ALIE_TEXTURE_CUBE)
            surfanalysis = self.write_tmp(root, "surfanalysis.pdb", SURFANALYSIS_PDB)

            result = run_preset(
                "alie",
                density,
                root / "products",
                texture_cube=alie,
                surfanalysis_pdb=surfanalysis,
            )

            text = result.vesta_path.read_text(encoding="utf-8")
            manifest = result.manifest_path.read_text(encoding="utf-8")

            self.assertIn("MIN0001", text)
            self.assertNotIn("MAX0001", text)
            self.assertIn("selection: `minima`", manifest)
            self.assertIn("extrema_count: `1`", manifest)
            self.assertIn("source_convention", manifest)

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
