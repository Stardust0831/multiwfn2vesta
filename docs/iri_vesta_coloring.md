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

This is equivalent to:

```text
mapped = A                  if A <= 0
mapped = 2 * A              if A > 0
mapped = min(max(mapped, -0.04), 0.04)
```

The implementation is now in:

- `multiwfn2vesta.cub.transform_iri_color_values`
- `multiwfn2vesta.cub.process_iri_color_cube`

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
    upper=0.04,
    positive_scale=2.0,
)
```

The output cube preserves the input cube origin, grid vectors, atoms, and data
shape.  Only scalar values are changed.  The IRI production path uses strict
cube parsing by default: if the scalar data count does not match `nx * ny * nz`,
the converter raises an error instead of padding or truncating the color field.

## Notes

- Cube headers and atom coordinates remain in the cube file's native units.
- The color cube should stay grid-compatible with the IRI surface cube for
  VESTA color mapping.
- Missing `func1.cub`, missing `func2.cub`, or malformed cube data should be
  treated as incomplete IRI output, not as a successful VESTA-ready result.
- Spatial cube stretching/resampling is a separate operation.  The historical
  project code only showed scalar-value remapping for the coloring field.
