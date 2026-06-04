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
6. Use a GUI-authored VESTA template or hand-configured VESTA scene to bind
   the processed color cube to the IRI surface cube until the `.vesta`
   isosurface/color-volume fields are fully automated.

## Color transform

Use the historical project transform unless the figure requires a different
color scale:

```text
if value > 0:
    value = 2 * value
value = clamp(value, -0.04, 0.04)
```

This reproduces the old interactive Multiwfn grid-processing sequence without
calling Multiwfn a second time.

## Implementation references

- `project/src/multiwfn2vesta/cub.py`
- `project/src/multiwfn2vesta/MultiwfnRunner.py`
- `project/tests/test_iri_cube.py`

## Cautions

- Do not change cube origin/grid vectors while doing scalar color remapping.
- Keep strict cube parsing enabled for production IRI processing so truncated
  or overlong cube data fail instead of generating a misleading color field.
- For IRI + AIM overlays in VESTA, AIM coordinates must be shifted by
  `-cube_origin_bohr * bohr_to_angstrom` for Multiwfn/Gaussian cube files.  The
  AIM converter exposes this as `--cube-frame-from-cube`.
- Do not assume that editing `ISURF` alone reproduces Multiwfn's
  `IRIfill.vmd`; VESTA also records section/texture/color-volume state.
  Prefer a GUI-authored VESTA template before making IRI isosurface rendering a
  maintained automation path.
- If a future workflow really needs spatial stretching, implement it as an
  explicit affine resampling step and test against a small synthetic cube.
- Keep the color cube grid-compatible with the IRI surface cube.
