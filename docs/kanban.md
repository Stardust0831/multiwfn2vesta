# Project Kanban

Updated: 2026-06-11 22:10 CST

## Current Request: 2026-06-11 README Refresh And One-Branch Closeout For FOD Route

- [x] Record user request immediately: update README, inspect the unusual
  branch state, converge back to one maintained branch if needed, and keep
  repository-local Git identity as `Stardust0831`.
- [x] Confirm local branch and identity before staging anything.  Current
  branch is `main`, tracking `origin/main`; remote tracking refs expose
  `origin/HEAD -> origin/main` and `origin/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.  Current uncommitted work is the
  function-100 fractional occupation density increment plus docs; local
  untracked `domain.cub` and `domain.pdb` must stay uncommitted.
- [x] Finish README/docs/tests/review for the FOD route, mirror root docs,
  fetch/prune and confirm whether any real merge-back is needed, then
  commit/push to the maintained branch.  Code/tests/docs now include the
  extra alias `fractional-occupancy-density`, standalone and mapped-surface
  fake-run coverage, and the caveat that FOD may need a lower standalone
  isosurface such as `--isosurface 0.001`.  Validation passed:
  `py_compile`, 74 focused `tests.test_multiwfn_grid` tests, 127 focused
  `tests.test_multiwfn_grid tests.test_cli` tests, 338 full no-GUI tests, and
  CLI smokes; `git diff --check` passed.  `git fetch --prune origin` found
  only `main`, `origin/main`, and `origin/HEAD -> origin/main`; no real
  merge-back is needed.  Root-docs mirror checksum dry-run is empty.  Final
  commit hash, push result, and post-push branch verification are reported in
  the assistant response.

## Active Goal Continuation: 2026-06-11 Next Function-100 Wavefunction Analysis Route

- [x] Record automatic continuation of the long-running objective: keep
  surveying valuable Multiwfn wavefunction analyses that can be visualized in
  VESTA, prioritizing ABACUS-compatible LCAO Molden or direct cube routes.
- [x] Recheck current repository state after the spin-channel density commit,
  preserve local untracked `domain.cub` and `domain.pdb`, and select the next
  bounded source-backed Multiwfn/VESTA increment.  Current `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `b565f4d4fe3dc021ad3dd3c744f1a0fbdffa431c`; only this kanban update plus
  untracked `domain.cub` and `domain.pdb` were present.  Selected increment:
  function-100 fractional occupation density FOD (`iuserfunc=90`), which local
  Multiwfn evaluates via `FODfunc(x,y,z)` and exports as `userfunc.cub`.
- [x] Implement the selected route with focused tests, README/usage/skill/
  research/worklog/kanban notes, root-docs mirror, validation, commit, push,
  and branch verification.  Code/tests/docs now include
  `grid-run --function fractional-occupation-density` / `fod` /
  `fractional-occupancy-density`, standalone `density` preset, mapped
  `surface-map`, and caveats for integer occupations, ABACUS Molden
  occupation export, metallic smearing, multi-k, SOC/noncollinear
  interpretation, and lowered FOD isosurfaces when needed.  Validation passed:
  `py_compile`, 74 focused `tests.test_multiwfn_grid` tests, 127 focused
  `tests.test_multiwfn_grid tests.test_cli` tests, 338 full no-GUI tests, and
  CLI smokes; `git diff --check` passed.  Root-docs mirror checksum dry-run is
  empty.  Final commit hash, push result, and branch verification are reported
  in the assistant response.

## Active Goal Continuation: 2026-06-11 Next ABACUS/Multiwfn VESTA Analysis Route

- [x] Record automatic continuation of the long-running objective: keep
  surveying valuable Multiwfn wavefunction analyses that can be visualized in
  VESTA, prioritizing routes that ABACUS can feed through current LCAO Molden
  files or direct cube outputs.
- [x] Recheck current repository state, pushed branch alignment, existing
  `grid-run`/`cube-preset`/analysis-matrix coverage, and local Multiwfn source
  before selecting the next bounded source-backed increment.  Current `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `c43d37ca0486be07ae8502256d0eaa5846fba615`; only this kanban update plus
  local untracked `domain.cub` and `domain.pdb` were present before the new
  increment.  Selected increment: function-100 alpha/beta density routes
  from local Multiwfn `iuserfunc=1/2`, which call
  `fspindens(x,y,z,'a'/'b')` and export `userfunc.cub`.
- [x] Implement one additional valuable route or visualization control with
  focused tests, README/usage/skill/research/worklog/kanban notes, root-docs
  mirror, validation, commit, push, and branch verification while preserving
  untracked `domain.cub` and `domain.pdb`.  Code/tests/docs now include
  `grid-run --function alpha-density` and `beta-density`, aliases
  `rho-alpha`/`alpha-rho`/`rho-beta`/`beta-rho`, standalone `density` preset,
  mapped `surface-map`, and caveats for closed-shell, EDF/ECP, and ABACUS
  `nspin=2` Molden usage.  Read-only subagent review supported the route and
  flagged alias/caveat refinements that were handled.  Validation passed:
  `py_compile`, 72 focused `tests.test_multiwfn_grid` tests, 125 focused
  `tests.test_multiwfn_grid tests.test_cli` tests, 336 full no-GUI tests,
  CLI smokes, and `git diff --check`.  Final root-docs mirror, commit hash,
  push result, and branch verification are reported in the assistant response.

## Current Request: 2026-06-11 README Refresh And Branch Closeout For Orbital-Weighted Fukui Routes

- [x] Record user request immediately: update README, inspect the unusual
  branch state, converge back to one maintained branch if needed, and keep
  repository-local Git identity as `Stardust0831`.
- [x] Confirm local branch and identity before staging anything.  Current
  branch is `main`, tracking `origin/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.  Current uncommitted work is the
  orbital-weighted Fukui/dual descriptor increment plus docs; local untracked
  `domain.cub` and `domain.pdb` must stay uncommitted.
- [x] Finish README/docs/tests/review for the orbital-weighted
  Fukui+/Fukui-/Fukui0/dual-descriptor route, mirror root docs, fetch/prune
  and confirm whether any real merge-back is needed, then commit/push to the
  maintained branch.  Code/tests/README/usage/skills/research/worklog now
  cover function-100 `iuserfunc=95/96/97/98`, aliases including `ow-dd`,
  standalone `density`/`signed` presets, mapped `surface-map`, and the
  source caveat that `orbwei_delta=0.1` a.u. remains a Multiwfn default.
  Validation passed: `py_compile`, 70 focused `tests.test_multiwfn_grid`
  tests, 123 focused `tests.test_multiwfn_grid tests.test_cli` tests, 334
  full no-GUI tests, CLI smokes, and `git diff --check`.  `git fetch --prune
  origin` still shows only the maintained `main` branch, so no merge-back is
  needed before committing.  Root docs checksum mirror dry-run is empty.
  Final commit hash, push result, and post-push branch verification are
  reported in the assistant response.

## Active Goal Continuation: 2026-06-11 Next ABACUS/Multiwfn VESTA Analysis Increment

- [x] Record automatic continuation of the long-running objective: keep
  surveying valuable Multiwfn wavefunction analyses that can be visualized in
  VESTA, prioritizing routes that ABACUS can feed through LCAO Molden files or
  direct cube outputs.
- [x] Recheck current repository state, existing analysis matrix, and local
  Multiwfn source/templates before selecting the next bounded increment.
  Current `main` is aligned with `origin/main`; only this kanban update plus
  untracked `domain.cub` and `domain.pdb` are present.  Selected increment:
  named orbital-weighted Fukui+/Fukui-/Fukui0/dual-descriptor routes from
  Multiwfn function `100` `iuserfunc=95/96/97/98`.
- [x] Implement one source-backed improvement that materially broadens the
  maintained ABACUS/Multiwfn/VESTA workflow, with focused tests and synced
  README/usage/skill/worklog/kanban notes.  Source evidence: local Multiwfn
  `function.f90` maps cases `95..98` to `orbwei_Fukui(1..4)` and exports
  function `100` as `userfunc.cub`; `define.f90` defaults `orbwei_delta` to
  `0.1` a.u.  Implementation/docs are now staged for validation: four named
  routes, short aliases, standalone and mapped presets, and focused resolver,
  command-stream, standalone, and mapped-surface tests are present.  Read-only
  subagent review confirmed the route and caveats, and validation passed.
- [x] Mirror root docs, commit, push, and verify `main` alignment while
  preserving untracked `domain.cub` and `domain.pdb`.  Root docs checksum
  mirror dry-run is empty; final commit hash and post-push branch verification
  are reported in the assistant response.

## Active Goal Continuation: 2026-06-11 Next ABACUS/Molden Visualization Increment

- [x] Record automatic continuation of the long-running objective: survey and
  implement valuable Multiwfn wavefunction analyses that can be visualized in
  VESTA, prioritizing analyses ABACUS can feed through LCAO Molden files or
  direct cube outputs.
- [x] Recheck current repository state, existing grid/preset coverage, and
  local Multiwfn source/templates before selecting the next bounded increment.
  Current branch is `main` aligned with `origin/main` after the DORI commit;
  only `docs/kanban.md` plus local untracked `domain.cub` and `domain.pdb`
  were present before this increment.  Source review found that
  function-100 `iuserfunc=28` is local Mulliken electronegativity and
  `iuserfunc=29` is local hardness, both exported as `userfunc.cub`; bundled
  examples provide generic `molsurfmap.vmd` but no dedicated color scale.
- [ ] Select and implement one source-backed route that moves the project
  closer to broad Multiwfn-to-VESTA coverage.  Selected increment:
  `grid-run --surface-cube` mapped texture controls plus named local
  reactivity routes.  Implementation now adds `local-mulliken-
  electronegativity` and `local-hardness` (`iuserfunc=28/29`), forwards
  `--tex-physical`, `--tex-percent`, `--tex-range-source`, `--surface-band`,
  and `--surface-nearest` from `grid-run` to `cube-preset`, records these
  controls in recipes, and exposes them in the interactive CLI.  Focused
  validation passed with `tests.test_multiwfn_grid tests.test_cli` (121
  tests), full no-GUI validation passed with 332 tests, CLI smokes and
  `git diff --check` passed, read-only subagent review found no blocker, and
  root docs are queued for a final checksum mirror.  Remaining: commit, push,
  and verify branch alignment while preserving untracked `domain.cub` and
  `domain.pdb`.

## Current Request: 2026-06-11 README Refresh And One-Branch Closeout For Local Reactivity Route

- [x] Record user request immediately: update README, inspect the unusual
  branch state, converge back to one maintained branch if needed, and keep
  repository-local Git identity as `Stardust0831`.
- [x] Confirm branch topology and identity before staging.  Current branch is
  `main`; upstream is `origin/main`; `origin/HEAD` points to `origin/main`;
  after `git fetch --prune origin`, `git ls-remote --heads origin` exposes
  only `refs/heads/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.  There is no feature branch that
  needs a real merge-back right now.
- [x] Finish the in-progress local reactivity / mapped texture route on
  `main`: README/usage/skills/research/worklog are synchronized; focused
  `py_compile`, focused 121-test grid/CLI validation, full 332-test no-GUI
  validation, CLI smokes, `git diff --check`, and read-only subagent review
  have passed.  Root docs are queued for final checksum mirror.  Final commit
  hash, push result, and branch verification are reported in the assistant
  response.  Preserve untracked `domain.cub` and `domain.pdb`.

## Current Request: 2026-06-11 README Refresh And One-Branch Closeout For DORI

- [x] Record user request immediately: update README, inspect the unusual
  branch state, converge back to one maintained branch if needed, and keep
  repository-local Git identity as `Stardust0831`.
- [x] Confirm branch topology and identity before staging.  Current branch is
  `main`; `origin/HEAD` points to `origin/main`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.  There is no feature branch that
  needs a real merge-back right now.
- [x] Finish the in-progress DORI route on `main`: README/usage/skills/
  research/worklog are synchronized; validation passed with focused
  `py_compile`, focused `tests.test_cube_preset tests.test_multiwfn_grid`
  with 111 tests, full no-GUI regression with 328 tests, CLI smoke, and
  `git diff --check`; read-only subagent review found no blocker or major
  issue and two documentation minor issues, both handled in this pass.  Root
  docs checksum mirror dry-run is empty.  Final commit hash, push result, and
  branch alignment are reported in the assistant response.  Preserve
  untracked `domain.cub` and `domain.pdb`.

## Active Goal Continuation: 2026-06-11 Next ABACUS-Compatible Visualization Route

- [x] Record automatic continuation of the long-running objective: survey
  valuable Multiwfn wavefunction analyses that can be visualized in VESTA,
  prioritizing routes that ABACUS can feed through LCAO Molden files or
  direct cube outputs.
- [x] Recheck current repository state before choosing the next increment.
  Current branch is `main` at `3e9657a0c65d0585a27d50b014021b8fda7f606f`,
  aligned with `origin/main` and `origin/HEAD`; only local untracked
  `domain.cub` and `domain.pdb` remain and must stay outside commits.
- [x] Re-audit existing `grid-run`/`cube-preset` coverage against local
  Multiwfn source, select one bounded source-backed analysis route or display
  setting that improves ABACUS-to-VESTA wavefunction visualization, then
  implement it with tests, README/usage/skill/research/worklog notes, root
  docs sync, review, commit, push, and branch verification.  Selected
  increment: DORI.  Source evidence: `function.f90` maps `iuserfunc=20` to
  `DORI(x,y,z)`, `0123dim.f90` exports function `100` as `userfunc.cub`,
  weak-interaction post-processing pairs DORI with sign(lambda2)rho, and
  bundled `DORIfill.vmd` uses DORI isosurface `0.95` with sign(lambda2)rho
  texture range `-0.04..0.02`.  Implementation added
  `grid-run --function dori`, `cube-preset dori-scalar`, and
  `cube-preset dori`.  Validation passed with focused `py_compile`,
  focused `tests.test_cube_preset tests.test_multiwfn_grid` with 111 tests,
  full no-GUI regression with 328 tests, CLI smoke, and `git diff --check`;
  review found no blocker or major issue.  Root docs checksum mirror dry-run
  is empty.  Final commit hash and post-push branch verification are reported
  in the assistant response.

## Current Request: 2026-06-11 README Refresh And Branch Consolidation For vdW Probe Route

- [x] Record user request immediately: update README, inspect the unusual
  branch state, converge back to one maintained branch if needed, and keep
  repository-local git identity as `Stardust0831`.
- [x] Confirm current branch and identity before staging anything.  Current
  branch is `main`; repository identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Finish the in-progress `grid-run --function vdw-potential
  --vdw-probe` route, including README/usage/skills/research/worklog notes,
  validation after the latest CLI/test changes, root docs sync, review-agent
  closeout, commit, push, and final branch verification.  Code/docs are
  updated and validation passed: focused `py_compile`,
  `tests.test_multiwfn_grid` with 64 tests,
  `tests.test_multiwfn_grid tests.test_cli` with 116 tests,
  `tests.test_multiwfn_grid tests.test_cube_preset` with 108 tests, full
  no-GUI regression with 325 tests, CLI smoke, and `git diff --check`.
  Root docs checksum mirror dry-run is empty.  Final commit/push and
  post-push branch verification are reported in the assistant response.
- [x] Recheck local/remote branch topology after fetch/prune and keep only
  the maintained `main` branch workflow unless a real remote side branch is
  found.  After `git fetch --prune origin`, local `main`, `origin/main`, and
  `origin/HEAD` are aligned at
  `e1ee45483eefc8cc9961994bb6ab4d2bfe02b26a`; `git ls-remote --heads origin`
  exposes only `refs/heads/main`, so no merge-back is needed.  Preserve local
  untracked probe files `domain.cub` and `domain.pdb` outside the commit.

## Active Goal Continuation: 2026-06-11 Next Wavefunction Analysis Survey

- [x] Record automatic continuation of the long-running objective: survey
  valuable Multiwfn wavefunction analyses that can be visualized in VESTA,
  prioritizing routes fed by ABACUS LCAO Molden files or ABACUS direct cube
  outputs.
- [x] Recheck current repository state, current `grid-run`/`cube-preset`
  coverage, and local Multiwfn source before selecting the next bounded
  feature increment.  Current `main` is aligned with `origin/main` at
  `e1ee45483eefc8cc9961994bb6ab4d2bfe02b26a`, with only local untracked
  `domain.cub` and `domain.pdb` probes plus this kanban update.  `grid-run`
  already covers main-function-5 functions `1-25`, `44`, `100`, `111`, and
  `112`; the next useful increment is run-local control of a source setting
  that changes an existing function's physical meaning.
- [x] Select and implement one source-backed analysis route that moves the
  project closer to broad Multiwfn-to-VESTA coverage, with tests, docs, root
  docs sync, validation, review, commit, push, and branch verification.
  Selected increment: expose `ivdwprobe` for `grid-run --function
  vdw-potential`.  Source evidence: local Multiwfn `settings.ini` defines
  `ivdwprobe=6` as the vdW potential probe atom; `function.f90` reports the
  selected probe in function `25` and `vdwpotfunc` uses it for UFF probe
  parameters; `0123dim.f90` exports `vdWpot.cub` and sets display
  `sur_value=1.0`.  Implementation in progress: default `ivdwprobe=6`,
  `--vdw-probe ELEMENT_OR_Z`, recipe recording, tests, README/usage/skill/
  research/worklog updates.  Validation passed after the final CLI/test
  patch: focused `py_compile`, `tests.test_multiwfn_grid` with 64 tests,
  `tests.test_multiwfn_grid tests.test_cli` with 116 tests, combined
  cube/grid tests with 108 tests, full no-GUI regression with 325 tests, CLI
  smoke, `git diff --check`, and root docs checksum mirror dry-run passed.
  Final commit hash and post-push branch alignment are reported in the
  assistant response to avoid a self-referential hash here.

## Active Goal Continuation: 2026-06-11 Next Wavefunction Visualization Increment

- [x] Record automatic continuation of the long-running objective: keep
  surveying Multiwfn analyses that can become VESTA products, prioritizing
  routes that ABACUS can feed through LCAO Molden files or direct cube
  outputs.
- [x] Recheck current branch and worktree before editing.  Local `main` is
  aligned with `origin/main` at
  `e5f9d7aa1016d2ffb7df5a60b1a63708a0b5008d`; only local untracked probes
  `domain.cub` and `domain.pdb` are present and must remain uncommitted.
- [x] Recheck current `grid-run` and `cube-preset` coverage against local
  Multiwfn source and select one bounded, source-backed next increment.
  Selected increment: expose run-local `ELFLOL_type` control for
  `grid-run --function elf/lol`.  Source evidence: Multiwfn `settings.ini`
  defines `ELFLOL_type=0/1/2/3`; `function.f90` changes function `9/10`
  labels between Becke, Tsirelson, and Tian Lu definitions according to this
  setting; `ELF_LOL` evaluates different formulae; and `0123dim.f90` still
  exports `ELF.cub`/`LOL.cub`.  The implementation should patch a run-local
  settings file and default ordinary `elf`/`lol` to Becke definitions so
  global Multiwfn settings do not silently change output semantics.
- [x] Implement the selected increment with tests, documentation, root docs
  sync, validation, review, commit, push, and branch verification.  The
  implementation and docs are complete; final commit hash and post-push
  branch alignment are reported in the assistant response to avoid a
  self-referential hash here.

## Current Request: 2026-06-11 README Update And Branch Consolidation With ELF/LOL Route

- [x] Record user request immediately: update README, inspect the unusual
  branch state, converge back to one maintained branch if needed, and keep
  git identity as `Stardust0831`.
- [x] Confirm current repository-local identity is already
  `Stardust0831 <13862180016@163.com>`.
- [x] Recheck local/remote branches and decide whether a merge is actually
  needed.  Local `main`, `origin/main`, and `origin/HEAD` are aligned at
  `e5f9d7aa1016d2ffb7df5a60b1a63708a0b5008d`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`, so there is no extra branch to
  merge back right now.
- [x] Preserve local untracked probe files `domain.cub` and `domain.pdb`;
  they are not part of the maintained branch state.
- [x] Finish the current uncommitted ELF/LOL run-local definition-control
  route, update README/usage/skill/research/worklog notes, sync root docs,
  validate, review, commit, push, and verify final one-branch alignment.
  Final pre-commit state: README and docs are updated, root docs checksum
  dry-run is empty, focused `py_compile` passed, `tests.test_multiwfn_grid`
  passed with 60 tests, combined cube/grid tests passed with 104 tests, full
  no-GUI regression passed with 320 tests, CLI smoke passed, and
  `git diff --check` is clean.  Read-only subagent review found one blocker
  (`LOL + d-over-d0`), which was fixed by making D/D0 ELF-only in code,
  docs, and tests.  Final commit hash and post-push branch alignment are
  reported in the assistant response.

## Active Goal Continuation: 2026-06-11 Spin Polarization Survey

- [x] Record automatic continuation of the long-running objective: keep
  surveying and implementing valuable Multiwfn wavefunction analyses for
  VESTA, prioritizing ABACUS LCAO Molden-compatible wavefunction routes.
- [x] Recheck repository state, current spin/grid coverage, and Multiwfn
  source evidence before editing.
- [x] Select whether the next bounded increment should expose Multiwfn's
  spin-polarization parameter route or defer it in favor of another
  ABACUS-compatible analysis.  Selected route: expose Multiwfn function `5`
  spin-polarization parameter as a named route because local `settings.ini`
  shows `ipolarpara=0/1`, `function.f90` changes function `5` display text
  and `fspindens` behavior according to `ipolarpara`, and `0123dim.f90`
  still exports `spindensity.cub`; the implementation should use run-local
  settings so global Multiwfn settings do not change.
- [x] Implement the selected increment with tests, docs, root docs sync,
  validation, review, commit, push, and branch verification.  Implementation,
  focused tests, README/usage/skill/research/worklog documentation, root docs
  sync, full validation, read-only review, commit, push, and final branch
  verification are complete; final commit hash is reported in the assistant
  response.

## Active Goal Continuation: 2026-06-11 Next ABACUS-Compatible Analysis Survey

- [x] Record automatic continuation of the long-running objective: keep
  surveying and implementing valuable Multiwfn wavefunction analyses that can
  become VESTA products, prioritizing ABACUS LCAO Molden-compatible routes
  and ABACUS direct cube products.
- [x] Recheck repository state, current `grid-run`/`cube-preset` coverage,
  and local Multiwfn 2026.6.2 source before selecting the next bounded
  feature increment.  Current worktree started from `main...origin/main`;
  only the new kanban edit plus local untracked `domain.cub`/`domain.pdb`
  were present.  Source review confirmed main-function-5 functions 1-25,
  44, 100, 111, and 112 coverage, and identified `iuserfunc` named analyses
  as the safest next ergonomics gap.
- [x] Select a source-backed analysis route that is useful for VESTA
  visualization and not already maintained.  Selected increment: dedicated
  named routes for high-value Multiwfn `iuserfunc` analyses already confirmed
  in `function.f90`, so `local-electron-affinity`, LEAE, information gain,
  Shannon entropy density, and Fisher information density can imply their
  `iuserfunc` values instead of requiring redundant manual indices.
- [x] Implement the selected route with focused tests and synchronized
  README/usage/research/worklog/skill notes.  Added per-route default
  `iuserfunc` handling for function-100 named analyses while preserving the
  generic `user-function --user-function-index` route; LEA/LEAE named routes
  auto-select mapped presets `lea`/`leae` when `--surface-cube` is supplied.
- [x] Sync root docs mirror, validate, review, and prepare explicit
  commit/push closeout.  Full no-GUI regression passed once with 312
  tests, CLI smoke passed, docs mirror dry-run was empty, and `git diff
  --check` passed.  Read-only subagent review found no blocker and three low
  follow-ups: mention LEA/LEAE in `--surface-cube` help, update mapped-default
  summary docs, and add tests for explicit `iuserfunc` override plus LEA/LEAE
  mapped preset selection; all three follow-ups were patched before final
  validation.  Final validation after those patches passed: focused
  `py_compile`, full 314-test no-GUI regression, `grid-run --list-functions`,
  `grid-run --help`, root docs checksum mirror dry-run, and
  `git diff --check`.  The actual pushed commit was
  `cc56b650b26a9138a93cd6a8386ec6d3c5e52870`
  (`Add named iuserfunc grid routes`), with local `main`, `origin/main`, and
  `origin/HEAD` aligned and only `domain.cub`/`domain.pdb` remaining
  untracked.

## Current Request: 2026-06-11 README Refresh And Branch Consolidation Recheck

- [x] Record user request immediately: update README, recheck the unusual
  branch state, converge back to one maintained branch if needed, and keep
  git identity as `Stardust0831`.
- [x] Audit current local/remote branch state and repository-local git
  identity before staging anything.
- [x] Refresh README and synchronized docs if the current branch state or CLI
  workflow needs clearer closeout text.
- [x] Validate and prepare an explicit closeout plan while preserving local
  untracked probe files.  Audit result before staging: after
  `git fetch --prune origin`, local `main`, `origin/main`, and `origin/HEAD`
  were aligned at `e1b3f866694e89d781f5722f0a4d18ca603c69ff`; remote heads
  exposed only `refs/heads/main`; repository-local identity was
  `Stardust0831 <13862180016@163.com>`.  Validation passed before staging:
  focused `py_compile`, full 311-test no-GUI regression, `grid-run
  --list-functions`, `cube-preset --list-presets`, `grid-run --help`,
  `bin/multiwfn2vesta --help`, root docs checksum mirror dry-run, and
  `git diff --check`; read-only subagent review found one documentation
  status problem about premature commit/push wording, fixed in this update.
- [x] Stage only intended tracked files, commit/push the real update, and
  verify `main`/`origin/main` alignment.  Final commit hash and post-push
  branch alignment were reported in the assistant response; the actual
  pushed commit was `0e587a076b136ad86fdba81fbd51939dc56f99d1`
  (`Add user-function grid preset`), with local `main`, `origin/main`, and
  `origin/HEAD` aligned and only `domain.cub`/`domain.pdb` remaining
  untracked.

## Active Goal Continuation: 2026-06-11 User-Function Grid Route

- [x] Record automatic continuation of the long-running objective: survey and
  implement valuable Multiwfn wavefunction analyses that can be visualized in
  VESTA, prioritizing analyses ABACUS can feed through LCAO Molden files or
  direct cube outputs.
- [x] Recheck current repository state, Multiwfn source evidence, and existing
  `grid-run`/`cube-preset` coverage before editing.  Source evidence:
  `settings.ini` defines `iuserfunc`, main menu `1000 -> 2` can set it,
  `function.f90` evaluates `userfunc(x,y,z)`, and `0123dim.f90` exports
  `userfunc.cub`.
- [x] Implement a maintained Multiwfn main-function-5 `ifuncsel=100`
  user-defined function route using run-local `iuserfunc` settings, with
  conservative exclusions for special external-grid modes.  Added
  `grid-run --function user-function --user-function-index IUSERFUNC`,
  `cube-preset user-function`, recipe fields, CLI help, and batch-mode
  rejection for non-orbital user-function options.
- [x] Add focused tests, README/usage/research/skill documentation, and
  worklog/skill notes.  Focused validation already passed for `py_compile`
  and 95 cube/grid tests; root docs mirror sync remains for final validation.
- [x] Validate, review, and prepare branch closeout on `main`;
  keep `domain.cub` and `domain.pdb` untracked.  Validation passed before
  review: focused `py_compile`, 95 focused cube/grid tests, full 311-test
  no-GUI regression, `grid-run --list-functions`, `cube-preset
  --list-presets`, `grid-run --help`, root docs checksum mirror dry-run, and
  `git diff --check`.  Pre-commit subagent review found no blocking issue and
  two low documentation mismatches; both were fixed by clarifying cube-preset
  versus grid-run aliases and batch-mode rejection docs.  Final validation
  passed again after the README branch refresh: focused `py_compile`, full
  311-test no-GUI regression, CLI smoke checks, root docs mirror dry-run, and
  `git diff --check`.  The final commit/push result is reported by the
  assistant response after it actually happens.

## Current Request: 2026-06-11 README Refresh And Main Branch Consolidation

- [x] Record user request: update README, inspect unusual branch state,
  consolidate back to one maintained branch if needed, and keep Git identity
  as `Stardust0831`.
- [x] Confirm repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Recheck branch state after `git fetch --prune origin`: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `13e657fb700cc8d4bbb4c126434d6762d0f4d5f5`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`.
- [x] Decide merge action: no merge-back is needed because there is no extra
  local or remote feature branch to consolidate.
- [x] Refresh README branch-status text to the current single-branch state
  and keep the pair-function closeout on `main`.
- [x] Sync root docs mirror and validate the documentation-only change.
  Passed checks: root docs checksum mirror dry-run, `git diff --check`,
  `bin/multiwfn2vesta --help`, remote-head audit, git identity audit, and
  read-only subagent review with no blocking issue.
- [x] Prepare explicit staging/commit/push closeout.  Final commit hash and
  post-push branch alignment are reported in the assistant response to avoid
  a self-referential docs loop; keep `domain.cub` and `domain.pdb` untracked.

## Active Goal Continuation: 2026-06-11 Next ABACUS-Compatible Wavefunction Visualization Increment

- [x] Record automatic continuation of the long-running objective: keep
  researching and implementing valuable Multiwfn wavefunction analyses that
  can become VESTA products, prioritizing workflows fed by ABACUS LCAO
  Molden files or direct ABACUS cube outputs.
- [x] Recheck current repository state before new edits: local `main` and
  `origin/main` are aligned at
  `c879f30c62e8361b6636f88504abed30bdce75b1`; local untracked probes
  `domain.cub` and `domain.pdb` remain outside version control.
- [x] Inspect current `grid-run`/`cube-preset` coverage and local Multiwfn
  2026.6.2 source for the next bounded, source-backed increment.
- [x] Selected increment: Multiwfn function `17` pair/correlation function.
  Source evidence: `function.f90` calls
  `pairfunc(refx,refy,refz,x,y,z)`, `settings.ini` controls the physical
  quantity through `pairfunctype`/`paircorrtype`, and `0123dim.f90` exports
  `fermihole.cub`.
- [x] Implement `grid-run --function pair-function` plus
  `cube-preset pair-function`, using `--reference-point`,
  `--reference-unit`, `--pair-function-type`, and
  `--pair-correlation-type`; preserve global Multiwfn settings by copying
  the selected `settings.ini` when available and patching a run-local
  `multiwfn_grid_settings.ini`.
- [x] Focused validation passed during implementation: `py_compile` for
  edited modules/tests and 90 tests across `tests.test_cube_preset` and
  `tests.test_multiwfn_grid`.
- [x] Finish README/usage/skills/research docs sync for the selected
  increment.
- [x] Sync root docs mirror and validate.  Passed checks: focused
  `py_compile`, 90 focused cube/grid tests, full 306-test no-GUI regression,
  `cube-preset --list-presets`, `grid-run --list-functions`,
  `grid-run --help`, `bin/multiwfn2vesta --help`, docs mirror dry-run,
  stale pair-function wording scan, and `git diff --check`.
- [x] Complete pre-commit review.  The delegated read-only subagent response
  was unrelated and not used as evidence; local review found no blocking
  issue in branch-status text, function-17 command stream, run-local
  settings handling, CLI validation, docs sync, or untracked probe handling.
- [x] Commit, push, and verify branch alignment for the pair-function feature:
  `13e657fb700cc8d4bbb4c126434d6762d0f4d5f5` is on local `main`,
  `origin/main`, and `origin/HEAD`; keep `domain.cub` and `domain.pdb`
  untracked.

## Current Request: 2026-06-10 README Refresh, Branch Check, Source Function Closeout

- [x] Record user request: update README, inspect unusual-looking branch
  state, converge back to one maintained branch if needed, and keep git
  identity as `Stardust0831`.
- [x] Confirm repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Recheck branch state after `git fetch --prune origin`: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `49a350619601fdff76c0e993b55b2c9c26024ccc`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`.
- [x] Decide merge action: no merge-back is needed because there is no extra
  local branch or remote feature branch to consolidate.
- [x] Refresh README branch-status text to the current single-branch state.
- [x] Preserve local untracked probes `domain.cub` and `domain.pdb` outside
  version control.
- [x] Run validation before review: focused `py_compile`; full
  `python3 -m unittest discover -s tests -v` with 302 tests; `cube-preset
  --list-presets`; `grid-run --list-functions`; `grid-run --help`;
  `bin/multiwfn2vesta --help`; and `git diff --check`.
- [x] Complete read-only subagent review.  No commit-blocking issue was
  found; the only non-blocking caveat was that a minimal `-set` file may
  bypass user-customized Multiwfn settings, so the implementation now copies
  and patches a base `settings.ini` when available.
- [x] Patch source-function settings generation to preserve base Multiwfn
  settings when possible.
- [x] Re-run validation after the settings-file patch: focused
  `py_compile`, 86 focused tests across `tests.test_cube_preset` and
  `tests.test_multiwfn_grid`, full 302-test no-GUI regression,
  `cube-preset --list-presets`, `grid-run --list-functions`,
  `grid-run --help`, `bin/multiwfn2vesta --help`, stale settings-wording
  scan, and `git diff --check`.
- [x] Complete final read-only review.  No commit-blocking issue was found;
  the only low item was this historical caveat wording, now cleaned up.
- [x] Prepare explicit staging/commit/push closeout.  Final commit hash and
  post-push branch alignment are reported in the assistant response to avoid
  a self-referential docs loop.

## Active Goal Continuation: 2026-06-10 Reference-Point Grid Function Resume

- [x] Record automatic continuation of the long-running objective: research
  and implement valuable Multiwfn wavefunction/grid analyses that can become
  VESTA products, especially workflows fed by ABACUS LCAO Molden files or
  direct ABACUS cube outputs.
- [x] Keep the previous README/branch closeout separated from this feature
  work: `main`, `origin/main`, and `origin/HEAD` were aligned at
  `49a350619601fdff76c0e993b55b2c9c26024ccc` after that documentation
  commit; local `domain.cub` and `domain.pdb` probes remain outside version
  control.
- [x] Inspect local Multiwfn 2026.6.2 source for reference-point dependent
  main-function-5 grid functions and choose the next bounded increment.
- [x] Implement the selected increment with focused tests and documentation,
  preserving existing standalone-cube, mapped-surface, and fragment-route
  separation.
- [x] Selected increment: Multiwfn function `19` source function.  Source
  evidence: `function.f90` calls `srcfunc(x,y,z,srcfuncmode)`, `srcfunc`
  depends on global `refx,refy,refz`, `0123dim.f90` exports `srcfunc.cub`,
  and main menu `1000 -> 1` sets the reference point.  Implementation uses
  run-local `multiwfn_grid_settings.ini` with `-set` for `srcfuncmode` and
  does not edit global Multiwfn settings.
- [x] Focused validation passed before full regression: `py_compile` for the
  edited modules/tests and `tests.test_cube_preset tests.test_multiwfn_grid`
  with 86 tests.
- [x] Validate implementation and CLI help before review.
- [x] Address subagent settings-file caveat by copying the selected
  Multiwfn `settings.ini` when available, patching `srcfuncmode` into a
  run-local `multiwfn_grid_settings.ini`, and keeping global settings
  untouched.
- [x] Re-run validation after the settings-file patch: focused
  `py_compile`, 86 focused tests across `tests.test_cube_preset` and
  `tests.test_multiwfn_grid`, full 302-test no-GUI regression, CLI smoke
  checks, stale settings-wording scan, and `git diff --check`.
- [x] Complete final read-only review.  No commit-blocking issue was found;
  the only low item was stale historical caveat wording in the kanban, now
  cleaned up.
- [x] Prepare explicit staging/commit/push closeout; keep `domain.cub` and
  `domain.pdb` untracked.  Final commit hash and post-push branch alignment
  are reported in the assistant response to avoid a self-referential docs
  loop.

## Current Request: 2026-06-10 README Refresh And Main Branch Consolidation At Delta-g Tip

- [x] Record user request before editing: update README, inspect the
  unusual-looking branch state, merge/converge back to one maintained branch
  if needed, and keep git identity as `Stardust0831`.
- [x] Confirm repository-local git identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Recheck current branch state after `git fetch --prune origin`: local
  `main`, `origin/main`, and `origin/HEAD` are aligned at
  `028a7caae9af6f10de3fa1639ce6fce6f136787d`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`.
- [x] Decide whether a merge-back is needed: no merge is needed because
  there is no extra local branch or remote feature branch to consolidate.
- [x] Refresh README and worklog with the current single-branch state,
  branch audit, git identity, and untracked probe-file handling.
- [x] Sync root docs mirror, validate, and complete read-only review before
  explicit staging.  Validation passed: root docs checksum mirror dry-run,
  `bin/multiwfn2vesta --help`, and `git diff --check`.  Review found no
  High/Medium/Low blocker and confirmed the README/worklog/kanban branch
  state is consistent, only `main` is exposed by the remote, and local
  `domain.cub`/`domain.pdb` probes remain untracked.  Final commit hash and
  post-push alignment are reported in the assistant response to avoid a
  self-referential docs loop.

## Active Goal Continuation: 2026-06-10 Next Reference-Point Grid Increment

- [x] Record automatic continuation of the long-running objective: keep
  enriching Multiwfn wavefunction analyses that can become VESTA products,
  prioritizing workflows fed by ABACUS LCAO Molden files or direct cube
  outputs.
- [x] Recheck current repository state before new edits: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `028a7caae9af6f10de3fa1639ce6fce6f136787d`; only local untracked probes
  `domain.cub` and `domain.pdb` remain outside version control.
- [ ] Deferred during the README/branch closeout so this pass remains a
  documentation-only maintenance update.
- [ ] Inspect local Multiwfn 2026.6.2 source for the next bounded,
  source-backed reference-point or real-space function increment.
- [ ] Implement the selected increment with focused tests and documentation,
  preserving existing standalone-cube, mapped-surface, and fragment-route
  separation.
- [ ] Sync root docs mirror, validate, review, commit, push, and verify
  branch alignment; keep `domain.cub` and `domain.pdb` untracked.

## Active Goal Continuation: 2026-06-10 Hirshfeld Delta-g And README Closeout

- [x] Record automatic continuation of the long-running objective: keep
  researching and implementing valuable Multiwfn wavefunction analyses that
  can be visualized in VESTA, prioritizing routes that ABACUS can feed via
  LCAO Molden wavefunction files or direct cube outputs.
- [x] Record user request: update README, inspect the unusual-looking branch
  state, converge back to one maintained branch if needed, and keep git
  identity as `Stardust0831`.
- [x] Recheck current repository state before new edits: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `9169e611a3ea3818b7f65d90ade6e45518322bde`; remote-visible branch state is
  only `refs/heads/main`, so no branch merge is needed; local untracked
  probes `domain.cub` and `domain.pdb` remain outside version control.
- [x] Inspect current `grid-run`/`cube-preset` coverage, local Multiwfn
  2026.6.2 source, and the analysis matrix.  Selected increment: Multiwfn
  main-function-5 function `23`, Delta-g with Hirshfeld partition, because
  `function.f90` calls `delta_g_Hirsh` and `0123dim.f90` leaves its cube
  export at generic `griddata.cub`.
- [x] Implement `cube-preset hirshfeld-delta-g` plus
  `grid-run --function hirshfeld-delta-g`, keeping function `22`
  `delta-g` aliases mapped to promolecular `Delta_g.cub` and keeping
  IGM/IGMH fragment `dg_inter.cub` mapped-surface routes separate.
- [x] Update focused tests, README, usage docs, skills, research matrix, and
  worklog with the `griddata.cub` raw-output behavior and single-branch
  closeout status.
- [x] Sync root docs mirror and validate before review.  Validation passed:
  root docs checksum mirror dry-run, focused `py_compile`, 81 focused tests
  across `tests.test_cube_preset` and `tests.test_multiwfn_grid`,
  `cube-preset --list-presets`, `grid-run --list-functions`,
  `grid-run --help`, `bin/multiwfn2vesta --help`, `git diff --check`, and
  full 297-test no-GUI regression.
- [x] Complete read-only review and prepare explicit staging/commit/push
  closeout; keep `domain.cub` and `domain.pdb` untracked.  Review found no
  High/Medium blocker and confirmed README branch status, function `22`
  promolecular `Delta_g.cub` separation, function `23` generic
  `griddata.cub` handling, docs/skills/worklog/kanban sync, and root docs
  mirror sync.  The only Low finding is to avoid `git add .` / `git add -A`
  because `domain.cub` and `domain.pdb` are local probes.  Final commit hash
  and post-push branch alignment are reported in the assistant response to
  avoid a self-referential docs loop.

## Active Goal Continuation: 2026-06-10 Hirshfeld Weight Grid Cube

- [x] Record automatic continuation of the long-running objective: keep
  researching and implementing valuable Multiwfn wavefunction/grid analyses
  that can become VESTA products, with priority on ABACUS LCAO
  Molden-compatible routes.
- [x] Recheck current repository state: local `main`, `origin/main`, and
  `origin/HEAD` are aligned at
  `e68ace19a4d2b155d8817cb3094dc9bba065ecb8`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`; only local untracked probes
  `domain.cub` and `domain.pdb` remain outside version control.
- [x] Inspect local Multiwfn 2026.6.2 source for the next bounded feature:
  main-function-5 function `112` asks for a Hirshfeld atom selection string,
  then asks how to generate atomic densities; choosing `2` uses built-in
  atomic densities and exports `Hirshfeld.cub`.
- [x] Implement `cube-preset hirshfeld-weight` and
  `grid-run --function hirshfeld-weight --hirshfeld-atoms ATOMS`, initially
  supporting the bounded built-in atomic-density mode.
- [x] Update tests, README, usage docs, skills, research matrix, and worklog.
- [x] Sync root docs mirror, validate, review, commit, push, and verify
  `main` remains aligned with `origin/main`; keep `domain.cub` and
  `domain.pdb` untracked.  Validation passed before commit: root docs
  checksum mirror dry-run, focused `py_compile`, 78 focused tests across
  `tests.test_cube_preset` and `tests.test_multiwfn_grid`, full 294-test
  no-GUI regression, `cube-preset --list-presets`,
  `grid-run --list-functions`, `grid-run --help`,
  `bin/multiwfn2vesta --help`, and `git diff --check`.  Read-only review
  found no High/Medium blocker and confirmed function `112` uses the
  `5,112,<selection>,2,<grid setup>,2,0,q` built-in-density command stream.
  Final commit hash and post-push branch alignment are reported in the
  assistant response to avoid a self-referential docs loop.

## Current Request: 2026-06-10 README Refresh And Single-Branch Closeout

- [x] Record user request before final edits: update README, check the
  unusual-looking branch state, converge to one maintained branch if needed,
  and keep git identity as `Stardust0831`.
- [x] Confirm current branch state: local `main`, `origin/main`, and
  `origin/HEAD` are aligned at
  `e68ace19a4d2b155d8817cb3094dc9bba065ecb8`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`; no extra branch needs merging.
- [x] Refresh README and docs with the current single-branch status plus the
  new Hirshfeld weight grid/preset workflow.
- [x] Sync root docs mirror, run validation, perform read-only review, commit
  and push to `origin/main`, then verify final branch alignment.  Validation
  passed before commit: root docs checksum mirror dry-run, focused
  `py_compile`, 78 focused tests, full 294-test no-GUI regression,
  `cube-preset --list-presets`, `grid-run --list-functions`,
  `grid-run --help`, `bin/multiwfn2vesta --help`, and `git diff --check`.
  Read-only review found no High/Medium blocker.  Final commit hash and
  post-push branch alignment are reported in the assistant response.

## Current Request: 2026-06-10 README Refresh And Branch Consolidation At Becke Tip

- [x] Record user request before editing: update README, inspect the
  unusual-looking branch state, merge/converge back to one maintained branch
  if needed, and keep git identity as `Stardust0831`.
- [x] Confirm the actual maintained repository for this workspace is
  `/mnt/g/work/multiwfn2vesta/project`; the workspace-level
  `/mnt/g/work/multiwfn2vesta/.git` is an empty metadata stub and is not the
  GitHub project checkout used for commits.
- [x] Recheck branch and identity state without destructive operations:
  after `git fetch --prune origin`, local `main`, `origin/main`, and
  `origin/HEAD` are aligned at
  `27065d0bf4b5f4096044065cd76a4eaa52735704`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Decide whether a branch merge is needed: no merge is needed because no
  extra local or remote feature branch exists; this closeout should stay on
  maintained `main`.
- [x] Refresh README and project docs with the current branch audit,
  one-branch policy, working checkout path, and untracked probe-file handling.
- [x] Sync root docs mirror, validate, review, commit, push, and verify
  `main` remains aligned with `origin/main`; keep `domain.cub` and
  `domain.pdb` untracked.  Validation passed before commit: root docs
  checksum mirror dry-run, `git diff --check`, and `bin/multiwfn2vesta
  --help`.  Final commit hash and post-push branch alignment are reported in
  the assistant response to avoid a self-referential docs loop.

## Active Goal Continuation: 2026-06-10 Next ABACUS-Molden Multiwfn Analysis

- [x] Record automatic continuation of the long-running objective: keep
  researching and implementing valuable Multiwfn wavefunction analyses that
  can become VESTA products, with priority on ABACUS LCAO Molden-compatible
  routes.
- [x] Re-inspect current `grid-run`/`cube-preset` coverage, local Multiwfn
  2026.6.2 source exports, and the research matrix for the next bounded
  source-backed increment.  Selected increment: Multiwfn main-function-5
  function `111` Becke atomic/overlap weight, because local source
  `0123dim.f90` prompts for atom indices before grid setup and exports
  `Becke.cub`; it is compatible with ABACUS LCAO Molden wavefunctions.
- [x] Implement `cube-preset becke-weight` plus `grid-run --function
  becke-weight --becke-atoms I J`, where `J=0` means Becke atomic weight and
  `I,J` means Becke overlap weight.
- [x] Update tests, README, usage docs, skills, research matrix, and worklog.
- [x] Implement the selected increment with tests and documentation while
  preserving existing mapped-surface and standalone-cube route separation.
  Focused validation passed: `py_compile` for changed modules/tests, 75
  focused tests across `tests.test_cube_preset tests.test_multiwfn_grid`, and
  `bin/multiwfn2vesta grid-run --help`.
- [x] Sync root docs mirror, validate, review, commit, push, and verify
  `main` remains aligned with `origin/main`; keep `domain.cub` and
  `domain.pdb` untracked.  Validation passed before commit: root docs
  checksum mirror dry-run, full 291-test no-GUI regression,
  `cube-preset --list-presets`, `grid-run --list-functions`,
  `grid-run --help`, `bin/multiwfn2vesta --help`, and `git diff --check`.
  Read-only review found no High blocker; the Medium reminder is to keep
  untracked `domain.cub` and `domain.pdb` out of staging.  Final commit hash
  and post-push branch alignment are reported in the assistant response.

## Active Goal Continuation: 2026-06-10 Next Multiwfn VESTA Analysis Gap

- [x] Record automatic continuation of the long-running objective: keep
  researching valuable Multiwfn wavefunction/grid analyses that can be
  visualized in VESTA, especially workflows that ABACUS can feed through
  LCAO Molden or direct cube outputs.
- [x] Inspect the current implemented coverage, local Multiwfn 2026.6.2
  source, and research matrix to choose the next source-backed, bounded
  feature increment.
- [x] Implement the selected increment with tests and documentation, keeping
  standalone single-cube routes separate from mapped surface/texture routes.
- [x] Sync root docs mirror, validate, review, commit, push, and verify
  `main` remains aligned with `origin/main`.

## Active Implementation: 2026-06-10 EDR and Orbital-Overlap Distance

- [x] Record user request: update README, inspect unusual branch state,
  merge/consolidate back to one branch where appropriate, and use identity
  `Stardust0831`.
- [x] Inspect current branch/remote/status without disturbing existing work:
  local `main`, `origin/main`, and `origin/HEAD` are aligned at
  `6de6b017d8fa8b66cde24731ca5403081201a0b4`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`; no extra branch needs merging.
- [x] Preserve local probes: `domain.cub` and `domain.pdb` remain untracked
  and must not be staged unless explicitly promoted later.
- [x] Select this bounded increment: Multiwfn 2026.6.2 source shows function
  `20` EDR(r;d) asks for length scale `d` in Bohr and exports `EDR.cub`;
  function `21` D(r) accepts default or manual EDR exponent parameters and
  exports `EDRDmax.cub`; both keep the global main-function-5
  `sur_value=0.05`.
- [x] Add `cube-preset electron-delocalization-range` and
  `cube-preset orbital-overlap-distance`.
- [x] Add `grid-run --function edr --edr-length D_BOHR` and
  `grid-run --function edrdmax [--edr-exponents COUNT START INCREMENT]`,
  including command-stream validation and recipe fields.
- [x] Update focused tests, README, usage docs, skills, research matrix, and
  worklog.
- [x] Sync root docs mirror, run full validation, collect read-only review,
  commit, push, and verify `main`/`origin/main` alignment.  Validation
  passed: focused `py_compile`, 72 focused tests across
  `tests.test_cube_preset tests.test_multiwfn_grid`, full 288-test no-GUI
  regression, `cube-preset --list-presets`, `grid-run --list-functions`,
  `grid-run --help`, `bin/multiwfn2vesta --help`, root-docs checksum
  mirror, and `git diff --check`.  Read-only review found no High blocker;
  the two Medium workflow notes were addressed by excluding `domain.cub` /
  `domain.pdb` from staging and syncing the root docs mirror.

## Active Implementation: 2026-06-10 Standalone vdW Potential Cube Preset

- [x] Record continuation request: keep enriching useful Multiwfn
  wavefunction/grid analyses that can be visualized in VESTA, especially
  workflows that ABACUS can feed through Molden or direct cube routes.
- [x] Record current user request: refresh README, audit the unusual-looking
  branch state, converge to one maintained branch if needed, and keep git
  identity as `Stardust0831 <13862180016@163.com>`.
- [x] Recheck current state: local `main` is aligned with `origin/main` at
  `fae7ac12d9a6d1fadbeda7a60c484752a643c23f`; untracked local probes
  `domain.cub` and `domain.pdb` remain uncommitted.
- [x] Recheck branch and identity state: local `main`, `origin/main`, and
  `origin/HEAD` are aligned at
  `fae7ac12d9a6d1fadbeda7a60c484752a643c23f`; `origin` points to
  `Github:Stardust0831/multiwfn2vesta.git`; remote-visible branch state is
  one maintained `main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Select this bounded increment: Multiwfn `function.f90` lists function
  `25` as van der Waals potential, `0123dim.f90` exports `vdWpot.cub`, and
  the export block sets `sur_value=1D0`; the project currently routes
  standalone `grid-run --function vdw-potential` through generic `signed`
  while only the `--surface-cube` route uses `vdw-map`.
- [x] Add a dedicated standalone `cube-preset vdw-potential` and map
  `grid-run --function vdw-potential` to it without changing `vdw-map`.
- [x] Update focused tests, README, usage docs, skills, research matrix, and
  worklog.
- [x] Sync root docs mirror, validate, and review: focused `py_compile`, 66
  focused tests across `tests.test_cube_preset tests.test_multiwfn_grid`,
  full 282-test no-GUI regression, `cube-preset --list-presets`,
  `grid-run --list-functions`, `bin/multiwfn2vesta --help`,
  root-docs checksum mirror, and `git diff --check` passed; read-only review
  found no High/Medium blocker and confirmed standalone `vdw-potential` plus
  mapped `vdw-map` routes stay separate.
- [x] Prepare explicit staging, commit, push, and post-push verification with
  `Stardust0831` identity.  Final commit hash and branch-alignment check are
  reported in the assistant response to avoid a self-referential docs loop.

## Active Implementation: 2026-06-10 Promolecular Delta-g Cube Preset

- [x] Record continuation request: keep enriching useful Multiwfn
  wavefunction/grid analyses that can be visualized in VESTA, especially
  workflows that ABACUS can feed through Molden or direct cube routes.
- [x] Recheck current state after README branch closeout: local `main` is
  aligned with `origin/main` at
  `4af3bec35b85fb9a5d1b49ab6770361de528ce16`; untracked local probes
  `domain.cub` and `domain.pdb` remain uncommitted.
- [x] Select this bounded increment: implement a dedicated VESTA preset for
  Multiwfn function `22` promolecular `Delta_g.cub`, keeping it separate
  from IGM/IGMH fragment `dg_inter.cub` mapped-surface routes.
- [x] Update source and focused tests for `cube-preset
  promolecular-delta-g` and `grid-run --function delta-g`.
- [x] Update README, usage docs, skills, research matrix, and worklog with
  the standalone `Delta_g.cub` route and the distinction from IGM/IGMH
  `dg_inter.cub`.
- [x] Sync root docs mirror.
- [x] Validate and review: focused `py_compile`, 63 focused tests across
  `tests.test_cube_preset tests.test_multiwfn_grid`, full 279-test no-GUI
  regression, `cube-preset --list-presets`, `grid-run --list-functions`,
  `bin/multiwfn2vesta --help`, and `git diff --check` passed; read-only
  review found no source/test blocker and confirmed IGM/IGMH plus IRI/RDG
  texture routes are not overwritten.
- [x] Prepare explicit staging, commit, push, and post-push verification with
  `Stardust0831` identity.  Final commit hash and branch-alignment check are
  reported in the assistant response to avoid a self-referential docs loop.

## Current Request: 2026-06-10 README Refresh And One-Branch Closeout

- [x] Record user request before editing: update README, inspect the
  unusual-looking branch state, merge or converge back to one maintained
  branch if needed, and use `Stardust0831` identity for git work.
- [x] Recheck branch and identity state without destructive operations:
  after `git fetch --prune origin`, local `main`, `origin/main`, and
  `origin/HEAD` are aligned at
  `764382c01698111f9d8b41932759a480233a272b`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Decide whether a branch merge is needed: no merge is needed in this
  pass because there is no extra local branch or remote feature branch to
  consolidate.
- [x] Refresh README and project docs so the current branch audit, single
  maintained `main` branch policy, and untracked local probe-file handling are
  explicit.
- [x] Sync root docs mirror, validate, and run read-only review: root docs
  mirror dry-run is clean; `git diff --check` and
  `bin/multiwfn2vesta --help` passed; the reviewer found no branch-status
  blocker and confirmed Promolecular Delta-g remains unfinished.
- [x] Prepare explicit staging, commit, push, and post-push verification with
  `Stardust0831` identity.  Final commit hash and branch-alignment check are
  reported in the assistant response to avoid a self-referential docs loop.

## Active Goal Continuation: 2026-06-10 Promolecular Delta-g Cube

- [x] Record continuation objective: keep expanding useful Multiwfn
  wavefunction/grid analyses that can become VESTA products, especially
  analyses ABACUS can feed through LCAO Molden or direct cube routes.
- [x] Recheck current state: local `main` is aligned with `origin/main` at
  `764382c01698111f9d8b41932759a480233a272b`; untracked local probes
  `domain.cub` and `domain.pdb` remain uncommitted.
- [x] Choose the next source-backed stable gap: Multiwfn 2026.6.2
  `function.f90` lists function `22` as Delta-g with promolecular
  approximation and `0123dim.f90` exports it as `Delta_g.cub`; at selection
  time, the project still routed `grid-run --function delta-g` through
  generic `density`.
- [x] Recheck source/template defaults, then add a maintained `cube-preset`
  and `grid-run` mapping for promolecular `Delta_g.cub` without changing
  IGM/IGMH fragment `dg_inter.cub` mapped-surface routes.
- [x] Sync root docs for the active implementation.
- [x] Validate, review, commit, push, and verify `main`
  remains aligned with `origin/main`; this is being completed by the active
  implementation section above, with final commit hash reported in the
  assistant response.

## Active Goal Continuation: 2026-06-10 Local Information Entropy Cube

- [x] Record continuation objective: keep expanding useful Multiwfn
  wavefunction analyses that can become VESTA products, especially analyses
  ABACUS can feed through LCAO Molden or direct cube routes.
- [x] Recheck current state: local `main` is aligned with `origin/main` at
  `287974cdd66db52b8f0f3581b63537d221980da1`; untracked local probes
  `domain.cub` and `domain.pdb` remain uncommitted.
- [x] Inspect current source-backed grid-function gaps: Multiwfn 2026.6.2
  `function.f90` lists function `11` as local information entropy and
  `0123dim.f90` exports it as `infoentro.cub`; reference-point and EDR
  routes were deferred at that time because they needed reference points or
  extra EDR parameters.  EDR/D(r) was later implemented in the 2026-06-10 EDR
  and orbital-overlap distance increment above; source function was later
  implemented in the 2026-06-10 source-function increment; pair/correlation
  functions were later implemented in the 2026-06-11 pair-function increment.
- [x] Add a maintained `cube-preset` and `grid-run` mapping for
  `infoentro.cub`, with focused tests and docs: implemented
  `cube-preset local-information-entropy`, mapped `grid-run --function
  information-entropy` to Multiwfn function `11`, documented the source
  evidence, and focused `py_compile` plus
  `tests.test_cube_preset tests.test_multiwfn_grid` passed with 61 tests.
- [x] Sync root docs, validate, review, then prepare commit/push on `main`:
  focused `py_compile`, 61 focused tests, full 277-test no-GUI regression,
  `cube-preset --list-presets`, `grid-run --list-functions`,
  `bin/multiwfn2vesta --help`, and `git diff --check` passed.  Commit/push
  and post-push branch verification are reported in the assistant response to
  avoid a self-referential hash loop.

## Current Request: 2026-06-10 README Refresh And Main Branch Closeout

- [x] Record user request: update README, inspect the unusual-looking branch
  state, merge back to one maintained branch if needed, and use
  `Stardust0831` identity.
- [x] Inspect branch and identity state without destructive operations:
  local `main`, `origin/main`, and `origin/HEAD` are aligned at
  `34b2b012ced5dd474874fecc55f74ac17e0c4caa`; `origin` points to
  `Github:Stardust0831/multiwfn2vesta.git`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Decide whether a branch merge is needed: no merge is needed because
  local and remote expose only the maintained `main` branch.
- [x] Refresh README repository-status wording to the current branch-audit
  baseline and keep the active IRI scalar increment on the same `main`
  branch.
- [x] Sync root docs, validate, review, then prepare commit/push on `main`:
  root docs mirror is clean; focused `py_compile`, 59 focused tests, full
  275-test no-GUI regression, `cube-preset --list-presets`,
  `grid-run --list-functions`, `bin/multiwfn2vesta --help`, remote-head
  audit, and `git diff --check` passed.  Commit/push and post-push branch
  verification are reported in the assistant response to avoid a
  self-referential hash loop.

## Current Continuation: 2026-06-10 IRI Scalar Cube Display

- [x] Record resumed objective: keep expanding maintained VESTA-ready
  Multiwfn/ABACUS wavefunction and cube analyses, prioritizing products that
  ABACUS can feed through Molden or direct cube routes.
- [x] Recheck current state: `main` is aligned with `origin/main` at
  `34b2b012ced5dd474874fecc55f74ac17e0c4caa`; untracked local probes
  `domain.cub` and `domain.pdb` remain uncommitted.
- [x] Inspect current `grid-run` and `cube-preset` coverage for real-space
  function `24` IRI scalar cubes: `grid-run` already generates `IRI.cub` but
  routes it through generic `density`; Multiwfn 2026.6.2 `0123dim.f90`
  confirms function `24` exports `IRI.cub` and sets `sur_value=1D0`.
- [x] Implement a standalone `iri-scalar` preset and map `grid-run
  --function iri` to it without changing the existing two-cube
  `cube-preset iri` / `rdg` texture route; focused `py_compile` and
  `tests.test_cube_preset tests.test_multiwfn_grid` currently pass with 59
  tests.
- [x] Sync root docs, validate, review, then prepare commit/push on `main`:
  root docs mirror is clean; focused and full no-GUI tests passed; CLI
  preset/function listings show `iri-scalar`; main-thread diff review found
  no blocker.  Commit/push and post-push verification are reported in the
  assistant response.

## Current Request: 2026-06-10 README Refresh At Spin-Density Tip

- [x] Record user request: update README, inspect the unusual-looking branch
  state, consolidate back to one maintained branch if needed, and use the
  `Stardust0831` git identity.
- [x] Inspect local/remote branches and repository identity without touching
  unrelated local probes: local `main`, `origin/main`, and `origin/HEAD` are
  aligned at `1a8bbc63cc785ec07b4b177078909971b8ac127b`
  (`Add spin-density cube arithmetic`); `git ls-remote --heads origin`
  exposes only `refs/heads/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Decide whether a branch merge is needed: no merge is needed because
  there is no extra local branch or remote feature branch to consolidate.
- [x] Refresh README repository-status wording so the single-branch state,
  SSH remote, commit identity, and branch-audit baseline are current.
- [x] Sync root docs mirror, validate the docs-only refresh, and run a
  read-only review: root docs mirror is clean; `git diff --check` and
  `bin/multiwfn2vesta --help` passed; read-only subagent review found no
  blocker.  Commit/push and post-push branch verification are reported in the
  assistant response to avoid another self-referential hash loop.

## Current Request: 2026-06-10 README Refresh And Branch Convergence

- [x] Record user request: update README, inspect the unusual branch state,
  converge the maintained work back to a single branch if needed, and use
  `Stardust0831` identity for commits.
- [x] Inspect local/remote branches, repository identity, and current
  uncommitted work without touching unrelated local probes: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `77c134e2d7cd844e6cc9c4dce59f316a90700192`; `origin` exposes only
  `refs/heads/main`; untracked `domain.cub` and `domain.pdb` remain local
  probes and must stay uncommitted.
- [x] Refresh README so current usage, maintained CLI entry points, docs
  locations, and branch policy are accurate.
- [x] Decide whether any branch merge is needed; no merge is needed because
  there is no extra local or remote feature branch to consolidate.
- [x] Sync root docs mirror, validate the documentation-only change, and run
  read-only subagent review: `git diff --check` and
  `bin/multiwfn2vesta --help` passed; subagent found no branch-status
  blockers.
- [x] Commit and push the README branch-convergence refresh with
  `Stardust0831` identity as `17b489348d229aae9fe63c74067b12eab8eefcb4`;
  post-push verification showed local `main`, `origin/main`, and
  `origin/HEAD` aligned at that commit, with only `refs/heads/main` exposed
  by the remote.  This docs-only closure records the verification; its final
  hash is reported in the assistant response to avoid a self-referential
  record loop.

## Current Continuation: 2026-06-10 Spin-Density Cube Arithmetic

- [x] Record resumed objective: keep expanding VESTA-ready Multiwfn/ABACUS
  wavefunction and cube analyses, especially where ABACUS can provide
  compatible cube inputs directly or through Molden.
- [x] Inspect current branch state: local `main` is aligned with
  `origin/main`; only untracked local probes `domain.cub` and `domain.pdb`
  are present and must stay uncommitted.
- [x] Choose the next bounded increment from the prior review: add an
  explicit `cube-arith` spin-density operation for alpha/beta or
  spin-up/spin-down density cubes, then route the result to
  `cube-preset spin-density`.
- [x] Implement CLI/tests/docs for `cube-arith --operation spin-density`
  without changing the existing generic `density-difference` behavior:
  `spin-density` uses `--plus-cube` alpha/spin-up density minus
  `--minus-cube` beta/spin-down density, and `--preset auto` routes the
  product to `cube-preset spin-density`.
- [x] Add focused tests for operation term construction, default
  `spin-density` VESTA preset selection, generated signed `ISURF` defaults,
  command-line execution, and interactive CLI argument construction; focused
  `tests.test_cube_arith` and `tests.test_cli` passed.
- [x] Update README, Chinese usage docs, worklog, skills, and the ABACUS
  analysis matrix with the new alpha/beta cube arithmetic route.
- [x] Sync root docs, validate, and review: root docs mirror is clean;
  `py_compile`, focused `tests.test_cube_arith tests.test_cli` with 63 tests,
  full 271-test no-GUI regression, `bin/multiwfn2vesta cube-arith --help`,
  `bin/multiwfn2vesta --help`, `git diff --check`, and read-only subagent
  review all passed.
- [x] Commit and push on `main` with `Stardust0831` identity as
  `1a8bbc63cc785ec07b4b177078909971b8ac127b`; post-push verification showed
  local `main`, `origin/main`, and `origin/HEAD` aligned at that commit with
  only `refs/heads/main` exposed by the remote.  This follow-up records the
  completed push before starting the next increment.

## Current Continuation: 2026-06-10 Gradient-Norm Cube Display

- [x] Record resumed objective: keep expanding maintained VESTA-ready
  Multiwfn/ABACUS wavefunction and cube analyses, prioritizing products that
  ABACUS can feed through Molden or direct cube routes.
- [x] Recheck current state: `main` is aligned with `origin/main` at
  `67a6e0f1a69f91b02481f5093477e32632f477de`; untracked local probes
  `domain.cub` and `domain.pdb` remain uncommitted.
- [x] Inspect current `grid-run` and `cube-preset` coverage for real-space
  function `2` gradient norm: `grid-run` already generated `gradient.cub` but
  routed it through generic `density`; Multiwfn 2026.6.2 `0123dim.f90`
  confirms function `2` exports `gradient.cub`, and `define.f90` provides the
  global default `sur_value=0.05D0`.
- [x] Implement tests/docs for the new preset/function mapping without
  changing existing density or signed presets: added `cube-preset
  gradient-norm`, mapped `grid-run --function gradient` to it, and focused
  `py_compile` plus `tests.test_cube_preset tests.test_multiwfn_grid` passed
  with 57 tests, including a fake Multiwfn integration-style run that writes
  `gradient.cub` and verifies the generated recipe/VESTA manifest uses
  `gradient-norm`.
- [x] Sync root docs, validate, and review: focused `py_compile` passed;
  focused `tests.test_cube_preset tests.test_multiwfn_grid` passed with 57
  tests; full no-GUI regression passed with 273 tests; `cube-preset
  --list-presets`, `grid-run --list-functions`, and `git diff --check`
  passed; read-only subagent review found no blocker, and its suggested
  integration-style gradient run test was added before closeout.  Commit/push
  and post-push branch verification are reported in the assistant response.

## Current Continuation: 2026-06-10 Grid Function Display Presets

- [x] Record resumed objective: keep enriching Multiwfn wavefunction analyses
  that ABACUS can feed through Molden or direct cubes, and express useful
  products in VESTA.
- [x] Inspect current branch state: local `main` is aligned with
  `origin/main`; only untracked local probes `domain.cub` and `domain.pdb`
  are present and must stay uncommitted.
- [x] Re-read the analysis matrix, CLI surface, `grid-run`, and `cube-preset`
  code to choose the next bounded high-value increment.
- [x] Add maintained VESTA display presets for common signed/scalar
  Multiwfn real-space grid functions that currently fall back to generic
  presets: spin density, Laplacian, Hamiltonian kinetic energy density
  `K(r)`, and Lagrangian kinetic energy density `G(r)`.
- [x] Process read-only subagent review: adjust `spin-density` default to
  Multiwfn `0123dim.f90` `sur_value=0.02`, and include adjacent standalone
  single-cube presets for `orbdens.cub`, `RDG.cub`, and `RDGprodens.cub`
  without changing the existing two-cube `rdg -> iri` texture route.
- [x] Add focused tests for preset listing, signed/single surface behavior,
  manifest notes, and `grid-run` function-to-preset resolution; focused
  validation currently passes 30 `cube-preset` tests and 25 `grid-run` tests.
- [x] Finish README/usage/skills/research/worklog sync and final validation:
  `py_compile`, 55 focused tests, full 268-test no-GUI regression,
  `bin/multiwfn2vesta --help`, `cube-preset --list-presets`,
  `grid-run --list-functions`, `git diff --check`, and stale-doc scan.
- [x] Mirror root docs and prepare the stable `main` closeout; final commit
  hash and post-push branch check are reported in the assistant response.

## Current Continuation: 2026-06-10 Multiwfn Analysis Expansion Sweep

- [x] Record resumed objective: keep surveying useful Multiwfn analyses that
  can become VESTA products, prioritizing wavefunction/cube workflows that
  ABACUS can produce directly or through the maintained Molden bridge.
- [x] Re-read the current analysis matrix, CLI surface, and local Multiwfn
  source evidence to choose the next high-value maintainable increment.
- [x] Implement or document the next bounded feature without touching files
  outside `/mnt/g/work/multiwfn2vesta`.
- [x] Add focused tests, update README/usage/skills/worklog, sync root docs,
  run review, and validate the direct ABACUS cube preset increment.
- [x] Prepare the stable `main` increment for commit and push; final commit
  hash and post-push branch check are reported in the assistant response.

## Current Request: 2026-06-10 README Refresh And One-Branch Closeout

- [x] Record user request: update README, inspect the unusual-looking branch
  state, converge work back to one branch if needed, and use
  `Stardust0831` identity.
- [x] Recheck repository state without destructive operations: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `809e2611aa51cd9a37fd5966b6d4e2e4673f9e44`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`.
- [x] Confirm repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Refresh README branch/status wording so the recorded hash is the
  pre-increment branch-audit baseline and not a stale final commit claim.
- [x] Keep the new ABACUS direct cube preset docs and skills in the same
  maintained `main` increment.
- [x] Resync root docs after final metadata edits, then prepare the `main`
  commit/push closeout with final hash reported in the assistant response.

## Active Goal Continuation: 2026-06-10 Multiwfn Analysis Expansion

- [x] Record continuation request: keep researching and implementing useful
  Multiwfn wavefunction analyses that can become VESTA products, especially
  ABACUS-compatible wavefunction/cube workflows.
- [x] Resume the pending aIGM/amIGM feasibility task from local Multiwfn
  source evidence and current IGM/IGMH runner implementation.
- [x] Implement a maintained runner or document the source-level blocker,
  then update tests, README/usage/skills/worklog, and root docs mirror.
- [x] Validate, run review, commit, and push a stable `main` increment if the
  result is maintainable.

## Current Request: 2026-06-10 README Refresh, One-Branch Closeout, And aIGM/amIGM Runner

- [x] Record user request: update README, inspect unusual branch state, converge work back to one branch, and use `Stardust0831` git identity.
- [x] Inspect current branch/remotes and local git identity without destructive operations: local `main`, `origin/main`, and `origin/HEAD` are aligned at `0fd0517`; the remote exposes only `refs/heads/main`; repository-local identity is `Stardust0831 <13862180016@163.com>`.
- [x] Update README to reflect the current CLI/workflows, aIGM/amIGM runner scope, and single-branch status.
- [x] Sync documentation mirror after final doc edits and keep kanban/worklog current.
- [x] Validate docs/tests, review diff, commit, and push to single `main` with `Stardust0831`; final commit hash and post-push branch check are reported in the assistant response.

## Current Continuation: 2026-06-10 aIGM/amIGM Runner Feasibility

- [x] Record the continued long-running objective: keep expanding useful
  Multiwfn wavefunction analyses that can become VESTA products, especially
  ABACUS-compatible Molden workflows.
- [x] Re-read the existing IGM/mIGM/IGMH runner and local Multiwfn weak
  interaction source before deciding whether aIGM/amIGM prompt streams are
  stable enough for a maintained CLI.
- [x] Implement the smallest aIGM/amIGM runner increment as a trajectory
  workflow that reuses `cube-preset aigm`; source evidence shows Multiwfn
  exports `avgdg_inter.cub`, `avgsl2r.cub`, optional `avgRDG.cub`, and
  optional `thermflu.cub`.
- [x] Address read-only review PBC grid risk: the runner now accepts
  `--periodic`/`--nonperiodic`, detects common trajectory cell markers, and
  rejects `--grid-mode points` for periodic input because Multiwfn reads PBC
  option `4` as spacing rather than `NX,NY,NZ`.
- [x] Add focused tests/docs/skill updates and sync project/root docs.
- [x] Validate, review if needed, then commit and push on `main` if stable; final commit hash and post-push branch check are reported in the assistant response.

## Current Request: 2026-06-10 README Refresh, One-Branch Closeout, And Fukui Runner

- [x] Record the user's request before editing: update README, inspect the
  odd-looking branch state, consolidate back to one branch if needed, and keep
  Git identity as `Stardust0831`.
- [x] Recheck repository state without discarding in-progress runner work:
  local `main`, `origin/main`, and `origin/HEAD` are aligned at `e92d98a`,
  and `git ls-remote --heads origin` exposes only `refs/heads/main`.
- [x] Confirm repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Finish focused `fukui-run` CLI tests before documenting the new surface:
  `tests.test_multiwfn_fukui` plus `tests.test_cli` currently pass 52 tests.
- [x] Refresh README and docs so the front page records the current
  single-branch state and the new high-level Fukui/dual-descriptor runner.
- [x] Sync `project/docs/` to the root docs mirror and verify with
  `rsync -ani --checksum docs/ ../docs/`.
- [x] Run code/help validation before mirror sync and review: `py_compile`
  passed, 88 focused tests passed, the full 242-test no-GUI regression
  passed, `bin/multiwfn2vesta --help`,
  `bin/multiwfn2vesta fukui-run --help`,
  `bin/multiwfn2vesta cube-preset --list-presets`, and `git diff --check`
  passed.
- [x] Run read-only subagent review: no blocker.  The non-blocking P2 about
  VESTA failure after cube arithmetic was fixed by preserving cube-only
  output in the top-level recipe while returning nonzero for the VESTA
  failure; the P3 was to write final sync/review status back to this board.
- [x] Commit and push on `main`: `43e00d2` (`Add Multiwfn Fukui runner`).
- [x] Recheck local/remote branch state after push: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at `43e00d2`, and
  `git ls-remote --heads origin` exposes only `refs/heads/main`.

## Current Continuation: 2026-06-10 Fukui/Dual Descriptor Wavefunction Runner

- [x] Record the continued long-running objective: keep expanding
  Multiwfn analyses that can become VESTA products from ABACUS-compatible
  wavefunction or cube data.
- [x] Confirm that existing `grid-run` density generation and `cube-arith`
  operations can be composed into a maintained Fukui/dual-descriptor runner
  without reimplementing cube math.
- [x] Implement the smallest useful high-level runner for finite-system
  charged-state wavefunctions, with explicit periodic/charged-system caveats.
- [x] Add focused tests, CLI wiring, docs, and a skill note.
- [x] Sync project/root docs, validate, run read-only review, then commit and
  push on `main` if stable.

## Current Continuation: 2026-06-10 Basin Analysis VESTA Route Exploration

- [x] Record the continued long-running objective: keep enriching
  Multiwfn analyses that can become VESTA products, especially workflows
  compatible with ABACUS Molden or ABACUS/Multiwfn cube data.
- [x] Re-read the current analysis matrix and local Multiwfn `basin.f90`
  evidence before deciding whether this increment should be a full
  command-stream runner or a safer display/preset layer for existing basin
  cubes.
- [x] Inspect current `cube-vesta`/`cube-preset` capabilities for displaying
  one or more binary basin cubes without depending on VESTA UI automation.
- [x] Implement the smallest useful basin-related increment: `cube-preset
  basin` for individual binary `basinNNNN.cub` files and `cube-preset
  basin-type` for signed `basinsyn.cub`, plus focused preset tests.
- [x] Validate: `py_compile`, 20 focused `cube-preset` tests,
  `cube-preset --list-presets`, full 233-test no-GUI regression, and
  `git diff --check` passed.
- [x] Address read-only review residual risk by rejecting all-index
  `basin.cub` in the binary basin preset.
- [x] Sync project/root docs after the guard update.
- [x] Commit and push on `main` if stable; final commit hash is reported in
  the assistant response.

## Current Request: 2026-06-10 README Refresh And Branch Consolidation After Domain Runner

- [x] Record the user's request before editing: update README, inspect the
  odd-looking branch state, consolidate back to one branch if needed, and keep
  Git identity as `Stardust0831`.
- [x] Fetch/prune and recheck local/remote branches before deciding whether a
  merge-back is required: local `main`, `origin/main`, and `origin/HEAD` are
  aligned at `da7d4b7`, and `git ls-remote --heads origin` exposes only
  `refs/heads/main`.
- [x] Confirm repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Review the in-progress `domain-run` README/docs/code diff so the README
  reflects the actual maintained CLI surface.
- [x] Sync `project/docs/` to the root docs mirror after documentation edits.
- [x] Run validation: `py_compile`, 67 focused tests, 230-test full no-GUI
  regression, top-level help, `domain-run --help`,
  `cube-preset --list-presets`, docs mirror checksum checks, and
  `git diff --check` passed.
- [x] Run read-only review: no blocker; residual risks were limited to keeping
  local `domain.cub`/`domain.pdb` unstaged and Multiwfn menu-version drift.
- [x] Commit and push the feature increment on `main`: `73018ab`
  (`Add Multiwfn domain runner`).
- [x] Run post-push branch check: local `main`, `origin/main`, and
  `origin/HEAD` are aligned at `73018ab`; `git ls-remote --heads origin`
  returns only `refs/heads/main`.
- [x] Prepare README/kanban closeout so the front page records the
  post-domain-run branch state; this docs-only closeout is committed on the
  same `main` branch.

## Current Continuation: 2026-06-10 Domain Analysis Runner From Cube Data

- [x] Continue the broad Multiwfn/ABACUS/VESTA analysis-expansion objective by
  taking the confirmed domain-analysis candidate to a maintained runner.
- [x] Re-read Multiwfn `otherfunc2.f90` evidence: main function `200`,
  subfunction `14`, menu option `3` sets `<`/`>` domain criteria, `-1`
  yields domains from current grid data in memory, `10` exports
  `domain.cub`, and `11` exports `domain.pdb`.
- [x] Implement `multiwfn2vesta domain-run` for existing cube/grid input,
  plus `cube-preset domain`, unified CLI/interactive wiring, and console
  script entries.
- [x] Add focused tests for command streams, output copying, VESTA preset
  chaining, missing-output errors, and CLI dispatch.
- [x] Run real H2O density-cube noGUI smoke:
  `smoke/multiwfn_domain_run_smoke_20260610/h2o_density/`, generating
  `h2o_density_domain.cub`, `h2o_density_domain.pdb`, and
  `h2o_density_domain_cube.vesta`.
- [x] Update README, usage docs, research matrix, skill note, kanban, and
  worklog for the new domain route.
- [x] Sync project/root docs and run final validation.
- [x] Run final read-only review: no blocker.
- [x] Commit and push on `main`: `73018ab` (`Add Multiwfn domain runner`).

## Current Request: 2026-06-10 README Refresh at STM Runner Tip

- [x] Record the user's request before editing: update README, inspect the
  odd-looking branch state, consolidate back to a single branch if needed, and
  keep Git identity as `Stardust0831`.
- [x] Recheck branch state after `git fetch --prune origin`: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `fdf85863ccb01c5783ce912163f1ec4a34060dd7`
  (`Add Multiwfn STM runner`).
- [x] Recheck remote heads: `git ls-remote --heads origin` returns only
  `refs/heads/main`, also at `fdf8586`, so no merge-back is needed in this
  pass.
- [x] Confirm repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Refresh `README.md` Repository Status so it records the current
  STM-runner tip rather than stale `bc462e1` branch-audit wording.
- [x] Sync project/root docs, run documentation validation, review, then
  commit and push on `main`: `1493c80` (`Refresh README branch status at STM
  tip`).

## Current Continuation: 2026-06-10 STM/LDOS Runner

- [x] Close the previous README refresh state: commit `bc462e1` was pushed to
  `origin/main`, and post-push branch checks showed only `refs/heads/main`.
- [x] Pick the next roadmap increment from the active goal: implement a
  maintained Multiwfn STM/LDOS constant-current cube runner that can feed
  VESTA.
- [x] Add `stm-run` to the unified CLI, package scripts, and cube preset layer.
- [x] Add focused tests for command-stream generation, output capture, VESTA
  chaining, CLI dispatch, and missing-cube failures.
- [x] Run a real H2O Multiwfn noGUI STM smoke and record the generated
  products.
- [x] Update README, usage docs, skills/worklog/research notes, and sync root
  docs.
- [x] Run validation: `py_compile`, 64 focused STM/preset/CLI tests,
  221-test full no-GUI regression, `stm-run --help`,
  `cube-preset --list-presets`, `git diff --check`, and root-doc checksum
  sync check all passed; optional `--prepare-fermi-temperature 298.15`
  STM smoke also returned 0 and generated `h2o_stm.cub`.
- [x] Run read-only review, then commit and push on `main`: `fdf8586`
  (`Add Multiwfn STM runner`).

## Current Request: 2026-06-10 README Refresh And Branch Consolidation

- [x] Record the user's request before editing: update README, inspect the
  odd-looking branch state, consolidate back to a single branch if needed, and
  keep Git identity as `Stardust0831`.
- [x] Inspect the current branch state: local `main`, `origin/main`, and
  `origin/HEAD` are aligned at `b99d80e`; no extra local or remote feature
  branch is visible, so no merge is currently required.
- [x] Confirm repository identity is `Stardust0831 <13862180016@163.com>`.
- [x] Refresh README so it reflects the current maintained CLI/workflows after
  the recent grid mapped-surface bridge.
- [x] Sync `project/docs/` to the root `docs/` mirror after documentation
  edits.
- [x] Validate documentation/branch state with `git diff --check`,
  `bin/multiwfn2vesta --help`, `rsync -ani --checksum project/docs/ docs/`,
  and post-fetch branch checks.
- [x] Run read-only pre-commit review: no blocker; reviewer confirmed branch
  audit, validation wording, kanban state, and root-doc mirror consistency.
- [x] Commit and push the README/docs update on `main`: `bc462e1`
  (`Refresh README branch status`).

## Current Continuation: 2026-06-10 STM/LDOS Candidate After Grid Surface Bridge

- [x] Record the resumed long-running objective: continue enriching
  ABACUS-compatible Multiwfn wavefunction analyses that can produce VESTA
  visualization products.
- [x] Re-read current project state and Multiwfn STM source prompts before
  choosing the exact implementation boundary.
- [x] Confirm the minimal STM command stream by a manual H2O noGUI probe:
  `300 -> 4 -> 1 -> 4 -> NX,NY,NZ -> 0 -> 2 -> 0 -> -1 -> 0 -> q`
  exports `STM.cub` in constant-current mode.
- [x] Implement the smallest reliable STM/LDOS increment if the prompt stream
  is stable enough, otherwise document the blocker and choose the next
  aligned increment.
- [x] Add tests, docs, and a no-GUI smoke scaled to the implemented boundary.
- [x] Sync project/root docs for the implemented STM/LDOS increment.
- [ ] Review, commit, and push the implemented STM/LDOS increment if stable.

## Current Continuation: 2026-06-10 Multiwfn Analysis Expansion After IGM/mIGM

- [x] Record the resumed long-running objective: continue researching and
  implementing valuable Multiwfn wavefunction analyses that can be visualized
  in VESTA, especially ABACUS-compatible Molden workflows.
- [x] Re-read the current roadmap, maintained CLI surface, and Multiwfn source
  evidence before choosing the next concrete increment.
- [x] Pick one increment that makes the requested end state more true without
  broad unrelated refactors: let `grid-run` use a generated Multiwfn grid cube
  as a texture on a provided density/surface cube through a new
  `--surface-cube` route, covering ESP/ALIE/vdW/sign(lambda2)rho mapped
  surfaces without hand-running `cube-preset`.
- [x] Implement the increment with tests, docs, and a smoke or no-GUI
  validation scaled to the risk: `grid-run --surface-cube` now maps the
  generated grid cube as texture on a provided surface cube, with mapped
  presets for ESP/ALIE/vdW/sign(lambda2)rho and a real H2O ESP mapped-surface
  smoke.
- [x] Validate the increment: `py_compile`, 65 focused grid/CLI tests,
  212-test full no-GUI regression, `git diff --check`, `grid-run --help`,
  `grid-run --list-functions`, and the real H2O ESP mapped-surface smoke
  passed.
- [x] Sync project/root docs and leave the board ready for the next
  continuation.
- [x] Run final read-only pre-commit review: no blockers; noted only that
  external positional unpacking of `MultiwfnGridResult` would see the added
  trailing fields.

## Current Request: 2026-06-10 README and Single-Branch Closure for IGM/mIGM

- [x] Record the user's request before continuing: update README, inspect the
  odd-looking branch state, merge/consolidate back to one branch if needed,
  and keep Git identity as `Stardust0831`.
- [x] Recheck local/remote branch state and repository identity without
  discarding the in-progress IGM/mIGM runner work: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at `440feec`; remote exposes
  only `refs/heads/main`; identity is `Stardust0831 <13862180016@163.com>`.
- [x] Wait for the read-only pre-commit subagent review of the current
  IGM/mIGM diff, then fix real blockers: fixed wrapper `--method` override
  rejection, method-specific VESTA titles, and method-specific error prefixes.
- [x] Finalize README/docs so they describe the actual maintained CLI surface
  and branch state after this increment.
- [x] Run focused/full validation and real smoke checks again after the review
  code changes: `py_compile`, 55 focused tests, 210-test full regression,
  `git diff --check`, top-level/IGMH help, fixed-wrapper help/override checks,
  and real H2O noGUI IGM/mIGM smokes passed under
  `smoke/multiwfn_igm_migm_run_smoke_20260610_review_fix/`.
- [x] Run final read-only pre-commit review after the fixes: no code blocker;
  only root-doc synchronization remained, which is handled before commit.
- [ ] Commit and push on `main` with identity `Stardust0831`; report the final
  commit hash and post-push branch check.

## Current Continuation: 2026-06-10 IGM and mIGM Command Streams

- [x] Record the continued long-running objective: keep expanding maintained
  Multiwfn wavefunction-analysis workflows that can feed VESTA, especially
  ABACUS-compatible Molden routes.
- [x] Choose the next concrete increment from the current roadmap: extend the
  weak-interaction runner beyond standard IGMH to cover Multiwfn IGM and mIGM
  command streams where the source prompts are stable.
- [x] Re-read current `igmh-run`, unified CLI, tests, docs, and local
  Multiwfn `visweak.f90`/`grid.f90` evidence before editing.
- [x] Implement the smallest reliable method-selection extension with focused
  tests, preserving the just-added PBC grid guard.
- [x] Real noGUI H2O smokes passed for `igm-run` and `migm-run`, generating
  `h2o_igm_cube.vesta` and `h2o_migm_cube.vesta`.
- [x] Update README, usage, skill, research, worklog, and root docs with the
  new IGM/mIGM boundary.
- [x] Validate and review after the fixed-method wrapper changes.
- [ ] Commit and push when stable.

## Current Request: 2026-06-10 README and Branch Consolidation After IGMH Runner Draft

- [x] Record the user's request: update README, inspect the unusual branch state, consolidate back to one branch if needed, and keep Git identity as `Stardust0831`.
- [x] Audit current local/remote branch state after fetching/pruning, without discarding the in-progress `igmh-run` work.
- [x] Finish and validate the in-progress IGMH command-stream wrapper if it is already in the worktree, because README should describe the actual maintained CLI surface.
- [x] Refresh README and synchronized docs/work records so repository status, branch guidance, and usage notes are current.
- [x] Real noGUI H2O smoke passed for `igmh-run`, generating `dg_inter.cub`, `sl2r.cub`, optional `dg_intra.cub`/`dg.cub`, and `h2o_igmh_cube.vesta`.
- [x] Read-only pre-commit review found a PBC grid semantics risk; the runner now rejects `--grid-mode points` for Molden `[Cell]` inputs and docs steer periodic workflows to spacing or `pbc-cell`.
- [x] Run focused and full no-GUI validation where feasible, then do a read-only review pass before committing: `py_compile`, 48 focused tests, 203-test full no-GUI regression, `git diff --check`, and `igmh-run --help` passed after the review fix.
- [x] Prepare the stable commit and push on `main` as `Stardust0831`; final commit hash and post-push branch check are reported in the assistant response.

## Current Request: 2026-06-10 IGMH Command-Stream Foundation

- [x] Continue the long-running Multiwfn/ABACUS/VESTA objective after the
  IGMH/aIGM display preset increment.
- [x] Choose the next concrete increment: investigate and implement the first
  maintainable Multiwfn IGM/IGMH command-stream wrapper so ABACUS Molden files
  can produce `dg_inter.cub`/`sl2r.cub` without hand-driving Multiwfn.
- [x] Inspect existing `aim-run`, `iri-run`, and `grid-run` runners plus the
  Multiwfn IGMH source/menu prompts.
- [x] Implement the smallest reliable `igmh-run` workflow with tests and docs,
  then connect its output to `cube-preset igmh` when requested.
- [x] Validate and review the implementation, including the PBC grid guard.
- [x] Prepare the stable commit and push closure; final commit hash and post-push branch check are reported in the assistant response.

## Current Request: 2026-06-10 IGMH/aIGM Cube Presets

- [x] Continue the long-running Multiwfn/ABACUS/VESTA objective by closing the
  IGMH display-layer preset gap.
- [x] Implement `cube-preset` entries for `igmh`/`igm-inter`, `igm-intra`,
  `aigm`, and `aigm-tfi` from bundled Multiwfn VMD defaults.
- [x] Add focused tests, documentation, a dedicated skill note, and a real
  Ag(111)+benzene no-GUI smoke.
- [x] Read-only pre-commit review verified the template defaults and noted
  only that this current board heading needed refreshing.
- [x] Final post-review validation passed: `git diff --check`, `py_compile`,
  52 focused cube/CLI tests, full 192-test no-GUI regression, and
  `cube-preset --list-presets`.
- [x] Prepare the implementation, tests, docs, and new skill file for commit
  and push on `main`; final commit hash is reported in the assistant response.

## Current Request: 2026-06-10 README Branch Cleanup at 8bf115a

- [x] Record the user's request: update README, inspect the confusing branch
  state, merge/consolidate back to one branch if needed, and use identity
  `Stardust0831`.
- [x] Rechecked project branch state before the README cleanup commit after
  `git fetch --prune origin`:
  local `main`, `origin/main`, and `origin/HEAD` all point at
  `8bf115a3fa332e1008c370d48e70e5235e942ac5`
  (`Add surface extrema VESTA overlay`).
- [x] Rechecked remote heads: `git ls-remote --heads origin` returns only
  `refs/heads/main`, so no local or remote feature branch needs merging in
  this pass.
- [x] Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- [x] Refresh README so the Repository Status section records the current
  audited `main` tip, the one-branch remote state, and the future
  merge-back pattern.
- [x] Sync project/root work records with this README and branch audit.
- [x] Validate the docs update and CLI entry point before commit:
  `git diff --check` and `bin/multiwfn2vesta --help` passed.
- [x] Read-only pre-commit review verified the README branch-status claims;
  it also noted that the pre-existing IGMH planning block is unrelated to the
  README cleanup, so the final response should call out that it is board
  planning rather than a README feature change.
- [x] Prepare the docs refresh for commit and push on `main` with identity
  `Stardust0831`; report the final commit hash and post-push branch check in
  the assistant response.

## Current Continuation: 2026-06-10 Multiwfn Analysis Expansion

- [x] Record the resumed long-running objective: research valuable
  Multiwfn wavefunction analyses that can be visualized in VESTA, especially
  routes starting from ABACUS-compatible wavefunction/cube outputs.
- [x] Re-read the current roadmap, maintained CLI surface, and relevant
  Multiwfn source/examples before choosing the next concrete increment.
- [x] Implement one maintained increment that makes the requested final state
  more true, with tests and docs scaled to the change.
- [x] Sync README/usage/skill/research docs plus project/root work records.
- [x] Focused validation passed for the implementation draft: `py_compile`,
  33 tests across `tests.test_cube_preset` and `tests.test_multiwfn_grid`,
  `cube-preset --list-presets`, and `grid-run --list-functions`.
- [x] Real H2O noGUI smokes passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_surface_map_20260610/`:
  `grid-run --function hamiltonian-ked`, `grid-run --function alie`,
  aligned density export, and `cube-preset alie` VESTA generation.
- [x] Read-only pre-commit review found one non-blocking default mismatch:
  `surface-map`/`molsurfmap` originally used isosurface `0.001`.  The main
  thread fixed it to match Multiwfn `molsurfmap.vmd`: isosurface `0.01` and
  texture range `0.0` to `0.002`.
- [x] Final pre-commit validation passed: `py_compile`, 68 focused tests
  across cube/grid/CLI, full 182-test no-GUI regression, `git diff --check`,
  `cube-preset --list-presets`, and `grid-run --list-functions`.
- [x] Prepared this closure record for the final implementation/docs push.
  The final commit hash and post-push branch check are reported in the
  assistant response to avoid an infinite chain of "record the record"
  commits.

## Current Increment: 2026-06-10 IGMH VESTA Preset Foundation

- [x] Record the continued objective: keep enriching VESTA workflows for
  valuable Multiwfn analyses, especially those reachable from ABACUS LCAO
  Molden wavefunction files.
- [x] Choose the next concrete increment: inspect IGMH/IRI/RDG display
  templates and add the smallest maintained VESTA preset foundation before
  attempting full Multiwfn IGMH command-stream automation.
- [x] Resume this increment after the README branch cleanup: implement the
  preset-layer foundation first, then leave full Multiwfn IGMH command-stream
  automation as a later increment.
- [x] Inspect current `cube-preset`, IGMH docs/smokes, and bundled Multiwfn
  VMD scripts for `dg_inter.cub`/`sl2r.cub` display defaults.
- [x] Implement maintained weak-interaction cube presets with focused tests:
  `igmh`/`igm-inter`, `igm-intra`, `aigm`, and `aigm-tfi`.
- [x] Real no-GUI smoke passed on Ag(111)+benzene IGMH cubes under
  `/mnt/g/work/multiwfn2vesta/smoke/igmh_preset_20260610_1128/products/`,
  generating `dg_inter_igmh_cube.vesta` and recipe from `dg_inter.cub` plus
  `sl2r.cub`.
- [x] Sync README/usage/skill/research docs and root work records.
- [x] Validate, review, commit, and push when stable.  Final commit hash is
  reported in the assistant response.

## Current Increment: 2026-06-10 Surface-Map Extrema Overlay

- [x] Record the continued objective: enrich maintained VESTA workflows for
  valuable Multiwfn analyses that can start from ABACUS-compatible
  wavefunction/cube data.
- [x] Choose the next concrete increment: support Multiwfn molecular surface
  extrema from `surfanalysis.pdb` as an optional VESTA overlay for
  density-surface mapped-property workflows.
- [x] Start a read-only sub-agent review for `surfanalysis.pdb` evidence,
  reusable VESTA/AIM code paths, CLI shape, and test risks.
- [x] Inspect current `cube-preset`, `cube-vesta`, AIM PDB, and multi-phase
  VESTA style code locally.
- [x] Implement a maintained parser/overlay command path with focused tests:
  `surface-extrema` standalone patcher and `cube-preset --surfanalysis-pdb`.
- [x] Real CLI smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/surface_extrema_overlay_20260610/`,
  covering `cube-preset surface-map --surfanalysis-pdb` and standalone
  `surface-extrema --selection minima`.
- [x] Update README/usage/skill/research docs and root work records.
- [x] Read-only pre-commit review found no blockers; documentation follow-up
  corrected standalone `--radius` vs `cube-preset --extrema-radius` wording
  and recorded append behavior.
- [x] Final validation passed: `py_compile`, 52 focused tests, full
  189-test no-GUI regression, `git diff --check`, top-level help,
  `cube-preset --help`, and `surface-extrema --help`.
- [x] Prepared this increment for commit and push.  The final commit hash and
  post-push branch check are reported in the assistant response to avoid an
  infinite chain of "record the record" commits.

## Current Request: 2026-06-10 README Refresh at 19bd45d

- [x] Record the user's request: update README, make the branch state less
  confusing, merge back to one branch if needed, and keep commit identity as
  `Stardust0831`.
- [x] Rechecked project branch state after `git fetch --prune origin`:
  local `main`, `origin/main`, and `origin/HEAD` all point at
  `19bd45dfc33f29309c90d408b5672fb137043b9f`
  (`Add surface-map presets and grid functions`).
- [x] Rechecked remote heads: `git ls-remote --heads origin` returns only
  `refs/heads/main`, so no local or remote branch needs merging in this pass.
- [x] Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- [x] Refresh README so the Repository Status section records the current
  audited `main` tip and removes stale branch-audit wording.
- [x] Sync project/root work records with this README and branch audit.
- [x] Validate the docs update and CLI entry point before commit:
  `git diff --check` and `bin/multiwfn2vesta --help` passed.
- [x] Prepare the README refresh for commit and push on `main` with identity
  `Stardust0831`.  The final commit hash and post-push branch check are
  reported in the assistant response to avoid an infinite chain of "record
  the record" commits.

## Current Request: 2026-06-10 README Single-Branch Refresh

- [x] Record the user's request: refresh README, make the branch state easier
  to understand, merge back to one branch if needed, and use identity
  `Stardust0831`.
- [x] Recheck the real project Git state with fetch/prune, branch listing,
  remote-head listing, and repository-local identity.
- [x] Refresh README so the Repository Status section describes the audited
  `main` tip and the one-branch remote state without stale branch-audit
  wording.
- [x] Sync project/root work records with this README and branch audit.
- [x] Validation passed before commit: `git diff --check` and
  `bin/multiwfn2vesta --help`.
- [x] Prepared this closure record for the final README/docs push.  The final
  commit hash and post-push branch check are reported in the assistant
  response to avoid an infinite chain of "record the record" commits.

## Current Request: 2026-06-10 Multiwfn Atom Table Coloring

- [x] Record the continued long-running objective: turn valuable
  Multiwfn/ABACUS wavefunction analyses into maintained VESTA workflows.
- [x] Chosen next concrete increment from the roadmap: a generic Multiwfn
  atom scalar table parser that feeds the maintained VESTA atom-coloring
  backend.  This targets Multiwfn charges, Fukui-like atom contributions,
  orbital/composition atom tables, or hand-normalized atom values exported as
  text/CSV/TSV.
- [x] Inspect the existing `vesta_atom_coloring`, `abacus_mulliken`, unified
  CLI, package metadata, and tests before editing.
- [x] Implement `multiwfn2vesta multiwfn-atom-color` plus parser tests and CLI
  tests.
- [x] Sync README, usage docs, skill notes, research matrix, kanban, and
  worklog.
- [x] Focused validation passed after review fixes: `py_compile`, 45 tests across
  `tests.test_multiwfn_atom_table` and `tests.test_cli`, and
  `multiwfn2vesta multiwfn-atom-color --help`.
- [x] Read-only pre-commit review found and the main thread fixed the
  behavior risks before commit: ambiguous multi-value tables now require
  `--value-column`; `atom-color` remains the historical
  `abacus-mulliken-color` alias; strict keyed tables validate key sets and
  duplicate keys rather than row order.
- [x] Real CLI smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_atom_color_smoke_20260610/`,
  writing `colored_after_review.vesta` and `values_after_review.csv`.
- [x] Full validation passed: 178-test no-GUI regression and
  `git diff --check`.
- [x] Committed and pushed to GitHub `main` as
  `7b305ea5762b3e8444b53338aecec190cc331a7f`
  (`Add Multiwfn atom table coloring`) with repository-local identity
  `Stardust0831 <13862180016@163.com>`.
- [x] Post-push verification after `git fetch --prune origin`: project
  `HEAD`, `origin/main`, and `origin/HEAD` all point at `7b305ea`; the remote
  exposes only `refs/heads/main`; repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- [x] Prepared this closure record for the final docs-only push.  The closure
  commit hash and final branch check are reported in the assistant response to
  avoid an infinite chain of "record the record" commits.

## Current Request: 2026-06-10 README Branch Consolidation Refresh

- [x] Record the user's request: update README, simplify/merge the branch
  state if needed, and use identity `Stardust0831`.
- [x] Rechecked project branch state with `git fetch --prune`,
  `git status --short --branch`, `git branch --all --verbose --no-abbrev`,
  and `git ls-remote --heads origin`.
- [x] Confirmed no merge is needed in this pass: local `main`,
  `origin/main`, and `origin/HEAD` all point at
  `2481cf79c87666503ea8d8186b4b76fba05b2847`, and the GitHub remote exposes
  only `refs/heads/main`.
- [x] Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- [x] Refresh README repository-status wording so the current single-branch
  state is clear and old branch-audit details do not read like competing
  active states.
- [x] Sync project/root work records with this branch audit.
- [x] Validated with `git diff --check`, `bin/multiwfn2vesta --help`,
  `git branch --all --verbose --no-abbrev`, `git ls-remote --symref origin
  HEAD`, and `git ls-remote --heads origin`.
- [x] Committed and pushed the README branch consolidation refresh to GitHub
  `main` as `500ffece49c42bcbb4a44d49bcd31044d915bce0`
  (`Refresh README branch consolidation status`).
- [x] Post-push verification after `git fetch --prune origin`: project
  `HEAD`, `origin/main`, and `origin/HEAD` all point at `500ffec`; the remote
  exposes only `refs/heads/main`; repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- [x] Prepared this closure record for the final docs-only push.  The closure
  commit hash and final branch check are reported in the assistant response to
  avoid an infinite chain of "record the record" commits.

## Doing

- Continue the long-running objective: research and turn valuable
  Multiwfn wavefunction analyses into maintained VESTA workflows, especially
  routes that can start from ABACUS LCAO Molden files.  The current increment
  implements a generic Multiwfn atom scalar table parser for VESTA atom
  coloring; next likely targets after push are higher-level charged-state cube
  templates, IGMH fragment command streams, specialized raw Multiwfn atom
  transcript parsers, and more real ABACUS Molden smokes.
- Turn the 2026-06-10 Multiwfn/ABACUS/VESTA research into the next
  maintainable features: IGMH command streams, real-system `abacus-molden`
  smoke coverage, Multiwfn atom scalar parsers, and more real IRI/RDG
  templates.  The first maintained IRI/RDG runner now exists as
  `multiwfn2vesta iri-run`.
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

- Implemented batch `orbital`/`orbital-density` export on top of
  `multiwfn2vesta grid-run`.  Batch mode repeats isolated single-orbital
  Multiwfn main-function-5 runs with one child output directory per orbital
  plus a top-level `multiwfn_grid_batch_recipe.md`.
- `grid-run --orbitals h l l+1` now defaults to `--function orbital` when no
  explicit function is supplied.  `--function orbital-density --orbitals ...`
  exports orbital-density cubes.  `--keep-going` continues after failed
  orbitals; otherwise later orbitals are marked `skipped`.
- Hardened batch argument handling after read-only sub-agent review:
  `--orbitals` rejects `--orbital`, `--commands-file`, `--expected-cube`, and
  `--raw-dir`; `--keep-going` without `--orbitals` is rejected instead of
  being silently ignored.
- Validation for batch orbital export passed: `py_compile` for touched Python
  files, 52 focused tests across `tests.test_multiwfn_grid` and
  `tests.test_cli`, full 163-test no-GUI regression, `grid-run --help`,
  top-level `multiwfn2vesta --help`, and `git diff --check`.
- Committed and pushed batch orbital export to GitHub `main` as
  `dcf7bd3cac0684f48f16ebd06458345b929837fd`
  (`Add batch orbital grid export`).  Post-push verification after
  `git fetch --prune origin`: `HEAD`, `origin/main`, and `origin/HEAD` all
  pointed at `dcf7bd3`; `git ls-remote --heads origin` returned only
  `refs/heads/main`.
- Started `multiwfn2vesta cube-arith`, a maintained compatible-cube linear
  arithmetic workflow for density difference, Fukui functions, and dual
  descriptors.  It supports generic `--term COEFF CUBE` entries and named
  operations `density-difference`, `fukui-plus`, `fukui-minus`, and
  `dual-descriptor`, writes `<stem>.cub` plus a markdown recipe, and
  optionally calls `cube-preset`; `--preset auto` uses `density` for
  `fukui-plus/minus` and `signed` otherwise.
- Integrated `cube-arith` into the unified CLI, aliases `cube-math`,
  `density-diff`, and `fukui-cube`, the interactive menu as item `11`, and
  console script `multiwfn2vesta-cube-arith`.
- Focused validation for the cube arithmetic feature passed: 39
  tests across `tests.test_cube_arith` and `tests.test_cli`, plus
  `py_compile`.
- Real CLI smokes passed under
  `/mnt/g/work/multiwfn2vesta/smoke/cube_arith_smoke_20260610/products_auto_signed/`
  and
  `/mnt/g/work/multiwfn2vesta/smoke/cube_arith_smoke_20260610/products_auto_fukui/`,
  covering auto signed VESTA output and cube-only Fukui output.
- Read-only pre-commit review found and the main thread fixed a real unit
  compatibility issue: `cube-arith` now rejects mixed Bohr/Angstrom cube unit
  conventions by default.
- Full no-GUI regression passed for the cube arithmetic increment: 153 tests
  across the project test suite.
- Committed and pushed the cube arithmetic workflow to GitHub `main` as
  `4123d00ae051a710c954ed3c3712aa8b012c4bc0`
  (`Add cube arithmetic workflow`).  Post-push verification after
  `git fetch --prune origin`: local `main`, `origin/main`, and `origin/HEAD`
  all pointed at `4123d00`; `git ls-remote --heads origin` returned only
  `refs/heads/main`; repository-local identity remained
  `Stardust0831 <13862180016@163.com>`.
- Pushed the first documentation closure as
  `4800cf4b2dbab559d64023852cc3579e7696ad15`
  (`Record cube arithmetic push`).  This docs-only commit preserves the same
  single-branch layout.
- Added `multiwfn2vesta grid-run`, a maintained Multiwfn main-function-5
  (`study3dim`) real-space grid runner.  It discovers Multiwfn, writes the
  exact command stream, stdout/stderr logs, raw cube directory, processed
  `<stem>_<function>.cub`, a markdown recipe, and optionally calls
  `cube-preset`/`cube-vesta` for `.vesta` output.
- `grid-run` currently covers density, gradient, Laplacian, orbital/MO value,
  spin density, nuclear ESP, ELF, LOL, total ESP/MEP, RDG,
  sign(lambda2)rho, Delta-g, IRI, vdW potential, and orbital density.  Orbital
  and orbital-density functions require `--orbital`; unlisted functions can
  be driven with `--function-index` and `--expected-cube`.
- Integrated `grid-run` into the unified CLI, aliases `multiwfn-grid`,
  `scalar-cube-run`, and `function-cube`, the interactive menu as item `10`,
  and console script `multiwfn2vesta-grid-run`.
- Focused unit validation passed for the new runner and CLI entry points: 39
  tests across `tests.test_multiwfn_grid` and `tests.test_cli`.
- Final pre-commit validation passed: `py_compile`, 140-test no-GUI
  regression, `grid-run --list-functions`, `grid-run --help`, top-level
  `multiwfn2vesta --help`, and `git diff --check`.
- Read-only sub-agent review found no blocking issue; the main follow-up
  narrowed the interactive preset prompt to single-cube presets because
  `iri`/`esp` presets require a texture cube.
- Real H2O noGUI density smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_density/products/`.
  Command stream was `5 / 1 / 4 / 12,12,12 / 2 / 0 / q`; Multiwfn returned
  `0`, wrote raw `density.cub`, processed `h2o_density.cub`, and generated
  `h2o_density_density_cube.vesta` plus both recipe files without launching
  VESTA.
- Real H2O noGUI ELF smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_elf/products/`
  with `--function elf --no-vesta`, producing raw `ELF.cub`,
  `h2o_elf.cub`, and a recipe.
- Synced README, usage docs, CLI/cube/ABACUS skill notes, new
  `docs/skills/multiwfn_grid_run_skill.md`, and the ABACUS/Multiwfn/VESTA
  research matrix with the maintained `grid-run` workflow.
- Committed and pushed `grid-run` to GitHub `main` as
  `3d192dc7ae9696dd433aae04e1a3bdb488b95482`
  (`Add Multiwfn grid runner`).  After `git fetch --prune`, `HEAD`,
  `origin/main`, and `origin/HEAD` pointed at that commit; the remote exposed
  only `refs/heads/main`, and repository-local identity remained
  `Stardust0831 <13862180016@163.com>`.
- Rechecked the branch state for the user's README/merge-back follow-up:
  local `main` and `origin/main` both point at
  `17667f2a1a7380fb7a2c2495f9df04ef633e0577`, and
  `git ls-remote --heads origin` returns only `refs/heads/main`.  There is
  no feature branch to merge back in this pass.
- Confirmed repository-local commit identity remains
  `Stardust0831 <13862180016@163.com>`.
- Updated README branch-maintenance notes with the current verified commit,
  expected one-branch remote state, maintainer identity commands, and the
  future fast-forward merge pattern for short-lived experiment branches.
- Committed and pushed the README branch follow-up to GitHub `main` as
  `41bfc9ce691b8de195a69566b56ac84df335947b`
  (`Refresh README branch follow-up`).  After push, `HEAD`, `origin/main`,
  and `origin/HEAD` pointed at that commit; the separate
  `src/multiwfn2vesta/multiwfn_grid.py` draft remained untracked and was not
  part of the branch-cleanup commit.
- Rechecked README/branch state for the user's 2026-06-10 cleanup request:
  after `git fetch --prune`, the project has local `main`, `origin/main`,
  and `origin/HEAD -> origin/main`; `git ls-remote --heads origin` reports
  only `refs/heads/main`.  There is no extra local or remote feature branch
  to merge back.
- Updated README repository-status notes so the current branch state is
  explicit: the historical experiment work is already represented as commits
  on `main`, future experiment branches should be short-lived, and
  repository-local commit identity remains
  `Stardust0831 <13862180016@163.com>`.
- Validated the README/docs-only update with `git diff --check` and
  `bin/multiwfn2vesta --help`, committed the README refresh as `dec8150`
  (`Refresh README branch status`), and pushed it to GitHub `main`.
  A final docs-only closure commit may sit after `dec8150`.
- Added `multiwfn2vesta iri-run`, a maintained Multiwfn IRI/RDG command-stream
  wrapper.  It discovers Multiwfn, writes the exact command stream and logs,
  runs in `multiwfn_iri_raw/`, preserves raw `func1.cub`/`func2.cub`, writes
  processed `<stem>_IRI1.cub` and `<stem>_IRI2.cub`, and calls
  `cube-preset iri` to write a mapped-surface `.vesta` unless `--no-vesta`
  is supplied.
- Integrated `iri-run` into the unified CLI, aliases `multiwfn-iri` and
  `rdg-run`, the interactive menu, and console script
  `multiwfn2vesta-iri-run`.
- Hardened `iri-run` failure handling after read-only pre-commit review:
  missing Multiwfn/input paths return a stable CLI error, Multiwfn nonzero
  exits report an `ERROR:` with log paths, and timeouts/launch failures write
  partial logs instead of traceback.
- Smoke-tested real H2O noGUI IRI/RDG under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_iri_run_smoke_20260610/`.
  The run generated raw `func1.cub`/`func2.cub`, processed `h2o_IRI1.cub` and
  `h2o_IRI2.cub`, and wrote `h2o_iri_cube.vesta` plus recipe without
  launching VESTA.
- Synced README, usage docs, IRI/cube/CLI skill notes, ABACUS/Multiwfn
  planning notes, research matrix, and root/project work records with the
  maintained IRI/RDG runner.
- Focused validation passed: 36 tests across `tests.test_multiwfn_iri`,
  `tests.test_cli`, and `tests.test_iri_cube`, plus `py_compile` for
  `multiwfn_iri.py` and `cli.py`.
- Full no-GUI regression passed: 118 tests across Molden checking, ABACUS
  Molden/Mulliken, cube preset, Multiwfn IRI, cube-to-VESTA, unified CLI,
  AIM+IGMH, executable discovery, Multiwfn AIM, IRI cube handling, AIM VESTA
  conversion, and VESTA atom coloring.  `multiwfn2vesta iri-run --help`,
  top-level `multiwfn2vesta --help`, and `git diff --check` also passed.
- Feature implementation commit was pushed to GitHub `main` at
  `16f345c76053454cdca026d707f885383d9122c3`
  (`Add Multiwfn IRI runner`), and `HEAD` matched `origin/main` after
  `git fetch origin main`.
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
- Feature implementation commit for cube preset was pushed to GitHub `main` at
  `c58600d3b4f276c43eef4095669b6402835df8ff`
  (`Add cube analysis presets`).
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
