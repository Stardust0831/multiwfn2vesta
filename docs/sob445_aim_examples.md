# Sobereva 445 AIM examples

This smoke run uses real Multiwfn AIM topology output from systems connected to
Sobereva article 445: http://sobereva.com/445

The direct article reproduction target is `GC.wfn`.  Additional local
wavefunction examples exercise compact hydrogen-bond, ring-critical-point, and
dense fused-ring cases.

| Case | Input | Atoms | CP total | CP type counts | Path points | Path groups | AIM VESTA |
| --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| `h2o_hf` | `examples/Vn/H2O-HF.wfn` | 5 | 9 | `C:5 N:4` | 291 | 8 | generated |
| `benzene` | `examples/benzene.wfn` | 12 | 25 | `C:12 N:12 O:1` | 954 | 24 | generated |
| `gc` | `examples/GC.wfn` | 29 | 67 | `C:29 N:33 O:5` | 2750 | 66 | generated |
| `phenanthrene` | `examples/phenanthrene.wfn` | 24 | 55 | `C:24 N:27 O:4` | 2268 | 54 | generated |

Smoke artifacts are kept outside the git project at:

`/mnt/g/work/multiwfn2vesta/smoke/20260605_sob445_more_aim_examples`

Final smoke PNGs were generated for both AIM-only and molecule plus AIM overlay
views.  The regenerated AIM inputs follow Multiwfn's VMD defaults: path points
use radius `0.0200`, and all CP/BCP pseudo-sites use radius `0.0700`.

Use the same conversion command for each case:

```bash
cd /mnt/g/work/multiwfn2vesta/project
PYTHONPATH=src python -m multiwfn2vesta.aim_vesta \
  ../smoke/20260605_sob445_more_aim_examples/<case>/paths.pdb \
  ../smoke/20260605_sob445_more_aim_examples/<case>/products/<case>_aim_atoms_only.vesta \
  --cps-pdb ../smoke/20260605_sob445_more_aim_examples/<case>/CPs.pdb \
  --title "Sobereva 445 <case> AIM paths and CPs"
```

Notes:

- The generated AIM VESTA files intentionally use no bonds.  Path points in
  `paths.pdb` are pseudo atoms sampled along AIM topology paths.
- `N` pseudo atoms are `(3,-1)` BCPs and are styled as orange CP spheres.
- `O` pseudo atoms are `(3,+1)` ring critical points and are styled yellow.
- Use `--path-radius`, `--cp-radius`, or `--bcp-radius` only when a figure
  intentionally needs stronger size emphasis than Multiwfn's default style.
- C60 and C18 examples mentioned by the article need wavefunction files before
  this AIM pipeline can run; local package files found so far are geometry
  inputs rather than ready AIM wavefunction inputs.
