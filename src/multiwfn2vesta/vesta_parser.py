"""Lossless parser prototype for VESTA .vesta text files.

The parser intentionally treats VESTA records as structured text blocks.  It
finds directive boundaries and preserves every original line so files can be
serialized byte-for-byte when no edits are made.
"""

from pathlib import Path
from typing import Iterable, List, Optional


DEFAULT_SECTION_NAMES = frozenset(
    {
        "CRYSTAL",
        "MOLECULE",
        "TITLE",
        "GROUP",
        "SYMOP",
        "TRANM",
        "LTRANSL",
        "LORIENT",
        "LMATRIX",
        "PHASON",
        "CELLP",
        "STRUC",
        "THERI",
        "SHAPE",
        "BOUND",
        "QCORIG",
        "SBOND",
        "SITET",
        "VECTR",
        "VECTT",
        "SPLAN",
        "LBLAT",
        "LBLSP",
        "DLATM",
        "DLBND",
        "DLPLY",
        "PLN2D",
        "ATOMT",
        "SCENE",
        "HBOND",
        "STYLE",
        "DISPF",
        "MODEL",
        "SURFS",
        "SECTS",
        "FORMS",
        "ATOMS",
        "BONDS",
        "POLYS",
        "VECTS",
        "FORMP",
        "ATOMP",
        "BONDP",
        "POLYP",
        "ISURF",
        "TEX3P",
        "SECTP",
        "CONTR",
        "HKLPP",
        "UCOLP",
        "COMPS",
        "LABEL",
        "PROJT",
        "BKGRC",
        "DPTHQ",
        "LIGHT0",
        "LIGHT1",
        "LIGHT2",
        "LIGHT3",
        "SECCL",
        "TEXCL",
        "ATOMM",
        "BONDM",
        "POLYM",
        "SURFM",
        "FORMM",
        "HKLPM",
    }
)

SENTINEL_TERMINATED_SECTIONS = frozenset(
    {
        "SYMOP",
        "STRUC",
        "THERI",
        "SBOND",
        "SITET",
        "VECTR",
        "VECTT",
        "SPLAN",
        "LBLAT",
        "LBLSP",
        "DLATM",
        "DLBND",
        "DLPLY",
        "PLN2D",
        "ATOMT",
    }
)


class VestaSection:
    """One VESTA directive line plus all following lines until the next directive."""

    def __init__(
        self,
        name: str,
        header_line: str,
        body_lines: Optional[List[str]] = None,
        start_line: int = 0,
    ) -> None:
        self.name = name
        self.header_line = header_line
        self.body_lines = body_lines or []
        self.start_line = start_line

    @property
    def end_line(self) -> int:
        return self.start_line + len(self.body_lines)

    @property
    def args(self) -> List[str]:
        return self.header_line.strip().split()[1:]

    @property
    def nonblank_body_lines(self) -> List[str]:
        return [line for line in self.body_lines if line.strip()]

    @property
    def terminator_line(self) -> Optional[str]:
        if self.name not in SENTINEL_TERMINATED_SECTIONS:
            return None
        for line in reversed(self.body_lines):
            stripped = line.strip()
            if stripped:
                return stripped
        return None

    def text(self) -> str:
        return self.header_line + "".join(self.body_lines)

    def replace_body(self, body_lines: Iterable[str]) -> None:
        self.body_lines = list(body_lines)


class VestaDocument:
    """A parsed VESTA document that can be serialized without format loss."""

    def __init__(
        self,
        preamble_lines: List[str],
        sections: List[VestaSection],
        encoding: str = "utf-8",
    ) -> None:
        self.preamble_lines = preamble_lines
        self.sections = sections
        self.encoding = encoding

    def text(self) -> str:
        return "".join(self.preamble_lines) + "".join(section.text() for section in self.sections)

    def to_bytes(self) -> bytes:
        return self.text().encode(self.encoding)

    def section(self, name: str) -> VestaSection:
        matches = self.sections_named(name)
        if not matches:
            raise KeyError(f"VESTA section not found: {name}")
        if len(matches) > 1:
            raise KeyError(f"VESTA section is not unique: {name}")
        return matches[0]

    def sections_named(self, name: str) -> List[VestaSection]:
        return [section for section in self.sections if section.name == name]

    def outline(self) -> List[dict]:
        return [
            {
                "name": section.name,
                "start_line": section.start_line,
                "end_line": section.end_line,
                "body_line_count": len(section.body_lines),
                "nonblank_body_line_count": len(section.nonblank_body_lines),
                "terminator_line": section.terminator_line,
            }
            for section in self.sections
        ]


def parse_vesta_text(
    text: str,
    *,
    section_names: Iterable[str] = DEFAULT_SECTION_NAMES,
    encoding: str = "utf-8",
) -> VestaDocument:
    names = set(section_names)
    lines = text.splitlines(keepends=True)
    preamble_lines: List[str] = []
    sections: List[VestaSection] = []
    current: Optional[VestaSection] = None

    for line_number, line in enumerate(lines, start=1):
        tokens = line.strip().split()
        is_section_header = bool(tokens and tokens[0] in names)
        if is_section_header:
            if current is not None:
                sections.append(current)
            current = VestaSection(
                name=tokens[0],
                header_line=line,
                start_line=line_number,
            )
        elif current is None:
            preamble_lines.append(line)
        else:
            current.body_lines.append(line)

    if current is not None:
        sections.append(current)

    return VestaDocument(preamble_lines=preamble_lines, sections=sections, encoding=encoding)


def read_vesta(path: Path, *, encoding: str = "utf-8") -> VestaDocument:
    return parse_vesta_text(path.read_text(encoding=encoding, newline=""), encoding=encoding)


def read_vesta_bytes(path: Path, *, encoding: str = "utf-8") -> VestaDocument:
    return parse_vesta_text(path.read_bytes().decode(encoding), encoding=encoding)
