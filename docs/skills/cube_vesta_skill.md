# Skill: Cube to VESTA workflow

Use this when an ABACUS or Multiwfn scalar cube should become a VESTA
isosurface file without opening VESTA interactively.

## Command

Single cube:

```bash
multiwfn2vesta cube-vesta density.cub cube_products --isosurface 0.01
```

Signed positive/negative cube:

```bash
multiwfn2vesta cube-vesta orbital.cub cube_products \
  --surface-mode signed \
  --isosurface 0.02
```

Surface cube plus texture/color cube:

```bash
multiwfn2vesta cube-vesta surface.cub cube_products \
  --texture-cube texture.cub \
  --isosurface 0.01 \
  --tex-physical -0.05 0.05
```

Surface-sampled texture scaling:

```bash
multiwfn2vesta cube-vesta surface.cub cube_products \
  --texture-cube texture.cub \
  --isosurface 0.01 \
  --tex-physical -0.05 0.05 \
  --tex-range-source surface-band
```

## Outputs

- `<output_dir>/<stem>_cube.vesta`
- `<output_dir>/<stem>_cube_vesta_recipe.md`
- copied cube dependencies unless `--no-copy-cubes` is used
- if surface and texture cubes share a basename but come from different
  directories, the later dependency is renamed, for example
  `foo.cub` plus `foo_texture.cub`, so VESTA imports do not point at an
  overwritten file

## VESTA Template Rules

- Surface cube goes in `IMPORT_DENSITY 1`.
- Texture/color cube goes in `IMPORT_TEXTURE`.
- Default sections are off: `SECTS 0 0`.
- `ISURF` stores the requested isosurface level.
- `--surface-mode single` writes one `ISURF` entry.
- `--surface-mode signed` treats `--isosurface X` as a magnitude and writes
  both `+abs(X)` and `-abs(X)`.  The default colors are yellow for positive
  values and blue for negative values.  Use `--positive-rgb`,
  `--negative-rgb`, and `--surface-opacity` to override the VESTA surface
  style.
- `TEX3P` stores VESTA percentage/normalized values, not physical scalar
  limits.
- `--tex-physical MIN MAX` converts physical limits to percentages using the
  selected texture reference range.
- `--tex-range-source full-cube` uses the full texture cube min/max.
- `--tex-range-source surface-band` uses texture values from grid points whose
  surface-cube values are close to the requested `--isosurface`.  Use
  `--surface-band` to set the half-width manually; otherwise a conservative
  automatic band is used.  If the band has no non-degenerate texture range,
  `--surface-nearest` nearest grid points are used as a fallback.

## Cube and Structure Rules

- Cube data counts are strict by default; malformed cube files should fail
  rather than generate misleading figures.
- Texture cube grid origin, vectors, and counts must match the surface cube by
  default.
- `--cube-units auto` treats ordinary positive cube grid counts as Bohr and
  negative grid counts as Angstrom.  Override with `--cube-units bohr` or
  `--cube-units angstrom` when needed.
- `--structure auto` creates a `CRYSTAL` structure phase when the cube origin
  is zero and atoms fall inside the cube cell.  Otherwise it creates a
  `MOLECULE` phase with coordinates shifted by the cube origin.

## Current Limits

- No VESTA rendering is launched by this command.
- Signed positive/negative isosurfaces are implemented as a generic VESTA
  preset, but analysis-specific Multiwfn command streams for producing orbital,
  density-difference, Fukui, or dual-descriptor cubes are still separate future
  work.
- Surface-band sampling uses grid-point values, not interpolation exactly on
  the triangulated VESTA isosurface.
- AIM/BCP pseudo-site overlays remain in the AIM/AIM+IGMH workflows, not this
  generic cube generator.

## Validation

```bash
PYTHONPATH=src python3 -m unittest tests.test_cube_vesta -v
```

Real smoke:

```text
/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_cli_smoke_20260610/
```
