import unittest
from pathlib import Path

from multiwfn2vesta.vesta_parser import read_vesta_bytes


SAMPLE = Path(__file__).resolve().parents[2] / "sj" / "C.vesta"


class TestVestaParser(unittest.TestCase):
    def test_vesta_parser_round_trips_sample_bytes(self):
        original = SAMPLE.read_bytes()
        document = read_vesta_bytes(SAMPLE)

        self.assertEqual(document.to_bytes(), original)

    def test_vesta_parser_finds_sample_boundaries_and_terminators(self):
        document = read_vesta_bytes(SAMPLE)

        self.assertEqual(document.preamble_lines[0], "#VESTA_FORMAT_VERSION 3.5.4\r\n")
        self.assertEqual(len(document.sections), 64)

        symop = document.section("SYMOP")
        self.assertEqual((symop.start_line, symop.end_line), (11, 24))
        self.assertEqual(
            symop.terminator_line,
            "-1.0 -1.0 -1.0  0 0 0  0 0 0  0 0 0",
        )

        struc = document.section("STRUC")
        self.assertEqual((struc.start_line, struc.end_line), (43, 48))
        self.assertEqual(struc.terminator_line, "0 0 0 0 0 0 0")

        hbond = document.section("HBOND")
        self.assertEqual(hbond.args, ["0", "2"])
        self.assertEqual(hbond.body_lines, ["\r\n"])

    def test_vesta_parser_rejects_ambiguous_unique_section_lookup(self):
        document = read_vesta_bytes(SAMPLE)
        document.sections.append(document.section("TITLE"))

        with self.assertRaisesRegex(KeyError, "not unique"):
            document.section("TITLE")

    def test_vesta_parser_recognizes_multiphase_directives(self):
        from multiwfn2vesta.vesta_parser import parse_vesta_text

        text = (
            "#VESTA_FORMAT_VERSION 3.5.4\r\n"
            "\r\n"
            "MOLECULE\r\n"
            "TITLE\r\n"
            "phase 1\r\n"
            "PHASON\r\n"
            " 0 0 0\r\n"
            "QCORIG\r\n"
            " 0.000000 0.000000 0.000000\r\n"
            "CRYSTAL\r\n"
            "TITLE\r\n"
            "phase 2\r\n"
            "PHASON\r\n"
            " 0 0 0\r\n"
            "QCORIG\r\n"
            " 0.000000 0.000000 0.000000\r\n"
            "STYLE\r\n"
            "BONDS   0\r\n"
        )

        document = parse_vesta_text(text)

        self.assertEqual(len(document.sections_named("MOLECULE")), 1)
        self.assertEqual(len(document.sections_named("CRYSTAL")), 1)
        self.assertEqual(len(document.sections_named("PHASON")), 2)
        self.assertEqual(len(document.sections_named("QCORIG")), 2)
        self.assertEqual(document.to_bytes(), text.encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
