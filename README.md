# multiwfn2vesta

`multiwfn2vesta` is a workspace-local Python interface for running selected
Multiwfn workflows and preparing VESTA visualization files.  The currently
maintained path covers ABACUS Molden handoff, cube-to-VESTA files, Multiwfn
real-space grid, AIM, and IRI/RDG command streams, atoms-only topology
overlays, and AIM+IGMH multi-phase VESTA figures.

The project is still experimental, but the CLI below is the maintained entry
point.

## Repository Status

- Maintained branch: `main`.
- GitHub remote: `origin` points to `Github:Stardust0831/multiwfn2vesta.git`,
  with `origin/HEAD -> origin/main`.
- Latest local/remote branch audits on 2026-06-10 confirmed the same branch
  layout: local `main` tracks `origin/main`, `origin/HEAD` points to
  `origin/main`, and `git ls-remote --heads origin` returns only
  `refs/heads/main`.
- Current cleanup result on 2026-06-10: there is no extra local or remote
  feature branch to merge back, so no merge action is required.  The
  apparently strange branch history is already represented as commits on
  `main`.
- Latest maintained feature push on 2026-06-10: `cube-arith` was committed and
  pushed as `4123d00ae051a710c954ed3c3712aa8b012c4bc0`
  (`Add cube arithmetic workflow`).  It added compatible-cube arithmetic for
  density differences, Fukui functions, and dual descriptors, with CLI/docs,
  tests, smoke evidence, and the unit-convention guard for mixed Bohr/Angstrom
  cube headers.
- The first documentation closure for that feature was pushed as
  `4800cf4b2dbab559d64023852cc3579e7696ad15`
  (`Record cube arithmetic push`).  Later docs-only commits may advance
  `main`, but they do not introduce extra branches.
- Previous maintained feature push on 2026-06-10: `grid-run` was committed as
  `3d192dc7ae9696dd433aae04e1a3bdb488b95482`
  (`Add Multiwfn grid runner`) and closed with documentation commit
  `9c9a43b402164044f32d94ad2c49f018d13e2b6f`
  (`Record grid runner push`).
- Previous experiment branches should be treated as short-lived workspaces:
  merge or fast-forward the useful commits into `main`, then remove the
  experiment branch once `origin/main` contains the maintained result.
- Repository-local commit identity is
  `Stardust0831 <13862180016@163.com>`.

Maintainer branch check and one-branch closeout:

```bash
git config user.name Stardust0831
git config user.email 13862180016@163.com
git fetch --prune origin
git status --short --branch
git branch --all --verbose --no-abbrev
git ls-remote --heads origin
```

At the time of this README refresh, the expected remote-head output is only
`refs/heads/main`.  If a future experiment branch appears, keep all final
project code, tests, and docs on `main` before pushing a release-style state:

```bash
git switch main
git pull --ff-only origin main
git merge --ff-only <experiment-branch>
git push origin main
```

If a fast-forward merge is impossible, make a normal reviewed merge commit on
`main` with the same `Stardust0831` identity, run the no-GUI tests, and only
then delete the temporary branch.

## Maintained Features

- Discover workspace, environment, and `PATH` executables for Multiwfn and
  VESTA.
- Generate ABACUS LCAO Molden files by exporting the latest ABACUS
  `interfaces/Multiwfn_interface/molden.py`, recording the source commit, and
  validating the result for Multiwfn use.
- Check Molden files before Multiwfn workflows, including ABACUS-specific
  `[Cell]` and `[Nval]` requirements.
- Create VESTA `.vesta` files directly from ABACUS or Multiwfn scalar cube
  files, with optional texture/color cube support, surface-band texture
  scaling, and signed positive/negative isosurface presets.
- Apply analysis-oriented cube presets for common ABACUS/Multiwfn products
  such as density, orbitals/wavefunctions, ELF/LOL, IRI/RDG/NCI, and ESP/MEP
  mapped surfaces.
- Combine compatible cube files with linear arithmetic for density
  differences, Fukui functions, and dual descriptors, then optionally write a
  VESTA file through `cube-preset`.
- Run Multiwfn IRI/RDG cube generation from a wavefunction file, process
  `func1.cub`/`func2.cub` into VESTA-ready `IRI1`/`IRI2` cubes, and write a
  mapped-surface `.vesta` through `cube-preset iri`.
- Run Multiwfn main function `5` real-space grid generation from a
  wavefunction file, export density, orbital/MO, Laplacian, ELF, LOL,
  ESP/MEP, RDG/IRI-like, and related scalar cubes, and optionally write a
  VESTA file through `cube-preset`.
- Color VESTA atom/site styles from ABACUS `mulliken.txt` charge or
  magnetism values produced by `out_mul 1`.
- Run Multiwfn AIM topology analysis from a wavefunction file such as
  `.molden`, `.fch`, `.fchk`, `.wfn`, or `.wfx`.
- Convert Multiwfn `paths.pdb` and `CPs.pdb` to an atoms-only `.vesta` file
  with AIM bonds disabled.
- Style saved AIM+IGMH multi-phase `.vesta` overlays with one yellow path
  pseudo-element, orange BCPs, optional BCP labels, and optional three-view
  export.
- Keep VESTA rendering explicit because the Windows VESTA automation route can
  still steal desktop focus.

## Quick Start

From this repository:

```bash
cd /mnt/g/work/multiwfn2vesta/project
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH
multiwfn2vesta --help
```

The workspace launcher automatically adds `src/` to Python's import path.  An
editable install also provides console scripts:

```bash
pip install -e .
multiwfn2vesta --help
```

The supported day-to-day entry point is the global `multiwfn2vesta` command.
Avoid running package modules from inside `src/multiwfn2vesta`; from the repo
root, either add `project/bin` to `PATH` as above or run with
`PYTHONPATH=src python3 -m multiwfn2vesta.cli`.

## Find Multiwfn and VESTA

```bash
multiwfn2vesta discover
multiwfn2vesta abacus-molden abacus_calc ABACUS_Multiwfn.molden
multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus
multiwfn2vesta cube-preset --list-presets
multiwfn2vesta cube-arith products --operation dual-descriptor \
  --anion-cube anion_density.cub \
  --neutral-cube neutral_density.cub \
  --cation-cube cation_density.cub
multiwfn2vesta iri-run input.molden iri_products --timeout 300
multiwfn2vesta grid-run input.molden grid_products --function density
```

Multiwfn discovery checks, in order:

1. Explicit `--multiwfn` paths for commands that accept it.
2. `MULTIWFN_PATH`, `MULTIWFNPATH`, `Multiwfnpath`, `MultiwfnPATH`,
   `MultiwfnPath`, `MULTIWFN_EXECUTABLE`.
3. Workspace-local tools, preferring
   `tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI`.
4. Shell `PATH`.

VESTA discovery checks:

1. Explicit VESTA render options such as `--vesta-dir`.
2. `VESTA_PATH`, `VESTA_DIR`, `VESTAPATH`, `VestaPATH`, `Vestapath`,
   `VESTA_EXECUTABLE`.
3. Workspace-local VESTA tools.
4. Shell `PATH`.

## Cube to VESTA

For direct ABACUS cubes such as charge density, potential, ELF, partial charge,
or real-space wavefunction cubes, and for Multiwfn-generated scalar cubes:

```bash
multiwfn2vesta cube-vesta density.cub cube_products --isosurface 0.01
```

For signed scalar fields such as real orbital amplitudes, real wavefunction
cubes, density differences, or dual-descriptor style cubes:

```bash
multiwfn2vesta cube-vesta orbital.cub cube_products \
  --surface-mode signed \
  --isosurface 0.02
```

In signed mode, `--isosurface X` is treated as a magnitude.  The generated
`ISURF` block contains `+abs(X)` in yellow and `-abs(X)` in blue by default.
Both levels must be inside the cube data range.

For a surface cube colored by a compatible texture cube:

```bash
multiwfn2vesta cube-vesta IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub \
  --isosurface 1.0 \
  --tex-physical -0.04 0.04
```

For IRI/RDG/ESP style mapped surfaces, the color range can be derived from
texture values near the requested surface instead of the whole texture cube:

```bash
multiwfn2vesta cube-vesta IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub \
  --isosurface 1.0 \
  --tex-physical -0.04 0.04 \
  --tex-range-source surface-band
```

The command writes a `.vesta` file, copies cube dependencies beside it by
default, and writes a markdown recipe.  `SECTS 0 0` is the default to avoid
VESTA section planes.  `TEX3P` is written as VESTA percentage/normalized
values, not direct physical scalar limits.

For common analysis products, `cube-preset` applies maintained defaults on
top of the same `cube-vesta` backend:

```bash
multiwfn2vesta cube-preset orbital orbital.cub cube_products
multiwfn2vesta cube-preset elf ELF.cub cube_products
multiwfn2vesta cube-preset rdg IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub
multiwfn2vesta cube-preset esp density.cub cube_products \
  --texture-cube esp.cub \
  --tex-physical -0.05 0.05
```

Available presets can be listed with `multiwfn2vesta cube-preset
--list-presets`.  Current presets cover density-like scalar cubes, signed
orbital/wavefunction/density-difference cubes, ELF/LOL cubes, IRI/RDG/NCI
mapped surfaces, and ESP/MEP mapped density surfaces.  The recipe records the
requested preset, canonical preset, effective isosurface, texture scaling
source, and explicit texture percentage overrides when they are used.

## Cube Arithmetic

`cube-arith` linearly combines compatible cube files and can send the result
to `cube-preset`.  This is the maintained bottom layer for density
differences, Fukui functions, and dual descriptors.  It does not compute the
underlying charged-state or excited-state wavefunctions; generate those cubes
first with ABACUS, Multiwfn, or `grid-run`.

Generic linear combination:

```bash
multiwfn2vesta cube-arith cube_arith_products \
  --term 1.0 cube_a.cub \
  --term -1.0 cube_b.cub \
  --stem density_difference
```

Common shortcuts:

```bash
multiwfn2vesta cube-arith cube_arith_products \
  --operation fukui-plus \
  --anion-cube density_Nplus1.cub \
  --neutral-cube density_N.cub

multiwfn2vesta cube-arith cube_arith_products \
  --operation fukui-minus \
  --neutral-cube density_N.cub \
  --cation-cube density_Nminus1.cub

multiwfn2vesta cube-arith cube_arith_products \
  --operation dual-descriptor \
  --anion-cube density_Nplus1.cub \
  --neutral-cube density_N.cub \
  --cation-cube density_Nminus1.cub
```

The formulae are:

- `density-difference`: `plus - minus`
- `fukui-plus`: `rho(N+1) - rho(N)`
- `fukui-minus`: `rho(N) - rho(N-1)`
- `dual-descriptor`: `rho(N+1) - 2*rho(N) + rho(N-1)`

All input cubes must share grid origin, grid vectors, point counts, and cube
unit convention.  With `--cube-units auto`, ordinary positive grid counts are
treated as Bohr and negative grid counts as Angstrom; mixed conventions are
rejected by default.  Atom lists must also match by default.  Use
`--no-strict-atoms` only when you have a deliberate atom-list mismatch but
still trust the shared grid.  The command refuses to overwrite any input cube.
Default outputs are `<stem>.cub`, `<stem>_cube_arith_recipe.md`, and, unless
`--no-vesta` is used, a VESTA file plus recipe.  `--preset auto` uses
`density` for `fukui-plus/minus` and `signed` for `density-difference`,
`dual-descriptor`, and generic linear combinations.

## Wavefunction to Scalar Cube VESTA

For wavefunction inputs accepted by Multiwfn, `grid-run` drives Multiwfn main
function `5` (`study3dim`) to export a real-space function cube, then can pass
the cube to `cube-preset`:

```bash
multiwfn2vesta grid-run input.molden grid_products \
  --function density \
  --grid-points 40 40 40 \
  --timeout 300
```

List maintained function aliases and Multiwfn default cube names with:

```bash
multiwfn2vesta grid-run --list-functions
```

Common functions:

- `density` / `rho`: Multiwfn function `1`, raw `density.cub`, preset
  `density`.
- `orbital` / `mo`: function `4`, raw `MOvalue.cub`, preset `signed`, requires
  `--orbital`.
- `orbital-density` / `orbdens`: function `44`, raw `orbdens.cub`, preset
  `density`, requires `--orbital`.
- `laplacian`, `spin-density`, `esp`, `nuclear-esp`, `signlambda2rho`, and
  `vdw-potential`: signed scalar fields, defaulting to the `signed` preset.
- `elf` and `lol`: localization cubes, defaulting to `cube-preset elf/lol`.
- `rdg`, `iri`, and `delta-g`: single scalar cubes; IRI/RDG mapped surfaces
  that need two coupled cubes should still use `iri-run` or explicit
  `cube-preset iri`.

Grid setup defaults to explicit point counts:

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function elf \
  --grid-mode points \
  --grid-points 120 120 120
```

For comparable overlays, reuse an existing cube grid:

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function esp \
  --grid-mode cube \
  --grid-cube density.cub \
  --no-vesta
```

Default outputs in `grid_products/`:

- `multiwfn_grid_input.txt`: exact command stream sent to Multiwfn.
- `multiwfn_grid.stdout.txt` and `multiwfn_grid.stderr.txt`.
- `multiwfn_grid_raw/<Multiwfn-default>.cub`.
- `<stem>_<function>.cub`.
- `multiwfn_grid_recipe.md`.
- `<stem>_<function>_<preset>_cube.vesta` and recipe, unless `--no-vesta` is
  used.

Validated H2O noGUI smokes:

- `smoke/multiwfn_grid_run_smoke_20260610_h2o_density/products/`: function
  `density`, grid `12 x 12 x 12`, generated `h2o_density.cub` and
  `h2o_density_density_cube.vesta`.
- `smoke/multiwfn_grid_run_smoke_20260610_h2o_elf/products/`: function `elf`,
  grid `12 x 12 x 12`, generated `h2o_elf.cub` with `--no-vesta`.

`grid-run` is for single-cube real-space functions.  ESP-on-density,
IRI/RDG/NCI color-mapped surfaces, and other two-cube texture figures still
need an explicit surface cube plus texture cube combination through
`cube-preset`/`cube-vesta`, or a workflow-specific runner such as `iri-run`.

## Wavefunction to IRI/RDG VESTA

For wavefunction inputs accepted by Multiwfn, `iri-run` drives the weak
interaction IRI/RDG path, captures the raw Multiwfn outputs, and then reuses
the maintained cube preset writer:

```bash
multiwfn2vesta iri-run input.molden iri_products --timeout 300
```

Default outputs in `iri_products/`:

- `multiwfn_iri_input.txt`
- `multiwfn_iri.stdout.txt`
- `multiwfn_iri.stderr.txt`
- `multiwfn_iri_raw/func1.cub`
- `multiwfn_iri_raw/func2.cub`
- `<stem>_IRI1.cub`: processed color/texture cube
- `<stem>_IRI2.cub`: surface cube
- `<stem>_multiwfn_iri_output.txt` when Multiwfn writes `output.txt`
- `<stem>_iri_cube.vesta`
- `<stem>_iri_cube_vesta_recipe.md`

The default Multiwfn command stream is recorded in
`multiwfn_iri_input.txt`.  Use `--commands-file` to replace it for a different
weak-interaction menu path.  `iri-run` discovers Multiwfn the same way as
`aim-run`, sets `Multiwfnpath`/`MULTIWFNPATH`/`MultiwfnPATH`, and does not
launch VESTA.  Pass `--no-vesta` if only the processed cubes are needed.

## ABACUS Calculation to Molden

For ABACUS LCAO calculations intended for Multiwfn wavefunction workflows,
generate and validate a Molden file with:

```bash
multiwfn2vesta abacus-molden \
  /path/to/abacus_calc \
  /path/to/ABACUS_Multiwfn.molden
```

The wrapper exports `interfaces/Multiwfn_interface/molden.py` from the selected
ABACUS git ref, runs it with an absolute `-o`, writes stdout/stderr logs and a
recipe markdown file, and then runs the same validation as
`molden-check --abacus`.

The upstream ABACUS converter imports `numpy`, `scipy`, and `matplotlib`.
`abacus-molden` checks these modules before launching the converter.  If your
default `python3` does not have them, pass `--python /path/to/python` pointing
at an environment that does.  `--no-dependency-check` only skips this preflight;
it does not remove the converter's real dependency on those packages.

Defaults:

- ABACUS repo: `/mnt/g/work/multiwfn2vesta/downloads/abacus_latest_molden/abacus-develop`
- Git ref: `origin/develop`
- Source path: `interfaces/Multiwfn_interface/molden.py`
- `--with-cell true`
- `--with-Nval true`
- `--with-pseudo false`

Useful refresh/run pattern:

```bash
multiwfn2vesta abacus-molden abacus_calc ABACUS_Multiwfn.molden \
  --fetch \
  --git-ref origin/develop \
  --python /path/to/python-with-numpy-scipy-matplotlib \
  --ngto 7 \
  --rel-r 2 \
  --with-Nval true
```

The ABACUS converter currently requires LCAO output, `INPUT`, `KPT`, `STRU`,
the corresponding `OUT.<suffix>` directory, pseudopotentials, orbital files,
and `out_wfc_lcao 1`.  It supports `nspin=1/2` and single Gamma/one-k-point
workflows; `nspin=4`/SOC and multi-k are not supported by the converter.
ABACUS' NAO-to-GTO conversion may write `.gto` and `.gto.png` files beside the
orbital files, so run it where `orbital_dir` is writable.

## ABACUS Mulliken Atom Coloring

For ABACUS LCAO calculations with `out_mul 1`, ABACUS writes `mulliken.txt`
in the output directory.  Color atoms in an existing `.vesta` by the final
ionic step Mulliken charge:

```bash
multiwfn2vesta abacus-mulliken-color \
  structure.vesta \
  mulliken.txt \
  structure_mulliken_charge.vesta \
  --property charge \
  --vmin -1 --vmax 1
```

For spin-polarized output, color by atomic magnetism:

```bash
multiwfn2vesta abacus-mulliken-color \
  structure.vesta \
  mulliken.txt \
  structure_mulliken_mag.vesta \
  --property magnetism \
  --vmin -4 --vmax 4 \
  --write-values mulliken_values.csv
```

For noncollinear `nspin=4`, use `--property magnetism-x`,
`magnetism-y`, `magnetism-z`, or `magnetism-norm`.  The parser reads all
`--- Ionic Step N ---` blocks and uses the last step by default; pass
`--step N` to choose a specific ionic step.  Values are mapped to VESTA sites
by one-based atom index, which avoids ambiguity when multiple atoms share the
same element label.  Strict mode is the default and requires the selected
VESTA `STRUC` site indices to match the Mulliken atom indices exactly; use
`--non-strict` only when intentionally coloring a subset.

## Wavefunction to AIM VESTA

For ABACUS-generated Molden files, check the file before using it as a
Multiwfn wavefunction input:

```bash
multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus
```

ABACUS mode requires `[Cell]`, `[Atoms]`, `[GTO]`, `[MO]`, and `[Nval]`.
`[Nval]` is required for pseudopotential systems so Multiwfn sees effective
valence nuclear charges instead of all-electron atomic numbers.

Run Multiwfn AIM analysis and convert the generated AIM PDB files:

```bash
multiwfn2vesta aim-run input.molden aim_out --timeout 180
```

Default outputs in `aim_out/`:

- `multiwfn_aim_input.txt`
- `multiwfn.stdout.txt`
- `multiwfn.stderr.txt`
- `paths.pdb`
- `CPs.pdb`
- `CPprop.txt`
- `mol.pdb`
- `aim_atoms_only.vesta`

Use an explicit Multiwfn executable when needed:

```bash
multiwfn2vesta aim-run input.fch aim_out \
  --multiwfn /mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI
```

The runner sets `Multiwfnpath`, `MULTIWFNPATH`, and `MultiwfnPATH` for the
Multiwfn subprocess based on the selected executable directory.  If Multiwfn
returns 0 but does not create `paths.pdb`, the CLI returns exit code `3` unless
`--allow-missing-paths` is supplied.

## Existing AIM PDB to VESTA

If Multiwfn has already produced `paths.pdb` and `CPs.pdb`:

```bash
multiwfn2vesta aim-pdb paths.pdb aim_atoms_only.vesta \
  --cps-pdb CPs.pdb \
  --title "AIM paths and CPs"
```

For overlays on VESTA-opened cube files, shift AIM coordinates into the cube
frame:

```bash
multiwfn2vesta aim-pdb paths.pdb aim_atoms_only_cube_frame.vesta \
  --cps-pdb CPs.pdb \
  --cube-frame-from-cube molecule_IRI2.cub
```

The generated `.vesta` intentionally disables AIM bonds, so VESTA does not
connect dense path points as ordinary chemical bonds.

## AIM+IGMH VESTA Overlay

For a saved VESTA file that already contains a structure/IGMH cube phase and
an imported AIM path/BCP phase:

```bash
multiwfn2vesta aim-igmh input_overlay.vesta products
```

Defaults:

- AIM path samples use one yellow pseudo-element, `Xe`, radius `0.0600`.
- BCPs use orange `Rn`, radius `0.1800`.
- AIM-phase `SBOND` is cleared.
- Real structure bonds are kept.
- BCPs are split into the final phase for visibility.
- Coordinates are not moved and overlapping path samples are not deleted.

Optional native VESTA site labels:

```bash
multiwfn2vesta aim-igmh input_overlay.vesta products --label-bcp-sites
```

Optional three-view rendering:

```bash
multiwfn2vesta aim-igmh input_overlay.vesta products \
  --render-three-views \
  --initial-view top \
  --extra-rotate top x -8 \
  --scale 2
```

Rendering is opt-in because local Windows VESTA automation may still steal
focus.  The maintained three-view renderer opens one `.vesta` once and exports
views by VESTA CLI rotations, rather than writing persistent front/right/top
`.vesta` files.

## Validation

Current focused no-GUI checks pass as a 118-test no-GUI regression set:

```bash
PYTHONPATH=src python3 -m unittest \
  tests.test_molden_check \
  tests.test_abacus_molden \
  tests.test_abacus_mulliken \
  tests.test_cube_preset \
  tests.test_multiwfn_iri \
  tests.test_cube_vesta \
  tests.test_cli \
  tests.test_aim_igmh_vesta \
  tests.test_vesta_aim_overlay_style \
  tests.test_executables \
  tests.test_multiwfn_aim \
  tests.test_iri_cube \
  tests.test_aim_vesta \
  tests.test_vesta_atom_coloring
```

Smoke-tested ABACUS Molden wrapper git export:

```text
/mnt/g/work/multiwfn2vesta/smoke/abacus_molden_wrapper_smoke_20260610/
```

This smoke exports the current ABACUS `origin/develop` converter script into
the smoke directory and records the source path, commit, and SHA256 without
running a full ABACUS conversion.

Smoke-tested ABACUS Mulliken atom coloring:

```text
/mnt/g/work/multiwfn2vesta/smoke/abacus_mulliken_color_smoke_20260610/
```

The smoke used `abacus-mulliken-color` on a two-atom Fe example, selected the
final ionic step, colored Fe1/Fe2 from magnetism `+4/-4`, and wrote
`values.csv` for inspection.

Smoke-tested ABACUS Molden check:

```bash
multiwfn2vesta molden-check \
  /mnt/g/work/multiwfn2vesta/smoke/abacus_server_artifacts_20260606/ag111_benzene/ag111_benzene_lcao_cont3_nval.molden \
  --abacus
```

The Ag(111)+benzene Molden check reported 60 atoms, 566 MO blocks, three
`[Nval]` entries (`Ag=19`, `C=4`, `H=1`), three numeric `[Cell]` rows, and
`Result: OK`.

Smoke-tested H2O-HF cube-to-VESTA run:

```text
/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_cli_smoke_20260610/
```

It generated `h2o_hf_iri_cube.vesta`, copied `h2o_hf_IRI2_surface.cub` and
`h2o_hf_IRI1_color.cub`, set `IMPORT_DENSITY`/`IMPORT_TEXTURE`, disabled
sections with `SECTS 0 0`, and wrote `TEX3P` as a percentage range.

Smoke-tested cube analysis presets:

```text
/mnt/g/work/multiwfn2vesta/smoke/cube_preset_smoke_20260610/
```

The smoke generated a signed orbital-style `.vesta` from the `orbital` alias
and an IRI/RDG texture-mapped `.vesta` from the `rdg` alias, both without
launching VESTA.

Smoke-tested Multiwfn noGUI IRI/RDG run:

```text
/mnt/g/work/multiwfn2vesta/smoke/multiwfn_iri_run_smoke_20260610/
```

This H2O run used the workspace Linux noGUI Multiwfn, produced raw
`func1.cub`/`func2.cub`, processed `h2o_IRI1.cub`/`h2o_IRI2.cub`, and wrote
`h2o_iri_cube.vesta` plus a recipe without launching VESTA.

Smoke-tested Multiwfn noGUI AIM run:

```text
/mnt/g/work/multiwfn2vesta/smoke/multiwfn_aim_cli_smoke_20260610/h2o/
```

This H2O run produced `paths.pdb`, `CPs.pdb`, `CPprop.txt`, `mol.pdb`, logs,
and `aim_atoms_only.vesta` without launching VESTA.

## Documentation Map

- `docs/usage.md`: fuller user guide.
- `docs/skills/multiwfn2vesta_cli_skill.md`: CLI operating notes.
- `docs/skills/cube_vesta_skill.md`: ABACUS/Multiwfn cube to VESTA workflow.
- `docs/skills/iri_vesta_cube_skill.md`: Multiwfn IRI/RDG cube generation and
  VESTA mapped-surface notes.
- `docs/skills/aim_paths_to_vesta_skill.md`: AIM topology to VESTA workflow.
- `docs/skills/aim_igmh_vesta_skill.md`: reusable AIM+IGMH overlay workflow.
- `docs/research/multiwfn_abacus_vesta_analysis_matrix.md`: roadmap for
  Multiwfn analyses that are useful in VESTA, especially ABACUS-driven ones.
- `docs/skills/abacus_multiwfn_vesta_analysis_skill.md`: checklist for choosing
  ABACUS direct-cube, ABACUS Molden, Multiwfn, and VESTA routes.
- `docs/skills/vesta_camera_and_layers_skill.md`: VESTA camera, layers, and
  three-view export notes.
- `docs/worklog.md`: implementation history and smoke results.
- `docs/kanban.md`: current project board.
