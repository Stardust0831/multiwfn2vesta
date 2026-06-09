# Project Kanban

Updated: 2026-06-10

## Doing

- Turn the 2026-06-10 Multiwfn/ABACUS/VESTA research into the next
  maintainable features: RDG/IRI/IGMH command streams, real-system
  `abacus-molden` smoke coverage, and Multiwfn atom scalar parsers.
- Keep non-empty `LBLAT` generation out of maintained code until a GUI-saved
  VESTA diff proves the record syntax; the verified native route now uses
  `LABEL 1` plus site labels.
- Finish the full Ag(111)+benzene IGMH+AIM BCP visibility fix under the user's
  latest three-view constraint: one source `.vesta`, opened once by VESTA,
  then front/right/top images exported by command-line `-rotate_*` and
  `-flush`.  Persistent front/right/top `.vesta` files made by patching
  `SCENE` are compatibility/diagnostic material, not the main workflow.
- Find or build a real non-focus renderer.  Windows minimized/hidden/WSH
  launch routes and the current Linux wrapper are not yet usable.
- Continue improving non-disruptive rendering only after the maintained
  focus-stealing Windows route is documented as explicit/opt-in.

## Done

- Added `multiwfn2vesta cube-preset`, a thin analysis-preset layer over the
  maintained `cube-vesta` backend.  Current presets cover density-like scalar
  cubes, signed orbital/wavefunction/density-difference cubes, ELF/LOL cubes,
  IRI/RDG/NCI mapped surfaces, and ESP/MEP mapped density surfaces.
- Integrated `cube-preset` into the unified CLI, interactive menu, aliases
  `preset` and `analysis-cube`, and console script
  `multiwfn2vesta-cube-preset`.
- Synced README, usage docs, cube workflow skill notes, CLI skill notes,
  ABACUS/Multiwfn planning notes, the analysis matrix, root/project kanban,
  and worklogs with the cube preset workflow.
- Smoke-tested the preset wrapper under
  `/mnt/g/work/multiwfn2vesta/smoke/cube_preset_smoke_20260610/`, generating
  a signed orbital-style `.vesta` from the `orbital` alias and an IRI/RDG
  texture-mapped `.vesta` from the `rdg` alias without launching VESTA.
- Validated the cube preset layer with 28 focused unit tests, `py_compile`,
  CLI help/list checks, `git diff --check`, and a 108-test no-GUI regression
  before commit.
- Addressed read-only pre-commit review findings before commit: explicitly
  staged the new implementation/test files, updated package Python metadata
  from `>=3.6` to `>=3.7`, and made `--tex-percent` recipe output record
  explicit percentage scaling instead of implying physical texture scaling.
- Added `multiwfn2vesta abacus-molden`, a maintained wrapper around the
  latest ABACUS `interfaces/Multiwfn_interface/molden.py`.  It exports the
  converter from `origin/develop`, records source path/commit/SHA256, runs
  with an absolute `-o`, writes stdout/stderr logs and a markdown recipe, and
  validates successful output with `molden-check --abacus`.
- Hardened `abacus-molden` for real CLI use: the wrapper now preflights
  `numpy`, `scipy`, and `matplotlib` in the selected Python environment,
  supports `--python`, records missing-dependency errors in logs/recipe, treats
  missing output Molden files as failure even with `--no-check`, and writes
  partial logs/recipe on timeout instead of traceback.
- Validated the ABACUS Molden wrapper and README/CLI refresh with a 97-test
  no-GUI regression, `py_compile`, `git diff --check`, CLI help checks, and a
  git-export smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/abacus_molden_wrapper_smoke_20260610/`.
- Read-only pre-commit review checked the current diff; all findings were
  addressed before commit: dependency preflight, timeout handling, smoke
  evidence, test-count update, and CLI alias help consistency.
- Confirmed the branch layout for this README cleanup: project branch `main`
  tracks `origin/main`, repository-local identity is `Stardust0831
  <13862180016@163.com>`, and no extra feature branch is present locally.
- Added `multiwfn2vesta abacus-mulliken-color`, the first maintained
  ABACUS atom-scalar parser/glue workflow.  It parses ABACUS `out_mul 1`
  `mulliken.txt`, selects the last ionic step by default, supports exact
  `--step`, and maps `charge`, `magnetism`, `magnetism-x/y/z`, or
  `magnetism-norm` to VESTA `SITET` colors by one-based atom index.
- Confirmed ABACUS latest `origin/develop` Mulliken output shape from
  documentation, source, and test references: blocks begin with
  `--- Ionic Step N ---`, atom records use `Atom N is LABEL`, scalar totals
  use `total charge on atom N`, and spinful output adds
  `total magnetism on atom N`.  Multi-k output uses the same file structure
  after summing k-point contributions.
- Added tests for ABACUS Mulliken `nspin=1`, `nspin=2`, `nspin=4`, legacy
  documentation format, ionic-step selection, VESTA atom color patching, and
  selected-values CSV export.
- Validated the ABACUS Mulliken coloring workflow with focused parser/CLI
  tests, `py_compile`, and a real CLI smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/abacus_mulliken_color_smoke_20260610/`.
  The smoke colored Fe1 red and Fe2 blue from final-step magnetism
  `+4/-4` and wrote `values.csv`.
- Final pre-commit no-GUI regression for the README/Mulliken update passed:
  87 unit tests across Molden checking, ABACUS Mulliken parsing/coloring,
  cube-to-VESTA, unified CLI, AIM+IGMH, executable discovery, Multiwfn AIM,
  IRI cube handling, AIM VESTA conversion, and generic atom coloring.
- Read-only pre-commit review found and main thread fixed a strict-mode
  blocker: ABACUS Mulliken coloring now verifies that selected VESTA `STRUC`
  site indices exactly match Mulliken atom indices before patching colors, so
  a wrong `.vesta` file or section cannot silently color only a subset.
- Refreshed README for the current single-branch state and maintained CLI:
  after `git fetch --prune`, only local `main` and remote `origin/main` are
  present, with repository-local identity
  `Stardust0831 <13862180016@163.com>`.
- Added signed positive/negative isosurface support to
  `multiwfn2vesta cube-vesta`.  `--surface-mode signed --isosurface X` writes
  both `+abs(X)` and `-abs(X)` `ISURF` entries, defaults to yellow positive
  and blue negative surfaces, rejects zero magnitudes, and checks every level
  against the cube data range.
- Added focused signed-cube tests for the generated VESTA `ISURF` block,
  manifest `surface_mode`/`isosurface_levels`, zero-level rejection, and
  negative-level range validation.
- Updated README, usage docs, cube workflow skill notes, ABACUS/Multiwfn
  planning notes, and the analysis matrix so signed cube output is documented
  as implemented while Multiwfn command streams for generating those cubes
  remain future work.
- Validated the signed cube preset and README/docs refresh with 78 no-GUI
  regression tests, `py_compile`, `git diff --check`, and a real signed cube
  CLI smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_signed_smoke_20260610/`.
  The recipe records `surface_mode: signed` and isosurface levels
  `0.2, -0.2`.
- Checked branch/remote state for the user's README cleanup follow-up:
  `git fetch --prune` and `git ls-remote --heads origin` show only `main`,
  with `origin/HEAD -> origin/main`; there is no extra branch left to merge
  back.
- Confirmed repository-local Git identity remains `Stardust0831
  <13862180016@163.com>`.
- Validated the README/CLI/cube-to-VESTA changes before commit with 73
  no-GUI regression tests, `py_compile`, and `git diff --check`.
- Fixed the pre-commit review blocker where same-basename surface and texture
  cubes from different directories could overwrite each other in the generated
  VESTA dependency directory.
- Added `multiwfn2vesta cube-vesta`, the first generic ABACUS/Multiwfn cube
  to VESTA workflow.  It writes `IMPORT_DENSITY`, optional `IMPORT_TEXTURE`,
  `SECTS 0 0`, `ISURF`, percentage `TEX3P`, a cube-derived structure phase,
  copied cube dependencies, and a markdown recipe without launching VESTA.
- Real H2O-HF cube smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_cli_smoke_20260610/`; output
  includes `h2o_hf_iri_cube.vesta`, copied surface/texture cubes, and a recipe.
- Added surface-band texture scaling to `multiwfn2vesta cube-vesta`.
  `--tex-range-source surface-band` converts `--tex-physical` limits using
  texture values from grid points near the requested isosurface, records the
  reference range/sample count in the recipe, and falls back to nearest grid
  points when the band is empty or degenerate.
- Validated surface-band texture scaling with 75 no-GUI regression tests and a
  real H2O-HF IRI smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_surface_band_smoke_20260610/`.
  The recipe records `tex_reference_source: surface-band`, reference range
  `-0.04` to `-0.0331239`, and 29 sampled grid points.
- Added `multiwfn2vesta molden-check`, a no-GUI Molden sanity checker.
  Generic mode checks `[Atoms]`, `[GTO]`, and `[MO]`; ABACUS mode also
  requires `[Cell]` and `[Nval]` before Multiwfn wavefunction workflows.
- Real Ag(111)+benzene ABACUS Molden smoke passed with `--abacus`:
  60 atoms, 566 MO blocks, 3 `[Nval]` entries, 3 numeric `[Cell]` rows, and
  `[Nval]` detail `Ag=19, C=4, H=1`.
- Added the Multiwfn/ABACUS/VESTA analysis matrix under
  `docs/research/multiwfn_abacus_vesta_analysis_matrix.md`.  It ranks useful
  Multiwfn wavefunction/grid analyses by VESTA visualization value, ABACUS
  input feasibility, and project priority.
- Added `docs/skills/abacus_multiwfn_vesta_analysis_skill.md` as a reusable
  planning checklist for ABACUS direct-cube routes, latest ABACUS Molden
  generation, `[Nval]` validation, and VESTA representation choice.
- Confirmed ABACUS `develop` moved the Molden converter to
  `interfaces/Multiwfn_interface/molden.py` at commit `19511fd`; latest
  checked `origin/develop` is `707f092`.  The current converter writes
  `[Nval]` by default and restricts the Molden path to LCAO, `nspin=1/2`, and
  Gamma/single-k calculations.
- Refreshed the README repository-status section so the front page explicitly
  says `main` is the maintained branch, `origin` points to
  `Github:Stardust0831/multiwfn2vesta.git`, `origin/HEAD -> origin/main`, and
  commits use repository-local identity
  `Stardust0831 <13862180016@163.com>`.
- Updated the README so the repository front page now documents the maintained
  `multiwfn2vesta` CLI, executable discovery, wavefunction-to-AIM runner,
  AIM PDB conversion, AIM+IGMH overlay workflow, rendering caveats, validation,
  and documentation map.
- Consolidated the branch state: `main` was fast-forwarded to the verified
  `vesta-nofocus-render` work at commit `2c19cd8`, pushed to GitHub, and the
  merged `vesta-nofocus-render` branch was deleted locally and remotely.
- Confirmed commit identity is repository-local `Stardust0831
  <13862180016@163.com>`.
- Added Multiwfn/VESTA executable discovery to the maintained CLI.
  `multiwfn2vesta discover` reports selected and candidate paths from
  environment variables, workspace tools, and `PATH`.
- Added `multiwfn2vesta aim-run <wavefunction> <output_dir>`.  It accepts
  Molden/FCHK/WFN-style inputs, runs Multiwfn AIM in the output directory,
  writes the exact command stream and logs, and converts generated
  `paths.pdb`/`CPs.pdb` into `aim_atoms_only.vesta` by default.
- Real H2O noGUI smoke succeeded under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_aim_cli_smoke_20260610/h2o/`.
  It produced `paths.pdb`, `CPs.pdb`, `CPprop.txt`, `mol.pdb`, logs, and
  `aim_atoms_only.vesta` without launching VESTA.
- Validation completed for the Multiwfn/VESTA discovery and wavefunction AIM
  runner integration: focused no-GUI tests, `py_compile`, CLI help,
  `multiwfn2vesta discover`, real H2O smoke, and `git diff --check`.
- Pushed the Multiwfn/VESTA discovery and wavefunction AIM runner integration
  to GitHub branch `vesta-nofocus-render` at commit `ce0fecb`.
- Added an easier global/interactive CLI entry point.  The user can add only
  `/mnt/g/work/multiwfn2vesta/project/bin` to `PATH`, run `multiwfn2vesta`,
  choose maintained workflows interactively, or call scriptable subcommands
  such as `multiwfn2vesta aim-igmh ...` without manually setting
  `PYTHONPATH`.
- Added `multiwfn2vesta.cli`, `bin/multiwfn2vesta`, editable-install console
  scripts, no-GUI CLI tests, and skill documentation
  `docs/skills/multiwfn2vesta_cli_skill.md`.
- Ran a unified CLI dry smoke without VESTA rendering under
  `/mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/unified_cli_smoke_20260610/`.
- Closed the Ag(111)+benzene AIM+IGMH drawing experience into a reusable
  Python/CLI workflow: `multiwfn2vesta.aim_igmh_vesta`.  It patches AIM
  path/BCP styles with the maintained yellow `Xe` path and orange `Rn` BCP
  defaults, preserves coordinates and structure bonds, splits BCPs into the
  final phase by default, copies relative IGMH cube files beside the product,
  writes a markdown manifest, and calls the one-source/one-session VESTA
  three-view exporter only when explicitly requested.
- Added focused no-GUI tests for the reusable AIM+IGMH workflow in
  `tests/test_aim_igmh_vesta.py`.
- Added skill documentation for the closed-loop reusable workflow:
  `docs/skills/aim_igmh_vesta_skill.md`.
- Ran a non-rendered Ag(111)+benzene dry smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/reusable_cli_smoke_20260610/`.
  The output contains a styled `.vesta`, a recipe markdown file, and copied
  `dg_inter.cub`/`sl2r.cub`.
- Updated maintained AIM overlay styling so `Xe` bond-path sample spheres use
  radius `0.0600` Angstrom by default.
- Generated a non-rendered Ag(111)+benzene smoke check file with yellow `Xe`
  path style patched to radius `0.0600` Angstrom:
  `/mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/products/ag111_benzene_igmh_aim_paths_single_xe_yellow_bcp_splitphase_path006_periodic_overlay.vesta`.
- Verified the change with focused unit tests, `py_compile`, and
  `git diff --check`.
- Researched VESTA atom/site labels for BCP numbering and documented the
  current recommendation: use site labels plus VESTA label visibility for
  simple labels, or use post-render image annotation for robust publication
  numbering until non-empty `LBLAT` syntax is reverse-engineered.
- Implemented `--label-bcp-sites` in `multiwfn2vesta.vesta_aim_overlay_style`.
  It preserves coordinates, rewrites BCP labels across `STRUC`, `THERI`, and
  `SITET`, sets the BCP `SITET` label flag to `1`, and uses `LABEL 1` for
  site-name labels.
- Real-rendered BCP text diagnostics under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_text_label_experiment_20260610/`.
  `LABEL 1` displays `BCP1`/`BCP2`/`BCP3`; `LABEL 0` displays `Rn`.  Native
  labels work but can overlap for nearby BCPs.
- IRI color cube processing notes and skill were added in earlier work.
- AIM path/CP VESTA conversion and style patching were added in earlier work.
- Added experimental minimized Windows VESTA renderer:
  `scripts/render_vesta_nofocus.py`.
- Added `docs/vesta_nofocus_rendering.md` with the 2026-06-08 Ag(111)+benzene
  retest result and PowerShell quoting pitfall.
- Added `scripts/add_single_view_compass.py` for one VESTA-like lower-left
  compass after PNG export.
- Updated `docs/skills/vesta_camera_and_layers_skill.md` with the current
  `COMPS 0` plus post-render single-compass workflow.
- User confirmed the minimized Windows VESTA wrapper still steals focus; it is
  not a no-disruption renderer.
- Fixed the post-render compass arrowhead geometry so arrowheads no longer
  appear reversed.
- Reworked `scripts/vesta_three_views.py` so default `cli-rotate` mode starts
  from one `.vesta`, prepares at most one render input for `COMPS 0` and
  relative cube colocation, opens that input once in VESTA, and exports
  front/right/top PNGs by command-line `-rotate_*`, `-flush`, and
  `-export_img`.  The old `SCENE`-copy path is retained only as
  `--mode scene-copies`.
- Recorded AIM overlay style guidance: use one pseudo-element for path sample
  points and tune path/BCP radii before drawing AIM bonds.
- Added `multiwfn2vesta.vesta_aim_overlay_style` for post-processing
  multi-phase AIM overlays.  It keeps all path sample points, maps path samples
  to a single pseudo-element such as `Xe`, maps BCPs to a distinct
  pseudo-element such as `Rn`, clears AIM `SBOND`, and preserves global
  structure bonds by default.
- Real-rendered BCP visibility diagnostics with VESTA after explicit user
  request.  BCP-only front/right/top PNGs were generated under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_render_20260609/`,
  and a zoomed front diagnostic was generated under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_zoom_render_20260609/`.
  Visual inspection confirms three orange BCP points are displayed.
- Tested whether BCP visibility depends on VESTA atom naming or element
  symbols.  BCP-only controls using `N+CP000*_N`, `N+BCP*`, `Rn+CP*_N`,
  `Rn+RBCP*`, `Xe+CP*_N`, `C+CP*_N`, and `He+CP*_N` all rendered visible
  points.  The full-overlay BCP issue is therefore not explained by the
  `CP000*_N` label pattern or the tested element symbols.
- Added `--split-bcp-phase` to `multiwfn2vesta.vesta_aim_overlay_style`.  It
  keeps all AIM path samples, clears AIM-phase bonds, moves BCPs into a final
  dedicated phase, and is idempotent for already-split files.
- Real-rendered the final Ag(111)+benzene IGMH+AIM split-BCP three views under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_cli_rotate_split_bcp_final_20260609/`.
  The output contains one `*_render_input.vesta`, the relative cube files, and
  three PNGs; it does not contain three view-specific `.vesta` files.
- Verified the final PNGs are valid `6096 x 3052` images and BCPs are visible
  in all views by orange-pixel counts: front `478`, right `363`, top `138`.
  The top view uses `--extra-rotate top x -8` as a temporary camera tilt before
  export, then undoes it; no BCP/path coordinates are moved.

## Next

- Try a non-activating launcher path or isolate rendering in a different
  desktop/session before using VESTA automation while the user is active.
- Add tests for `scripts/vesta_three_views.py` once script-level tests are
  organized for project utilities.
- If continuing Linux VESTA, add missing GUI libraries inside the workspace
  rather than modifying system packages.
- If the user asks for fresh PNGs, either run an explicitly accepted
  focus-stealing VESTA CLI export or continue the Linux/local-library
  non-focus route first.
