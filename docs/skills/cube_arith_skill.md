# Skill: Cube arithmetic for density differences and Fukui maps

Use this workflow when compatible ABACUS or Multiwfn cube files should be
combined before VESTA visualization.  Typical cases are density differences,
Fukui functions, and dual descriptors.

## Command

Generic linear combination:

```bash
multiwfn2vesta cube-arith cube_arith_products \
  --term 1.0 rho_a.cub \
  --term -1.0 rho_b.cub \
  --stem density_difference
```

Named operations:

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

## Formulae

- `density-difference`: `plus - minus`
- `fukui-plus`: `rho(N+1) - rho(N)`
- `fukui-minus`: `rho(N) - rho(N-1)`
- `dual-descriptor`: `rho(N+1) - 2*rho(N) + rho(N-1)`

## Outputs

- `<stem>.cub`
- `<stem>_cube_arith_recipe.md`
- by default, a VESTA output via `cube-preset`; `--preset auto` uses
  `density` for `fukui-plus/minus` and `signed` otherwise

Use `--no-vesta` for cube-only output.  Use `--preset density`, `--preset
signed`, or another `cube-preset` value to override the automatic display
style.

## Requirements

- All input cubes must share grid origin, grid vectors, grid point counts, and
  cube unit convention.
- With `--cube-units auto`, positive grid counts are interpreted as Bohr and
  negative grid counts as Angstrom; mixed conventions are rejected by default.
- Atom lists must also match by default.
- Use `--no-strict-atoms` only when the atom list differs deliberately but the
  shared grid is trustworthy.
- The output path must not be any input cube path; the command refuses to
  overwrite inputs.

## ABACUS and Multiwfn context

`cube-arith` does not generate charged-state or excited-state wavefunctions.
Generate the source cubes first, for example:

- ABACUS `out_chg`, `out_pchg`, `out_wfc_norm`, or `out_wfc_re_im`
- `multiwfn2vesta grid-run ... --function density`
- `multiwfn2vesta grid-run ... --function orbital`

For comparable Fukui/dual-descriptor maps, all source cubes should be
generated on the same grid.  With Multiwfn, use `grid-run --grid-mode cube
--grid-cube reference.cub` after making the first cube.

## Validation

```bash
PYTHONPATH=src python3 -m unittest tests.test_cube_arith tests.test_cli -v
bin/multiwfn2vesta cube-arith --help
```
