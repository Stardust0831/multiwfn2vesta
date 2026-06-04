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
- Otherwise builds an orthorhombic bounding cell around all AIM points.
- Converts Cartesian Angstrom coordinates to fractional `STRUC` coordinates.
- Labels path points as `P<path>_<point>`, for example `P0003_0012`.
- Optionally adds CP sites from `CPs.pdb` with larger radii and type colors.
- Emits an empty `SBOND` section.
- Sets `BONDS   0`.

This is intentionally an atoms-only representation. It avoids VESTA automatic
bond creation and does not try to draw continuous tubes/lines between path
points.

