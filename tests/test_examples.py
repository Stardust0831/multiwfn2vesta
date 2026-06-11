import io
import json
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

    def test_verify_project_files(self):
        output = io.StringIO()
        with patch("sys.stdout", output):
            code = examples.main(["--verify"])

        self.assertEqual(code, 0)
        self.assertIn("Project example docs and gallery files are present", output.getvalue())


if __name__ == "__main__":
    unittest.main()
