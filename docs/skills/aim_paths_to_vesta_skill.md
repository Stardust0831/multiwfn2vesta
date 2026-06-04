# Skill: Multiwfn AIM paths to VESTA

## When to use

Use this workflow when Multiwfn AIM topology analysis has produced `paths.pdb`
and optionally `CPs.pdb`, and VESTA should display the paths/critical points
without generating dense automatic bonds between path points.

## Inputs

- Multiwfn noGUI executable:
  `/mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI`
- Wavefunction file, for example:
  `tools/Multiwfn_2026.6.2_bin_Linux_noGUI/examples/H2O.fch`
- Optional existing Multiwfn command stream:
  `tools/Multiwfn_2026.6.2_bin_Linux_noGUI/examples/scripts/AIM.txt`
- Converter module:
  `multiwfn2vesta.aim_vesta`

## Key facts

- Multiwfn `paths.pdb` writes every path sample point as `HETATM` with atom
  name/element `C`, residue name `PTH`, and residue sequence equal to the path
  index.
- Multiwfn `CPs.pdb` uses element codes for CP type:
  - `C`: `(3,-3)` nuclear attractor
  - `N`: `(3,-1)` BCP
  - `O`: `(3,+1)`
  - `F`: `(3,+3)`
- VESTA direct import may treat dense path points as carbon atoms and generate
  excessive C-C bonds.
- The safe VESTA output has empty `SBOND` and `BONDS   0` for the AIM point
  phase.

## Steps

1. Run Multiwfn AIM topology analysis in an isolated working directory.

   ```bash
   timeout 60s /mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI \
     /path/to/input.fch \
     < AIM_exit.txt > multiwfn.stdout.txt 2> multiwfn.stderr.txt
   ```

2. Confirm outputs exist.

   ```bash
   ls -lh paths.pdb CPs.pdb CPprop.txt mol.pdb
   ```

3. Convert AIM paths/CPs to atoms-only VESTA.

   ```bash
   cd /mnt/g/work/multiwfn2vesta
   PYTHONPATH=project/src python -m multiwfn2vesta.aim_vesta \
     /path/to/paths.pdb \
     /path/to/aim_atoms_only.vesta \
     --cps-pdb /path/to/CPs.pdb \
     --title "AIM paths and CPs"
   ```

4. Verify no AIM bonds will be drawn.

   ```bash
   rg -n '^SBOND$|^BONDS|CP.*_N' /path/to/aim_atoms_only.vesta
   ```

## Expected validation

- `paths.pdb` should have many `HETATM ... PTH ...` records and `TER` after
  each path.
- `CPs.pdb` should have `N` records for BCPs.
- Generated `.vesta` should contain:
  - `SBOND` followed by `0 0 0 0`
  - `BONDS   0`
  - BCP labels such as `CP0004_N`

## Real smoke result

H2O smoke directory:

```text
smoke/20260604_task_i_h2o_aim_final/
```

Observed:

- 120 path points
- 4 paths
- 5 CPs
- 2 BCPs
- VESTA PNG exported successfully from atoms-only `.vesta`

## Failure notes

- Full `unittest discover` currently fails because old tests still import
  `src.multiwfn_vesta`; use focused tests until package naming is repaired.
- VESTA Windows interop may return nonzero or timeout after exporting an image.
  Check the output file and run a cleanup close/taskkill command.

