# Project Kanban

Updated: 2026-06-08

## Doing

- Test and refine the maintained three-view export entry point based on
  `SCENE` patching.  Rendering remains disabled by default until a
  non-focus-stealing VESTA route is available.
- Find or build a real non-focus renderer.  Windows minimized/hidden/WSH
  launch routes and the current Linux wrapper are not yet usable.

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
- User confirmed the minimized Windows VESTA wrapper still steals focus; it is
  not a no-disruption renderer.
- Fixed the post-render compass arrowhead geometry so arrowheads no longer
  appear reversed.
- Added `scripts/vesta_three_views.py`, which starts from one `.vesta`, writes
  front/right/top `SCENE` variants, copies relative cube files, sets `COMPS 0`
  by default, and only renders when an explicit command template is supplied.
- Recorded AIM overlay style guidance: use one pseudo-element for path sample
  points and tune path/BCP radii before drawing AIM bonds.

## Next

- Try a non-activating launcher path or isolate rendering in a different
  desktop/session before using VESTA automation while the user is active.
- Add tests for `scripts/vesta_three_views.py` once script-level tests are
  organized for project utilities.
- If continuing Linux VESTA, add missing GUI libraries inside the workspace
  rather than modifying system packages.
