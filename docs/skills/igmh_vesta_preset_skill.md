# Skill: IGM/IGMH/aIGM cube presets for VESTA

Use this when Multiwfn has already generated IGM, IGMH, or aIGM cube files
and the task is to make a VESTA mapped-surface file without manually choosing
the display defaults.

## Inputs

The preset layer does not run the Multiwfn fragment menus yet.  It expects
compatible cube pairs already produced by Multiwfn:

- `igmh` / `igm-inter`: surface `dg_inter.cub`, texture `sl2r.cub`.
- `igm-intra`: surface `dg_intra.cub`, texture `sl2r.cub`.
- `aigm`: surface `avgdg_inter.cub`, texture `avgsl2r.cub`.
- `aigm-tfi`: surface `avgdg_inter.cub`, texture `thermflu.cub`.

For ABACUS workflows, first produce a Multiwfn-readable Molden file with
`multiwfn2vesta abacus-molden`, then run the relevant Multiwfn IGMH/aIGM menu
manually or through a future command-stream wrapper.

## Commands

```bash
multiwfn2vesta cube-preset igmh dg_inter.cub products \
  --texture-cube sl2r.cub

multiwfn2vesta cube-preset igm-intra dg_intra.cub products \
  --texture-cube sl2r.cub

multiwfn2vesta cube-preset aigm avgdg_inter.cub products \
  --texture-cube avgsl2r.cub

multiwfn2vesta cube-preset aigm-tfi avgdg_inter.cub products \
  --texture-cube thermflu.cub
```

The output `.vesta` imports the surface cube through `IMPORT_DENSITY`, imports
the color cube through `IMPORT_TEXTURE`, disables sections by default, and
writes a recipe containing the canonical preset, effective isosurface, and
texture scaling source.

## Defaults

Defaults are copied from the bundled Multiwfn VMD templates:

| Preset | Template | Isosurface | Texture physical range |
| --- | --- | ---: | --- |
| `igmh` / `igm-inter` | `IGM_inter.vmd` | `0.01` | `-0.05` to `0.05` |
| `igm-intra` | `IGM_intra.vmd` | `0.2` | `-0.05` to `0.05` |
| `aigm` | `aIGM.vmd` | `0.008` | `-0.05` to `0.05` |
| `aigm-tfi` | `aIGM_TFI.vmd` | `0.008` | `0.0` to `1.5` |

These presets use `full-cube` texture range conversion.  This matches the VMD
`scaleminmax` intent: the requested physical values are converted to VESTA
`TEX3P` percentage values using the texture cube's data range.

## Verified Smoke

The Ag(111)+benzene periodic-cell IGMH cubes were smoke-tested without
launching VESTA:

```text
/mnt/g/work/multiwfn2vesta/smoke/igmh_preset_20260610_1128/products/
```

The smoke generated `dg_inter_igmh_cube.vesta` and
`dg_inter_igmh_cube_vesta_recipe.md` from `dg_inter.cub` plus `sl2r.cub`.

## Limitations

- Fragment selection and Multiwfn IGMH command-stream automation are still a
  later increment.
- AIM path/BCP overlays are handled by `multiwfn2vesta aim-igmh` after VESTA
  has a saved multi-phase overlay.
- For publication images, inspect the generated VESTA file and adjust
  `--isosurface`, `--tex-physical`, `--boundary`, or camera settings if the
  system-specific range needs tuning.
