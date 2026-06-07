# Project Kanban

Updated: 2026-06-08

## Doing

- Wait for user-side confirmation on whether minimized Windows VESTA rendering
  still steals mouse focus.

## Done

- IRI color cube processing notes and skill were added in earlier work.
- AIM path/CP VESTA conversion and style patching were added in earlier work.
- Added experimental minimized Windows VESTA renderer:
  `scripts/render_vesta_nofocus.py`.
- Added `docs/vesta_nofocus_rendering.md` with the 2026-06-08 Ag(111)+benzene
  retest result and PowerShell quoting pitfall.
- Added `scripts/add_single_view_compass.py` for one VESTA-like lower-left
  compass after PNG export.
- Updated `docs/skills/vesta_camera_and_layers_skill.md` with the current
  `COMPS 0` plus post-render single-compass workflow.

## Next

- If the minimized renderer still steals focus, try a non-activating launcher
  path or isolate rendering in a different desktop/session.
- Promote three-view generation and single-compass post-processing from smoke
  scripts into reusable maintained project commands.
