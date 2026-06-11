# Skill: multiwfn2vesta unified CLI

## When to use

Use this entry point when operating the project from a shell and the goal is to
avoid remembering `PYTHONPATH=src python -m ...` module paths.

## One-time setup

Add only the project `bin` directory to `PATH`:

```bash
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH
```

This is workspace-local and does not modify system files.  The launcher
automatically prepends `/mnt/g/work/multiwfn2vesta/project/src` to Python's
module path.

## Modes

Interactive chooser:

```bash
multiwfn2vesta
```

Scriptable subcommands:

```bash
multiwfn2vesta discover
multiwfn2vesta abacus-molden --help
multiwfn2vesta cube-preset --help
multiwfn2vesta surface-extrema --help
multiwfn2vesta cube-arith --help
multiwfn2vesta iri-run --help
multiwfn2vesta igmh-run --help
multiwfn2vesta igm-run --help
multiwfn2vesta migm-run --help
multiwfn2vesta aigm-run --help
multiwfn2vesta amigm-run --help
multiwfn2vesta grid-run --help
multiwfn2vesta fukui-run --help
multiwfn2vesta stm-run --help
multiwfn2vesta domain-run --help
multiwfn2vesta multiwfn-atom-color --help
multiwfn2vesta aim-run --help
multiwfn2vesta aim-pdb --help
multiwfn2vesta aim-igmh --help
```

Aliases:

- `multiwfn2vesta where` and `multiwfn2vesta env` are aliases for `discover`.
- `multiwfn2vesta molden ...` and `multiwfn2vesta abacus-multiwfn-molden ...`
  are aliases for `abacus-molden`.
- `multiwfn2vesta cube ...` is an alias for `cube-vesta`.
- `multiwfn2vesta preset ...` and `multiwfn2vesta analysis-cube ...` are
  aliases for `cube-preset`.
- `multiwfn2vesta surf-extrema ...` and
  `multiwfn2vesta surfanalysis-vesta ...` are aliases for `surface-extrema`.
- `multiwfn2vesta cube-math ...`, `multiwfn2vesta density-diff ...`, and
  `multiwfn2vesta fukui-cube ...` are aliases for `cube-arith`.
- `multiwfn2vesta multiwfn-iri ...` and `multiwfn2vesta rdg-run ...` are
  aliases for `iri-run`.
- `multiwfn2vesta multiwfn-igmh ...` and
  `multiwfn2vesta multiwfn-igmh-run ...` are aliases for `igmh-run`.
- `multiwfn2vesta multiwfn-igm ...` and
  `multiwfn2vesta multiwfn-igm-run ...` are aliases for `igm-run`.
- `multiwfn2vesta multiwfn-migm ...` and
  `multiwfn2vesta multiwfn-migm-run ...` are aliases for `migm-run`.
- `multiwfn2vesta multiwfn-aigm ...`,
  `multiwfn2vesta multiwfn-aigm-run ...`, and
  `multiwfn2vesta averaged-igm-run ...` are aliases for `aigm-run`.
- `multiwfn2vesta multiwfn-amigm ...`,
  `multiwfn2vesta multiwfn-amigm-run ...`, and
  `multiwfn2vesta averaged-migm-run ...` are aliases for `amigm-run`.
- `multiwfn2vesta multiwfn-grid ...`,
  `multiwfn2vesta scalar-cube-run ...`, and
  `multiwfn2vesta function-cube ...` are aliases for `grid-run`.
- `multiwfn2vesta multiwfn-fukui ...`,
  `multiwfn2vesta multiwfn-fukui-run ...`, and
  `multiwfn2vesta dual-descriptor-run ...` are aliases for `fukui-run`.
- `multiwfn2vesta multiwfn-stm ...`,
  `multiwfn2vesta multiwfn-stm-run ...`, and
  `multiwfn2vesta ldos-run ...` are aliases for `stm-run`.
- `multiwfn2vesta multiwfn-domain ...`,
  `multiwfn2vesta multiwfn-domain-run ...`, and
  `multiwfn2vesta cube-domain ...` are aliases for `domain-run`.
- `multiwfn2vesta multiwfn-table-color ...` and
  `multiwfn2vesta atom-table-color ...` are aliases for
  `multiwfn-atom-color`.
- `multiwfn2vesta atom-color ...` remains a backward-compatible alias for
  `abacus-mulliken-color`.
- `multiwfn2vesta multiwfn-aim ...` is the same as `aim-run`.
- `multiwfn2vesta aim-vesta ...` is the same as `aim-pdb`.
- `multiwfn2vesta igmh ...` is the same as `aim-igmh`; this top-level alias
  styles an already saved AIM+IGMH overlay.  The IGMH cube display preset is
  invoked as `multiwfn2vesta cube-preset igmh ...`, while automated
  Multiwfn fragment runs are `multiwfn2vesta igmh-run ...`,
  `multiwfn2vesta igm-run ...`, and `multiwfn2vesta migm-run ...`.
  Trajectory-average runs are `multiwfn2vesta aigm-run ...` and
  `multiwfn2vesta amigm-run ...`.

## Maintained workflows

### Discover executables

```bash
multiwfn2vesta discover
```

Use this before a new run.  It prints every Multiwfn/VESTA candidate and a
`selected:` line for the path that will be used by default.  Discovery prefers
explicit paths, environment variables, workspace-local tools, then `PATH`.

Multiwfn environment variables accepted:

- `MULTIWFN_PATH`
- `MULTIWFNPATH`
- `Multiwfnpath`
- `MultiwfnPATH`
- `MultiwfnPath`
- `MULTIWFN_EXECUTABLE`

VESTA environment variables accepted:

- `VESTA_PATH`
- `VESTA_DIR`
- `VESTAPATH`
- `VestaPATH`
- `Vestapath`
- `VESTA_EXECUTABLE`

### ABACUS calculation to Molden

```bash
multiwfn2vesta abacus-molden \
  abacus_calc \
  ABACUS_Multiwfn.molden
```

The command exports the ABACUS converter from
`interfaces/Multiwfn_interface/molden.py`, writes logs/recipe metadata, keeps
`[Nval]` enabled by default, and runs `molden-check --abacus` on the output.
The selected Python must be able to import `numpy`, `scipy`, and
`matplotlib`; use `--python /path/to/python` if the default `python3`
environment is not suitable.

### Cube analysis preset to VESTA

```bash
multiwfn2vesta cube-preset --list-presets
multiwfn2vesta cube-preset orbital orbital.cub cube_products
multiwfn2vesta cube-preset orbital-density orbdens.cub cube_products
multiwfn2vesta cube-preset gradient-norm gradient.cub cube_products
multiwfn2vesta cube-preset spin-density spindensity.cub cube_products
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
multiwfn2vesta cube-preset vdw-potential vdWpot.cub cube_products
multiwfn2vesta cube-preset potential pot_es.cube cube_products
multiwfn2vesta cube-preset partial-charge pchg.cube cube_products
multiwfn2vesta cube-preset wavefunction-norm wfc_norm.cube cube_products
multiwfn2vesta cube-preset rdg IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub
multiwfn2vesta cube-preset domain domain.cub cube_products
multiwfn2vesta cube-preset basin basin0001.cub cube_products
multiwfn2vesta cube-preset basin-type basinsyn.cub cube_products
multiwfn2vesta cube-preset igmh dg_inter.cub cube_products \
  --texture-cube sl2r.cub
multiwfn2vesta cube-preset alie density.cub cube_products \
  --texture-cube avglocion.cub \
  --surfanalysis-pdb surfanalysis.pdb
multiwfn2vesta cube-preset vdw-surface density.cub cube_products \
  --texture-cube vdW.cub
```

Use this when the file is a common ABACUS/Multiwfn cube product and the
default style is enough to start.  Presets cover density-like scalar cubes,
signed orbital/wavefunction/density-difference cubes, Multiwfn
orbital-density, spin-density, Laplacian, K(r), G(r), pair/correlation
function, Becke and Hirshfeld weight cubes, standalone RDG, and promolecular
RDG cubes, standalone IRI and vdW potential cubes, direct
ABACUS potential cubes, ABACUS partial-charge/state-density cubes,
nonnegative ABACUS wavefunction-norm cubes, ELF/LOL, IRI/RDG/NCI mapped
surfaces, binary domain isosurfaces, binary basin isosurfaces, signed
basin-type maps,
IGM/IGMH/aIGM weak-interaction mapped surfaces, ESP/MEP mapped density
surfaces, generic molecular surface maps, ALIE/LEA/LEAE density-surface maps,
and vdW-potential density-surface maps.
All VESTA writing still goes through the maintained `cube-vesta`
backend.
`igmh`/`igm-intra`/`aigm` defaults follow bundled Multiwfn IGM VMD templates,
while `surface-map`/`molsurfmap` defaults follow the bundled Multiwfn
`molsurfmap.vmd` template.

Patch an existing VESTA file with Multiwfn surface extrema:

```bash
multiwfn2vesta surface-extrema input.vesta surfanalysis.pdb output.vesta \
  --surface-cube density.cub \
  --selection all
```

### Cube arithmetic to density-difference/spin-density/Fukui VESTA

```bash
multiwfn2vesta cube-arith cube_arith_products \
  --operation spin-density \
  --plus-cube alpha_density.cub \
  --minus-cube beta_density.cub \
  --stem spin_density

multiwfn2vesta cube-arith cube_arith_products \
  --operation dual-descriptor \
  --anion-cube density_Nplus1.cub \
  --neutral-cube density_N.cub \
  --cation-cube density_Nminus1.cub
```

Use this after ABACUS, Multiwfn, or `grid-run` has produced compatible cube
files.  It writes a new cube and, by default, calls `cube-preset`; `--preset
auto` uses `density` for `fukui-plus/minus`, `spin-density` for
`spin-density`, and `signed` for `density-difference`, `dual-descriptor`,
and generic linear combinations.
Generic linear combinations use repeated `--term COEFF CUBE` entries.

The named formulae are `alpha/spin-up density - beta/spin-down density` for
`spin-density`, `rho(N+1)-rho(N)` for `fukui-plus`,
`rho(N)-rho(N-1)` for `fukui-minus`, and
`rho(N+1)-2*rho(N)+rho(N-1)` for `dual-descriptor`.

### Wavefunction to shared-grid Fukui/dual VESTA

```bash
multiwfn2vesta fukui-run fukui_products \
  --neutral neutral.molden \
  --anion anion.molden \
  --cation cation.molden \
  --operation all \
  --grid-mode points \
  --grid-points 80 80 80
```

Use this when neutral, N+1, and/or N-1 wavefunction files are available and
the desired product is a Fukui or dual-descriptor cube.  The command is a
composition layer:

- neutral density is generated first through `grid-run --function density`;
- charged-state density cubes are generated through `grid-run --grid-mode
  cube --grid-cube <neutral_density.cub>` so they share the neutral grid;
- requested maps are produced by `cube-arith`.

Operation subsets:

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

Default outputs are `multiwfn_fukui_recipe.md`, one `grid-run` child
directory per required state, and one `cube-arith` child directory per
requested operation.  Use `--state-vesta` to also write density VESTA files
for the individual states.  Use `--no-vesta` for map cube-only output.

This route is intended for finite systems with comparable geometries.  Charged
periodic cells and metal slabs need separate physical checks before the maps
are interpreted.

### Wavefunction to Multiwfn IRI/RDG to VESTA

```bash
multiwfn2vesta iri-run \
  input.molden \
  iri_products \
  --timeout 300
```

Inputs can be any wavefunction file Multiwfn accepts, such as `.molden`,
`.fch`, `.fchk`, `.wfn`, or `.wfx`.  The command writes the exact Multiwfn
input stream and stdout/stderr logs, preserves raw `func1.cub`/`func2.cub`
under `multiwfn_iri_raw/`, processes them into `<stem>_IRI1.cub` and
`<stem>_IRI2.cub`, then calls `cube-preset iri` to create a mapped-surface
`.vesta` unless `--no-vesta` is supplied.

Explicit executable override:

```bash
multiwfn2vesta iri-run input.fch iri_products \
  --multiwfn /path/to/Multiwfn_noGUI \
  --nthreads 6 \
  --surface-band 0.25
```

Use `--commands-file commands.txt` to replace the default weak-interaction
menu stream.  The runner sets `Multiwfnpath`, `MULTIWFNPATH`, and
`MultiwfnPATH` to the selected executable directory for the subprocess.

### Wavefunction to Multiwfn IGM/IGMH to VESTA

```bash
multiwfn2vesta igmh-run \
  input.molden \
  igmh_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --grid-mode spacing \
  --grid-spacing 0.25 \
  --timeout 600

multiwfn2vesta migm-run \
  input.molden \
  migm_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --sl2r-source actual \
  --grid-mode spacing \
  --grid-spacing 0.25
```

Inputs can be any wavefunction file Multiwfn accepts.  The command writes the
exact Multiwfn input stream and stdout/stderr logs, preserves raw
`dg_inter.cub` and `sl2r.cub` under `multiwfn_<method>_raw/`, copies them to
`<stem>_dg_inter.cub` and `<stem>_sl2r.cub`, preserves optional
`dg_intra.cub`/`dg.cub`, then calls `cube-preset igmh` for IGMH or
`cube-preset igm` for IGM/mIGM unless `--no-vesta` is supplied.

Fragments are passed directly to Multiwfn, so use the same atom-index syntax
you would type interactively.  At least two `--fragment` entries are required
for the default stream; `--commands-file commands.txt` can replace the entire
stream for special cases.

IGM/mIGM have an extra sign(lambda2)rho prompt when wavefunction information
is present.  Use `--sl2r-source actual` or `--sl2r-source promolecular`.
IGMH is fixed to actual density by Multiwfn.  `igm-run` and `migm-run` fix
their method from the command name and reject an extra `--method`; use
`igmh-run --method igm|migm|igmh` for an explicitly selected generic route.

For periodic ABACUS Molden files with `[Cell]`, do not use `--grid-mode
points`.  Multiwfn's PBC grid option `4` reads a spacing value in that case,
so the runner rejects `points` before launch.  Use `--grid-mode spacing
--grid-spacing VALUE` or `--grid-mode pbc-cell`.

### Trajectory to Multiwfn aIGM/amIGM to VESTA

```bash
multiwfn2vesta aigm-run \
  trajectory.xyz \
  aigm_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --frame-range 1 200 \
  --periodic \
  --grid-mode spacing \
  --grid-spacing 0.25 \
  --timeout 1200

multiwfn2vesta amigm-run \
  trajectory.xyz \
  amigm_products \
  --fragment 1-48 \
  --fragment c \
  --export-tfi \
  --tfi-vesta
```

This route is for Multiwfn trajectory-average weak-interaction analysis, not
ordinary single-wavefunction IGMH.  It writes `avgdg_inter.cub` and
`avgsl2r.cub`, then calls `cube-preset aigm` unless `--no-vesta` is supplied.
Use `--export-rdg`, `--export-tfi`, and `--export-scatter` for optional
`avgRDG.cub`, `thermflu.cub`, and scatter `output.txt`.

For periodic trajectory inputs, use `--periodic` with `spacing` or
`pbc-cell`.  The runner rejects `points` for detected periodic trajectories
because Multiwfn's PBC grid option `4` reads a spacing value, not `NX,NY,NZ`.

### Wavefunction to Multiwfn scalar grid cube

```bash
multiwfn2vesta grid-run \
  input.molden \
  grid_products \
  --function density \
  --grid-points 40 40 40 \
  --timeout 300
```

Use this for Multiwfn main function `5` real-space scalar cubes.  The command
records the exact command stream, stdout/stderr, raw Multiwfn cube, processed
`<stem>_<function>.cub`, and a markdown recipe.  By default it calls
`cube-preset` with the function's maintained display preset.  Pass
`--no-vesta` for cube-only generation.

Function discovery:

```bash
multiwfn2vesta grid-run --list-functions
```

Common functions include `density`, `gradient`, `orbital --orbital h`,
`orbital-density`, `spin-density`, `laplacian`, `hamiltonian-ked`,
`lagrangian-ked`, `local-information-entropy`, `elf`, `lol`, `esp`, `alie`,
`pair-function`, `source-function`, `user-function`,
`local-electron-affinity`, `local-electron-attachment-energy`,
`information-gain-density`, `shannon-entropy-density`,
`fisher-information-density`, `second-fisher-information-density`, `edr`, `edrdmax`,
`becke`, `hirshfeld`, `rdg`, `promolecular-rdg`, `delta-g`,
`hirshfeld-delta-g`, `iri`, `signlambda2rho`,
`promolecular-signlambda2rho`, and `vdw-potential`.
The scalar display defaults are
function-specific where possible: `gradient.cub` uses `gradient-norm`,
`spindensity.cub` uses `cube-preset spin-density`, `orbdens.cub` uses
`orbital-density`, `laplacian.cub` uses `laplacian`, `K(r).cub` uses
`hamiltonian-ked`, `G(r).cub` uses `lagrangian-ked`, `infoentro.cub` uses
`local-information-entropy`, `EDR.cub` uses `electron-delocalization-range`,
`EDRDmax.cub` uses `orbital-overlap-distance`, `fermihole.cub` uses
`pair-function`, `srcfunc.cub` uses `source-function`, `userfunc.cub` uses
`user-function`, `Becke.cub` uses `becke-weight`, `Hirshfeld.cub` uses
`hirshfeld-weight`, `RDG.cub` uses `rdg-scalar`, `RDGprodens.cub` uses
`promolecular-rdg`, `Delta_g.cub` uses
`promolecular-delta-g`, Multiwfn function `23` generic `griddata.cub` uses
`hirshfeld-delta-g`, `IRI.cub` uses `iri-scalar`, and `vdWpot.cub` uses
`vdw-potential` with `+/-1.0`
kcal/mol signed surfaces.  `grid-run --function pair-function` requires
`--reference-point X Y Z`; `--pair-function-type` and
`--pair-correlation-type` patch Multiwfn `pairfunctype`/`paircorrtype`
through a run-local settings file copied from the selected Multiwfn
`settings.ini` when available and passed with `-set`.
`grid-run --function source-function` requires `--reference-point X Y Z`;
`--source-function-mode` is patched into a run-local settings file copied
from the selected Multiwfn `settings.ini` when available and passed with
`-set`.
Generic `grid-run --function user-function` requires `--user-function-index
IUSERFUNC`; named routes automatically patch common source-backed values:
`local-electron-affinity` / `lea` = `27`,
`local-electron-attachment-energy` / `leae` = `-27`,
`information-gain-density` = `49`, `shannon-entropy-density` = `50`, and
`fisher-information-density` / `second-fisher-information-density` =
`51` / `52`.  The runner writes `iuserfunc` into a run-local settings file
copied from the selected Multiwfn `settings.ini` when available and passed
with `-set`.  LEA/LEAE named routes also auto-select mapped presets
`lea`/`leae` when `--surface-cube` is supplied.
`grid-run --function becke` requires
`--becke-atoms I J`; `I J` requests Becke overlap weight and `I 0` requests
Becke atomic weight.  `grid-run --function hirshfeld` requires
`--hirshfeld-atoms ATOMS`, for example `2,3,7-10`, and currently selects
Multiwfn's built-in atomic-density mode.  The existing `cube-preset iri`
name remains the two-cube surface+texture route, `vdw-map` remains the
density/surface plus vdW-potential texture route, and IGM/IGMH
`dg_inter.cub` still uses the `igmh`/`igm` texture route.

Batch frontier orbital export:

```bash
multiwfn2vesta grid-run input.fch orbital_products \
  --orbitals h l l+1 \
  --grid-points 80 80 80 \
  --no-vesta
```

With `--orbitals` and no explicit `--function`, the CLI defaults to
`orbital`.  Use `--function orbital-density --orbitals h l` for orbital
density cubes.  Batch mode is repeated isolated single-orbital execution: each
orbital gets a child directory with its own command stream, logs, raw cube
directory, processed cube, optional VESTA output, and one top-level
`multiwfn_grid_batch_recipe.md`.  Add `--keep-going` to continue after a
failed orbital; otherwise later orbitals are marked `skipped`.

Reference-cube grids are useful for aligned overlays:

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function esp \
  --grid-mode cube \
  --grid-cube density.cub \
  --no-vesta
```

When the reference cube is also the surface to display, use `--surface-cube`
and let the generated grid cube become the texture:

```bash
multiwfn2vesta grid-run input.fch esp_map \
  --function esp \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub
```

With `--preset auto`, ESP/nuclear ESP use `cube-preset esp`, ALIE uses
`cube-preset alie`, LEA/LEAE use `cube-preset lea`/`cube-preset leae`,
sign(lambda2)rho uses `cube-preset iri`, vdW potential uses
`cube-preset vdw-map`, and other functions fall back to `surface-map`.  Batch
orbital export rejects `--surface-cube`.

### Wavefunction to Multiwfn STM/LDOS to VESTA

```bash
multiwfn2vesta stm-run \
  input.molden \
  stm_products \
  --bias -1.0 \
  --fermi -4.8 \
  --grid-points 120 120 60 \
  --x-range -6 6 \
  --y-range -6 6 \
  --z-range 2 8
```

Use this for Multiwfn main function `300`, subfunction `4`, constant-current
STM/LDOS cubes.  The runner toggles STM from default constant-distance mode
to constant-current mode, exports `STM.cub`, copies it to `<stem>_stm.cub`,
and calls `cube-preset stm` unless `--no-vesta` is supplied.

For metallic/slab ABACUS Molden files with smearing or non-integer
occupations, try `--prepare-fermi-temperature TEMP_K` to insert the Multiwfn
`300 -> 9` occupation/Fermi preparation step before STM.

The wavefunction must contain GTO/GTF information.  The maintained output is a
3D `STM.cub` isosurface, not Multiwfn's GUI 2D STM plane plot.

### Cube/Grid to Multiwfn Domain to VESTA

```bash
multiwfn2vesta domain-run density.cub domain_products \
  --criterion '<0.5' \
  --domain-index 1 \
  --timeout 300
```

Use this for Multiwfn main function `200`, subfunction `14`, when an existing
cube/grid file should be clustered into connected domains.  The runner
exports raw `domain.cub`/`domain.pdb`, copies them to
`<stem>_domain.cub`/`<stem>_domain.pdb`, and calls `cube-preset domain`
unless `--no-vesta` is supplied.

### Wavefunction to Multiwfn AIM to VESTA

```bash
multiwfn2vesta aim-run \
  input.molden \
  aim_out \
  --timeout 180
```

Inputs can be any wavefunction file Multiwfn accepts, such as `.molden`,
`.fch`, `.fchk`, `.wfn`, or `.wfx`.  The command writes the exact Multiwfn
input stream and stdout/stderr logs into `aim_out/`, then converts
`paths.pdb` and `CPs.pdb` into `aim_atoms_only.vesta`.

Explicit executable override:

```bash
multiwfn2vesta aim-run input.fch aim_out \
  --multiwfn /path/to/Multiwfn_noGUI
```

The runner sets `Multiwfnpath`, `MULTIWFNPATH`, and `MultiwfnPATH` to the
selected executable directory for the subprocess.  If Multiwfn returns `0` but
does not write `paths.pdb`, the CLI returns `3` unless
`--allow-missing-paths` is explicitly supplied.

### AIM PDB to atoms-only VESTA

```bash
multiwfn2vesta aim-pdb \
  paths.pdb \
  aim_atoms_only.vesta \
  --cps-pdb CPs.pdb
```

### AIM+IGMH overlay style and optional render

```bash
multiwfn2vesta aim-igmh \
  input_overlay.vesta \
  output_dir \
  --label-bcp-sites
```

Rendering must be explicit because Windows VESTA automation can still steal
focus:

```bash
multiwfn2vesta aim-igmh \
  input_overlay.vesta \
  output_dir \
  --render-three-views \
  --initial-view top \
  --extra-rotate top x -8 \
  --scale 2
```

## Validation

No-GUI checks:

```bash
bin/multiwfn2vesta --help
bin/multiwfn2vesta discover
bin/multiwfn2vesta cube-preset --list-presets
bin/multiwfn2vesta iri-run --help
bin/multiwfn2vesta grid-run --help
bin/multiwfn2vesta fukui-run --help
bin/multiwfn2vesta stm-run --help
bin/multiwfn2vesta domain-run --help
bin/multiwfn2vesta aim-run --help
bin/multiwfn2vesta aim-igmh --help
printf 'q\n' | bin/multiwfn2vesta
PYTHONPATH=src python3 -m unittest tests.test_cli tests.test_cube_preset tests.test_executables tests.test_multiwfn_aim tests.test_multiwfn_iri tests.test_multiwfn_grid tests.test_multiwfn_fukui tests.test_multiwfn_stm tests.test_multiwfn_domain
```

Real H2O Multiwfn noGUI smoke:

```bash
bin/multiwfn2vesta aim-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_aim_cli_smoke_20260610/h2o \
  --timeout 180
```

Observed output: `paths.pdb`, `CPs.pdb`, `CPprop.txt`, `mol.pdb`,
`multiwfn_aim_input.txt`, `multiwfn.stdout.txt`, `multiwfn.stderr.txt`, and
`aim_atoms_only.vesta`.

Real H2O Multiwfn noGUI IRI/RDG smoke:

```bash
bin/multiwfn2vesta iri-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_iri_run_smoke_20260610/h2o_run1/products \
  --timeout 240 \
  --stem h2o \
  --surface-band 0.25
```

Observed output: raw `func1.cub`/`func2.cub`, processed `h2o_IRI1.cub` and
`h2o_IRI2.cub`, `h2o_iri_cube.vesta`, and
`h2o_iri_cube_vesta_recipe.md`.  VESTA was not launched.

Real H2O Multiwfn noGUI grid-run density smoke:

```bash
bin/multiwfn2vesta grid-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_density/products \
  --function density \
  --grid-points 12 12 12 \
  --stem h2o \
  --timeout 180
```

Observed output: raw `density.cub`, processed `h2o_density.cub`,
`h2o_density_density_cube.vesta`, and both recipes.  VESTA was not launched.

Real H2O Multiwfn noGUI STM/LDOS smoke:

```bash
bin/multiwfn2vesta stm-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_stm_run_smoke_20260610/h2o \
  --grid-points 10 10 6 \
  --stem h2o \
  --timeout 300
```

Observed output: raw `STM.cub`, processed `h2o_stm.cub`,
`h2o_stm_cube.vesta`, and both recipes.  The cube has 600 grid points with
range `3.7332e-13` to `0.0151741`; VESTA was not launched.

Dry smoke for the current Ag(111)+benzene overlay:

```bash
bin/multiwfn2vesta aim-igmh \
  /mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/products/ag111_benzene_igmh_aim_paths_single_xe_yellow_bcp_periodic_overlay.vesta \
  /mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/unified_cli_smoke_20260610 \
  --stem ag111_benzene_igmh_aim_unified_cli \
  --label-bcp-sites
```

This smoke writes a styled `.vesta`, a recipe markdown file, and copied
`dg_inter.cub`/`sl2r.cub`; it does not launch VESTA unless
`--render-three-views` is added.
