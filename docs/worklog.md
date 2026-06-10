# Worklog

## 2026-06-10: README branch consolidation refresh at Becke tip

- User requested a README refresh, branch-state audit, possible merge-back to
  one branch, and git identity `Stardust0831`.
- Confirmed the maintained GitHub checkout is
  `/mnt/g/work/multiwfn2vesta/project`; the workspace-level
  `/mnt/g/work/multiwfn2vesta/.git` remains an empty metadata stub and is not
  used for project commits.
- Rechecked repository state after `git fetch --prune origin`: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `27065d0bf4b5f4096044065cd76a4eaa52735704` (`Add Becke weight cube
  preset`), and `git ls-remote --heads origin` exposes only
  `refs/heads/main`.
- Repository-local identity is `Stardust0831 <13862180016@163.com>`.
- No branch merge is needed in this pass because no extra local branch or
  remote feature branch exists; the closeout remains on maintained `main`.
- Local untracked probes `domain.cub` and `domain.pdb` remain uncommitted.

## 2026-06-10: Becke atomic and overlap weight cube preset

- Continued the long-running Multiwfn/ABACUS/VESTA analysis objective by
  selecting a source-backed, ABACUS LCAO Molden-compatible real-space grid
  increment.
- Rechecked local Multiwfn 2026.6.2 source evidence: main-function-5
  function `111` prompts for two atom indices before grid setup, computes
  Becke weight with `beckewei`, and exports `Becke.cub`; `I,J` computes
  Becke overlap weight and `I,0` computes Becke atomic weight.
- Added `cube-preset becke-weight` with aliases `becke`,
  `becke-overlap-weight`, `becke-atomic-weight`, and `beckewei`.  The preset
  uses a single positive `0.5` isosurface for the usual dimensionless `0..1`
  weight range.
- Added `grid-run --function becke --becke-atoms I J`, including atom-index
  validation, command-stream generation, recipe fields, CLI help, and fake
  Multiwfn `Becke.cub` tests.
- Updated README, usage docs, cube/grid/CLI/ABACUS skills, research matrix,
  and kanban.  Local untracked probes `domain.cub` and `domain.pdb` remain
  uncommitted.
- Focused validation passed before full regression: `py_compile` for the
  changed modules/tests, 75 focused tests across `tests.test_cube_preset` and
  `tests.test_multiwfn_grid`, and `bin/multiwfn2vesta grid-run --help`.
- Full validation passed before commit: root docs checksum mirror dry-run,
  full 291-test no-GUI regression, `cube-preset --list-presets`,
  `grid-run --list-functions`, `grid-run --help`,
  `bin/multiwfn2vesta --help`, and `git diff --check`.  Read-only review
  found no High blocker and confirmed EDR/RDG/IRI/vdW routes are not broken;
  `domain.cub` and `domain.pdb` remain untracked local probes.

## 2026-06-10: README branch consolidation refresh at EDR tip

- User requested a README refresh, branch-state audit, possible merge-back to
  one branch, and git identity `Stardust0831`.
- Confirmed the maintained GitHub checkout is
  `/mnt/g/work/multiwfn2vesta/project`; the workspace-level
  `/mnt/g/work/multiwfn2vesta/.git` is an empty metadata directory and is not
  used for project commits.
- Rechecked repository state after `git fetch --prune origin`: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `ef8d498bc4931bb7a03f828d43000da3c8efafc5` (`Add EDR grid cube presets`),
  and `git ls-remote --heads origin` exposes only `refs/heads/main`.
- Repository-local identity is `Stardust0831 <13862180016@163.com>`.
- No branch merge is needed in this pass because no extra local branch or
  remote feature branch exists; the closeout remains on maintained `main`.
- Local untracked probes `domain.cub` and `domain.pdb` remain uncommitted.

## 2026-06-10: EDR and orbital-overlap distance cube presets

- User requested a README refresh, branch-state audit, possible one-branch
  closeout, and continued use of the `Stardust0831` git identity while an
  automatic continuation had started another Multiwfn grid-analysis
  increment.
- Rechecked repository state: local `main`, `origin/main`, and
  `origin/HEAD` were aligned at
  `6de6b017d8fa8b66cde24731ca5403081201a0b4` (`Add standalone vdW potential
  cube preset`); `git ls-remote --heads origin` exposed only
  `refs/heads/main`; no extra local or remote branch needed merging.
- Added `cube-preset electron-delocalization-range` for Multiwfn function
  `20` `EDR.cub`, with aliases including `edr`, and a single positive
  `0.05` isosurface default.
- Added `cube-preset orbital-overlap-distance` for Multiwfn function `21`
  `EDRDmax.cub`, with aliases including `edrdmax` and `d(r)`, and a single
  positive `0.05` isosurface default.
- Updated `grid-run` with function-table entries for functions `20` and
  `21`; function `20` requires `--edr-length D_BOHR`, and function `21` uses
  Multiwfn's default exponent set `20, 2.50, 1.50` unless
  `--edr-exponents COUNT START INCREMENT` is supplied.
- Rechecked local Multiwfn 2026.6.2 source evidence: `function.f90`
  prompts function `20` for length scale `d` in Bohr and function `21` for
  either default or manual EDR exponent parameters; `0123dim.f90` exports
  `EDR.cub` and `EDRDmax.cub`; neither function resets the global
  main-function-5 `sur_value=0.05`.
- Added focused tests for preset listing, alias resolution, command streams,
  EDR parameter validation, fake Multiwfn `EDR.cub`/`EDRDmax.cub` runs,
  recipe fields, and VESTA manifest defaults.
- Updated README, usage docs, CLI/cube/grid/ABACUS skills, the analysis
  matrix, and kanban.  The README branch audit now records that `main` and
  `origin/main` are aligned at `6de6b017...` before this closeout and that no
  branch merge-back is needed.
- Local untracked probes `domain.cub` and `domain.pdb` remain uncommitted.

## 2026-06-10: Standalone vdW potential cube display preset

- User requested a README refresh, branch-state audit, possible one-branch
  closeout, and continued use of the `Stardust0831` git identity while the
  active vdW potential increment was in progress.
- Rechecked repository state before the closeout: local `main`,
  `origin/main`, and `origin/HEAD` were aligned at
  `fae7ac12d9a6d1fadbeda7a60c484752a643c23f` (`Add promolecular delta-g
  cube preset`); the GitHub SSH remote is
  `Github:Stardust0831/multiwfn2vesta.git`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`; no extra local or remote feature
  branch needed merging.
- Added `cube-preset vdw-potential` for standalone Multiwfn `vdWpot.cub`
  from main-function-5 function `25`.  It writes signed VESTA isosurfaces at
  `+/-1.0` kcal/mol.
- Updated `grid-run --function vdw-potential` and aliases `vdw`, `vdwpot`,
  and `van-der-waals-potential` so generated `vdWpot.cub` products route to
  `cube-preset vdw-potential` instead of generic `signed`.
- Preserved the mapped route: when `--surface-cube` is supplied,
  `grid-run --function vdw-potential` still uses `cube-preset vdw-map` so the
  generated vdW potential cube colors an existing density/surface cube.
- Rechecked local Multiwfn 2026.6.2 source evidence: `function.f90` lists
  function `25` as van der Waals potential and calls `vdwpotfunc`;
  `vdwpotfunc` source comments identify the function as UFF vdW potential in
  kcal/mol; `0123dim.f90` exports `vdWpot.cub` and sets `sur_value=1.0`.
- Added focused tests for preset listing, `vdwpot` alias resolution, signed
  `ISURF` output, manifest notes, function alias resolution, a fake Multiwfn
  standalone `grid-run --function vdw` run, and a fake `--surface-cube` run
  confirming `vdw-map` remains the mapped preset.
- Updated README, usage docs, CLI/cube/grid/ABACUS skills, and the analysis
  matrix so standalone `vdw-potential` and mapped `vdw-map` are documented as
  separate routes.
- Validation passed before commit/push: focused `py_compile`, 66 focused
  tests across `tests.test_cube_preset` and `tests.test_multiwfn_grid`, full
  282-test no-GUI regression, `bin/multiwfn2vesta cube-preset
  --list-presets`, `bin/multiwfn2vesta grid-run --list-functions`,
  `bin/multiwfn2vesta --help`, root docs mirror checksum check, and
  `git diff --check`.
- Read-only review found no High/Medium blocker and confirmed the default
  standalone route and the `--surface-cube` mapped `vdw-map` route remain
  separate; `domain.cub` and `domain.pdb` remain untracked local probes.

## 2026-06-10: Promolecular Delta-g cube display preset

- Added `cube-preset promolecular-delta-g` for Multiwfn `Delta_g.cub` from
  main-function-5 function `22` (`Delta-g (promolecular approximation)`).
  It writes a single positive VESTA isosurface with default value `0.05`.
- Updated `grid-run --function delta-g` and aliases `deltag`, `delta_g`,
  `promolecular-deltag`, and `delta-g-promol` so generated `Delta_g.cub`
  products route to the dedicated preset instead of generic `density`.
- Rechecked local Multiwfn 2026.6.2 source evidence: `function.f90` lists
  function `22` as promolecular Delta-g and calls `delta_g_promol`;
  `0123dim.f90` exports `Delta_g.cub`; `define.f90` initializes the global
  main-function-5 `sur_value=0.05`, and function `22` does not reset it.
- Preserved the IGM/IGMH fragment route: `dg_inter.cub` plus `sl2r.cub`
  still belongs to `cube-preset igmh`/`igm` and the automated
  `igmh-run`/`igm-run`/`migm-run` workflows.
- Added focused tests for preset listing, single-positive `ISURF` output,
  manifest notes, alias resolution, and a fake Multiwfn
  `grid-run --function delta-g` run that verifies the command stream,
  `Delta_g.cub` handling, recipe, and VESTA manifest.
- Validation passed: focused `py_compile`, 63 focused tests across
  `tests.test_cube_preset` and `tests.test_multiwfn_grid`, the full 279-test
  no-GUI regression, `bin/multiwfn2vesta cube-preset --list-presets`,
  `bin/multiwfn2vesta grid-run --list-functions`,
  `bin/multiwfn2vesta --help`, and `git diff --check`.
- Read-only review found no source/test blocker: IGM/IGMH
  `dg_inter.cub + sl2r.cub` routes and IRI/RDG texture routes are not
  overwritten, and the new aliases do not collide with existing routes.

## 2026-06-10: README branch closeout after local information entropy preset

- User requested another README refresh, branch-state audit, possible
  one-branch merge-back, and git identity `Stardust0831`.
- Rechecked the repository after `git fetch --prune origin`: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `764382c01698111f9d8b41932759a480233a272b` (`Add local information entropy
  cube preset`), and `git ls-remote --heads origin` exposes only
  `refs/heads/main`.
- Repository-local identity is `Stardust0831 <13862180016@163.com>`.
- No merge-back is needed in this pass because there is no extra local or
  remote feature branch to consolidate.
- README now records the current branch-audit baseline and explicitly notes
  that local untracked probes such as `domain.cub` and `domain.pdb` are not
  part of the maintained branch state unless promoted into documented
  fixtures.

## 2026-06-10: Local information entropy cube display preset

- Added `cube-preset local-information-entropy` for Multiwfn
  `infoentro.cub` from main-function-5 function `11`.  It writes signed
  positive/negative VESTA isosurfaces with default magnitude `0.05`.
- Updated `grid-run --function local-information-entropy` and aliases
  `information-entropy`, `infoentro`, `local-info-entropy`, and
  `local-shannon-entropy` so generated `infoentro.cub` products route to the
  dedicated preset instead of a generic scalar preset.
- Rechecked local Multiwfn 2026.6.2 source evidence: `function.f90` lists
  function `11` as local information entropy and evaluates
  `-rho/N*ln(rho/N)`; `0123dim.f90` exports `infoentro.cub` and does not
  reset `sur_value`, so the maintained default follows the global
  main-function-5 `sur_value=0.05`.
- At that time, Fermi hole/source function and EDR/D(r) cube routes were
  deferred because they needed reference points or extra prompt parameters;
  EDR/D(r) was later implemented as the dedicated 2026-06-10 EDR and
  orbital-overlap distance increment above, while reference-point functions
  remain deferred.
- Added focused tests for preset listing, signed `ISURF` defaults, manifest
  notes, function alias resolution, and a fake Multiwfn
  `grid-run --function information-entropy` run that verifies the recipe and
  VESTA manifest use `local-information-entropy`.
- Validation passed: focused `py_compile`, 61 focused tests across
  `tests.test_cube_preset` and `tests.test_multiwfn_grid`, the full 277-test
  no-GUI regression, `bin/multiwfn2vesta cube-preset --list-presets`,
  `bin/multiwfn2vesta grid-run --list-functions`,
  `bin/multiwfn2vesta --help`, and `git diff --check`.

## 2026-06-10: Standalone IRI scalar cube display preset

- Added `cube-preset iri-scalar` for standalone Multiwfn `IRI.cub` from
  main-function-5 function `24`.  It writes a single positive VESTA
  isosurface using Multiwfn's source default `sur_value=1D0`.
- Updated `grid-run --function iri` and alias `interaction-region-indicator`
  so generated `IRI.cub` products route to `cube-preset iri-scalar` instead
  of the generic density preset.
- Preserved the existing `cube-preset iri` / `rdg` behavior for two-cube
  IRI/RDG/NCI mapped surfaces colored by sign(lambda2)rho-like texture cubes.
- Added focused tests for preset listing, standalone `IRI.cub` single-surface
  output, texture-route separation, function alias resolution, and a fake
  Multiwfn `grid-run --function iri` run that verifies the recipe and VESTA
  manifest use `iri-scalar`.
- Validation passed: focused `py_compile`, 59 focused tests across
  `tests.test_cube_preset` and `tests.test_multiwfn_grid`, the full 275-test
  no-GUI regression, `bin/multiwfn2vesta cube-preset --list-presets`,
  `bin/multiwfn2vesta grid-run --list-functions`,
  `bin/multiwfn2vesta --help`, and `git diff --check`.

## 2026-06-10: Gradient-norm cube display preset

- Added `cube-preset gradient-norm` for Multiwfn `gradient.cub` from
  main-function-5 function `2` (`Gradient norm of rho`).  It writes a single
  positive VESTA isosurface because the field is nonnegative.
- Updated `grid-run --function gradient` and aliases `rho-gradient` /
  `grad-rho` so generated `gradient.cub` products route to
  `cube-preset gradient-norm` instead of the generic density preset.
- Rechecked local Multiwfn 2026.6.2 source evidence: `0123dim.f90` exports
  `gradient.cub` for function `2`, while `define.f90` initializes the global
  `sur_value=0.05D0`; Multiwfn does not reset a function-specific value for
  gradient norm.  The maintained default is therefore `0.05`, with
  system-specific tuning expected.
- Added focused tests for preset listing, alias resolution, generated
  single-positive `ISURF`, manifest notes, and `grid-run` function-to-preset
  mapping.
- Added an integration-style fake Multiwfn grid-run test for
  `--function gradient`, verifying that `gradient.cub` becomes
  `case_gradient.cub`, the recipe records `auto_vesta_preset:
  gradient-norm`, and the generated VESTA manifest resolves to the
  `gradient-norm` preset.
- Validation passed: focused `py_compile`, 57 focused tests across
  `tests.test_cube_preset` and `tests.test_multiwfn_grid`, the full 273-test
  no-GUI regression, `bin/multiwfn2vesta cube-preset --list-presets`,
  `bin/multiwfn2vesta grid-run --list-functions`, `git diff --check`, root
  docs mirror check, and read-only subagent review with no blockers.

## 2026-06-10: README branch audit at spin-density tip

- Rechecked the branch state for the user's README/branch-convergence request
  after the spin-density cube arithmetic increment.  Local `main`,
  `origin/main`, and `origin/HEAD` all point at
  `1a8bbc63cc785ec07b4b177078909971b8ac127b`; the SSH remote
  `Github:Stardust0831/multiwfn2vesta.git` exposes only `refs/heads/main`.
- Confirmed the repository-local commit identity remains
  `Stardust0831 <13862180016@163.com>`.
- Refreshed README repository-status wording so the current single-branch
  state and branch-audit baseline reflect the latest pushed feature tip.
- No branch merge was needed in this pass.  Local probe files `domain.cub` and
  `domain.pdb` remain untracked and uncommitted.
- Validation for the docs-only refresh passed: root docs mirror clean,
  `git diff --check`, `bin/multiwfn2vesta --help`, and read-only subagent
  review with no blockers.

## 2026-06-10: Spin-density cube arithmetic

- Added a named `cube-arith --operation spin-density` shortcut for compatible
  alpha/beta or spin-up/spin-down density cubes.  The operation writes
  alpha/spin-up density minus beta/spin-down density through the existing
  cube arithmetic backend.
- Preserved the generic `density-difference` behavior.  `spin-density` shares
  the same `plus - minus` arithmetic shape, but has its own semantic
  operation name and default display route.
- Updated `--preset auto` so `spin-density` products go through
  `cube-preset spin-density`, giving the maintained red/blue signed
  isosurfaces and Multiwfn `spindensity.cub` default magnitude `0.02`.
- Extended the unified CLI help and interactive launcher so menu item `11`
  can build spin-density arguments with alpha/spin-up and beta/spin-down cube
  prompts.
- Added tests for operation term construction, VESTA preset selection,
  generated `ISURF` colors/defaults, CLI command execution, and interactive
  argument construction.  Focused validation passed for
  `tests.test_cube_arith` and `tests.test_cli`.
- Updated README, Chinese usage docs, cube arithmetic skill, unified CLI
  skill, cube-to-VESTA skill, ABACUS analysis skill, and the analysis matrix.

## 2026-06-10: README branch convergence refresh

- Rechecked the branch state for the user's README/branch-convergence request.
  Local `main`, `origin/main`, and `origin/HEAD` all point at
  `77c134e2d7cd844e6cc9c4dce59f316a90700192`; the SSH remote
  `Github:Stardust0831/multiwfn2vesta.git` exposes only `refs/heads/main`.
- Confirmed the repository-local commit identity is
  `Stardust0831 <13862180016@163.com>`.
- Refreshed README repository-status wording so the current single-branch
  state is explicit and the prior pre-increment branch-audit hash no longer
  reads like a pending final commit claim.
- Left local probe files `domain.cub` and `domain.pdb` untracked and
  uncommitted.

## 2026-06-10: Grid-function display presets

- Continued the Multiwfn/ABACUS/VESTA analysis-expansion sweep by tightening
  display defaults for Multiwfn main-function-5 scalar cubes that ABACUS can
  feed through the maintained LCAO Molden route.
- Added dedicated `cube-preset` entries for `spin-density`, `laplacian`,
  `hamiltonian-ked`, `lagrangian-ked`, `orbital-density`, `rdg-scalar`, and
  `promolecular-rdg`.
- Rechecked local Multiwfn `0123dim.f90`.  Source defaults used directly:
  `spindensity.cub` `sur_value=0.02`, `orbdens.cub` `0.005`, `RDG.cub`
  `0.5`, and `RDGprodens.cub` `0.4`.  Laplacian, K(r), and G(r) still need
  system-specific isosurface tuning, with conservative maintained defaults.
- Updated `grid-run` so function aliases now auto-select the specific display
  presets for `laplacian`, `spin-density`, `hamiltonian-ked`,
  `lagrangian-ked`, `orbital-density`, `rdg`, and `promolecular-rdg`.
- Preserved the existing `cube-preset rdg` alias for the two-cube
  `iri`/NCI mapped-surface workflow.  Standalone `RDG.cub` display uses the
  new `rdg-scalar`/`rdg-cube` names to avoid breaking that route.
- Added focused tests for preset listing, signed/single `ISURF` behavior,
  manifest notes, Multiwfn-source default isosurfaces, and `grid-run`
  function-to-preset resolution.
- Focused validation passed: 30 `tests.test_cube_preset` tests and 25
  `tests.test_multiwfn_grid` tests.
- Final validation passed: `py_compile`, 55 focused tests across
  `tests.test_cube_preset` and `tests.test_multiwfn_grid`, full 268-test
  no-GUI regression, `bin/multiwfn2vesta --help`,
  `bin/multiwfn2vesta cube-preset --list-presets`,
  `bin/multiwfn2vesta grid-run --list-functions`, `git diff --check`, and a
  targeted documentation scan for stale spin-density/orbital-density/RDG
  preset defaults.

## 2026-06-10: ABACUS direct cube display presets

- Continued the Multiwfn/ABACUS/VESTA analysis-expansion sweep by improving
  the direct ABACUS cube route, where no additional Multiwfn wavefunction
  analysis is needed.
- Added `cube-preset potential` for direct `out_pot`/potential cube signed
  positive/negative isosurfaces.  This is distinct from `cube-preset esp`,
  which remains the density/surface cube plus potential texture workflow.
- Added `cube-preset partial-charge` for ABACUS `calculation get_pchg` /
  `out_pchg` partial charge, band-density, or state-density cubes.
- Added `cube-preset wavefunction-norm` for nonnegative ABACUS
  `out_wfc_norm` wavefunction norm/magnitude cubes; signed real/imaginary
  `out_wfc_re_im` cubes still use `cube-preset signed` or alias `orbital`.
- Added focused tests for preset listing, aliases, signed/single surface
  behavior, and manifest notes.
- Validation passed: `py_compile`, 23 focused `cube-preset` tests,
  `cube-preset --list-presets`, `bin/multiwfn2vesta --help`,
  `git diff --check`, and the full 261-test no-GUI regression.

## 2026-06-10: aIGM/amIGM trajectory-average runner

- Continued the long-running Multiwfn/ABACUS/VESTA analysis-expansion goal by
  turning the pending aIGM/amIGM feasibility note into a maintained runner.
- Re-read local Multiwfn `visweak.f90`.  Source evidence shows aIGM/amIGM are
  trajectory-average weak-interaction menu entries (`12` and `-12`), not
  ordinary single-wavefunction IGMH variants.  Post-processing option `3`
  exports `avgdg_inter.cub` and `avgsl2r.cub`; option `4` exports
  `avgRDG.cub`; option `5` exports `thermflu.cub`; option `2` exports
  scatter `output.txt`.
- Added `multiwfn2vesta aigm-run` and `multiwfn2vesta amigm-run`, backed by
  `src/multiwfn2vesta/multiwfn_aigm.py`.  The default stream enters Multiwfn
  main function `20`, selects aIGM/amIGM, sends two or more fragments, sends
  either an explicit frame range or an empty response for all frames, selects
  the grid, exports averaged cubes, and then calls `cube-preset aigm` unless
  `--no-vesta` is used.
- Optional flags preserve additional Multiwfn products:
  `--export-rdg` for `avgRDG.cub`, `--export-tfi` for `thermflu.cub`,
  `--export-scatter` for `output.txt`, and `--tfi-vesta` for an extra
  `cube-preset aigm-tfi` VESTA file.
- Source cross-check note: post-processing menu option `5` calls
  `calcexport_TFI` and writes `thermflu.cub`; the hidden option `6` branch in
  the same subroutine writes `TFI-aIGM.cub`/`TFI-amIGM.cub`, but the maintained
  runner deliberately does not use that hidden menu branch.
- Read-only review found a real periodic-grid risk: Multiwfn's PBC setgrid
  option `4` reads a spacing value rather than `NX,NY,NZ`.  Added
  `--periodic`/`--nonperiodic`, lightweight `Lattice=`/`pbc=`/`CRYST1`
  trajectory detection, and a guard that rejects `--grid-mode points` for
  periodic aIGM/amIGM input.  Periodic trajectories should use
  `--grid-mode spacing --grid-spacing VALUE` or `--grid-mode pbc-cell`.
- Integrated the runner into the unified CLI, interactive chooser item `18`,
  aliases `multiwfn-aigm`, `multiwfn-aigm-run`, `averaged-igm-run`,
  `multiwfn-amigm`, `multiwfn-amigm-run`, and `averaged-migm-run`, plus
  package console scripts.
- Added focused tests in `tests/test_multiwfn_aigm.py` plus CLI coverage for
  help text, direct dispatch, alias dispatch, and interactive argument
  building.  The documented boundary is explicit: ABACUS Molden workflows
  still use `igmh-run`/`igm-run`/`migm-run`; aIGM/amIGM is for trajectories.
- Validation passed: `py_compile`, 83 focused aIGM/CLI/preset tests,
  `bin/multiwfn2vesta --help`, `aigm-run --help`, `amigm-run --help`,
  `cube-preset --list-presets`, `git diff --check`, and the full 258-test
  no-GUI regression.  Read-only review findings were addressed before
  commit; local `domain.cub` and `domain.pdb` remain unstaged probe files.

## 2026-06-10: README branch status refresh at aIGM/amIGM closeout

- User asked to update README again, noted that the branch state still looked
  unusual, suggested merging back to one branch if useful, and requested Git
  identity `Stardust0831`.
- Rechecked repository state without destructive operations: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `0fd0517e35c4ae308b276417ee253a81138e7840`
  (`Refresh README branch closeout status`) before the aIGM/amIGM runner
  closeout.
- Rechecked remote heads: `git ls-remote --heads origin` exposes only
  `refs/heads/main`, so no branch merge-back is needed in this pass.
- Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- Refreshed README Repository Status so the branch audit records the current
  closeout tip and the fact that the aIGM/amIGM runner increment is kept on
  the same maintained `main` branch.
- Synced `project/docs/` to the root `docs/` mirror after final documentation
  edits and verified the mirror with `rsync -ani --checksum docs/ ../docs/`.

## 2026-06-10: README branch status refresh at Fukui closeout tip

- User asked to update README again, noted that the branch state still looked
  unusual, suggested merging back to one branch if useful, and requested Git
  identity `Stardust0831`.
- Rechecked repository state without destructive operations: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `f8e1a4815d2f32b8562f74824e7e0253c6dc6b8e`
  (`Close Fukui runner branch status`).
- Rechecked remote heads: `git ls-remote --heads origin` exposes only
  `refs/heads/main`, so no branch merge-back is needed in this pass.
- Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- Refreshed README Repository Status so the branch audit records the current
  closeout tip while still identifying `43e00d2` as the latest feature commit.

## 2026-06-10: Fukui/dual descriptor runner and README branch closeout

- User asked to update the README, noted that the branch state looked unusual,
  and requested that commits use identity `Stardust0831`.
- Rechecked repository state before editing: local `main`, `origin/main`, and
  `origin/HEAD` were aligned at
  `e92d98ad631b35ac27eebd9ce6f7da97a7ec5689`
  (`Add Multiwfn basin cube presets`), and `git ls-remote --heads origin`
  exposed only `refs/heads/main`.  No merge-back branch was present.
- Confirmed repository-local identity:
  `Stardust0831 <13862180016@163.com>`.
- Added `multiwfn2vesta fukui-run`, backed by
  `src/multiwfn2vesta/multiwfn_fukui.py`.  The command composes existing
  maintained layers instead of duplicating them: neutral density is generated
  first through `grid-run --function density`, charged-state densities reuse
  the neutral cube as `--grid-mode cube --grid-cube <neutral_density.cub>`,
  and Fukui/dual maps are built through `cube-arith`.
- Supported operations are `fukui-plus`, `fukui-minus`, `dual-descriptor`, and
  `all`.  The runner requires only the charged states needed by the selected
  operations and writes `multiwfn_fukui_recipe.md` with caveats and child run
  paths.
- Integrated the command into the unified CLI, interactive chooser item `17`,
  aliases `multiwfn-fukui`, `multiwfn-fukui-run`, and
  `dual-descriptor-run`, plus package console scripts.
- Added focused tests in `tests/test_multiwfn_fukui.py` and CLI coverage for
  help text, command dispatch, alias dispatch, and interactive argument
  building.
- Updated README, usage notes, research matrix, unified CLI skill, and added
  `docs/skills/multiwfn_fukui_run_skill.md`.  The documented scope is finite
  or otherwise carefully reviewed charged-state systems; existing compatible
  density cubes should still use `cube-arith` directly.
- Read-only review found no blocker.  It noted one P2 residual risk: if
  VESTA preset generation failed after cube arithmetic had written the output
  cube, the top-level Fukui recipe could still say the operation was not
  generated.  Fixed this by retrying the arithmetic child in cube-only mode
  and recording that cube output while still returning a nonzero code for the
  VESTA failure.
- Validation passed after the review fix: `py_compile` for the new runner,
  CLI, and tests; 88 focused tests covering `multiwfn_fukui`, unified CLI,
  `cube_arith`, and `multiwfn_grid`; `bin/multiwfn2vesta --help`;
  `bin/multiwfn2vesta fukui-run --help`; `bin/multiwfn2vesta cube-preset
  --list-presets`; `git diff --check`; and the full 242-test no-GUI
  regression.
- Pushed commit `43e00d2218699574d3644c51dc0bd1249f60d0da`
  (`Add Multiwfn Fukui runner`) to `origin/main`.  Post-push branch checks
  found local `main`, `origin/main`, and `origin/HEAD` aligned at that commit;
  `git ls-remote --heads origin` still exposed only `refs/heads/main`.

## 2026-06-10: Basin cube display presets

- Continued the long-running Multiwfn/ABACUS/VESTA analysis-expansion goal by
  addressing the next research-matrix gap: basin analysis visualization.
- Re-read local Multiwfn `basin.f90` evidence.  Basin analysis option `-5`
  exports all-index `basin.cub`, individual binary `basinNNNN.cub`,
  selected-function `basinsel.cub`, and signed mono-/disynaptic
  `basinsyn.cub`.  The source recommends isovalue `0.5` for individual
  binary basin cube visualization.
- Added `cube-preset basin` for individual binary `basinNNNN.cub` files and
  `cube-preset basin-type` for `basinsyn.cub`.  This deliberately stops at
  the display layer; a full basin-generation runner remains deferred because
  generation depends on real-space function choice, grid source, and
  clustering choices.
- Added a guard that rejects `cube-preset basin basin.cub ...`, because
  Multiwfn's all-index `basin.cub` is not a binary basin mask.
- Validation passed: `py_compile`, 20 focused `cube-preset` tests,
  `cube-preset --list-presets`, `git diff --check`, and the full 233-test
  no-GUI regression.

## 2026-06-10: README branch refresh after domain runner

- User asked to update README, noted that the branch state looked unusual,
  suggested consolidating back to one branch if useful, and requested Git
  identity `Stardust0831`.
- Rechecked `/mnt/g/work/multiwfn2vesta/project` after
  `git fetch --prune origin`: local `main`, `origin/main`, and `origin/HEAD`
  are aligned at
  `da7d4b759c663d7a1b53ec8cb71e5d96db28d68d`
  (`Close README branch refresh board`).
- Rechecked remote heads with `git ls-remote --heads origin`: the remote
  exposes only `refs/heads/main`, also at `da7d4b7`, so no branch merge-back
  is needed in this pass.
- Confirmed repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- Refreshed README Repository Status while closing the in-progress
  `domain-run` feature increment on `main`.
- After the domain-run feature push, rechecked local `main`, `origin/main`,
  and `origin/HEAD` at
  `73018ab1d8bca119d74cf9d51a39b244242bbc5f`
  (`Add Multiwfn domain runner`).  `git ls-remote --heads origin` still
  exposes only `refs/heads/main`, so the repository remains consolidated on a
  single maintained branch.

## 2026-06-10: Multiwfn domain analysis runner from cube data

- Continued the long-running Multiwfn/ABACUS/VESTA analysis-expansion goal by
  turning the confirmed Multiwfn `200 -> 14` domain-analysis prompt stream
  into a maintained cube post-processing runner.
- Added `multiwfn2vesta domain-run`, backed by
  `src/multiwfn2vesta/multiwfn_domain.py`.  The default stream enters
  Multiwfn main function `200`, subfunction `14`, uses menu option `3` to set
  a `<`/`>` domain criterion, sends `-1` to yield domains from current grid
  data in memory, then exports `domain.cub` and `domain.pdb` with menu
  options `10` and `11`.
- Added `cube-preset domain` plus aliases `domain-cube`, `domain-analysis`,
  and `binary-domain`; the preset uses a single isosurface at `0.5` because
  Multiwfn writes binary `domain.cub` values, `1` inside the selected domain
  and `0` outside.
- Integrated `domain-run` into the unified CLI, aliases `multiwfn-domain`,
  `multiwfn-domain-run`, and `cube-domain`, the interactive chooser, and
  package console scripts.
- Added focused tests in `tests/test_multiwfn_domain.py` plus CLI/preset
  coverage.  Focused validation passed:
  `PYTHONPATH=src python3 -m unittest tests.test_multiwfn_domain
  tests.test_cube_preset tests.test_cli` (67 tests).  Full no-GUI regression
  passed with `PYTHONPATH=src python3 -m unittest discover -s tests`
  (230 tests).
- Real H2O density-cube noGUI smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_domain_run_smoke_20260610/h2o_density/`:
  `domain-run --criterion '<0.5' --domain-index 1 --stem h2o_density
  --timeout 300` generated raw `domain.cub`/`domain.pdb`, processed
  `h2o_density_domain.cub`/`h2o_density_domain.pdb`, and
  `h2o_density_domain_cube.vesta`.

## 2026-06-10: README branch refresh at STM runner tip

- User asked to update README again, noted that the branch state looked
  unusual, suggested merging back to one branch if useful, and requested Git
  identity `Stardust0831`.
- Rechecked `/mnt/g/work/multiwfn2vesta/project` after
  `git fetch --prune origin`: local `main`, `origin/main`, and `origin/HEAD`
  are aligned at
  `fdf85863ccb01c5783ce912163f1ec4a34060dd7`
  (`Add Multiwfn STM runner`).
- Rechecked remote heads with `git ls-remote --heads origin`: the remote
  exposes only `refs/heads/main`, also at `fdf8586`, so no branch merge-back
  is needed in this pass.
- Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- Refreshed `README.md` Repository Status so the branch-audit commit and
  remote-head wording match the current STM/LDOS runner tip.
- Left untracked `domain.cub` and `domain.pdb` untouched as local
  domain-analysis probe artifacts; they are not part of this README cleanup.
- Committed and pushed the README/docs refresh on `main` as `1493c80`
  (`Refresh README branch status at STM tip`).

## 2026-06-10: Multiwfn STM/LDOS runner

- Continued the long-running Multiwfn/ABACUS/VESTA analysis-expansion goal by
  adding a maintained STM/LDOS cube route after source-prompt confirmation.
- Added `multiwfn2vesta stm-run`, backed by
  `src/multiwfn2vesta/multiwfn_stm.py`.  The default stream enters Multiwfn
  main function `300`, subfunction `4`, switches from default
  constant-distance to constant-current mode, sets grid/ranges when requested,
  calculates, and exports `STM.cub` from the post-processing menu.
- Added optional `--bias`, `--fermi`, `--prepare-fermi-temperature`,
  `--grid-points`, `--x-range`, `--y-range`, and `--z-range` controls.
  `--prepare-fermi-temperature` inserts the `300 -> 9` Fermi/occupation
  preparation step before entering STM, useful for metallic/slab Molden files.
- Added `cube-preset stm` plus aliases `ldos`, `stm-ldos`, and
  `tunneling-current`, with default single positive isosurface `0.001`.
- Integrated `stm-run` into the unified CLI, aliases `multiwfn-stm`,
  `multiwfn-stm-run`, and `ldos-run`, the interactive chooser, and package
  console scripts.
- Added focused tests in `tests/test_multiwfn_stm.py` plus CLI/preset tests.
  Focused validation passed: `py_compile` for the changed modules and
  `PYTHONPATH=src python3 -m unittest tests.test_multiwfn_stm
  tests.test_cube_preset tests.test_cli` (64 tests).  Full no-GUI regression
  passed with `PYTHONPATH=src python3 -m unittest discover -s tests`
  (221 tests).
- Real H2O noGUI smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_stm_run_smoke_20260610/h2o/`:
  `stm-run --grid-points 10 10 6 --stem h2o --timeout 300` generated raw
  `STM.cub`, processed `h2o_stm.cub`, `h2o_stm_cube.vesta`, and recipes.
  The processed cube has 600 grid points and range `3.7332e-13` to
  `0.0151741`.
- Optional occupation/Fermi-preparation smoke also passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_stm_run_smoke_20260610/h2o_prepare_fermi/`:
  `--prepare-fermi-temperature 298.15 --grid-points 6 6 4 --no-vesta`
  generated `h2o_stm.cub` with 144 grid points and range `3.7332e-13` to
  `0.00603356`.

## 2026-06-10: README branch refresh at grid surface bridge tip

- User asked to update README again, noted that the branch state still looked
  unusual, suggested merging back to one branch if useful, and requested Git
  identity `Stardust0831`.
- Rechecked `/mnt/g/work/multiwfn2vesta/project` after
  `git fetch --prune origin`: local `main`, `origin/main`, and `origin/HEAD`
  are aligned at `b99d80e2d3879eb7dbad260e4b8722c50427ad98`
  (`Add grid mapped-surface bridge`).  `git ls-remote --heads origin`
  exposes only `refs/heads/main`, also at `b99d80e`; no merge-back is needed
  in this pass.
- Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- Refreshed `README.md` so the front page records the current audited branch
  state, explicitly mentions the `grid-run --surface-cube` mapped-surface
  handoff, shows a quick ESP-on-density `grid-run` example, and replaces the
  stale 118-test validation note with the current 212-test no-GUI regression
  command.

## 2026-06-10: grid-run mapped-surface bridge

- Continued the long-running Multiwfn/ABACUS/VESTA analysis-expansion goal by
  closing a small but common gap between single-cube `grid-run` outputs and
  VESTA surface+texture figures.
- Added `grid-run --surface-cube SURFACE.cub`.  The command still generates
  one new Multiwfn real-space grid cube, but when `--surface-cube` is present
  that new cube is passed to `cube-preset` as the texture cube on the provided
  density/surface cube.
- Added mapped-preset defaults for main-function-5 outputs: ESP/nuclear ESP
  use `esp`, ALIE uses `alie`, sign(lambda2)rho uses `iri`, vdW potential
  uses `vdw-map`, and other functions fall back to `surface-map`.
- Batch orbital export now rejects `--surface-cube`, because each child run
  owns its own output and mapped-surface batch semantics are not yet defined.
- Real H2O noGUI smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_surface_cube_map_20260610/h2o_esp_map/`:
  `grid-run --function esp --surface-cube h2o_density.cub --grid-mode cube`
  generated `h2o_esp.cub` and `h2o_esp_esp_cube.vesta`.  The VESTA recipe
  records the density cube as Surface Cube and ESP as Texture Cube.
- A read-only source exploration noted two good later candidates: an STM/LDOS
  runner from Multiwfn main function `300`, subfunction `4`, exporting
  `STM.cub`; and domain extraction from main function `200`, subfunction
  `14`, exporting `domain.cub`/`domain.pdb`.

## 2026-06-10: IGM and mIGM command streams

- Continued the long-running Multiwfn/ABACUS/VESTA analysis-expansion goal by
  closing the next weak-interaction command-stream gap after IGMH.
- Rechecked local Multiwfn source evidence: `visweak.f90` menu options `10`,
  `-10`, and `11` dispatch to IGM, mIGM, and IGMH; IGM/mIGM ask for
  sign(lambda2)rho source when wavefunction information is present, while
  IGMH forces actual-density sign(lambda2)rho.
- Extended the maintained runner with `--method igmh|igm|migm` and
  `--sl2r-source actual|promolecular`.  `igmh-run` remains the default IGMH
  route; `igm-run` and `migm-run` are unified CLI convenience commands that
  inject the corresponding method.
- Output logs and raw directories are now method-aware:
  `multiwfn_igmh_*`, `multiwfn_igm_*`, or `multiwfn_migm_*`.  VESTA files are
  named `<stem>_<method>_cube.vesta`.
- Kept the periodic Molden `[Cell]` guard from the IGMH increment: `points`
  grid mode is still rejected for PBC inputs before Multiwfn launch.
- Added focused tests for IGM/mIGM command streams, IGMH rejection of
  promolecular sign(lambda2)rho, method-aware VESTA output naming, and unified
  CLI dispatch for `igmh-run`, `igm-run`, and `migm-run`.
- Read-only pre-commit review found a real wrapper risk: `igm-run --method
  igmh` or `migm-run --method igmh` could silently override the command name.
  The wrappers now reject any user-supplied `--method`; the generic
  `igmh-run --method igm|migm|igmh` route remains available for explicit
  method selection.
- The VESTA preset layer now receives a method-specific title such as
  `<stem>_dg_inter (igm)` so `igm`/`migm` recipes are not labeled as `igmh`
  just because the display preset resolves to the shared canonical `igmh`
  preset.
- Rechecked the repository after `git fetch --prune origin` for this closeout:
  local `main`, `origin/main`, and `origin/HEAD` are aligned at the pre-commit
  tip, `git ls-remote --heads origin` exposes only `refs/heads/main`, and the
  repository-local identity is `Stardust0831 <13862180016@163.com>`.
- Real noGUI H2O smokes passed for both new methods under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_igm_migm_run_smoke_20260610_review_fix/`,
  generating `h2o_igm_cube.vesta` and `h2o_migm_cube.vesta` with
  method-specific recipe titles and without launching the VESTA UI.
- Synced README, usage docs, CLI/IGM skills, research matrix, kanban, and root
  docs with the updated IGM/mIGM boundary.

## 2026-06-10: IGMH command-stream runner and README refresh

- User asked to update README, make the branch state less confusing, merge
  back to one branch if useful, and keep commit identity as `Stardust0831`.
- Rechecked the repository after `git fetch --prune origin`: local `main`,
  `origin/main`, and `origin/HEAD` are aligned, and `git ls-remote --heads
  origin` exposes only `refs/heads/main`.  No merge-back is needed in this
  pass.
- Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- Added `multiwfn2vesta igmh-run`, a maintained Multiwfn IGMH command-stream
  runner for wavefunction inputs and fragment definitions.  The default stream
  enters main function `20`, selects IGMH option `11`, forwards two-or-more
  fragment strings, selects a grid mode, exports `dg_inter.cub`/`sl2r.cub`,
  then calls `cube-preset igmh` unless `--no-vesta` is used.
- Integrated `igmh-run` into the unified CLI, aliases `multiwfn-igmh` and
  `multiwfn-igmh-run`, the interactive menu, and package console scripts.
  The existing top-level `igmh` alias remains the AIM+IGMH overlay styler.
- Added focused tests for generated command streams, complement fragment
  input, output copying, missing-cube failure handling, VESTA preset chaining,
  and CLI error handling.
- Read-only pre-commit review found a real periodic-grid risk: Multiwfn PBC
  grid option `4` reads spacing through `setgrid_for_PBC`, while non-PBC
  option `4` can read explicit `NX,NY,NZ`.  The runner now detects Molden
  `[Cell]` and rejects `--grid-mode points` before launching Multiwfn; docs
  steer periodic ABACUS workflows to `--grid-mode spacing` or `pbc-cell`, and
  tests cover the guard and the `pbc-cell` stream.
- Real noGUI smoke passed on H2O:
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_igmh_run_smoke_20260610/h2o/`.
  The run used fragments `1` and `2-3`, grid `8 x 8 x 8`, generated
  `h2o_dg_inter.cub`, `h2o_sl2r.cub`, optional `h2o_dg_intra.cub` and
  `h2o_dg.cub`, plus `h2o_igmh_cube.vesta` without launching VESTA.
- Refreshed README branch-status wording so it records the current one-branch
  state without stale commit hashes, and documented `igmh-run` usage,
  outputs, and relationship to `cube-preset igmh`.
- Synced usage docs, CLI skill notes, the IGMH preset skill, new
  `docs/skills/multiwfn_igmh_run_skill.md`, the research matrix, kanban, and
  root docs.

## 2026-06-10: IGMH and aIGM cube presets

- Continued the Multiwfn/ABACUS/VESTA roadmap by closing a display-layer gap
  for Multiwfn IGM/IGMH/aIGM weak-interaction cube pairs.
- Rechecked bundled Multiwfn VMD templates:
  `IGM_inter.vmd` uses `dg_inter.cub` as the isosurface at `0.01000` and
  `sl2r.cub` as texture with `scaleminmax -0.05 0.05`;
  `IGM_intra.vmd` uses `dg_intra.cub` at `0.2000` with the same texture range;
  `aIGM.vmd` uses `avgdg_inter.cub` at `0.008` colored by `avgsl2r.cub`; and
  `aIGM_TFI.vmd` uses `avgdg_inter.cub` at `0.008` colored by `thermflu.cub`
  with range `0.0` to `1.5`.
- Added `cube-preset` entries for `igmh`/`igm-inter`, `igm-intra`, `aigm`,
  and `aigm-tfi`.  These are VESTA display presets for already-generated cube
  pairs; Multiwfn fragment command-stream automation remains a later
  increment.
- Added focused tests for preset listing, alias resolution, template-derived
  isosurfaces, texture physical ranges, and manifest notes.
- Real no-GUI smoke passed on the Ag(111)+benzene periodic-cell IGMH cubes:
  `/mnt/g/work/multiwfn2vesta/smoke/igmh_preset_20260610_1128/products/`.
  The run generated `dg_inter_igmh_cube.vesta` and
  `dg_inter_igmh_cube_vesta_recipe.md` from `dg_inter.cub` plus `sl2r.cub`
  without launching VESTA.
- Final validation passed after read-only review: `git diff --check`,
  `py_compile`, 52 focused cube/CLI tests, full 192-test no-GUI regression,
  and `cube-preset --list-presets`.
- Synced README, usage docs, cube/CLI/ABACUS/AIM+IGMH skill notes, new
  `docs/skills/igmh_vesta_preset_skill.md`, the research matrix, and
  project/root kanban/worklog.  Final validation and commit hash are reported
  in the assistant response to avoid an infinite chain of "record the record"
  commits.

## 2026-06-10: README branch cleanup at surface-extrema tip

- User asked to update README again, noted that the branch state looked
  confusing, suggested merging back to one branch if useful, and requested
  commit identity `Stardust0831`.
- Rechecked `/mnt/g/work/multiwfn2vesta/project` before the README cleanup
  commit after `git fetch --prune origin`.  Local `main`, `origin/main`, and
  `origin/HEAD` all pointed at
  `8bf115a3fa332e1008c370d48e70e5235e942ac5`
  (`Add surface extrema VESTA overlay`), and `git ls-remote --heads origin`
  exposes only `refs/heads/main`.
- Confirmed no merge-back is needed in this pass because there is no extra
  local or remote feature branch.  The branch shape is a single `main` history
  containing feature commits and documentation closure commits.
- Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- Refreshed `README.md` Repository Status so it records the current audited
  tip, the one-branch remote state, and the future short-lived experiment
  branch merge pattern.
- Validation passed: `git diff --check` and `bin/multiwfn2vesta --help`.
- Read-only pre-commit review verified the README branch-status claims.  It
  noted that the current `docs/kanban.md` diff also contains an IGMH planning
  block; this is retained as board planning, not described as a README feature
  change.
- Synced project/root kanban and worklog records.  Commit hash and post-push
  branch check are reported in the assistant response to avoid an infinite
  chain of "record the record" commits.

## 2026-06-10: Surface extrema overlays for mapped surfaces

- Continued the Multiwfn/ABACUS/VESTA roadmap by closing the next
  surface-map gap: optional VESTA overlays for Multiwfn `surfanalysis.pdb`
  extrema points.
- Rechecked Multiwfn source and bundled scripts.  Evidence used:
  `surfana.f90` menu item `2` exports `surfanalysis.pdb`; maxima are written
  as carbon records, minima as oxygen records, and B-factor stores mapped
  function values; bundled `molsurfmap.vmd`, `ALIE.vmd`, `LEA_isoext.vmd`,
  and `LEAE_isoext.vmd` load `surfanalysis.pdb` for mapped-surface extrema.
- Added `src/multiwfn2vesta/surface_extrema_vesta.py`, including
  `surfanalysis.pdb` parsing, cube-origin coordinate alignment, VESTA
  atoms-only phase rendering, `COMPS 0` patching, and standalone CLI
  `multiwfn2vesta surface-extrema`.
- Extended `cube-preset` with `--surfanalysis-pdb`, `--surf-extrema
  auto|all|maxima|minima`, extrema radius/color controls, and optional
  extrema labels.  Auto mode follows bundled VMD intent: `alie`/`leae`
  minima, `lea` maxima, other mapped-surface presets all extrema.
- Added focused tests for parser semantics, coordinate shift, extrema phase
  insertion, standalone CLI dispatch, and `cube-preset alie` auto minima
  overlay.
- Real CLI smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/surface_extrema_overlay_20260610/`.
  The generated VESTA file contains `MAX0001`/`MIN0001`, overlay `SBOND`
  disabled, `COMPS 0`, and a `Surface Extrema Overlay` recipe block; the
  standalone command produced a minima-only overlay.
- Synced README, usage docs, cube/ABACUS skill notes, research matrix, and
  project/root kanban/worklog.  Final validation and commit hash are reported
  in the assistant response to avoid an infinite chain of "record the record"
  commits.
- Read-only pre-commit review found no blockers.  The main thread fixed the
  only immediate documentation mismatch: standalone `surface-extrema` uses
  `--radius`, while `cube-preset` uses `--extrema-radius`.  The skill note now
  also records that standalone patching appends a new phase each run and that
  `CRYST1` is not yet cross-checked against `--surface-cube`.
- Final validation passed: `py_compile`, 52 focused tests across
  `tests.test_surface_extrema_vesta`, `tests.test_cube_preset`, and
  `tests.test_cli`, full 189-test no-GUI regression, `git diff --check`,
  top-level help, `cube-preset --help`, and `surface-extrema --help`.

## 2026-06-10: README refresh at surface-map/grid tip

- User asked to update README, noted that the branch state still looked odd,
  suggested merging back to one branch if useful, and requested identity
  `Stardust0831`.
- Rechecked `/mnt/g/work/multiwfn2vesta/project` after `git fetch --prune
  origin`.  Local `main`, `origin/main`, and `origin/HEAD` all point at
  `19bd45dfc33f29309c90d408b5672fb137043b9f`
  (`Add surface-map presets and grid functions`), and the GitHub remote
  exposes only `refs/heads/main`.
- Confirmed there is no extra local or remote feature branch to merge back in
  this pass.  The apparently unusual branch history is a linear `main`
  history with feature commits and documentation closure commits.
- Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- Refreshed `README.md` Repository Status so it records the current audited
  `main` tip, describes the current one-branch remote state, and lists the
  latest maintained feature as the surface-map/grid expansion.
- Validation before commit passed: `git diff --check` and
  `bin/multiwfn2vesta --help`.  The final docs commit hash and post-push
  branch check are reported in the assistant response to avoid an infinite
  chain of "record the record" commits.

## 2026-06-10: Surface-map presets and expanded Multiwfn grid table

- Continued the long-running Multiwfn/ABACUS/VESTA roadmap by targeting two
  closely related gaps: more Multiwfn main-function-5 real-space functions
  from ABACUS-compatible wavefunction files, and VESTA presets for
  density-surface mapped-property figures.
- Rechecked local Multiwfn source/examples.  Evidence used:
  `function.f90` lists K(r), G(r), ALIE, promolecular RDG/sign(lambda2)rho,
  and vdW potential in the real-space function menu; `0123dim.f90` records
  default cube filenames `K(r).cub`, `G(r).cub`, `avglocion.cub`,
  `RDGprodens.cub`, and `signlambda2rhoprodens.cub`; bundled VMD scripts
  show ALIE/LEA/LEAE/vdW as density/surface cube plus mapped texture cube.
- Added `cube-preset` entries for `surface-map`, `alie`, `lea`, `leae`, and
  `vdw-map`.  These write density/surface + texture VESTA files through the
  existing `cube-vesta` backend.  Default surface-map/ALIE/LEA/LEAE/vdW
  isosurfaces and texture ranges follow the bundled Multiwfn VMD examples.
- Added `grid-run` function-table entries for Hamiltonian KED `K(r)`,
  Lagrangian KED `G(r)`, promolecular RDG, promolecular
  sign(lambda2)rho, and ALIE `avglocion.cub`.
- Updated tests for preset listing/default manifests and grid function
  resolution/command streams.
- Synced README, usage docs, cube/grid/ABACUS/CLI skill notes, the
  Multiwfn/ABACUS/VESTA analysis matrix, and project/root kanban/worklog.
- Focused validation passed: `py_compile`, 33 tests across
  `tests.test_cube_preset` and `tests.test_multiwfn_grid`,
  `bin/multiwfn2vesta cube-preset --list-presets`, and
  `bin/multiwfn2vesta grid-run --list-functions`.
- Real H2O noGUI smokes passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_surface_map_20260610/`.
  Multiwfn exported raw `K(r).cub` for `hamiltonian-ked`, raw
  `avglocion.cub` for `alie`, a matching `density.cub`, and
  `cube-preset alie` wrote `h2o_alie_surface_cube.vesta` plus its recipe.
- Read-only pre-commit review found no blocker, but caught that the
  `surface-map`/`molsurfmap` default should match Multiwfn `molsurfmap.vmd`.
  The main thread fixed the preset to use density isosurface `0.01` and
  default texture range `0.0` to `0.002`, then added a unit test for that
  default.
- Final pre-commit validation passed: `py_compile`, 68 focused tests across
  `tests.test_cube_preset`, `tests.test_multiwfn_grid`, and `tests.test_cli`,
  full 182-test no-GUI regression, `git diff --check`,
  `bin/multiwfn2vesta cube-preset --list-presets`, and
  `bin/multiwfn2vesta grid-run --list-functions`.
- Deliberately left Multiwfn `surfanalysis.pdb` extrema overlays as the next
  surface-map layer rather than mixing phase appending into this preset-table
  increment.

## 2026-06-10: README single-branch refresh

- User asked to update README, noted that the branch state still looked odd,
  suggested merging back to one branch if useful, and requested identity
  `Stardust0831`.
- Rechecked `/mnt/g/work/multiwfn2vesta/project` after `git fetch --prune
  origin`.  Local `main`, `origin/main`, and `origin/HEAD` all pointed at
  `0c1b5c6b88e65501437b6a947dc97f4876cfdc61`
  (`Record Multiwfn atom table coloring push`), and the GitHub remote exposed
  only `refs/heads/main`.
- Confirmed there is no extra local or remote feature branch to merge back in
  this pass.  The apparently unusual branch history is a linear set of normal
  `main` commits, including feature commits and documentation closure commits.
- Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- Refreshed `README.md` Repository Status so it records the verified
  pre-refresh `main` tip, explains that earlier branch-refresh entries are
  ordinary `main` history rather than active branches, and lists the latest
  maintained feature as generic Multiwfn atom scalar table coloring.
- Validation before commit passed: `git diff --check` and
  `bin/multiwfn2vesta --help`.  The final docs commit hash and post-push
  branch check are reported in the assistant response to avoid an infinite
  chain of "record the record" commits.

## 2026-06-10: Multiwfn atom table coloring

- Continued the long-running Multiwfn/ABACUS/VESTA roadmap by implementing a
  maintained generic atom-scalar table entry point:
  `multiwfn2vesta multiwfn-atom-color`.
- Added `src/multiwfn2vesta/multiwfn_atom_table.py`.  The parser accepts
  CSV, TSV, and whitespace tables copied/exported from Multiwfn or prepared
  manually.  It supports one ordered value per line, one-based atom-index
  keyed tables, VESTA-label keyed tables, `--value-column` for multi-value
  tables, and `--key-column` when the key column is ambiguous.
- The workflow reuses the existing VESTA atom-coloring backend:
  per-atom values are mapped to blue-white-red RGB values in Python and
  written into VESTA `SITET` rows.  It does not rely on a VESTA-native scalar
  atom colormap.
- Strict mode now requires ordered row counts to match the selected VESTA
  `STRUC` section exactly.  For index- or label-keyed tables it requires the
  same key set and rejects duplicate keys, but does not require the table row
  order to match VESTA.  `--non-strict` is the explicit route for intentional
  subset coloring.
- Integrated the command into the unified CLI as `multiwfn-atom-color` with
  aliases `multiwfn-table-color` and `atom-table-color`, plus interactive menu
  item `12` and console script
  `multiwfn2vesta-multiwfn-atom-color`.
  The older `atom-color` alias remains mapped to `abacus-mulliken-color` for
  compatibility.
- Added focused tests in `tests/test_multiwfn_atom_table.py` and extended
  `tests/test_cli.py` for direct dispatch, aliases, help text, and
  interactive argument construction.
- Synced README, usage docs, CLI/atom-coloring skill notes, the
  ABACUS/Multiwfn/VESTA research matrix, and project/root kanban/worklog.
- Focused validation passed before full regression: `py_compile` for touched
  Python files, 45 tests across `tests.test_multiwfn_atom_table` and
  `tests.test_cli`, and CLI help checks for `multiwfn-atom-color` and the
  top-level launcher.
- Read-only pre-commit review found and the main thread fixed three behavior
  issues before commit: ambiguous multi-value tables now require
  `--value-column` instead of relying on unordered alias iteration;
  `atom-color` remains the historical ABACUS Mulliken alias; strict keyed
  tables validate key sets rather than row order and reject duplicate keys.
- Real CLI smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_atom_color_smoke_20260610/`.
  The smoke colored a three-site H/O/H VESTA file from a Multiwfn-like
  `Atom Label Charge Fukui` table, wrote `colored_after_review.vesta`, and
  wrote normalized `values_after_review.csv`.
- Final pre-commit validation passed: 178-test no-GUI regression and
  `git diff --check`.
- Feature implementation commit was pushed to GitHub `main` as
  `7b305ea5762b3e8444b53338aecec190cc331a7f`
  (`Add Multiwfn atom table coloring`).
- Post-push verification after `git fetch --prune origin`: project `HEAD`,
  `origin/main`, and `origin/HEAD` all pointed at `7b305ea`; remote heads
  exposed only `refs/heads/main`; repository-local identity remained
  `Stardust0831 <13862180016@163.com>`.

## 2026-06-10: README branch consolidation refresh

- User asked to update README again, noted that the branch state looked odd,
  suggested merging back to one branch if needed, and requested identity
  `Stardust0831`.
- Rechecked `/mnt/g/work/multiwfn2vesta/project` with
  `git fetch --prune origin`, `git status --short --branch`,
  `git branch --all --verbose --no-abbrev`, and
  `git ls-remote --heads origin`.
- Result: local `main`, `origin/main`, and `origin/HEAD` all point at
  `2481cf79c87666503ea8d8186b4b76fba05b2847`
  (`Record batch orbital push`), and the GitHub remote exposes only
  `refs/heads/main`.  There is no local or remote feature branch to merge in
  this pass.
- Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- Refreshed `README.md` so its Repository Status section records the current
  verified branch tip, states explicitly that no merge action is needed, and
  describes future experiment branches as short-lived branches that should be
  merged or fast-forwarded back to `main`.
- Synced project/root kanban and worklog entries with this branch audit.
- Validation before the first README/docs commit passed:
  `git diff --check`, `bin/multiwfn2vesta --help`,
  `git branch --all --verbose --no-abbrev`,
  `git ls-remote --symref origin HEAD`, and `git ls-remote --heads origin`.
- Committed and pushed the README branch consolidation refresh to GitHub
  `main` as `500ffece49c42bcbb4a44d49bcd31044d915bce0`
  (`Refresh README branch consolidation status`).
- Post-push verification after `git fetch --prune origin`: project `HEAD`,
  `origin/main`, and `origin/HEAD` all pointed at `500ffec`; remote heads
  exposed only `refs/heads/main`; repository-local identity remained
  `Stardust0831 <13862180016@163.com>`.

## 2026-06-10: Batch orbital grid export and README branch refresh

- User asked to refresh README, simplify the branch state if needed, and keep
  commits under identity `Stardust0831`.  Rechecked the project state before
  editing: local `main` tracks `origin/main`, `origin/HEAD` points to
  `origin/main`, and the remote exposes only `refs/heads/main`, so there is
  no extra feature branch to merge in this pass.
- Continued the existing `grid-run` roadmap by adding batch
  `orbital`/`orbital-density` export.  Batch mode is implemented as repeated
  isolated single-orbital Multiwfn main-function-5 runs, not as a new
  Multiwfn menu stream.
- Added `run_multiwfn_grid_batch`, `MultiwfnGridBatchResult`, safe orbital
  labels such as `l+1 -> lplus1`, per-orbital child directories, and a
  top-level `multiwfn_grid_batch_recipe.md`.
- Batch child runs write their own command stream, stdout/stderr logs, raw
  cube directory, processed cube, single-run recipe, and optional VESTA output.
  The batch recipe records requested orbitals, safe labels, status,
  failed/skipped counts, and child paths.  It is written before the first
  child run and refreshed after each child run.
- Integrated the feature into `grid-run --orbitals`.  If `--orbitals` is used
  without `--function`, the CLI now defaults to `orbital`; use
  `--function orbital-density --orbitals ...` for orbital-density batches.
  `--keep-going` continues after failed orbitals; the default stops after the
  first failure and marks later orbitals as `skipped`.
- Hardened invalid CLI combinations after read-only sub-agent review:
  `--orbitals` rejects `--orbital`, `--commands-file`, `--expected-cube`, and
  `--raw-dir`; `--keep-going` without `--orbitals` is rejected instead of
  being silently ignored.
- Adjusted the interactive launcher so entering one or more orbital selectors
  defaults the function prompt to `orbital`; multiple selectors build
  `--orbitals`.
- Added focused tests for isolated batch output, default stop-on-failure,
  `--keep-going`, batch recipe status/skipped records, direct
  `grid-run --orbitals` CLI behavior, invalid argument combinations, and the
  interactive launcher.
- Synced README, usage docs, CLI/grid/ABACUS skill notes, the ABACUS/Multiwfn
  analysis matrix, and project/root work records with the maintained batch
  orbital workflow and the verified single-branch repository state.
- Focused validation already passed before full regression:
  `py_compile` for touched Python files and 52 tests across
  `tests.test_multiwfn_grid` and `tests.test_cli`.
- Final validation before commit passed: full 163-test no-GUI regression,
  `grid-run --help`, top-level `multiwfn2vesta --help`, and
  `git diff --check`.
- Feature implementation commit was pushed to GitHub `main` at
  `dcf7bd3cac0684f48f16ebd06458345b929837fd`
  (`Add batch orbital grid export`).  Post-push verification after
  `git fetch --prune origin`: `HEAD`, `origin/main`, and `origin/HEAD` all
  pointed at `dcf7bd3`; `git ls-remote --heads origin` returned only
  `refs/heads/main`; repository-local identity remained
  `Stardust0831 <13862180016@163.com>`.

## 2026-06-10: Cube arithmetic foundation

- Continued the long-running Multiwfn/ABACUS/VESTA roadmap by implementing
  `multiwfn2vesta cube-arith`, a maintained compatible-cube linear arithmetic
  bottom layer for density differences, Fukui functions, and dual
  descriptors.
- The command supports generic repeated `--term COEFF CUBE` entries plus named
  operations: `density-difference` (`plus - minus`), `fukui-plus`
  (`rho(N+1)-rho(N)`), `fukui-minus` (`rho(N)-rho(N-1)`), and
  `dual-descriptor` (`rho(N+1)-2*rho(N)+rho(N-1)`).
- The workflow writes `<stem>.cub`, `<stem>_cube_arith_recipe.md`, refuses to
  overwrite any input cube, requires compatible cube grids by default, and
  optionally calls `cube-preset` for VESTA output.  The default display preset
  is `auto`: `fukui-plus/minus` use `density`, while density differences,
  dual descriptors, and generic linear combinations use `signed`.
- Integrated the command into the unified CLI, aliases `cube-math`,
  `density-diff`, and `fukui-cube`, interactive menu item `11`, and console
  script `multiwfn2vesta-cube-arith`.
- Added `tests/test_cube_arith.py` and extended `tests/test_cli.py`.
  Focused validation passed: 39 tests across `tests.test_cube_arith` and
  `tests.test_cli`, plus `py_compile`.
- A read-only pre-commit review found a real unit compatibility edge case.
  The main thread fixed it by requiring matching cube unit conventions by
  default, so `--cube-units auto` rejects mixed positive-count Bohr and
  negative-count Angstrom cube headers before arithmetic.  An explicit
  `--cube-units bohr` or `--cube-units angstrom` remains a user override.
- Real CLI smokes passed under
  `/mnt/g/work/multiwfn2vesta/smoke/cube_arith_smoke_20260610/products_auto_signed/`
  and
  `/mnt/g/work/multiwfn2vesta/smoke/cube_arith_smoke_20260610/products_auto_fukui/`.
  The first wrote `signed_half.cub`, its arithmetic recipe, and signed VESTA
  files via `--preset auto`; the second wrote a zero Fukui-plus cube and
  recipe with `--no-vesta`.
- Full no-GUI regression passed after the auto-preset/unit fix: 153 tests across
  the project suite.
- Synced README, usage docs, cube/CLI skill notes, new
  `docs/skills/cube_arith_skill.md`, the ABACUS/Multiwfn/VESTA research
  matrix, and project/root work records.  This is documented as a cube
  post-processing foundation, not as automatic generation of charged-state
  wavefunctions.
- Feature implementation commit was pushed to GitHub `main` at
  `4123d00ae051a710c954ed3c3712aa8b012c4bc0`
  (`Add cube arithmetic workflow`).  Post-push verification after
  `git fetch --prune origin`: local `main`, `origin/main`, and `origin/HEAD`
  all pointed at `4123d00`; `git ls-remote --heads origin` returned only
  `refs/heads/main`; repository-local identity remained
  `Stardust0831 <13862180016@163.com>`.
- The first documentation closure was pushed as
  `4800cf4b2dbab559d64023852cc3579e7696ad15`
  (`Record cube arithmetic push`).  This docs-only commit preserves the same
  single-branch layout.

## 2026-06-10: Multiwfn real-space grid runner

- Continued the long-running Multiwfn/ABACUS/VESTA roadmap by turning
  Multiwfn main function `5` (`study3dim`) into a maintained CLI workflow:
  `multiwfn2vesta grid-run`.
- Implemented `src/multiwfn2vesta/multiwfn_grid.py`.  The runner discovers
  Multiwfn, records `multiwfn_grid_input.txt`, stdout/stderr logs, raw cube
  directory, processed `<stem>_<function>.cub`, and `multiwfn_grid_recipe.md`.
  It optionally calls `cube-preset`/`cube-vesta` for VESTA `.vesta` output.
- Function table currently covers density, gradient, Laplacian, orbital/MO
  value, spin density, nuclear ESP, ELF, LOL, total ESP/MEP, RDG,
  sign(lambda2)rho, Delta-g, IRI, vdW potential, and orbital density.  Orbital
  and orbital-density functions require `--orbital`; custom function indices
  can use `--function-index` plus `--expected-cube`.
- Integrated `grid-run` into the unified CLI, aliases `multiwfn-grid`,
  `scalar-cube-run`, and `function-cube`, interactive menu item `10`, and
  console script `multiwfn2vesta-grid-run`.
- Added `tests/test_multiwfn_grid.py` and extended `tests/test_cli.py`.
  Focused validation passed: 39 tests across `tests.test_multiwfn_grid` and
  `tests.test_cli`.
- A read-only pre-commit sub-agent review found no blocking issue.  The main
  follow-up narrowed the interactive `grid-run` preset prompt to
  `auto/density/signed/elf/lol`, because `iri` and `esp` presets require a
  separate texture cube.
- Real H2O density smoke:
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_density/products/`.
  It used
  `/mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI`,
  command stream `5 / 1 / 4 / 12,12,12 / 2 / 0 / q`, returned `0`, wrote raw
  `density.cub`, processed `h2o_density.cub`, and generated
  `h2o_density_density_cube.vesta` plus recipe.  VESTA was not launched.
- Real H2O ELF smoke:
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_elf/products/`.
  It ran `--function elf --no-vesta`, returned `0`, wrote raw `ELF.cub`,
  processed `h2o_elf.cub`, and wrote `multiwfn_grid_recipe.md`.
- Synced README, usage docs, CLI/cube/ABACUS skill notes, new
  `docs/skills/multiwfn_grid_run_skill.md`, and the research matrix.  The
  matrix now records that main-function-5 single cube generation is
  implemented, while batch orbital export, Fukui/dual descriptor, and IGMH
  fragment command streams remain future work.
- Final pre-commit validation passed: `py_compile`, 140-test no-GUI
  regression, `grid-run --list-functions`, `grid-run --help`, top-level
  `multiwfn2vesta --help`, and `git diff --check`.
- Feature implementation commit was pushed to GitHub `main` at
  `3d192dc7ae9696dd433aae04e1a3bdb488b95482`
  (`Add Multiwfn grid runner`).  The commit explicitly included the new
  runner, CLI/package integration, README/usage/skill docs, the updated
  analysis matrix, the new tests, and the cleanup of stale legacy test
  imports.
- Post-push verification after `git fetch --prune`: `HEAD`, `origin/main`,
  and `origin/HEAD` all pointed at `3d192dc`; `git ls-remote --heads origin`
  returned only `refs/heads/main`; repository-local identity remained
  `Stardust0831 <13862180016@163.com>`.

## 2026-06-10: README branch follow-up audit

- User asked to update README again, noted that the branch state looked odd,
  suggested merging back to one branch if needed, and requested
  `Stardust0831` identity for the work.
- Rechecked `/mnt/g/work/multiwfn2vesta/project` with `git fetch --prune`,
  `git status --short --branch`, `git branch --all --verbose --no-abbrev`,
  and `git ls-remote --heads origin`.
- Result: local `main` and `origin/main` both point at
  `17667f2a1a7380fb7a2c2495f9df04ef633e0577`; `origin/HEAD` points to
  `origin/main`; the GitHub remote exposes only `refs/heads/main`.  There is
  no feature branch to merge back during this pass.
- Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- Updated `README.md` so the repository-status section records the verified
  commit, the one-branch remote state, the maintainer identity commands, and
  a future fast-forward merge pattern for short-lived experiment branches.
- Validation before commit passed with `git diff --check` and
  `bin/multiwfn2vesta --help`.  A read-only sub-agent review found no content
  blocker and explicitly warned not to use `git add .` because the separate
  `grid-run` draft is still untracked.
- The working tree also contains the ongoing `grid-run` implementation draft
  (`src/multiwfn2vesta/multiwfn_grid.py`) and related kanban notes.  That
  feature remains a separate increment and is intentionally not treated as a
  branch-merge cleanup.
- Committed and pushed the README branch follow-up as
  `41bfc9ce691b8de195a69566b56ac84df335947b`
  (`Refresh README branch follow-up`).  Push target was
  `Github:Stardust0831/multiwfn2vesta.git`, branch `main`, advancing the
  remote from `17667f2` to `41bfc9c`.
- Post-push status check showed `HEAD -> main`, `origin/main`, and
  `origin/HEAD` all at `41bfc9c`; `src/multiwfn2vesta/multiwfn_grid.py`
  remained untracked, confirming the README/branch cleanup did not include
  the unfinished `grid-run` code.

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
- Validation passed with `git diff --check` and
  `bin/multiwfn2vesta --help`.  The README refresh was committed as
  `dec8150` (`Refresh README branch status`) and pushed to GitHub `main`;
  any later docs-only closure commit only records this result.

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
