# Skill: VESTA trajectory frames

## When to use

Use this workflow when a standard XYZ or extXYZ trajectory should become a
directory of per-frame VESTA structure files.  This is the maintained upstream
step before VESTA PNG rendering and `trajectory-video` MP4 encoding.

## Current maintained command

Minimal Cd/Cl example:

```bash
multiwfn2vesta trajectory-frames examples/cdcl_trajectory_video/cdcl_tiny.extxyz \
  /tmp/cdcl_vesta_frames \
  --bond Cd Cl 0 3.5 \
  --boundary -0.05 1.05 -0.05 1.05 -0.05 1.05
```

Reuse a saved VESTA style/camera tail:

```bash
multiwfn2vesta trajectory-frames traj.extxyz frame_products \
  --reference-vesta nvt_frame_0001_saved.vesta \
  --bond Cd Cl 0 3.5 \
  --boundary -0.05 1.05 -0.05 1.05 -0.05 1.05 \
  --stride 20
```

## Inputs

- Standard XYZ multi-frame files.
- extXYZ files with `Lattice="a1x a1y a1z a2x ... a3z"`; these are written
  as VESTA `CRYSTAL` frames with fractional coordinates.
- Standard XYZ plus `--cell-vectors` for periodic frames when no extXYZ
  lattice is available.
- Optional reference `.vesta` for the `SCENE`/`STYLE` tail.

## Outputs

- `vesta/frame_0001.vesta` etc.
- `frame_trajectory_frames_manifest.json`.
- `frame_trajectory_frames_recipe.md`.

The command does not start VESTA and does not render PNG images.

## Practical defaults

- Use `--boundary -0.05 1.05 -0.05 1.05 -0.05 1.05` for periodic materials
  when atoms near cell edges should remain visible.
- Use repeated `--bond E1 E2 MIN MAX` rules for chemically meaningful bonds.
  The Cd/Cl smoke uses `--bond Cd Cl 0 3.5`.
- Use `--reference-vesta` after manually saving a well-framed VESTA file if
  style and camera consistency matter.
- Use `--stride` for quick previews before generating a long sequence.

## Boundaries

- ASE `.traj` is not read directly yet; export XYZ/extXYZ first.
- Unattended VESTA PNG rendering is still a separate workflow because the GUI
  can steal focus.
- MP4 encoding is handled by `multiwfn2vesta trajectory-video` after PNG
  frames exist.
