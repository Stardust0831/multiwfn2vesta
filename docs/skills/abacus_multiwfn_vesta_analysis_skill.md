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
real orbital cubes, density differences, Fukui functions, or dual
descriptors:

```bash
multiwfn2vesta cube-vesta signed_scalar.cub cube_products \
  --surface-mode signed \
  --isosurface 0.02
```

This writes both positive and negative `ISURF` entries in one `.vesta` file,
using yellow for positive values and blue for negative values by default.

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
`density`, `orbital --orbital h`, `orbital-density --orbital h`, `laplacian`,
`elf`, `lol`, `esp`, `rdg`, `iri`, and `signlambda2rho`.

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

- P0: generic cube VESTA, orbital cubes, density-derived cubes, ELF/LOL, AIM,
  IGMH+AIM.
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
