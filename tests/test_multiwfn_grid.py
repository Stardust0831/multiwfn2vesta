import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.executables import ExecutableCandidate
from multiwfn2vesta.multiwfn_grid import (
    GRID_OUTPUT_MISSING_CODE,
    GRID_PROCESSING_FAILED_CODE,
    available_functions_text,
    build_grid_commands,
    resolve_grid_function,
    run_multiwfn_grid_batch,
    run_multiwfn_grid,
)


DENSITY_CUBE = """density comment one
density comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.00 0.02 0.04 0.06 0.08 0.10 0.12 0.14
"""


IRI_CUBE = """iri comment one
iri comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.00 0.40 0.80 1.00 1.10 1.20 1.60 2.00
"""


DORI_CUBE = """dori comment one
dori comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.00 0.40 0.80 0.95 1.00 1.10 1.20 1.60
"""


INFOENTRO_CUBE = """info entropy comment one
info entropy comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -0.20 -0.10 0.00 0.02 0.04 0.06 0.08 0.10
"""


DELTA_G_CUBE = """delta g comment one
delta g comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.00 0.01 0.02 0.04 0.05 0.06 0.08 0.10
"""


HIRSHFELD_DELTA_G_CUBE = """hirshfeld delta g comment one
hirshfeld delta g comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.00 0.01 0.02 0.04 0.05 0.06 0.08 0.10
"""


VDW_POTENTIAL_CUBE = """vdw potential comment one
vdw potential comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -2.00 -1.20 -0.40 0.00 0.40 1.00 1.50 2.00
"""


VDW_REPULSION_CUBE = """vdw repulsion comment one
vdw repulsion comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.00 0.20 0.50 0.80 1.00 1.20 1.50 2.00
"""


VDW_DISPERSION_CUBE = """vdw dispersion comment one
vdw dispersion comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -2.00 -1.50 -1.20 -1.00 -0.80 -0.50 -0.20 0.00
"""


EDR_CUBE = """edr comment one
edr comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.00 0.01 0.02 0.04 0.05 0.06 0.08 0.10
"""


EDRDMAX_CUBE = """edrdmax comment one
edrdmax comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.00 0.01 0.02 0.04 0.05 0.06 0.08 0.10
"""


BECKE_CUBE = """becke comment one
becke comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.00 0.10 0.25 0.40 0.50 0.60 0.75 1.00
"""


HIRSHFELD_CUBE = """hirshfeld comment one
hirshfeld comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.00 0.10 0.25 0.40 0.50 0.60 0.75 1.00
"""


SOURCE_FUNCTION_CUBE = """source function comment one
source function comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -0.20 -0.10 -0.05 0.00 0.05 0.10 0.15 0.20
"""


PAIR_FUNCTION_CUBE = """pair function comment one
pair function comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -0.20 -0.10 -0.05 0.00 0.05 0.10 0.15 0.20
"""


USER_FUNCTION_CUBE = """user function comment one
user function comment two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 -0.20 -0.10 -0.05 0.00 0.05 0.10 0.15 0.20
"""


class TestMultiwfnGridRunner(unittest.TestCase):
    def make_candidate(self, root):
        fake_exe = Path(root) / "Multiwfn_noGUI"
        fake_exe.write_text("#!/bin/sh\n", encoding="utf-8")
        fake_exe.chmod(0o755)
        return ExecutableCandidate("Multiwfn_noGUI", fake_exe, "test", True, True)

    def test_available_functions_and_alias_resolution(self):
        text = available_functions_text()
        self.assertIn("density", text)
        self.assertIn("orbital", text)
        self.assertIn("hamiltonian-ked", text)
        self.assertIn("preset=gradient-norm", text)
        self.assertIn("preset=spin-density", text)
        self.assertIn("preset=spin-polarization", text)
        self.assertIn("settings: ipolarpara=0", text)
        self.assertIn("settings: ipolarpara=1", text)
        self.assertIn("settings: ELFLOL_type=0", text)
        self.assertIn("settings: ivdwprobe=6", text)
        self.assertIn("preset=laplacian", text)
        self.assertIn("preset=hamiltonian-ked", text)
        self.assertIn("preset=lagrangian-ked", text)
        self.assertIn("preset=local-information-entropy", text)
        self.assertIn("preset=orbital-density", text)
        self.assertIn("preset=rdg-scalar", text)
        self.assertIn("preset=promolecular-rdg", text)
        self.assertIn("preset=promolecular-delta-g", text)
        self.assertIn("preset=hirshfeld-delta-g", text)
        self.assertIn("preset=iri-scalar", text)
        self.assertIn("preset=dori-scalar", text)
        self.assertIn("preset=vdw-potential", text)
        self.assertIn("preset=electron-delocalization-range", text)
        self.assertIn("preset=orbital-overlap-distance", text)
        self.assertIn("preset=pair-function", text)
        self.assertIn("preset=source-function", text)
        self.assertIn("preset=user-function", text)
        self.assertIn("preset=becke-weight", text)
        self.assertIn("preset=hirshfeld-weight", text)
        self.assertIn("promolecular-rdg", text)
        self.assertIn("alie", text)
        self.assertIn("mapped preset with --surface-cube: esp", text)
        self.assertIn("mapped preset with --surface-cube: alie", text)
        self.assertIn("mapped preset with --surface-cube: lea", text)
        self.assertIn("local-mulliken-electronegativity", text)
        self.assertIn("local-hardness", text)
        self.assertIn("mapped preset with --surface-cube: surface-map", text)
        self.assertIn("alpha-density", text)
        self.assertIn("beta-density", text)
        self.assertIn("default iuserfunc=1", text)
        self.assertIn("default iuserfunc=2", text)
        self.assertIn("fractional-occupation-density", text)
        self.assertIn("default iuserfunc=90", text)
        self.assertIn("default iuserfunc=20", text)
        self.assertIn("default iuserfunc=27", text)
        self.assertIn("default iuserfunc=-27", text)
        self.assertIn("default iuserfunc=28", text)
        self.assertIn("default iuserfunc=29", text)
        self.assertIn("thomas-fermi-ked", text)
        self.assertIn("weizsacker-ked", text)
        self.assertIn("pauli-ked", text)
        self.assertIn("default iuserfunc=1200", text)
        self.assertIn("default iuserfunc=114", text)
        self.assertIn("settings: iKEDsel=3", text)
        self.assertIn("settings: iKEDsel=4", text)
        self.assertIn("settings: iKEDsel=2", text)
        self.assertIn("orbital-weighted-fukui-plus", text)
        self.assertIn("orbital-weighted-dual-descriptor", text)
        self.assertIn("default iuserfunc=95", text)
        self.assertIn("default iuserfunc=98", text)
        self.assertIn("vdw-repulsion-potential", text)
        self.assertIn("preset=vdw-repulsion-potential", text)
        self.assertIn("vdw-dispersion-potential", text)
        self.assertIn("preset=vdw-dispersion-potential", text)
        self.assertIn("default iuserfunc=93", text)
        self.assertIn("default iuserfunc=94", text)
        self.assertIn("requires --orbital", text)
        self.assertEqual(resolve_grid_function("rho").name, "density")
        self.assertEqual(resolve_grid_function("rho-gradient").name, "gradient")
        self.assertEqual(resolve_grid_function("grad-rho").preset, "gradient-norm")
        self.assertEqual(resolve_grid_function("12").name, "esp")
        self.assertEqual(resolve_grid_function(None, 9).name, "elf")
        self.assertEqual(resolve_grid_function("k(r)").output_filename, "K(r).cub")
        self.assertEqual(resolve_grid_function("k(r)").preset, "hamiltonian-ked")
        self.assertEqual(resolve_grid_function("lagrangian-kinetic-density").index, 7)
        self.assertEqual(resolve_grid_function("lagrangian-kinetic-density").preset, "lagrangian-ked")
        self.assertEqual(resolve_grid_function("information-entropy").index, 11)
        self.assertEqual(resolve_grid_function("local-info-entropy").output_filename, "infoentro.cub")
        self.assertEqual(resolve_grid_function("local-shannon-entropy").preset, "local-information-entropy")
        self.assertEqual(resolve_grid_function("spin").preset, "spin-density")
        self.assertEqual(resolve_grid_function("spin-density").settings_updates, (("ipolarpara", 0),))
        self.assertEqual(resolve_grid_function("spin-polarization").preset, "spin-polarization")
        self.assertEqual(resolve_grid_function("spin-pol").settings_updates, (("ipolarpara", 1),))
        self.assertEqual(resolve_grid_function(None, 5).name, "spin-density")
        self.assertEqual(resolve_grid_function("elf").settings_updates, (("ELFLOL_type", 0),))
        self.assertEqual(resolve_grid_function("lol").settings_updates, (("ELFLOL_type", 0),))
        self.assertEqual(resolve_grid_function("lap").preset, "laplacian")
        self.assertEqual(resolve_grid_function("orbdens").preset, "orbital-density")
        self.assertEqual(resolve_grid_function("rdg").preset, "rdg-scalar")
        self.assertEqual(resolve_grid_function("rdg-pro").preset, "promolecular-rdg")
        self.assertEqual(resolve_grid_function("delta-g").preset, "promolecular-delta-g")
        self.assertEqual(resolve_grid_function("deltag").output_filename, "Delta_g.cub")
        self.assertEqual(resolve_grid_function("delta_g").index, 22)
        self.assertEqual(resolve_grid_function("delta-g-promol").preset, "promolecular-delta-g")
        self.assertEqual(resolve_grid_function("hirshfeld-delta-g").index, 23)
        self.assertEqual(resolve_grid_function("delta-g-hirshfeld").output_filename, "griddata.cub")
        self.assertEqual(resolve_grid_function("deltag-hirshfeld").preset, "hirshfeld-delta-g")
        self.assertEqual(resolve_grid_function("igmh-scalar").name, "hirshfeld-delta-g")
        self.assertEqual(resolve_grid_function("iri").preset, "iri-scalar")
        self.assertEqual(resolve_grid_function("interaction-region-indicator").output_filename, "IRI.cub")
        self.assertEqual(resolve_grid_function("vdw").preset, "vdw-potential")
        self.assertEqual(resolve_grid_function("vdwpot").output_filename, "vdWpot.cub")
        self.assertEqual(resolve_grid_function("vdw").settings_updates, (("ivdwprobe", 6),))
        self.assertEqual(resolve_grid_function("van-der-waals-potential").index, 25)
        self.assertEqual(resolve_grid_function("repul").preset, "vdw-repulsion-potential")
        self.assertEqual(resolve_grid_function("repulsion-potential").default_user_function_index, 93)
        self.assertEqual(resolve_grid_function("vdw-repulsion").settings_updates, (("ivdwprobe", 6),))
        self.assertEqual(resolve_grid_function("vdw-repulsion").mapped_preset, "vdw-map")
        self.assertEqual(resolve_grid_function("disp").preset, "vdw-dispersion-potential")
        self.assertEqual(resolve_grid_function("dispersion-potential").default_user_function_index, 94)
        self.assertEqual(resolve_grid_function("vdw-dispersion").settings_updates, (("ivdwprobe", 6),))
        self.assertEqual(resolve_grid_function("vdw-dispersion").mapped_preset, "vdw-map")
        self.assertEqual(resolve_grid_function("edr").index, 20)
        self.assertEqual(resolve_grid_function("edr").output_filename, "EDR.cub")
        self.assertEqual(resolve_grid_function("edrdmax").index, 21)
        self.assertEqual(resolve_grid_function("edrdmax").output_filename, "EDRDmax.cub")
        self.assertEqual(resolve_grid_function("d(r)").preset, "orbital-overlap-distance")
        self.assertEqual(resolve_grid_function("pair-function").index, 17)
        self.assertEqual(resolve_grid_function("fermihole").output_filename, "fermihole.cub")
        self.assertEqual(resolve_grid_function("correlation-hole").preset, "pair-function")
        self.assertEqual(resolve_grid_function("xc-density").name, "pair-function")
        self.assertEqual(resolve_grid_function("pair-density").index, 17)
        self.assertEqual(resolve_grid_function("source-function").index, 19)
        self.assertEqual(resolve_grid_function("srcfunc").output_filename, "srcfunc.cub")
        self.assertEqual(resolve_grid_function("source").preset, "source-function")
        self.assertEqual(resolve_grid_function("user-function").index, 100)
        self.assertEqual(resolve_grid_function("userfunc").output_filename, "userfunc.cub")
        self.assertEqual(resolve_grid_function(None, 100).name, "user-function")
        self.assertEqual(resolve_grid_function("100").name, "user-function")
        self.assertEqual(resolve_grid_function("alpha-density").preset, "density")
        self.assertEqual(resolve_grid_function("rho-alpha").default_user_function_index, 1)
        self.assertEqual(resolve_grid_function("alpha-rho").mapped_preset, "surface-map")
        self.assertEqual(resolve_grid_function("beta-density").preset, "density")
        self.assertEqual(resolve_grid_function("rho-beta").default_user_function_index, 2)
        self.assertEqual(resolve_grid_function("beta-rho").mapped_preset, "surface-map")
        self.assertEqual(resolve_grid_function("fractional-occupation-density").preset, "density")
        self.assertEqual(resolve_grid_function("fod").default_user_function_index, 90)
        self.assertEqual(resolve_grid_function("fractional-occupancy-density").default_user_function_index, 90)
        self.assertEqual(resolve_grid_function("fod-density").mapped_preset, "surface-map")
        self.assertEqual(resolve_grid_function("local-electron-affinity").preset, "user-function")
        self.assertEqual(resolve_grid_function("local-electron-affinity").default_user_function_index, 27)
        self.assertEqual(resolve_grid_function("local-electron-affinity").mapped_preset, "lea")
        self.assertEqual(resolve_grid_function("leae-function").name, "local-electron-attachment-energy")
        self.assertEqual(resolve_grid_function("leae-function").default_user_function_index, -27)
        self.assertEqual(resolve_grid_function("leae-function").mapped_preset, "leae")
        self.assertEqual(resolve_grid_function("dori").preset, "dori-scalar")
        self.assertEqual(resolve_grid_function("dori-function").default_user_function_index, 20)
        self.assertEqual(resolve_grid_function("density-overlap-regions-indicator").name, "dori")
        self.assertEqual(
            resolve_grid_function("local-electronegativity").name,
            "local-mulliken-electronegativity",
        )
        self.assertEqual(resolve_grid_function("electronegativity").default_user_function_index, 28)
        self.assertEqual(resolve_grid_function("local-hardness").mapped_preset, "surface-map")
        self.assertEqual(resolve_grid_function("local-chemical-hardness").default_user_function_index, 29)
        self.assertEqual(resolve_grid_function("thomas-fermi-ked").preset, "kinetic-energy-density")
        self.assertEqual(resolve_grid_function("tf-ked").default_user_function_index, 1200)
        self.assertEqual(resolve_grid_function("tf-ked").settings_updates, (("iKEDsel", 3),))
        self.assertEqual(resolve_grid_function("weizsacker-ked").default_user_function_index, 1200)
        self.assertEqual(resolve_grid_function("vw-ked").settings_updates, (("iKEDsel", 4),))
        self.assertEqual(resolve_grid_function("pauli-ked").default_user_function_index, 114)
        self.assertEqual(resolve_grid_function("pauli-kinetic-energy-density").settings_updates, (("iKEDsel", 2),))
        self.assertEqual(resolve_grid_function("pauli-ked").mapped_preset, "surface-map")
        self.assertEqual(resolve_grid_function("ow-fukui-plus").preset, "density")
        self.assertEqual(resolve_grid_function("orbital-weighted-fplus").default_user_function_index, 95)
        self.assertEqual(resolve_grid_function("ow-fukui-minus").default_user_function_index, 96)
        self.assertEqual(resolve_grid_function("ow-f0").default_user_function_index, 97)
        self.assertEqual(resolve_grid_function("orbital-weighted-dual").preset, "signed")
        self.assertEqual(resolve_grid_function("ow-dual").default_user_function_index, 98)
        self.assertEqual(resolve_grid_function("ow-dd").default_user_function_index, 98)
        self.assertEqual(resolve_grid_function("information-gain-density").default_user_function_index, 49)
        self.assertEqual(resolve_grid_function("relative-shannon-entropy").name, "information-gain-density")
        self.assertEqual(resolve_grid_function("shannon-entropy-density").default_user_function_index, 50)
        self.assertEqual(resolve_grid_function("fisher-information-density").default_user_function_index, 51)
        self.assertEqual(resolve_grid_function("second-fisher-information-density").default_user_function_index, 52)
        self.assertEqual(resolve_grid_function("becke").index, 111)
        self.assertEqual(resolve_grid_function("becke").output_filename, "Becke.cub")
        self.assertEqual(resolve_grid_function("becke-overlap-weight").preset, "becke-weight")
        self.assertEqual(resolve_grid_function("becke-atomic-weight").name, "becke-weight")
        self.assertEqual(resolve_grid_function("hirshfeld").index, 112)
        self.assertEqual(resolve_grid_function("hirshfeld").output_filename, "Hirshfeld.cub")
        self.assertEqual(resolve_grid_function("hirshfeld-atomic-weight").preset, "hirshfeld-weight")
        self.assertEqual(resolve_grid_function(None, 18).name, "alie")
        self.assertEqual(resolve_grid_function("sl2r-pro").index, 16)
        custom = resolve_grid_function(None, 99)
        self.assertEqual(custom.index, 99)
        self.assertEqual(custom.output_filename, "griddata.cub")

    def test_build_density_points_command_stream(self):
        function = resolve_grid_function("density")
        commands = build_grid_commands(function, grid_points=(12, 13, 14))
        self.assertEqual(commands, ["5", "1", "4", "12,13,14", "2", "0", "q"])

    def test_build_orbital_command_requires_orbital_selector(self):
        function = resolve_grid_function("orbital")
        with self.assertRaises(ValueError):
            build_grid_commands(function)
        self.assertEqual(
            build_grid_commands(function, orbital="h", grid_mode="low"),
            ["5", "4", "h", "1", "2", "0", "q"],
        )

    def test_build_reference_cube_grid_command_stream(self):
        function = resolve_grid_function("elf")
        with tempfile.TemporaryDirectory() as tmp:
            ref = Path(tmp) / "ref.cub"
            ref.write_text(DENSITY_CUBE, encoding="utf-8")
            commands = build_grid_commands(function, grid_mode="cube", grid_cube=ref)

        self.assertEqual(commands[:3], ["5", "9", "8"])
        self.assertTrue(commands[3].endswith("ref.cub"))
        self.assertEqual(commands[-3:], ["2", "0", "q"])

    def test_build_spin_polarization_command_stream_uses_function_5(self):
        function = resolve_grid_function("spin-polarization")
        self.assertEqual(
            build_grid_commands(function, grid_points=(10, 11, 12)),
            ["5", "5", "4", "10,11,12", "2", "0", "q"],
        )

    def test_build_alie_command_stream_uses_function_18(self):
        function = resolve_grid_function("alie")
        commands = build_grid_commands(function, grid_mode="medium")

        self.assertEqual(commands, ["5", "18", "2", "2", "0", "q"])

    def test_build_source_function_command_stream_sets_reference_point(self):
        function = resolve_grid_function("source-function")

        with self.assertRaisesRegex(ValueError, "requires --reference-point"):
            build_grid_commands(function)
        with self.assertRaisesRegex(ValueError, "--source-function-mode must be 1 or 2"):
            build_grid_commands(function, reference_point=(1.0, 2.0, 3.0), source_function_mode=3)

        self.assertEqual(
            build_grid_commands(
                function,
                reference_point=(1.0, 2.0, 3.0),
                source_function_mode=2,
                grid_points=(10, 11, 12),
            ),
            ["1000", "1", "1.0,2.0,3.0", "5", "19", "4", "10,11,12", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(
                function,
                reference_point=(1.0, 2.0, 3.0),
                reference_unit="angstrom",
                grid_mode="low",
            ),
            ["1000", "1", "1.0,2.0,3.0 A", "5", "19", "1", "2", "0", "q"],
        )
        with self.assertRaisesRegex(ValueError, "--reference-point is only valid"):
            build_grid_commands(resolve_grid_function("density"), reference_point=(1.0, 2.0, 3.0))
        with self.assertRaisesRegex(ValueError, "--source-function-mode is only valid"):
            build_grid_commands(resolve_grid_function("density"), source_function_mode=2)
        self.assertEqual(
            build_grid_commands(resolve_grid_function("density"), reference_unit="au", grid_mode="low"),
            ["5", "1", "1", "2", "0", "q"],
        )
        with self.assertRaisesRegex(ValueError, "--reference-unit is only valid"):
            build_grid_commands(resolve_grid_function("density"), reference_unit="angstrom")

    def test_build_pair_function_command_stream_sets_reference_point(self):
        function = resolve_grid_function("pair-function")

        with self.assertRaisesRegex(ValueError, "requires --reference-point"):
            build_grid_commands(function)
        with self.assertRaisesRegex(ValueError, "--pair-function-type must be one of"):
            build_grid_commands(function, reference_point=(1.0, 2.0, 3.0), pair_function_type=3)
        with self.assertRaisesRegex(ValueError, "--pair-correlation-type must be 1, 2, or 3"):
            build_grid_commands(function, reference_point=(1.0, 2.0, 3.0), pair_correlation_type=4)

        self.assertEqual(
            build_grid_commands(
                function,
                reference_point=(1.0, 2.0, 3.0),
                pair_function_type=7,
                pair_correlation_type=1,
                grid_points=(10, 11, 12),
            ),
            ["1000", "1", "1.0,2.0,3.0", "5", "17", "4", "10,11,12", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(
                function,
                reference_point=(1.0, 2.0, 3.0),
                reference_unit="angstrom",
                grid_mode="low",
            ),
            ["1000", "1", "1.0,2.0,3.0 A", "5", "17", "1", "2", "0", "q"],
        )
        with self.assertRaisesRegex(ValueError, "--pair-function-type is only valid"):
            build_grid_commands(resolve_grid_function("density"), pair_function_type=1)
        with self.assertRaisesRegex(ValueError, "--pair-correlation-type is only valid"):
            build_grid_commands(resolve_grid_function("density"), pair_correlation_type=3)

    def test_build_user_function_command_stream_uses_iuserfunc_settings_only(self):
        function = resolve_grid_function("user-function")

        with self.assertRaisesRegex(ValueError, "requires --user-function-index"):
            build_grid_commands(function)
        with self.assertRaisesRegex(ValueError, "special external-grid"):
            build_grid_commands(function, user_function_index=-1)
        with self.assertRaisesRegex(ValueError, "Shubin"):
            build_grid_commands(function, user_function_index=57)

        self.assertEqual(
            build_grid_commands(
                function,
                user_function_index=27,
                grid_points=(10, 11, 12),
            ),
            ["5", "100", "4", "10,11,12", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(
                function,
                user_function_index=-27,
                grid_mode="low",
            ),
            ["5", "100", "1", "2", "0", "q"],
        )
        with self.assertRaisesRegex(ValueError, "--user-function-index is only valid"):
            build_grid_commands(resolve_grid_function("density"), user_function_index=27)

    def test_build_named_user_function_uses_default_iuserfunc(self):
        function = resolve_grid_function("local-electron-affinity")

        self.assertEqual(
            build_grid_commands(function, grid_points=(10, 11, 12)),
            ["5", "100", "4", "10,11,12", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(
                resolve_grid_function("shannon-entropy-density"),
                grid_mode="low",
            ),
            ["5", "100", "1", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(resolve_grid_function("dori"), grid_mode="low"),
            ["5", "100", "1", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(resolve_grid_function("local-hardness"), grid_mode="low"),
            ["5", "100", "1", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(resolve_grid_function("alpha-density"), grid_mode="low"),
            ["5", "100", "1", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(resolve_grid_function("fod"), grid_mode="low"),
            ["5", "100", "1", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(resolve_grid_function("pauli-ked"), grid_mode="low"),
            ["5", "100", "1", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(resolve_grid_function("repul"), grid_mode="low"),
            ["5", "100", "1", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(resolve_grid_function("disp"), grid_mode="low"),
            ["5", "100", "1", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(resolve_grid_function("orbital-weighted-dual-descriptor"), grid_mode="low"),
            ["5", "100", "1", "2", "0", "q"],
        )
        with self.assertRaisesRegex(ValueError, "special external-grid"):
            build_grid_commands(function, user_function_index=-1)

    def test_build_edr_command_stream_requires_length_scale(self):
        function = resolve_grid_function("edr")
        with self.assertRaisesRegex(ValueError, "requires --edr-length"):
            build_grid_commands(function)
        with self.assertRaisesRegex(ValueError, "must be positive"):
            build_grid_commands(function, edr_length=0)

        commands = build_grid_commands(function, edr_length=0.85, grid_points=(10, 11, 12))

        self.assertEqual(commands, ["5", "20", "0.85", "4", "10,11,12", "2", "0", "q"])

    def test_build_orbital_overlap_distance_command_stream_uses_default_or_manual_exponents(self):
        function = resolve_grid_function("orbital-overlap-distance")

        self.assertEqual(
            build_grid_commands(function, grid_mode="low"),
            ["5", "21", "2", "1", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(function, edr_exponents=(12, 3.0, 1.2), grid_mode="medium"),
            ["5", "21", "1", "12 3.0 1.2", "2", "2", "0", "q"],
        )
        with self.assertRaisesRegex(ValueError, "count must be an integer"):
            build_grid_commands(function, edr_exponents=(12.5, 3.0, 1.2))
        with self.assertRaisesRegex(ValueError, "increment must be at least 1.01"):
            build_grid_commands(function, edr_exponents=(12, 3.0, 1.0))
        with self.assertRaisesRegex(ValueError, "only valid for electron-delocalization-range"):
            build_grid_commands(function, edr_length=0.85)

    def test_build_becke_weight_command_stream_requires_atom_pair(self):
        function = resolve_grid_function("becke")

        with self.assertRaisesRegex(ValueError, "requires --becke-atoms"):
            build_grid_commands(function)
        with self.assertRaisesRegex(ValueError, "first Becke atom index must be positive"):
            build_grid_commands(function, becke_atoms=(0, 4))
        with self.assertRaisesRegex(ValueError, "second Becke atom index must be zero or positive"):
            build_grid_commands(function, becke_atoms=(1, -1))

        self.assertEqual(
            build_grid_commands(function, becke_atoms=(1, 4), grid_points=(10, 11, 12)),
            ["5", "111", "1,4", "4", "10,11,12", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(function, becke_atoms=(5, 0), grid_mode="low"),
            ["5", "111", "5,0", "1", "2", "0", "q"],
        )
        with self.assertRaisesRegex(ValueError, "only valid for Becke"):
            build_grid_commands(resolve_grid_function("density"), becke_atoms=(1, 4))

    def test_build_hirshfeld_weight_command_stream_uses_builtin_density(self):
        function = resolve_grid_function("hirshfeld")

        with self.assertRaisesRegex(ValueError, "requires --hirshfeld-atoms"):
            build_grid_commands(function)
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            build_grid_commands(function, hirshfeld_atoms=" ")
        with self.assertRaisesRegex(ValueError, "ranges must be ascending"):
            build_grid_commands(function, hirshfeld_atoms="5-3")
        with self.assertRaisesRegex(ValueError, "indices must be positive"):
            build_grid_commands(function, hirshfeld_atoms="0,2")
        with self.assertRaisesRegex(ValueError, "currently supported"):
            build_grid_commands(function, hirshfeld_atoms="2,3", hirshfeld_density_type="atomic-wfn")

        self.assertEqual(
            build_grid_commands(
                function,
                hirshfeld_atoms="2, 3, 7-10",
                grid_points=(10, 11, 12),
            ),
            ["5", "112", "2,3,7-10", "2", "4", "10,11,12", "2", "0", "q"],
        )
        self.assertEqual(
            build_grid_commands(
                function,
                hirshfeld_atoms="4",
                hirshfeld_density_type="built-in",
                grid_mode="low",
            ),
            ["5", "112", "4", "2", "1", "2", "0", "q"],
        )
        with self.assertRaisesRegex(ValueError, "only valid for Hirshfeld"):
            build_grid_commands(resolve_grid_function("density"), hirshfeld_atoms="2,3")

    def test_build_hirshfeld_delta_g_command_stream_has_no_extra_prompt(self):
        function = resolve_grid_function("hirshfeld-delta-g")

        self.assertEqual(
            build_grid_commands(function, grid_points=(10, 11, 12)),
            ["5", "23", "4", "10,11,12", "2", "0", "q"],
        )

    def test_run_multiwfn_grid_writes_cube_vesta_and_recipe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "density.cub").write_text(DENSITY_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="warn")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        nthreads=2,
                        timeout=30,
                        stem="case",
                        grid_points=(12, 12, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.cli_returncode, 0)
            self.assertEqual(mocked_run.call_args.args[0], [str(candidate.path), str(wavefunction.resolve()), "-nt", "2"])
            self.assertEqual(mocked_run.call_args.kwargs["timeout"], 30)
            self.assertEqual(mocked_run.call_args.kwargs["env"]["Multiwfnpath"], str(candidate.path.parent))
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n1\n4\n12,12,12\n2\n0\nq\n")
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "ok")
            self.assertEqual(result.stderr_log.read_text(encoding="utf-8"), "warn")
            self.assertTrue(result.raw_cube.exists())
            self.assertTrue(result.cube.exists())
            self.assertEqual(result.cube.name, "case_density.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertTrue(result.vesta_result.vesta_path.exists())
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_index: `1`", recipe)
            self.assertIn("auto_vesta_preset: `density`", recipe)

    def test_run_multiwfn_grid_gradient_uses_gradient_norm_preset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "gradient.cub").write_text(DENSITY_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="gradient",
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n2\n4\n10,11,12\n2\n0\nq\n")
            self.assertEqual(result.raw_cube.name, "gradient.cub")
            self.assertEqual(result.cube.name, "case_gradient.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(result.vesta_result.vesta_path.name, "case_gradient_gradient-norm_cube.vesta")
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `gradient`", recipe)
            self.assertIn("function_index: `2`", recipe)
            self.assertIn("auto_vesta_preset: `gradient-norm`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `gradient-norm`", manifest)
            self.assertIn("effective_isosurface: `0.05`", manifest)

    def test_run_multiwfn_grid_spin_routes_patch_ipolarpara(self):
        cases = (
            ("spin-density", "1", "0", "spin-density"),
            ("spin-polarization", "0", "1", "spin-polarization"),
        )
        for function_name, base_value, expected_value, expected_preset in cases:
            with self.subTest(function_name=function_name):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    wavefunction = root / "h2o.fch"
                    wavefunction.write_text("wavefunction", encoding="utf-8")
                    candidate = self.make_candidate(root)
                    (candidate.path.parent / "settings.ini").write_text(
                        f"laplfac= 6\nipolarpara= {base_value}\nother_setting= keep\n",
                        encoding="utf-8",
                    )

                    def fake_run(command, **kwargs):
                        cwd = Path(kwargs["cwd"])
                        (cwd / "spindensity.cub").write_text(VDW_POTENTIAL_CUBE, encoding="utf-8")
                        return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

                    with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                        with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run) as mocked_run:
                            result = run_multiwfn_grid(
                                wavefunction,
                                root / "products",
                                function_name=function_name,
                                stem="case",
                                grid_points=(10, 11, 12),
                            )

                    self.assertTrue(result.success)
                    self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n5\n4\n10,11,12\n2\n0\nq\n")
                    self.assertEqual(
                        mocked_run.call_args.args[0],
                        [
                            str(candidate.path),
                            str(wavefunction.resolve()),
                            "-set",
                            str((root / "products" / "multiwfn_grid_raw" / "multiwfn_grid_settings.ini").resolve()),
                        ],
                    )
                    self.assertIsNotNone(result.settings_override)
                    settings_text = result.settings_override.read_text(encoding="utf-8")
                    self.assertIn("laplfac= 6", settings_text)
                    self.assertIn(f"ipolarpara= {expected_value}", settings_text)
                    self.assertNotIn(f"ipolarpara= {base_value}\n", settings_text)
                    self.assertIn("other_setting= keep", settings_text)
                    self.assertEqual(result.raw_cube.name, "spindensity.cub")
                    self.assertEqual(result.cube.name, f"case_{function_name}.cub")
                    self.assertIsNotNone(result.vesta_result)
                    self.assertEqual(
                        result.vesta_result.vesta_path.name,
                        f"case_{function_name}_{expected_preset}_cube.vesta",
                    )
                    recipe = result.recipe_path.read_text(encoding="utf-8")
                    self.assertIn("function_index: `5`", recipe)
                    self.assertIn("local_settings_file:", recipe)
                    manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
                    self.assertIn(f"canonical_preset: `{expected_preset}`", manifest)

    def test_run_multiwfn_grid_elf_lol_routes_patch_elflol_type(self):
        cases = (
            ("elf", None, "0", "ELF.cub", "elf"),
            ("elf", "d-over-d0", "3", "ELF.cub", "elf"),
            ("lol", "tsirelson", "1", "LOL.cub", "lol"),
        )
        for function_name, requested_type, expected_value, raw_name, expected_preset in cases:
            with self.subTest(function_name=function_name):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    wavefunction = root / "h2o.fch"
                    wavefunction.write_text("wavefunction", encoding="utf-8")
                    candidate = self.make_candidate(root)
                    (candidate.path.parent / "settings.ini").write_text(
                        "ELFLOL_type= 2 // stale global setting\nother_setting= keep\n",
                        encoding="utf-8",
                    )

                    def fake_run(command, **kwargs):
                        cwd = Path(kwargs["cwd"])
                        (cwd / raw_name).write_text(IRI_CUBE, encoding="utf-8")
                        return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

                    with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                        with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run) as mocked_run:
                            result = run_multiwfn_grid(
                                wavefunction,
                                root / "products",
                                function_name=function_name,
                                stem="case",
                                grid_points=(10, 11, 12),
                                elflol_type=requested_type,
                            )

                    self.assertTrue(result.success)
                    self.assertEqual(
                        mocked_run.call_args.args[0],
                        [
                            str(candidate.path),
                            str(wavefunction.resolve()),
                            "-set",
                            str((root / "products" / "multiwfn_grid_raw" / "multiwfn_grid_settings.ini").resolve()),
                        ],
                    )
                    self.assertEqual(result.elflol_type, int(expected_value))
                    self.assertIsNotNone(result.settings_override)
                    settings_text = result.settings_override.read_text(encoding="utf-8")
                    self.assertIn(f"ELFLOL_type= {expected_value} // stale global setting", settings_text)
                    self.assertIn("other_setting= keep", settings_text)
                    self.assertEqual(result.raw_cube.name, raw_name)
                    self.assertEqual(result.cube.name, f"case_{function_name}.cub")
                    recipe = result.recipe_path.read_text(encoding="utf-8")
                    self.assertIn(f"elflol_type: `{expected_value}`", recipe)
                    manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
                    self.assertIn(f"canonical_preset: `{expected_preset}`", manifest)

    def test_run_multiwfn_grid_rejects_lol_d_over_d0(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "only valid for elf"):
                run_multiwfn_grid(
                    Path(tmp) / "h2o.fch",
                    Path(tmp) / "products",
                    function_name="lol",
                    elflol_type="d-over-d0",
                )

    def test_run_multiwfn_grid_information_entropy_uses_dedicated_preset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "infoentro.cub").write_text(INFOENTRO_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="information-entropy",
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n11\n4\n10,11,12\n2\n0\nq\n")
            self.assertEqual(result.raw_cube.name, "infoentro.cub")
            self.assertEqual(result.cube.name, "case_local-information-entropy.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_local-information-entropy_local-information-entropy_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `local-information-entropy`", recipe)
            self.assertIn("function_index: `11`", recipe)
            self.assertIn("auto_vesta_preset: `local-information-entropy`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `local-information-entropy`", manifest)
            self.assertIn("effective_isosurface: `0.05`", manifest)

    def test_run_multiwfn_grid_source_function_uses_reference_point_and_local_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)
            (candidate.path.parent / "settings.ini").write_text(
                "laplfac= 6\nsrcfuncmode= 1\nother_setting= keep\n",
                encoding="utf-8",
            )

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "srcfunc.cub").write_text(SOURCE_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="source-function",
                        reference_point=(1.0, 2.0, 3.0),
                        reference_unit="angstrom",
                        source_function_mode=2,
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.reference_point, (1.0, 2.0, 3.0))
            self.assertEqual(result.reference_unit, "angstrom")
            self.assertEqual(result.source_function_mode, 2)
            self.assertEqual(
                result.command_file.read_text(encoding="utf-8"),
                "1000\n1\n1.0,2.0,3.0 A\n5\n19\n4\n10,11,12\n2\n0\nq\n",
            )
            self.assertEqual(
                mocked_run.call_args.args[0],
                [
                    str(candidate.path),
                    str(wavefunction.resolve()),
                    "-set",
                    str((root / "products" / "multiwfn_grid_raw" / "multiwfn_grid_settings.ini").resolve()),
                ],
            )
            self.assertIsNotNone(result.settings_override)
            self.assertEqual(result.settings_override.name, "multiwfn_grid_settings.ini")
            settings_text = result.settings_override.read_text(encoding="utf-8")
            self.assertIn("laplfac= 6", settings_text)
            self.assertIn("srcfuncmode= 2", settings_text)
            self.assertNotIn("srcfuncmode= 1", settings_text)
            self.assertIn("other_setting= keep", settings_text)
            self.assertEqual(result.raw_cube.name, "srcfunc.cub")
            self.assertEqual(result.cube.name, "case_source-function.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_source-function_source-function_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_index: `19`", recipe)
            self.assertIn("reference_point: `(1.0, 2.0, 3.0)`", recipe)
            self.assertIn("reference_unit: `angstrom`", recipe)
            self.assertIn("source_function_mode: `2`", recipe)
            self.assertIn("local_settings_file:", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `source-function`", manifest)
            self.assertIn("effective_surface_mode: `signed`", manifest)
            self.assertIn("srcfunc.cub", manifest)
            self.assertIn("srcfuncmode", manifest)
            self.assertIn("-set", manifest)

    def test_run_multiwfn_grid_pair_function_uses_reference_point_and_local_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)
            (candidate.path.parent / "settings.ini").write_text(
                "laplfac= 6\npairfunctype= 1\npaircorrtype= 3\nother_setting= keep\n",
                encoding="utf-8",
            )

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "fermihole.cub").write_text(PAIR_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="pair-function",
                        reference_point=(1.0, 2.0, 3.0),
                        reference_unit="angstrom",
                        pair_function_type=7,
                        pair_correlation_type=1,
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.reference_point, (1.0, 2.0, 3.0))
            self.assertEqual(result.reference_unit, "angstrom")
            self.assertEqual(result.pair_function_type, 7)
            self.assertEqual(result.pair_correlation_type, 1)
            self.assertEqual(
                result.command_file.read_text(encoding="utf-8"),
                "1000\n1\n1.0,2.0,3.0 A\n5\n17\n4\n10,11,12\n2\n0\nq\n",
            )
            self.assertEqual(
                mocked_run.call_args.args[0],
                [
                    str(candidate.path),
                    str(wavefunction.resolve()),
                    "-set",
                    str((root / "products" / "multiwfn_grid_raw" / "multiwfn_grid_settings.ini").resolve()),
                ],
            )
            self.assertIsNotNone(result.settings_override)
            self.assertEqual(result.settings_override.name, "multiwfn_grid_settings.ini")
            settings_text = result.settings_override.read_text(encoding="utf-8")
            self.assertIn("laplfac= 6", settings_text)
            self.assertIn("pairfunctype= 7", settings_text)
            self.assertIn("paircorrtype= 1", settings_text)
            self.assertNotIn("pairfunctype= 1\n", settings_text)
            self.assertNotIn("paircorrtype= 3\n", settings_text)
            self.assertIn("other_setting= keep", settings_text)
            self.assertEqual(result.raw_cube.name, "fermihole.cub")
            self.assertEqual(result.cube.name, "case_pair-function.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_pair-function_pair-function_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_index: `17`", recipe)
            self.assertIn("reference_point: `(1.0, 2.0, 3.0)`", recipe)
            self.assertIn("reference_unit: `angstrom`", recipe)
            self.assertIn("pair_function_type: `7`", recipe)
            self.assertIn("pair_correlation_type: `1`", recipe)
            self.assertIn("local_settings_file:", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `pair-function`", manifest)
            self.assertIn("effective_surface_mode: `signed`", manifest)
            self.assertIn("fermihole.cub", manifest)
            self.assertIn("pairfunctype", manifest)
            self.assertIn("paircorrtype", manifest)
            self.assertIn("-set", manifest)

    def test_run_multiwfn_grid_user_function_uses_local_iuserfunc_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)
            (candidate.path.parent / "settings.ini").write_text(
                "laplfac= 6\niuserfunc= 0\nother_setting= keep\n",
                encoding="utf-8",
            )

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "userfunc.cub").write_text(USER_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="local-electron-affinity",
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.user_function_index, 27)
            self.assertEqual(
                result.command_file.read_text(encoding="utf-8"),
                "5\n100\n4\n10,11,12\n2\n0\nq\n",
            )
            self.assertEqual(
                mocked_run.call_args.args[0],
                [
                    str(candidate.path),
                    str(wavefunction.resolve()),
                    "-set",
                    str((root / "products" / "multiwfn_grid_raw" / "multiwfn_grid_settings.ini").resolve()),
                ],
            )
            self.assertIsNotNone(result.settings_override)
            settings_text = result.settings_override.read_text(encoding="utf-8")
            self.assertIn("laplfac= 6", settings_text)
            self.assertIn("iuserfunc= 27", settings_text)
            self.assertNotIn("iuserfunc= 0", settings_text)
            self.assertIn("other_setting= keep", settings_text)
            self.assertEqual(result.raw_cube.name, "userfunc.cub")
            self.assertEqual(result.cube.name, "case_local-electron-affinity.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_local-electron-affinity_user-function_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `local-electron-affinity`", recipe)
            self.assertIn("function_index: `100`", recipe)
            self.assertIn("user_function_index_iuserfunc: `27`", recipe)
            self.assertIn("local_settings_file:", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `user-function`", manifest)
            self.assertIn("effective_surface_mode: `signed`", manifest)
            self.assertIn("userfunc.cub", manifest)
            self.assertIn("iuserfunc", manifest)
            self.assertIn("-set", manifest)

    def test_run_named_user_function_can_override_default_iuserfunc(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)
            (candidate.path.parent / "settings.ini").write_text("iuserfunc= 0\n", encoding="utf-8")

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "userfunc.cub").write_text(USER_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="local-electron-affinity",
                        user_function_index=49,
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.user_function_index, 49)
            self.assertIn("iuserfunc= 49", result.settings_override.read_text(encoding="utf-8"))
            self.assertEqual(result.cube.name, "case_local-electron-affinity.cub")
            self.assertIn(
                "user_function_index_iuserfunc: `49`",
                result.recipe_path.read_text(encoding="utf-8"),
            )

    def test_run_orbital_weighted_dual_descriptor_uses_named_iuserfunc(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)
            (candidate.path.parent / "settings.ini").write_text("iuserfunc= 0\n", encoding="utf-8")

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "userfunc.cub").write_text(USER_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="orbital-weighted-dual-descriptor",
                        stem="case",
                        grid_mode="low",
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.user_function_index, 98)
            self.assertIn("iuserfunc= 98", result.settings_override.read_text(encoding="utf-8"))
            self.assertEqual(result.raw_cube.name, "userfunc.cub")
            self.assertEqual(result.cube.name, "case_orbital-weighted-dual-descriptor.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_orbital-weighted-dual-descriptor_signed_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `orbital-weighted-dual-descriptor`", recipe)
            self.assertIn("function_index: `100`", recipe)
            self.assertIn("user_function_index_iuserfunc: `98`", recipe)
            self.assertIn("auto_vesta_preset: `signed`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `signed`", manifest)
            self.assertIn("effective_surface_mode: `signed`", manifest)

    def test_run_alpha_density_uses_named_iuserfunc_and_density_preset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)
            (candidate.path.parent / "settings.ini").write_text("iuserfunc= 0\n", encoding="utf-8")

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "userfunc.cub").write_text(USER_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="rho-alpha",
                        stem="case",
                        grid_mode="low",
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.user_function_index, 1)
            self.assertIn("iuserfunc= 1", result.settings_override.read_text(encoding="utf-8"))
            self.assertEqual(result.raw_cube.name, "userfunc.cub")
            self.assertEqual(result.cube.name, "case_alpha-density.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(result.vesta_result.vesta_path.name, "case_alpha-density_density_cube.vesta")
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `alpha-density`", recipe)
            self.assertIn("function_index: `100`", recipe)
            self.assertIn("user_function_index_iuserfunc: `1`", recipe)
            self.assertIn("auto_vesta_preset: `density`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `density`", manifest)
            self.assertIn("effective_surface_mode: `single`", manifest)

    def test_run_beta_density_surface_map_uses_named_iuserfunc(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            surface_cube = root / "density.cub"
            surface_cube.write_text(DENSITY_CUBE, encoding="utf-8")
            candidate = self.make_candidate(root)
            (candidate.path.parent / "settings.ini").write_text("iuserfunc= 0\n", encoding="utf-8")

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "userfunc.cub").write_text(USER_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="rho-beta",
                        surface_cube=surface_cube,
                        tex_physical=(0.0, 0.01),
                        tex_range_source="surface-band",
                        stem="case",
                        grid_mode="low",
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.user_function_index, 2)
            self.assertIn("iuserfunc= 2", result.settings_override.read_text(encoding="utf-8"))
            self.assertEqual(result.cube.name, "case_beta-density.cub")
            self.assertEqual(result.mapped_preset, "surface-map")
            self.assertIsNotNone(result.vesta_result)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `beta-density`", recipe)
            self.assertIn("user_function_index_iuserfunc: `2`", recipe)
            self.assertIn("auto_vesta_preset: `density`", recipe)
            self.assertIn("mapped_vesta_preset: `surface-map`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `surface-map`", manifest)
            self.assertIn("effective_tex_physical: `0.0` to `0.01`", manifest)

    def test_run_fractional_occupation_density_uses_named_iuserfunc(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)
            (candidate.path.parent / "settings.ini").write_text("iuserfunc= 0\n", encoding="utf-8")

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "userfunc.cub").write_text(USER_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="fod",
                        stem="case",
                        grid_mode="low",
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.user_function_index, 90)
            self.assertIn("iuserfunc= 90", result.settings_override.read_text(encoding="utf-8"))
            self.assertEqual(result.raw_cube.name, "userfunc.cub")
            self.assertEqual(result.cube.name, "case_fractional-occupation-density.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_fractional-occupation-density_density_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `fractional-occupation-density`", recipe)
            self.assertIn("user_function_index_iuserfunc: `90`", recipe)
            self.assertIn("auto_vesta_preset: `density`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `density`", manifest)

    def test_run_fractional_occupation_density_surface_map_passes_texture_scale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            surface_cube = root / "density.cub"
            surface_cube.write_text(DENSITY_CUBE, encoding="utf-8")
            candidate = self.make_candidate(root)
            (candidate.path.parent / "settings.ini").write_text("iuserfunc= 0\n", encoding="utf-8")

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "userfunc.cub").write_text(USER_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="fractional-occupancy-density",
                        surface_cube=surface_cube,
                        tex_physical=(0.0, 0.005),
                        tex_range_source="surface-band",
                        stem="case",
                        grid_mode="low",
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.user_function_index, 90)
            self.assertEqual(result.cube.name, "case_fractional-occupation-density.cub")
            self.assertEqual(result.mapped_preset, "surface-map")
            self.assertEqual(result.tex_physical, (0.0, 0.005))
            self.assertEqual(result.tex_range_source, "surface-band")
            self.assertIsNotNone(result.vesta_result)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `fractional-occupation-density`", recipe)
            self.assertIn("user_function_index_iuserfunc: `90`", recipe)
            self.assertIn("auto_vesta_preset: `density`", recipe)
            self.assertIn("mapped_vesta_preset: `surface-map`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `surface-map`", manifest)
            self.assertIn("effective_tex_physical: `0.0` to `0.005`", manifest)

    def test_run_ked_named_user_functions_patch_iuserfunc_and_ikedsel(self):
        cases = (
            ("thomas-fermi-ked", 1200, 3, "case_thomas-fermi-ked.cub"),
            ("weizsacker-ked", 1200, 4, "case_weizsacker-ked.cub"),
            ("pauli-ked", 114, 2, "case_pauli-ked.cub"),
        )
        for function_name, expected_iuserfunc, expected_ikedsel, expected_cube in cases:
            with self.subTest(function_name=function_name):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    wavefunction = root / "h2o.fch"
                    wavefunction.write_text("wavefunction", encoding="utf-8")
                    candidate = self.make_candidate(root)
                    (candidate.path.parent / "settings.ini").write_text(
                        "iuserfunc= 0 // stale userfunc\niKEDsel= 0 // stale KED\n",
                        encoding="utf-8",
                    )

                    def fake_run(command, **kwargs):
                        cwd = Path(kwargs["cwd"])
                        (cwd / "userfunc.cub").write_text(USER_FUNCTION_CUBE, encoding="utf-8")
                        return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

                    with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                        with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                            result = run_multiwfn_grid(
                                wavefunction,
                                root / "products",
                                function_name=function_name,
                                stem="case",
                                grid_mode="low",
                            )

                    self.assertTrue(result.success)
                    self.assertEqual(result.user_function_index, expected_iuserfunc)
                    self.assertEqual(result.cube.name, expected_cube)
                    self.assertEqual(result.raw_cube.name, "userfunc.cub")
                    self.assertIsNotNone(result.settings_override)
                    settings_text = result.settings_override.read_text(encoding="utf-8")
                    self.assertIn(f"iuserfunc= {expected_iuserfunc} // stale userfunc", settings_text)
                    self.assertIn(f"iKEDsel= {expected_ikedsel} // stale KED", settings_text)
                    self.assertIsNotNone(result.vesta_result)
                    self.assertEqual(
                        result.vesta_result.vesta_path.name,
                        expected_cube.replace(".cub", "_kinetic-energy-density_cube.vesta"),
                    )
                    recipe = result.recipe_path.read_text(encoding="utf-8")
                    self.assertIn(f"function_name: `{function_name}`", recipe)
                    self.assertIn(f"user_function_index_iuserfunc: `{expected_iuserfunc}`", recipe)
                    self.assertIn(f"('iKEDsel', {expected_ikedsel})", recipe)
                    self.assertIn("auto_vesta_preset: `kinetic-energy-density`", recipe)
                    manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
                    self.assertIn("canonical_preset: `kinetic-energy-density`", manifest)
                    self.assertIn("effective_surface_mode: `single`", manifest)

    def test_run_orbital_weighted_dual_descriptor_surface_map_passes_texture_scale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            surface_cube = root / "density.cub"
            surface_cube.write_text(DENSITY_CUBE, encoding="utf-8")
            candidate = self.make_candidate(root)
            (candidate.path.parent / "settings.ini").write_text("iuserfunc= 0\n", encoding="utf-8")

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "userfunc.cub").write_text(USER_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="ow-dd",
                        surface_cube=surface_cube,
                        tex_physical=(-0.04, 0.04),
                        tex_range_source="surface-band",
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.user_function_index, 98)
            self.assertEqual(result.mapped_preset, "surface-map")
            self.assertEqual(result.tex_physical, (-0.04, 0.04))
            self.assertEqual(result.tex_range_source, "surface-band")
            self.assertIsNotNone(result.vesta_result)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `orbital-weighted-dual-descriptor`", recipe)
            self.assertIn("user_function_index_iuserfunc: `98`", recipe)
            self.assertIn("auto_vesta_preset: `signed`", recipe)
            self.assertIn("mapped_vesta_preset: `surface-map`", recipe)
            self.assertIn("mapped_tex_physical: `(-0.04, 0.04)`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `surface-map`", manifest)
            self.assertIn("effective_tex_physical: `-0.04` to `0.04`", manifest)

    def test_run_multiwfn_grid_dori_uses_named_iuserfunc_and_scalar_preset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "userfunc.cub").write_text(DORI_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="dori",
                        stem="case",
                        grid_mode="low",
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.user_function_index, 20)
            self.assertIsNotNone(result.settings_override)
            self.assertIn("iuserfunc= 20", result.settings_override.read_text(encoding="utf-8"))
            self.assertEqual(result.raw_cube.name, "userfunc.cub")
            self.assertEqual(result.cube.name, "case_dori.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_dori_dori-scalar_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `dori`", recipe)
            self.assertIn("function_index: `100`", recipe)
            self.assertIn("user_function_index_iuserfunc: `20`", recipe)
            self.assertIn("auto_vesta_preset: `dori-scalar`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `dori-scalar`", manifest)
            self.assertIn("effective_isosurface: `0.95`", manifest)
            self.assertIn("DORIfill.vmd", manifest)

    def test_named_lea_leae_user_functions_select_mapped_presets(self):
        for function_name, expected_preset in (
            ("local-electron-affinity", "lea"),
            ("local-electron-attachment-energy", "leae"),
        ):
            with self.subTest(function_name=function_name):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    wavefunction = root / "h2o.fch"
                    wavefunction.write_text("wavefunction", encoding="utf-8")
                    surface_cube = root / "density.cub"
                    surface_cube.write_text(DENSITY_CUBE, encoding="utf-8")
                    candidate = self.make_candidate(root)

                    def fake_run(command, **kwargs):
                        cwd = Path(kwargs["cwd"])
                        (cwd / "userfunc.cub").write_text(USER_FUNCTION_CUBE, encoding="utf-8")
                        return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

                    with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                        with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                            result = run_multiwfn_grid(
                                wavefunction,
                                root / "products",
                                function_name=function_name,
                                surface_cube=surface_cube,
                                stem="case",
                                grid_points=(10, 11, 12),
                            )

                    self.assertTrue(result.success)
                    self.assertEqual(result.mapped_preset, expected_preset)
                    self.assertIsNotNone(result.vesta_result)
                    manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
                    self.assertIn(f"canonical_preset: `{expected_preset}`", manifest)
                    self.assertIn("texture_cube:", manifest)

    def test_run_multiwfn_grid_iri_uses_standalone_iri_scalar_preset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "IRI.cub").write_text(IRI_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="iri",
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n24\n4\n10,11,12\n2\n0\nq\n")
            self.assertEqual(result.raw_cube.name, "IRI.cub")
            self.assertEqual(result.cube.name, "case_iri.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(result.vesta_result.vesta_path.name, "case_iri_iri-scalar_cube.vesta")
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `iri`", recipe)
            self.assertIn("function_index: `24`", recipe)
            self.assertIn("auto_vesta_preset: `iri-scalar`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `iri-scalar`", manifest)
            self.assertIn("effective_isosurface: `1.0`", manifest)

    def test_run_multiwfn_grid_delta_g_uses_promolecular_delta_g_preset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "Delta_g.cub").write_text(DELTA_G_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="delta-g",
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n22\n4\n10,11,12\n2\n0\nq\n")
            self.assertEqual(result.raw_cube.name, "Delta_g.cub")
            self.assertEqual(result.cube.name, "case_delta-g.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_delta-g_promolecular-delta-g_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `delta-g`", recipe)
            self.assertIn("function_index: `22`", recipe)
            self.assertIn("auto_vesta_preset: `promolecular-delta-g`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `promolecular-delta-g`", manifest)
            self.assertIn("effective_isosurface: `0.05`", manifest)
            self.assertIn("dg_inter.cub", manifest)

    def test_run_multiwfn_grid_hirshfeld_delta_g_uses_griddata_and_dedicated_preset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "griddata.cub").write_text(HIRSHFELD_DELTA_G_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="hirshfeld-delta-g",
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n23\n4\n10,11,12\n2\n0\nq\n")
            self.assertEqual(result.raw_cube.name, "griddata.cub")
            self.assertEqual(result.cube.name, "case_hirshfeld-delta-g.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_hirshfeld-delta-g_hirshfeld-delta-g_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `hirshfeld-delta-g`", recipe)
            self.assertIn("function_index: `23`", recipe)
            self.assertIn("multiwfn_default_cube: `griddata.cub`", recipe)
            self.assertIn("auto_vesta_preset: `hirshfeld-delta-g`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `hirshfeld-delta-g`", manifest)
            self.assertIn("effective_isosurface: `0.05`", manifest)
            self.assertIn("function 23", manifest)
            self.assertIn("griddata.cub", manifest)
            self.assertIn("dg_inter.cub", manifest)

    def test_run_multiwfn_grid_vdw_uses_standalone_vdw_potential_preset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)
            (candidate.path.parent / "settings.ini").write_text(
                "ivdwprobe= 8 // stale probe\nother_setting= keep\n",
                encoding="utf-8",
            )

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "vdWpot.cub").write_text(VDW_POTENTIAL_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="vdw",
                        vdw_probe="U",
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(
                mocked_run.call_args.args[0],
                [
                    str(candidate.path),
                    str(wavefunction.resolve()),
                    "-set",
                    str((root / "products" / "multiwfn_grid_raw" / "multiwfn_grid_settings.ini").resolve()),
                ],
            )
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n25\n4\n10,11,12\n2\n0\nq\n")
            self.assertEqual(result.vdw_probe, 92)
            self.assertIsNotNone(result.settings_override)
            settings_text = result.settings_override.read_text(encoding="utf-8")
            self.assertIn("ivdwprobe= 92 // stale probe", settings_text)
            self.assertIn("other_setting= keep", settings_text)
            self.assertEqual(result.raw_cube.name, "vdWpot.cub")
            self.assertEqual(result.cube.name, "case_vdw-potential.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_vdw-potential_vdw-potential_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_name: `vdw-potential`", recipe)
            self.assertIn("function_index: `25`", recipe)
            self.assertIn("vdw_probe_atomic_number_ivdwprobe: `92`", recipe)
            self.assertIn("auto_vesta_preset: `vdw-potential`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `vdw-potential`", manifest)
            self.assertIn("effective_isosurface: `1.0`", manifest)
            self.assertIn("kcal/mol", manifest)

    def test_run_multiwfn_grid_rejects_vdw_probe_for_other_functions(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "vdW potential routes"):
                run_multiwfn_grid(
                    Path(tmp) / "h2o.fch",
                    Path(tmp) / "products",
                    function_name="density",
                    vdw_probe="O",
                )

    def test_run_multiwfn_grid_vdw_component_routes_patch_iuserfunc_and_probe(self):
        cases = (
            (
                "repul",
                "Ar",
                18,
                93,
                VDW_REPULSION_CUBE,
                "vdw-repulsion-potential",
                "1.0",
            ),
            (
                "disp",
                "O",
                8,
                94,
                VDW_DISPERSION_CUBE,
                "vdw-dispersion-potential",
                "-1.0",
            ),
        )
        for function_name, requested_probe, expected_probe, expected_iuserfunc, cube_text, expected_preset, expected_isosurface in cases:
            with self.subTest(function_name=function_name):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    wavefunction = root / "h2o.fch"
                    wavefunction.write_text("wavefunction", encoding="utf-8")
                    candidate = self.make_candidate(root)
                    (candidate.path.parent / "settings.ini").write_text(
                        "ivdwprobe= 6 // stale probe\niuserfunc= 0 // stale userfunc\nother_setting= keep\n",
                        encoding="utf-8",
                    )

                    def fake_run(command, **kwargs):
                        cwd = Path(kwargs["cwd"])
                        (cwd / "userfunc.cub").write_text(cube_text, encoding="utf-8")
                        return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

                    with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                        with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run) as mocked_run:
                            result = run_multiwfn_grid(
                                wavefunction,
                                root / "products",
                                function_name=function_name,
                                vdw_probe=requested_probe,
                                stem="case",
                                grid_mode="low",
                            )

                    self.assertTrue(result.success)
                    self.assertEqual(
                        mocked_run.call_args.args[0],
                        [
                            str(candidate.path),
                            str(wavefunction.resolve()),
                            "-set",
                            str((root / "products" / "multiwfn_grid_raw" / "multiwfn_grid_settings.ini").resolve()),
                        ],
                    )
                    self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n100\n1\n2\n0\nq\n")
                    self.assertEqual(result.user_function_index, expected_iuserfunc)
                    self.assertEqual(result.vdw_probe, expected_probe)
                    self.assertIsNotNone(result.settings_override)
                    settings_text = result.settings_override.read_text(encoding="utf-8")
                    self.assertIn(f"ivdwprobe= {expected_probe} // stale probe", settings_text)
                    self.assertIn(f"iuserfunc= {expected_iuserfunc} // stale userfunc", settings_text)
                    self.assertIn("other_setting= keep", settings_text)
                    self.assertEqual(result.raw_cube.name, "userfunc.cub")
                    self.assertEqual(result.cube.name, f"case_{expected_preset}.cub")
                    self.assertIsNotNone(result.vesta_result)
                    self.assertEqual(
                        result.vesta_result.vesta_path.name,
                        f"case_{expected_preset}_{expected_preset}_cube.vesta",
                    )
                    recipe = result.recipe_path.read_text(encoding="utf-8")
                    self.assertIn(f"function_name: `{expected_preset}`", recipe)
                    self.assertIn("function_index: `100`", recipe)
                    self.assertIn(f"user_function_index_iuserfunc: `{expected_iuserfunc}`", recipe)
                    self.assertIn(f"vdw_probe_atomic_number_ivdwprobe: `{expected_probe}`", recipe)
                    self.assertIn(f"auto_vesta_preset: `{expected_preset}`", recipe)
                    manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
                    self.assertIn(f"canonical_preset: `{expected_preset}`", manifest)
                    self.assertIn(f"effective_isosurface: `{expected_isosurface}`", manifest)
                    self.assertIn("kcal/mol", manifest)

    def test_run_multiwfn_grid_vdw_probe_defaults_and_normalizes_inputs(self):
        cases = (
            (None, "6"),
            ("17", "17"),
            ("cl", "17"),
        )
        for requested_probe, expected_probe in cases:
            with self.subTest(requested_probe=requested_probe):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    wavefunction = root / "h2o.fch"
                    wavefunction.write_text("wavefunction", encoding="utf-8")
                    candidate = self.make_candidate(root)

                    def fake_run(command, **kwargs):
                        Path(kwargs["cwd"], "vdWpot.cub").write_text(VDW_POTENTIAL_CUBE, encoding="utf-8")
                        return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

                    with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                        with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                            result = run_multiwfn_grid(
                                wavefunction,
                                root / "products",
                                function_name="vdw-potential",
                                vdw_probe=requested_probe,
                                stem="case",
                                grid_mode="low",
                                make_vesta=False,
                            )

                    self.assertTrue(result.success)
                    self.assertEqual(result.vdw_probe, int(expected_probe))
                    self.assertIsNotNone(result.settings_override)
                    settings_text = result.settings_override.read_text(encoding="utf-8")
                    self.assertIn(f"ivdwprobe= {expected_probe}", settings_text)

    def test_run_multiwfn_grid_rejects_invalid_vdw_probe_boundaries(self):
        for requested_probe in ("0", "104"):
            with self.subTest(requested_probe=requested_probe):
                with tempfile.TemporaryDirectory() as tmp:
                    with self.assertRaisesRegex(ValueError, "range 1..103"):
                        run_multiwfn_grid(
                            Path(tmp) / "h2o.fch",
                            Path(tmp) / "products",
                            function_name="vdw-potential",
                            vdw_probe=requested_probe,
                        )

    def test_run_multiwfn_grid_edr_uses_length_scale_and_dedicated_preset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "EDR.cub").write_text(EDR_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="edr",
                        edr_length=0.85,
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.edr_length, 0.85)
            self.assertIsNone(result.edr_exponents)
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n20\n0.85\n4\n10,11,12\n2\n0\nq\n")
            self.assertEqual(result.raw_cube.name, "EDR.cub")
            self.assertEqual(result.cube.name, "case_electron-delocalization-range.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_electron-delocalization-range_electron-delocalization-range_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_index: `20`", recipe)
            self.assertIn("edr_length_bohr: `0.85`", recipe)
            self.assertIn("EDR.cub", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `electron-delocalization-range`", manifest)
            self.assertIn("effective_isosurface: `0.05`", manifest)
            self.assertIn("d in Bohr", manifest)

    def test_run_multiwfn_grid_orbital_overlap_distance_uses_manual_exponents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "EDRDmax.cub").write_text(EDRDMAX_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="edrdmax",
                        edr_exponents=(12, 3.0, 1.2),
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertIsNone(result.edr_length)
            self.assertEqual(result.edr_exponents, (12, 3.0, 1.2))
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n21\n1\n12 3.0 1.2\n4\n10,11,12\n2\n0\nq\n")
            self.assertEqual(result.raw_cube.name, "EDRDmax.cub")
            self.assertEqual(result.cube.name, "case_orbital-overlap-distance.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_orbital-overlap-distance_orbital-overlap-distance_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_index: `21`", recipe)
            self.assertIn("edr_exponents_count_start_increment: `(12, 3.0, 1.2)`", recipe)
            self.assertIn("EDRDmax.cub", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `orbital-overlap-distance`", manifest)
            self.assertIn("effective_isosurface: `0.05`", manifest)
            self.assertIn("default EDR exponent set 20, 2.50, 1.50", manifest)

    def test_run_multiwfn_grid_becke_uses_atom_pair_and_dedicated_preset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "Becke.cub").write_text(BECKE_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="becke",
                        becke_atoms=(1, 4),
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.becke_atoms, (1, 4))
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n111\n1,4\n4\n10,11,12\n2\n0\nq\n")
            self.assertEqual(result.raw_cube.name, "Becke.cub")
            self.assertEqual(result.cube.name, "case_becke-weight.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_becke-weight_becke-weight_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_index: `111`", recipe)
            self.assertIn("becke_atom_indices_i_j: `(1, 4)`", recipe)
            self.assertIn("Becke.cub", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `becke-weight`", manifest)
            self.assertIn("effective_isosurface: `0.5`", manifest)
            self.assertIn("Becke weights", manifest)

    def test_run_multiwfn_grid_hirshfeld_uses_atom_selection_and_dedicated_preset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "Hirshfeld.cub").write_text(HIRSHFELD_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="hirshfeld",
                        hirshfeld_atoms="2, 3, 7-10",
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.hirshfeld_atoms, "2,3,7-10")
            self.assertEqual(result.hirshfeld_density_type, "builtin")
            self.assertEqual(
                result.command_file.read_text(encoding="utf-8"),
                "5\n112\n2,3,7-10\n2\n4\n10,11,12\n2\n0\nq\n",
            )
            self.assertEqual(result.raw_cube.name, "Hirshfeld.cub")
            self.assertEqual(result.cube.name, "case_hirshfeld-weight.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(
                result.vesta_result.vesta_path.name,
                "case_hirshfeld-weight_hirshfeld-weight_cube.vesta",
            )
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("function_index: `112`", recipe)
            self.assertIn("hirshfeld_atom_selection: `2,3,7-10`", recipe)
            self.assertIn("hirshfeld_density_type: `builtin`", recipe)
            self.assertIn("Hirshfeld.cub", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `hirshfeld-weight`", manifest)
            self.assertIn("effective_isosurface: `0.5`", manifest)
            self.assertIn("built-in atomic densities", manifest)

    def test_run_multiwfn_grid_vdw_surface_cube_keeps_vdw_map_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            surface_cube = root / "density_surface.cub"
            surface_cube.write_text(DENSITY_CUBE, encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "vdWpot.cub").write_text(VDW_POTENTIAL_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="vdw-potential",
                        surface_cube=surface_cube,
                        stem="case",
                        grid_points=(8, 8, 8),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.surface_cube, surface_cube.resolve())
            self.assertEqual(result.mapped_preset, "vdw-map")
            self.assertEqual(result.cube.name, "case_vdw-potential.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(result.vesta_result.vesta_path.name, "case_vdw-potential_vdw-map_cube.vesta")
            self.assertIn("IMPORT_TEXTURE", result.vesta_result.vesta_path.read_text(encoding="utf-8"))
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `vdw-map`", manifest)
            self.assertIn("texture_cube:", manifest)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("mapped_vesta_preset: `vdw-map`", recipe)

    def test_run_multiwfn_grid_can_map_generated_texture_on_surface_cube(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            surface_cube = root / "density_surface.cub"
            surface_cube.write_text(DENSITY_CUBE, encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "totesp.cub").write_text(DENSITY_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="esp",
                        surface_cube=surface_cube,
                        stem="case",
                        grid_points=(8, 8, 8),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.surface_cube, surface_cube.resolve())
            self.assertEqual(result.mapped_preset, "esp")
            self.assertEqual(result.cube.name, "case_esp.cub")
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(result.vesta_result.vesta_path.name, "case_esp_esp_cube.vesta")
            self.assertIn("IMPORT_TEXTURE", result.vesta_result.vesta_path.read_text(encoding="utf-8"))
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("requested_preset: `esp`", manifest)
            self.assertIn("texture_cube:", manifest)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("surface_cube_for_texture_map:", recipe)
            self.assertIn("mapped_vesta_preset: `esp`", recipe)

    def test_run_multiwfn_grid_surface_cube_passes_texture_scaling_options(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            surface_cube = root / "density_surface.cub"
            surface_cube.write_text(DENSITY_CUBE, encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "userfunc.cub").write_text(USER_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="local-hardness",
                        surface_cube=surface_cube,
                        tex_physical=(-0.1, 0.1),
                        tex_range_source="surface-band",
                        surface_band=0.25,
                        surface_nearest=4,
                        stem="case",
                        grid_points=(8, 8, 8),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.user_function_index, 29)
            self.assertEqual(result.mapped_preset, "surface-map")
            self.assertEqual(result.tex_physical, (-0.1, 0.1))
            self.assertEqual(result.tex_range_source, "surface-band")
            self.assertEqual(result.surface_band, 0.25)
            self.assertEqual(result.surface_nearest, 4)
            self.assertIsNotNone(result.vesta_result)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `surface-map`", manifest)
            self.assertIn("effective_tex_physical: `-0.1` to `0.1`", manifest)
            self.assertIn("tex_reference_source: `surface-band`", manifest)
            self.assertIn("surface_band: `0.25`", manifest)
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("user_function_index_iuserfunc: `29`", recipe)
            self.assertIn("mapped_tex_physical: `(-0.1, 0.1)`", recipe)
            self.assertIn("mapped_tex_range_source: `surface-band`", recipe)
            self.assertIn("mapped_surface_nearest: `4`", recipe)

    def test_run_multiwfn_grid_rejects_texture_scaling_without_surface_cube(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "require --surface-cube"):
                run_multiwfn_grid(
                    wavefunction,
                    root / "products",
                    tex_physical=(-0.1, 0.1),
                )

    def test_run_multiwfn_grid_rejects_negative_surface_band(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            surface_cube = root / "density_surface.cub"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            surface_cube.write_text(DENSITY_CUBE, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "--surface-band must be non-negative"):
                run_multiwfn_grid(
                    wavefunction,
                    root / "products",
                    surface_cube=surface_cube,
                    tex_range_source="surface-band",
                    surface_band=-0.1,
                )

    def test_run_multiwfn_grid_can_skip_vesta_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                Path(kwargs["cwd"], "density.cub").write_text(DENSITY_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(wavefunction, root / "products", make_vesta=False)

            self.assertTrue(result.success)
            self.assertTrue(result.cube.exists())
            self.assertIsNone(result.vesta_result)

    def test_run_multiwfn_grid_expected_cube_keeps_relative_subdirectory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                nested = Path(kwargs["cwd"]) / "nested"
                nested.mkdir()
                (nested / "custom.cub").write_text(DENSITY_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        commands=["5", "1", "0", "q"],
                        expected_cube=Path("nested/custom.cub"),
                        make_vesta=False,
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.raw_cube, root / "products" / "multiwfn_grid_raw" / "nested" / "custom.cub")
            self.assertTrue(result.cube.exists())

    def test_run_multiwfn_grid_batch_writes_isolated_orbital_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "MOvalue.cub").write_text(DENSITY_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_grid_batch(
                        wavefunction,
                        root / "batch",
                        orbitals=["h", "l+1"],
                        grid_points=(6, 7, 8),
                        stem="case",
                        make_vesta=False,
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.cli_returncode, 0)
            self.assertEqual(len(result.results), 2)
            self.assertEqual(mocked_run.call_count, 2)
            first, second = result.results
            self.assertEqual(first.command_file.read_text(encoding="utf-8"), "5\n4\nh\n4\n6,7,8\n2\n0\nq\n")
            self.assertEqual(second.command_file.read_text(encoding="utf-8"), "5\n4\nl+1\n4\n6,7,8\n2\n0\nq\n")
            self.assertEqual(first.output_dir.name, "001_orbital_h")
            self.assertEqual(second.output_dir.name, "002_orbital_lplus1")
            self.assertEqual(first.cube.name, "case_h_orbital.cub")
            self.assertEqual(second.cube.name, "case_lplus1_orbital.cub")
            manifest = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("orbitals: `h, l+1`", manifest)
            self.assertIn("completed_runs: `2`", manifest)
            self.assertIn("requested_orbital: `l+1`", manifest)
            self.assertIn("safe_label: `lplus1`", manifest)
            self.assertIn("status: `success`", manifest)

    def test_run_multiwfn_grid_batch_stops_after_failure_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_grid.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(candidate.path)], 7, stdout="", stderr="bad"),
                ) as mocked_run:
                    result = run_multiwfn_grid_batch(
                        wavefunction,
                        root / "batch",
                        orbitals=["h", "l"],
                        make_vesta=False,
                    )

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, 7)
            self.assertEqual(len(result.results), 1)
            self.assertEqual(mocked_run.call_count, 1)
            manifest = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("failed_runs: `1`", manifest)
            self.assertIn("skipped_runs: `1`", manifest)
            self.assertIn("status: `failed`", manifest)
            self.assertIn("status: `skipped`", manifest)

    def test_run_multiwfn_grid_batch_keep_going_after_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)
            calls = {"count": 0}

            def fake_run(command, **kwargs):
                calls["count"] += 1
                if calls["count"] == 1:
                    return subprocess.CompletedProcess(command, 7, stdout="", stderr="bad")
                Path(kwargs["cwd"], "MOvalue.cub").write_text(DENSITY_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid_batch(
                        wavefunction,
                        root / "batch",
                        orbitals=["h", "l"],
                        make_vesta=False,
                        keep_going=True,
                    )

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, 7)
            self.assertEqual(len(result.results), 2)
            self.assertFalse(result.results[0].success)
            self.assertTrue(result.results[1].success)

    def test_run_multiwfn_grid_batch_rejects_non_orbital_function(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "requires an orbital function"):
                run_multiwfn_grid_batch(
                    Path(tmp) / "h2o.fch",
                    Path(tmp) / "batch",
                    function_name="density",
                    orbitals=["h"],
                )

    def test_main_batch_orbitals_defaults_to_orbital_function(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                Path(kwargs["cwd"], "MOvalue.cub").write_text(DENSITY_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    with patch("sys.stdout", io.StringIO()):
                        code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                            [
                                str(wavefunction),
                                str(root / "batch"),
                                "--orbitals",
                                "h",
                                "l",
                                "--grid-mode",
                                "low",
                                "--no-vesta",
                            ]
                        )

            self.assertEqual(code, 0)
            first = root / "batch" / "001_orbital_h" / "multiwfn_grid_input.txt"
            second = root / "batch" / "002_orbital_l" / "multiwfn_grid_input.txt"
            self.assertEqual(first.read_text(encoding="utf-8"), "5\n4\nh\n1\n2\n0\nq\n")
            self.assertEqual(second.read_text(encoding="utf-8"), "5\n4\nl\n1\n2\n0\nq\n")

    def test_main_source_function_accepts_reference_options(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                Path(kwargs["cwd"], "srcfunc.cub").write_text(SOURCE_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    with patch("sys.stdout", io.StringIO()):
                        code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                            [
                                str(wavefunction),
                                str(root / "products"),
                                "--function",
                                "srcfunc",
                                "--reference-point",
                                "1",
                                "2",
                                "3",
                                "--source-function-mode",
                                "2",
                                "--grid-mode",
                                "low",
                                "--no-vesta",
                            ]
                        )

            self.assertEqual(code, 0)
            self.assertEqual(
                (root / "products" / "multiwfn_grid_input.txt").read_text(encoding="utf-8"),
                "1000\n1\n1.0,2.0,3.0\n5\n19\n1\n2\n0\nq\n",
            )
            settings = root / "products" / "multiwfn_grid_raw" / "multiwfn_grid_settings.ini"
            self.assertIn("srcfuncmode= 2", settings.read_text(encoding="utf-8"))

    def test_main_elf_accepts_elflol_type_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                Path(kwargs["cwd"], "ELF.cub").write_text(DENSITY_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    with patch("sys.stdout", io.StringIO()):
                        code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                            [
                                str(wavefunction),
                                str(root / "products"),
                                "--function",
                                "elf",
                                "--elflol-type",
                                "tian-lu",
                                "--grid-mode",
                                "low",
                                "--no-vesta",
                            ]
                        )

            self.assertEqual(code, 0)
            self.assertEqual(
                (root / "products" / "multiwfn_grid_input.txt").read_text(encoding="utf-8"),
                "5\n9\n1\n2\n0\nq\n",
            )
            settings = root / "products" / "multiwfn_grid_raw" / "multiwfn_grid_settings.ini"
            self.assertIn("ELFLOL_type= 2", settings.read_text(encoding="utf-8"))

    def test_main_vdw_accepts_probe_symbol(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                Path(kwargs["cwd"], "vdWpot.cub").write_text(VDW_POTENTIAL_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    with patch("sys.stdout", io.StringIO()):
                        code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                            [
                                str(wavefunction),
                                str(root / "products"),
                                "--function",
                                "vdw-potential",
                                "--vdw-probe",
                                "O",
                                "--grid-mode",
                                "low",
                                "--no-vesta",
                            ]
                        )

            self.assertEqual(code, 0)
            self.assertEqual(
                (root / "products" / "multiwfn_grid_input.txt").read_text(encoding="utf-8"),
                "5\n25\n1\n2\n0\nq\n",
            )
            settings = root / "products" / "multiwfn_grid_raw" / "multiwfn_grid_settings.ini"
            self.assertIn("ivdwprobe= 8", settings.read_text(encoding="utf-8"))

    def test_main_pair_function_accepts_reference_and_pair_options(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                Path(kwargs["cwd"], "fermihole.cub").write_text(PAIR_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    with patch("sys.stdout", io.StringIO()):
                        code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                            [
                                str(wavefunction),
                                str(root / "products"),
                                "--function",
                                "fermihole",
                                "--reference-point",
                                "1",
                                "2",
                                "3",
                                "--pair-function-type",
                                "12",
                                "--pair-correlation-type",
                                "1",
                                "--grid-mode",
                                "low",
                                "--no-vesta",
                            ]
                        )

            self.assertEqual(code, 0)
            self.assertEqual(
                (root / "products" / "multiwfn_grid_input.txt").read_text(encoding="utf-8"),
                "1000\n1\n1.0,2.0,3.0\n5\n17\n1\n2\n0\nq\n",
            )
            settings = root / "products" / "multiwfn_grid_raw" / "multiwfn_grid_settings.ini"
            settings_text = settings.read_text(encoding="utf-8")
            self.assertIn("pairfunctype= 12", settings_text)
            self.assertIn("paircorrtype= 1", settings_text)

    def test_main_user_function_accepts_iuserfunc_option(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                Path(kwargs["cwd"], "userfunc.cub").write_text(USER_FUNCTION_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    with patch("sys.stdout", io.StringIO()):
                        code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                            [
                                str(wavefunction),
                                str(root / "products"),
                                "--function",
                                "userfunc",
                                "--user-function-index",
                                "-27",
                                "--grid-mode",
                                "low",
                                "--no-vesta",
                            ]
                        )

            self.assertEqual(code, 0)
            self.assertEqual(
                (root / "products" / "multiwfn_grid_input.txt").read_text(encoding="utf-8"),
                "5\n100\n1\n2\n0\nq\n",
            )
            settings = root / "products" / "multiwfn_grid_raw" / "multiwfn_grid_settings.ini"
            self.assertIn("iuserfunc= -27", settings.read_text(encoding="utf-8"))

    def test_main_rejects_batch_single_orbital_conflict(self):
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                [
                    "input.fch",
                    "products",
                    "--orbital",
                    "h",
                    "--orbitals",
                    "l",
                ]
            )

        self.assertEqual(code, 2)
        self.assertIn("--orbital and --orbitals cannot be used together", stderr.getvalue())

    def test_main_rejects_batch_custom_command_stream_options(self):
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                [
                    "input.fch",
                    "products",
                    "--orbitals",
                    "h",
                    "l",
                    "--commands-file",
                    "commands.txt",
                ]
            )

        self.assertEqual(code, 2)
        self.assertIn("--commands-file and --expected-cube", stderr.getvalue())

    def test_main_rejects_batch_raw_dir_override(self):
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                [
                    "input.fch",
                    "products",
                    "--function",
                    "orbital",
                    "--orbitals",
                    "h",
                    "l",
                    "--raw-dir",
                    "shared_raw",
                ]
            )

        self.assertEqual(code, 2)
        self.assertIn("--raw-dir is not supported with --orbitals", stderr.getvalue())

    def test_main_rejects_batch_surface_cube(self):
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                [
                    "input.fch",
                    "products",
                    "--function",
                    "orbital",
                    "--orbitals",
                    "h",
                    "l",
                    "--surface-cube",
                    "density.cub",
                ]
            )

        self.assertEqual(code, 2)
        self.assertIn("--surface-cube is not supported with --orbitals", stderr.getvalue())

    def test_main_rejects_batch_source_function_options(self):
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                [
                    "input.fch",
                    "products",
                    "--orbitals",
                    "h",
                    "l",
                    "--reference-point",
                    "1",
                    "2",
                    "3",
                ]
            )

        self.assertEqual(code, 2)
        self.assertIn("--reference-point", stderr.getvalue())

    def test_main_rejects_batch_user_function_options(self):
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                [
                    "input.fch",
                    "products",
                    "--orbitals",
                    "h",
                    "l",
                    "--user-function-index",
                    "27",
                ]
            )

        self.assertEqual(code, 2)
        self.assertIn("--user-function-index", stderr.getvalue())

    def test_main_rejects_keep_going_without_batch(self):
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                ["input.fch", "products", "--keep-going"]
            )

        self.assertEqual(code, 2)
        self.assertIn("--keep-going is only supported with --orbitals", stderr.getvalue())

    def test_run_multiwfn_grid_reports_missing_cube(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_grid.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(candidate.path)], 0, stdout="ok", stderr=""),
                ):
                    result = run_multiwfn_grid(wavefunction, root / "products")

        self.assertFalse(result.success)
        self.assertEqual(result.cli_returncode, GRID_OUTPUT_MISSING_CODE)
        self.assertIn("expected grid cube output", result.error or "")
        self.assertIsNone(result.cube)
        self.assertIsNone(result.vesta_result)

    def test_run_multiwfn_grid_records_nonzero_multiwfn_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_grid.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(candidate.path)], 7, stdout="bad", stderr="failed"),
                ):
                    result = run_multiwfn_grid(wavefunction, root / "products")

            self.assertFalse(result.success)
            self.assertEqual(result.returncode, 7)
            self.assertEqual(result.cli_returncode, 7)
            self.assertIn("return code 7", result.error or "")
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "bad")
            self.assertEqual(result.stderr_log.read_text(encoding="utf-8"), "failed")

    def test_run_multiwfn_grid_timeout_writes_partial_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                raise subprocess.TimeoutExpired(command, timeout=5, output="partial stdout", stderr="partial stderr")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(wavefunction, root / "products", timeout=5)

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, GRID_PROCESSING_FAILED_CODE)
            self.assertIn("timed out after 5 seconds", result.error or "")
            self.assertIn("partial stdout", result.stdout_log.read_text(encoding="utf-8"))
            self.assertIn("partial stderr", result.stderr_log.read_text(encoding="utf-8"))
            self.assertIn("timed out", result.recipe_path.read_text(encoding="utf-8"))

    def test_run_multiwfn_grid_launch_error_writes_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=OSError("boom")):
                    result = run_multiwfn_grid(wavefunction, root / "products")

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, GRID_PROCESSING_FAILED_CODE)
            self.assertIn("Failed to launch", result.error or "")
            self.assertIn("boom", result.stderr_log.read_text(encoding="utf-8"))

    def test_run_multiwfn_grid_requires_wavefunction(self):
        candidate = self.make_candidate(Path(tempfile.mkdtemp()))
        with tempfile.TemporaryDirectory() as tmp:
            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with self.assertRaises(FileNotFoundError):
                    run_multiwfn_grid(Path(tmp) / "missing.fch", Path(tmp) / "products")

    def test_main_reports_discovery_errors_without_traceback(self):
        stderr = io.StringIO()
        with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=None):
            with patch("sys.stderr", stderr):
                code = __import__("multiwfn2vesta.multiwfn_grid", fromlist=["main"]).main(
                    ["missing.fch", "products"]
                )

        self.assertEqual(code, 2)
        self.assertIn("Cannot find Multiwfn", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
