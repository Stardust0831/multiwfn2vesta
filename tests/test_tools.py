import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta import cli, tools


class TestHumanFacingTools(unittest.TestCase):
    def test_tools_list_supports_chinese(self):
        stdout = io.StringIO()
        with patch("sys.stdout", stdout):
            code = tools.main(["--lang", "zh"])

        self.assertEqual(code, 0)
        text = stdout.getvalue()
        self.assertIn("multiwfn2vesta 稳定工具", text)
        self.assertIn("esp-surface", text)
        self.assertIn("excitation-bridge", text)

    def test_global_cli_help_supports_chinese(self):
        stdout = io.StringIO()
        with patch("sys.stdout", stdout):
            code = cli.main(["--lang", "zh", "--help"])

        self.assertEqual(code, 0)
        self.assertIn("稳定 tools", stdout.getvalue())

    def test_tools_run_forwards_excitation_bridge(self):
        with patch("multiwfn2vesta.tools.abacus_lr_to_multiwfn.main", return_value=0) as mocked:
            code = tools.main(["run", "excitation-bridge", "--", "OUT.lr", "state.excit.txt", "--label", "singlet"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["OUT.lr", "state.excit.txt", "--label", "singlet"])

    def test_tools_run_esp_surface_sample_outputs_vesta(self):
        root = Path(__file__).resolve().parents[1]
        density = root / "examples" / "cof_direct_cube_suite" / "sample_esp" / "rho_demo.cube"
        esp = root / "examples" / "cof_direct_cube_suite" / "sample_esp" / "potes_demo.cube"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "esp_surface"
            stdout = io.StringIO()
            with patch("sys.stdout", stdout):
                code = tools.main(
                    [
                        "run",
                        "esp-surface",
                        "--",
                        str(density),
                        str(esp),
                        str(out),
                        "--axis",
                        "z",
                        "--vacuum-side",
                        "high",
                        "--vacuum-fraction",
                        "0.5",
                        "--tex-physical",
                        "-3.5",
                        "1.5",
                    ]
                )

            self.assertEqual(code, 0)
            shifted = out / "potes_demo_vacuum0.cube"
            report = out / "potes_demo_alignment.md"
            vesta = out / "vesta" / "esp_surface_cube.vesta"
            recipe = out / "vesta" / "esp_surface_cube_vesta_recipe.md"
            self.assertTrue(shifted.exists())
            self.assertTrue(report.exists())
            self.assertTrue(vesta.exists())
            self.assertTrue(recipe.exists())
            self.assertIn("subtracted_offset: `4.500000000000E+00`", report.read_text(encoding="utf-8"))
            vesta_text = vesta.read_text(encoding="utf-8")
            self.assertIn("IMPORT_TEXTURE", vesta_text)
            self.assertIn("BONDS   1", vesta_text)
            self.assertIn("TEX3P", vesta_text)
            self.assertIn("vesta:", stdout.getvalue())

    def test_interactive_guided_esp_surface_builds_outputs(self):
        root = Path(__file__).resolve().parents[1]
        density = root / "examples" / "cof_direct_cube_suite" / "sample_esp" / "rho_demo.cube"
        esp = root / "examples" / "cof_direct_cube_suite" / "sample_esp" / "potes_demo.cube"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "guided_esp"
            answers = iter(
                [
                    "4",
                    "n",
                    str(density),
                    str(esp),
                    str(out),
                    "z",
                    "high",
                    "0.5",
                    "0.001",
                    "-3.5 1.5",
                    "",
                    "y",
                ]
            )
            stdout = io.StringIO()
            with patch("builtins.input", lambda _prompt: next(answers)), patch("sys.stdout", stdout):
                code = tools.main(["interactive", "--lang", "zh"])

            self.assertEqual(code, 0)
            self.assertTrue((out / "potes_demo_vacuum0.cube").exists())
            self.assertTrue((out / "vesta" / "esp_surface_cube.vesta").exists())
            self.assertIn("将使用的参数", stdout.getvalue())

    def test_interactive_manual_mode_forwards_raw_args(self):
        answers = iter(["5", "y", "OUT.lr state.excit.txt --label singlet", "y"])
        with patch("builtins.input", lambda _prompt: next(answers)), patch("sys.stdout", io.StringIO()):
            with patch("multiwfn2vesta.tools.abacus_lr_to_multiwfn.main", return_value=0) as mocked:
                code = tools.main(["interactive", "--lang", "en"])

        self.assertEqual(code, 0)
        mocked.assert_called_once_with(["OUT.lr", "state.excit.txt", "--label", "singlet"])


if __name__ == "__main__":
    unittest.main()
