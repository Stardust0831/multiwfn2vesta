# Skill: VESTA trajectory video

## When to use

Use this workflow when VESTA trajectory frames have already been rendered to a
PNG sequence and the next step is to make a reproducible MP4.  This skill does
not cover ASE/XYZ trajectory parsing or VESTA frame rendering yet.

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
- It does not yet create VESTA frame files from ASE/XYZ trajectories.
- It does not yet apply reference `.vesta` camera, Boundary, or bond rules to
  new frames.
- The next workflow increment should connect trajectory-to-frame generation
  and VESTA PNG rendering to the same artifact manifest contract.
