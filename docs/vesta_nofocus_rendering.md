# VESTA no-focus rendering branch

This branch isolates experiments for rendering with less UI interference.

The first maintained experiment is not strictly headless.  It starts Windows
VESTA from WSL through PowerShell with `-WindowStyle Minimized`, waits for the
export to finish, and then cleans only `VESTA.exe` processes whose command line
contains this workspace path.

Script:

```bash
python project/scripts/render_vesta_nofocus.py input.vesta output.png \
  --scale 2 \
  --clean-before
```

Current intent:

- avoid stealing the user's mouse/focus where possible;
- keep the normal VESTA renderer for visual fidelity;
- keep this route separate from the ordinary Windows VESTA CLI workflow until
  it is proven reliable.

Known limitations:

- This is not a true no-UI renderer; it still launches VESTA.
- Windows may still briefly focus a GUI process depending on desktop policy.
- The script validates success by output file existence because VESTA can
  return nonzero codes after writing a valid image.
- True headless Linux VESTA remains blocked locally: earlier `-nogui` tests
  opened files but did not export images, and the GTK build needed additional
  GUI libraries.

## 2026-06-08 retest

Retested on the current Ag(111)+benzene IGMH+AIM right-view file:

```bash
python3 project/scripts/render_vesta_nofocus.py \
  smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_igmh_aim_paths_clear/ag111_benzene_igmh_aim_paths_clear_periodic_overlay_right.vesta \
  smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/nofocus_render_retest_20260608/right_nofocus_raw.png \
  --scale 2 --clean-before --timeout 240
```

Result:

- render exit status: `0`;
- output: valid `3014 x 1600` RGB PNG;
- post-render process check: no `VESTA.exe` process with command line matching
  `G:\work\multiwfn2vesta`;
- user-side focus stealing was later confirmed, so this wrapper is not an
  acceptable no-disruption renderer.

When checking Windows processes from WSL, quote PowerShell scripts with bash
single quotes or escape `$`.  Bash double quotes expand `$_` before PowerShell
sees it and can produce thousands of false `/bin/bash.Name` errors.

Current status:

- keep this script only as a controlled one-shot Windows VESTA automation path;
- do not use it as the default renderer while the user is actively using the
  desktop;
- prefer generating patched `.vesta` files without rendering until a
  non-activating or true headless render path is available.

Additional failed experiments:

- Linux VESTA through the local wrapper did not start because
  `libwebkit2gtk-4.0.so.37` was missing from the workspace-local library set.
- Windows WSH `WScript.Shell.Run(..., 7, True)` returned without creating a
  PNG.
- PowerShell `Start-Process -WindowStyle Hidden` timed out without creating a
  PNG.

## 2026-06-09 BCP display diagnostic

The user explicitly requested real rendering to confirm BCP display, so the
known focus-stealing wrapper was used as a controlled one-shot route.

Example command:

```bash
python3 project/scripts/render_vesta_nofocus.py \
  smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_render_20260609/ag111_benzene_aim_interface_bcp_only_periodic_front.vesta \
  smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_render_20260609/ag111_benzene_aim_interface_bcp_only_periodic_front.png \
  --scale 2 --clean-before --timeout 240
```

Result:

- BCP-only front/right/top PNGs were written successfully under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_render_20260609/`.
- A zoom-only diagnostic PNG was written under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_zoom_render_20260609/`.
- The rendered images confirm BCP sites can be displayed by VESTA; the full
  overlay issue is visibility/overlap/occlusion, not absent records.
- No workspace-scoped VESTA process remained after the render.

## 2026-06-09 BCP naming diagnostic

The same controlled one-shot wrapper was used for BCP-only atom naming
controls.

Rendered files:

```text
smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_name_diagnostic_20260609/bcp_name_matrix_top.png
smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_name_diagnostic_20260609/single_*.png
```

Result:

- All PNGs were written successfully as valid `3048 x 1500` RGB images.
- `N+CP000*_N`, `N+BCP*`, `Rn+CP*_N`, `Rn+RBCP*`, `Xe+CP*_N`,
  `C+CP*_N`, and `He+CP*_N` all rendered visible BCP-only points.
- Pixel counting found colored BCP pixels in every single-variant render.
- No workspace-scoped VESTA process remained after rendering.
