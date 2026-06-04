# AIM `paths.pdb` to atoms-only `.vesta`

Multiwfn's AIM path export writes `paths.pdb` as PDB `HETATM` records, but the
records are not chemical atoms. Each `C` atom is a sampled point on an AIM
topology path; the residue sequence number stores the path index. Loading this
file directly into VESTA can trigger distance-based C-C bond detection between
many dense path points.

Use `multiwfn2vesta.aim_vesta` to create a `.vesta` file that disables bonds and
displays the path points as small atom-like spheres.

```bash
cd /mnt/g/work/multiwfn2vesta/project
PYTHONPATH=src python -m multiwfn2vesta.aim_vesta \
  /path/to/paths.pdb \
  /path/to/aim_paths_atoms_only.vesta \
  --cps-pdb /path/to/CPs.pdb \
  --title "AIM topology"
```

Behavior:

- Parses PDB `ATOM`/`HETATM` fixed columns, with whitespace fallback.
- Uses `CRYST1` as the VESTA cell when present.
- If `CRYST1` is present, writes a `CRYSTAL` phase and converts Cartesian
  Angstrom coordinates to fractional `STRUC` coordinates.
- If `CRYST1` is absent, writes a `MOLECULE` phase and keeps the raw
  Multiwfn/PDB Cartesian coordinates in `STRUC`.  This keeps AIM paths/CPs
  aligned with molecule layers saved by VESTA from `mol.pdb`.
- Labels path points as `P<path>_<point>`, for example `P0003_0012`.
- Optionally adds CP sites from `CPs.pdb` with Multiwfn-style radii and type colors:
  `(3,-3)` `C` purple, `(3,-1)` BCP `N` orange, `(3,+1)` `O` yellow, and
  `(3,+3)` `F` green.  These follow Multiwfn's 3D `CP_RGB` defaults in
  `settings.ini` and `examples/scripts/AIM.vmd`: path points default to
  radius `0.02`, and all CP types default to radius `0.07`.
- For publication figures that need stronger emphasis, use `--path-radius`,
  `--cp-radius`, and `--bcp-radius` to override the defaults.
- Emits an empty `SBOND` section.
- Sets `BONDS   0`.

This is intentionally an atoms-only representation. It avoids VESTA automatic
bond creation and does not try to draw continuous tubes/lines between path
points.

When an AIM layer is imported over a molecular layer and VESTA saves the merged
file, VESTA may keep only the base layer's global `ATOMT` table.  If the AIM
colors fall back to defaults, patch the saved merged file before exporting:

```bash
PYTHONPATH=src python -m multiwfn2vesta.vesta_aim_style \
  merged.vesta \
  merged_aim_style.vesta
```

Large VDW-style base molecule radii can also hide BCPs because BCPs sit close
to nuclei.  Use smaller base atom/bond radii for AIM overlay figures when the
CPs need to be inspected directly.
