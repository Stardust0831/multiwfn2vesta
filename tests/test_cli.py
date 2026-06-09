import io
import unittest
from unittest.mock import patch

from multiwfn2vesta import cli


class TestUnifiedCli(unittest.TestCase):
    def test_help_lists_maintained_workflows(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = cli.main(["--help"])

        self.assertEqual(code, 0)
        text = output.getvalue()
        self.assertIn("discover", text)
        self.assertIn("abacus-molden", text)
        self.assertIn("molden-check", text)
        self.assertIn("cube-vesta", text)
        self.assertIn("cube-preset", text)
        self.assertIn("abacus-mulliken-color", text)
        self.assertIn("aim-run", text)
        self.assertIn("aim-pdb", text)
        self.assertIn("aim-igmh", text)

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

    def test_dispatches_abacus_mulliken_color_command(self):
        with patch("multiwfn2vesta.cli.abacus_mulliken.main", return_value=0) as mocked:
            code = cli.main(["abacus-mulliken-color", "input.vesta", "mulliken.txt", "colored.vesta"])

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

    def test_dispatches_cube_preset_alias(self):
        with patch("multiwfn2vesta.cli.cube_preset.main", return_value=0) as mocked:
            code = cli.main(["preset", "density", "density.cub", "out"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["density", "density.cub", "out"])

    def test_unknown_command_returns_error(self):
        with patch("sys.stderr", io.StringIO()), patch("sys.stdout", io.StringIO()):
            code = cli.main(["unknown"])

        self.assertEqual(code, 2)

    def test_interactive_quit(self):
        with patch("builtins.input", return_value="q"), patch("sys.stdout", io.StringIO()):
            code = cli.main([])

        self.assertEqual(code, 0)

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
                "8",
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
                "7",
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


if __name__ == "__main__":
    unittest.main()
