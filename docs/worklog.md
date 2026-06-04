# Worklog

## 2026-06-05: VESTA atom scalar coloring

- Added `multiwfn2vesta.vesta_atom_coloring`.
- Implemented blue-white-red diverging RGB mapping with configurable
  `vmin`, `vmax`, and `center`.
- Added text/file APIs that patch `SITET` rows while preserving other VESTA
  sections through the lossless parser.
- Added CSV/TSV/whitespace value table reader supporting ordered values,
  `label,value`, and `index,value` forms.
- Added CLI:
  `python -m multiwfn2vesta.vesta_atom_coloring input.vesta values.csv output.vesta`.
- Missing `SITET` rows are inserted before the `SITET` sentinel, using `ATOMT`
  radius/alpha when possible.
- Added focused tests in `tests/test_vesta_atom_coloring.py`.
- Added docs:
  - `docs/vesta_atom_value_coloring.md`
  - `docs/skills/vesta_atom_value_coloring_skill.md`

Limitations recorded:

- This is generator-side per-site RGB patching, not VESTA-native scalar
  colormap support.
- VESTA will not know the scalar values or create a legend automatically.
