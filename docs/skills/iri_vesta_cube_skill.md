# Skill: IRI cube preparation for VESTA

Use this when generating or preparing Multiwfn IRI/RDG output for VESTA.

## Inputs

- A wavefunction file accepted by Multiwfn, such as `.molden`, `.fch`,
  `.fchk`, `.wfn`, or `.wfx`.
- Multiwfn-generated `func1.cub` and `func2.cub`, or the maintained
  `multiwfn2vesta iri-run` workflow that creates them through the
  weak-interaction menu stream.

## Maintained command

```bash
multiwfn2vesta iri-run input.molden iri_products --timeout 300
```

This command:

- discovers Multiwfn from explicit `--multiwfn`, environment variables,
  workspace tools, then `PATH`;
- writes `multiwfn_iri_input.txt` with the exact command stream;
- writes `multiwfn_iri.stdout.txt` and `multiwfn_iri.stderr.txt`;
- runs Multiwfn in `multiwfn_iri_raw/`;
- preserves raw `func1.cub`, `func2.cub`, and `output.txt` when present;
- writes `<stem>_IRI1.cub` as the processed texture/color cube;
- writes `<stem>_IRI2.cub` as the surface cube;
- calls `cube-preset iri` to write `<stem>_iri_cube.vesta` and a recipe
  unless `--no-vesta` is supplied.

Use `--commands-file commands.txt` when the default weak-interaction command
stream is not suitable.  Use `--surface-band` or `--surface-nearest` to tune
how the VESTA `TEX3P` percentage range is derived from values near the
displayed surface.

## Workflow

1. Prefer `multiwfn2vesta iri-run` for maintained runs from a wavefunction
   file.
2. Let Multiwfn calculate the paired IRI data.
3. Treat `func1.cub` as `sign(lambda2)rho` color data.
4. Treat `func2.cub` as the IRI isosurface data.
5. Run `process_iri_color_cube` on `func1.cub`.
6. If adding AIM paths/CPs, generate the AIM `.vesta` with
   `--cube-frame-from-cube func2.cub` so the AIM sites align with VESTA's cube
   import frame.
7. In VESTA, keep the surface cube as `IMPORT_DENSITY` and attach the processed
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

- `project/src/multiwfn2vesta/multiwfn_iri.py`
- `project/src/multiwfn2vesta/cub.py`
- `project/src/multiwfn2vesta/cube_preset.py`
- `project/tests/test_multiwfn_iri.py`
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

## Validation

Focused tests:

```bash
PYTHONPATH=src python3 -m unittest tests.test_multiwfn_iri tests.test_cli tests.test_iri_cube -v
```

Real H2O noGUI smoke:

```text
/mnt/g/work/multiwfn2vesta/smoke/multiwfn_iri_run_smoke_20260610/
```

Observed output: raw `func1.cub`/`func2.cub`, processed `h2o_IRI1.cub` and
`h2o_IRI2.cub`, `h2o_iri_cube.vesta`, and
`h2o_iri_cube_vesta_recipe.md`; VESTA was not launched.
