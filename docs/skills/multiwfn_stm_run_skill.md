# Skill: Multiwfn STM/LDOS runner to VESTA

## When to use

Use `stm-run` when a Multiwfn-readable wavefunction file contains GTO/GTF
information and the target visualization is a constant-current STM/LDOS
isosurface in VESTA.

## Command

```bash
multiwfn2vesta stm-run input.molden stm_products \
  --bias -1.0 \
  --fermi -4.8 \
  --grid-points 120 120 60 \
  --x-range -6 6 \
  --y-range -6 6 \
  --z-range 2 8
```

The maintained stream is:

```text
300
4
1
4
NX,NY,NZ
0
2
0
-1
0
q
```

`300` enters Multiwfn other functions part 3, `4` enters STM, `1` switches
from default constant-distance mode to constant-current mode, `0` calculates,
and post-processing option `2` exports `STM.cub`.

## Options

- `--bias VALUE`: set bias voltage in V.
- `--fermi VALUE`: set Fermi energy in eV.
- `--prepare-fermi-temperature TEMP_K`: insert Multiwfn `300 -> 9` before STM
  to prepare occupations, useful for ABACUS metallic/slab Molden files with
  smearing or non-integer occupations.
- `--grid-points NX NY NZ`: set the 3D STM cube grid.
- `--x-range MIN MAX`, `--y-range MIN MAX`, `--z-range MIN MAX`: set the STM
  box ranges in Angstrom.
- `--no-vesta`: keep only cubes and logs.
- `--preset stm`, `--isosurface VALUE`: override the VESTA display preset or
  STM isosurface.

## Outputs

- `multiwfn_stm_input.txt`
- `multiwfn_stm.stdout.txt`
- `multiwfn_stm.stderr.txt`
- `multiwfn_stm_raw/STM.cub`
- `<stem>_stm.cub`
- `multiwfn_stm_recipe.md`
- `<stem>_stm_cube.vesta`
- `<stem>_stm_cube_vesta_recipe.md`

## VESTA preset

`cube-preset stm` is a single positive isosurface preset for `STM.cub`.
Aliases: `ldos`, `stm-ldos`, `tunneling-current`.  Default isosurface is
`0.001`; tune it per bias and system.

## Validated smoke

```bash
bin/multiwfn2vesta stm-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_stm_run_smoke_20260610/h2o \
  --grid-points 10 10 6 \
  --stem h2o \
  --timeout 300
```

This generated `h2o_stm.cub` and `h2o_stm_cube.vesta`; the cube contains 600
grid points with data range `3.7332e-13` to `0.0151741`.

The optional Fermi-preparation branch was also smoke-tested:

```bash
bin/multiwfn2vesta stm-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_stm_run_smoke_20260610/h2o_prepare_fermi \
  --grid-points 6 6 4 \
  --prepare-fermi-temperature 298.15 \
  --stem h2o \
  --timeout 300 \
  --no-vesta
```

This generated `h2o_stm.cub` with 144 grid points and range `3.7332e-13` to
`0.00603356`.

## Caveats

- The wavefunction must contain GTF/GTO information; otherwise Multiwfn STM
  returns without producing `STM.cub`.
- The runner exports a 3D cube suitable for VESTA isosurfaces, not Multiwfn's
  GUI 2D STM plane plot.
- Positive bias needs enough unoccupied orbital information in the wavefunction
  file.
