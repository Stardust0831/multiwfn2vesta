import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.abacus_molden import (
    MOLDEN_SCRIPT_PATH,
    REQUIRED_CONVERTER_MODULES,
    check_python_modules,
    prepare_molden_script,
    run_abacus_molden,
)


ABACUS_MOLDEN = """[Molden Format]
[Cell]
  4.0 0.0 0.0
  0.0 4.0 0.0
  0.0 0.0 12.0
[Atoms] AU
C 1 6 0.0 0.0 0.0
H 2 1 0.0 0.0 1.8
[Nval]
C 4
H 1
[GTO]
1 0
s 1 1.00
  1.0 1.0
[5D7F]
[MO]
 Sym= A1
 Ene= -0.500
 Spin= Alpha
 Occup= 2.000
  1 0.100
"""


class TestAbacusMolden(unittest.TestCase):
    def test_run_abacus_molden_with_explicit_script_writes_logs_recipe_and_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            calc_dir = root / "calc"
            calc_dir.mkdir()
            script = root / "molden.py"
            script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            output = root / "products" / "ABACUS_Multiwfn.molden"

            def fake_run(command, **kwargs):
                if command[1].endswith("ABACUS_Multiwfn_abacus_molden.py"):
                    output.write_text(ABACUS_MOLDEN, encoding="utf-8")
                    return subprocess.CompletedProcess(command, 0, stdout="generated", stderr="warn")
                raise AssertionError(f"unexpected command: {command}")

            with patch("multiwfn2vesta.abacus_molden.subprocess.run", side_effect=fake_run) as mocked_run:
                result = run_abacus_molden(
                    calc_dir,
                    output,
                    script=script,
                    python_executable="pythonX",
                    ndigits=4,
                    ngto=8,
                    rel_r="1.5,2",
                    with_pseudo=True,
                    check_dependencies=False,
                )

            self.assertTrue(result.success)
            self.assertEqual(result.cli_returncode, 0)
            self.assertTrue(output.exists())
            self.assertEqual(result.source.origin, "file")
            self.assertEqual(result.source.source_path, str(script.resolve()))
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "generated")
            self.assertEqual(result.stderr_log.read_text(encoding="utf-8"), "warn")
            self.assertTrue(result.check_result.ok)
            self.assertIn("ABACUS Molden Recipe", result.recipe.read_text(encoding="utf-8"))
            self.assertIn("Result: OK", result.recipe.read_text(encoding="utf-8"))
            command = mocked_run.call_args.args[0]
            self.assertEqual(command[0], "pythonX")
            self.assertIn("-f", command)
            self.assertIn(str(calc_dir.resolve()), command)
            self.assertIn("-o", command)
            self.assertIn(str(output.resolve()), command)
            self.assertIn("--with-Nval", command)
            self.assertIn("true", command)
            self.assertIn("--with-pseudo", command)
            self.assertIn("true", command)

    def test_run_abacus_molden_reports_check_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            calc_dir = root / "calc"
            calc_dir.mkdir()
            script = root / "molden.py"
            script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            output = root / "bad.molden"

            def fake_run(command, **kwargs):
                output.write_text("[Molden Format]\n[Atoms] AU\n", encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

            with patch("multiwfn2vesta.abacus_molden.subprocess.run", side_effect=fake_run):
                result = run_abacus_molden(calc_dir, output, script=script, check_dependencies=False)

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, 1)
            self.assertIn("Result: FAILED", result.recipe.read_text(encoding="utf-8"))

    def test_run_abacus_molden_reports_missing_output_after_successful_converter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            calc_dir = root / "calc"
            calc_dir.mkdir()
            script = root / "molden.py"
            script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            output = root / "missing.molden"

            with patch(
                "multiwfn2vesta.abacus_molden.subprocess.run",
                return_value=subprocess.CompletedProcess(["python"], 0, stdout="ok", stderr=""),
            ):
                result = run_abacus_molden(calc_dir, output, script=script, check_dependencies=False)

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, 1)
            self.assertIn("did not write output Molden", result.error or "")
            self.assertIn("did not write output Molden", result.recipe.read_text(encoding="utf-8"))

    def test_run_abacus_molden_reports_missing_output_even_when_check_is_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            calc_dir = root / "calc"
            calc_dir.mkdir()
            script = root / "molden.py"
            script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            output = root / "missing_no_check.molden"

            with patch(
                "multiwfn2vesta.abacus_molden.subprocess.run",
                return_value=subprocess.CompletedProcess(["python"], 0, stdout="ok", stderr=""),
            ):
                result = run_abacus_molden(
                    calc_dir,
                    output,
                    script=script,
                    check_output=False,
                    check_dependencies=False,
                )

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, 1)
            self.assertIn("did not write output Molden", result.error or "")

    def test_run_abacus_molden_reports_missing_python_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            calc_dir = root / "calc"
            calc_dir.mkdir()
            script = root / "molden.py"
            script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            output = root / "missing_deps.molden"

            with patch("multiwfn2vesta.abacus_molden.check_python_modules", return_value=["scipy"]):
                result = run_abacus_molden(calc_dir, output, script=script, python_executable="pythonX")

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, 2)
            self.assertIn("missing scipy", result.error or "")
            self.assertIn("missing scipy", result.stderr_log.read_text(encoding="utf-8"))
            self.assertIn("--python", result.recipe.read_text(encoding="utf-8"))

    def test_run_abacus_molden_timeout_writes_partial_logs_and_recipe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            calc_dir = root / "calc"
            calc_dir.mkdir()
            script = root / "molden.py"
            script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            output = root / "timeout.molden"

            def fake_run(command, **kwargs):
                raise subprocess.TimeoutExpired(command, timeout=5, output="partial stdout", stderr="partial stderr")

            with patch("multiwfn2vesta.abacus_molden.subprocess.run", side_effect=fake_run):
                result = run_abacus_molden(
                    calc_dir,
                    output,
                    script=script,
                    timeout=5,
                    check_dependencies=False,
                )

            self.assertFalse(result.success)
            self.assertEqual(result.cli_returncode, 2)
            self.assertIn("timed out after 5 seconds", result.error or "")
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "partial stdout")
            self.assertIn("partial stderr", result.stderr_log.read_text(encoding="utf-8"))
            self.assertIn("timed out after 5 seconds", result.recipe.read_text(encoding="utf-8"))

    def test_check_python_modules_reports_missing_names_from_probe_stdout(self):
        completed = subprocess.CompletedProcess(["python"], 1, stdout="numpy,scipy\n", stderr="")
        with patch("multiwfn2vesta.abacus_molden.subprocess.run", return_value=completed) as mocked_run:
            missing = check_python_modules("pythonX", REQUIRED_CONVERTER_MODULES)

        self.assertEqual(missing, ["numpy", "scipy"])
        self.assertEqual(mocked_run.call_args.args[0][0], "pythonX")

    def test_prepare_molden_script_exports_from_git_ref_without_touching_worktree_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "abacus"
            repo.mkdir()
            output = root / "out" / "ABACUS_Multiwfn.molden"
            calls = []

            def fake_run(command, **kwargs):
                calls.append(command)
                if command[:2] == ["git", "rev-parse"]:
                    return subprocess.CompletedProcess(command, 0, stdout="abc123\n", stderr="")
                if command[:3] == ["git", "show", "-s"]:
                    return subprocess.CompletedProcess(command, 0, stdout="2026-06-10T00:00:00+00:00\n", stderr="")
                if command[:2] == ["git", "show"]:
                    self.assertEqual(command[2], f"origin/develop:{MOLDEN_SCRIPT_PATH}")
                    return subprocess.CompletedProcess(command, 0, stdout="#!/usr/bin/env python3\nprint('ok')\n", stderr="")
                raise AssertionError(f"unexpected command: {command}")

            with patch("multiwfn2vesta.abacus_molden.subprocess.run", side_effect=fake_run):
                source = prepare_molden_script(output_molden=output, abacus_repo=repo, git_ref="origin/develop")

            self.assertEqual(source.origin, "git")
            self.assertEqual(source.commit, "abc123")
            self.assertEqual(source.source_path, MOLDEN_SCRIPT_PATH)
            self.assertTrue(source.script_path.exists())
            self.assertIn("print('ok')", source.script_path.read_text(encoding="utf-8"))
            self.assertEqual(calls[0], ["git", "rev-parse", "origin/develop"])


if __name__ == "__main__":
    unittest.main()
