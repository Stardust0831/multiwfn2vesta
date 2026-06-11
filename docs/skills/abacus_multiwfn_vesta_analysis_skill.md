# Skill: ABACUS to Multiwfn to VESTA Analysis Planning

Use this when deciding whether a Multiwfn analysis should become a maintained
VESTA workflow for ABACUS-generated data.

## Decision Order

1. Prefer ABACUS direct cube output when the target is simply density,
   potential, ELF, partial charge, or real-space wavefunction visualization.
2. Use ABACUS Molden only when Multiwfn needs a full wavefunction, for example
   AIM, IGMH, IRI/RDG from actual density, STM/LDOS, orbital cubes, ELF/LOL,
   ALIE, or density derivatives.
3. For ABACUS Molden, use the latest
   `interfaces/Multiwfn_interface/molden.py` from `abacus-develop`, not the old
   `tools/molden/molden.py` path.
4. Reject or warn on non-Gamma/multi-k, `nspin=4`, SOC spinors, missing
   `[Nval]`, or missing `[Cell]` when the workflow claims to be periodic.
5. Choose the VESTA representation:
   - one cube: isosurface or section;
   - signed cube: positive/negative isosurfaces;
   - two compatible cubes: density/surface cube plus texture cube;
   - PDB/topology: pseudo-sites with controlled `SITET` and disabled unwanted
     AIM bonds;
   - atom values: patch `SITET` RGB from a scalar table.

## ABACUS Checklist

For direct cube products:

```text
out_chg 1       # charge density cube
out_pot 1       # local potential cube
out_pot 2       # electrostatic potential cube
out_elf 1       # ELF cube
calculation get_pchg + out_pchg ...       # partial charge cubes
calculation get_wf + out_wfc_norm ...      # wavefunction norm cubes
calculation get_wf + out_wfc_re_im ...     # real/imaginary wavefunction cubes
```

Prepare these cubes for VESTA with the maintained no-GUI generator:

```bash
multiwfn2vesta cube-vesta density.cub cube_products --isosurface 0.01
```

For common products, use the preset wrapper to get analysis-specific defaults
without manually spelling every `cube-vesta` option:

```bash
multiwfn2vesta cube-preset density density.cub cube_products
multiwfn2vesta cube-preset orbital wfc_real.cub cube_products
multiwfn2vesta cube-preset orbital-density orbdens.cub cube_products
multiwfn2vesta cube-preset gradient-norm gradient.cub cube_products
multiwfn2vesta cube-preset spin-density spindensity.cub cube_products
multiwfn2vesta cube-preset laplacian laplacian.cub cube_products
multiwfn2vesta cube-preset hamiltonian-ked 'K(r).cub' cube_products
multiwfn2vesta cube-preset lagrangian-ked 'G(r).cub' cube_products
multiwfn2vesta cube-preset local-information-entropy infoentro.cub cube_products
multiwfn2vesta cube-preset electron-delocalization-range EDR.cub cube_products
multiwfn2vesta cube-preset orbital-overlap-distance EDRDmax.cub cube_products
multiwfn2vesta cube-preset pair-function fermihole.cub cube_products
multiwfn2vesta cube-preset source-function srcfunc.cub cube_products
multiwfn2vesta cube-preset becke-weight Becke.cub cube_products
multiwfn2vesta cube-preset hirshfeld-weight Hirshfeld.cub cube_products
multiwfn2vesta cube-preset rdg-scalar RDG.cub cube_products
multiwfn2vesta cube-preset promolecular-rdg RDGprodens.cub cube_products
multiwfn2vesta cube-preset promolecular-delta-g Delta_g.cub cube_products
multiwfn2vesta cube-preset hirshfeld-delta-g griddata.cub cube_products
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
  --texture-cube avglocion.cub
multiwfn2vesta cube-preset vdw-surface density.cub cube_products \
  --texture-cube vdW.cub
```

For signed ABACUS/Multiwfn scalar cubes such as real wavefunction amplitudes,
real orbital cubes, spin density, density differences, Fukui functions, or
dual descriptors:

```bash
multiwfn2vesta cube-vesta signed_scalar.cub cube_products \
  --surface-mode signed \
  --isosurface 0.02
```

This writes both positive and negative `ISURF` entries in one `.vesta` file,
using yellow for positive values and blue for negative values by default.
Use `cube-preset spin-density` directly when Multiwfn has already exported
`spindensity.cub`.  When separate alpha/beta or spin-up/spin-down density
cubes already exist on the same grid, build the spin-density cube first:

```bash
multiwfn2vesta cube-arith spin_products \
  --operation spin-density \
  --plus-cube alpha_density.cub \
  --minus-cube beta_density.cub \
  --stem spin_density
```

`cube-arith --preset auto` sends this product through
`cube-preset spin-density`; it does not generate the spin-channel cubes.

For a surface cube plus a compatible texture cube:

```bash
multiwfn2vesta cube-vesta surface.cub cube_products \
  --texture-cube texture.cub \
  --isosurface 0.01 \
  --tex-physical -0.05 0.05
```

For mapped surfaces whose color scale should reflect the actual displayed
surface rather than the full texture cube:

```bash
multiwfn2vesta cube-vesta surface.cub cube_products \
  --texture-cube texture.cub \
  --isosurface 0.01 \
  --tex-physical -0.05 0.05 \
  --tex-range-source surface-band
```

Keep `SECTS 0 0` as the default.  Treat `TEX3P` as VESTA percentage state,
not as direct physical scalar values.

For ABACUS Mulliken atom values:

```text
out_mul 1
```

Then color a VESTA structure by Mulliken charge or magnetism:

```bash
multiwfn2vesta abacus-mulliken-color structure.vesta mulliken.txt colored.vesta \
  --property charge \
  --vmin -1 --vmax 1
```

The parser follows current ABACUS `mulliken.txt` records:
`--- Ionic Step N ---`, `Atom N is LABEL`, `total charge on atom N`, and
optional `total magnetism on atom N`.  It uses the last ionic step by default
and maps values to VESTA sites by one-based atom index.  Keep strict mode on
unless deliberately coloring a subset; strict mode verifies that selected
VESTA `STRUC` site indices exactly match Mulliken atom indices.

For Molden products:

```text
basis_type lcao
gamma_only 1
out_wfc_lcao 1
```

Then run the latest converter:

```bash
multiwfn2vesta abacus-molden \
  /path/to/abacus/calc \
  /path/to/ABACUS_Multiwfn.molden
```

The wrapper exports `interfaces/Multiwfn_interface/molden.py` from the ABACUS
git ref, records the source path/commit/SHA256, runs the converter with an
absolute `-o`, writes stdout/stderr logs, and runs `molden-check --abacus`.
Use `--fetch --git-ref origin/develop` when refreshing the local ABACUS
checkout before conversion.

The upstream converter imports `numpy`, `scipy`, and `matplotlib`.
`abacus-molden` runs a dependency preflight with the selected Python before
starting the conversion.  Use `--python /path/to/python` to point at an
environment that has these modules; `--no-dependency-check` skips only the
preflight, not the converter's dependency.

The underlying ABACUS converter currently expects literal `INPUT`, `KPT`, and
`STRU` files plus `OUT.<suffix>`, pseudopotentials, and orbital files.  It
uses boolean values such as `--with-Nval true`; keep `[Nval]` enabled for
pseudopotential systems.  It may write `.gto` and `.gto.png` side products
beside files in `orbital_dir`, so make that directory writable.

If a Molden file already exists, verify the header before starting Multiwfn:

```bash
multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus
```

`[Nval]` must be present for pseudopotential systems.

For IRI/RDG from a full wavefunction, use the maintained command stream
wrapper:

```bash
multiwfn2vesta iri-run ABACUS_Multiwfn.molden iri_products \
  --timeout 300
```

This keeps raw Multiwfn `func1.cub`/`func2.cub`, writes processed
`<stem>_IRI1.cub`/`<stem>_IRI2.cub`, and then calls `cube-preset iri` for the
VESTA mapped surface.  Use `--commands-file` for non-default weak-interaction
menu choices.

For single real-space function cubes from the same ABACUS Molden file, use
`grid-run`:

```bash
multiwfn2vesta grid-run ABACUS_Multiwfn.molden grid_products \
  --function density \
  --grid-points 80 80 80 \
  --timeout 300
```

Useful `grid-run` functions for ABACUS-compatible Molden files include
`density`, `gradient`, `orbital --orbital h`, `orbital-density --orbital h`,
`spin-density`, `laplacian`, `hamiltonian-ked`, `lagrangian-ked`, `elf`,
`lol`, `local-information-entropy`, `esp`, `rdg`, `promolecular-rdg`,
`pair-function`, `source-function`, `edr`, `edrdmax`, `becke`, `hirshfeld`,
`delta-g`, `hirshfeld-delta-g`, `iri`, `vdw-potential`, and
`signlambda2rho`.
The single-cube display presets for `gradient.cub`, `spindensity.cub`,
`orbdens.cub`, `infoentro.cub`, `fermihole.cub`, `EDR.cub`,
`EDRDmax.cub`, `srcfunc.cub`, `Becke.cub`, `Hirshfeld.cub`, `RDG.cub`,
`RDGprodens.cub`, `Delta_g.cub`, function `23` generic `griddata.cub`,
`IRI.cub`, and `vdWpot.cub` follow
Multiwfn main-function-5 `sur_value`
defaults where the source defines them.  For `gradient.cub`, `infoentro.cub`,
`fermihole.cub`, `EDR.cub`, `EDRDmax.cub`, `srcfunc.cub`, `Delta_g.cub`,
and function `23` `griddata.cub`, Multiwfn leaves the function at the global
`sur_value=0.05`, so tune the VESTA isosurface per system.
`grid-run --function edr` requires `--edr-length D_BOHR`; `grid-run
--function edrdmax` uses Multiwfn's default exponent set unless
`--edr-exponents COUNT START INCREMENT` is supplied; `grid-run --function
pair-function` requires `--reference-point X Y Z`, patches `pairfunctype`
through `--pair-function-type`, and patches `paircorrtype` through
`--pair-correlation-type`; `grid-run --function source-function` requires
`--reference-point X Y Z`; `--source-function-mode` is patched into a
run-local settings file copied from the selected Multiwfn `settings.ini` when
available and passed with `-set`; `grid-run --function becke` requires `--becke-atoms I J`,
with `I J` for Becke overlap weight and `I 0` for Becke atomic weight;
`grid-run --function hirshfeld` requires
`--hirshfeld-atoms ATOMS`, for example `2,3,7-10`, and currently selects
Multiwfn's built-in atomic-density mode.  `infoentro.cub` uses signed
`local-information-entropy`, `fermihole.cub` uses `pair-function`,
`EDR.cub` uses `electron-delocalization-range`, `EDRDmax.cub` uses
`orbital-overlap-distance`, `srcfunc.cub` uses `source-function`,
`Becke.cub` uses
`becke-weight`, `Hirshfeld.cub` uses `hirshfeld-weight`, `Delta_g.cub`
uses standalone `promolecular-delta-g`, function `23` generic
`griddata.cub` uses standalone `hirshfeld-delta-g`, `IRI.cub` uses
standalone `iri-scalar`, and `vdWpot.cub` uses standalone
`vdw-potential` with `+/-1.0` kcal/mol signed
surfaces.  Use the existing two-cube `cube-preset iri` route when a
sign(lambda2)rho-like texture cube is available; use `vdw-map` when a vdW
potential cube should color a density/surface cube.  IGM/IGMH fragment
`dg_inter.cub` remains a separate mapped-surface workflow through
`cube-preset igmh`/`igm`.

For ABACUS LCAO Molden frontier orbital inspection, batch export is now the
maintained route:

```bash
multiwfn2vesta grid-run ABACUS_Multiwfn.molden orbital_products \
  --orbitals h l l+1 \
  --grid-points 80 80 80 \
  --no-vesta
```

The batch route repeats isolated single-orbital Multiwfn runs and writes a
top-level manifest plus one child directory per orbital.  Use
`--function orbital-density --orbitals ...` for density-like orbital maps.
For aligned potential-on-density, ALIE, vdW-map, or sign(lambda2)rho maps
where one density/surface cube is already available, let `grid-run` generate
the texture cube on the same grid and immediately call the mapped preset:

```bash
multiwfn2vesta grid-run ABACUS_Multiwfn.molden esp_map \
  --function esp \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub
```

Use explicit `cube-preset`/`cube-vesta` when both cubes already exist, for
LEA/LEAE user-function cubes, or for more specialized multi-layer products.

For constant-current STM/LDOS from ABACUS LCAO Molden, use `stm-run`:

```bash
multiwfn2vesta stm-run ABACUS_Multiwfn.molden stm_products \
  --bias -1.0 \
  --fermi -4.8 \
  --grid-points 120 120 60 \
  --x-range -6 6 \
  --y-range -6 6 \
  --z-range 2 8
```

If the ABACUS calculation used smearing/non-integer occupations, try
`--prepare-fermi-temperature TEMP_K` before STM.  The maintained output is the
3D `STM.cub` route and `cube-preset stm`, not Multiwfn's GUI 2D STM plane
plot.

## Priority Rules

- P0: generic cube VESTA, orbital cubes, density-derived/spin-density cubes,
  ELF/LOL, AIM, IGMH+AIM.
- P1: IRI/RDG/NCI, ESP/MEP mapped surfaces, STM/LDOS, ALIE/LEA/LEAE,
  vdW potential, ABACUS/Multiwfn atom scalar coloring.  ALIE/LEA/LEAE/vdW surface-map
  display presets now exist, and `surfanalysis.pdb` extrema overlays are
  maintained through `cube-preset --surfanalysis-pdb` and `surface-extrema`.
- P2: basins, excited-state hole/electron/CDD, ETS-NOCV, AdNDP, Fukui/dual
  descriptor, NICS/current arrows.

## Project References

- Research matrix:
  `docs/research/multiwfn_abacus_vesta_analysis_matrix.md`
- Cube to VESTA:
  `docs/skills/cube_vesta_skill.md`
- Surface extrema overlay:
  `docs/skills/surface_extrema_vesta_skill.md`
- Multiwfn grid-run:
  `docs/skills/multiwfn_grid_run_skill.md`
- AIM:
  `docs/skills/aim_paths_to_vesta_skill.md`
- AIM+IGMH:
  `docs/skills/aim_igmh_vesta_skill.md`
- IGMH cube preset:
  `docs/skills/igmh_vesta_preset_skill.md`
- IRI cube coloring:
  `docs/skills/iri_vesta_cube_skill.md`
- Atom scalar coloring:
  `docs/skills/vesta_atom_value_coloring_skill.md`
