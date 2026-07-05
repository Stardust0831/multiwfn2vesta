import unittest
from pathlib import Path


class TestProjectSkill(unittest.TestCase):
    def test_multiwfn2vesta_operator_skill_has_required_files(self):
        root = Path(__file__).resolve().parents[1]
        skill = root / "docs" / "codex_skills" / "multiwfn2vesta-operator"
        skill_md = skill / "SKILL.md"
        self.assertTrue(skill_md.exists())
        text = skill_md.read_text(encoding="utf-8")
        self.assertIn("name: multiwfn2vesta-operator", text)
        self.assertIn("description:", text)
        self.assertIn("references/stable_tools.md", text)
        self.assertIn("references/vesta_file_format.md", text)
        self.assertIn("references/project_packaging.md", text)
        for name in ("stable_tools.md", "vesta_file_format.md", "project_packaging.md"):
            self.assertTrue((skill / "references" / name).exists())

    def test_vesta_reference_mentions_key_fields(self):
        root = Path(__file__).resolve().parents[1]
        ref = root / "docs" / "codex_skills" / "multiwfn2vesta-operator" / "references" / "vesta_file_format.md"
        text = ref.read_text(encoding="utf-8")
        for field in ("STRUC", "SITET", "SBOND", "SCENE", "ISURF", "TEX3P", "BOUND", "PHASON", "QCORIG"):
            self.assertIn(field, text)


if __name__ == "__main__":
    unittest.main()
