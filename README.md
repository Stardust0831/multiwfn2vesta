# multiwfn2vesta

`multiwfn2vesta` is a workspace-local Python interface for running selected
Multiwfn workflows and preparing VESTA visualization files.  The currently
maintained path covers ABACUS Molden handoff, cube-to-VESTA files, Multiwfn
real-space grid, charged-state Fukui/dual-descriptor maps, STM/LDOS,
cube-domain extraction, basin cube display, AIM, IRI/RDG, and IGM/IGMH
command streams, aIGM/amIGM trajectory-average weak-interaction maps,
atoms-only topology overlays, surface extrema overlays, and AIM+IGMH
multi-phase VESTA figures.

The project is still experimental, but the CLI below is the maintained entry
point.

## Repository Status

- Maintained branch: `main`; this is the only branch currently exposed by the
  GitHub remote.
- GitHub remote: `origin` points to `Github:Stardust0831/multiwfn2vesta.git`,
  with `origin/HEAD -> origin/main`.
- Working checkout: `/mnt/g/work/multiwfn2vesta/project`.  The workspace-level
  `/mnt/g/work/multiwfn2vesta/.git` is an empty metadata stub and is not used
  for project commits.
- Branch audit on 2026-06-11, after `git fetch --prune origin`, found only
  local `main`, `origin/main`, and `origin/HEAD`; `git ls-remote --heads
  origin` returned only `refs/heads/main`.  No merge-back was needed because
  there was no extra local or remote feature branch to consolidate.
- Feature closeouts, including the user-function, spin-polarization,
  ELF/LOL definition-control, vdW-probe, and DORI grid routes, are kept on
  the maintained `main` branch.  Use
  `git log --oneline --decorate -5` after pulling if an exact current commit
  hash is needed.
- Local untracked probe files such as `domain.cub` and `domain.pdb` are not
  part of the maintained branch state and should stay uncommitted unless they
  are explicitly promoted into documented fixtures.
- The apparently unusual branch history is a normal linear `main` history
  containing feature commits and documentation closure commits, not active
  competing branches.
- Recent maintained feature work includes dedicated VESTA presets for
  Multiwfn gradient norm, spin-density, spin-polarization parameter,
  orbital-density, Laplacian, K(r),
  G(r), local information entropy, electron delocalization range EDR(r;d),
  orbital-overlap distance D(r), pair/correlation function, source function,
  Becke atomic/overlap weight, Hirshfeld weight, standalone RDG,
  promolecular RDG, promolecular Delta-g,
  Hirshfeld-partition Delta-g, standalone IRI scalar, standalone DORI scalar
  and DORI+sign(lambda2)rho mapped surfaces, and standalone vdW potential
  cubes with run-local probe-atom control, ABACUS direct cube presets for potential,
  partial-charge, and wavefunction-norm cubes,
  charged-state `fukui-run` orchestration, aIGM/amIGM trajectory-average
  weak-interaction generation, cube/grid domain extraction, basin cube VESTA
  presets,
  IGM/mIGM/IGMH command-stream automation, IGMH/aIGM VESTA cube presets,
  surface extrema overlays for
  `surfanalysis.pdb`, surface-map/grid expansion, generic Multiwfn atom table
  coloring, batch orbital export, `cube-arith`, `grid-run`,
  `grid-run --surface-cube` mapped-surface handoff, `stm-run`
  constant-current STM/LDOS cube export, and earlier AIM/IRI/RDG/AIM+IGMH
  VESTA workflows.
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
  such as density, orbitals/wavefunctions, orbital density, spin density,
  spin-polarization parameter, Laplacian, K(r)/G(r) kinetic-density cubes,
  standalone RDG/promolecular
  RDG, local information entropy, EDR(r;d),
  orbital-overlap distance D(r), Becke atomic/overlap weight, Hirshfeld
  weight, promolecular Delta-g, Hirshfeld-partition Delta-g, standalone IRI
  scalar, standalone vdW potential, ABACUS direct potential, partial charge,
  wavefunction norm cubes, ELF/LOL, IRI/RDG/NCI, DORI, ESP/MEP,
  IGM/IGMH/aIGM weak-interaction maps, ALIE/LEA/LEAE, and vdW-potential
  mapped surfaces.
- Overlay Multiwfn molecular-surface extrema from `surfanalysis.pdb` onto
  mapped-surface VESTA files as an extra atoms-only phase, with automatic
  minima/maxima selection for ALIE/LEA/LEAE presets.
- Combine compatible cube files with linear arithmetic for density
  differences, alpha-minus-beta spin density, Fukui functions, and dual
  descriptors, then optionally write a VESTA file through `cube-preset`.
- Run high-level Fukui/dual-descriptor maps from neutral, anion, and cation
  wavefunction files by generating Multiwfn density cubes on a shared neutral
  grid and then delegating the map arithmetic to `cube-arith`.
- Run Multiwfn IRI/RDG cube generation from a wavefunction file, process
  `func1.cub`/`func2.cub` into VESTA-ready `IRI1`/`IRI2` cubes, and write a
  mapped-surface `.vesta` through `cube-preset iri`.
- Run Multiwfn IGM, mIGM, or IGMH fragment analysis from a wavefunction file
  and fragment definitions, export `dg_inter.cub` plus `sl2r.cub`, preserve
  optional `dg_intra.cub`/`dg.cub`, and write a mapped-surface `.vesta`
  through `cube-preset igm`/`igmh`.
- Run Multiwfn aIGM or amIGM trajectory-average fragment analysis from a
  Multiwfn-readable trajectory such as XYZ, export `avgdg_inter.cub` plus
  `avgsl2r.cub`, optionally preserve `avgRDG.cub`, `thermflu.cub`, and
  scatter data, and write a mapped-surface `.vesta` through `cube-preset
  aigm`/`aigm-tfi`.
- Run Multiwfn main function `5` real-space grid generation from a
  wavefunction file, export density, orbital/MO, spin density,
  spin-polarization parameter, Laplacian, K(r)/G(r) kinetic-energy-density
  cubes, ELF/LOL with run-local `ELFLOL_type` control, ESP/MEP,
  ALIE, RDG/IRI-like,
  promolecular RDG/sign(lambda2)rho, local information entropy, EDR(r;d),
  orbital-overlap distance D(r), pair/correlation functions with run-local
  `pairfunctype`/`paircorrtype`, source function with run-local
  `srcfuncmode`, user-defined `iuserfunc` cubes such as DORI, LEA/LEAE, and
  information-theory densities, Becke atomic/overlap weight, Hirshfeld weight,
  promolecular Delta-g, Hirshfeld-partition Delta-g, vdW potential with
  run-local `ivdwprobe` probe selection, and related scalar cubes, export
  multiple orbitals through
  isolated batch runs, optionally write VESTA files through `cube-preset`,
  and map generated ESP/ALIE/vdW/sign(lambda2)rho cubes as textures on a
  provided density/surface cube.
- Run Multiwfn main function `300` subfunction `4` STM simulation in
  constant-current mode, export raw `STM.cub`, copy it to a stable
  `<stem>_stm.cub`, and write a VESTA isosurface through `cube-preset stm`.
- Run Multiwfn main function `200` subfunction `14` domain analysis from an
  existing cube/grid file, export raw `domain.cub` and `domain.pdb`, copy them
  to stable `<stem>_domain.*` products, and write a binary domain isosurface
  through `cube-preset domain`.
- Display Multiwfn basin-analysis cube exports: individual binary
  `basinNNNN.cub` files through `cube-preset basin`, and signed
  mono-/disynaptic `basinsyn.cub` maps through `cube-preset basin-type`.
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
multiwfn2vesta cube-arith products --operation spin-density \
  --plus-cube alpha_density.cub \
  --minus-cube beta_density.cub
multiwfn2vesta fukui-run fukui_products \
  --neutral neutral.molden \
  --anion anion.molden \
  --cation cation.molden \
  --operation dual-descriptor
multiwfn2vesta surface-extrema input.vesta surfanalysis.pdb output.vesta \
  --surface-cube density.cub
multiwfn2vesta iri-run input.molden iri_products --timeout 300
multiwfn2vesta igmh-run input.molden igmh_products \
  --fragment 1-48 --fragment 49-60 \
  --grid-mode spacing --grid-spacing 0.25
multiwfn2vesta igm-run input.molden igm_products \
  --fragment 1-48 --fragment 49-60 \
  --grid-mode spacing --grid-spacing 0.25
multiwfn2vesta aigm-run trajectory.xyz aigm_products \
  --fragment 1-48 --fragment 49-60 \
  --frame-range 1 200 \
  --grid-mode spacing --grid-spacing 0.25
multiwfn2vesta grid-run input.molden grid_products --function density
multiwfn2vesta grid-run input.molden grid_products --function spin-polarization
multiwfn2vesta grid-run input.molden grid_products --function vdw-potential \
  --vdw-probe C
multiwfn2vesta grid-run input.molden grid_products \
  --function edr \
  --edr-length 0.85
multiwfn2vesta grid-run input.molden grid_products \
  --function edrdmax \
  --edr-exponents 12 3.0 1.2
multiwfn2vesta grid-run input.molden grid_products \
  --function pair-function \
  --reference-point 0 0 0 \
  --pair-function-type 1 \
  --pair-correlation-type 3
multiwfn2vesta grid-run input.molden grid_products \
  --function source-function \
  --reference-point 0 0 0 \
  --source-function-mode 1
multiwfn2vesta grid-run input.molden grid_products \
  --function local-electron-affinity
multiwfn2vesta grid-run input.molden grid_products \
  --function dori
multiwfn2vesta grid-run input.molden grid_products \
  --function becke \
  --becke-atoms 1 4
multiwfn2vesta grid-run input.molden grid_products \
  --function hirshfeld \
  --hirshfeld-atoms '2,3,7-10'
multiwfn2vesta grid-run input.molden grid_products \
  --function hirshfeld-delta-g
multiwfn2vesta grid-run input.molden esp_map \
  --function esp \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub
multiwfn2vesta stm-run input.molden stm_products --grid-points 80 80 40
multiwfn2vesta domain-run density.cub domain_products --criterion '<0.5'
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
multiwfn2vesta cube-preset gradient-norm gradient.cub cube_products
multiwfn2vesta cube-preset orbital-density orbdens.cub cube_products
multiwfn2vesta cube-preset spin-density spindensity.cub cube_products
multiwfn2vesta cube-preset spin-polarization spindensity.cub cube_products
multiwfn2vesta cube-preset laplacian laplacian.cub cube_products
multiwfn2vesta cube-preset hamiltonian-ked 'K(r).cub' cube_products
multiwfn2vesta cube-preset lagrangian-ked 'G(r).cub' cube_products
multiwfn2vesta cube-preset local-information-entropy infoentro.cub cube_products
multiwfn2vesta cube-preset electron-delocalization-range EDR.cub cube_products
multiwfn2vesta cube-preset orbital-overlap-distance EDRDmax.cub cube_products
multiwfn2vesta cube-preset pair-function fermihole.cub cube_products
multiwfn2vesta cube-preset source-function srcfunc.cub cube_products
multiwfn2vesta cube-preset user-function userfunc.cub cube_products
multiwfn2vesta cube-preset becke-weight Becke.cub cube_products
multiwfn2vesta cube-preset hirshfeld-weight Hirshfeld.cub cube_products
multiwfn2vesta cube-preset rdg-scalar RDG.cub cube_products
multiwfn2vesta cube-preset promolecular-rdg RDGprodens.cub cube_products
multiwfn2vesta cube-preset promolecular-delta-g Delta_g.cub cube_products
multiwfn2vesta cube-preset hirshfeld-delta-g griddata.cub cube_products
multiwfn2vesta cube-preset iri-scalar IRI.cub cube_products
multiwfn2vesta cube-preset dori-scalar userfunc.cub cube_products
multiwfn2vesta cube-preset vdw-potential vdWpot.cub cube_products
multiwfn2vesta cube-preset potential pot_es.cube cube_products
multiwfn2vesta cube-preset partial-charge pchg.cube cube_products
multiwfn2vesta cube-preset wavefunction-norm wfc_norm.cube cube_products
multiwfn2vesta cube-preset elf ELF.cub cube_products
multiwfn2vesta cube-preset rdg IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub
multiwfn2vesta cube-preset dori DORI.cub cube_products \
  --texture-cube sl2r.cub
multiwfn2vesta cube-preset stm STM.cub cube_products
multiwfn2vesta cube-preset domain domain.cub cube_products
multiwfn2vesta cube-preset basin basin0001.cub cube_products
multiwfn2vesta cube-preset basin-type basinsyn.cub cube_products
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
orbital/wavefunction/density-difference cubes, Multiwfn gradient norm,
orbital-density, spin-density, spin-polarization parameter, Laplacian, K(r),
G(r), local information entropy, electron delocalization range,
orbital-overlap distance, standalone pair/correlation function, source
function, Becke atomic/overlap weight, Hirshfeld weight, RDG, promolecular
RDG, and promolecular Delta-g, Hirshfeld-partition Delta-g, standalone IRI
scalar cubes, standalone vdW potential cubes, direct ABACUS potential cubes,
ABACUS partial-charge/state-density cubes, nonnegative ABACUS wavefunction
norm cubes, ELF/LOL cubes, IRI/RDG/NCI mapped surfaces, STM/LDOS
tunneling-current surfaces, binary domain isosurfaces, binary basin
isosurfaces, signed basin-type maps, IGM/IGMH/aIGM weak-interaction mapped
surfaces, ESP/MEP mapped density surfaces, generic molecular surface maps,
ALIE/LEA/LEAE density-surface maps, and vdW-potential density-surface maps.
The recipe
records the requested preset, canonical preset, effective
isosurface, texture scaling source, and explicit texture percentage overrides
when they are used.  The `surface-map`/`molsurfmap` defaults follow the
bundled Multiwfn `molsurfmap.vmd` template.

Use `vdw-potential` for standalone Multiwfn function `25` `vdWpot.cub`
isosurfaces; it uses signed surfaces at `+/-1.0` kcal/mol, matching
Multiwfn's main-function-5 display default.  `grid-run` fixes the Multiwfn
`ivdwprobe` probe atom to carbon/6 by default and accepts `--vdw-probe O`,
`--vdw-probe Cl`, or an atomic number for other UFF probe atoms.  Use
`vdw-map`/`vdw-surface` when a vdW potential cube should color a
density/surface cube.  Use `potential` for direct `out_pot`/potential cube
isosurfaces.  Use `esp` when a density or molecular surface cube should be
colored by a potential texture cube.

Use `electron-delocalization-range`/`edr` for Multiwfn function `20`
`EDR.cub`; `grid-run` requires `--edr-length D_BOHR` because Multiwfn asks
for the EDR length scale before grid setup.  Use
`orbital-overlap-distance`/`edrdmax` for function `21` `EDRDmax.cub`; omit
`--edr-exponents` to use Multiwfn's default exponent set `20, 2.50, 1.50`,
or pass `--edr-exponents COUNT START INCREMENT` for manual control.

Use `pair-function`/`fermihole`/`correlation-hole` for Multiwfn function
`17` `fermihole.cub`.  `grid-run` requires `--reference-point X Y Z`;
coordinates are Bohr by default and can be Angstrom with
`--reference-unit angstrom`.  `--pair-function-type` controls Multiwfn
`pairfunctype` (`1/2` correlation hole alpha/beta, `4/5` correlation
factor, `7/8` exchange-correlation density, `10/11/12` pair density), and
`--pair-correlation-type` controls `paircorrtype` (`1` exchange only, `2`
Coulomb correlation only, `3` both).  The runner copies the selected
Multiwfn `settings.ini` when available, patches only `pairfunctype` and
`paircorrtype`, and passes the run-local settings file with `-set`.

Use `source-function`/`source`/`srcfunc` for Multiwfn function `19`
`srcfunc.cub`.  `grid-run` requires `--reference-point X Y Z`; coordinates
are Bohr by default and can be Angstrom with `--reference-unit angstrom`.
The maintained command stream sets the reference point through Multiwfn main
menu `1000 -> 1`, then enters main function `5`.  `--source-function-mode`
controls Multiwfn `srcfuncmode`; the runner copies the selected Multiwfn
`settings.ini` when available, patches only `srcfuncmode`, and passes that
run-local `multiwfn_grid_settings.ini` with `-set`, so the global Multiwfn
installation settings are not modified.  The VESTA preset shows signed
`+/-0.05` isosurfaces by default.

Use `user-function`/`userfunc` for generic Multiwfn function `100`
`userfunc.cub`; this generic route requires `--user-function-index
IUSERFUNC`.  Source-backed named routes now imply common `iuserfunc` values:
`dori` sets `20`, `local-electron-affinity` sets `27`,
`local-electron-attachment-energy` sets `-27`,
`information-gain-density` sets `49`, `shannon-entropy-density` sets `50`,
and `fisher-information-density` / `second-fisher-information-density` set
`51` / `52`.  The runner copies the selected Multiwfn `settings.ini` when
available, patches only `iuserfunc`, and passes the run-local settings file
with `-set`.  Generic standalone `userfunc.cub` uses signed `+/-0.05`
surfaces by default; `grid-run --function dori` uses the `dori-scalar`
single-surface preset at `0.95`, and LEA/LEAE named routes automatically
select the `lea`/`leae` mapped-surface preset when `--surface-cube
density.cub` is supplied.  For DORI surfaces colored by sign(lambda2)rho,
generate the DORI cube and sign(lambda2)rho cube separately, then run
`cube-preset dori DORI.cub ... --texture-cube sl2r.cub`; the existing
`grid-run --surface-cube` option keeps its older direction of supplied
surface cube plus generated texture cube.

Use `becke-weight`/`becke` for Multiwfn function `111` `Becke.cub`;
`grid-run` requires `--becke-atoms I J` because Multiwfn asks for atom
indices before grid setup.  Use `I J` for Becke overlap weight and `I 0`
for Becke atomic weight.  The maintained preset shows a single positive
dimensionless `0.5` isosurface for the normal `0..1` weight range.

Use `hirshfeld-weight`/`hirshfeld` for Multiwfn function `112`
`Hirshfeld.cub`; `grid-run` requires `--hirshfeld-atoms ATOMS`, using the
same comma/range syntax Multiwfn accepts, for example `2,3,7-10`.  The
maintained command stream currently selects Multiwfn's built-in atomic
density mode (`2`) and intentionally defers the separate atomic `.wfn` file
prompt path.  The preset shows a single positive dimensionless `0.5`
isosurface for the normal `0..1` weight range.

Use `hirshfeld-delta-g`/`delta-g-hirshfeld` for Multiwfn function `23`
Delta-g with Hirshfeld partition.  In the inspected Multiwfn 2026.6.2
source, this route exports the generic `griddata.cub`; `grid-run` keeps that
raw file and copies it to a stable `<stem>_hirshfeld-delta-g.cub` processed
product.  This is a standalone full-system scalar and remains separate from
IGM/IGMH fragment `dg_inter.cub` mapped-surface routes.

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
differences, alpha-minus-beta spin density, Fukui functions, and dual
descriptors.  It does not compute the underlying charged-state, spin-channel,
or excited-state wavefunctions; generate those cubes first with ABACUS,
Multiwfn, or `grid-run`.

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

multiwfn2vesta cube-arith cube_arith_products \
  --operation spin-density \
  --plus-cube alpha_density.cub \
  --minus-cube beta_density.cub \
  --stem spin_density
```

The formulae are:

- `density-difference`: `plus - minus`
- `spin-density`: `alpha/spin-up density - beta/spin-down density`
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
`density` for `fukui-plus/minus`, `spin-density` for `spin-density`, and
`signed` for `density-difference`, `dual-descriptor`, and generic linear
combinations.

## Wavefunction to Fukui/Dual VESTA

When the neutral, anion, and cation wavefunctions are available as
Multiwfn-readable files, `fukui-run` composes the maintained density grid
runner and cube arithmetic layer:

```bash
multiwfn2vesta fukui-run fukui_products \
  --neutral neutral.molden \
  --anion anion.molden \
  --cation cation.molden \
  --operation all \
  --grid-mode points \
  --grid-points 80 80 80
```

The neutral density cube is generated first.  Required charged-state density
cubes are then generated with `grid-run --grid-mode cube --grid-cube
<neutral_density.cub>`, so all resulting density cubes share the neutral cube
grid before `cube-arith` builds the requested maps.

Useful operation subsets:

```bash
multiwfn2vesta fukui-run fplus_products \
  --neutral neutral.fch \
  --anion anion.fch \
  --operation fukui-plus

multiwfn2vesta fukui-run dual_products \
  --neutral neutral.fch \
  --anion anion.fch \
  --cation cation.fch \
  --operation dual-descriptor
```

Default outputs in `fukui_products/`:

- `multiwfn_fukui_recipe.md`: top-level manifest and caveats.
- `neutral_density/`, `anion_density/`, and/or `cation_density/`: ordinary
  `grid-run` child directories with Multiwfn command streams, logs, raw cubes,
  processed density cubes, and optional per-state density VESTA files when
  `--state-vesta` is used.
- `fukui_plus/`, `fukui_minus/`, and/or `dual_descriptor/`: ordinary
  `cube-arith` output directories with the map cube, arithmetic recipe, and
  optional VESTA file.

This workflow is intended for finite systems with comparable geometries.
Charged periodic supercells can be physically delicate, especially for slabs
or metals, so inspect the setup before interpreting the map.  If the density
cubes already exist, use `cube-arith` directly.

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
- `gradient` / `rho-gradient`: function `2`, raw `gradient.cub`, preset
  `gradient-norm`, single positive surface by default.  The default
  isosurface follows Multiwfn's global main-function-5 `sur_value=0.05` and
  should be tuned per system.
- `orbital` / `mo`: function `4`, raw `MOvalue.cub`, preset `signed`, requires
  `--orbital` for one orbital or `--orbitals` for batch export.
- `orbital-density` / `orbdens`: function `44`, raw `orbdens.cub`, preset
  `orbital-density`, requires `--orbital` for one orbital or `--orbitals` for
  batch export.
- `laplacian` / `lap`: function `3`, raw `laplacian.cub`, preset
  `laplacian`, signed by default.
- `spin-density` / `spin`: function `5`, raw `spindensity.cub`, preset
  `spin-density`, signed by default.  The runner writes a run-local
  `multiwfn_grid_settings.ini` with `ipolarpara=0` and passes it with
  `-set`, so stale global Multiwfn settings cannot accidentally switch this
  route to the spin-polarization parameter.
- `spin-polarization` / `spin-pol`: function `5`, raw `spindensity.cub`,
  preset `spin-polarization`, signed by default at `+/-0.5`.  This uses the
  same Multiwfn cube filename as spin density, but writes run-local
  `ipolarpara=1`; Multiwfn then evaluates
  `(rho_alpha-rho_beta)/(rho_alpha+rho_beta)`.
- `hamiltonian-ked` / `k(r)`: function `6`, raw `K(r).cub`, preset
  `hamiltonian-ked`, signed by default.
- `lagrangian-ked` / `g(r)`: function `7`, raw `G(r).cub`, preset
  `lagrangian-ked`, single positive surface by default.
- `local-information-entropy` / `information-entropy`: function `11`, raw
  `infoentro.cub`, preset `local-information-entropy`, signed by default.
  Multiwfn evaluates function `11` as local information entropy
  `-rho/N*ln(rho/N)` and keeps the global main-function-5 default
  `sur_value=0.05`.
- `pair-function` / `fermihole` / `correlation-hole`: function `17`, raw
  `fermihole.cub`, preset `pair-function`, signed by default.  Pass
  `--reference-point X Y Z`; add `--reference-unit angstrom` when those
  coordinates are Angstrom.  `--pair-function-type` controls `pairfunctype`
  and `--pair-correlation-type` controls `paircorrtype` through a run-local
  `-set` settings file copied from the selected Multiwfn `settings.ini` when
  available.
- `source-function` / `source` / `srcfunc`: function `19`, raw
  `srcfunc.cub`, preset `source-function`, signed by default.  Pass
  `--reference-point X Y Z`; add `--reference-unit angstrom` when those
  coordinates are Angstrom.  `--source-function-mode` controls
  `srcfuncmode` through a run-local `-set` settings file copied from the
  selected Multiwfn `settings.ini` when available.
- `user-function` / `userfunc`: generic function `100`, raw `userfunc.cub`,
  preset `user-function`, signed by default.  Pass `--user-function-index
  IUSERFUNC` unless using a named route below.  Named routes
  `dori`, `local-electron-affinity`, `local-electron-attachment-energy`,
  `information-gain-density`, `shannon-entropy-density`,
  `fisher-information-density`, and `second-fisher-information-density`
  automatically patch `iuserfunc=20/27/-27/49/50/51/52` into a run-local
  `-set` settings file, leaving global Multiwfn settings untouched.
- `electron-delocalization-range` / `edr`: function `20`, raw `EDR.cub`,
  preset `electron-delocalization-range`, single positive surface by default.
  Pass `--edr-length D_BOHR`; Multiwfn asks for this EDR length scale before
  grid setup and keeps the global main-function-5 `sur_value=0.05`.
- `orbital-overlap-distance` / `edrdmax`: function `21`, raw
  `EDRDmax.cub`, preset `orbital-overlap-distance`, single positive surface
  by default.  Without `--edr-exponents`, `grid-run` chooses Multiwfn's
  default exponent set `20, 2.50, 1.50`; pass `--edr-exponents COUNT START
  INCREMENT` to use manual exponent parameters.
- `becke-weight` / `becke`: function `111`, raw `Becke.cub`, preset
  `becke-weight`, single positive `0.5` isosurface by default.  Pass
  `--becke-atoms I J`; `I J` computes Becke overlap weight and `I 0`
  computes Becke atomic weight.
- `hirshfeld-weight` / `hirshfeld`: function `112`, raw `Hirshfeld.cub`,
  preset `hirshfeld-weight`, single positive `0.5` isosurface by default.
  Pass `--hirshfeld-atoms ATOMS`, for example `2,3,7-10`.  The maintained
  stream selects built-in atomic densities; separate atomic `.wfn` density
  prompts are not automated yet.
- `esp`, `nuclear-esp`, and `signlambda2rho`: signed scalar fields,
  defaulting to the `signed` preset; with `--surface-cube`,
  `esp`/`nuclear-esp` map through `cube-preset esp` and
  `signlambda2rho` maps through `cube-preset iri`.
- `vdw-potential` / `vdw`: function `25`, raw `vdWpot.cub`, preset
  `vdw-potential`, signed at `+/-1.0` kcal/mol by default.  With
  `--surface-cube`, it maps through `cube-preset vdw-map` instead so the
  generated vdW potential cube colors an existing density/surface cube.
  `grid-run` writes run-local `ivdwprobe=6` by default and accepts
  `--vdw-probe ELEMENT_OR_Z` for other probe atoms.
- `elf` and `lol`: localization cubes, defaulting to `cube-preset elf/lol`.
  The runner copies the selected Multiwfn `settings.ini` when available and
  writes run-local `ELFLOL_type=0` for ordinary Becke ELF/LOL definitions.
  Use `--elflol-type tsirelson` or `--elflol-type tian-lu` for alternate
  ELF/LOL definitions, or `--elflol-type d-over-d0` for the ELF-only D/D0
  term, without changing global settings.
- `alie` / `avglocion`: function `18`, raw `avglocion.cub`.  With
  `--surface-cube density.cub`, the generated ALIE cube is used as the
  texture for `cube-preset alie`.
- `local-electron-affinity` and `local-electron-attachment-energy`: function
  `100`, raw `userfunc.cub`.  With `--surface-cube density.cub`, the
  generated LEA/LEAE cube is used as the texture for `cube-preset lea` or
  `cube-preset leae`.
- `dori`: function `100`, raw `userfunc.cub`, run-local `iuserfunc=20`,
  preset `dori-scalar` with a single `0.95` isosurface.  For the classic
  DORI surface colored by sign(lambda2)rho, use explicit
  `cube-preset dori DORI.cub ... --texture-cube sl2r.cub`; this follows the
  bundled `DORIfill.vmd` direction of DORI as surface and sign(lambda2)rho
  as texture.
- `rdg` / `promolecular-rdg`: functions `13` and `14`, raw `RDG.cub` and
  `RDGprodens.cub`, presets `rdg-scalar` and `promolecular-rdg`.
  IRI/RDG mapped surfaces that need two coupled cubes should still use
  `iri-run` or explicit `cube-preset iri`.
- `delta-g` / `deltag`: function `22`, raw `Delta_g.cub`, preset
  `promolecular-delta-g`, single positive surface by default.  This is the
  standalone promolecular approximation and is separate from IGM/IGMH
  `dg_inter.cub` mapped surfaces.
- `hirshfeld-delta-g` / `delta-g-hirshfeld`: function `23`, raw
  `griddata.cub`, preset `hirshfeld-delta-g`, single positive surface by
  default.  Multiwfn does not give this export a dedicated filename in
  `0123dim.f90`, so `grid-run` renames the processed cube to a stable
  `<stem>_hirshfeld-delta-g.cub`.
- `iri` / `interaction-region-indicator`: function `24`, raw `IRI.cub`,
  preset `iri-scalar`, single positive surface by default.  The default
  isosurface follows Multiwfn's main-function-5 `sur_value=1.0`.
- `signlambda2rho` and `promolecular-signlambda2rho`: single scalar cubes;
  sign(lambda2)rho can become the texture in a mapped `cube-preset iri`
  workflow.

Grid setup defaults to explicit point counts:

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function elf \
  --elflol-type becke \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function lol \
  --elflol-type tsirelson \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function edr \
  --edr-length 0.85 \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function edrdmax \
  --edr-exponents 12 3.0 1.2 \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function pair-function \
  --reference-point 0 0 0 \
  --pair-function-type 1 \
  --pair-correlation-type 3 \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function source-function \
  --reference-point 0 0 0 \
  --source-function-mode 1 \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function local-electron-affinity \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function user-function \
  --user-function-index 49 \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function becke \
  --becke-atoms 1 4 \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function hirshfeld \
  --hirshfeld-atoms '2,3,7-10' \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function hirshfeld-delta-g \
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

multiwfn2vesta grid-run input.fch lea_map \
  --function local-electron-affinity \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub
```

With `--preset auto`, mapped defaults are `esp` for ESP/nuclear ESP, `alie`
for ALIE, `lea`/`leae` for LEA/LEAE, `iri` for sign(lambda2)rho, `vdw-map`
for vdW potential, and `surface-map` for other functions.  Batch orbital export rejects
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
`--expected-cube`, `--raw-dir`, `--surface-cube`, reference-point,
pair/source/user-function, and other non-orbital function-specific options,
because each child run owns its own command stream and raw output directory.

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

## Wavefunction to STM/LDOS VESTA

For wavefunction inputs accepted by Multiwfn and containing GTF/GTO
information, `stm-run` drives Multiwfn main function `300`, subfunction `4`,
switches STM from the default constant-distance mode to constant-current mode,
calculates a 3D tunneling-current/LDOS grid, exports `STM.cub`, and then writes
a VESTA file through `cube-preset stm`:

```bash
multiwfn2vesta stm-run input.molden stm_products \
  --bias -1.0 \
  --fermi -4.8 \
  --grid-points 120 120 60 \
  --x-range -6 6 \
  --y-range -6 6 \
  --z-range 2 8
```

For ABACUS metallic/slab Molden files with smeared or non-integer occupation,
`--prepare-fermi-temperature TEMP_K` inserts the Multiwfn `300 -> 9` Fermi
preparation step before entering the STM menu.  The runner does not create a
2D GUI STM plane plot; the maintained output is the exported 3D `STM.cub`
isosurface.

Default outputs in `stm_products/`:

- `multiwfn_stm_input.txt`: exact command stream sent to Multiwfn.
- `multiwfn_stm.stdout.txt` and `multiwfn_stm.stderr.txt`.
- `multiwfn_stm_raw/STM.cub`.
- `<stem>_stm.cub`.
- `multiwfn_stm_recipe.md`.
- `<stem>_stm_cube.vesta` and `<stem>_stm_cube_vesta_recipe.md`, unless
  `--no-vesta` is used.

Validated H2O noGUI smoke:

```text
/mnt/g/work/multiwfn2vesta/smoke/multiwfn_stm_run_smoke_20260610/h2o/
```

This run used grid `10 x 10 x 6`, produced `h2o_stm.cub`, measured data range
`3.7332e-13` to `0.0151741`, and wrote `h2o_stm_cube.vesta` with default STM
isosurface `0.001`, without launching VESTA.

## Cube/Grid to Domain VESTA

For existing scalar cube data from ABACUS, Multiwfn `grid-run`, or another
compatible source, `domain-run` drives Multiwfn main function `200`,
subfunction `14`, sets a domain criterion, yields domains from the current
grid data in memory, exports `domain.cub` and `domain.pdb`, and then writes a
VESTA isosurface through `cube-preset domain`:

```bash
multiwfn2vesta domain-run density.cub domain_products \
  --criterion '<0.5' \
  --domain-index 1 \
  --timeout 300
```

Default outputs in `domain_products/`:

- `multiwfn_domain_input.txt`: exact command stream sent to Multiwfn.
- `multiwfn_domain.stdout.txt` and `multiwfn_domain.stderr.txt`.
- `multiwfn_domain_raw/domain.cub`.
- `multiwfn_domain_raw/domain.pdb`.
- `<stem>_domain.cub`.
- `<stem>_domain.pdb`.
- `multiwfn_domain_recipe.md`.
- `<stem>_domain_cube.vesta` and `<stem>_domain_cube_vesta_recipe.md`, unless
  `--no-vesta` is used.

`domain.cub` is binary: Multiwfn writes `1` inside the selected domain and
`0` outside, so the maintained VESTA preset uses isosurface `0.5`.  The
companion `domain.pdb` stores boundary grid points for the selected domain.

Validated H2O density-cube noGUI smoke:

```text
/mnt/g/work/multiwfn2vesta/smoke/multiwfn_domain_run_smoke_20260610/h2o_density/
```

This run used criterion `<0.5`, exported domain index `1`, produced
`h2o_density_domain.cub`, `h2o_density_domain.pdb`, and
`h2o_density_domain_cube.vesta`, without launching VESTA.

## Basin Cube VESTA Presets

Multiwfn basin analysis currently remains a semi-manual upstream workflow,
because generating basins depends on the selected real-space function, grid
settings, and whether a cube is already loaded in memory.  The maintained
project layer starts at the stable exported cube products from basin analysis
menu option `-5`.

For individual binary basin cubes such as `basin0001.cub`, where Multiwfn
writes `1` inside the selected basin and `0` outside:

```bash
multiwfn2vesta cube-preset basin basin0001.cub basin_products
```

For `basinsyn.cub`, where Multiwfn writes monosynaptic basin regions as `-1`
and disynaptic regions as `+1`:

```bash
multiwfn2vesta cube-preset basin-type basinsyn.cub basin_products
```

The `basin` preset rejects an input file named `basin.cub`, because Multiwfn's
all-index `basin.cub` grid values are basin indices rather than a binary
membership mask.  Use individual `basinNNNN.cub` files for basin boundary
surfaces.

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

## Trajectory to aIGM/amIGM VESTA

For Multiwfn-readable trajectories, typically XYZ trajectories from MD or
AIMD, `aigm-run` drives the weak-interaction menu `20`, selects aIGM option
`12` or amIGM option `-12`, records fragment definitions and the frame range,
then exports averaged cubes:

```bash
multiwfn2vesta aigm-run trajectory.xyz aigm_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --frame-range 1 200 \
  --periodic \
  --grid-mode spacing \
  --grid-spacing 0.25 \
  --timeout 1200

multiwfn2vesta amigm-run trajectory.xyz amigm_products \
  --fragment 1-48 \
  --fragment c \
  --export-tfi \
  --tfi-vesta
```

Default outputs in `aigm_products/`, with `aigm` replaced by `amigm` for that
method:

- `multiwfn_aigm_input.txt`
- `multiwfn_aigm.stdout.txt`
- `multiwfn_aigm.stderr.txt`
- `multiwfn_aigm_raw/avgdg_inter.cub`
- `multiwfn_aigm_raw/avgsl2r.cub`
- `<stem>_avgdg_inter.cub`
- `<stem>_avgsl2r.cub`
- `<stem>_avgRDG.cub` when `--export-rdg` is used
- `<stem>_thermflu.cub` when `--export-tfi` is used
- `<stem>_multiwfn_aigm_output.txt` when `--export-scatter` is used
- `<stem>_<method>_cube.vesta`
- `<stem>_<method>_cube_vesta_recipe.md`
- optional `<stem>_<method>_tfi_cube.vesta` when `--tfi-vesta` is used

The maintained VESTA view uses `avgdg_inter.cub` as the isosurface and
`avgsl2r.cub` as the texture cube through `cube-preset aigm`.  TFI coloring is
opt-in because Multiwfn only writes `thermflu.cub` when requested.  This is a
trajectory-average workflow, not a single-wavefunction ABACUS Molden workflow;
use `igmh-run`, `igm-run`, or `migm-run` for ordinary wavefunction fragment
analysis.

For periodic trajectories, pass `--periodic --grid-mode spacing
--grid-spacing VALUE` or `--grid-mode pbc-cell`.  The runner also lightly
detects common `Lattice=`, `pbc=`, and `CRYST1` markers and rejects
`--grid-mode points` for periodic input, because Multiwfn's PBC grid option
`4` reads a spacing value rather than `NX,NY,NZ`.

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

Current no-GUI regression passed as a 242-test suite after the `fukui-run`
increment:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

Focused `fukui-run` validation used:

```bash
PYTHONPATH=src python3 -m py_compile src/multiwfn2vesta/multiwfn_fukui.py src/multiwfn2vesta/cli.py tests/test_multiwfn_fukui.py tests/test_cli.py
PYTHONPATH=src python3 -m unittest tests.test_multiwfn_fukui tests.test_cli tests.test_cube_arith tests.test_multiwfn_grid
bin/multiwfn2vesta --help
bin/multiwfn2vesta fukui-run --help
bin/multiwfn2vesta cube-preset --list-presets
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
- `docs/skills/multiwfn_aigm_run_skill.md`: Multiwfn aIGM/amIGM trajectory-average
  runner notes.
- `docs/skills/multiwfn_fukui_run_skill.md`: shared-grid
  Fukui/dual-descriptor runner notes.
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
