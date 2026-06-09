# Project Kanban

Updated: 2026-06-09

## Doing

- Test and refine the maintained three-view export entry point based on
  `SCENE` patching.  Rendering remains disabled by default until a
  non-focus-stealing VESTA route is available.
- Find or build a real non-focus renderer.  Windows minimized/hidden/WSH
  launch routes and the current Linux wrapper are not yet usable.
- Keep the current Ag(111)+benzene IGMH+AIM overlay state inspectable without
  forcing VESTA rendering.  Latest preferred files are under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_single_xe_yellow_bcp_visible/`;
  they use original structure colors, one yellow Xe pseudo-element for AIM
  path samples, Rn pseudo-elements for BCPs, no AIM bonds, and `COMPS 0`.
- Decide the minimal full-overlay BCP visibility fix only after the user asks
  for style changes.  The current diagnostic conclusion is that VESTA can
  render BCP sites; full-overlay invisibility is a size/overlap/occlusion
  problem, not missing `CP000*_N` records.

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
- Added `multiwfn2vesta.vesta_aim_overlay_style` for post-processing
  multi-phase AIM overlays.  It keeps all path sample points, maps path samples
  to a single pseudo-element such as `Xe`, maps BCPs to a distinct
  pseudo-element such as `Rn`, clears AIM `SBOND`, and preserves global
  structure bonds by default.
- Real-rendered BCP visibility diagnostics with VESTA after explicit user
  request.  BCP-only front/right/top PNGs were generated under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_render_20260609/`,
  and a zoomed front diagnostic was generated under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_zoom_render_20260609/`.
  Visual inspection confirms three orange BCP points are displayed.
- Tested whether BCP visibility depends on VESTA atom naming or element
  symbols.  BCP-only controls using `N+CP000*_N`, `N+BCP*`, `Rn+CP*_N`,
  `Rn+RBCP*`, `Xe+CP*_N`, `C+CP*_N`, and `He+CP*_N` all rendered visible
  points.  The full-overlay BCP issue is therefore not explained by the
  `CP000*_N` label pattern or the tested element symbols.

## Next

- Try a non-activating launcher path or isolate rendering in a different
  desktop/session before using VESTA automation while the user is active.
- Add tests for `scripts/vesta_three_views.py` once script-level tests are
  organized for project utilities.
- If continuing Linux VESTA, add missing GUI libraries inside the workspace
  rather than modifying system packages.
- If the user asks for fresh PNGs, either run an explicitly accepted
  focus-stealing VESTA export or continue the Linux/local-library non-focus
  route first.
- For full-overlay BCP invisibility, investigate path-point overlap, phase
  draw order, depth/scale, and `SITET`/`ATOMT` style-table interaction before
  changing the BCP label naming scheme.
