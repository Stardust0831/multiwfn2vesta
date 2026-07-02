# Skill: ABACUS ESP on vdW density surface in VESTA

Use this when ABACUS direct cubes should be rendered as an electrostatic
potential map on a `rho=0.001` electron-density surface.

## Inputs

- ABACUS density cube from `out_chg`, for example `SPIN1_CHG.cube`.
- ABACUS electrostatic-potential cube from `out_pot`, for example
  `ElecStaticPot.cube`.
- Prefer a validated LCAO/GPU, CPU, or single-rank GPU output.  Do not use
  known-risk PW/GPU multi-rank direct cubes unless a density-integral check
  passes.

## Sanity checks

1. Read cube grid and cell with `cube_units=bohr` unless the cube count
   convention explicitly says Angstrom.
2. Integrate density over the raw Bohr voxel volume.  The result should match
   the expected valence-electron count.
3. Inspect the planar-average ESP along the slab normal.  For a monolayer/slab,
   the low/high vacuum plateaus should be flat and similar.

The COF reference case:

```text
smoke/cof_esp_vdw_surface_20260625/
density integral = 233.99939580839157 e, expected 234 e
high-z vacuum window = planes 162:180
ESP offset = 3.513736488613E-02
```

## Vacuum-align ESP

```bash
PYTHONPATH=project/src python3 -m multiwfn2vesta.abacus_esp_align \
  ElecStaticPot.cube ElecStaticPot_vacuum0.cube \
  --axis z \
  --vacuum-side high \
  --vacuum-fraction 0.1 \
  --profile-csv ElecStaticPot_profile_z.csv \
  --report-md ElecStaticPot_alignment.md
```

Use an explicit `--vacuum-start` / `--vacuum-end` when the automatic high/low
window is not truly vacuum.

## Build VESTA scene

```bash
PYTHONPATH=project/src python3 -m multiwfn2vesta.cube_vesta \
  SPIN1_CHG.cube esp_vdw_surface \
  --texture-cube ElecStaticPot_vacuum0.cube \
  --stem system_esp_vdw_surface \
  --title "ESP on rho=0.001 density surface" \
  --isosurface 0.001 \
  --surface-mode single \
  --tex-physical -0.08 0.08 \
  --tex-range-source surface-band \
  --surface-band 0.005 \
  --cube-units bohr \
  --structure crystal \
  --boundary -0.05 1.05 -0.05 1.05 -0.05 1.05 \
  --sections off
```

For the COF case, the user-adjusted VESTA color scale was reversed and set to
`-0.08..0.08 a.u.`.  The saved VESTA `TEX3P` percentages can be back-converted
with:

```bash
python3 project/scripts/vesta_tex3p_scale.py input.vesta --known-physical -0.08 0.08
```

In the COF case:

```text
TEX3P = -1  2.09774E-02  1.04690E+00
inferred reference = -0.0832715762378 .. 0.0726856080566
```

## Bonds

`BONDS 1` is only the display switch; visible structure bonds also require
non-empty `SBOND` search rules.  Current `cube-vesta` / `cube-preset` exports
write default `SBOND` rules automatically from a static 1-118 element covalent
radius table.  For unusual coordination, trajectory frames, or deliberately
loose metal-ligand contacts, add explicit rules such as
`--bond Cd Cl 0 3.5`.

Use a derived render file instead of overwriting a manually tuned `.vesta`.

## Export PNG

For large density+texture cube scenes, a single immediate `-export_img` may
export a `40 x 40` or `60 x 60` icon-like PNG.  Insert multiple `-flush`
commands after `-open`:

```text
VESTA.exe -open input.vesta -flush -flush -flush \
  -export_img scale=4 output.png -flush -close
```

Windows VESTA may return code `255` even after writing a valid image.  Treat
the PNG dimensions and file size as the primary export check.

Reference final render:

```text
smoke/cof_esp_vdw_surface_20260625/products/cof12000n2_esp_vdw_surface_vesta_zoom_bonds.png
```
