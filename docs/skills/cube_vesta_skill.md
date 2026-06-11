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
multiwfn2vesta cube-preset spin-polarization spindensity.cub cube_products
multiwfn2vesta cube-preset laplacian laplacian.cub cube_products
multiwfn2vesta cube-preset hamiltonian-ked 'K(r).cub' cube_products
multiwfn2vesta cube-preset lagrangian-ked 'G(r).cub' cube_products
multiwfn2vesta cube-preset kinetic-energy-density userfunc.cub cube_products
multiwfn2vesta cube-preset local-information-entropy infoentro.cub cube_products
multiwfn2vesta cube-preset electron-delocalization-range EDR.cub cube_products
multiwfn2vesta cube-preset orbital-overlap-distance EDRDmax.cub cube_products
multiwfn2vesta cube-preset pair-function fermihole.cub cube_products
multiwfn2vesta cube-preset source-function srcfunc.cub cube_products
multiwfn2vesta cube-preset user-function userfunc.cub cube_products
multiwfn2vesta cube-preset becke-weight Becke.cub cube_products
multiwfn2vesta cube-preset hirshfeld-weight Hirshfeld.cub cube_products
multiwfn2vesta cube-preset rdg-scalar RDG.cub cube_products
multiwfn2vesta cube-preset promolecular-rdg RDGprodens.cub cube_products
multiwfn2vesta cube-preset promolecular-delta-g Delta_g.cub cube_products
multiwfn2vesta cube-preset hirshfeld-delta-g griddata.cub cube_products
multiwfn2vesta cube-preset iri-scalar IRI.cub cube_products
multiwfn2vesta cube-preset dori-scalar userfunc.cub cube_products
multiwfn2vesta cube-preset vdw-potential vdWpot.cub cube_products
multiwfn2vesta cube-preset potential pot_es.cube cube_products
multiwfn2vesta cube-preset partial-charge pchg.cube cube_products
multiwfn2vesta cube-preset wavefunction-norm wfc_norm.cube cube_products
multiwfn2vesta cube-preset elf ELF.cub cube_products
multiwfn2vesta cube-preset rdg IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub
multiwfn2vesta cube-preset dori DORI.cub cube_products \
  --texture-cube sl2r.cub
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
If Multiwfn function `100` already exported alpha or beta density
`userfunc.cub` (`iuserfunc=1/2`), display it with `cube-preset density` or
regenerate it through `grid-run --function alpha-density` /
`grid-run --function beta-density`.
If function `100` exported FOD `userfunc.cub` (`iuserfunc=90`), display it
with `cube-preset density` or regenerate it through
`grid-run --function fractional-occupation-density`.  The density preset
default `0.01` isosurface may hide weak FOD fields; try `--isosurface 0.001`
or tune the value per system.
If Multiwfn function `100` already exported orbital-weighted Fukui
`userfunc.cub` (`iuserfunc=95/96/97`), display it with `cube-preset density`
or regenerate it through `grid-run --function orbital-weighted-fukui-*`.
For orbital-weighted dual descriptor (`iuserfunc=98`), use
`cube-preset signed` for standalone positive/negative surfaces or
`cube-preset surface-map` when it should color a density/surface cube.

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
  `--surface-band` to set the non-negative half-width manually; otherwise a
  conservative automatic band is used.  If the band has no non-degenerate
  texture range, `--surface-nearest` nearest grid points are used as a
  fallback and must be positive.

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
- `spin-polarization` aliases: `spin-polarization-parameter`, `spin-pol`,
  `spin-polarisation`; positive/negative surfaces for Multiwfn function `5`
  `spindensity.cub` generated with `ipolarpara=1`, default magnitude `0.5`.
- `laplacian` aliases: `lap`, `laplacian-rho`; positive/negative surfaces
  for Multiwfn `laplacian.cub`, default magnitude `0.05`; tune per system.
- `hamiltonian-ked` aliases: `k-r`, `k(r)`, `kinetic-k`; positive/negative
  surfaces for Multiwfn `K(r).cub`, default magnitude `0.01`.
- `lagrangian-ked` aliases: `g-r`, `g(r)`, `kinetic-g`; single positive
  surface for Multiwfn `G(r).cub`, default isosurface `0.01`.
- `kinetic-energy-density` aliases: `positive-ked`, `ked`,
  `thomas-fermi-ked`, `tf-ked`, `weizsacker-ked`, `vw-ked`, `pauli-ked`;
  single positive surface for selected function-100 KED variants exported as
  `userfunc.cub`, default isosurface `0.01`.  Use this for
  `grid-run --function thomas-fermi-ked`, `weizsacker-ked`, or `pauli-ked`;
  inspect the value range and tune the isosurface per system.
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
- `pair-function` aliases: `fermihole`, `fermi-hole`, `correlation-hole`,
  `corr-hole`, `correlation-factor`, `corr-factor`,
  `exchange-correlation-density`, `xc-density`, `pair-density`;
  positive/negative surfaces for Multiwfn function `17` `fermihole.cub`,
  default magnitude `0.05`.  When generating the cube with `grid-run`, pass
  `--reference-point X Y Z`; `--reference-unit angstrom` is available for
  Angstrom input coordinates.  `--pair-function-type` patches Multiwfn
  `pairfunctype`, `--pair-correlation-type` patches `paircorrtype`, and both
  settings are written to a run-local settings file copied from the selected
  Multiwfn `settings.ini` when available and passed with `-set`.
- `source-function` aliases: `source`, `srcfunc`, `source-func`;
  positive/negative surfaces for Multiwfn function `19` `srcfunc.cub`,
  default magnitude `0.05`.  When generating the cube with `grid-run`, pass
  `--reference-point X Y Z`; `--reference-unit angstrom` is available for
  Angstrom input coordinates, and `--source-function-mode` is patched into a
  run-local settings file copied from the selected Multiwfn `settings.ini`
  when available and passed with `-set`.
- `user-function` aliases: `userfunc`, `user-defined-function`,
  `custom-function`, `lea-function`, `leae-function`,
  `information-gain-density`, `relative-shannon-entropy`,
  `shannon-entropy-density`, `fisher-information-density`;
  positive/negative surfaces for Multiwfn function `100` `userfunc.cub`,
  default magnitude `0.05`.  When generating the cube with `grid-run`, the
  generic `--function user-function` route still requires
  `--user-function-index IUSERFUNC`, while named routes automatically patch
  common values: `alpha-density` / `beta-density` = `1` / `2`,
  `electron-esp` / `electronic-esp` = `14`,
  `dori` / `density-overlap-regions-indicator` = `20`,
  `local-electron-affinity` / `lea` = `27`,
  `local-electron-attachment-energy` / `leae` = `-27`,
  `local-mulliken-electronegativity` / `local-electronegativity` = `28`,
  `local-hardness` / `local-chemical-hardness` = `29`,
  `information-gain-density` = `49`, `shannon-entropy-density` = `50`,
  `fisher-information-density` / `second-fisher-information-density` =
  `51` / `52`, `fractional-occupation-density` / `fod` = `90`,
  `vdw-repulsion-potential` / `vdw-dispersion-potential` = `93` / `94`,
  ESP components = `101` / `102` / `103`, orbital-weighted Fukui/dual =
  `95` / `96` / `97` / `98`, and selected KED routes = `1200` or `114`
  plus run-local `iKEDsel`.  For LEA/LEAE density-surface maps, use
  `grid-run --function local-electron-affinity --surface-cube density.cub`
  or the lower-level `lea`/`leae` texture presets with `density.cub` plus
  `userfunc.cub`.  For local electronegativity/local hardness maps, use
  `grid-run --surface-cube` with `surface-map` and pass `--tex-physical`,
  `--tex-percent`, `--tex-range-source surface-band`, `--surface-band`, or
  `--surface-nearest` directly through `grid-run` when the generic color
  scale needs tuning.
- `electron-esp` aliases: `electronic-esp`, `electron-mep`,
  `electronic-mep`, `electron-electrostatic-potential`; single negative
  surface for Multiwfn function-100 `userfunc.cub` with `iuserfunc=14`,
  default isosurface `-0.05`.  Multiwfn evaluates `eleesp(x,y,z)`, the
  electron contribution to ESP; for mapped density/surface figures, generate
  it with `grid-run --function electron-esp --surface-cube density.cub`.
- `becke-weight` aliases: `becke`, `becke-overlap-weight`,
  `becke-atomic-weight`, `beckewei`; single positive surface for Multiwfn
  function `111` `Becke.cub`, default isosurface `0.5`.  When generating the
  cube with `grid-run`, pass `--becke-atoms I J`; `I J` requests Becke
  overlap weight and `I 0` requests Becke atomic weight.
- `hirshfeld-weight` aliases: `hirshfeld`, `hirshfeld-atomic-weight`,
  `hirshfeldwei`; single positive surface for Multiwfn function `112`
  `Hirshfeld.cub`, default isosurface `0.5`.  When generating the cube with
  `grid-run`, pass `--hirshfeld-atoms ATOMS`, for example `2,3,7-10`.  The
  maintained stream selects built-in atomic densities; the separate atomic
  `.wfn` density-source mode is not automated yet.
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
- `hirshfeld-delta-g` aliases: `delta-g-hirshfeld`,
  `deltag-hirshfeld`, `delta_g_hirshfeld`, `igmh-scalar`; single positive
  surface for Multiwfn function `23` Delta-g with Hirshfeld partition,
  default isosurface `0.05`.  Multiwfn 2026.6.2 exports this route as the
  generic `griddata.cub`; `grid-run` renames the processed product to a
  stable `<stem>_hirshfeld-delta-g.cub`.  Keep this standalone full-system
  scalar separate from IGM/IGMH fragment `dg_inter.cub` mapped-surface
  routes.
- `iri-scalar` aliases: `iri-cube`, `standalone-iri`,
  `interaction-region-indicator`; single positive surface for standalone
  Multiwfn `IRI.cub`, default isosurface `1.0`.  Use `iri` with
  `--texture-cube` for IRI/RDG/NCI surfaces colored by sign(lambda2)rho.
- `dori-scalar` aliases: `standalone-dori`, `dori-cube`; single positive
  surface for Multiwfn function-100 `userfunc.cub` with `iuserfunc=20`,
  default isosurface `0.95`.  Use `dori` with `--texture-cube` for DORI
  surfaces colored by sign(lambda2)rho.
- `vdw-potential` aliases: `vdw`, `vdwpot`, `vdw-potential-cube`,
  `van-der-waals-potential`; positive/negative surfaces for standalone
  Multiwfn function `25` `vdWpot.cub`, default magnitude `1.0` kcal/mol.
  Multiwfn evaluates this UFF vdW potential and sets main-function-5
  `sur_value=1.0`.  `grid-run` defaults the UFF probe to carbon/6 with
  run-local `ivdwprobe` and accepts `--vdw-probe` for other probe atoms.  Use
  `vdw-map` instead when the vdW potential cube should color a density/surface
  cube.
- `vdw-repulsion-potential` aliases: `vdw-repulsion`,
  `repulsion-potential`, `repul`, `repul-potential`; single positive surface
  for standalone UFF vdW repulsion potential cubes.  Use for Multiwfn
  function-100 `userfunc.cub` with `iuserfunc=93`, or `repul.cub` from the
  vdW potential module.  Default isosurface is `+1.0` kcal/mol.
- `vdw-dispersion-potential` aliases: `vdw-dispersion`,
  `dispersion-potential`, `disp`, `disp-potential`; single negative surface
  for standalone UFF vdW dispersion potential cubes.  Use for Multiwfn
  function-100 `userfunc.cub` with `iuserfunc=94`, or `disp.cub` from the
  vdW potential module.  Default isosurface is `-1.0` kcal/mol because the
  attractive dispersion component is normally negative.  This is still a
  single-surface preset, so standalone color overrides use `--positive-rgb`.
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
  For Multiwfn-generated ELF, `grid-run` defaults function `9` to
  `ELFLOL_type=0` and accepts `--elflol-type` for Tsirelson/Tian-Lu
  variants, plus ELF-only D/D0.
- `lol`; single surface, default isosurface `0.50`.  Multiwfn LOL uses the
  same run-local `ELFLOL_type` control as ELF when generated through
  `grid-run`.
- `iri` aliases: `rdg`, `nci`, `weak-interaction`; requires
  `--texture-cube`, defaults to `--isosurface 1.0`,
  `--tex-physical -0.04 0.04`, and surface-band texture scaling.
- `dori` aliases: `dori-map`, `dori-fill`,
  `density-overlap-regions-indicator`; requires `--texture-cube`, defaults
  to `--isosurface 0.95`, `--tex-physical -0.04 0.02`, and surface-band
  texture scaling.  DORI is the surface cube and sign(lambda2)rho is the
  texture cube, matching Multiwfn `DORIfill.vmd`.
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
  user-function, and related scalar cubes.  IRI/RDG mapped surfaces with two
  coupled cubes have a separate maintained runner as `multiwfn2vesta
  iri-run`; this cube workflow remains the lower-level VESTA writer both
  runners call.
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
