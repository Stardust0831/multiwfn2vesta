# Skill: multiwfn2vesta unified CLI

## When to use

Use this entry point when operating the project from a shell and the goal is to
avoid remembering `PYTHONPATH=src python -m ...` module paths.

## One-time setup

Add only the project `bin` directory to `PATH`:

```bash
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH
```

This is workspace-local and does not modify system files.  The launcher
automatically prepends `/mnt/g/work/multiwfn2vesta/project/src` to Python's
module path.

## Modes

Interactive chooser:

```bash
multiwfn2vesta
```

Scriptable subcommands:

```bash
multiwfn2vesta discover
multiwfn2vesta abacus-molden --help
multiwfn2vesta cube-preset --help
multiwfn2vesta cube-arith --help
multiwfn2vesta iri-run --help
multiwfn2vesta grid-run --help
multiwfn2vesta aim-run --help
multiwfn2vesta aim-pdb --help
multiwfn2vesta aim-igmh --help
```

Aliases:

- `multiwfn2vesta where` and `multiwfn2vesta env` are aliases for `discover`.
- `multiwfn2vesta molden ...` and `multiwfn2vesta abacus-multiwfn-molden ...`
  are aliases for `abacus-molden`.
- `multiwfn2vesta cube ...` is an alias for `cube-vesta`.
- `multiwfn2vesta preset ...` and `multiwfn2vesta analysis-cube ...` are
  aliases for `cube-preset`.
- `multiwfn2vesta cube-math ...`, `multiwfn2vesta density-diff ...`, and
  `multiwfn2vesta fukui-cube ...` are aliases for `cube-arith`.
- `multiwfn2vesta multiwfn-iri ...` and `multiwfn2vesta rdg-run ...` are
  aliases for `iri-run`.
- `multiwfn2vesta multiwfn-grid ...`,
  `multiwfn2vesta scalar-cube-run ...`, and
  `multiwfn2vesta function-cube ...` are aliases for `grid-run`.
- `multiwfn2vesta multiwfn-aim ...` is the same as `aim-run`.
- `multiwfn2vesta aim-vesta ...` is the same as `aim-pdb`.
- `multiwfn2vesta igmh ...` is the same as `aim-igmh`.

## Maintained workflows

### Discover executables

```bash
multiwfn2vesta discover
```

Use this before a new run.  It prints every Multiwfn/VESTA candidate and a
`selected:` line for the path that will be used by default.  Discovery prefers
explicit paths, environment variables, workspace-local tools, then `PATH`.

Multiwfn environment variables accepted:

- `MULTIWFN_PATH`
- `MULTIWFNPATH`
- `Multiwfnpath`
- `MultiwfnPATH`
- `MultiwfnPath`
- `MULTIWFN_EXECUTABLE`

VESTA environment variables accepted:

- `VESTA_PATH`
- `VESTA_DIR`
- `VESTAPATH`
- `VestaPATH`
- `Vestapath`
- `VESTA_EXECUTABLE`

### ABACUS calculation to Molden

```bash
multiwfn2vesta abacus-molden \
  abacus_calc \
  ABACUS_Multiwfn.molden
```

The command exports the ABACUS converter from
`interfaces/Multiwfn_interface/molden.py`, writes logs/recipe metadata, keeps
`[Nval]` enabled by default, and runs `molden-check --abacus` on the output.
The selected Python must be able to import `numpy`, `scipy`, and
`matplotlib`; use `--python /path/to/python` if the default `python3`
environment is not suitable.

### Cube analysis preset to VESTA

```bash
multiwfn2vesta cube-preset --list-presets
multiwfn2vesta cube-preset orbital orbital.cub cube_products
multiwfn2vesta cube-preset rdg IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub
```

Use this when the file is a common ABACUS/Multiwfn cube product and the
default style is enough to start.  Presets cover density-like scalar cubes,
signed orbital/wavefunction/density-difference cubes, ELF/LOL, IRI/RDG/NCI
mapped surfaces, and ESP/MEP mapped density surfaces.  All VESTA writing still
goes through the maintained `cube-vesta` backend.

### Cube arithmetic to density-difference/Fukui VESTA

```bash
multiwfn2vesta cube-arith cube_arith_products \
  --operation dual-descriptor \
  --anion-cube density_Nplus1.cub \
  --neutral-cube density_N.cub \
  --cation-cube density_Nminus1.cub
```

Use this after ABACUS, Multiwfn, or `grid-run` has produced compatible cube
files.  It writes a new cube and, by default, calls `cube-preset`; `--preset
auto` uses `density` for `fukui-plus/minus` and `signed` for
`density-difference`, `dual-descriptor`, and generic linear combinations.
Generic linear combinations use repeated `--term COEFF CUBE` entries.

The named formulae are `rho(N+1)-rho(N)` for `fukui-plus`,
`rho(N)-rho(N-1)` for `fukui-minus`, and
`rho(N+1)-2*rho(N)+rho(N-1)` for `dual-descriptor`.

### Wavefunction to Multiwfn IRI/RDG to VESTA

```bash
multiwfn2vesta iri-run \
  input.molden \
  iri_products \
  --timeout 300
```

Inputs can be any wavefunction file Multiwfn accepts, such as `.molden`,
`.fch`, `.fchk`, `.wfn`, or `.wfx`.  The command writes the exact Multiwfn
input stream and stdout/stderr logs, preserves raw `func1.cub`/`func2.cub`
under `multiwfn_iri_raw/`, processes them into `<stem>_IRI1.cub` and
`<stem>_IRI2.cub`, then calls `cube-preset iri` to create a mapped-surface
`.vesta` unless `--no-vesta` is supplied.

Explicit executable override:

```bash
multiwfn2vesta iri-run input.fch iri_products \
  --multiwfn /path/to/Multiwfn_noGUI \
  --nthreads 6 \
  --surface-band 0.25
```

Use `--commands-file commands.txt` to replace the default weak-interaction
menu stream.  The runner sets `Multiwfnpath`, `MULTIWFNPATH`, and
`MultiwfnPATH` to the selected executable directory for the subprocess.

### Wavefunction to Multiwfn scalar grid cube

```bash
multiwfn2vesta grid-run \
  input.molden \
  grid_products \
  --function density \
  --grid-points 40 40 40 \
  --timeout 300
```

Use this for Multiwfn main function `5` real-space scalar cubes.  The command
records the exact command stream, stdout/stderr, raw Multiwfn cube, processed
`<stem>_<function>.cub`, and a markdown recipe.  By default it calls
`cube-preset` with the function's maintained display preset.  Pass
`--no-vesta` for cube-only generation.

Function discovery:

```bash
multiwfn2vesta grid-run --list-functions
```

Common functions include `density`, `orbital --orbital h`, `orbital-density`,
`laplacian`, `elf`, `lol`, `esp`, `rdg`, `iri`, and `signlambda2rho`.

Batch frontier orbital export:

```bash
multiwfn2vesta grid-run input.fch orbital_products \
  --orbitals h l l+1 \
  --grid-points 80 80 80 \
  --no-vesta
```

With `--orbitals` and no explicit `--function`, the CLI defaults to
`orbital`.  Use `--function orbital-density --orbitals h l` for orbital
density cubes.  Batch mode is repeated isolated single-orbital execution: each
orbital gets a child directory with its own command stream, logs, raw cube
directory, processed cube, optional VESTA output, and one top-level
`multiwfn_grid_batch_recipe.md`.  Add `--keep-going` to continue after a
failed orbital; otherwise later orbitals are marked `skipped`.

Reference-cube grids are useful for aligned overlays:

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function esp \
  --grid-mode cube \
  --grid-cube density.cub \
  --no-vesta
```

### Wavefunction to Multiwfn AIM to VESTA

```bash
multiwfn2vesta aim-run \
  input.molden \
  aim_out \
  --timeout 180
```

Inputs can be any wavefunction file Multiwfn accepts, such as `.molden`,
`.fch`, `.fchk`, `.wfn`, or `.wfx`.  The command writes the exact Multiwfn
input stream and stdout/stderr logs into `aim_out/`, then converts
`paths.pdb` and `CPs.pdb` into `aim_atoms_only.vesta`.

Explicit executable override:

```bash
multiwfn2vesta aim-run input.fch aim_out \
  --multiwfn /path/to/Multiwfn_noGUI
```

The runner sets `Multiwfnpath`, `MULTIWFNPATH`, and `MultiwfnPATH` to the
selected executable directory for the subprocess.  If Multiwfn returns `0` but
does not write `paths.pdb`, the CLI returns `3` unless
`--allow-missing-paths` is explicitly supplied.

### AIM PDB to atoms-only VESTA

```bash
multiwfn2vesta aim-pdb \
  paths.pdb \
  aim_atoms_only.vesta \
  --cps-pdb CPs.pdb
```

### AIM+IGMH overlay style and optional render

```bash
multiwfn2vesta aim-igmh \
  input_overlay.vesta \
  output_dir \
  --label-bcp-sites
```

Rendering must be explicit because Windows VESTA automation can still steal
focus:

```bash
multiwfn2vesta aim-igmh \
  input_overlay.vesta \
  output_dir \
  --render-three-views \
  --initial-view top \
  --extra-rotate top x -8 \
  --scale 2
```

## Validation

No-GUI checks:

```bash
bin/multiwfn2vesta --help
bin/multiwfn2vesta discover
bin/multiwfn2vesta cube-preset --list-presets
bin/multiwfn2vesta iri-run --help
bin/multiwfn2vesta grid-run --help
bin/multiwfn2vesta aim-run --help
bin/multiwfn2vesta aim-igmh --help
printf 'q\n' | bin/multiwfn2vesta
PYTHONPATH=src python3 -m unittest tests.test_cli tests.test_cube_preset tests.test_executables tests.test_multiwfn_aim tests.test_multiwfn_iri
```

Real H2O Multiwfn noGUI smoke:

```bash
bin/multiwfn2vesta aim-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_aim_cli_smoke_20260610/h2o \
  --timeout 180
```

Observed output: `paths.pdb`, `CPs.pdb`, `CPprop.txt`, `mol.pdb`,
`multiwfn_aim_input.txt`, `multiwfn.stdout.txt`, `multiwfn.stderr.txt`, and
`aim_atoms_only.vesta`.

Real H2O Multiwfn noGUI IRI/RDG smoke:

```bash
bin/multiwfn2vesta iri-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_iri_run_smoke_20260610/h2o_run1/products \
  --timeout 240 \
  --stem h2o \
  --surface-band 0.25
```

Observed output: raw `func1.cub`/`func2.cub`, processed `h2o_IRI1.cub` and
`h2o_IRI2.cub`, `h2o_iri_cube.vesta`, and
`h2o_iri_cube_vesta_recipe.md`.  VESTA was not launched.

Real H2O Multiwfn noGUI grid-run density smoke:

```bash
bin/multiwfn2vesta grid-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_density/products \
  --function density \
  --grid-points 12 12 12 \
  --stem h2o \
  --timeout 180
```

Observed output: raw `density.cub`, processed `h2o_density.cub`,
`h2o_density_density_cube.vesta`, and both recipes.  VESTA was not launched.

Dry smoke for the current Ag(111)+benzene overlay:

```bash
bin/multiwfn2vesta aim-igmh \
  /mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/products/ag111_benzene_igmh_aim_paths_single_xe_yellow_bcp_periodic_overlay.vesta \
  /mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/unified_cli_smoke_20260610 \
  --stem ag111_benzene_igmh_aim_unified_cli \
  --label-bcp-sites
```

This smoke writes a styled `.vesta`, a recipe markdown file, and copied
`dg_inter.cub`/`sl2r.cub`; it does not launch VESTA unless
`--render-three-views` is added.
