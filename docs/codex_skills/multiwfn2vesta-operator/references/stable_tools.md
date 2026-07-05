# Stable Human-Facing Tools

Use these through:

```bash
multiwfn2vesta tools --lang zh
multiwfn2vesta tools run <tool> -- <args>
```

Only list a workflow here when it has local tests, committed sample inputs, or
the user explicitly confirmed it works.

| Tool | Purpose | Backing command | Stability note |
| --- | --- | --- | --- |
| `discover` | Find Multiwfn/VESTA executables | `discover` | No calculation; safe diagnostic. |
| `examples` | Show curated examples/gallery/readiness | `examples` | Uses committed docs/assets. |
| `cube` | Cube to VESTA via maintained preset | `cube-preset` | VESTA file generation only; no GUI. |
| `esp-surface` | ABACUS density + ESP cubes to vacuum-zero ESP-colored VESTA scene | `abacus-esp-align` + `cube-preset esp` | Tested on committed tiny cube sample and real COF workflow experience. |
| `excitation-bridge` | ABACUS LR amplitudes to Multiwfn excitation text | `abacus-lr-to-multiwfn` | Stable only for single-rank/Gamma-style output. |
| `aim-pdb` | Multiwfn AIM PDB to atoms-only VESTA | `aim-pdb` | Avoids fake bonds by design. |
| `aim-igmh` | Style saved AIM+IGMH overlay | `aim-igmh` | Coordinates are not shifted to fix views. |
| `trajectory-frames` | XYZ/extXYZ trajectory to VESTA frames | `trajectory-frames` | Does not render PNG or start VESTA. |
| `trajectory-video` | Already-rendered PNG frames to MP4 | `trajectory-video` | Does not start VESTA. |
| `abacus-atom-color` | ABACUS Mulliken charge/magnetism to atom colors | `abacus-mulliken-color` | Per-site RGB patch, not native VESTA scalar map. |
| `atom-table-color` | Generic atom scalar table to atom colors | `multiwfn-atom-color` | Per-site RGB patch; include external legend if needed. |

## Not Stable Tools Yet

- VESTA no-focus/headless PNG rendering: still environment-sensitive.
- ABACUS LR multi-rank/multi-k excitation conversion: needs gather metadata.
- ABACUS GPU/PW multi-rank direct cube workflows: known risk in tested beta
  versions.
- NICS/current-vector rendering: miscellaneous record only, not maintained.

## Common Commands

ESP surface:

```bash
multiwfn2vesta tools run esp-surface -- chg.cube potes.cube esp_products \
  --axis z --tex-physical -0.08 0.08
```

Excited-state bridge:

```bash
multiwfn2vesta tools run excitation-bridge -- OUT.lr state.excit.txt \
  --label singlet --coeff-threshold 0.01
```

Trajectory movie:

```bash
multiwfn2vesta tools run trajectory-video -- png_frames movie.mp4 \
  --bitrate 20M --run
```
