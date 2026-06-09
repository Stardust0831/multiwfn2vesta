# Worklog

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
