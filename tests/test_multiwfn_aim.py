import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta.executables import ExecutableCandidate
from multiwfn2vesta.multiwfn_aim import DEFAULT_AIM_COMMANDS, read_command_file, run_multiwfn_aim


class TestMultiwfnAimRunner(unittest.TestCase):
    def test_read_command_file_preserves_blank_lines_as_enter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "commands.txt"
            path.write_text("2\n\n  3  \nq\n", encoding="utf-8")

            self.assertEqual(read_command_file(path), ["2", "", "3", "q"])

    def test_run_multiwfn_aim_writes_logs_and_converts_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            fake_exe = root / "Multiwfn_noGUI"
            fake_exe.write_text("#!/bin/sh\n", encoding="utf-8")
            fake_exe.chmod(0o755)
            candidate = ExecutableCandidate("Multiwfn_noGUI", fake_exe, "test", True, True)

            def fake_run(command, **kwargs):
                cwd = Path(kwargs["cwd"])
                (cwd / "paths.pdb").write_text("paths", encoding="utf-8")
                (cwd / "CPs.pdb").write_text("cps", encoding="utf-8")
                (cwd / "mol.pdb").write_text("mol", encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, stdout="ok", stderr="warn")

            with patch("multiwfn2vesta.multiwfn_aim.find_multiwfn", return_value=candidate):
                with patch("multiwfn2vesta.multiwfn_aim.subprocess.run", side_effect=fake_run) as mocked_run:
                    with patch("multiwfn2vesta.multiwfn_aim.convert_aim_pdb_to_vesta") as mocked_convert:
                        result = run_multiwfn_aim(
                            wavefunction,
                            root / "out",
                            nthreads=2,
                            timeout=10,
                            output_vesta=Path("custom.vesta"),
                        )

            run_kwargs = mocked_run.call_args.kwargs
            self.assertEqual(mocked_run.call_args.args[0], [str(fake_exe), str(wavefunction.resolve()), "-nt", "2"])
            self.assertEqual(run_kwargs["cwd"], str(root / "out"))
            self.assertEqual(run_kwargs["timeout"], 10)
            self.assertEqual(run_kwargs["env"]["Multiwfnpath"], str(fake_exe.parent))
            self.assertEqual(run_kwargs["env"]["MULTIWFNPATH"], str(fake_exe.parent))
            self.assertEqual(result.returncode, 0)
            self.assertTrue(result.success)
            self.assertEqual(result.cli_returncode, 0)
            self.assertIsNone(result.error)
            self.assertEqual(result.output_vesta, root / "out" / "custom.vesta")
            self.assertIn("\n".join(DEFAULT_AIM_COMMANDS[:3]), result.command_file.read_text(encoding="utf-8"))
            self.assertEqual(result.stdout_log.read_text(encoding="utf-8"), "ok")
            self.assertEqual(result.stderr_log.read_text(encoding="utf-8"), "warn")
            mocked_convert.assert_called_once()
            self.assertEqual(mocked_convert.call_args.args[0], root / "out" / "paths.pdb")
            self.assertEqual(mocked_convert.call_args.args[1], root / "out" / "custom.vesta")

    def test_run_multiwfn_aim_marks_missing_paths_as_cli_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            fake_exe = root / "Multiwfn_noGUI"
            fake_exe.write_text("#!/bin/sh\n", encoding="utf-8")
            fake_exe.chmod(0o755)
            candidate = ExecutableCandidate("Multiwfn_noGUI", fake_exe, "test", True, True)

            with patch("multiwfn2vesta.multiwfn_aim.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_aim.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(fake_exe)], 0, stdout="ok", stderr=""),
                ):
                    with patch("multiwfn2vesta.multiwfn_aim.convert_aim_pdb_to_vesta") as mocked_convert:
                        result = run_multiwfn_aim(wavefunction, root / "out")

            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.cli_returncode, 3)
            self.assertFalse(result.success)
            self.assertIn("paths.pdb", result.error or "")
            self.assertIsNone(result.output_vesta)
            mocked_convert.assert_not_called()

    def test_run_multiwfn_aim_can_allow_missing_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wavefunction = root / "h2o.fch"
            wavefunction.write_text("wavefunction", encoding="utf-8")
            fake_exe = root / "Multiwfn_noGUI"
            fake_exe.write_text("#!/bin/sh\n", encoding="utf-8")
            fake_exe.chmod(0o755)
            candidate = ExecutableCandidate("Multiwfn_noGUI", fake_exe, "test", True, True)

            with patch("multiwfn2vesta.multiwfn_aim.find_multiwfn", return_value=candidate):
                with patch(
                    "multiwfn2vesta.multiwfn_aim.subprocess.run",
                    return_value=subprocess.CompletedProcess([str(fake_exe)], 0, stdout="ok", stderr=""),
                ):
                    result = run_multiwfn_aim(wavefunction, root / "out", require_paths=False)

            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.cli_returncode, 0)
            self.assertTrue(result.success)
            self.assertIsNone(result.error)

    def test_run_multiwfn_aim_requires_wavefunction(self):
        candidate = ExecutableCandidate("Multiwfn_noGUI", Path("/bin/true"), "test", True, True)
        with tempfile.TemporaryDirectory() as tmp:
            with patch("multiwfn2vesta.multiwfn_aim.find_multiwfn", return_value=candidate):
                with self.assertRaises(FileNotFoundError):
                    run_multiwfn_aim(Path(tmp) / "missing.fch", Path(tmp) / "out")


if __name__ == "__main__":
    unittest.main()
