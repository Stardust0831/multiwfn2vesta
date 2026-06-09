# Skill: VESTA camera reuse, layers, and frame export

## When to use

Use this workflow when a VESTA `.vesta` file needs reproducible camera angles,
front/right/top PNG exports, multi-phase layer show/hide control, or trajectory
style frame sequences.

## Key facts from local reverse engineering

- VESTA overlays are stored as multiple phases in one `.vesta` file.
- A multi-phase file has one shared `STYLE` block.
- Observed VESTA-saved phases may each contain `PHASON` and `QCORIG`.
- Observed multi-phase files have one global `SCENE`, not one `SCENE` per
  phase.
- `SCENE` is the primary camera/view record:

  ```text
  SCENE
   4x4 matrix
   x_shift y_shift
   unknown_scalar
   zoom_like_scalar
  ```

- No local sample has confirmed a true per-phase visibility flag. Do not treat
  `PHASON` or `QCORIG` as visibility controls without a GUI hidden-phase diff.

## Recommended interfaces

### `copy-camera`

Use this when a user has tuned one `.vesta` file manually and wants the same
view in generated outputs.

Minimum behavior:

1. Read `SCENE` from the source `.vesta`.
2. Replace the target `.vesta` `SCENE` with the source `SCENE`.
3. Preserve all other records byte-for-byte as much as possible.

Optional full-view behavior may also copy:

- `PROJT`
- `DPTHQ`
- `BKGRC`
- `LIGHT0` to `LIGHT3`

Default should copy only `SCENE` because `STYLE` is shared and can affect atom,
bond, surface, and label rendering.

### `set-phase-visible`

Use this for layer toggling or frame rendering.

Supported selectors should be:

- 1-based phase index.
- `TITLE` substring.

Recommended modes:

- `remove`: render copy contains only visible phases. This is the safest first
  implementation.
- `style`: keep inactive phases but set their `SITET` radii to `0.0000`, set
  alpha-like fields to `0`, and clear inactive `SBOND`. This must be validated
  with VESTA image exports.
- `dim`: keep inactive phases visible but make them smaller, gray, and more
  transparent for history trails.

Do not edit `QCORIG` for visibility. It may affect origin/alignment.

Do not edit `PHASON` for visibility until a hidden-phase GUI diff proves its
role. It looks more like a per-phase transform/orientation matrix in current
samples.

### `export-three-views`

Use this when users need reproducible front/right/top images.

Maintained behavior:

1. Start from one input `.vesta`.
2. Prepare at most one `*_render_input.vesta` to make `COMPS 0` and relative
   cube-file colocation explicit.
3. Open that input once in VESTA.
4. Export front/right/top PNGs by applying VESTA command-line `-rotate_*`,
   `-flush`, and `-export_img` operations in one command stream.
5. Keep the original `.vesta` unchanged.  Do not create persistent
   front/right/top `.vesta` files as the main workflow.

Initial named views:

- `front`
- `right`
- `top`

Use `--initial-view` when the saved source already opens in a known view.  Use
`--extra-rotate VIEW AXIS DEGREES` for a temporary per-view camera tilt; the
script undoes that rotation after export, so it is not a coordinate change.

Maintained script:

```bash
python3 scripts/vesta_three_views.py input.vesta three_views_out \
  --initial-view top \
  --extra-rotate top x -8 \
  --comps off \
  --scale 2
```

This writes PNGs directly.  It may write one `*_render_input.vesta` beside the
PNGs when `COMPS` or relative cube placement must be adjusted for rendering.
It does not write separate view-specific `.vesta` files unless the explicit
compatibility mode `--mode scene-copies` is requested.

Use `--mode scene-copies` only as a diagnostic or fallback for environments
where VESTA's native `-rotate_*` commands cannot be used.

For multi-phase overlays, suppress VESTA's native compass before rendering:

1. Set `COMPS 0` in the render-copy `.vesta`.
2. Export the PNG.
3. Add exactly one screen-fixed lower-left compass in post-processing.

Current local implementation:

```bash
python3 scripts/add_single_view_compass.py view.png --view right
```

The post-processing script clears its lower-left compass area before drawing,
so repeated runs do not accumulate arrows.  This is more reliable than leaving
`COMPS 1` in multi-phase VESTA files, where native compass arrows can appear
duplicated.

### `export-frame-sequence`

Use this for trajectory-style visualization or progressive layer reveal.

Suggested modes:

- `current-only`: base phase plus one active frame phase.
- `cumulative`: base phase plus all frame phases up to the current one.
- `trail`: base phase, current phase bright, previous phases dimmed.

Progress bar strategy:

- Prefer `external` progress bars drawn after PNG export. A true 2D VESTA HUD
  field has not been identified.
- Treat `vesta-phase` progress bars as experimental because pseudo-atoms used
  as a progress indicator are affected by camera, depth, zoom, and clipping.

## VESTA CLI export pattern

From WSL, use the Windows VESTA executable with individually quoted Windows
paths:

```bash
VESTA='G:\work\multiwfn2vesta\tools\VESTA-win64\VESTA.exe'
IN=$(wslpath -w input.vesta)
OUT=$(wslpath -w output.png)

timeout 40s /mnt/c/WINDOWS/system32/cmd.exe /c "$VESTA" \
  -open "$IN" \
  -export_img scale=1 "$OUT" \
  -flush -close
```

For a single VESTA session with rotations:

```bash
VESTA.exe -open input.vesta \
  -export_img scale=2 front.png -flush \
  -rotate_y -90 -flush \
  -export_img scale=2 right.png -flush \
  -rotate_y 90 -flush -rotate_x -90 -flush \
  -export_img scale=2 top.png -flush \
  -close
```

VESTA can time out or return a nonzero code after producing output. Always
check that the target `.vesta` or `.png` exists.

For lower focus interference on Windows, use the experimental branch-local
wrapper:

```bash
python3 project/scripts/render_vesta_nofocus.py input.vesta output.png \
  --scale 2 --clean-before
```

It launches VESTA through PowerShell `Start-Process -WindowStyle Minimized`,
waits for export, and cleans only `VESTA.exe` processes whose command line
contains this workspace path.  This is not true headless rendering and has
been confirmed to still steal desktop focus, so only use it when that
interruption is acceptable.

## Validation checklist

Before relying on a generated image sequence:

- Confirm phase counts: `MOLECULE`/`CRYSTAL`, `TITLE`, `PHASON`, `QCORIG`,
  and `STYLE`.
- Confirm exactly one global `SCENE` exists in current VESTA-saved files.
- For AIM overlays, confirm inactive/active phase edits did not change atom
  coordinates or `QCORIG`.
- Export at least one PNG after any new camera or visibility edit.
- For oversized structures, verify boundary fit and CP visibility visually.
- For three-view presets, validate on a non-planar molecule to catch sign
  convention mistakes.
- For multi-phase overlays, confirm the generated render input has `COMPS 0`
  and final PNGs have only one lower-left compass.
- If a strict top/surface-normal projection hides interface BCPs, prefer a
  temporary camera tilt such as `--extra-rotate top x -8`; do not move AIM/BCP
  coordinates to fix a view/projection problem.

## Known risks

- Hidden phase state may be stored in a field not present in all-visible local
  samples.
- `STYLE` is shared, so global `BONDS`, `ATOMS`, and model flags can affect all
  phases.
- Native VESTA `-rotate_*` sign conventions still need calibration per source
  camera.  Use `--initial-view` and a small smoke render before a long batch.
- The final `SCENE` scalar is zoom-like in local reasoning, but its direction
  and numeric scale must be measured with exported PNGs.
- Alpha-like `SITET`/`ATOMT` columns may not fully hide sites in every render
  mode; `remove` mode is safer for first implementation.

## Real smoke result

Ag(111)+benzene IGMH+AIM split-BCP overlay:

```text
smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_cli_rotate_split_bcp_final_20260609/
```

Command pattern:

```bash
python3 project/scripts/vesta_three_views.py \
  smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/products/ag111_benzene_igmh_aim_paths_single_xe_yellow_bcp_splitphase_periodic_overlay.vesta \
  smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_cli_rotate_split_bcp_final_20260609 \
  --stem ag111_benzene_igmh_aim_paths_single_xe_yellow_bcp_splitphase_periodic_overlay \
  --initial-view top \
  --extra-rotate top x -8 \
  --scale 2 \
  --clean-before
```

Observed:

- One render input `.vesta`, two cube files, and three PNGs were produced.
  No front/right/top `.vesta` files were produced.
- All PNGs are `6096 x 3052`.
- Orange BCP pixel counts: front `478`, right `363`, top `138`.
- The strict top projection hid the BCPs; the temporary `top x -8` camera tilt
  made them visible without changing coordinates.

## Next experiments

1. Save a two-phase file from VESTA with phase 2 manually hidden and diff it
   against the all-visible file.
2. Export the same file with several edited final `SCENE` scalar values to
   calibrate zoom/padding.
3. Export edited `SCENE` pan values to calibrate screen direction.
4. Validate `style` hiding by zeroing phase 2 `SITET` radii/alpha and clearing
   phase 2 `SBOND`.
5. Calibrate front/right/top matrices on H2O and a larger AIM example.
