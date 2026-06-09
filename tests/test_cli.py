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
        self.assertIn("aim-pdb", text)
        self.assertIn("aim-igmh", text)

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
                "2",
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


if __name__ == "__main__":
    unittest.main()
