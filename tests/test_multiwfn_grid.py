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
        self.assertIn("preset=vdw-potential", text)
        self.assertIn("preset=electron-delocalization-range", text)
        self.assertIn("preset=orbital-overlap-distance", text)
        self.assertIn("preset=source-function", text)
        self.assertIn("preset=becke-weight", text)
        self.assertIn("preset=hirshfeld-weight", text)
        self.assertIn("promolecular-rdg", text)
        self.assertIn("alie", text)
        self.assertIn("mapped preset with --surface-cube: esp", text)
        self.assertIn("mapped preset with --surface-cube: alie", text)
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
        self.assertEqual(resolve_grid_function("van-der-waals-potential").index, 25)
        self.assertEqual(resolve_grid_function("edr").index, 20)
        self.assertEqual(resolve_grid_function("edr").output_filename, "EDR.cub")
        self.assertEqual(resolve_grid_function("edrdmax").index, 21)
        self.assertEqual(resolve_grid_function("edrdmax").output_filename, "EDRDmax.cub")
        self.assertEqual(resolve_grid_function("d(r)").preset, "orbital-overlap-distance")
        self.assertEqual(resolve_grid_function("source-function").index, 19)
        self.assertEqual(resolve_grid_function("srcfunc").output_filename, "srcfunc.cub")
        self.assertEqual(resolve_grid_function("source").preset, "source-function")
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

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "vdWpot.cub").write_text(VDW_POTENTIAL_CUBE, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="")

            with patch("multiwfn2vesta.multiwfn_grid.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_grid.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_grid(
                        wavefunction,
                        root / "products",
                        function_name="vdw",
                        stem="case",
                        grid_points=(10, 11, 12),
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "5\n25\n4\n10,11,12\n2\n0\nq\n")
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
            self.assertIn("auto_vesta_preset: `vdw-potential`", recipe)
            manifest = result.vesta_result.manifest_path.read_text(encoding="utf-8")
            self.assertIn("canonical_preset: `vdw-potential`", manifest)
            self.assertIn("effective_isosurface: `1.0`", manifest)
            self.assertIn("kcal/mol", manifest)

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
