# Skill: VESTA multi-phase overlay

## When to use

Use this workflow when a real molecular/structural layer and an AIM point layer
should be shown together in one VESTA graphics area.

## Key facts

- VESTA multi-layer data are saved as phases.
- A multi-phase `.vesta` file is not a concatenation of complete `.vesta` files.
- Observed VESTA-saved layout:

  ```text
  #VESTA_FORMAT_VERSION ...
  MOLECULE or CRYSTAL  phase 1
  ...
  MOLECULE or CRYSTAL  phase 2
  ...
  STYLE                shared style
  ...
  ```

- `-open file1 -open file2` opens tabs/windows and saves the current tab.
- `-open file1 -i file2 -save out.vesta` imports file2 as an overlaid phase in
  the same data set.

## Steps

1. Convert the base molecular PDB to `.vesta`.

   Use individually quoted Windows paths when calling Windows VESTA from WSL.

   ```bash
   timeout 30s /mnt/c/WINDOWS/system32/cmd.exe /c "$VESTA_EXE" \
     -open "$BASE_PDB_WIN" \
     -save "$BASE_VESTA_WIN" \
     -export_img scale=1 "$BASE_PNG_WIN" \
     -flush -close
   ```

2. Import the AIM atoms-only `.vesta` as a second phase.

   ```bash
   timeout 40s /mnt/c/WINDOWS/system32/cmd.exe /c "$VESTA_EXE" \
     -open "$BASE_VESTA_WIN" \
     -i "$AIM_VESTA_WIN" \
     -save "$MULTIPHASE_VESTA_WIN" \
     -export_img scale=1 "$MULTIPHASE_PNG_WIN" \
     -flush -close
   ```

3. Cleanup VESTA if needed.

   ```bash
   /mnt/c/WINDOWS/system32/cmd.exe /c "$VESTA_EXE" -close || true
   /mnt/c/WINDOWS/system32/cmd.exe /c "taskkill /IM VESTA.exe /F" || true
   ```

4. Patch AIM atom types after VESTA saves the merged file.

   VESTA may keep only the base phase's global `ATOMT` rows when it writes a
   multi-phase file.  If the AIM phase uses C/N/O/F pseudo atom types for path
   and CP colors, patch the saved file before the final image export.

   ```bash
   PYTHONPATH=project/src python -m multiwfn2vesta.vesta_aim_style \
     "$MULTIPHASE_VESTA" \
     "$MULTIPHASE_VESTA_PATCHED"
   ```

5. Verify phase structure.

   ```bash
   PYTHONPATH=project/src python - <<'PY'
   from pathlib import Path
   from multiwfn2vesta.vesta_parser import read_vesta_bytes
   p = Path("path/to/multiphase.vesta")
   d = read_vesta_bytes(p)
   for name in ["MOLECULE", "CRYSTAL", "TITLE", "PHASON", "QCORIG", "STYLE"]:
       print(name, len(d.sections_named(name)))
   print(d.to_bytes() == p.read_bytes())
   PY
   ```

## Real smoke result

Overlay directory:

```text
smoke/h2o_aim_multiphase/products/
```

Outputs:

- `h2o_mol.vesta`
- `h2o_mol.png`
- `h2o_mol_plus_aim_multiphase.vesta`
- `h2o_mol_plus_aim_multiphase.png`

Observed phase counts:

- `MOLECULE`: 1
- `CRYSTAL`: 1
- `TITLE`: 2
- `PHASON`: 2
- `QCORIG`: 2
- `STYLE`: 1
- byte round-trip: true

This real overlay was generated from:

- base molecular layer: `smoke/20260604_task_i_h2o_aim_final/mol.pdb`
- AIM layer: `smoke/20260604_task_i_h2o_aim_final/h2o_aim_atoms_only.vesta`

Important detail: first save `mol.pdb` to `h2o_mol.vesta`, then import the AIM
`.vesta` with `-i`. Direct `-open mol.pdb -i aim.vesta -save ...` did not save
successfully in the local smoke test.

For AIM-focused overlays, avoid VDW-sized base molecule atoms.  In the H2O
alignment smoke, VESTA's default H radius was large enough to completely cover
nearby BCPs.  A small-atom base layer plus `vesta_aim_style` post-processing
produced a visible BCP overlay:

```text
smoke/20260605_aim_overlay_alignment/products/h2o_mol_small_plus_aim_aligned_postatomt.vesta
smoke/20260605_aim_overlay_alignment/products/h2o_mol_small_plus_aim_aligned_postatomt.png
```

## Failure notes

- If VESTA reports that `smoke\...` cannot be saved, the Windows path was
  probably passed as a relative path. Use `wslpath -w` and quote each argument
  individually instead of placing the whole command in one quoted `cmd /C`
  string.
- Shared `STYLE` may contain `BONDS   1` for the base molecular phase. The AIM
  phase can still avoid path-point bonds because its `SBOND` section is empty.
- If CP colors disappear after `-save`, inspect the final `ATOMT` section.
  Missing C/N/O/F rows mean VESTA dropped the AIM atom type table; run
  `multiwfn2vesta.vesta_aim_style` on the saved merged file.
