# Skill: Multiwfn Fukui and dual-descriptor runner

Use this workflow when neutral and charged-state wavefunction files should be
converted into shared-grid density cubes, then combined into Fukui or
dual-descriptor maps for VESTA.

## Command

```bash
multiwfn2vesta fukui-run fukui_products \
  --neutral neutral.molden \
  --anion anion.molden \
  --cation cation.molden \
  --operation all \
  --grid-mode points \
  --grid-points 80 80 80
```

Inputs can be any file accepted by Multiwfn and the underlying `grid-run`,
such as `.molden`, `.fch`, `.fchk`, `.wfn`, or `.wfx`.

## Operation Logic

`fukui-run` is a composition layer:

1. Generate the neutral density cube through `grid-run --function density`.
2. Generate required charged-state density cubes through `grid-run
   --function density --grid-mode cube --grid-cube <neutral_density.cub>`.
3. Combine the density cubes through `cube-arith`.

The charged-state cubes therefore reuse the neutral density cube as the
reference grid.  The runner does not invent a new Fukui formula or duplicate
cube arithmetic.

## Operations

All operations:

```bash
multiwfn2vesta fukui-run fukui_products \
  --neutral neutral.fch \
  --anion anion.fch \
  --cation cation.fch \
  --operation all
```

Fukui plus only:

```bash
multiwfn2vesta fukui-run fplus_products \
  --neutral neutral.fch \
  --anion anion.fch \
  --operation fukui-plus
```

Fukui minus only:

```bash
multiwfn2vesta fukui-run fminus_products \
  --neutral neutral.fch \
  --cation cation.fch \
  --operation fukui-minus
```

Dual descriptor only:

```bash
multiwfn2vesta fukui-run dual_products \
  --neutral neutral.fch \
  --anion anion.fch \
  --cation cation.fch \
  --operation dual-descriptor
```

Formulae:

- `fukui-plus`: `rho(N+1) - rho(N)`
- `fukui-minus`: `rho(N) - rho(N-1)`
- `dual-descriptor`: `rho(N+1) - 2*rho(N) + rho(N-1)`

## Outputs

Top level:

- `multiwfn_fukui_recipe.md`

Density child runs:

- `neutral_density/`
- `anion_density/` when required
- `cation_density/` when required

Each density child is an ordinary `grid-run` output directory with the
Multiwfn command stream, stdout/stderr logs, raw cube directory, processed
density cube, and recipe.  Add `--state-vesta` if per-state density VESTA
files are useful.

Map child runs:

- `fukui_plus/`
- `fukui_minus/`
- `dual_descriptor/`

Each map child is an ordinary `cube-arith` output directory with the map cube,
cube-arithmetic recipe, and optional VESTA output.  Use `--no-vesta` for
cube-only map generation.

## Grid Controls

The neutral state accepts the same grid controls as `grid-run`:

```bash
multiwfn2vesta fukui-run fukui_products \
  --neutral neutral.fch \
  --anion anion.fch \
  --operation fukui-plus \
  --grid-mode spacing \
  --grid-spacing 0.20
```

For ABACUS periodic Molden files, prefer `--grid-mode spacing`,
`--grid-mode pbc-cell`, or an explicit reference cube.  Avoid interpreting
charged periodic supercells without checking the electrostatic setup.

## VESTA Style

By default, `--preset auto` follows `cube-arith`:

- `fukui-plus` and `fukui-minus` use the `density` preset.
- `dual-descriptor` uses the `signed` preset.

Override as needed:

```bash
multiwfn2vesta fukui-run dual_products \
  --neutral neutral.fch \
  --anion anion.fch \
  --cation cation.fch \
  --operation dual-descriptor \
  --preset signed \
  --isosurface 0.002 \
  --structure molecule
```

## Caveats

- This route is most defensible for finite systems with comparable
  geometries.
- Charged periodic cells, metal slabs, smearing, and compensating-background
  setups require separate physical review.
- If density cubes already exist and are known to be compatible, use
  `cube-arith` directly.

## Validation

```bash
PYTHONPATH=src python3 -m unittest tests.test_multiwfn_fukui tests.test_cli
bin/multiwfn2vesta fukui-run --help
```
