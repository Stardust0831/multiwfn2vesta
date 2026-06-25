# ABACUS Molden + Multiwfn Excitation Bridge

Updated: 2026-06-26 CST

## Status

- [x] ABACUS Molden export path updated: the wrapper now prefers
  `tools/molden/molden.py` and falls back to the legacy
  `interfaces/Multiwfn_interface/molden.py` layout.
- [x] Multiwfn excitation input requirements rechecked from local source:
  hole/electron analysis needs a reference wavefunction plus a separate
  excitation list.
- [x] Existing project skeleton already has
  `examples/abacus_lr_tddft_excitation_bridge/` for a Gamma-only H2O smoke.
- [x] First converter implemented as `multiwfn2vesta abacus-lr-to-multiwfn`.
  It converts single-rank `Excitation_Energy_<label>.dat` and
  `Excitation_Amplitude_<label>_0.dat` into Multiwfn plain excitation text.
- [x] H2O LCAO/Gamma-only ABACUS smoke has been executed and verified in
  Multiwfn main function 18.

## What the Molden side can do

`abacus-molden` is only the reference-wavefunction half of the workflow.
With an LCAO Gamma/single-k ABACUS calculation it can export a Molden file
that Multiwfn can use for AIM, IGMH, IRI/RDG, STM/LDOS, and related ground
state analyses.

The wrapper now accepts both ABACUS tree layouts:

- latest: `tools/molden/molden.py`
- legacy fallback: `interfaces/Multiwfn_interface/molden.py`

That makes the wrapper usable across older and newer `abacus-develop`
checkouts without manual path edits.

## What Multiwfn still needs for excitation analysis

From the local Multiwfn source, excitation analysis is not satisfied by a
Molden file alone. The bridge needs:

1. a reference wavefunction file;
2. an excitation file listing state energies and orbital-transition
   coefficients;
3. for periodic cases, enough orbital/band metadata to map the occupied and
   virtual states back to the ABACUS output.

The practical text format is a plain excitation list such as:

```text
 Excited State     1   1    7.250000
  5 -> 6 0.53
  4 -> 7 -0.18

 Excited State     2   1    8.100000
  5 -> 7 0.42
```

That is the shortest path to hole/electron, transition-density, and NTO-like
workflows. It is also the least fragile compared with faking a CP2K output.
The blank line after each state is required in practice: Multiwfn's plain text
reader stops collecting the current state's orbital pairs when it sees a blank
line.

## ABACUS output gap

ABACUS LR-TDDFT already exposes the pieces we need in principle:

- `Excitation_Energy_*`
- `Excitation_Amplitude_*`

The first converter now:

1. reads those files from either the calculation directory or `OUT.*`;
2. infers `nocc` and `nvirt` from ABACUS running logs or INPUT files when
   possible, while still allowing explicit `--nocc/--nvirt` overrides because
   the amplitude file itself does not store these dimensions;
3. maps ABACUS pair index as `iocc * nvirt + ivirt`;
4. writes Multiwfn 1-based MO indices as `iocc+1 -> nocc+ivirt+1`;
5. scales coefficients by `1/sqrt(2)` by default, matching Multiwfn's
   closed-shell TDDFT normalization convention;
6. rejects multiple rank amplitude files by default.

The intentional first-version gap is distributed/multi-rank LR output. The
per-rank amplitude files are local pieces of ABACUS' 2D-distributed LR vector;
without the BLACS/Parallel_2D gather metadata, blindly concatenating rank
files would risk assigning coefficients to the wrong occupied/virtual pair.

## Recommended first smoke

Start from the existing H2O Gamma-only bridge example:

- `examples/abacus_lr_tddft_excitation_bridge/INPUT.scf`
- `examples/abacus_lr_tddft_excitation_bridge/INPUT.lr`
- `examples/abacus_lr_tddft_excitation_bridge/STRU`
- `examples/abacus_lr_tddft_excitation_bridge/KPT`

Expected output chain:

1. ABACUS SCF run.
2. `abacus-molden` export of the reference wavefunction.
3. ABACUS LR-TDDFT output collection.
4. parser -> Multiwfn excitation text.
5. Multiwfn hole/electron or transition-density export.
6. VESTA preview.

Converter command:

```bash
multiwfn2vesta abacus-lr-to-multiwfn OUT.lr h2o_singlet.excit.txt \
  --label singlet \
  --coeff-threshold 0.01
```

## Real H2O Smoke Result

Local result directory:

```text
smoke/abacus_h2o_lr_bridge_20260626/
```

Server calculation directory:

```text
~/multiwfn2vesta_runs/abacus_h2o_lr_bridge_cpu_device_20260626
```

The working ABACUS route was LCAO/Gamma-only with `device cpu`, `nbands 20`,
`nocc 4`, `nvirt 16`, and `lr_nstates 5`.  The initial `nbands 28` input failed
because the H2O basis had only 23 local orbitals (`NLOCAL < NBANDS`).  A GPU LR
attempt with corrected `nbands 20` reached SCF but failed in ABACUS LCAO/GPU LR
at `gint_rho_gpu.cu` with a CUDA illegal memory access, so the verified bridge
uses explicit CPU for the LR stage.

Generated ABACUS LR files:

```text
raw/OUT.abacus_h2o_lr/Excitation_Energy_singlet.dat
raw/OUT.abacus_h2o_lr/Excitation_Amplitude_singlet_0.dat
```

Generated bridge products:

```text
products/h2o_singlet.excit.txt
products/h2o_singlet.excit.txt.recipe.md
products/ABACUS_Multiwfn.molden
products/ABACUS_Multiwfn_abacus_molden_recipe.md
products/multiwfn_function18_he_probe.log
```

The converter inferred `nocc=4` and `nvirt=16` from
`OUT.abacus_h2o_lr/running_scf_1.log`.  After applying the default
`coefficient_scale=1/sqrt(2)`, Multiwfn loaded the converted plain text in main
function `18 -> 1`, recognized 5 singlet states, and for S1 reported coefficient
normalization `0.499713`, only `0.000287` away from the expected `0.5`.

The latest local `origin/develop` of ABACUS at commit
`4b1fc7d8787c69c4406e02651faa85a32310510a` still did not contain
`tools/molden/molden.py`; the wrapper therefore used the maintained fallback
`interfaces/Multiwfn_interface/molden.py`.  The output Molden contains `[Cell]`
and `[Nval]`, and `molden-check --abacus` passed.

## Practical next step

Run the parser against one real LR-TDDFT output first, then keep the format
intentionally narrow:

- Gamma-only only.
- LCAO only.
- single-rank amplitude file only.
- restricted closed-shell singlet/triplet first; open-shell label is accepted
  as a label but not yet converted to spin-suffixed `A/B` transition lines.
- Closed-shell H2O smoke is now verified.

Once that is stable, decide whether the same format can cover periodic slab or
COF cases without adding extra ABACUS-specific branches.
