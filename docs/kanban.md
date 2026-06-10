# Project Kanban

Updated: 2026-06-10 23:28 CST

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
  `0123dim.f90` exports it as `infoentro.cub`; Fermi hole/source function/EDR
  were deferred at that time because they needed reference points or extra
  EDR parameters.  EDR/D(r) was later implemented in the 2026-06-10 EDR and
  orbital-overlap distance increment above; reference-point functions remain
  deferred.
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
## Incoming Request: 2026-06-10 README and Branch Hygiene

- [x] Record user request: update README, inspect unusual branch state, merge/consolidate back to one branch where appropriate, and use identity `Stardust0831`.
- [ ] Inspect current branch/remote/status without disturbing existing work.
- [ ] Finish or reconcile in-progress documentation/code edits before README update.
- [ ] Update README and mirrored docs consistently.
- [ ] Validate, review, commit, and push with `Stardust0831` identity.
