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
multiwfn2vesta aim-pdb --help
multiwfn2vesta aim-igmh --help
```

Aliases:

- `multiwfn2vesta aim-vesta ...` is the same as `aim-pdb`.
- `multiwfn2vesta igmh ...` is the same as `aim-igmh`.

## Maintained workflows

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
bin/multiwfn2vesta aim-igmh --help
printf 'q\n' | bin/multiwfn2vesta
PYTHONPATH=src python3 -m unittest tests.test_cli
```

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
