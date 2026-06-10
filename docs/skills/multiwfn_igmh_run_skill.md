# Skill: Multiwfn IGMH command-stream runner

Use this workflow when the input is a Multiwfn-readable wavefunction file and
the goal is to generate IGMH interfragment cubes, then prepare a VESTA
mapped-surface file.

## Command

```bash
multiwfn2vesta igmh-run input.molden igmh_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --grid-mode spacing \
  --grid-spacing 0.25 \
  --timeout 600
```

Accepted wavefunction inputs are whatever the local Multiwfn executable can
read, typically `.molden`, `.fch`, `.fchk`, `.wfn`, or `.wfx`.

## Fragment Rules

Pass one `--fragment` per Multiwfn fragment prompt.  The strings are forwarded
to Multiwfn, so use the same atom-index syntax used interactively:

- `1-48`
- `1,4,9`
- `49-60`
- `c` for complement-style input when the prompt accepts it

The default generated stream requires at least two fragments.  Use
`--commands-file commands.txt` only when the complete Multiwfn prompt sequence
needs to be replaced.

## Command Stream

For two fragments and an explicit finite-molecule point grid, the generated
stream is:

```text
20
11
2
<fragment_1>
<fragment_2>
4
NX,NY,NZ
3
0
0
q
```

`20` enters the weak-interaction analysis menu, `11` selects IGMH, `3` in the
post-processing step exports cube files, and the final zeros unwind the menus.
The runner writes this stream to `multiwfn_igmh_input.txt` before launching
Multiwfn.

Supported grid modes:

- `low`, `medium`, `high`: Multiwfn built-in grid levels
- `points`: explicit `NX,NY,NZ` for finite non-PBC inputs only
- `spacing`: explicit grid spacing in Bohr
- `cube`: reuse a reference cube grid
- `pbc-cell`: periodic-cell style prompt values

For periodic Molden files containing `[Cell]`, do not use `points`.  Multiwfn
routes option `4` to `setgrid_for_PBC(..., iskip=1)`, so the next response is
read as a single grid spacing rather than `NX,NY,NZ`.  The runner detects
`[Cell]` and rejects `points` before launching Multiwfn.  Use `spacing` for a
whole-cell spacing prompt, or `pbc-cell` to provide origin, box lengths, and
spacing.

## Outputs

The runner writes:

- `multiwfn_igmh_input.txt`
- `multiwfn_igmh.stdout.txt`
- `multiwfn_igmh.stderr.txt`
- `multiwfn_igmh_raw/dg_inter.cub`
- `multiwfn_igmh_raw/sl2r.cub`
- `<stem>_dg_inter.cub`
- `<stem>_sl2r.cub`
- `<stem>_dg_intra.cub` and `<stem>_dg.cub` when Multiwfn writes them
- `<stem>_igmh_cube.vesta` unless `--no-vesta` is used
- `<stem>_igmh_cube_vesta_recipe.md`
- `multiwfn_igmh_recipe.md`

The VESTA layer uses `cube-preset igmh`: surface `dg_inter.cub`, texture
`sl2r.cub`, isosurface `0.01`, and texture physical range `-0.05` to `0.05`.

## Discovery

Use `--multiwfn /path/to/Multiwfn_noGUI` for an explicit executable.  Without
that, discovery follows the project executable rules:

1. Multiwfn environment variables such as `MULTIWFN_PATH`, `MULTIWFNPATH`,
   `Multiwfnpath`, and `MultiwfnPATH`
2. workspace-local Multiwfn tools
3. shell `PATH`

The subprocess receives `Multiwfnpath`, `MULTIWFNPATH`, and `MultiwfnPATH`
pointing at the selected executable directory.

## ABACUS Route

For ABACUS LCAO workflows, first make a Multiwfn-readable Molden file:

```bash
multiwfn2vesta abacus-molden /path/to/abacus_calc ABACUS_Multiwfn.molden
multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus
```

Keep `[Nval]` enabled for pseudopotential systems, especially AIM/IGMH/ESP
analysis.

## Smoke

Real noGUI H2O smoke:

```text
/mnt/g/work/multiwfn2vesta/smoke/multiwfn_igmh_run_smoke_20260610/h2o/
```

Command shape:

```bash
bin/multiwfn2vesta igmh-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_igmh_run_smoke_20260610/h2o \
  --fragment 1 \
  --fragment 2-3 \
  --grid-mode points \
  --grid-points 8 8 8 \
  --stem h2o \
  --timeout 180
```

The run returned 0 and generated `h2o_dg_inter.cub`, `h2o_sl2r.cub`,
`h2o_dg_intra.cub`, `h2o_dg.cub`, and `h2o_igmh_cube.vesta` without
launching the VESTA UI.

## Boundaries

- This runner automates standard IGMH.  IGM, mIGM, and aIGM command streams
  remain separate future increments.
- AIM path/BCP overlays are handled after the cube layer by
  `multiwfn2vesta aim-igmh`.
- If VESTA rendering is needed, keep it as an explicit later step because the
  Windows VESTA automation path can still take desktop focus.
