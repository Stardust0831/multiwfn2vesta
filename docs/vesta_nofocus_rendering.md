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
- user-side focus stealing still needs visual confirmation from the desktop.

When checking Windows processes from WSL, quote PowerShell scripts with bash
single quotes or escape `$`.  Bash double quotes expand `$_` before PowerShell
sees it and can produce thousands of false `/bin/bash.Name` errors.
