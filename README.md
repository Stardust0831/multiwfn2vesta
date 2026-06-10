# multiwfn2vesta

`multiwfn2vesta` is a workspace-local Python interface for running selected
Multiwfn workflows and preparing VESTA visualization files.  The currently
maintained path covers ABACUS Molden handoff, cube-to-VESTA files, Multiwfn
real-space grid, AIM, IRI/RDG, and IGM/IGMH command streams, atoms-only topology
overlays, surface extrema overlays, and AIM+IGMH multi-phase VESTA figures.

The project is still experimental, but the CLI below is the maintained entry
point.

## Repository Status

- Maintained branch: `main`; this is the only branch currently exposed by the
  GitHub remote.
- GitHub remote: `origin` points to `Github:Stardust0831/multiwfn2vesta.git`,
  with `origin/HEAD -> origin/main`.
- Branch audit on 2026-06-10 15:16 CST, after `git fetch --prune origin`,
  found local `main`, `origin/main`, and `origin/HEAD` aligned at
  `b99d80e2d3879eb7dbad260e4b8722c50427ad98`.
- `git ls-remote --heads origin` currently returns only
  `refs/heads/main`, also at `b99d80e`; no merge-back was needed in this pass
  because there is no extra local or remote feature branch to consolidate.
- The apparently unusual branch history is a normal linear `main` history
  containing feature commits and documentation closure commits, not active
  competing branches.
- Recent maintained feature work includes IGM/mIGM/IGMH command-stream automation,
  IGMH/aIGM VESTA cube presets, surface extrema overlays for
  `surfanalysis.pdb`, surface-map/grid expansion, generic Multiwfn atom table
  coloring, batch orbital export, `cube-arith`, `grid-run`, and
  `grid-run --surface-cube` mapped-surface handoff.
- Future experiment branches should be short-lived: merge or fast-forward the
  useful commits into `main`, then remove the experiment branch once
  `origin/main` contains the maintained result.
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

At the time of the branch audit, the remote-head output contained only
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
  such as density, orbitals/wavefunctions, ELF/LOL, IRI/RDG/NCI, ESP/MEP,
  IGM/IGMH/aIGM weak-interaction maps, ALIE/LEA/LEAE, and vdW-potential
  mapped surfaces.
- Overlay Multiwfn molecular-surface extrema from `surfanalysis.pdb` onto
  mapped-surface VESTA files as an extra atoms-only phase, with automatic
  minima/maxima selection for ALIE/LEA/LEAE presets.
- Combine compatible cube files with linear arithmetic for density
  differences, Fukui functions, and dual descriptors, then optionally write a
  VESTA file through `cube-preset`.
- Run Multiwfn IRI/RDG cube generation from a wavefunction file, process
  `func1.cub`/`func2.cub` into VESTA-ready `IRI1`/`IRI2` cubes, and write a
  mapped-surface `.vesta` through `cube-preset iri`.
- Run Multiwfn IGM, mIGM, or IGMH fragment analysis from a wavefunction file
  and fragment definitions, export `dg_inter.cub` plus `sl2r.cub`, preserve
  optional `dg_intra.cub`/`dg.cub`, and write a mapped-surface `.vesta`
  through `cube-preset igm`/`igmh`.
- Run Multiwfn main function `5` real-space grid generation from a
  wavefunction file, export density, orbital/MO, Laplacian, K(r)/G(r)
  kinetic-energy-density cubes, ELF, LOL, ESP/MEP, ALIE, RDG/IRI-like,
  promolecular RDG/sign(lambda2)rho, and related scalar cubes, export
  multiple orbitals through isolated batch runs, optionally write VESTA files
  through `cube-preset`, and map generated ESP/ALIE/vdW/sign(lambda2)rho
  cubes as textures on a provided density/surface cube.
- Color VESTA atom/site styles from ABACUS `mulliken.txt` charge or
  magnetism values produced by `out_mul 1`, or from generic Multiwfn-style
  atom scalar tables such as charges, Fukui-like atom values, or atom
  contribution tables.
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
multiwfn2vesta surface-extrema input.vesta surfanalysis.pdb output.vesta \
  --surface-cube density.cub
multiwfn2vesta iri-run input.molden iri_products --timeout 300
multiwfn2vesta igmh-run input.molden igmh_products \
  --fragment 1-48 --fragment 49-60 \
  --grid-mode spacing --grid-spacing 0.25
multiwfn2vesta igm-run input.molden igm_products \
  --fragment 1-48 --fragment 49-60 \
  --grid-mode spacing --grid-spacing 0.25
multiwfn2vesta grid-run input.molden grid_products --function density
multiwfn2vesta grid-run input.molden esp_map \
  --function esp \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub
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
multiwfn2vesta cube-preset igmh dg_inter.cub cube_products \
  --texture-cube sl2r.cub
multiwfn2vesta cube-preset esp density.cub cube_products \
  --texture-cube esp.cub \
  --tex-physical -0.05 0.05
multiwfn2vesta cube-preset alie density.cub cube_products \
  --texture-cube avglocion.cub \
  --surfanalysis-pdb surfanalysis.pdb
multiwfn2vesta cube-preset vdw-surface density.cub cube_products \
  --texture-cube vdW.cub
```

Available presets can be listed with `multiwfn2vesta cube-preset
--list-presets`.  Current presets cover density-like scalar cubes, signed
orbital/wavefunction/density-difference cubes, ELF/LOL cubes, IRI/RDG/NCI
mapped surfaces, IGM/IGMH/aIGM weak-interaction mapped surfaces, ESP/MEP
mapped density surfaces, generic molecular surface maps, ALIE/LEA/LEAE
density-surface maps, and vdW-potential density-surface maps.  The recipe
records the requested preset, canonical preset, effective
isosurface, texture scaling source, and explicit texture percentage overrides
when they are used.  The `surface-map`/`molsurfmap` defaults follow the
bundled Multiwfn `molsurfmap.vmd` template.

When Multiwfn main function `12` has exported `surfanalysis.pdb`,
`cube-preset --surfanalysis-pdb` embeds surface maxima/minima as an extra
atoms-only phase.  Multiwfn writes maxima as carbon records and minima as
oxygen records; the maintained overlay labels them `MAX0001`/`MIN0001`,
styles maxima red and minima blue, clears overlay bonds, and sets `COMPS 0`
for the multi-phase file.  With `--surf-extrema auto`, `alie` and `leae`
show minima, `lea` shows maxima, and other mapped-surface presets show all
extrema.  Existing VESTA files can be patched directly:

```bash
multiwfn2vesta surface-extrema input.vesta surfanalysis.pdb output.vesta \
  --surface-cube density.cub \
  --selection all
```

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
  `--orbital` for one orbital or `--orbitals` for batch export.
- `orbital-density` / `orbdens`: function `44`, raw `orbdens.cub`, preset
  `density`, requires `--orbital` for one orbital or `--orbitals` for batch
  export.
- `hamiltonian-ked` / `k(r)`: function `6`, raw `K(r).cub`, signed by
  default.  `lagrangian-ked` / `g(r)`: function `7`, raw `G(r).cub`, density
  style by default.
- `laplacian`, `spin-density`, `esp`, `nuclear-esp`, `signlambda2rho`, and
  `vdw-potential`: signed scalar fields, defaulting to the `signed` preset;
  with `--surface-cube`, `esp`/`nuclear-esp` map through `cube-preset esp`,
  `signlambda2rho` maps through `cube-preset iri`, and `vdw-potential` maps
  through `cube-preset vdw-map`.
- `elf` and `lol`: localization cubes, defaulting to `cube-preset elf/lol`.
- `alie` / `avglocion`: function `18`, raw `avglocion.cub`.  With
  `--surface-cube density.cub`, the generated ALIE cube is used as the
  texture for `cube-preset alie`.
- `rdg`, `promolecular-rdg`, `signlambda2rho`,
  `promolecular-signlambda2rho`, `iri`, and `delta-g`: single scalar cubes;
  IRI/RDG mapped surfaces that need two coupled cubes should still use
  `iri-run` or explicit `cube-preset iri`.

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

For mapped-surface figures, pass a compatible density/surface cube.  The
generated grid cube is then used as the texture cube in `cube-preset`:

```bash
multiwfn2vesta grid-run input.fch esp_map \
  --function esp \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub

multiwfn2vesta grid-run input.fch alie_map \
  --function alie \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub
```

With `--preset auto`, mapped defaults are `esp` for ESP/nuclear ESP, `alie`
for ALIE, `iri` for sign(lambda2)rho, `vdw-map` for vdW potential, and
`surface-map` for other functions.  Batch orbital export rejects
`--surface-cube`.

For frontier-orbital batches, use `--orbitals`.  If `--function` is omitted in
batch mode, it defaults to `orbital`; use `--function orbital-density` for
orbital-density cubes:

```bash
multiwfn2vesta grid-run input.molden orbital_products \
  --orbitals h l l+1 \
  --grid-mode points \
  --grid-points 80 80 80 \
  --no-vesta
```

Batch mode is intentionally implemented as repeated single-orbital runs, not
as a single Multiwfn batch menu.  Each orbital gets its own output directory,
command stream, logs, raw cube directory, processed cube, and optional VESTA
file.  The top-level `multiwfn_grid_batch_recipe.md` records requested
orbitals, safe labels, run status, skipped orbitals, and child paths.

Default batch outputs in `orbital_products/`:

- `multiwfn_grid_batch_recipe.md`.
- `001_orbital_h/`, `002_orbital_l/`, `003_orbital_lplus1/`, etc.
- inside each child directory: `multiwfn_grid_input.txt`, stdout/stderr logs,
  `multiwfn_grid_raw/<Multiwfn-default>.cub`, processed
  `<stem>_<orbital>_<function>.cub`, and optional VESTA files.

The batch command stops after the first failed orbital by default.  Add
`--keep-going` to continue later orbitals and record failed/skipped states in
the batch manifest.  Batch mode rejects `--orbital`, `--commands-file`,
`--expected-cube`, and `--raw-dir`, because each child run owns its own command
stream and raw output directory.

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
- `smoke/multiwfn_grid_surface_cube_map_20260610/h2o_esp_map/`: function
  `esp`, grid reused from `h2o_density.cub`, generated `h2o_esp.cub` and
  `h2o_esp_esp_cube.vesta` as a density-surface ESP texture map.

Each `grid-run` child run still produces one new scalar cube.  For two-cube
texture figures, use `--surface-cube` when that generated cube should color a
pre-existing surface; otherwise use explicit `cube-preset`/`cube-vesta`, or a
workflow-specific runner such as `iri-run` or `igmh-run`.

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

## Wavefunction to IGM/IGMH VESTA

For wavefunction inputs accepted by Multiwfn, `igmh-run` drives main function
`20`, records the fragment command stream, and then reuses the maintained
`cube-preset igmh`/`igm` writer.  The default method is IGMH.  Use the fixed
wrapper commands `igm-run` and `migm-run` for those methods, or use the
generic `igmh-run --method igm|migm|igmh` form when the method must be chosen
explicitly.  The wrapper commands reject an extra `--method` so the command
name cannot silently disagree with the generated Multiwfn stream:

```bash
multiwfn2vesta igmh-run input.molden igmh_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --grid-mode spacing \
  --grid-spacing 0.25 \
  --timeout 600

multiwfn2vesta migm-run input.molden migm_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --sl2r-source actual \
  --grid-mode spacing \
  --grid-spacing 0.25
```

Default outputs in `igmh_products/`, with `igmh` replaced by `igm` or `migm`
for those methods:

- `multiwfn_igmh_input.txt`
- `multiwfn_igmh.stdout.txt`
- `multiwfn_igmh.stderr.txt`
- `multiwfn_igmh_raw/dg_inter.cub`
- `multiwfn_igmh_raw/sl2r.cub`
- `<stem>_dg_inter.cub`
- `<stem>_sl2r.cub`
- `<stem>_dg_intra.cub` and `<stem>_dg.cub` when Multiwfn writes them
- `<stem>_<method>_cube.vesta`
- `<stem>_<method>_cube_vesta_recipe.md`

Fragments are passed as Multiwfn atom-index strings, so ranges such as
`1-48`, lists such as `1,4,9`, and complement-style inputs such as `c` can be
used when they are accepted by the corresponding Multiwfn prompt.  Useful grid
modes are `low`, `medium`, `high`, `points`, `spacing`, `cube`, and
`pbc-cell`.  `points` is only safe for finite non-PBC inputs; when a Molden
file contains `[Cell]`, the runner rejects `points` before launching Multiwfn
because the PBC menu interprets option `4` as grid spacing.  Use
`--grid-mode spacing --grid-spacing VALUE` or `--grid-mode pbc-cell` for
ABACUS periodic Molden files.

`igmh-run` discovers Multiwfn the same way as `iri-run`, sets
`Multiwfnpath`/`MULTIWFNPATH`/`MultiwfnPATH`, and does not launch VESTA.  Pass
`--no-vesta` if only the Multiwfn cubes are needed.  The top-level alias
`multiwfn2vesta igmh` intentionally remains the AIM+IGMH overlay styler;
use `igmh-run`, `igm-run`, or `migm-run` for the Multiwfn fragment run.

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

## Multiwfn Atom Table Coloring

For atom scalar values copied or exported from Multiwfn, or prepared manually
from Multiwfn analyses, use the generic table parser:

```bash
multiwfn2vesta multiwfn-atom-color \
  structure.vesta \
  atom_values.txt \
  structure_atom_values.vesta \
  --value-column charge \
  --vmin -1 --vmax 1 \
  --write-values parsed_atom_values.csv
```

Accepted inputs are CSV, TSV, or whitespace text.  A typical Multiwfn-like
table can be:

```text
Atom Label Charge
1 C1 -0.12
2 H1  0.08
```

Header names such as `Atom`, `index`, `label`, `charge`, `value`, `fukui`,
`dual`, `contribution`, and `weight` are recognized.  Use `--value-column`
when a table has multiple numeric columns.  Use `--key-column` when the key
column is not obvious.  Tables may also be one ordered value per line, in
which case strict mode requires the row count to match the selected VESTA
`STRUC` section.  As with ABACUS Mulliken coloring, this patches VESTA
`SITET` RGB values; VESTA will not know the original scalar values or create a
native colorbar.

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

Current no-GUI regression passed as a 212-test suite at the audited
`b99d80e` tip:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

For documentation-only refreshes, the minimum local validation is:

```bash
git diff --check
bin/multiwfn2vesta --help
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

The maintained Multiwfn atom table parser is unit-tested with CSV, TSV, and
whitespace table shapes through `tests.test_multiwfn_atom_table`; it reuses
the same VESTA `SITET` RGB patching backend as ABACUS Mulliken coloring.

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

Smoke-tested IGMH cube preset on the Ag(111)+benzene products:

```text
/mnt/g/work/multiwfn2vesta/smoke/igmh_preset_20260610_1128/products/
```

It generated `dg_inter_igmh_cube.vesta` from `dg_inter.cub` plus
`sl2r.cub`, using the Multiwfn `IGM_inter.vmd` defaults: isosurface `0.01`
and texture physical range `-0.05` to `0.05`, without launching VESTA.

Smoke-tested Multiwfn noGUI IGMH run:

```text
/mnt/g/work/multiwfn2vesta/smoke/multiwfn_igmh_run_smoke_20260610/h2o/
```

This H2O run used fragments `1` and `2-3`, grid `8 x 8 x 8`, produced raw
`dg_inter.cub`/`sl2r.cub` plus optional `dg_intra.cub`/`dg.cub`, and wrote
`h2o_igmh_cube.vesta` plus a recipe without launching VESTA.

Smoke-tested Multiwfn noGUI IGM and mIGM runs:

```text
/mnt/g/work/multiwfn2vesta/smoke/multiwfn_igm_migm_run_smoke_20260610_review_fix/
```

The H2O IGM and mIGM runs used fragments `1` and `2-3`, grid `8 x 8 x 8`,
produced `h2o_igm_cube.vesta` and `h2o_migm_cube.vesta`, confirmed
method-specific recipe titles, and did not launch the VESTA UI.

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
- `docs/skills/igmh_vesta_preset_skill.md`: Multiwfn IGM/IGMH/aIGM cube
  preset notes.
- `docs/skills/multiwfn_igmh_run_skill.md`: Multiwfn IGM/mIGM/IGMH command-stream
  runner notes.
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
