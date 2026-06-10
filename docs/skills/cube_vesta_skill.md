# Skill: Cube to VESTA workflow

Use this when an ABACUS or Multiwfn scalar cube should become a VESTA
isosurface file without opening VESTA interactively.

## Command

Single cube:

```bash
multiwfn2vesta cube-vesta density.cub cube_products --isosurface 0.01
```

Signed positive/negative cube:

```bash
multiwfn2vesta cube-vesta orbital.cub cube_products \
  --surface-mode signed \
  --isosurface 0.02
```

Surface cube plus texture/color cube:

```bash
multiwfn2vesta cube-vesta surface.cub cube_products \
  --texture-cube texture.cub \
  --isosurface 0.01 \
  --tex-physical -0.05 0.05
```

Surface-sampled texture scaling:

```bash
multiwfn2vesta cube-vesta surface.cub cube_products \
  --texture-cube texture.cub \
  --isosurface 0.01 \
  --tex-physical -0.05 0.05 \
  --tex-range-source surface-band
```

Analysis preset wrapper:

```bash
multiwfn2vesta cube-preset --list-presets
multiwfn2vesta cube-preset orbital orbital.cub cube_products
multiwfn2vesta cube-preset orbital-density orbdens.cub cube_products
multiwfn2vesta cube-preset gradient-norm gradient.cub cube_products
multiwfn2vesta cube-preset spin-density spindensity.cub cube_products
multiwfn2vesta cube-preset laplacian laplacian.cub cube_products
multiwfn2vesta cube-preset hamiltonian-ked 'K(r).cub' cube_products
multiwfn2vesta cube-preset lagrangian-ked 'G(r).cub' cube_products
multiwfn2vesta cube-preset local-information-entropy infoentro.cub cube_products
multiwfn2vesta cube-preset electron-delocalization-range EDR.cub cube_products
multiwfn2vesta cube-preset orbital-overlap-distance EDRDmax.cub cube_products
multiwfn2vesta cube-preset becke-weight Becke.cub cube_products
multiwfn2vesta cube-preset rdg-scalar RDG.cub cube_products
multiwfn2vesta cube-preset promolecular-rdg RDGprodens.cub cube_products
multiwfn2vesta cube-preset promolecular-delta-g Delta_g.cub cube_products
multiwfn2vesta cube-preset iri-scalar IRI.cub cube_products
multiwfn2vesta cube-preset vdw-potential vdWpot.cub cube_products
multiwfn2vesta cube-preset potential pot_es.cube cube_products
multiwfn2vesta cube-preset partial-charge pchg.cube cube_products
multiwfn2vesta cube-preset wavefunction-norm wfc_norm.cube cube_products
multiwfn2vesta cube-preset elf ELF.cub cube_products
multiwfn2vesta cube-preset rdg IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub
multiwfn2vesta cube-preset igmh dg_inter.cub cube_products \
  --texture-cube sl2r.cub
multiwfn2vesta cube-preset esp density.cub cube_products \
  --texture-cube esp.cub \
  --tex-physical -0.05 0.05
multiwfn2vesta cube-preset alie density.cub cube_products \
  --texture-cube avglocion.cub \
  --surfanalysis-pdb surfanalysis.pdb
multiwfn2vesta cube-preset vdw-surface density.cub cube_products \
  --texture-cube vdW.cub
```

`cube-preset` is a thin layer over `cube-vesta`; it selects maintained
defaults but does not duplicate VESTA-writing logic.

IGM/IGMH/aIGM presets are available when Multiwfn has already produced the
compatible cube pair:

- `igmh` / `igm-inter`: `dg_inter.cub` surface plus `sl2r.cub` texture,
  isosurface `0.01`, texture physical range `-0.05` to `0.05`.
- `igm-intra`: `dg_intra.cub` surface plus `sl2r.cub` texture, isosurface
  `0.2`, texture physical range `-0.05` to `0.05`.
- `aigm`: `avgdg_inter.cub` surface plus `avgsl2r.cub` texture, isosurface
  `0.008`, texture physical range `-0.05` to `0.05`.
- `aigm-tfi`: `avgdg_inter.cub` surface plus `thermflu.cub` texture,
  isosurface `0.008`, texture physical range `0.0` to `1.5`.

These defaults come from the bundled Multiwfn VMD templates
`IGM_inter.vmd`, `IGM_intra.vmd`, `aIGM.vmd`, and `aIGM_TFI.vmd`.

Surface extrema overlay:

```bash
multiwfn2vesta surface-extrema input.vesta surfanalysis.pdb output.vesta \
  --surface-cube density.cub \
  --selection all
```

Use `cube-preset --surfanalysis-pdb` when the extrema should be embedded as
part of the preset run.  Use `surface-extrema` when patching an existing
VESTA file.

Cube arithmetic wrapper:

```bash
multiwfn2vesta cube-arith cube_arith_products \
  --term 1.0 rho_a.cub \
  --term -1.0 rho_b.cub \
  --stem density_difference

multiwfn2vesta cube-arith cube_arith_products \
  --operation spin-density \
  --plus-cube alpha_density.cub \
  --minus-cube beta_density.cub \
  --stem spin_density

multiwfn2vesta cube-arith cube_arith_products \
  --operation dual-descriptor \
  --anion-cube density_Nplus1.cub \
  --neutral-cube density_N.cub \
  --cation-cube density_Nminus1.cub
```

`cube-arith` writes a new cube from compatible input cubes and, unless
`--no-vesta` is used, sends that cube through `cube-preset` for display.  It
is the maintained bottom layer for density-difference, alpha-minus-beta spin
density, Fukui, and dual-descriptor maps.  If Multiwfn already exported
`spindensity.cub`, use `cube-preset spin-density` directly.

If starting from a Multiwfn-readable wavefunction instead of an existing cube,
use `grid-run` for single real-space function cubes:

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function density \
  --grid-points 80 80 80
```

`grid-run` calls Multiwfn main function `5`, exports the cube, then optionally
passes it back through `cube-preset`.

## Outputs

- `<output_dir>/<stem>_cube.vesta`
- `<output_dir>/<stem>_cube_vesta_recipe.md`
- for `cube-preset`, the same recipe gains a `Cube Preset` block recording
  requested/canonical preset names and effective defaults
- if `--surfanalysis-pdb` is used, the recipe gains a `Surface Extrema
  Overlay` block recording extrema counts, selection, radius, colors, and the
  Multiwfn C/O source convention
- copied cube dependencies unless `--no-copy-cubes` is used
- if surface and texture cubes share a basename but come from different
  directories, the later dependency is renamed, for example
  `foo.cub` plus `foo_texture.cub`, so VESTA imports do not point at an
  overwritten file

## VESTA Template Rules

- Surface cube goes in `IMPORT_DENSITY 1`.
- Texture/color cube goes in `IMPORT_TEXTURE`.
- Default sections are off: `SECTS 0 0`.
- `ISURF` stores the requested isosurface level.
- `--surface-mode single` writes one `ISURF` entry.
- `--surface-mode signed` treats `--isosurface X` as a magnitude and writes
  both `+abs(X)` and `-abs(X)`.  The default colors are yellow for positive
  values and blue for negative values.  Use `--positive-rgb`,
  `--negative-rgb`, and `--surface-opacity` to override the VESTA surface
  style.
- `TEX3P` stores VESTA percentage/normalized values, not physical scalar
  limits.
- `--tex-physical MIN MAX` converts physical limits to percentages using the
  selected texture reference range.
- `--tex-range-source full-cube` uses the full texture cube min/max.
- `--tex-range-source surface-band` uses texture values from grid points whose
  surface-cube values are close to the requested `--isosurface`.  Use
  `--surface-band` to set the half-width manually; otherwise a conservative
  automatic band is used.  If the band has no non-degenerate texture range,
  `--surface-nearest` nearest grid points are used as a fallback.

## Cube and Structure Rules

- Cube data counts are strict by default; malformed cube files should fail
  rather than generate misleading figures.
- Texture cube grid origin, vectors, and counts must match the surface cube by
  default.
- `--cube-units auto` treats ordinary positive cube grid counts as Bohr and
  negative grid counts as Angstrom.  Override with `--cube-units bohr` or
  `--cube-units angstrom` when needed.
- `--structure auto` creates a `CRYSTAL` structure phase when the cube origin
  is zero and atoms fall inside the cube cell.  Otherwise it creates a
  `MOLECULE` phase with coordinates shifted by the cube origin.

## Analysis Presets

- `density` aliases: `rho`, `charge-density`, `scalar`; single surface,
  default isosurface `0.01`.
- `gradient-norm` aliases: `gradient`, `rho-gradient`, `grad-rho`; single
  positive surface for Multiwfn `gradient.cub`, default isosurface `0.05`.
  Multiwfn leaves this at the global main-function-5 `sur_value`, so tune per
  system.
- `signed` aliases: `orbital`, `mo`, `wavefunction`, `abacus-wfc`,
  `density-difference`, `dual-descriptor`; positive/negative surfaces,
  default magnitude `0.02`.
- `orbital-density` aliases: `orbdens`, `mo-density`; single positive
  surface for Multiwfn `orbdens.cub`, default isosurface `0.005`.
- `spin-density` aliases: `spin`, `spindensity`, `magnetization-density`;
  positive/negative surfaces for Multiwfn `spindensity.cub`, default
  magnitude `0.02`.
- `laplacian` aliases: `lap`, `laplacian-rho`; positive/negative surfaces
  for Multiwfn `laplacian.cub`, default magnitude `0.05`; tune per system.
- `hamiltonian-ked` aliases: `k-r`, `k(r)`, `kinetic-k`; positive/negative
  surfaces for Multiwfn `K(r).cub`, default magnitude `0.01`.
- `lagrangian-ked` aliases: `g-r`, `g(r)`, `kinetic-g`; single positive
  surface for Multiwfn `G(r).cub`, default isosurface `0.01`.
- `local-information-entropy` aliases: `information-entropy`, `infoentro`,
  `local-info-entropy`, `local-shannon-entropy`; positive/negative surfaces
  for Multiwfn `infoentro.cub`, default magnitude `0.05`.  Multiwfn function
  `11` evaluates local information entropy as `-rho/N*ln(rho/N)` and keeps
  the global main-function-5 `sur_value`.
- `electron-delocalization-range` aliases: `edr`, `edr-r-d`,
  `electron-delocalization-range-function`; single positive surface for
  Multiwfn function `20` `EDR.cub`, default isosurface `0.05`.  When
  generating the cube with `grid-run`, pass `--edr-length D_BOHR`.
- `orbital-overlap-distance` aliases: `orbital-overlap-length`, `edrdmax`,
  `edr-dmax`, `d-r`, `d(r)`; single positive surface for Multiwfn function
  `21` `EDRDmax.cub`, default isosurface `0.05`.  `grid-run` uses
  Multiwfn's default exponent set unless `--edr-exponents COUNT START
  INCREMENT` is supplied.
- `becke-weight` aliases: `becke`, `becke-overlap-weight`,
  `becke-atomic-weight`, `beckewei`; single positive surface for Multiwfn
  function `111` `Becke.cub`, default isosurface `0.5`.  When generating the
  cube with `grid-run`, pass `--becke-atoms I J`; `I J` requests Becke
  overlap weight and `I 0` requests Becke atomic weight.
- `rdg-scalar` aliases: `rdg-cube`, `scalar-rdg`,
  `reduced-density-gradient`; single positive surface for standalone Multiwfn
  `RDG.cub`, default isosurface `0.5`.  Use `iri` with `--texture-cube` for
  RDG/NCI surfaces colored by sign(lambda2)rho.
- `promolecular-rdg` aliases: `rdg-pro`, `prodens-rdg`,
  `promolecular-rdg-scalar`; single positive surface for Multiwfn
  `RDGprodens.cub`, default isosurface `0.4`.
- `promolecular-delta-g` aliases: `delta-g`, `deltag`, `delta_g`,
  `promolecular-deltag`, `delta-g-promol`; single positive surface for
  Multiwfn function `22` `Delta_g.cub`, default isosurface `0.05`.
  This is the standalone promolecular Delta-g cube; do not use it for
  IGM/IGMH fragment `dg_inter.cub`, which remains a texture route via
  `cube-preset igmh`/`igm`.
- `iri-scalar` aliases: `iri-cube`, `standalone-iri`,
  `interaction-region-indicator`; single positive surface for standalone
  Multiwfn `IRI.cub`, default isosurface `1.0`.  Use `iri` with
  `--texture-cube` for IRI/RDG/NCI surfaces colored by sign(lambda2)rho.
- `vdw-potential` aliases: `vdw`, `vdwpot`, `vdw-potential-cube`,
  `van-der-waals-potential`; positive/negative surfaces for standalone
  Multiwfn function `25` `vdWpot.cub`, default magnitude `1.0` kcal/mol.
  Multiwfn evaluates this UFF vdW potential and sets main-function-5
  `sur_value=1.0`.  Use `vdw-map` instead when the vdW potential cube should
  color a density/surface cube.
- `potential` aliases: `abacus-potential`, `out-pot`, `local-potential`,
  `pot-es`; signed direct potential cube isosurfaces, default magnitude
  `0.05`.  Use `esp` instead for density-surface potential coloring.
- `partial-charge` aliases: `pchg`, `abacus-pchg`, `out-pchg`,
  `band-density`, `state-density`; single positive surface for ABACUS
  `get_pchg`/`out_pchg` cubes, default isosurface `0.001`.
- `wavefunction-norm` aliases: `wfc-norm`, `abacus-wfc-norm`,
  `out-wfc-norm`, `wavefunction-magnitude`; single positive surface for
  nonnegative ABACUS `out_wfc_norm` cubes, default isosurface `0.001`.
  Use `signed`/`orbital` for real/imaginary `out_wfc_re_im` cubes.
- `elf` alias: `abacus-elf`; single surface, default isosurface `0.80`.
- `lol`; single surface, default isosurface `0.50`.
- `iri` aliases: `rdg`, `nci`, `weak-interaction`; requires
  `--texture-cube`, defaults to `--isosurface 1.0`,
  `--tex-physical -0.04 0.04`, and surface-band texture scaling.
- `esp` aliases: `mep`, `electrostatic-potential`, `density-esp`; requires
  `--texture-cube`, defaults to density isosurface `0.001`; pass
  `--tex-physical` for comparable figures.
- `surface-map` aliases: `molsurfmap`, `mapped-surface`,
  `density-surface-map`; requires `--texture-cube` and uses a generic
  density/surface cube plus mapped-property cube.  Defaults follow the
  bundled `molsurfmap.vmd` template: isosurface `0.01` and texture range
  `0.0 0.002`.
- `alie` aliases: `average-local-ionization-energy`, `avglocion`; requires
  `--texture-cube`, defaults to density isosurface `0.0005` and physical
  texture range `0.32 0.36` a.u. for `density.cub + avglocion.cub`.
- `lea` and `leae`; require `--texture-cube`, use `density.cub +
  userfunc.cub`, and default to density isosurfaces `0.01` and `0.004`,
  respectively.
- `vdw-map` aliases: `vdw-surface`, `vdw-density-surface`,
  `vdw-potential-map`; requires `--texture-cube`, defaults to density
  isosurface `0.0001` and physical texture range `-0.3 0.3` kcal/mol for
  `density.cub + vdW.cub`/`vdWpot.cub`.

## Current Limits

- No VESTA rendering is launched by this command.
- Analysis-specific display presets now exist for common cube products.
  Cube arithmetic now exists as `multiwfn2vesta cube-arith` for compatible
  cube linear combinations such as density difference, alpha-minus-beta spin
  density, Fukui functions, and dual descriptors.
  Multiwfn main-function-5 single-cube generation now exists as
  `multiwfn2vesta grid-run` for density, orbital/MO, Laplacian, K(r)/G(r),
  ELF, LOL, ESP/MEP, ALIE, RDG/IRI-like, promolecular RDG/sign(lambda2)rho,
  and related scalar cubes.  IRI/RDG mapped surfaces with two coupled cubes
  have a separate maintained runner as `multiwfn2vesta iri-run`; this cube
  workflow remains the lower-level VESTA writer both runners call.
- Surface-band sampling uses grid-point values, not interpolation exactly on
  the triangulated VESTA isosurface.
- AIM/BCP pseudo-site overlays remain in the AIM/AIM+IGMH workflows, not this
  generic cube generator.  Multiwfn `surfanalysis.pdb` extrema overlays for
  ALIE/LEA/LEAE/molecular-surface maps are a separate future layer.

## Validation

```bash
PYTHONPATH=src python3 -m unittest tests.test_cube_preset tests.test_cube_vesta -v
```

Real smoke:

```text
/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_cli_smoke_20260610/
/mnt/g/work/multiwfn2vesta/smoke/cube_preset_smoke_20260610/
/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_density/
```
