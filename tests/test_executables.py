import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from multiwfn2vesta import executables


class TestExecutableDiscovery(unittest.TestCase):
    def test_multiwfn_env_directory_candidate_uses_multiwfnpath_spelling(self):
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "Multiwfn_noGUI"
            exe.write_text("#!/bin/sh\n", encoding="utf-8")
            exe.chmod(0o755)

            with patch.dict(os.environ, {"Multiwfnpath": tmp}, clear=False):
                candidates = executables.multiwfn_candidates()

        self.assertTrue(any(candidate.path == exe for candidate in candidates))
        self.assertTrue(any(candidate.source == "env:Multiwfnpath" for candidate in candidates))

    def test_vesta_windows_dir_accepts_explicit_directory_or_exe(self):
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "VESTA.exe"
            exe.write_text("fake", encoding="utf-8")

            self.assertEqual(executables.vesta_windows_dir(str(Path(tmp))), Path(tmp))
            self.assertEqual(executables.vesta_windows_dir(str(exe)), Path(tmp))

    def test_explicit_relative_multiwfn_path_is_resolved_before_cwd_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            exe = root / "Multiwfn_noGUI"
            exe.write_text("#!/bin/sh\n", encoding="utf-8")
            exe.chmod(0o755)
            old_cwd = os.getcwd()
            os.chdir(str(root))
            try:
                candidates = executables.multiwfn_candidates("Multiwfn_noGUI")
            finally:
                os.chdir(old_cwd)

        self.assertEqual(candidates[0].path, exe.resolve())

    def test_find_multiwfn_ignores_non_executable_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "Multiwfn_noGUI"
            exe.write_text("#!/bin/sh\n", encoding="utf-8")

            selected = executables.find_multiwfn(str(exe))

        self.assertNotEqual(selected.path if selected else None, exe)

    def test_workspace_candidates_include_local_tools(self):
        multiwfn_paths = [candidate.path for candidate in executables.multiwfn_candidates()]
        vesta_paths = [candidate.path for candidate in executables.vesta_candidates()]

        self.assertIn(
            Path("/mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI"),
            multiwfn_paths,
        )
        self.assertIn(Path("/mnt/g/work/multiwfn2vesta/tools/VESTA-win64/VESTA.exe"), vesta_paths)

    def test_discovery_report_names_selected_executables(self):
        report = executables.discovery_report()

        self.assertIn("selected:", report)
        self.assertIn("## Multiwfn", report)
        self.assertIn("## VESTA", report)


if __name__ == "__main__":
    unittest.main()
