# IRI VESTA cube coloring workflow

This project keeps Multiwfn responsible for calculating IRI grids, but no
longer needs a second interactive Multiwfn pass to prepare the VESTA coloring
cube.

## Multiwfn outputs

The weak-interaction IRI workflow writes two cube files:

- `func1.cub`: `sign(lambda2)rho`, used as the surface coloring scalar.
- `func2.cub`: IRI, used as the isosurface scalar.

The VESTA/VMD convention is to draw the IRI isosurface from `func2.cub` and
color it with `func1.cub`.

## Python color remapping

The old `MultiwfnRunner.IRI()` command stream reopened `func1.cub` in Multiwfn
main function 13 and applied this sequence:

1. `abs(A)`
2. `abs(A) / 3`
3. `abs(A) / 3 + A`
4. `1.5 * (abs(A) / 3 + A)`
5. clamp values below `-0.04` to `-0.04`
6. clamp values above `0.04` to `0.04`

The historical fully clipped output is equivalent to:

```text
mapped = A                  if A <= 0
mapped = 2 * A              if A > 0
mapped = min(max(mapped, -0.04), 0.04)
```

The current VESTA-oriented default keeps the same positive scaling and lower
clip but does not clip values above `0.04`.  The upper physical color bound is
handled by converting `[-0.04, 0.04]` to VESTA `TEX3P` percentages.

The implementation is now in:

- `multiwfn2vesta.cub.transform_iri_color_values`
- `multiwfn2vesta.cub.process_iri_color_cube`
- `multiwfn2vesta.cub.vesta_percent_range_for_values`

`MultiwfnRunner.IRI()` calls `process_iri_color_cube("func1.cub",
"<basename>_IRI1.cub")` directly, then renames `func2.cub` to
`<basename>_IRI2.cub`.

## Direct API

```python
from multiwfn2vesta.cub import process_iri_color_cube

process_iri_color_cube(
    "func1.cub",
    "molecule_IRI1.cub",
    lower=-0.04,
    upper=None,
    positive_scale=2.0,
)
```

The output cube preserves the input cube origin, grid vectors, atoms, and data
shape.  Only scalar values are changed.  The IRI production path uses strict
cube parsing by default: if the scalar data count does not match `nx * ny * nz`,
the converter raises an error instead of padding or truncating the color field.

To write VESTA `TEX3P`, convert the target physical color range to percentages
from the values VESTA will sample:

```python
from multiwfn2vesta.cub import vesta_percent_range_for_values

tex_min, tex_max = vesta_percent_range_for_values(
    sampled_texture_values,
    target_lower=-0.04,
    target_upper=0.04,
)
```

## Notes

- Cube headers and atom coordinates remain in the cube file's native units.
- The color cube should stay grid-compatible with the IRI surface cube for
  VESTA color mapping.
- Missing `func1.cub`, missing `func2.cub`, or malformed cube data should be
  treated as incomplete IRI output, not as a successful VESTA-ready result.
- If an AIM `.vesta` layer is imported over a VESTA-opened cube, generate it
  with `multiwfn2vesta.aim_vesta --cube-frame-from-cube <surface.cub>`.  VESTA
  shifts cube atoms into a cube-origin frame, while Multiwfn AIM PDB
  coordinates are raw Angstrom coordinates.  The current converter treats the
  cube origin as a Multiwfn/Gaussian cube origin in Bohr.
- Spatial cube stretching/resampling is a separate operation.  The historical
  project code only showed scalar-value remapping for the coloring field.
- For VESTA surface coloring, keep the physical `[-0.04, 0.04]` clipping in the
  VESTA `TEX3P` percentage conversion, not by forcing all positive cube values
  above `0.04` back to `0.04`.  Local VESTA evidence indicates `TEX3P` should be
  treated as a normalized/percentage range, not as the physical
  `sign(lambda2)rho` min/max.  Convert the desired physical color scale to
  percentages using the texture values sampled by the selected isosurface.

## VESTA Isosurface Caveat

Multiwfn's `IRIfill.vmd` loads two cube files:

- `func1.cub`: color volume, `sign(lambda2)rho`
- `func2.cub`: IRI volume, drawn as `Isosurface 1.0`

VESTA CLI smoke tests showed that simply opening `func2.cub` and patching the
saved `.vesta` `ISURF` value to `1.0` does not reproduce the VMD scene.  The
saved VESTA files still contain section/texture-related state such as `SECTS`,
`TEX3P`, `SECTP`, and `CONTR`, and the export can show a large colored plane
instead of a clean IRI isosurface.

The current H2O-HF smoke evidence is closer:

- `IMPORT_DENSITY` points to the processed IRI surface cube (`IRI2`).
- `IMPORT_TEXTURE` points to the processed `sign(lambda2)rho` color cube
  (`IRI1`).
- `ISURF` level is `1.0`.
- `SECTS   0  0` disables section planes.
- `TEX3P` stores percentages.  For the H2O-HF smoke, the `IRI2=1.0` surface
  samples about `[-0.04, -0.0334954]` from the processed color cube, so the
  target physical range `[-0.04, 0.04]` corresponds to about `0..12.299`.

A GUI-authored VESTA template is still useful before making this a maintained
automation path, because `COMPS`, color scales, and object routing are only
partly reverse-engineered.
