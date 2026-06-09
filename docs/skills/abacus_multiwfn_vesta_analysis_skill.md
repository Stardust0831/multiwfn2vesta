# Skill: ABACUS to Multiwfn to VESTA Analysis Planning

Use this when deciding whether a Multiwfn analysis should become a maintained
VESTA workflow for ABACUS-generated data.

## Decision Order

1. Prefer ABACUS direct cube output when the target is simply density,
   potential, ELF, partial charge, or real-space wavefunction visualization.
2. Use ABACUS Molden only when Multiwfn needs a full wavefunction, for example
   AIM, IGMH, IRI/RDG from actual density, orbital cubes, ELF/LOL, ALIE, or
   density derivatives.
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

For Molden products:

```text
basis_type lcao
gamma_only 1
out_wfc_lcao 1
```

Then run the latest converter:

```bash
python interfaces/Multiwfn_interface/molden.py \
  -f /path/to/abacus/calc \
  -o ABACUS_Multiwfn.molden
```

Verify the Molden header before starting Multiwfn:

```bash
multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus
```

`[Nval]` must be present for pseudopotential systems.

## Priority Rules

- P0: generic cube VESTA, orbital cubes, density-derived cubes, ELF/LOL, AIM,
  IGMH+AIM.
- P1: IRI/RDG/NCI, ESP/MEP mapped surfaces, ALIE/LEA/LEAE, vdW potential,
  ABACUS/Multiwfn atom scalar coloring.
- P2: basins, excited-state hole/electron/CDD, ETS-NOCV, AdNDP, Fukui/dual
  descriptor, NICS/current arrows.

## Project References

- Research matrix:
  `docs/research/multiwfn_abacus_vesta_analysis_matrix.md`
- Cube to VESTA:
  `docs/skills/cube_vesta_skill.md`
- AIM:
  `docs/skills/aim_paths_to_vesta_skill.md`
- AIM+IGMH:
  `docs/skills/aim_igmh_vesta_skill.md`
- IRI cube coloring:
  `docs/skills/iri_vesta_cube_skill.md`
- Atom scalar coloring:
  `docs/skills/vesta_atom_value_coloring_skill.md`
