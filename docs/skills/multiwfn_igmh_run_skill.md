# Skill: Multiwfn IGM/mIGM/IGMH command-stream runner

Use this workflow when the input is a Multiwfn-readable wavefunction file and
the goal is to generate IGM, mIGM, or IGMH interfragment cubes, then prepare
a VESTA mapped-surface file.

## Command

```bash
multiwfn2vesta igmh-run input.molden igmh_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --grid-mode spacing \
  --grid-spacing 0.25 \
  --timeout 600

multiwfn2vesta igm-run input.molden igm_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --sl2r-source actual \
  --grid-mode spacing \
  --grid-spacing 0.25

multiwfn2vesta migm-run input.molden migm_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --sl2r-source actual \
  --grid-mode spacing \
  --grid-spacing 0.25
```

Accepted wavefunction inputs are whatever the local Multiwfn executable can
read, typically `.molden`, `.fch`, `.fchk`, `.wfn`, or `.wfx`.

## Method Selection

Use `igmh-run` for the default IGMH stream.  Use `igm-run` or `migm-run` when
the command name should fix the method; these wrappers reject an extra
`--method` argument so the method cannot be silently overridden.  Use
`igmh-run --method igm|migm|igmh` only when a single generic command needs to
choose the method explicitly.

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
IGMH stream is:

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

For IGM and mIGM, the method line changes and a sign(lambda2)rho source prompt
appears when wavefunction information is present:

```text
20
10
2
<fragment_1>
<fragment_2>
1
4
NX,NY,NZ
3
0
0
q
```

Use `10` for IGM and `-10` for mIGM.  The `1` after the fragments means
actual-density sign(lambda2)rho; use `2` for promolecular sign(lambda2)rho.
The CLI exposes this as `--sl2r-source actual|promolecular`.  IGMH always
uses actual density in Multiwfn and rejects `--sl2r-source promolecular`.

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

The runner writes these files, replacing `<method>` with `igmh`, `igm`, or
`migm`:

- `multiwfn_<method>_input.txt`
- `multiwfn_<method>.stdout.txt`
- `multiwfn_<method>.stderr.txt`
- `multiwfn_<method>_raw/dg_inter.cub`
- `multiwfn_<method>_raw/sl2r.cub`
- `<stem>_dg_inter.cub`
- `<stem>_sl2r.cub`
- `<stem>_dg_intra.cub` and `<stem>_dg.cub` when Multiwfn writes them
- `<stem>_<method>_cube.vesta` unless `--no-vesta` is used
- `<stem>_<method>_cube_vesta_recipe.md`
- `multiwfn_<method>_recipe.md`

The VESTA layer uses `cube-preset igmh` for IGMH and `cube-preset igm` for
IGM/mIGM: surface `dg_inter.cub`, texture `sl2r.cub`, isosurface `0.01`,
and texture physical range `-0.05` to `0.05`.

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

Real noGUI H2O IGMH smoke:

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

Real noGUI H2O IGM and mIGM smokes:

```text
/mnt/g/work/multiwfn2vesta/smoke/multiwfn_igm_migm_run_smoke_20260610_review_fix/
```

The `h2o_igm/` and `h2o_migm/` runs used fragments `1` and `2-3`, grid
`8 x 8 x 8`, and generated `h2o_igm_cube.vesta` plus
`h2o_migm_cube.vesta` without launching the VESTA UI.  Their VESTA recipes
record method-specific titles, not the shared canonical preset name.

## Boundaries

- This runner automates standard IGM, mIGM, and IGMH.  aIGM/amIGM command
  streams remain separate future increments.
- AIM path/BCP overlays are handled after the cube layer by
  `multiwfn2vesta aim-igmh`.
- If VESTA rendering is needed, keep it as an explicit later step because the
  Windows VESTA automation path can still take desktop focus.
