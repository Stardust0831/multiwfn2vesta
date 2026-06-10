# Skill: Multiwfn aIGM/amIGM trajectory-average runner

Use this when the input is a Multiwfn-readable trajectory, usually XYZ from
MD/AIMD, and the desired output is an averaged weak-interaction VESTA surface.
For single wavefunction fragment analysis, use `igmh-run`, `igm-run`, or
`migm-run` instead.

## Commands

```bash
multiwfn2vesta aigm-run trajectory.xyz aigm_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --frame-range 1 200 \
  --periodic \
  --grid-mode spacing \
  --grid-spacing 0.25 \
  --timeout 1200

multiwfn2vesta amigm-run trajectory.xyz amigm_products \
  --fragment 1-48 \
  --fragment c \
  --export-tfi \
  --tfi-vesta
```

`aigm-run` is the generic command and accepts `--method aigm|amigm`.
`amigm-run` fixes the method from the command name and rejects an extra
`--method`.

## Multiwfn Stream

The maintained default stream enters Multiwfn weak-interaction menu `20`,
selects `12` for aIGM or `-12` for amIGM, sends two or more fragment
definitions, sends the optional frame range, selects a grid, and then uses
post-processing option `3` to export:

- `avgdg_inter.cub`
- `avgsl2r.cub`

Optional outputs:

- `--export-rdg`: post-processing option `4`, exports `avgRDG.cub`.
- `--export-tfi`: post-processing option `5`, exports `thermflu.cub`.
- `--export-scatter`: post-processing option `2`, exports `output.txt`.
- `--tfi-vesta`: when `--export-tfi` is used, also writes an `aigm-tfi`
  VESTA file from `avgdg_inter.cub` plus `thermflu.cub`.

## Outputs

Default output directory contents include:

- `multiwfn_<method>_input.txt`
- `multiwfn_<method>.stdout.txt`
- `multiwfn_<method>.stderr.txt`
- `multiwfn_<method>_raw/avgdg_inter.cub`
- `multiwfn_<method>_raw/avgsl2r.cub`
- `<stem>_avgdg_inter.cub`
- `<stem>_avgsl2r.cub`
- `<stem>_<method>_cube.vesta`
- `<stem>_<method>_cube_vesta_recipe.md`
- `multiwfn_<method>_recipe.md`

The VESTA surface uses `avgdg_inter.cub` as the surface cube and
`avgsl2r.cub` as the texture cube through `cube-preset aigm`.  TFI coloring
uses `cube-preset aigm-tfi`.

## Notes

- Frame indices start from 1.  Omit `--frame-range` to send an empty response
  and let Multiwfn process all frames.
- Fragments are passed directly to Multiwfn.  Use the same syntax as the
  interactive prompt, such as `1-48`, `1,4,9`, or complement `c`.
- For periodic trajectories, use `--periodic --grid-mode spacing
  --grid-spacing VALUE` or `--grid-mode pbc-cell`.  The runner lightly detects
  `Lattice=`, `pbc=`, and `CRYST1` markers and rejects `--grid-mode points`
  for periodic input because Multiwfn's PBC option `4` reads a spacing value.
- `--export-tfi` uses the visible Multiwfn post-processing option `5`
  `thermflu.cub` route.  It does not drive the hidden option `6` branch that
  writes `TFI-aIGM.cub` or `TFI-amIGM.cub`.
- The runner starts Multiwfn only; it does not launch VESTA.
- If Multiwfn exits 0 but does not write `avgdg_inter.cub` and
  `avgsl2r.cub`, the CLI returns a nonzero code and keeps stdout/stderr logs.
