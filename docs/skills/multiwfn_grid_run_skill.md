# Skill: Multiwfn real-space grid runner

Use this when a Multiwfn-readable wavefunction file should become one
real-space function cube, or several isolated orbital/orbital-density cubes,
optionally followed by VESTA `.vesta` files.

## Command

```bash
multiwfn2vesta grid-run input.molden grid_products \
  --function density \
  --grid-points 40 40 40 \
  --timeout 300
```

The workflow drives Multiwfn main menu `5` (`study3dim`), selects a
real-space function, sets a grid, and uses post-processing option `2` to
export a Gaussian cube file.

List maintained names and aliases:

```bash
multiwfn2vesta grid-run --list-functions
```

## Function Table

- `density`, aliases `rho`, `electron-density`, `charge-density`: function
  `1`, raw `density.cub`, preset `density`.
- `gradient`, aliases `rho-gradient`, `grad-rho`: function `2`, raw
  `gradient.cub`, preset `gradient-norm` with a single positive isosurface.
  The default isosurface `0.05` follows Multiwfn's global main-function-5
  `sur_value`; tune it per system.
- `laplacian`, aliases `lap`, `laplacian-rho`: function `3`, raw
  `laplacian.cub`, preset `laplacian` with signed positive/negative
  isosurfaces.
- `orbital`, aliases `mo`, `wavefunction`, `mo-value`: function `4`, raw
  `MOvalue.cub`, preset `signed`, requires `--orbital` for one orbital or
  `--orbitals` for batch export.
- `spin-density`: function `5`, raw `spindensity.cub`, preset
  `spin-density` with signed positive/negative isosurfaces.  The runner
  writes a run-local `multiwfn_grid_settings.ini` with `ipolarpara=0`, copied
  from the selected Multiwfn `settings.ini` when available and passed with
  `-set`, so global Multiwfn settings are not modified or accidentally reused.
- `spin-polarization`, aliases `spin-polarization-parameter`, `spin-pol`,
  `spin-polarisation`: function `5`, raw `spindensity.cub`, preset
  `spin-polarization` with signed positive/negative isosurfaces.  This uses
  the same Multiwfn output filename as spin density, but writes run-local
  `ipolarpara=1`; Multiwfn evaluates
  `(rho_alpha-rho_beta)/(rho_alpha+rho_beta)`.
- `hamiltonian-ked`, aliases `k-r`, `k(r)`, `kinetic-k`,
  `hamiltonian-kinetic-density`: function `6`, raw `K(r).cub`, preset
  `hamiltonian-ked` with signed positive/negative isosurfaces.
- `lagrangian-ked`, aliases `g-r`, `g(r)`, `kinetic-g`,
  `lagrangian-kinetic-density`: function `7`, raw `G(r).cub`, preset
  `lagrangian-ked` with a single positive isosurface.
- `nuclear-esp`: function `8`, raw `nucleiesp.cub`, preset `signed`;
  mapped preset `esp` when `--surface-cube` is supplied.
- `elf`: function `9`, raw `ELF.cub`, preset `elf`.
- `lol`: function `10`, raw `LOL.cub`, preset `lol`.
- `local-information-entropy`, aliases `information-entropy`, `infoentro`,
  `local-info-entropy`, `local-shannon-entropy`: function `11`, raw
  `infoentro.cub`, preset `local-information-entropy` with signed
  positive/negative isosurfaces.  Multiwfn evaluates this as
  `-rho/N*ln(rho/N)` and keeps the global main-function-5 `sur_value=0.05`.
- `esp`, aliases `mep`, `total-esp`, `electrostatic-potential`: function
  `12`, raw `totesp.cub`, preset `signed`; mapped preset `esp` with
  `--surface-cube`.
- `rdg`: function `13`, raw `RDG.cub`, preset `rdg-scalar`.
- `promolecular-rdg`: function `14`, raw `RDGprodens.cub`, preset
  `promolecular-rdg`.
- `signlambda2rho`: function `15`, raw `signlambda2rho.cub`, preset
  `signed`; mapped preset `iri` with `--surface-cube`.
- `promolecular-signlambda2rho`: function `16`, raw
  `signlambda2rhoprodens.cub`, preset `signed`; mapped preset `iri` with
  `--surface-cube`.
- `pair-function`, aliases `fermihole`, `fermi-hole`, `correlation-hole`,
  `corr-hole`, `correlation-factor`, `corr-factor`,
  `exchange-correlation-density`, `xc-density`, `pair-density`: function
  `17`, raw `fermihole.cub`, preset `pair-function` with signed
  positive/negative isosurfaces.  Pass `--reference-point X Y Z`;
  coordinates are Bohr by default, or Angstrom with `--reference-unit
  angstrom`.  `--pair-function-type` controls Multiwfn `pairfunctype` and
  `--pair-correlation-type` controls `paircorrtype` through a run-local
  `multiwfn_grid_settings.ini`, copied from the selected Multiwfn
  `settings.ini` when available and passed with `-set`, so global Multiwfn
  settings are not modified.
- `alie`, aliases `average-local-ionization-energy`, `avglocion`: function
  `18`, raw `avglocion.cub`, preset `density`; mapped preset `alie` with
  `--surface-cube`.
- `source-function`, aliases `source`, `srcfunc`, `source-func`: function
  `19`, raw `srcfunc.cub`, preset `source-function` with signed
  positive/negative isosurfaces.  Pass `--reference-point X Y Z`; coordinates
  are Bohr by default, or Angstrom with `--reference-unit angstrom`.
  `--source-function-mode` controls Multiwfn `srcfuncmode` through a
  run-local `multiwfn_grid_settings.ini`, copied from the selected Multiwfn
  `settings.ini` when available and passed with `-set`, so global Multiwfn
  settings are not modified.
- `user-function`, aliases `userfunc`, `user-defined-function`,
  `custom-function`: generic function `100`, raw `userfunc.cub`, preset
  `user-function` with signed positive/negative isosurfaces.  Pass
  `--user-function-index IUSERFUNC` unless using a named route.
- Named `iuserfunc` routes use the same function `100` command stream and
  `userfunc.cub` output, but automatically patch the source-backed
  `iuserfunc` value into a run-local `multiwfn_grid_settings.ini` copied
  from the selected Multiwfn `settings.ini` when available:
  `local-electron-affinity` / `lea` = `27`,
  `local-electron-attachment-energy` / `leae` = `-27`,
  `information-gain-density` / `relative-shannon-entropy` = `49`,
  `shannon-entropy-density` = `50`, `fisher-information-density` = `51`,
  and `second-fisher-information-density` = `52`.  LEA/LEAE named routes
  also auto-select mapped presets `lea`/`leae` when `--surface-cube` is
  supplied.  Special external-grid modes `-1`, `-3`, and Shubin `57/58/59`
  are intentionally rejected by this generic route.
- `electron-delocalization-range`, aliases `edr`, `edr-r-d`,
  `electron-delocalization-range-function`: function `20`, raw `EDR.cub`,
  preset `electron-delocalization-range` with a single positive isosurface.
  `grid-run` requires `--edr-length D_BOHR` because Multiwfn asks for the
  EDR length scale before grid setup.
- `orbital-overlap-distance`, aliases `orbital-overlap-length`, `edrdmax`,
  `edr-dmax`, `d-r`, `d(r)`: function `21`, raw `EDRDmax.cub`, preset
  `orbital-overlap-distance` with a single positive isosurface.  Omit
  `--edr-exponents` to use Multiwfn's default exponent set `20, 2.50, 1.50`,
  or pass `--edr-exponents COUNT START INCREMENT` for manual control.
- `becke-weight`, aliases `becke`, `becke-overlap-weight`,
  `becke-atomic-weight`, `beckewei`: function `111`, raw `Becke.cub`, preset
  `becke-weight` with a single positive `0.5` isosurface.  Pass
  `--becke-atoms I J`; `I J` requests Becke overlap weight and `I 0`
  requests Becke atomic weight.
- `hirshfeld-weight`, aliases `hirshfeld`, `hirshfeld-atomic-weight`,
  `hirshfeldwei`: function `112`, raw `Hirshfeld.cub`, preset
  `hirshfeld-weight` with a single positive `0.5` isosurface.  Pass
  `--hirshfeld-atoms ATOMS`, for example `2,3,7-10`; the maintained stream
  uses built-in atomic densities and does not automate separate atomic
  `.wfn` prompts yet.
- `delta-g`, aliases `deltag`, `delta_g`, `promolecular-deltag`,
  `delta-g-promol`: function `22`, raw `Delta_g.cub`, preset
  `promolecular-delta-g` with a single positive isosurface.  This is
  Multiwfn's promolecular approximation and is distinct from IGM/IGMH
  fragment `dg_inter.cub` mapped-surface routes.
- `hirshfeld-delta-g`, aliases `delta-g-hirshfeld`,
  `deltag-hirshfeld`, `delta_g_hirshfeld`, `igmh-scalar`: function `23`,
  raw `griddata.cub`, preset `hirshfeld-delta-g` with a single positive
  isosurface.  Multiwfn 2026.6.2 does not assign a dedicated cube filename
  for this export, so `grid-run` keeps the raw `griddata.cub` and writes a
  stable processed `<stem>_hirshfeld-delta-g.cub`.
- `iri`, alias `interaction-region-indicator`: function `24`, raw
  `IRI.cub`, preset `iri-scalar` with a single positive isosurface.  Use the
  separate two-cube `cube-preset iri` route when coloring IRI/RDG/NCI surfaces
  by sign(lambda2)rho.
- `vdw-potential`, aliases `vdw`, `vdwpot`,
  `van-der-waals-potential`: function `25`, raw `vdWpot.cub`, preset
  `vdw-potential` with signed `+/-1.0` kcal/mol isosurfaces.  Multiwfn
  evaluates the UFF vdW potential and sets main-function-5 `sur_value=1.0`.
  Mapped preset `vdw-map` is used with `--surface-cube`.
- `orbital-density`: function `44`, raw `orbdens.cub`, preset
  `orbital-density`, requires `--orbital` for one orbital or `--orbitals` for
  batch export.

Use `--function-index N --expected-cube name.cub` for an unlisted function or
custom command stream.

## Batch Orbital Export

```bash
multiwfn2vesta grid-run input.fch orbital_products \
  --orbitals h l l+1 \
  --grid-mode points \
  --grid-points 80 80 80 \
  --no-vesta
```

When `--orbitals` is present and `--function` is omitted, the function defaults
to `orbital`.  Use `--function orbital-density --orbitals h l` for orbital
density cubes.

Batch mode is repeated isolated single-orbital execution, not a single
Multiwfn batch menu.  Each orbital gets a child directory such as
`001_orbital_h/`, `002_orbital_l/`, or `003_orbital_lplus1/`, with its own
command stream, stdout/stderr logs, raw cube directory, processed cube, and
optional VESTA output.  The top-level `multiwfn_grid_batch_recipe.md` records
requested orbitals, safe labels, status, failed/skipped counts, and child
paths.

Default behavior stops after the first failed orbital.  Add `--keep-going` to
continue later orbitals.  Batch mode rejects `--orbital`, `--commands-file`,
`--expected-cube`, `--raw-dir`, reference-point/source-function/pair-function/
user-function options, and other function-specific non-orbital options because those
options would make the child run ownership ambiguous.

## Grid Modes

Default explicit point counts:

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function elf \
  --grid-mode points \
  --grid-points 80 80 80
```

Coarse built-ins:

```bash
multiwfn2vesta grid-run input.fch grid_products --function density --grid-mode low
multiwfn2vesta grid-run input.fch grid_products --function density --grid-mode medium
multiwfn2vesta grid-run input.fch grid_products --function density --grid-mode high
```

Spacing mode, in Multiwfn's non-PBC grid menu:

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function density \
  --grid-mode spacing \
  --grid-spacing 0.30
```

Reference-cube mode for aligned overlays:

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function esp \
  --grid-mode cube \
  --grid-cube density.cub \
  --no-vesta
```

Mapped-surface mode reuses the same surface cube for display and grid
alignment.  The generated grid cube becomes the texture cube:

```bash
multiwfn2vesta grid-run input.fch esp_map \
  --function esp \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub
```

With `--preset auto`, mapped defaults are `esp` for ESP/nuclear ESP, `alie`
for ALIE, `lea`/`leae` for LEA/LEAE, `iri` for sign(lambda2)rho, `vdw-map`
for vdW potential, and `surface-map` for other functions.  Batch orbital export rejects
`--surface-cube`.

## Outputs

Single-run outputs:

- `multiwfn_grid_input.txt`
- `multiwfn_grid.stdout.txt`
- `multiwfn_grid.stderr.txt`
- `multiwfn_grid_raw/<Multiwfn-default>.cub`
- `<stem>_<function>.cub`
- `multiwfn_grid_recipe.md`
- optional `<stem>_<function>_<preset>_cube.vesta`
- optional `<stem>_<function>_<preset>_cube_vesta_recipe.md`

Batch outputs:

- `multiwfn_grid_batch_recipe.md`
- one child directory per orbital, each containing the single-run outputs
  above

The runner sets `Multiwfnpath`, `MULTIWFNPATH`, and `MultiwfnPATH` to the
selected Multiwfn executable directory.

## Choosing VESTA Output

By default, `--preset auto` maps the selected function to a `cube-preset`
style.  Use `--no-vesta` when only the cube is needed.

Examples:

```bash
multiwfn2vesta grid-run input.fch products --function density
multiwfn2vesta grid-run input.fch products --function spin-polarization
multiwfn2vesta grid-run input.fch products --function orbital --orbital h
multiwfn2vesta grid-run input.fch products --orbitals h l l+1 --no-vesta
multiwfn2vesta grid-run input.fch products --function elf
multiwfn2vesta grid-run input.fch products --function esp --no-vesta
multiwfn2vesta grid-run input.fch products --function esp --surface-cube density.cub --grid-mode cube --grid-cube density.cub
multiwfn2vesta grid-run input.fch products --function hamiltonian-ked --no-vesta
multiwfn2vesta grid-run input.fch products --function alie --no-vesta
multiwfn2vesta grid-run input.fch products --function pair-function --reference-point 0 0 0 --pair-function-type 1 --pair-correlation-type 3
multiwfn2vesta grid-run input.fch products --function source-function --reference-point 0 0 0 --source-function-mode 1
multiwfn2vesta grid-run input.fch products --function local-electron-affinity
multiwfn2vesta grid-run input.fch products --function user-function --user-function-index 49
multiwfn2vesta grid-run input.fch products --function edr --edr-length 0.85
multiwfn2vesta grid-run input.fch products --function edrdmax --edr-exponents 12 3.0 1.2
multiwfn2vesta grid-run input.fch products --function becke --becke-atoms 1 4
multiwfn2vesta grid-run input.fch products --function hirshfeld --hirshfeld-atoms '2,3,7-10'
multiwfn2vesta grid-run input.fch products --function delta-g
multiwfn2vesta grid-run input.fch products --function hirshfeld-delta-g
multiwfn2vesta grid-run input.fch products --function vdw-potential
```

For two-cube mapped surfaces, use `--surface-cube` when the new grid cube
should color an existing density/surface cube.  Use manual `cube-preset` when
the surface and texture cubes are both already available or need special
handling.

## Validation

Focused tests:

```bash
PYTHONPATH=src python3 -m unittest tests.test_multiwfn_grid tests.test_cli -v
```

Real H2O noGUI density smoke:

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
`h2o_density_density_cube.vesta`, and both recipe files.

Real H2O noGUI ELF smoke:

```bash
bin/multiwfn2vesta grid-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_elf/products \
  --function elf \
  --grid-points 12 12 12 \
  --stem h2o \
  --timeout 180 \
  --no-vesta
```

Observed output: raw `ELF.cub`, processed `h2o_elf.cub`, and recipe.

Real H2O noGUI ESP mapped-surface smoke:

```bash
bin/multiwfn2vesta grid-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_surface_cube_map_20260610/h2o_esp_map \
  --function esp \
  --surface-cube /mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_surface_map_20260610/h2o_density/h2o_density.cub \
  --grid-mode cube \
  --grid-cube /mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_surface_map_20260610/h2o_density/h2o_density.cub \
  --timeout 300 \
  --stem h2o
```

Observed output: `h2o_esp.cub`, `h2o_esp_esp_cube.vesta`, and recipes showing
the density cube as Surface Cube and ESP as Texture Cube.
