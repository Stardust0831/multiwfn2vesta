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

## 2026-06-08: VESTA no-focus rendering and single compass

- Added `scripts/render_vesta_nofocus.py`, an experimental Windows interop
  wrapper that launches VESTA through PowerShell
  `Start-Process -WindowStyle Minimized`, waits for export, and cleans only
  workspace-scoped `VESTA.exe` processes.
- Added `docs/vesta_nofocus_rendering.md`.
- Retested on the current Ag(111)+benzene IGMH+AIM right-view `.vesta` outside
  this Git repository's tracked tree.  The minimized route returned success
  and wrote a valid `3014 x 1600` PNG.  A correctly quoted PowerShell process
  check found no residual `VESTA.exe` with command line matching
  `G:\work\multiwfn2vesta`.
- Added `scripts/add_single_view_compass.py`, which adds one screen-fixed
  VESTA-like lower-left compass to an exported PNG.
- Current multi-phase overlay recommendation: set `COMPS 0` in render-copy
  `.vesta` files, export the PNG, then draw one post-render compass.  The
  compass script clears its lower-left area before drawing, so repeated runs do
  not accumulate arrows.
- Updated `docs/skills/vesta_camera_and_layers_skill.md` with the no-focus
  wrapper and single-compass workflow.
- WSL/PowerShell pitfall: quote `Where-Object { $_.Name ... }` scripts with
  bash single quotes or escape `$`; bash double quotes expand `$_` before
  PowerShell receives the script.

## 2026-06-08: Follow-up on focus and compass

- User confirmed the minimized Windows VESTA wrapper still steals mouse focus.
  Keep `scripts/render_vesta_nofocus.py` as an explicit one-shot automation
  path only; do not treat it as a no-disruption renderer.
- Fixed the post-render compass arrowhead geometry in
  `scripts/add_single_view_compass.py`.  The previous head geometry made the
  triangle appear to point backward even when the axis vector was correct.

## 2026-06-08: Maintained three-view generator

- Added `scripts/vesta_three_views.py`.
- The script starts from one `.vesta` file and writes front/right/top view
  variants by replacing the global `SCENE` block.
- It copies relative `IMPORT_DENSITY` and `IMPORT_TEXTURE` cube files into the
  output directory so generated view files remain self-contained for VESTA
  export.
- It sets `COMPS 0` by default for multi-phase overlays, avoiding duplicated
  VESTA compass arrows; post-render compass drawing remains a separate step.
- Rendering is opt-in through `--render-command` because local VESTA automation
  still steals desktop focus.
- Smoke-verified without rendering on the Ag(111)+benzene IGMH+AIM preferred
  style file: original structure colors, yellow AIM path points, orange BCPs,
  relative cube copies, and `COMPS 0` were preserved in the generated right
  view.

## 2026-06-08: Rendering and AIM style follow-up

- Additional non-focus rendering attempts did not produce a usable renderer:
  Linux VESTA lacked `libwebkit2gtk-4.0.so.37`, WSH minimized/no-active launch
  returned without a PNG, and PowerShell hidden launch timed out without a PNG.
- Updated AIM workflow notes: use one pseudo-element such as `Xe` for all AIM
  path sample points in VESTA overlays instead of mixed rare gases per branch.
  This keeps `ATOMT`/`SITET` styling deterministic and easier to inspect.
- For BCP visibility, prefer smaller yellow path points plus larger orange
  BCPs before enabling AIM bonds.
