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
  and larger orange BCPs, is easier to maintain.  Current maintained overlay
  default for the yellow `Xe` path sample spheres is radius `0.0600` Angstrom.
- If BCPs are invisible, first check whether path sample points occupy the same
  coordinates and draw over them.  Reduce path point radius, increase BCP
  radius, and use a distinct BCP color before adding VESTA bonds.
- In saved multi-phase overlays, if BCPs still disappear and the user wants to
  keep all path sample points, do not delete overlapping path points and do not
  move BCP coordinates to solve a viewing problem.  Instead map paths and BCPs
  to different pseudo-elements, optionally split BCPs into a final phase, then
  solve remaining visibility issues with the camera/view.  The maintained
  helper is:

  ```bash
  python -m multiwfn2vesta.vesta_aim_overlay_style \
    input_overlay.vesta \
    output_overlay.vesta \
    --path-element Xe \
    --bcp-element Rn \
    --path-radius 0.060 \
    --bcp-radius 0.180 \
    --path-rgb 255 230 0 \
    --bcp-rgb 255 80 0 \
    --split-bcp-phase
  ```

  This keeps every `P...._....` path sample site, keeps BCP labels such as
  `CP0001_N`, clears AIM-phase `SBOND`, leaves real structure bonds enabled by
  default, and leaves coordinates unchanged.
- To isolate whether VESTA can display BCPs at all, render a BCP-only
  single-phase diagnostic before changing the full overlay style.  The
  2026-06-09 Ag(111)+benzene diagnostic rendered three orange `CP000*_N`
  points successfully.  A zoom-only copy, changing only the final `SCENE`
  scalar from `0.800` to `2.400`, made the same points clearly visible without
  changing BCP radius or color.  Treat a successful BCP-only render as evidence
  that any full-overlay invisibility is caused by overlap, occlusion, or scale,
  not absent BCP records.
- If atom naming is suspected, test it with BCP-only controls before changing
  the maintained overlay naming scheme.  The 2026-06-09 Ag(111)+benzene
  controls rendered visible BCP points for `N+CP000*_N`, `N+BCP*`,
  `Rn+CP*_N`, `Rn+RBCP*`, `Xe+CP*_N`, `C+CP*_N`, and `He+CP*_N`.  Therefore
  the `CP000*_N` label pattern and these tested element symbols are not enough
  to explain BCP invisibility.
- For BCP index labels, use VESTA's documented atom/site label route rather
  than arbitrary text objects.  Rename BCP site labels to concise strings such
  as `BCP1`, `BCP2`, or `B001`, then enable atom labels as "Names of sites".
  In `.vesta` output this means `LABEL 1 ...`; `LABEL 0 ...` displays element
  names instead.  Set the BCP `SITET` tail flag to `1`.  Do not generate
  non-empty `LBLAT` records until a GUI-save diff has confirmed the exact
  syntax.  Native VESTA label placement is not per-site adjustable and can
  overlap for nearby BCPs, so publication figures should still prefer
  post-render PNG/SVG text annotation.

  ```bash
  python -m multiwfn2vesta.vesta_aim_overlay_style \
    input_overlay.vesta \
    output_labeled_overlay.vesta \
    --path-element Xe \
    --bcp-element Rn \
    --path-radius 0.060 \
    --bcp-radius 0.180 \
    --split-bcp-phase \
    --label-bcp-sites \
    --label-mode 1 \
    --label-font-size 18 \
    --label-offset 0.650
  ```

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
- For periodic or large-cell overlays, whole-cell camera framing can make
  Multiwfn-like BCP radii appear nearly invisible.  Before changing style,
  make a zoom-only render copy by editing only the final `SCENE` scalar and
  confirm the points are really present.
- When BCP-only naming controls pass but the full overlay still hides BCPs,
  prioritize checks in this order: identical-coordinate path samples over BCPs,
  phase draw order, depth/camera scale, then whether VESTA rewrote or ignored
  `SITET`/`ATOMT` rows in the saved multi-phase file.
- For periodic IGMH+AIM overlays, a strict top/surface-normal projection can
  hide BCPs even when the sites are present and styled.  Treat that as a camera
  problem.  Use the VESTA CLI three-view exporter and, if needed, a temporary
  per-view camera tilt such as `--extra-rotate top x -8`; do not shift AIM path
  or BCP coordinates for the final figure.

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

Ag(111)+benzene BCP-only display diagnostic:

```text
smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_render_20260609/
smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_zoom_render_20260609/
```

Observed:

- BCP-only front/right/top VESTA exports are valid `3048 x 1500` RGB PNGs.
- The front whole-cell view shows three small orange BCP points.
- The zoom-only front view changes only `SCENE` `0.800 -> 2.400` and shows the
  same three BCP points clearly.
- The full overlay's BCP invisibility is therefore a visibility problem, not a
  missing-record problem.

Ag(111)+benzene BCP naming diagnostic:

```text
smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_name_diagnostic_20260609/
```

Observed:

- VESTA rendered the combined naming matrix and each single-variant BCP-only
  control.
- Tested naming combinations: `N+CP000*_N`, `N+BCP*`, `Rn+CP*_N`,
  `Rn+RBCP*`, `Xe+CP*_N`, `C+CP*_N`, and `He+CP*_N`.
- Pixel counting found colored BCP pixels in every single-variant render.
- Do not treat `CP000*_N` naming as the primary cause unless a future
  multi-phase-specific diff proves otherwise.

Ag(111)+benzene full IGMH+AIM split-BCP three-view render:

```text
smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_cli_rotate_split_bcp_final_20260609/
```

Observed:

- VESTA opened one render input once and exported front/right/top PNGs through
  CLI `-rotate_*`, `-flush`, and `-export_img`.
- The output directory has one `*_render_input.vesta`, `dg_inter.cub`,
  `sl2r.cub`, and three PNGs.  It does not have three view-specific `.vesta`
  files.
- All PNGs are `6096 x 3052`.
- Orange BCP pixel counts: front `478`, right `363`, top `138`.
- Strict top projection hid BCPs; `--extra-rotate top x -8` made BCPs visible
  by camera tilt only.  AIM path points and BCP coordinates were not moved.

## Failure notes

- Full `unittest discover` currently fails because old tests still import
  `src.multiwfn_vesta`; use focused tests until package naming is repaired.
- VESTA Windows interop may return nonzero or timeout after exporting an image.
  Check the output file and run a cleanup close/taskkill command.
