# Skill: Multiwfn AIM paths to VESTA

## When to use

Use this workflow when Multiwfn AIM topology analysis has produced `paths.pdb`
and optionally `CPs.pdb`, and VESTA should display the paths/critical points
without generating dense automatic bonds between path points.

## Inputs

- Multiwfn noGUI executable:
  `/mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI`
- Wavefunction file, for example:
  `tools/Multiwfn_2026.6.2_bin_Linux_noGUI/examples/H2O.fch`
- Optional existing Multiwfn command stream:
  `tools/Multiwfn_2026.6.2_bin_Linux_noGUI/examples/scripts/AIM.txt`
- Converter module:
  `multiwfn2vesta.aim_vesta`

## Key facts

- Multiwfn `paths.pdb` writes every path sample point as `HETATM` with atom
  name/element `C`, residue name `PTH`, and residue sequence equal to the path
  index.
- Multiwfn `CPs.pdb` uses element codes for CP type:
  - `C`: `(3,-3)` nuclear attractor
  - `N`: `(3,-1)` BCP
  - `O`: `(3,+1)`
  - `F`: `(3,+3)`
- VESTA direct import may treat dense path points as carbon atoms and generate
  excessive C-C bonds.
- The safe VESTA output has empty `SBOND` and `BONDS   0` for the AIM point
  phase.
- Non-periodic AIM exports without `CRYST1` must be written as a VESTA
  `MOLECULE` phase with raw Cartesian coordinates.  Do not build an artificial
  bounding cell for these files; that shifts/scales the AIM layer relative to a
  molecule layer saved from `mol.pdb`.
- BCPs are encoded as `N`; use the same radius as other CPs by default and a
  color distinct from the path color.  Multiwfn's VMD script uses
  `pathsize=0.02` and `CPsize=0.07`; Multiwfn's 3D `CP_RGB` defaults use
  purple, orange, yellow, and green for `(3,-3)`, `(3,-1)`, `(3,+1)`, and
  `(3,+3)`.
- Use `--path-radius`, `--cp-radius`, and `--bcp-radius` only when a
  publication figure needs deliberate size emphasis beyond the Multiwfn-style
  default.
- For VESTA overlays, prefer one pseudo-element for all AIM path sample points
  instead of assigning different rare gases per path branch.  Mixed
  `He/Ne/Ar/Kr/Xe/Rn` path elements make the style table harder to reason
  about and can produce inconsistent rendering if VESTA drops or reorders
  `ATOMT` rows.  A single rare element such as `Xe`, with yellow path points
  and larger orange BCPs, is easier to maintain.
- If BCPs are invisible, first check whether path sample points occupy the same
  coordinates and draw over them.  Reduce path point radius, increase BCP
  radius, and use a distinct BCP color before adding VESTA bonds.
- In saved multi-phase overlays, if BCPs still disappear and the user wants to
  keep all path sample points, do not delete overlapping path points.  Instead
  map paths and BCPs to different pseudo-elements.  The maintained helper is:

  ```bash
  python -m multiwfn2vesta.vesta_aim_overlay_style \
    input_overlay.vesta \
    output_overlay.vesta \
    --path-element Xe \
    --bcp-element Rn \
    --path-radius 0.055 \
    --bcp-radius 0.180 \
    --path-rgb 255 230 0 \
    --bcp-rgb 255 80 0
  ```

  This keeps every `P...._....` path sample site, keeps BCP labels such as
  `CP0001_N`, clears AIM-phase `SBOND`, and leaves real structure bonds
  enabled by default.

## Steps

1. Run Multiwfn AIM topology analysis in an isolated working directory.

   ```bash
   timeout 60s /mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI \
     /path/to/input.fch \
     < AIM_exit.txt > multiwfn.stdout.txt 2> multiwfn.stderr.txt
   ```

2. Confirm outputs exist.

   ```bash
   ls -lh paths.pdb CPs.pdb CPprop.txt mol.pdb
   ```

3. Convert AIM paths/CPs to atoms-only VESTA.

   ```bash
   cd /mnt/g/work/multiwfn2vesta
   PYTHONPATH=project/src python -m multiwfn2vesta.aim_vesta \
     /path/to/paths.pdb \
     /path/to/aim_atoms_only.vesta \
     --cps-pdb /path/to/CPs.pdb \
     --title "AIM paths and CPs"
   ```

4. Verify no AIM bonds will be drawn.

   ```bash
   rg -n '^MOLECULE$|^CRYSTAL$|^SBOND$|^BONDS|CP.*_N' /path/to/aim_atoms_only.vesta
   ```

5. If the AIM layer was imported into a base molecule and then saved by VESTA,
   patch the saved merged file before final export.  VESTA may drop the AIM
   phase's global `ATOMT` rows and keep only the base molecule atom types.

   ```bash
   PYTHONPATH=project/src python -m multiwfn2vesta.vesta_aim_style \
     /path/to/merged.vesta \
     /path/to/merged_aim_style.vesta
   ```

## Expected validation

- `paths.pdb` should have many `HETATM ... PTH ...` records and `TER` after
  each path.
- `CPs.pdb` should have `N` records for BCPs.
- Generated `.vesta` should contain:
  - `MOLECULE` for ordinary non-periodic AIM exports
  - `SBOND` followed by `0 0 0 0`
  - `BONDS   0`
  - BCP labels such as `CP0004_N`
  - `CP000*_N  0.0700 255 128 0` in `SITET`
- For overlay figures, inspect the molecule layer radii.  VESTA's PDB import
  can use large VDW radii (`H` around `0.4600` in the H2O smoke case), which
  hides BCPs even when coordinates are correct.  Use a small-atom base layer or
  hide conventional bonds/large atom spheres for AIM-focused figures.

## Real smoke result

H2O smoke directory:

```text
smoke/20260604_task_i_h2o_aim_final/
```

Observed:

- 120 path points
- 4 paths
- 5 CPs
- 2 BCPs
- VESTA PNG exported successfully from atoms-only `.vesta`

Alignment/style regression smoke:

```text
smoke/20260605_aim_overlay_alignment/products/
```

Observed:

- `h2o_aim_molecule_aligned.vesta` is `MOLECULE`, not `CRYSTAL`.
- `CP0004_N` and `CP0005_N` retain raw H2O AIM coordinates and orange `0.0700`
  `SITET` styling.
- `h2o_mol_small_plus_aim_aligned_postatomt.png` shows BCPs after using a
  small-atom base molecule and post-processing merged `ATOMT`.

## Failure notes

- Full `unittest discover` currently fails because old tests still import
  `src.multiwfn_vesta`; use focused tests until package naming is repaired.
- VESTA Windows interop may return nonzero or timeout after exporting an image.
  Check the output file and run a cleanup close/taskkill command.
