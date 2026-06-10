# Skill: Multiwfn basin cube presets for VESTA

## When to use

Use this after Multiwfn basin analysis has already exported cube files from
basin analysis option `-5`.  The maintained project layer starts from the
exported cubes; it does not yet automate the full basin-generation menu.

## Individual basin surfaces

For individual binary basin cubes such as `basin0001.cub`, Multiwfn writes
`1` inside the selected basin and `0` outside.  Use:

```bash
multiwfn2vesta cube-preset basin basin0001.cub basin_products
```

The preset uses a single isosurface at `0.5`.

Aliases:

- `basin-cube`
- `binary-basin`
- `aim-basin`
- `elf-basin`

## Basin type maps

For `basinsyn.cub`, Multiwfn writes monosynaptic basin regions as `-1`,
disynaptic basin regions as `+1`, and other regions as `0`.  Use:

```bash
multiwfn2vesta cube-preset basin-type basinsyn.cub basin_products
```

The preset uses signed surfaces at `+0.5` and `-0.5`.

Aliases:

- `basinsyn`
- `basin-synaptic`
- `elf-basin-type`

## Important caveat

Do not use `cube-preset basin` directly on the all-index `basin.cub` file.
The preset rejects an input file named `basin.cub`, because that file stores
basin indices as grid values rather than a binary membership mask.  For
boundary visualization, export individual `basinNNNN.cub` files from Multiwfn
and use the binary basin preset on those files.

## Source evidence

Local Multiwfn `basin.f90` option `-5` documents these exports:

- `basin.cub`: all-index grid, value is basin index.
- `basinNNNN.cub`: individual binary basin membership cube.
- `basinsel.cub`: selected-basin real-space function values.
- `basinsyn.cub`: monosynaptic `-1` and disynaptic `+1` regions.

The source also states that individual binary basin cubes should be visualized
with isovalue `0.5`.
