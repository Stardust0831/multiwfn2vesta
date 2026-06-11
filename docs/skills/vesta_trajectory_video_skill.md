# Skill: VESTA trajectory video

## When to use

Use this workflow when VESTA trajectory frames have already been rendered to a
PNG sequence and the next step is to make a reproducible MP4.  If the starting
point is XYZ/extXYZ rather than PNG, first use `trajectory-frames` to write
per-frame `.vesta` files.

## Current maintained command

Dry-run from an explicit PNG frame directory:

```bash
multiwfn2vesta trajectory-video png_frames trajectory.mp4 \
  --fps 24 \
  --bitrate 20M
```

Dry-run from a curated artifact manifest:

```bash
multiwfn2vesta trajectory-video \
  --manifest examples/cdcl_trajectory_video/artifact_manifest.json \
  --output /tmp/cdcl_trajectory.mp4 \
  --fps 24 \
  --bitrate 20M
```

Execute ffmpeg only after checking the printed command and recipe:

```bash
multiwfn2vesta trajectory-video png_frames trajectory.mp4 \
  --fps 24 \
  --bitrate 20M \
  --run
```

Add `--overwrite` only when replacing an existing MP4 is intended.

## Outputs

- `<output>_frames.txt`: ffmpeg concat input list with naturally sorted PNG
  frames.
- `<output>_trajectory_video_recipe.md`: frame directory, frame count,
  first/last frame, encoding settings, command, and run status.
- `<output>.mp4`: only when `--run` is used and ffmpeg succeeds.

## Quality defaults

- Default codec: `libx264`.
- Default pixel format: `yuv420p`.
- Default bitrate: `20M`, matching the high-bitrate Cd/Cl smoke convention.
- Use `--crf N` instead of `--bitrate` when CRF quality mode is preferred.

## Cd/Cl smoke example

The current curated example is:

```bash
multiwfn2vesta examples --id cdcl_trajectory_video --verify-smoke
multiwfn2vesta trajectory-frames examples/cdcl_trajectory_video/cdcl_tiny.extxyz \
  /tmp/cdcl_vesta_frames \
  --bond Cd Cl 0 3.5 \
  --boundary -0.05 1.05 -0.05 1.05 -0.05 1.05
multiwfn2vesta trajectory-video \
  --manifest examples/cdcl_trajectory_video/artifact_manifest.json \
  --output /tmp/cdcl_trajectory.mp4 \
  --fps 24 \
  --bitrate 20M
```

The manifest records the committed poster frames and workspace-local smoke
evidence.  Large videos remain in `smoke/` and are not committed.

## Boundaries

- This command does not start VESTA and should not steal focus.
- XYZ/extXYZ to `.vesta` frame generation is handled by
  `multiwfn2vesta trajectory-frames`.
- ASE `.traj` direct reading is still not maintained; export XYZ/extXYZ first.
- Unattended VESTA PNG rendering is still separate and should eventually
  connect to the same artifact manifest contract.
