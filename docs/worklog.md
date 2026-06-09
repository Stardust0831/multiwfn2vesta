# Worklog

## 2026-06-10: README branch-state refresh

- User requested a README update and branch simplification because the branch
  state looked confusing.  Commits for this maintenance pass use the
  repository-local identity `Stardust0831 <13862180016@163.com>`.
- Rechecked project branch state with `git fetch --prune`,
  `git status --short --branch`, `git branch --all --verbose --no-abbrev`,
  and `git ls-remote --heads origin`.
- Result: local `main` tracks `origin/main`, `origin/HEAD` points to
  `origin/main`, and the GitHub remote exposes only `refs/heads/main`.
  There is no extra branch to merge back in this pass.
- Updated README to state that the apparently strange branch history is
  already represented as commits on `main`, and that future experiment
  branches should be short-lived workspaces whose useful commits are merged or
  fast-forwarded into `main`.
- README now also repeats the supported day-to-day CLI entry point:
  add `/mnt/g/work/multiwfn2vesta/project/bin` to `PATH` and use
  `multiwfn2vesta`, or run from the repo root with
  `PYTHONPATH=src python3 -m multiwfn2vesta.cli`.

## 2026-06-10: Multiwfn IRI/RDG runner and README branch check

- User requested another README update, branch simplification if needed, and
  commits using repository-local identity `Stardust0831`.
- Rechecked project branch state: local `main` tracks `origin/main`,
  `origin/HEAD` points to `origin/main`, `git ls-remote --heads origin`
  returns only `refs/heads/main`, and repository-local identity is
  `Stardust0831 <13862180016@163.com>`.  There is no feature branch to merge
  back.
- Added `multiwfn2vesta.multiwfn_iri` and unified CLI command
  `multiwfn2vesta iri-run`, with aliases `multiwfn-iri` and `rdg-run`, an
  interactive menu entry, and console script `multiwfn2vesta-iri-run`.
- The command discovers Multiwfn, writes `multiwfn_iri_input.txt`, stdout and
  stderr logs, runs Multiwfn in `multiwfn_iri_raw/`, preserves raw
  `func1.cub`/`func2.cub`, writes processed `<stem>_IRI1.cub` and
  `<stem>_IRI2.cub`, copies `output.txt` when present, and calls
  `cube-preset iri` to write a mapped-surface `.vesta` unless `--no-vesta` is
  used.
- Hardened failure handling after read-only pre-commit review: missing
  Multiwfn/input paths return a stable CLI error, Multiwfn nonzero exits set
  an `ERROR:` message with log paths, and timeout/launch failures write
  partial logs instead of traceback.
- Ran a real H2O noGUI smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_iri_run_smoke_20260610/`.
  It selected
  `/mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI`,
  returned `0`, generated raw `func1.cub`/`func2.cub`, processed
  `h2o_IRI1.cub`/`h2o_IRI2.cub`, and wrote `h2o_iri_cube.vesta` plus recipe
  without launching VESTA.
- Smoke recipe notes: surface grid `24 x 46 x 32`, surface data range
  `0.37856` to `11.3977`, texture data range `-0.04` to `0.524624`,
  `tex_percent_range` `0.0` to `0.14361986693619327`,
  `tex_reference_source: surface-nearest`, and
  `surface_nearest_fallback: true`.
- Updated README, usage docs, IRI/cube/CLI skill notes,
  ABACUS/Multiwfn planning notes, and the analysis matrix so IRI/RDG is no
  longer documented as only a future command stream.
- Focused validation passed: 36 tests across `tests.test_multiwfn_iri`,
  `tests.test_cli`, and `tests.test_iri_cube`; `py_compile` passed for
  `multiwfn_iri.py` and `cli.py`.
- Final no-GUI validation passed before commit: 118 tests across Molden
  checking, ABACUS Molden/Mulliken, cube preset, Multiwfn IRI, cube-to-VESTA,
  unified CLI, AIM+IGMH, executable discovery, Multiwfn AIM, IRI cube
  handling, AIM VESTA conversion, and VESTA atom coloring.  `bin/multiwfn2vesta
  iri-run --help`, top-level `bin/multiwfn2vesta --help`, and
  `git diff --check` also passed.
- Feature implementation commit was pushed to GitHub `main` at
  `16f345c76053454cdca026d707f885383d9122c3`
  (`Add Multiwfn IRI runner`), and `HEAD` matched `origin/main` after
  `git fetch origin main`.

## 2026-06-10: Cube analysis presets

- Added `multiwfn2vesta.cube_preset`, a thin analysis-oriented preset layer
  over the existing `cube_vesta.run_workflow` backend.  It deliberately keeps
  all VESTA writing in `cube-vesta`.
- Presets implemented:
  `density`/`rho`/`charge-density`/`scalar`,
  `signed`/`orbital`/`mo`/`wavefunction`/`abacus-wfc`/
  `density-difference`/`dual-descriptor`,
  `elf`/`abacus-elf`,
  `lol`,
  `iri`/`rdg`/`nci`/`weak-interaction`,
  and `esp`/`mep`/`electrostatic-potential`/`density-esp`.
- IRI/RDG/NCI defaults require `--texture-cube`, use `--isosurface 1.0`,
  physical texture range `-0.04` to `0.04`, and `surface-band` texture
  scaling.  ESP/MEP defaults require a texture cube and intentionally leave
  the physical texture range for the user to set when figures need to be
  comparable.
- Integrated the command into the unified CLI, interactive chooser, aliases
  `preset` and `analysis-cube`, and console script
  `multiwfn2vesta-cube-preset`.
- Updated README, usage docs, cube workflow skill notes, CLI skill notes,
  ABACUS/Multiwfn planning notes, and the analysis matrix.  The docs now
  distinguish implemented display presets from future Multiwfn command
  streams that would generate the underlying cubes.
- Synthetic no-GUI smoke directory:
  `/mnt/g/work/multiwfn2vesta/smoke/cube_preset_smoke_20260610/`.
  It generated `orbital_products/orbital_signed_cube.vesta` from the
  `orbital` alias and `iri_products/iri2_iri_cube.vesta` from the `rdg`
  alias with a texture cube.  `SUMMARY.md` records the exact commands and
  output paths.
- Focused validation passed: 28 tests across `tests.test_cube_preset` and
  `tests.test_cli`, `py_compile` for `cube_preset.py` and `cli.py`,
  `multiwfn2vesta --help`, and `multiwfn2vesta cube-preset --list-presets`.
- Full no-GUI regression passed with 108 tests across Molden checking, ABACUS
  Molden/Mulliken, cube preset, cube-to-VESTA, unified CLI, AIM+IGMH,
  executable discovery, Multiwfn AIM, IRI cube handling, AIM VESTA conversion,
  and VESTA atom coloring.
- Read-only pre-commit review findings were addressed before commit: the new
  implementation/test files are explicitly included, package metadata now
  requires Python `>=3.7`, and `--tex-percent` writes
  `effective_tex_range_source: explicit-percent` plus an explicit note that
  physical texture scaling was not applied.
- Feature implementation commit was pushed to GitHub `main` at
  `c58600d3b4f276c43eef4095669b6402835df8ff`
  (`Add cube analysis presets`).

## 2026-06-10: ABACUS Molden wrapper and README branch cleanup

- Added `multiwfn2vesta.abacus_molden` plus unified CLI command
  `multiwfn2vesta abacus-molden`.
- The wrapper exports ABACUS `interfaces/Multiwfn_interface/molden.py` from
  the selected git ref, defaulting to local ABACUS checkout
  `/mnt/g/work/multiwfn2vesta/downloads/abacus_latest_molden/abacus-develop`
  at `origin/develop`.
- Latest local ABACUS `origin/develop` evidence used for the smoke:
  commit `707f09266842c3340a0d5f7a21d3224306aafd58`, commit date
  `2026-06-09T10:41:56+08:00`, source path
  `interfaces/Multiwfn_interface/molden.py`.
- The command writes `<stem>_abacus_molden.py`,
  `<stem>_abacus_molden.stdout.txt`, `<stem>_abacus_molden.stderr.txt`, and
  `<stem>_abacus_molden_recipe.md`, then runs `molden-check --abacus` unless
  `--no-check` is supplied.
- Hardened the wrapper after read-only pre-commit review: it preflights
  `numpy`, `scipy`, and `matplotlib` in the selected Python environment,
  accepts `--python`, logs missing dependencies to stderr/recipe, treats a
  missing output Molden as failure even with `--no-check`, and writes partial
  stdout/stderr plus recipe on timeout instead of traceback.
- Updated README, usage docs, CLI skill notes, ABACUS/Multiwfn analysis skill
  notes, and the analysis matrix.  The docs now state that ABACUS
  `molden.py` needs `numpy`, `scipy`, and `matplotlib`, and that `--python`
  should point to the environment that has them.
- Added `multiwfn2vesta-abacus-molden` console-script entry points in
  `pyproject.toml` and `setup.py`, plus unified CLI aliases `molden` and
  `abacus-multiwfn-molden`.
- Ran a git-export smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/abacus_molden_wrapper_smoke_20260610/`.
  It exported `ABACUS_Multiwfn_abacus_molden.py` from ABACUS
  `origin/develop`, recorded SHA256
  `3c24c3260285b55f2eeac8421776bd07eb9ee0a22879507bc34a8bfa17563208`, and
  did not run a real ABACUS conversion.
- Final validation passed: 97 no-GUI unit tests, `py_compile` for
  `abacus_molden.py` and `cli.py`, `git diff --check`, `multiwfn2vesta
  --help`, and `multiwfn2vesta abacus-molden --help`.
- Branch state for this README cleanup remained simple: project `main` tracks
  `origin/main`, repository-local identity is
  `Stardust0831 <13862180016@163.com>`, and no extra local branch was present
  before the final push.

## 2026-06-10: ABACUS Mulliken atom coloring

- Added `multiwfn2vesta.abacus_mulliken` and unified CLI command
  `multiwfn2vesta abacus-mulliken-color`.
- The parser handles current ABACUS `mulliken.txt` blocks headed by
  `--- Ionic Step N ---`, atom headers `Atom N is LABEL`, `total charge on
  atom N`, and optional `total magnetism on atom N`.  It also accepts the
  older documentation style using `STEP:` and `Total Charge on atom:`.
- Supported properties are `charge`, `magnetism`, `magnetism-x`,
  `magnetism-y`, `magnetism-z`, and `magnetism-norm`.  The command selects
  the last ionic step by default, accepts `--step N`, maps values to VESTA
  sites by one-based atom index, and can write a selected-values CSV with
  `--write-values`.
- Checked ABACUS latest `origin/develop` evidence from
  `docs/advanced/elec_properties/Mulliken.md`,
  `source/source_io/module_mulliken/output_mulliken.cpp`, and reference
  `mulliken.txt.ref` files for `nspin=1/2/4`.  Multi-k output has the same
  file fields after k-point contributions are summed.
- Added focused tests for `nspin=1`, `nspin=2`, `nspin=4`, legacy format
  compatibility, ionic-step selection, VESTA `SITET` coloring, and CSV export.
- Focused parser/CLI tests passed, and `py_compile` passed for
  `abacus_mulliken.py` and `cli.py`.
- Ran a real CLI smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/abacus_mulliken_color_smoke_20260610/`:
  `abacus-mulliken-color` used the final ionic step, colored Fe1 red and Fe2
  blue from magnetism `+4/-4`, and wrote `values.csv` with the selected
  values.
- Final pre-commit no-GUI regression passed with 87 tests covering the
  maintained Molden, ABACUS Mulliken, cube-to-VESTA, unified CLI, AIM+IGMH,
  executable discovery, Multiwfn AIM, IRI cube, AIM VESTA, and atom-coloring
  modules.
- Read-only pre-commit review found one blocker: strict ABACUS Mulliken
  coloring could ignore surplus Mulliken atom indices because the generic
  atom-coloring backend intentionally allows partial mapping keys.  Fixed this
  in the ABACUS-specific entry by checking selected VESTA `STRUC` site indices
  against Mulliken atom indices before writing the output, and added a
  surplus-atom regression test.
- Re-ran the real CLI smoke after the strict-index fix.  The strict recheck
  wrote `colored_magnetism_strict_recheck.vesta` and
  `values_strict_recheck.csv` under the same smoke directory and reported
  `colored 2 atoms from Mulliken step 2`.

## 2026-06-10: README refresh, branch check, and signed cube preset

- Rechecked branch state for the README cleanup request.  After
  `git fetch --prune`, the project has only local `main` and remote
  `origin/main`; `origin/HEAD` points to `origin/main`, so there is no extra
  feature branch left to merge.
- Confirmed repository-local commit identity is
  `Stardust0831 <13862180016@163.com>`.
- Updated README repository status so the front page records the single
  maintained branch, SSH remote, and local commit identity.
- Added signed positive/negative isosurface support to
  `multiwfn2vesta cube-vesta`.  `--surface-mode signed --isosurface X` writes
  two `ISURF` entries, `+abs(X)` and `-abs(X)`, with yellow positive and blue
  negative defaults.  Zero magnitudes are rejected and all generated levels
  are checked against the cube data range.
- Added focused tests for the signed VESTA `ISURF` block, manifest fields,
  zero-level rejection, and negative-level range checking.
- Updated README, usage docs, cube workflow skill notes, ABACUS/Multiwfn
  planning notes, and the analysis matrix.  Signed cube display is now a
  maintained generic VESTA preset; Multiwfn command streams for producing
  orbital/density-difference/Fukui/dual-descriptor cubes remain future work.
- Validation passed with 78 no-GUI regression tests, `py_compile` for
  `cube_vesta.py` and `cli.py`, and `git diff --check`.
- Ran a signed cube CLI smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_signed_smoke_20260610/`.
  The output `.vesta` contains an `ISURF` block and the recipe records
  `surface_mode: signed`, data range `-0.3` to `0.4`, and isosurface levels
  `0.2, -0.2`.

## 2026-06-10: AIM path radius and BCP label research

- Updated `multiwfn2vesta.vesta_aim_overlay_style` so AIM bond-path sample
  points mapped to `Xe` use a maintained default radius of `0.0600` Angstrom.
  The BCP default remains `0.1800` Angstrom unless explicitly overridden.
- Updated focused tests so an old `0.0550` path style is patched to the new
  default `0.0600` in both `SITET` and `ATOMT`.
- Researched VESTA label support.  VESTA's documented atom-label mechanism can
  display either element names or site names near atoms, with a z-axis offset
  in Angstrom, and the Objects tab exposes per-site label visibility.  Public
  documentation did not reveal a stable arbitrary 3D text-object directive for
  `.vesta` files.
- Added `docs/vesta_bcp_labeling.md` and updated the AIM skill.  Recommended
  near-term BCP numbering is either to rename BCP site labels such as
  `CP0001_N` to concise `BCP1`/`BCP2` and enable VESTA atom/site labels, or to
  render with VESTA and add publication labels in a PNG/SVG post-processing
  step.  Direct non-empty `LBLAT` generation remains unimplemented until a
  GUI-save diff confirms the record syntax.
- Added `--label-bcp-sites` to `multiwfn2vesta.vesta_aim_overlay_style`.
  It rewrites BCP labels consistently across `STRUC`, `THERI`, and `SITET`,
  sets the BCP `SITET` label flag to `1`, and patches/inserts a global
  `LABEL` style line.  `LABEL 1` is the verified site-name mode; `LABEL 0`
  displays element names.
- Rendered BCP label smoke outputs under
  `/mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_text_label_experiment_20260610/`.
  `bcp_only/bcp_only_labelmode1.png` shows `BCP1`/`BCP2`/`BCP3`, while
  `bcp_only/bcp_only_labelmode0.png` shows `Rn`.  The full-overlay front
  render confirms native text appears in the real Ag(111)+benzene overlay,
  but close BCP labels overlap, so post-render annotation remains the
  publication-quality path.
- Generated a non-rendered Ag(111)+benzene check file outside the tracked
  project tree:
  `/mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/products/ag111_benzene_igmh_aim_paths_single_xe_yellow_bcp_splitphase_path006_periodic_overlay.vesta`.
  It contains no old `0.0550` yellow-Xe path style, has one `Xe` `ATOMT`
  radius `0.0600`, and keeps three `Rn` BCP records.

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
- Initial implementation started from one `.vesta` file and wrote
  front/right/top view variants by replacing the global `SCENE` block.  This
  was superseded on 2026-06-09 by the default `cli-rotate` workflow that opens
  one render input once and uses VESTA `-rotate_*` commands to export PNGs.
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

## 2026-06-09: Status check

- Confirmed the project repository is on branch `vesta-nofocus-render`, clean,
  and tracking `origin/vesta-nofocus-render`.
- Confirmed no workspace-scoped VESTA, ABACUS, or Multiwfn processes were
  running at the time of the check.
- Current recommended Ag(111)+benzene IGMH+AIM files remain the VESTA source
  under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/products/ag111_benzene_igmh_aim_paths_single_xe_yellow_bcp_periodic_overlay.vesta`
  and generated three-view VESTA files under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_single_xe_yellow_bcp/`.
- Rendering remains blocked as a background/no-disruption workflow.  The known
  Windows VESTA automation path still steals focus, so fresh PNG generation
  should stay explicit/opt-in until a separate non-focus route is validated.

## 2026-06-09: BCP visibility in single-Xe AIM overlay

- User reported that
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_single_xe_yellow_bcp/`
  has no rendered PNGs and that BCPs are not visible when opened manually in
  VESTA.
- Confirmed no PNGs exist in that directory; only `.vesta` and cube files were
  generated because rendering is disabled by default while VESTA steals focus.
- Confirmed BCP records are present: three `CP000*_N` sites exist in `STRUC`,
  `THERI`, and `SITET`, with orange styling.  They sit exactly on top of the
  first path points of the corresponding AIM paths.
- Added `src/multiwfn2vesta/vesta_aim_overlay_style.py` plus unit tests.  The
  patcher does not remove any path points.  It assigns path samples to one
  pseudo-element (`Xe` in the Ag smoke case), assigns BCPs to a separate
  pseudo-element (`Rn` in the Ag smoke case), clears AIM-phase `SBOND`, and
  leaves structure bonds enabled by default.
- Generated the revised smoke product:
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/products/ag111_benzene_igmh_aim_paths_single_xe_yellow_bcp_visible_periodic_overlay.vesta`.
- Generated revised three-view `.vesta` files under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_single_xe_yellow_bcp_visible/`.
  Validation found 588 `Xe` path points, 3 `Rn` BCP sites, BCP `SITET` radius
  `0.1800` with RGB `255 80 0`, and `COMPS 0` in all three views.
- PNG rendering was not run at that point because the available VESTA
  automation route still steals focus; a later explicit user request triggered
  the real-render diagnostic recorded below.

## 2026-06-09: Real BCP display diagnostic render

- User explicitly requested real VESTA rendering to confirm BCP point display,
  accepting the known focus-stealing risk for this diagnostic.
- Rendered a BCP-over-structure front view:
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_display_diagnostic_20260609/ag111_benzene_igmh_aim_bcp_periodic_overlay_front.png`.
- Rendered strict BCP-only front/right/top views from the single-phase
  periodic BCP diagnostic under:
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_render_20260609/`.
  The PNGs are valid `3048 x 1500` RGB images.
- Rendered an additional zoom-only BCP diagnostic:
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_zoom_render_20260609/ag111_benzene_aim_interface_bcp_only_periodic_front_zoom2p4.png`.
  The `.vesta` copy changes only the final `SCENE` zoom-like scalar from
  `0.800` to `2.400`; BCP coordinates, `SITET` radius `0.0700`, and orange
  RGB style are unchanged.
- Visual inspection: the BCP-only front render shows three small orange BCP
  points, and the zoom diagnostic shows the same three points clearly.
  Conclusion: VESTA can render BCP sites from `CP000*_N` records.  The
  full-overlay invisibility is therefore a size, overlap, or occlusion issue,
  not absent BCP data.
- No workspace-scoped VESTA, Multiwfn, ABACUS, or MPI process remained after
  the diagnostic render.

## 2026-06-09: BCP atom naming diagnostic

- User asked whether BCP invisibility might be caused by atom naming or element
  symbols, and requested additional BCP-only tests.
- Generated BCP-only naming controls under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_name_diagnostic_20260609/`.
  The controls include one combined matrix and single-variant files for:
  `N+CP000*_N`, `N+BCP*`, `Rn+CP*_N`, `Rn+RBCP*`, `Xe+CP*_N`,
  `C+CP*_N`, and `He+CP*_N`.
- Rendered the matrix and all single variants with VESTA.  Every PNG is a
  valid `3048 x 1500` RGB image.
- Visual inspection: the combined matrix shows all tested groups of BCP
  points, and the single `N+CP000*_N` file shows the three original-style BCP
  labels.
- Pixel validation with PIL found colored BCP pixels in every single-variant
  image: `78` high-saturation colored pixels per PNG.  This confirms that
  `CP000*_N` labels and the tested element symbols do not by themselves stop
  VESTA from drawing BCP-only sites.
- Current conclusion for the full Ag(111)+benzene IGMH+AIM overlay: keep
  investigating path-point overlap at identical coordinates, phase draw order,
  depth/scale, and `SITET`/`ATOMT` style-table interactions before changing
  BCP label naming.

## 2026-06-09: VESTA CLI three-view export and full-overlay BCP visibility

- User corrected the maintained three-view requirement: final export should
  load one `.vesta` once, then use command-line rotations and image exports.
  Do not treat three persistent front/right/top `.vesta` files produced by
  `SCENE` patching as the main workflow.
- Checked VESTA manual chapter 17 and local project evidence.  The relevant
  VESTA CLI commands are `-rotate_x`, `-rotate_y`, `-rotate_z`, `-flush`, and
  `-export_img`.
- Reworked `scripts/vesta_three_views.py`.  Default `cli-rotate` mode prepares
  at most one `*_render_input.vesta` for `COMPS 0` and relative cube
  colocation, opens that input once in VESTA, then exports front/right/top PNGs
  by command-line rotations in one command stream.  The old `SCENE` copy path
  remains as `--mode scene-copies` only.
- Added `--initial-view` so a saved source can declare what its current camera
  already represents, and `--extra-rotate VIEW AXIS DEGREES` for temporary
  per-view camera tilts.  Temporary rotations are undone after the PNG export
  and are not coordinate changes.
- Removed the BCP coordinate-offset interface from
  `multiwfn2vesta.vesta_aim_overlay_style`.  The user clarified that the BCP
  issue is view/projection, not wrong coordinates.  Split BCP phases now keep
  all AIM path points and all BCP coordinates unchanged.
- Real-rendered the final Ag(111)+benzene IGMH+AIM split-BCP three views with
  `--initial-view top --extra-rotate top x -8 --scale 2` under:
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_cli_rotate_split_bcp_final_20260609/`.
  The output contains one render input, `dg_inter.cub`, `sl2r.cub`, and three
  PNGs; it does not contain three view-specific `.vesta` files.
- Final PNG validation: all images are `6096 x 3052`; orange BCP pixel counts
  are front `478`, right `363`, top `138`.  Strict top projection hid the BCPs,
  while the temporary top `x -8` camera tilt made them visible without moving
  any BCP/path coordinates.  No workspace-scoped `VESTA.exe` process remained
  afterward.

## 2026-06-10: Reusable AIM+IGMH VESTA CLI

- User asked to close the Ag(111)+benzene AIM+IGMH plotting experience into
  reusable Python code with CLI options.
- Added `multiwfn2vesta.aim_igmh_vesta`, a high-level wrapper that starts from
  a saved structure/IGMH cube + AIM overlay `.vesta`, applies the maintained
  AIM path/BCP style, copies relative cube dependencies, writes a markdown
  recipe manifest, and optionally calls the one-source/one-session three-view
  renderer.
- Default high-level style now matches the current Ag interface recipe:
  yellow `Xe` AIM path samples with radius `0.0600`, orange `Rn` BCPs with
  radius `0.1800`, AIM `SBOND` cleared, real structure bonds retained, BCPs
  split into the final phase, and no coordinate movement or path-point
  deletion.
- Rendering remains explicit via `--render-three-views` because VESTA Windows
  automation still steals focus.  The render command delegates to
  `scripts/vesta_three_views.py` in `cli-rotate` mode, so it opens one
  `.vesta` once and exports images through CLI rotations rather than making
  three persistent view-specific `.vesta` files.
- Added a console entry point `multiwfn2vesta-aim-igmh` in both
  `pyproject.toml` and `setup.py`, while keeping `python -m
  multiwfn2vesta.aim_igmh_vesta` as the direct tested route.
- Added unit tests in `tests/test_aim_igmh_vesta.py` for cube reference
  discovery, default style output, cube copying, manifest content, render
  command planning, and compass/`COMPS` mapping.  These tests do not launch
  VESTA.
- Added skill documentation:
  `docs/skills/aim_igmh_vesta_skill.md`.
- Ran a real Ag dry smoke without VESTA rendering:
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/reusable_cli_smoke_20260610/`.
  The directory contains the styled `.vesta`, recipe markdown, `dg_inter.cub`,
  and `sl2r.cub`.

## 2026-06-10: Unified interactive CLI

- User asked for better interactivity and a more convenient global CLI entry,
  ideally requiring only one path to be added to the environment.
- Added `multiwfn2vesta.cli`, a maintained dispatcher for stable workflows.
  With no arguments it opens an interactive chooser.  With subcommands it
  dispatches scriptable workflows:
  `multiwfn2vesta aim-pdb ...` and `multiwfn2vesta aim-igmh ...`.
- Added workspace-local launcher `bin/multiwfn2vesta`.  It automatically adds
  `project/src` to Python's import path, so the user can run it after only:
  `export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH`.
- Registered editable-install console scripts in both `pyproject.toml` and
  `setup.py`: `multiwfn2vesta`, `multiwfn2vesta-aim-pdb`, and
  `multiwfn2vesta-aim-igmh`.
- Added no-GUI tests in `tests/test_cli.py` for help text, command dispatch,
  aliases, unknown-command handling, interactive quit, and the AIM+IGMH
  interactive argument builder.
- Ran a real unified CLI dry smoke without rendering:
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/unified_cli_smoke_20260610/`.
  The output contains the styled `.vesta`, recipe markdown, `dg_inter.cub`,
  and `sl2r.cub`.

## 2026-06-10: Multiwfn/VESTA discovery and wavefunction AIM runner

- User asked whether Multiwfn invocation is integrated, and requested a scheme
  where Multiwfn and VESTA can be found from environment variables and `PATH`,
  while the workflow accepts a Molden/wavefunction path rather than only
  existing `paths.pdb`/`CPs.pdb`.
- Added `multiwfn2vesta.executables`.  `multiwfn2vesta discover` now reports
  candidate executables and a selected default.  Multiwfn discovery accepts
  explicit `--multiwfn`, `MULTIWFN_PATH`, `MULTIWFNPATH`, `Multiwfnpath`,
  `MultiwfnPATH`, `MultiwfnPath`, `MULTIWFN_EXECUTABLE`, workspace-local
  tools, and then `PATH`.  VESTA discovery accepts `VESTA_PATH`, `VESTA_DIR`,
  `VESTAPATH`, `VestaPATH`, `Vestapath`, `VESTA_EXECUTABLE`, workspace-local
  tools, and then `PATH`.
- Discovery prefers workspace-local Multiwfn noGUI and workspace-local
  `tools/VESTA-win64/VESTA.exe` before arbitrary external `PATH` hits, unless
  an explicit path or environment variable is supplied.
- Added `multiwfn2vesta.multiwfn_aim` and the unified CLI command
  `multiwfn2vesta aim-run <wavefunction> <output_dir>`.  It runs Multiwfn AIM
  in the output directory, writes `multiwfn_aim_input.txt`,
  `multiwfn.stdout.txt`, and `multiwfn.stderr.txt`, then converts generated
  `paths.pdb`/`CPs.pdb` to `aim_atoms_only.vesta` by default.
- Multiwfn subprocess environment is pinned to the selected executable
  directory through `Multiwfnpath`, `MULTIWFNPATH`, and `MultiwfnPATH`.
  Relative explicit `--multiwfn ./...` paths are resolved before changing
  `cwd` to the output directory.
- Failure semantics: if Multiwfn returns 0 but does not generate `paths.pdb`,
  the CLI returns 3 and points to the logs.  `--allow-missing-paths` keeps
  Multiwfn's raw return code for diagnostic-only runs.
- Added installable console scripts: `multiwfn2vesta-discover` and
  `multiwfn2vesta-aim-run`, while keeping the preferred entry point as
  `multiwfn2vesta discover` and `multiwfn2vesta aim-run`.
- Added focused no-GUI tests in `tests/test_executables.py` and
  `tests/test_multiwfn_aim.py`, plus CLI dispatch/interactive coverage.
- Real H2O smoke succeeded:
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_aim_cli_smoke_20260610/h2o/`.
  The run used the workspace `Multiwfn_noGUI`, returned 0, and produced
  `paths.pdb` (124 lines), `CPs.pdb` (6 lines), `mol.pdb` (5 lines),
  `CPprop.txt`, logs, and `aim_atoms_only.vesta` (579 lines).  VESTA was not
  launched during this smoke.

## 2026-06-10: README refresh and branch consolidation

- User asked to update the README, simplify the branch situation, and use
  `Stardust0831` identity for commits.
- Confirmed repository-local Git identity:
  `Stardust0831 <13862180016@163.com>`.
- Rewrote `README.md` to describe the maintained CLI: quick start,
  `multiwfn2vesta discover`, `aim-run`, `aim-pdb`, `aim-igmh`, explicit VESTA
  rendering caveat, validation command, smoke output, and documentation map.
- Pushed README update on the verified maintenance branch at commit `2c19cd8`.
- Fast-forwarded `main` from `8605928` to `2c19cd8`, so `main` now contains
  the maintained CLI, AIM runner, VESTA utilities, tests, docs, and README.
- Deleted the merged `vesta-nofocus-render` branch locally and remotely.
  Remote `origin` now tracks only `main`, with `origin/HEAD -> origin/main`.
- Follow-up README cleanup recorded the current repository status directly in
  the front page: maintained branch `main`, GitHub remote
  `Github:Stardust0831/multiwfn2vesta.git`, `origin/HEAD -> origin/main`, and
  repository-local identity `Stardust0831 <13862180016@163.com>`.

## 2026-06-10: Multiwfn/ABACUS/VESTA analysis matrix

- Continued the long-running research goal: identify Multiwfn analyses worth
  turning into VESTA workflows, with emphasis on inputs ABACUS can provide.
- Spawned two read-only sidecar agents.  One reviewed Multiwfn 2026.6.2 source
  and bundled scripts for VESTA-suitable cube/PDB products.  The other
  reviewed ABACUS Molden, `[Nval]`, cube outputs, and local Ag(111)+benzene
  smoke evidence.
- Checked ABACUS `origin/develop` on 2026-06-10.  Latest remote head observed
  was `707f09266842c3340a0d5f7a21d3224306aafd58`.  The Molden converter moved
  to `interfaces/Multiwfn_interface/molden.py` in commit
  `19511fd68bebb5fb44b5d7d89bd1d7262023df34`.
- Recorded the current ABACUS Molden rule: use the latest
  `interfaces/Multiwfn_interface/molden.py`; keep `[Nval]` enabled; treat the
  route as LCAO, `nspin=1/2`, Gamma/single-k only; and warn that NAO2GTO is an
  approximation for quantitative density-topology work.
- Added `docs/research/multiwfn_abacus_vesta_analysis_matrix.md`.  The matrix
  ranks direct ABACUS cube routes, ABACUS Molden wavefunction routes, Multiwfn
  AIM/IGMH/IRI/RDG/orbital/surface/basin/excited-state analyses, VESTA
  representations, and project implementation priorities.
- Added `docs/skills/abacus_multiwfn_vesta_analysis_skill.md` as a reusable
  checklist for deciding whether to use ABACUS direct cubes, ABACUS Molden plus
  Multiwfn, PDB pseudo-site overlays, dual-cube surface coloring, or atom
  scalar coloring.

## 2026-06-10: Molden sanity checker

- Started the first low-risk P0 implementation from the analysis matrix:
  `multiwfn2vesta molden-check`.
- Added `multiwfn2vesta.molden_check`, a no-GUI/no-Multiwfn text-level checker
  for Molden files.  Generic mode requires `[Atoms]`, `[GTO]`, and `[MO]`.
  ABACUS mode additionally requires `[Cell]` and `[Nval]`.
- Added the `molden-check` command and `check-molden` alias to the unified CLI,
  plus an interactive launcher entry.
- Documented the check in README, usage notes, and the ABACUS/Multiwfn/VESTA
  planning skill.
- Real ABACUS Ag(111)+benzene Molden smoke passed:
  `/mnt/g/work/multiwfn2vesta/smoke/abacus_server_artifacts_20260606/ag111_benzene/ag111_benzene_lcao_cont3_nval.molden`.
  Reported values: 60 atoms, 566 MO blocks, 3 `[Nval]` entries, 3 numeric
  `[Cell]` rows, `[Nval]` detail `Ag=19, C=4, H=1`, and `Result: OK`.

## 2026-06-10: Generic cube to VESTA CLI

- Implemented the first generic cube-to-VESTA workflow from the
  Multiwfn/ABACUS/VESTA analysis matrix: `multiwfn2vesta cube-vesta`.
- The workflow reads a scalar cube header, writes a `.vesta` file with
  `IMPORT_DENSITY 1`, optional `IMPORT_TEXTURE`, `SURFS 0 1 1`,
  `SECTS 0 0`, `ISURF`, and `TEX3P`, and writes a markdown recipe.
- It copies cube dependencies beside the generated `.vesta` by default, checks
  cube data count, rejects incompatible texture grids by default, and rejects
  zero-span texture values when `--tex-physical` needs percentage conversion.
- It creates a structure phase from the cube atom records.  `--structure auto`
  chooses `CRYSTAL` for origin-zero cubes whose atoms fall inside the cube
  cell, otherwise `MOLECULE`.
- Real H2O-HF smoke:
  `/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_cli_smoke_20260610/`.
  The output contains `h2o_hf_iri_cube.vesta`,
  `h2o_hf_iri_cube_vesta_recipe.md`, `h2o_hf_IRI2_surface.cub`, and
  `h2o_hf_IRI1_color.cub`.  The `.vesta` file uses `IMPORT_DENSITY`,
  `IMPORT_TEXTURE`, `SECTS 0 0`, `ISURF 1.0`, and percentage `TEX3P`.

## 2026-06-10: README and branch cleanup follow-up

- User requested another README refresh and branch cleanup because the branch
  state looked confusing.
- Checked the repository after `git fetch --prune` and
  `git ls-remote --heads origin`: the project has local `main`, `origin/main`,
  and `origin/HEAD -> origin/main`; the GitHub remote currently exposes only
  `refs/heads/main`.
- Confirmed repository-local commit identity is still
  `Stardust0831 <13862180016@163.com>`.
- README now documents the maintained single-branch status, unified CLI,
  executable discovery, Molden checker, generic cube-to-VESTA workflow,
  Multiwfn AIM runner, AIM PDB conversion, AIM+IGMH overlay workflow,
  rendering caveat, validation commands, smoke paths, and documentation map.
- Pre-commit validation passed: 73 no-GUI unit tests, `py_compile` for
  `cube_vesta.py` and `cli.py`, and `git diff --check`.
- A read-only pre-commit sub-agent review found one blocker: surface and
  texture cubes with the same basename but different directories could be
  copied into the output directory under one name.  Fixed this by reserving
  dependency filenames during copy and renaming only colliding later files,
  for example `foo_texture.cub`.

## 2026-06-10: Surface-band texture scaling for cube-vesta

- Continued the long-running Multiwfn/ABACUS/VESTA roadmap by improving the
  generic cube-to-VESTA workflow for mapped surfaces such as IRI, RDG, ESP,
  and IGMH.
- Added `--tex-range-source full-cube|surface-band` to `multiwfn2vesta
  cube-vesta`.  The default remains `full-cube` for compatibility.
- In `surface-band` mode, `--tex-physical MIN MAX` is converted to VESTA
  `TEX3P` percentages using texture values at grid points whose surface-cube
  values are close to the requested `--isosurface`.  `--surface-band` can set
  the half-width manually; otherwise a conservative automatic band is used.
- If the surface band has no non-degenerate texture range, the workflow falls
  back to the `--surface-nearest` nearest grid points and records this in the
  recipe.
- The generated recipe now records `tex_reference_source`,
  `tex_reference_range`, `tex_reference_sample_count`, optional
  `surface_band`, and whether nearest-grid fallback was used.
- Validation passed: focused `tests.test_cube_vesta` with 11 tests, full
  no-GUI regression with 75 tests, `py_compile`, and `git diff --check`.
- Real H2O-HF surface-band smoke:
  `/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_surface_band_smoke_20260610/`.
  It generated `h2o_hf_iri_surface_band_cube.vesta`, copied
  `h2o_hf_IRI2_surface.cub` and `h2o_hf_IRI1_color.cub`, and wrote
  `h2o_hf_iri_surface_band_cube_vesta_recipe.md`.
- The H2O-HF recipe records `tex_reference_source: surface-band`,
  `tex_reference_range: -0.04 to -0.0331239`,
  `tex_reference_sample_count: 29`, and automatic
  `surface_band: 0.059750500000000005`.
