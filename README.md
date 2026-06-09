# multiwfn2vesta

`multiwfn2vesta` is a workspace-local Python interface for running selected
Multiwfn workflows and preparing VESTA visualization files.  The currently
maintained path focuses on AIM topology data, VESTA atoms-only overlays, and
AIM+IGMH multi-phase VESTA figures.

The project is still experimental, but the CLI below is the maintained entry
point.

## Repository Status

- Maintained branch: `main`.
- GitHub remote: `origin` points to `Github:Stardust0831/multiwfn2vesta.git`,
  with `origin/HEAD -> origin/main`.
- Current local/remote branch check after `git fetch --prune`: only `main`
  and `origin/main` are present.
- Previous experiment branches have been merged into `main` and removed from
  the remote when no longer needed.
- Repository-local commit identity is
  `Stardust0831 <13862180016@163.com>`.

## Maintained Features

- Discover workspace, environment, and `PATH` executables for Multiwfn and
  VESTA.
- Check Molden files before Multiwfn workflows, including ABACUS-specific
  `[Cell]` and `[Nval]` requirements.
- Create VESTA `.vesta` files directly from ABACUS or Multiwfn scalar cube
  files, with optional texture/color cube support, surface-band texture
  scaling, and signed positive/negative isosurface presets.
- Run Multiwfn AIM topology analysis from a wavefunction file such as
  `.molden`, `.fch`, `.fchk`, `.wfn`, or `.wfx`.
- Convert Multiwfn `paths.pdb` and `CPs.pdb` to an atoms-only `.vesta` file
  with AIM bonds disabled.
- Style saved AIM+IGMH multi-phase `.vesta` overlays with one yellow path
  pseudo-element, orange BCPs, optional BCP labels, and optional three-view
  export.
- Keep VESTA rendering explicit because the Windows VESTA automation route can
  still steal desktop focus.

## Quick Start

From this repository:

```bash
cd /mnt/g/work/multiwfn2vesta/project
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH
multiwfn2vesta --help
```

The workspace launcher automatically adds `src/` to Python's import path.  An
editable install also provides console scripts:

```bash
pip install -e .
multiwfn2vesta --help
```

## Find Multiwfn and VESTA

```bash
multiwfn2vesta discover
multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus
```

Multiwfn discovery checks, in order:

1. Explicit `--multiwfn` paths for commands that accept it.
2. `MULTIWFN_PATH`, `MULTIWFNPATH`, `Multiwfnpath`, `MultiwfnPATH`,
   `MultiwfnPath`, `MULTIWFN_EXECUTABLE`.
3. Workspace-local tools, preferring
   `tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI`.
4. Shell `PATH`.

VESTA discovery checks:

1. Explicit VESTA render options such as `--vesta-dir`.
2. `VESTA_PATH`, `VESTA_DIR`, `VESTAPATH`, `VestaPATH`, `Vestapath`,
   `VESTA_EXECUTABLE`.
3. Workspace-local VESTA tools.
4. Shell `PATH`.

## Cube to VESTA

For direct ABACUS cubes such as charge density, potential, ELF, partial charge,
or real-space wavefunction cubes, and for Multiwfn-generated scalar cubes:

```bash
multiwfn2vesta cube-vesta density.cub cube_products --isosurface 0.01
```

For signed scalar fields such as real orbital amplitudes, real wavefunction
cubes, density differences, or dual-descriptor style cubes:

```bash
multiwfn2vesta cube-vesta orbital.cub cube_products \
  --surface-mode signed \
  --isosurface 0.02
```

In signed mode, `--isosurface X` is treated as a magnitude.  The generated
`ISURF` block contains `+abs(X)` in yellow and `-abs(X)` in blue by default.
Both levels must be inside the cube data range.

For a surface cube colored by a compatible texture cube:

```bash
multiwfn2vesta cube-vesta IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub \
  --isosurface 1.0 \
  --tex-physical -0.04 0.04
```

For IRI/RDG/ESP style mapped surfaces, the color range can be derived from
texture values near the requested surface instead of the whole texture cube:

```bash
multiwfn2vesta cube-vesta IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub \
  --isosurface 1.0 \
  --tex-physical -0.04 0.04 \
  --tex-range-source surface-band
```

The command writes a `.vesta` file, copies cube dependencies beside it by
default, and writes a markdown recipe.  `SECTS 0 0` is the default to avoid
VESTA section planes.  `TEX3P` is written as VESTA percentage/normalized
values, not direct physical scalar limits.

## Wavefunction to AIM VESTA

For ABACUS-generated Molden files, check the file before using it as a
Multiwfn wavefunction input:

```bash
multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus
```

ABACUS mode requires `[Cell]`, `[Atoms]`, `[GTO]`, `[MO]`, and `[Nval]`.
`[Nval]` is required for pseudopotential systems so Multiwfn sees effective
valence nuclear charges instead of all-electron atomic numbers.

Run Multiwfn AIM analysis and convert the generated AIM PDB files:

```bash
multiwfn2vesta aim-run input.molden aim_out --timeout 180
```

Default outputs in `aim_out/`:

- `multiwfn_aim_input.txt`
- `multiwfn.stdout.txt`
- `multiwfn.stderr.txt`
- `paths.pdb`
- `CPs.pdb`
- `CPprop.txt`
- `mol.pdb`
- `aim_atoms_only.vesta`

Use an explicit Multiwfn executable when needed:

```bash
multiwfn2vesta aim-run input.fch aim_out \
  --multiwfn /mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI
```

The runner sets `Multiwfnpath`, `MULTIWFNPATH`, and `MultiwfnPATH` for the
Multiwfn subprocess based on the selected executable directory.  If Multiwfn
returns 0 but does not create `paths.pdb`, the CLI returns exit code `3` unless
`--allow-missing-paths` is supplied.

## Existing AIM PDB to VESTA

If Multiwfn has already produced `paths.pdb` and `CPs.pdb`:

```bash
multiwfn2vesta aim-pdb paths.pdb aim_atoms_only.vesta \
  --cps-pdb CPs.pdb \
  --title "AIM paths and CPs"
```

For overlays on VESTA-opened cube files, shift AIM coordinates into the cube
frame:

```bash
multiwfn2vesta aim-pdb paths.pdb aim_atoms_only_cube_frame.vesta \
  --cps-pdb CPs.pdb \
  --cube-frame-from-cube molecule_IRI2.cub
```

The generated `.vesta` intentionally disables AIM bonds, so VESTA does not
connect dense path points as ordinary chemical bonds.

## AIM+IGMH VESTA Overlay

For a saved VESTA file that already contains a structure/IGMH cube phase and
an imported AIM path/BCP phase:

```bash
multiwfn2vesta aim-igmh input_overlay.vesta products
```

Defaults:

- AIM path samples use one yellow pseudo-element, `Xe`, radius `0.0600`.
- BCPs use orange `Rn`, radius `0.1800`.
- AIM-phase `SBOND` is cleared.
- Real structure bonds are kept.
- BCPs are split into the final phase for visibility.
- Coordinates are not moved and overlapping path samples are not deleted.

Optional native VESTA site labels:

```bash
multiwfn2vesta aim-igmh input_overlay.vesta products --label-bcp-sites
```

Optional three-view rendering:

```bash
multiwfn2vesta aim-igmh input_overlay.vesta products \
  --render-three-views \
  --initial-view top \
  --extra-rotate top x -8 \
  --scale 2
```

Rendering is opt-in because local Windows VESTA automation may still steal
focus.  The maintained three-view renderer opens one `.vesta` once and exports
views by VESTA CLI rotations, rather than writing persistent front/right/top
`.vesta` files.

## Validation

Current focused no-GUI checks:

```bash
PYTHONPATH=src python3 -m unittest \
  tests.test_molden_check \
  tests.test_cube_vesta \
  tests.test_cli \
  tests.test_aim_igmh_vesta \
  tests.test_vesta_aim_overlay_style \
  tests.test_executables \
  tests.test_multiwfn_aim \
  tests.test_iri_cube \
  tests.test_aim_vesta \
  tests.test_vesta_atom_coloring
```

Smoke-tested ABACUS Molden check:

```bash
multiwfn2vesta molden-check \
  /mnt/g/work/multiwfn2vesta/smoke/abacus_server_artifacts_20260606/ag111_benzene/ag111_benzene_lcao_cont3_nval.molden \
  --abacus
```

The Ag(111)+benzene Molden check reported 60 atoms, 566 MO blocks, three
`[Nval]` entries (`Ag=19`, `C=4`, `H=1`), three numeric `[Cell]` rows, and
`Result: OK`.

Smoke-tested H2O-HF cube-to-VESTA run:

```text
/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_cli_smoke_20260610/
```

It generated `h2o_hf_iri_cube.vesta`, copied `h2o_hf_IRI2_surface.cub` and
`h2o_hf_IRI1_color.cub`, set `IMPORT_DENSITY`/`IMPORT_TEXTURE`, disabled
sections with `SECTS 0 0`, and wrote `TEX3P` as a percentage range.

Smoke-tested Multiwfn noGUI AIM run:

```text
/mnt/g/work/multiwfn2vesta/smoke/multiwfn_aim_cli_smoke_20260610/h2o/
```

This H2O run produced `paths.pdb`, `CPs.pdb`, `CPprop.txt`, `mol.pdb`, logs,
and `aim_atoms_only.vesta` without launching VESTA.

## Documentation Map

- `docs/usage.md`: fuller user guide.
- `docs/skills/multiwfn2vesta_cli_skill.md`: CLI operating notes.
- `docs/skills/cube_vesta_skill.md`: ABACUS/Multiwfn cube to VESTA workflow.
- `docs/skills/aim_paths_to_vesta_skill.md`: AIM topology to VESTA workflow.
- `docs/skills/aim_igmh_vesta_skill.md`: reusable AIM+IGMH overlay workflow.
- `docs/research/multiwfn_abacus_vesta_analysis_matrix.md`: roadmap for
  Multiwfn analyses that are useful in VESTA, especially ABACUS-driven ones.
- `docs/skills/abacus_multiwfn_vesta_analysis_skill.md`: checklist for choosing
  ABACUS direct-cube, ABACUS Molden, Multiwfn, and VESTA routes.
- `docs/skills/vesta_camera_and_layers_skill.md`: VESTA camera, layers, and
  three-view export notes.
- `docs/worklog.md`: implementation history and smoke results.
- `docs/kanban.md`: current project board.
