import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.executables import ExecutableCandidate
from multiwfn2vesta.multiwfn_domain import (
    DOMAIN_OUTPUT_MISSING_CODE,
    build_domain_commands,
    run_multiwfn_domain,
)


DOMAIN_CUBE = """domain one
domain two
    2    -1.000000    -2.000000     0.500000
    2     0.500000     0.000000     0.000000
    2     0.000000     0.500000     0.000000
    2     0.000000     0.000000     0.500000
    8     8.000000    -1.000000    -2.000000     0.500000
    1     1.000000    -0.500000    -2.000000     0.500000
 0.0 0.0 0.0 1.0 1.0 1.0 0.0 0.0
"""


DOMAIN_PDB = """\
HETATM    1  C   DOM A   1      -0.500   0.000   0.500  1.00  0.00           C
HETATM    2  C   DOM A   1       0.000   0.500   0.500  1.00  0.00           C
END
"""


class TestMultiwfnDomainRunner(unittest.TestCase):
    def make_candidate(self, root):
        fake_exe = Path(root) / "Multiwfn_noGUI"
        fake_exe.write_text("#!/bin/sh\n", encoding="utf-8")
        fake_exe.chmod(0o755)
        return ExecutableCandidate("Multiwfn_noGUI", fake_exe, "test", True, True)

    def test_build_default_domain_command_stream(self):
        commands = build_domain_commands()

        self.assertEqual(commands, ["200", "14", "3", "<0.5", "-1", "10", "1", "11", "1", "0", "0", "q"])

    def test_build_domain_command_stream_validates_criterion_and_index(self):
        self.assertEqual(build_domain_commands(">0.001", 3)[3], ">0.001")
        with self.assertRaisesRegex(ValueError, "must start with"):
            build_domain_commands("0.5")
        with self.assertRaisesRegex(ValueError, "positive integer"):
            build_domain_commands("<0.5", 0)

    def test_run_multiwfn_domain_writes_outputs_and_vesta(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = root / "density.cub"
            cube.write_text(DOMAIN_CUBE, encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "domain.cub").write_text(DOMAIN_CUBE, encoding="utf-8")
                (cwd / "domain.pdb").write_text(DOMAIN_PDB, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="warn")

            with patch("multiwfn2vesta.multiwfn_domain.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_domain.subprocess.run", side_effect=fake_run) as mocked_run:
                    result = run_multiwfn_domain(
                        cube,
                        root / "products",
                        stem="case",
                        criterion="<0.5",
                        domain_index=1,
                        nthreads=2,
                    )

            self.assertTrue(result.success)
            self.assertEqual(result.cli_returncode, 0)
            self.assertEqual(mocked_run.call_args.args[0], [str(candidate.path), str(cube.resolve()), "-nt", "2"])
            self.assertEqual(mocked_run.call_args.kwargs["cwd"], str(root / "products" / "multiwfn_domain_raw"))
            self.assertEqual(mocked_run.call_args.kwargs["env"]["Multiwfnpath"], str(candidate.path.parent))
            self.assertEqual(result.command_file.read_text(encoding="utf-8"), "200\n14\n3\n<0.5\n-1\n10\n1\n11\n1\n0\n0\nq\n")
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "ok")
            self.assertEqual(result.stderr_log.read_text(encoding="utf-8"), "warn")
            self.assertEqual(result.domain_cube.name, "case_domain.cub")
            self.assertEqual(result.domain_pdb.name, "case_domain.pdb")
            self.assertTrue(result.domain_cube.exists())
            self.assertTrue(result.domain_pdb.exists())
            self.assertIsNotNone(result.vesta_result)
            self.assertEqual(result.vesta_result.vesta_path.name, "case_domain_cube.vesta")
            self.assertIn("canonical_preset: `domain`", result.vesta_result.manifest_path.read_text(encoding="utf-8"))
            recipe = result.recipe_path.read_text(encoding="utf-8")
            self.assertIn("criterion: `<0.5`", recipe)
            self.assertIn("domain_index: `1`", recipe)

    def test_run_multiwfn_domain_can_skip_vesta_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = root / "density.cub"
            cube.write_text(DOMAIN_CUBE, encoding="utf-8")
            candidate = self.make_candidate(root)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "domain.cub").write_text(DOMAIN_CUBE, encoding="utf-8")
                (cwd / "domain.pdb").write_text(DOMAIN_PDB, encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            with patch("multiwfn2vesta.multiwfn_domain.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_domain.subprocess.run", side_effect=fake_run):
                    result = run_multiwfn_domain(cube, root / "products", make_vesta=False)

            self.assertTrue(result.success)
            self.assertTrue(result.domain_cube.exists())
            self.assertTrue(result.domain_pdb.exists())
            self.assertIsNone(result.vesta_result)

    def test_run_multiwfn_domain_reports_missing_cube(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cube = root / "density.cub"
            cube.write_text(DOMAIN_CUBE, encoding="utf-8")
            candidate = self.make_candidate(root)

            with patch("multiwfn2vesta.multiwfn_domain.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_domain.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(candidate.path)], 0, stdout="ok", stderr=""),
                ):
                    result = run_multiwfn_domain(cube, root / "products")

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, DOMAIN_OUTPUT_MISSING_CODE)
            self.assertIn("required domain output is missing", result.error or "")
            self.assertIsNone(result.vesta_result)

    def test_main_reports_discovery_errors_without_traceback(self):
        stderr = io.StringIO()
        with patch("multiwfn2vesta.multiwfn_domain.find_multiwfn", return_value=None):
            with patch("sys.stderr", stderr):
                code = __import__("multiwfn2vesta.multiwfn_domain", fromlist=["main"]).main(
                    ["missing.cub", "products"]
                )

        self.assertEqual(code, 2)
        self.assertIn("domain-run:", stderr.getvalue())
        self.assertIn("Cannot find Multiwfn", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
