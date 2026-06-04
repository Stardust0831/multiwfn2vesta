# Multiwfn AIM `paths.pdb` / `CPs.pdb` to VESTA notes

Date: 2026-06-04

## Sources

- Sobereva tutorial: http://sobereva.com/445
  - Article title: using Multiwfn + VMD to plot AIM topology maps.
  - The article says the script exports critical points to `CPs.pdb`, topology paths to `paths.pdb`, and molecular geometry to `mol.pdb`.
  - It also says different topology paths in `paths.pdb` correspond to different residue numbers, so VMD can select paths by `resid`.
- Multiwfn 2026.6.2 source in this workspace:
  - `tools/Multiwfn_2026.6.2_src_Linux/topology.f90:411-444`
  - `tools/Multiwfn_2026.6.2_src_Linux/topology.f90:612-641`
- Multiwfn bundled VMD script:
  - `tools/Multiwfn_2026.6.2_bin_Linux/examples/scripts/AIM.vmd:9-35`
- wwPDB coordinate record reference:
  - https://www.wwpdb.org/documentation/file-format-content/format33/sect9.html
- VESTA online manual:
  - Bonds/search modes: https://jp-minerals.org/vesta/en/doc/VESTAch8.html
  - Display styles: https://jp-minerals.org/vesta/en/doc/VESTAch5.html
- Local VESTA sample/notes:
  - `sj/C.vesta:40-111`
  - `docs/vesta_directive_fields.md:31-68`

## Format conclusions

`paths.pdb` is standard-shaped PDB `HETATM` coordinate records, but semantically the atoms are artificial visualization points, not chemical atoms.

Multiwfn writes each path point as:

```text
HETATM <serial>  C   PTH A<resSeq>    <x> <y> <z>  1.00  0.00           C
TER
```

Confirmed field mapping from the Fortran format string:

- Record name: `HETATM`
- Atom serial: running point index across all paths, `i5`
- Atom name: `C`
- Residue name: `PTH`
- Chain ID: `A`
- Residue sequence number: path index
- Coordinates: Angstrom, because Multiwfn writes internal Bohr coordinates multiplied by `b2a`
- Occupancy: `1.00`
- Temperature factor: `0.00`
- Element: `C`
- `TER` is written after each path
- PBC mode writes a `CRYST1` line first; option `-6` may add boundary image paths, with residue number still equal to the original path index

`CPs.pdb` is also standard-shaped `HETATM`, but the element is used as a CP type code:

- `C` means `(3,-3)`
- `N` means `(3,-1)`
- `O` means `(3,+1)`
- `F` means `(3,+3)`
- Residue name: `CPS`
- Chain ID: `A`
- Non-PBC residue sequence number: always `1`
- PBC boundary-image mode uses residue sequence number as the original unique CP index
- A remark line records the C/N/O/F mapping

The wwPDB reference confirms the same core columns for `ATOM`/`HETATM`: record name, serial, atom name, residue name, chain ID, residue sequence number, x/y/z in Angstrom, occupancy, temperature factor, and element.

## Why VESTA can over-bond or crash

This is a display-data-vs-structure-data mismatch.

`paths.pdb` encodes every sample point on a bond path as a carbon atom. Multiwfn's default path step is very small, and the exported coordinates are in Angstrom. VESTA's bond search is distance-based; its manual describes modes that search atom pairs by minimum/maximum distance, including a molecular search mode that checks all pairs. The local `sj/C.vesta` sample has an `SBOND` C-C rule from `0.00000` to `1.89002` Angstrom and `BONDS 1`.

Therefore, if VESTA imports `paths.pdb` as ordinary carbon atoms and applies C-C or generic molecular bond searching, it may create many bonds:

- Between neighboring path points.
- Between non-neighbor points on the same path that are still within the cutoff.
- Between nearby points belonging to different paths.
- Between path points and real molecular atoms if all files are merged.
- Across boundary images if PBC export is used.

The number of candidate pairs can grow rapidly. Even if only a fraction are displayed, VESTA still has to search, store, and render them. That explains direct-import symptoms such as excessive bonds, UI stalls, crashes, or apparent infinite expansion under recursive/boundary bond-search modes.

Extra PDB-level risks:

- `HETATM` serial is `i5`, so more than 99,999 path points can overflow the traditional PDB serial field.
- Residue sequence number is `i4`, so more than 9,999 paths can overflow.
- Coordinate fields are `f8.3`, so very large coordinates can become malformed.

## VESTA conversion recommendations

Prefer generating a `.vesta` file directly instead of asking VESTA to infer chemistry from `paths.pdb`.

### Structure and cell

- Use a simple `P 1` / identity-symmetry model unless a real periodic cell is present.
- If `paths.pdb` has `CRYST1`, use that cell.
- If no cell exists, create an orthorhombic bounding cell around all AIM points and molecular atoms, with a small margin, then convert Cartesian Angstrom coordinates to fractional coordinates for `STRUC`.
- Set `BOUND` to one visible cell only, for example `0 1 0 1 0 1`, and do not ask VESTA to replicate path points.
- If Multiwfn option `-6` already exported boundary images, treat those images as explicit sites and still keep `BOUND` at one cell.

### Path representation

- Represent each path point as a site in `STRUC` with a small sphere radius. This matches the bundled VMD script, which displays `paths.pdb` as tiny VDW spheres rather than chemical bonds.
- Preserve path grouping in generated labels, for example `P001_0001`, `P001_0002`, or in an internal mapping table. VESTA site labels can keep path identity even though `.vesta` itself does not use PDB residue IDs.
- Do not use VESTA bonds to draw path continuity unless a tested explicit-bond representation is added later. Dense spheres are safer and avoid automatic bond search.

### Critical point representation

- Preserve the CP type mapping from `CPs.pdb`, but do not rely on chemically meaningful C/N/O/F styling if the real molecule is also present.
- Either:
  - keep `C/N/O/F` and override each CP site's style via `SITET`, or
  - map CP/path pseudo-sites to rarely used valid element symbols and use `ATOMT` for compact element-level styling.
- Use larger radii for CPs than path points and distinct colors matching the tutorial convention.

### Disable bonds

- Emit an empty `SBOND` section:

```text
SBOND
  0 0 0 0
```

- Set the style switch to hide bonds:

```text
BONDS   0
```

- Do not copy template C-C `SBOND` rules such as the one in `sj/C.vesta`.
- Keep `HBOND 0 2` or another empty hydrogen-bond section; do not add H-bond rules for pseudo-sites.

### Atom style

- Keep atoms visible, for example `ATOMS   0  0  1`.
- Use small radii for path points, roughly the VMD script scale: path point radius around `0.02` to `0.07` Angstrom-equivalent, depending on VESTA rendering.
- Use CP radius around `0.07` or larger.
- If a generated file contains thousands of path points, prefer element-level `ATOMT` styling to avoid huge per-site `SITET` sections. Use per-site `SITET` only when element symbols collide with real molecular atoms and distinct styles are required.

## Practical implementation stance

The converter should parse PDB fixed columns, not split by whitespace. The fields are standard-position PDB fields, and fixed-column parsing preserves chain/residue/serial even when spacing changes.

For `paths.pdb`, the important semantic key is `resSeq`: it is the path index. For `CPs.pdb`, the important semantic key is `element/name`: it is the CP type code, and `serial` is the CP index in the ordinary non-PBC export.

The generated `.vesta` should be atoms-only for AIM path and CP pseudo-sites, with bond search disabled by construction.
