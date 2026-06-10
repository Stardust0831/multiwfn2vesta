# Skill: Reusable AIM+IGMH VESTA overlays

## When to use

Use this workflow when a VESTA file already contains a structure/IGMH cube
phase and an imported AIM path/critical-point phase, and the goal is to make a
repeatable figure-ready `.vesta` product plus optional front/right/top PNGs.

If the starting point is only Multiwfn IGMH cubes, first create the IGMH cube
layer with:

```bash
multiwfn2vesta cube-preset igmh dg_inter.cub igmh_products \
  --texture-cube sl2r.cub
```

Then import/merge the AIM path/BCP phase in VESTA and run this style workflow
on the saved multi-phase file.

## Maintained CLI

Preferred unified entry point:

```bash
multiwfn2vesta aim-igmh \
  input_overlay.vesta \
  output_dir
```

If `multiwfn2vesta` is not on `PATH`, add the workspace-local launcher:

```bash
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH
```

It writes:

- `<output_dir>/<stem>_styled.vesta`
- `<output_dir>/<stem>_aim_igmh_recipe.md`
- copied relative cube dependencies such as `dg_inter.cub` and `sl2r.cub`

Rendering is explicit because Windows VESTA automation still steals focus:

```bash
multiwfn2vesta aim-igmh \
  input_overlay.vesta \
  output_dir \
  --render-three-views \
  --initial-view top \
  --extra-rotate top x -8 \
  --scale 2
```

## Defaults

The high-level CLI encodes the current Ag(111)+benzene IGMH+AIM experience:

- AIM path samples: pseudo-element `Xe`, radius `0.0600`, RGB `255 230 0`.
- BCPs: pseudo-element `Rn`, radius `0.1800`, RGB `255 80 0`.
- Keep all AIM path samples, including samples colocated with BCPs.
- Do not move AIM path or BCP coordinates.
- Clear AIM-phase `SBOND`; keep real structure bonds via global `BONDS 1`.
- Split BCPs into a final phase by default so they draw after path samples.
- Copy relative `IMPORT_DENSITY` and `IMPORT_TEXTURE` cube files beside the
  styled `.vesta`.
- Write a markdown recipe manifest for reproducibility.
- For three-view rendering, default to VESTA CLI `cli-rotate` mode, `COMPS 0`,
  post-render single compass, and the current `top x -8` temporary camera tilt.

## Useful options

```bash
--stem NAME
--output-vesta FILE
--manifest FILE
--strict-cubes
--no-copy-cubes
--path-element Xe
--path-radius 0.060
--path-rgb 255 230 0
--bcp-element Rn
--bcp-radius 0.180
--bcp-rgb 255 80 0
--no-split-bcp-phase
--keep-aim-sbond
--structure-bonds-off
--label-bcp-sites
--bcp-label-prefix BCP
--render-three-views
--views front right top
--initial-view top
--no-default-top-tilt
--extra-rotate top x -8
--compass post
--scale 2
--timeout 240
--vesta-dir tools/VESTA-win64
```

Use `--label-bcp-sites` only when native VESTA site labels are desired.  It
renames BCP sites to `BCP1`, `BCP2`, ... and sets `LABEL 1`.  Native VESTA
label placement can overlap for nearby BCPs, so post-render labels remain
better for publication figures.

## Three-view rule

The maintained renderer must start from one source `.vesta`, open it once in
VESTA, and export images by command-line rotations:

```text
open styled.vesta -> export front -> rotate -> export right -> rotate -> export top -> close
```

Do not make three persistent front/right/top `.vesta` files as the primary
workflow.  `scripts/vesta_three_views.py --mode scene-copies` is only a
diagnostic fallback.

## Validation checklist

Before trusting an AIM+IGMH product:

- `rg -n 'IMPORT_DENSITY|IMPORT_TEXTURE' styled.vesta` still finds the cube
  records, and the referenced relative cubes exist beside the styled file.
- `rg -n 'AIM BCP final|Xe|Rn|BONDS|SBOND' styled.vesta` shows yellow `Xe`
  path sites, orange `Rn` BCP sites, final BCP phase, and `BONDS   1`.
- No `0.02200` AIM `SBOND` radius remains unless `--keep-aim-sbond` was used.
- If rendered, the output directory contains at most one `*_render_input.vesta`
  and the PNGs; it should not contain three view-specific `.vesta` files.
- For strict top views, if BCPs are hidden by projection, use a temporary
  camera tilt such as `--extra-rotate top x -8`; do not move coordinates.

## Ag(111)+benzene smoke

Dry smoke command:

```bash
bin/multiwfn2vesta aim-igmh \
  /mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/products/ag111_benzene_igmh_aim_paths_single_xe_yellow_bcp_periodic_overlay.vesta \
  /mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/unified_cli_smoke_20260610 \
  --stem ag111_benzene_igmh_aim_unified_cli \
  --label-bcp-sites
```

Observed output:

```text
smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/unified_cli_smoke_20260610/
```

- `ag111_benzene_igmh_aim_unified_cli_styled.vesta`
- `ag111_benzene_igmh_aim_unified_cli_aim_igmh_recipe.md`
- `dg_inter.cub`
- `sl2r.cub`

This smoke did not start VESTA.  It verified the reusable style/cube/manifest
pipeline without a focus-stealing render.
