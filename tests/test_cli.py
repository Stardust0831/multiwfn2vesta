import io
from pathlib import Path
import unittest
from unittest.mock import patch

from multiwfn2vesta import cli


class TestUnifiedCli(unittest.TestCase):
    def test_packaging_entry_points_cover_atom_coloring_commands(self):
        root = Path(__file__).resolve().parents[1]
        pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
        setup_py = (root / "setup.py").read_text(encoding="utf-8")
        expected = (
            "multiwfn2vesta-tools=multiwfn2vesta.tools:main",
            "multiwfn2vesta-abacus-mulliken-color=multiwfn2vesta.abacus_mulliken:main",
            "multiwfn2vesta-multiwfn-atom-color=multiwfn2vesta.multiwfn_atom_table:main",
        )
        for entry in expected:
            pyproject_entry = entry.replace("=", ' = "')
            self.assertIn(pyproject_entry, pyproject)
            self.assertIn(entry, setup_py)

    def test_help_lists_maintained_workflows(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = cli.main(["--help"])

        self.assertEqual(code, 0)
        text = output.getvalue()
        self.assertIn("discover", text)
        self.assertIn("tools", text)
        self.assertIn("abacus-molden", text)
        self.assertIn("molden-check", text)
        self.assertIn("cube-vesta", text)
        self.assertIn("cube-preset", text)
        self.assertIn("surface-extrema", text)
        self.assertIn("cube-arith", text)
        self.assertIn("iri-run", text)
        self.assertIn("igmh-run", text)
        self.assertIn("igm-run", text)
        self.assertIn("migm-run", text)
        self.assertIn("aigm-run", text)
        self.assertIn("amigm-run", text)
        self.assertIn("grid-run", text)
        self.assertIn("fukui-run", text)
        self.assertIn("stm-run", text)
        self.assertIn("domain-run", text)
        self.assertIn("abacus-mulliken-color", text)
        self.assertIn("multiwfn-atom-color", text)
        self.assertIn("aim-run", text)
        self.assertIn("aim-pdb", text)
        self.assertIn("aim-igmh", text)
        self.assertIn("trajectory-frames", text)
        self.assertIn("trajectory-video", text)
        self.assertIn("examples", text)

    def test_dispatches_discover_command(self):
        with patch("multiwfn2vesta.cli.discovery_report", return_value="report\n") as mocked:
            output = io.StringIO()
            with patch("sys.stdout", output):
                code = cli.main(["discover"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with()
        self.assertEqual(output.getvalue(), "report\n")

    def test_dispatches_aim_run_command(self):
        with patch("multiwfn2vesta.cli.multiwfn_aim.main", return_value=0) as mocked:
            code = cli.main(["aim-run", "input.molden", "out", "--timeout", "30"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.molden", "out", "--timeout", "30"])

    def test_dispatches_abacus_molden_command(self):
        with patch("multiwfn2vesta.cli.abacus_molden.main", return_value=0) as mocked:
            code = cli.main(["abacus-molden", "calc", "ABACUS_Multiwfn.molden"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["calc", "ABACUS_Multiwfn.molden"])

    def test_dispatches_molden_check_command(self):
        with patch("multiwfn2vesta.cli.molden_check.main", return_value=0) as mocked:
            code = cli.main(["molden-check", "input.molden", "--abacus"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.molden", "--abacus"])

    def test_dispatches_cube_vesta_command(self):
        with patch("multiwfn2vesta.cli.cube_vesta.main", return_value=0) as mocked:
            code = cli.main(["cube-vesta", "density.cub", "products", "--isosurface", "0.01"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["density.cub", "products", "--isosurface", "0.01"])

    def test_dispatches_cube_preset_command(self):
        with patch("multiwfn2vesta.cli.cube_preset.main", return_value=0) as mocked:
            code = cli.main(["cube-preset", "orbital", "orb.cub", "products"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["orbital", "orb.cub", "products"])

    def test_dispatches_surface_extrema_command(self):
        with patch("multiwfn2vesta.cli.surface_extrema_vesta.main", return_value=0) as mocked:
            code = cli.main(["surface-extrema", "in.vesta", "surfanalysis.pdb", "out.vesta", "--surface-cube", "density.cub"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["in.vesta", "surfanalysis.pdb", "out.vesta", "--surface-cube", "density.cub"])

    def test_dispatches_surface_extrema_alias(self):
        with patch("multiwfn2vesta.cli.surface_extrema_vesta.main", return_value=0) as mocked:
            code = cli.main(["surf-extrema", "in.vesta", "surfanalysis.pdb", "out.vesta", "--surface-cube", "density.cub"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["in.vesta", "surfanalysis.pdb", "out.vesta", "--surface-cube", "density.cub"])

    def test_interactive_surface_extrema_builds_expected_args(self):
        answers = iter(
            [
                "13",
                "input.vesta",
                "surfanalysis.pdb",
                "out.vesta",
                "density.cub",
                "minima",
                "0.12",
                "y",
                "n",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.surface_extrema_vesta.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "input.vesta",
                "surfanalysis.pdb",
                "out.vesta",
                "--surface-cube",
                "density.cub",
                "--selection",
                "minima",
                "--radius",
                "0.12",
                "--label-extrema",
            ]
        )

    def test_dispatches_cube_arith_command(self):
        with patch("multiwfn2vesta.cli.cube_arith.main", return_value=0) as mocked:
            code = cli.main(["cube-arith", "products", "--term", "1", "a.cub", "--term", "-1", "b.cub"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["products", "--term", "1", "a.cub", "--term", "-1", "b.cub"])

    def test_dispatches_iri_run_command(self):
        with patch("multiwfn2vesta.cli.multiwfn_iri.main", return_value=0) as mocked:
            code = cli.main(["iri-run", "input.molden", "products", "--timeout", "300"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.molden", "products", "--timeout", "300"])

    def test_dispatches_igmh_run_command(self):
        with patch("multiwfn2vesta.cli.multiwfn_igmh.main", return_value=0) as mocked:
            code = cli.main(["igmh-run", "input.molden", "products", "--fragment", "1", "--fragment", "2"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.molden", "products", "--fragment", "1", "--fragment", "2"])

    def test_dispatches_igm_run_with_method_injection(self):
        with patch("multiwfn2vesta.cli.multiwfn_igmh.main_igm", return_value=0) as mocked:
            code = cli.main(["igm-run", "input.molden", "products", "--fragment", "1", "--fragment", "2"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.molden", "products", "--fragment", "1", "--fragment", "2"])

    def test_dispatches_migm_alias_with_method_injection(self):
        with patch("multiwfn2vesta.cli.multiwfn_igmh.main_migm", return_value=0) as mocked:
            code = cli.main(["multiwfn-migm", "input.molden", "products", "--fragment", "1", "--fragment", "2"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.molden", "products", "--fragment", "1", "--fragment", "2"])

    def test_dispatches_aigm_run_command(self):
        with patch("multiwfn2vesta.cli.multiwfn_aigm.main", return_value=0) as mocked:
            code = cli.main(["aigm-run", "traj.xyz", "products", "--fragment", "1", "--fragment", "2"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["traj.xyz", "products", "--fragment", "1", "--fragment", "2"])

    def test_dispatches_amigm_alias_with_method_injection(self):
        with patch("multiwfn2vesta.cli.multiwfn_aigm.main_amigm", return_value=0) as mocked:
            code = cli.main(["multiwfn-amigm", "traj.xyz", "products", "--fragment", "1", "--fragment", "2"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["traj.xyz", "products", "--fragment", "1", "--fragment", "2"])

    def test_dispatches_grid_run_command(self):
        with patch("multiwfn2vesta.cli.multiwfn_grid.main", return_value=0) as mocked:
            code = cli.main(["grid-run", "input.molden", "products", "--function", "density"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.molden", "products", "--function", "density"])

    def test_dispatches_fukui_run_command(self):
        with patch("multiwfn2vesta.cli.multiwfn_fukui.main", return_value=0) as mocked:
            code = cli.main(
                [
                    "fukui-run",
                    "products",
                    "--neutral",
                    "neutral.molden",
                    "--anion",
                    "anion.molden",
                    "--operation",
                    "fukui-plus",
                ]
            )

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "products",
                "--neutral",
                "neutral.molden",
                "--anion",
                "anion.molden",
                "--operation",
                "fukui-plus",
            ]
        )

    def test_dispatches_fukui_run_alias(self):
        with patch("multiwfn2vesta.cli.multiwfn_fukui.main", return_value=0) as mocked:
            code = cli.main(["dual-descriptor-run", "products", "--neutral", "n.molden"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["products", "--neutral", "n.molden"])

    def test_dispatches_stm_run_command(self):
        with patch("multiwfn2vesta.cli.multiwfn_stm.main", return_value=0) as mocked:
            code = cli.main(["stm-run", "input.molden", "products", "--grid-points", "10", "10", "6"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.molden", "products", "--grid-points", "10", "10", "6"])

    def test_dispatches_domain_run_command(self):
        with patch("multiwfn2vesta.cli.multiwfn_domain.main", return_value=0) as mocked:
            code = cli.main(["domain-run", "density.cub", "products", "--criterion", "<0.5"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["density.cub", "products", "--criterion", "<0.5"])

    def test_dispatches_domain_run_alias(self):
        with patch("multiwfn2vesta.cli.multiwfn_domain.main", return_value=0) as mocked:
            code = cli.main(["cube-domain", "density.cub", "products"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["density.cub", "products"])

    def test_dispatches_abacus_mulliken_color_command(self):
        with patch("multiwfn2vesta.cli.abacus_mulliken.main", return_value=0) as mocked:
            code = cli.main(["abacus-mulliken-color", "input.vesta", "mulliken.txt", "colored.vesta"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.vesta", "mulliken.txt", "colored.vesta"])

    def test_dispatches_multiwfn_atom_color_command(self):
        with patch("multiwfn2vesta.cli.multiwfn_atom_table.main", return_value=0) as mocked:
            code = cli.main(["multiwfn-atom-color", "input.vesta", "atom_values.csv", "colored.vesta"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.vesta", "atom_values.csv", "colored.vesta"])

    def test_dispatches_multiwfn_atom_table_alias(self):
        with patch("multiwfn2vesta.cli.multiwfn_atom_table.main", return_value=0) as mocked:
            code = cli.main(["atom-table-color", "input.vesta", "atom_values.csv", "colored.vesta"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.vesta", "atom_values.csv", "colored.vesta"])

    def test_atom_color_alias_remains_abacus_mulliken_for_compatibility(self):
        with patch("multiwfn2vesta.cli.abacus_mulliken.main", return_value=0) as mocked:
            code = cli.main(["atom-color", "input.vesta", "mulliken.txt", "colored.vesta"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.vesta", "mulliken.txt", "colored.vesta"])

    def test_dispatches_aim_igmh_command(self):
        with patch("multiwfn2vesta.cli.aim_igmh_vesta.main", return_value=0) as mocked:
            code = cli.main(["aim-igmh", "input.vesta", "out", "--label-bcp-sites"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.vesta", "out", "--label-bcp-sites"])

    def test_dispatches_alias(self):
        with patch("multiwfn2vesta.cli.aim_igmh_vesta.main", return_value=0) as mocked:
            code = cli.main(["igmh", "input.vesta", "out"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.vesta", "out"])

    def test_dispatches_examples_command(self):
        with patch("multiwfn2vesta.cli.examples_index.main", return_value=0) as mocked:
            code = cli.main(["examples", "--status", "ready"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["--status", "ready"])

    def test_dispatches_trajectory_video_command(self):
        with patch("multiwfn2vesta.cli.trajectory_video.main", return_value=0) as mocked:
            code = cli.main(["trajectory-video", "png", "movie.mp4", "--bitrate", "20M"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["png", "movie.mp4", "--bitrate", "20M"])

    def test_dispatches_trajectory_frames_command(self):
        with patch("multiwfn2vesta.cli.trajectory_frames.main", return_value=0) as mocked:
            code = cli.main(["trajectory-frames", "traj.xyz", "frames", "--stride", "2"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["traj.xyz", "frames", "--stride", "2"])

    def test_dispatches_trajectory_frames_alias(self):
        with patch("multiwfn2vesta.cli.trajectory_frames.main", return_value=0) as mocked:
            code = cli.main(["traj-frames", "traj.xyz", "frames"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["traj.xyz", "frames"])

    def test_dispatches_trajectory_video_alias(self):
        with patch("multiwfn2vesta.cli.trajectory_video.main", return_value=0) as mocked:
            code = cli.main(["traj-video", "png", "movie.mp4"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["png", "movie.mp4"])

    def test_dispatches_examples_alias(self):
        with patch("multiwfn2vesta.cli.examples_index.main", return_value=0) as mocked:
            code = cli.main(["gallery", "--verify"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["--verify"])

    def test_dispatches_cube_preset_alias(self):
        with patch("multiwfn2vesta.cli.cube_preset.main", return_value=0) as mocked:
            code = cli.main(["preset", "density", "density.cub", "out"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["density", "density.cub", "out"])

    def test_dispatches_cube_arith_alias(self):
        with patch("multiwfn2vesta.cli.cube_arith.main", return_value=0) as mocked:
            code = cli.main(["fukui-cube", "products", "--operation", "fukui-plus"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["products", "--operation", "fukui-plus"])

    def test_dispatches_iri_run_alias(self):
        with patch("multiwfn2vesta.cli.multiwfn_iri.main", return_value=0) as mocked:
            code = cli.main(["rdg-run", "input.molden", "products"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.molden", "products"])

    def test_dispatches_grid_run_alias(self):
        with patch("multiwfn2vesta.cli.multiwfn_grid.main", return_value=0) as mocked:
            code = cli.main(["scalar-cube-run", "input.molden", "products"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.molden", "products"])

    def test_dispatches_stm_run_alias(self):
        with patch("multiwfn2vesta.cli.multiwfn_stm.main", return_value=0) as mocked:
            code = cli.main(["ldos-run", "input.molden", "products"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["input.molden", "products"])

    def test_unknown_command_returns_error(self):
        with patch("sys.stderr", io.StringIO()), patch("sys.stdout", io.StringIO()):
            code = cli.main(["unknown"])

        self.assertEqual(code, 2)

    def test_interactive_quit(self):
        with patch("builtins.input", return_value="q"), patch("sys.stdout", io.StringIO()):
            code = cli.main([])

        self.assertEqual(code, 0)

    def test_interactive_default_opens_stable_tools(self):
        with patch("builtins.input", return_value=""):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.tools.interactive", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with("en")

    def test_interactive_examples_still_available_by_number(self):
        with patch("builtins.input", return_value="19"):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.examples_index.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with([])

    def test_interactive_aim_igmh_builds_expected_args(self):
        answers = iter(
            [
                "3",
                "overlay.vesta",
                "products",
                "case",
                "y",
                "n",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.aim_igmh_vesta.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            ["overlay.vesta", "products", "--stem", "case", "--label-bcp-sites"]
        )

    def test_interactive_trajectory_frames_builds_expected_args(self):
        answers = iter(
            [
                "21",
                "traj.extxyz",
                "frames_out",
                "cdcl",
                "5",
                "crystal",
                "-0.05 1.05 -0.05 1.05 -0.05 1.05",
                "Cd Cl 0 3.5",
                "",
                "ref.vesta",
                "y",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.trajectory_frames.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "traj.extxyz",
                "frames_out",
                "--stem",
                "cdcl",
                "--stride",
                "5",
                "--structure",
                "crystal",
                "--boundary",
                "-0.05",
                "1.05",
                "-0.05",
                "1.05",
                "-0.05",
                "1.05",
                "--bond",
                "Cd",
                "Cl",
                "0",
                "3.5",
                "--reference-vesta",
                "ref.vesta",
                "--comps",
                "on",
            ]
        )

    def test_interactive_aim_run_builds_expected_args(self):
        answers = iter(
            [
                "1",
                "input.molden",
                "aim_out",
                "/opt/Multiwfn",
                "4",
                "120",
                "",
                "n",
                "surface.cub",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.multiwfn_aim.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "input.molden",
                "aim_out",
                "--multiwfn",
                "/opt/Multiwfn",
                "--nthreads",
                "4",
                "--timeout",
                "120",
                "--cube-frame-from-cube",
                "surface.cub",
            ]
        )

    def test_interactive_molden_check_builds_expected_args(self):
        answers = iter(["4", "ABACUS_Multiwfn.molden", "y"])
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.molden_check.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["ABACUS_Multiwfn.molden", "--abacus"])

    def test_interactive_abacus_molden_builds_expected_args(self):
        answers = iter(
            [
                "9",
                "calc",
                "out.molden",
                "/src/abacus",
                "origin/develop",
                "y",
                "8",
                "1.5,2",
                "y",
                "y",
                "120",
                "n",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.abacus_molden.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "calc",
                "out.molden",
                "--abacus-repo",
                "/src/abacus",
                "--git-ref",
                "origin/develop",
                "--fetch",
                "--ngto",
                "8",
                "--rel-r",
                "1.5,2",
                "--with-pseudo",
                "true",
                "--timeout",
                "120",
            ]
        )

    def test_interactive_cube_preset_builds_expected_args(self):
        answers = iter(
            [
                "6",
                "iri",
                "iri2.cub",
                "preset_products",
                "iri1.cub",
                "0.8",
                "-0.03 0.03",
                "molecule",
                "n",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.cube_preset.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "iri",
                "iri2.cub",
                "preset_products",
                "--texture-cube",
                "iri1.cub",
                "--isosurface",
                "0.8",
                "--tex-physical",
                "-0.03",
                "0.03",
                "--structure",
                "molecule",
                "--no-copy-cubes",
            ]
        )

    def test_interactive_iri_run_builds_expected_args(self):
        answers = iter(
            [
                "7",
                "input.molden",
                "iri_products",
                "/opt/Multiwfn",
                "6",
                "300",
                "case",
                "n",
                "rdg",
                "0.9",
                "-0.04 0.04",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.multiwfn_iri.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "input.molden",
                "iri_products",
                "--multiwfn",
                "/opt/Multiwfn",
                "--nthreads",
                "6",
                "--timeout",
                "300",
                "--stem",
                "case",
                "--preset",
                "rdg",
                "--isosurface",
                "0.9",
                "--tex-physical",
                "-0.04",
                "0.04",
            ]
        )

    def test_interactive_cube_arith_builds_expected_args(self):
        answers = iter(
            [
                "11",
                "arith_products",
                "dual-descriptor",
                "neutral.cub",
                "anion.cub",
                "cation.cub",
                "dual",
                "n",
                "signed",
                "0.01",
                "crystal",
                "n",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.cube_arith.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "arith_products",
                "--operation",
                "dual-descriptor",
                "--neutral-cube",
                "neutral.cub",
                "--anion-cube",
                "anion.cub",
                "--cation-cube",
                "cation.cub",
                "--stem",
                "dual",
                "--preset",
                "signed",
                "--isosurface",
                "0.01",
                "--structure",
                "crystal",
                "--no-copy-cubes",
            ]
        )

    def test_interactive_cube_arith_builds_spin_density_args(self):
        answers = iter(
            [
                "11",
                "spin_products",
                "spin-density",
                "alpha.cub",
                "beta.cub",
                "spin",
                "n",
                "auto",
                "",
                "auto",
                "y",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.cube_arith.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "spin_products",
                "--operation",
                "spin-density",
                "--plus-cube",
                "alpha.cub",
                "--minus-cube",
                "beta.cub",
                "--stem",
                "spin",
                "--preset",
                "auto",
                "--structure",
                "auto",
            ]
        )

    def test_interactive_grid_run_builds_expected_args(self):
        answers = iter(
            [
                "10",
                "input.molden",
                "grid_products",
                "h",
                "",
                "/opt/Multiwfn",
                "4",
                "180",
                "case",
                "points",
                "12 13 14",
                "n",
                "signed",
                "0.03",
                "",
                "molecule",
                "n",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.multiwfn_grid.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "input.molden",
                "grid_products",
                "--function",
                "orbital",
                "--orbital",
                "h",
                "--multiwfn",
                "/opt/Multiwfn",
                "--nthreads",
                "4",
                "--timeout",
                "180",
                "--stem",
                "case",
                "--grid-mode",
                "points",
                "--grid-points",
                "12",
                "13",
                "14",
                "--preset",
                "signed",
                "--isosurface",
                "0.03",
                "--structure",
                "molecule",
                "--no-copy-cubes",
            ]
        )

    def test_interactive_grid_run_builds_mapped_texture_scaling_args(self):
        answers = iter(
            [
                "10",
                "input.molden",
                "grid_products",
                "",
                "local-hardness",
                "",
                "",
                "",
                "case",
                "points",
                "12 13 14",
                "n",
                "auto",
                "",
                "density.cub",
                "-0.1 0.1",
                "surface-band",
                "0.25",
                "4",
                "crystal",
                "y",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.multiwfn_grid.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "input.molden",
                "grid_products",
                "--function",
                "local-hardness",
                "--stem",
                "case",
                "--grid-mode",
                "points",
                "--grid-points",
                "12",
                "13",
                "14",
                "--preset",
                "auto",
                "--surface-cube",
                "density.cub",
                "--tex-physical",
                "-0.1",
                "0.1",
                "--tex-range-source",
                "surface-band",
                "--surface-band",
                "0.25",
                "--surface-nearest",
                "4",
                "--structure",
                "crystal",
            ]
        )

    def test_interactive_grid_run_builds_batch_orbitals_args(self):
        answers = iter(
            [
                "10",
                "input.molden",
                "grid_products",
                "h l+1",
                "",
                "",
                "",
                "",
                "case",
                "low",
                "y",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.multiwfn_grid.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "input.molden",
                "grid_products",
                "--function",
                "orbital",
                "--orbitals",
                "h",
                "l+1",
                "--stem",
                "case",
                "--grid-mode",
                "low",
                "--no-vesta",
            ]
        )

    def test_interactive_grid_run_builds_vdw_probe_args(self):
        answers = iter(
            [
                "10",
                "input.molden",
                "grid_products",
                "",
                "vdw-potential",
                "O",
                "",
                "",
                "",
                "",
                "low",
                "y",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.multiwfn_grid.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "input.molden",
                "grid_products",
                "--function",
                "vdw-potential",
                "--vdw-probe",
                "O",
                "--grid-mode",
                "low",
                "--no-vesta",
            ]
        )

    def test_interactive_grid_run_builds_vdw_component_probe_args(self):
        answers = iter(
            [
                "10",
                "input.molden",
                "grid_products",
                "",
                "disp",
                "Xe",
                "",
                "",
                "",
                "",
                "low",
                "y",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.multiwfn_grid.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "input.molden",
                "grid_products",
                "--function",
                "disp",
                "--vdw-probe",
                "Xe",
                "--grid-mode",
                "low",
                "--no-vesta",
            ]
        )

    def test_interactive_fukui_run_builds_expected_args(self):
        answers = iter(
            [
                "17",
                "fukui_products",
                "neutral.molden",
                "all",
                "anion.molden",
                "cation.molden",
                "/opt/Multiwfn",
                "4",
                "300",
                "case",
                "points",
                "10 11 12",
                "n",
                "n",
                "signed",
                "0.02",
                "molecule",
                "n",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.multiwfn_fukui.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "fukui_products",
                "--neutral",
                "neutral.molden",
                "--operation",
                "all",
                "--anion",
                "anion.molden",
                "--cation",
                "cation.molden",
                "--multiwfn",
                "/opt/Multiwfn",
                "--nthreads",
                "4",
                "--timeout",
                "300",
                "--stem",
                "case",
                "--grid-mode",
                "points",
                "--grid-points",
                "10",
                "11",
                "12",
                "--preset",
                "signed",
                "--isosurface",
                "0.02",
                "--structure",
                "molecule",
                "--no-copy-cubes",
            ]
        )

    def test_interactive_aigm_run_builds_expected_args(self):
        answers = iter(
            [
                "18",
                "traj.xyz",
                "aigm_products",
                "amigm",
                "1-48",
                "c",
                "",
                "1 200",
                "/opt/Multiwfn",
                "6",
                "600",
                "case",
                "y",
                "spacing",
                "0.25",
                "y",
                "y",
                "y",
                "y",
                "n",
                "aigm",
                "0.008",
                "-0.05 0.05",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.multiwfn_aigm.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "traj.xyz",
                "aigm_products",
                "--method",
                "amigm",
                "--fragment",
                "1-48",
                "--fragment",
                "c",
                "--frame-range",
                "1",
                "200",
                "--multiwfn",
                "/opt/Multiwfn",
                "--nthreads",
                "6",
                "--timeout",
                "600",
                "--stem",
                "case",
                "--periodic",
                "--grid-mode",
                "spacing",
                "--grid-spacing",
                "0.25",
                "--export-rdg",
                "--export-tfi",
                "--tfi-vesta",
                "--export-scatter",
                "--preset",
                "aigm",
                "--isosurface",
                "0.008",
                "--tex-physical",
                "-0.05",
                "0.05",
            ]
        )

    def test_interactive_cube_vesta_builds_expected_args(self):
        answers = iter(
            [
                "5",
                "surface.cub",
                "cube_products",
                "texture.cub",
                "1.0",
                "-0.04 0.04",
                "molecule",
                "n",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.cube_vesta.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "surface.cub",
                "cube_products",
                "--texture-cube",
                "texture.cub",
                "--isosurface",
                "1.0",
                "--tex-physical",
                "-0.04",
                "0.04",
                "--structure",
                "molecule",
                "--no-copy-cubes",
            ]
        )

    def test_interactive_abacus_mulliken_color_builds_expected_args(self):
        answers = iter(
            [
                "8",
                "input.vesta",
                "mulliken.txt",
                "colored.vesta",
                "magnetism",
                "2",
                "-4 4",
                "0.0",
                "0",
                "values.csv",
                "n",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.abacus_mulliken.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "input.vesta",
                "mulliken.txt",
                "colored.vesta",
                "--property",
                "magnetism",
                "--step",
                "2",
                "--vmin",
                "-4",
                "--vmax",
                "4",
                "--center",
                "0.0",
                "--section-index",
                "0",
                "--write-values",
                "values.csv",
            ]
        )

    def test_interactive_multiwfn_atom_color_builds_expected_args(self):
        answers = iter(
            [
                "12",
                "input.vesta",
                "atom_values.csv",
                "colored.vesta",
                "charge",
                "Atom",
                "-1 1",
                "0.0",
                "0",
                "values.csv",
                "n",
            ]
        )
        with patch("builtins.input", lambda _prompt: next(answers)):
            with patch("sys.stdout", io.StringIO()):
                with patch("multiwfn2vesta.cli.multiwfn_atom_table.main", return_value=0) as mocked:
                    code = cli.main([])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(
            [
                "input.vesta",
                "atom_values.csv",
                "colored.vesta",
                "--value-column",
                "charge",
                "--key-column",
                "Atom",
                "--vmin",
                "-1",
                "--vmax",
                "1",
                "--center",
                "0.0",
                "--section-index",
                "0",
                "--write-values",
                "values.csv",
            ]
        )


if __name__ == "__main__":
    unittest.main()
