# Skill: IRI cube preparation for VESTA

Use this when preparing Multiwfn IRI output for VESTA.

## Inputs

- A wavefunction file accepted by Multiwfn.
- Multiwfn-generated `func1.cub` and `func2.cub`, or a workflow that creates
  them through weak-interaction menu `20 -> 4`.

## Workflow

1. Let Multiwfn calculate the paired IRI data.
2. Treat `func1.cub` as `sign(lambda2)rho` color data.
3. Treat `func2.cub` as the IRI isosurface data.
4. Run `process_iri_color_cube` on `func1.cub`.
5. If adding AIM paths/CPs, generate the AIM `.vesta` with
   `--cube-frame-from-cube func2.cub` so the AIM sites align with VESTA's cube
   import frame.
6. In VESTA, keep the surface cube as `IMPORT_DENSITY` and attach the processed
   color cube as `IMPORT_TEXTURE`.  The current smoke recipe uses `ISURF=1.0`,
   `SECTS 0 0`, and `TEX3P` percentages computed from the surface-sampled
   texture range.

## Color transform

Use the VESTA-oriented transform unless the figure requires a different color
scale:

```text
if value > 0:
    value = 2 * value
value = max(value, -0.04)
```

This keeps positive values above `0.04` in the cube.  The upper physical color
bound is handled later by converting the target range to VESTA `TEX3P`
percentages.  Passing `upper=0.04` to `process_iri_color_cube` reproduces the
old fully clipped behavior for comparison.

## Implementation references

- `project/src/multiwfn2vesta/cub.py`
- `project/src/multiwfn2vesta/MultiwfnRunner.py`
- `project/tests/test_iri_cube.py`

## Cautions

- Do not change cube origin/grid vectors while doing scalar color remapping.
- Keep strict cube parsing enabled for production IRI processing so truncated
  or overlong cube data fail instead of generating a misleading color field.
- Keep the physical upper color bound out of the cube values by default.
  VESTA's `TEX3P` range is best treated as normalized/percentage state, so do
  not write `-0.04 0.04` there and do not force all values above `0.04` to
  `0.04`.  Convert the target physical range to percentages:
  `p = (target_value - sampled_min) / (sampled_max - sampled_min)`.
- For IRI + AIM overlays in VESTA, AIM coordinates must be shifted by
  `-cube_origin_bohr * bohr_to_angstrom` for Multiwfn/Gaussian cube files.  The
  AIM converter exposes this as `--cube-frame-from-cube`.
- Do not assume that editing `ISURF` alone reproduces Multiwfn's
  `IRIfill.vmd`; VESTA also records section/texture/color-volume state.
  Current local evidence also needs `IMPORT_TEXTURE`, `SECTS 0 0`, and
  percentage-style `TEX3P`; H2O-HF needs about `0..12.299` for physical
  `[-0.04, 0.04]`.
- If a future workflow really needs spatial stretching, implement it as an
  explicit affine resampling step and test against a small synthetic cube.
- Keep the color cube grid-compatible with the IRI surface cube.
