import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from multiwfn2vesta import examples


class TestExamplesIndex(unittest.TestCase):
    def test_default_output_lists_curated_examples_and_docs(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main([])

        self.assertEqual(code, 0)
        text = output.getvalue()
        self.assertIn("multiwfn2vesta curated examples", text)
        self.assertIn("manual_zh", text)
        self.assertIn("ag111_benzene_igmh_aim", text)
        self.assertIn("gc_aim", text)
        self.assertIn("cdcl_trajectory_video", text)

    def test_status_filter(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--status", "misc"])

        self.assertEqual(code, 0)
        text = output.getvalue()
        self.assertIn("benzene_nics_vector_misc", text)
        self.assertNotIn("ag111_benzene_igmh_aim", text)

    def test_json_output(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--status", "ready", "--json"])

        self.assertEqual(code, 0)
        records = json.loads(output.getvalue())
        ids = {item["id"] for item in records}
        self.assertIn("ag111_benzene_igmh_aim", ids)
        self.assertIn("gc_aim", ids)
        self.assertNotIn("h2o_hf_iri_aim_debug", ids)

    def test_id_filter_limits_text_output(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--id", "cdcl_trajectory_video"])

        self.assertEqual(code, 0)
        text = output.getvalue()
        self.assertIn("cdcl_trajectory_video", text)
        self.assertIn("artifact_manifest.json", text)
        self.assertNotIn("ag111_benzene_igmh_aim", text)

    def test_id_filter_supports_comma_separated_json_output(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--id", "gc_aim,benzene_aim", "--json"])

        self.assertEqual(code, 0)
        records = json.loads(output.getvalue())
        self.assertEqual([item["id"] for item in records], ["gc_aim", "benzene_aim"])

    def test_json_output_includes_optional_manifest(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--id", "cdcl_trajectory_video", "--json"])

        self.assertEqual(code, 0)
        records = json.loads(output.getvalue())
        self.assertEqual(records[0]["manifest"], "examples/cdcl_trajectory_video/artifact_manifest.json")

    def test_planned_real_system_examples_are_indexed(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--status", "needs-work", "--json"])

        self.assertEqual(code, 0)
        records = json.loads(output.getvalue())
        ids = {item["id"] for item in records}
        expected = {
            "ag111_benzene_extended_fields",
            "benzene_dimer_scalar_suite",
            "gc_weak_interaction_suite",
            "cof_direct_cube_suite",
            "fukui_dual_reactivity",
            "spin_atom_coloring_suite",
            "h2o_domain_baseline",
            "short_aigm_trajectory",
        }
        self.assertLessEqual(expected, ids)
        for item in records:
            if item["id"] in expected:
                self.assertTrue(item["runbook"].startswith(f"examples/{item['id']}/"))
                self.assertEqual(item["gallery"], [])

    def test_coverage_output_lists_feature_status(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--coverage"])

        self.assertEqual(code, 0)
        text = output.getvalue()
        self.assertIn("feature example coverage", text)
        self.assertIn("grid-run", text)
        self.assertIn("rose/sedd", text)
        self.assertIn("steric/sbl", text)
        self.assertIn("on-top-pair-density", text)
        self.assertIn("aim-igmh", text)
        self.assertIn("trajectory-video", text)
        self.assertIn("docs/feature_examples_zh.md", text)

    def test_needs_render_filters_coverage_records(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--needs-render"])

        self.assertEqual(code, 0)
        text = output.getvalue()
        self.assertIn("grid-run", text)
        self.assertIn("surface-extrema", text)
        self.assertNotIn("aim-igmh", text)

    def test_command_filter_implies_coverage(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--command", "trajectory-video"])

        self.assertEqual(code, 0)
        text = output.getvalue()
        self.assertIn("feature example coverage", text)
        self.assertIn("trajectory-video", text)
        self.assertIn("cdcl_trajectory_video", text)
        self.assertNotIn("surface-extrema", text)

    def test_command_filter_supports_feature_terms_and_json(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--command", "rose", "--json"])

        self.assertEqual(code, 0)
        records = json.loads(output.getvalue())
        commands = {item["command"] for item in records}
        self.assertEqual(commands, {"grid-run --function rose/sedd"})

        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--command", "on-top-pair", "--json"])

        self.assertEqual(code, 0)
        records = json.loads(output.getvalue())
        commands = {item["command"] for item in records}
        self.assertEqual(commands, {"grid-run --function on-top-pair-density"})

        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--command", "surface-extrema", "--json"])

        self.assertEqual(code, 0)
        records = json.loads(output.getvalue())
        self.assertEqual(records[0]["example"], "gc_weak_interaction_suite")

    def test_command_filter_supports_cli_aliases(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--command", "rdg-run", "--json"])

        self.assertEqual(code, 0)
        records = json.loads(output.getvalue())
        self.assertEqual([item["command"] for item in records], ["iri-run"])

    def test_command_filter_examples_does_not_match_runbook_paths(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--command", "examples", "--json"])

        self.assertEqual(code, 0)
        records = json.loads(output.getvalue())
        self.assertEqual([item["command"] for item in records], ["examples"])
        self.assertEqual(records[0]["gallery"], ["docs/assets/gallery/current_feature_overview.png"])

    def test_gallery_assets_output_lists_project_images(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--gallery-assets", "--status", "ready"])

        self.assertEqual(code, 0)
        text = output.getvalue()
        self.assertIn("rendered gallery assets", text)
        self.assertIn("ag111_benzene_igmh_aim_front.png", text)
        self.assertIn("gc_aim_overlay.png", text)
        self.assertIn("current_feature_overview.png", text)
        self.assertNotIn("h2o_iri_aim_overlay.png", text)

    def test_gallery_assets_json_includes_existence_flag(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--gallery-assets", "--id", "gc_aim", "--json"])

        self.assertEqual(code, 0)
        records = json.loads(output.getvalue())
        self.assertEqual([item["example_id"] for item in records], ["gc_aim"])
        self.assertTrue(records[0]["exists"])
        self.assertEqual(records[0]["image"], "docs/assets/gallery/gc_aim_overlay.png")

    def test_systems_output_lists_valuable_real_systems(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--systems"])

        self.assertEqual(code, 0)
        text = output.getvalue()
        self.assertIn("recommended real systems", text)
        self.assertIn("ag111_benzene", text)
        self.assertIn("gc_base_pair", text)
        self.assertIn("cof_12000n2_monolayer", text)

    def test_systems_json_is_priority_ordered(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--systems", "--json"])

        self.assertEqual(code, 0)
        records = json.loads(output.getvalue())
        self.assertEqual(records[0]["id"], "ag111_benzene")
        self.assertLess(records[0]["priority"], records[-1]["priority"])

    def test_coverage_json_filter(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--coverage", "--coverage-status", "ready", "--json"])

        self.assertEqual(code, 0)
        records = json.loads(output.getvalue())
        commands = {item["command"] for item in records}
        self.assertIn("aim-igmh", commands)
        self.assertIn("trajectory-video", commands)
        self.assertNotIn("grid-run", commands)

    def test_unknown_id_is_an_error(self):
        error = io.StringIO()
        with patch("sys.stderr", error):
            code = examples.main(["--id", "not_a_real_example"])

        self.assertEqual(code, 2)
        self.assertIn("Unknown example id", error.getvalue())

    def test_verify_project_files(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--verify"])

        self.assertEqual(code, 0)
        self.assertIn("Project example docs and gallery files are present", output.getvalue())

    def test_verify_smoke_checks_workspace_evidence_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()
            smoke_root = Path(tmp) / "smoke" / "vesta_trajectory_video_1608" / "ase_nvt_refstyle_stride20_cdcl3p50"
            (smoke_root / "png").mkdir(parents=True)
            (smoke_root / "patched").mkdir(parents=True)
            (smoke_root / "ase_nvt_refstyle_stride20_cdcl3p50_hq20m.mp4").write_text("mp4", encoding="utf-8")
            (smoke_root / "png" / "frame_0001.png").write_text("png", encoding="utf-8")
            npt_root = Path(tmp) / "smoke" / "vesta_trajectory_video_1608" / "ase_npt_refstyle_stride20"
            npt_root.mkdir(parents=True)
            (npt_root / "ase_npt_refstyle_stride20_hq20m.mp4").write_text("mp4", encoding="utf-8")

            output = io.StringIO()
            with patch("multiwfn2vesta.examples.PROJECT_ROOT", project_root), patch("sys.stdout", output):
                code = examples.main(["--id", "cdcl_trajectory_video", "--verify-smoke"])

        self.assertEqual(code, 0)
        self.assertIn("Smoke evidence paths are present", output.getvalue())

    def test_verify_smoke_reports_missing_workspace_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            project_root.mkdir()

            output = io.StringIO()
            with patch("multiwfn2vesta.examples.PROJECT_ROOT", project_root), patch("sys.stdout", output):
                code = examples.main(["--id", "cdcl_trajectory_video", "--verify-smoke"])

        self.assertEqual(code, 1)
        self.assertIn("Missing smoke evidence", output.getvalue())


if __name__ == "__main__":
    unittest.main()
