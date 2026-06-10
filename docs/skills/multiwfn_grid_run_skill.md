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
  `gradient.cub`, preset `density`.
- `laplacian`, aliases `lap`, `laplacian-rho`: function `3`, raw
  `laplacian.cub`, preset `laplacian` with signed positive/negative
  isosurfaces.
- `orbital`, aliases `mo`, `wavefunction`, `mo-value`: function `4`, raw
  `MOvalue.cub`, preset `signed`, requires `--orbital` for one orbital or
  `--orbitals` for batch export.
- `spin-density`: function `5`, raw `spindensity.cub`, preset
  `spin-density` with signed positive/negative isosurfaces.
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
- `alie`, aliases `average-local-ionization-energy`, `avglocion`: function
  `18`, raw `avglocion.cub`, preset `density`; mapped preset `alie` with
  `--surface-cube`.
- `delta-g`: function `22`, raw `Delta_g.cub`, preset `density`.
- `iri`: function `24`, raw `IRI.cub`, preset `density`.
- `vdw-potential`: function `25`, raw `vdWpot.cub`, preset `signed`;
  mapped preset `vdw-map` with `--surface-cube`.
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
`--expected-cube`, and `--raw-dir` because those options would make the child
run ownership ambiguous.

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
for ALIE, `iri` for sign(lambda2)rho, `vdw-map` for vdW potential, and
`surface-map` for other functions.  Batch orbital export rejects
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
multiwfn2vesta grid-run input.fch products --function orbital --orbital h
multiwfn2vesta grid-run input.fch products --orbitals h l l+1 --no-vesta
multiwfn2vesta grid-run input.fch products --function elf
multiwfn2vesta grid-run input.fch products --function esp --no-vesta
multiwfn2vesta grid-run input.fch products --function esp --surface-cube density.cub --grid-mode cube --grid-cube density.cub
multiwfn2vesta grid-run input.fch products --function hamiltonian-ked --no-vesta
multiwfn2vesta grid-run input.fch products --function alie --no-vesta
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
