# Skill: VESTA atom scalar value coloring

Use this when a `.vesta` file should color atoms/sites by per-atom scalar
values such as Mulliken, RESP, Bader charge, Fukui index, or atom contribution.

## Core rule

Do not look for a VESTA-native atom scalar colormap field.  Local evidence says
the reliable route is:

1. read sites from `STRUC`,
2. read scalar values by site order, label, or index,
3. map values to RGB in Python,
4. patch each site's `SITET` RGB triplets.

This is explicit per-site styling, not semantic scalar data inside VESTA.

## Command

```bash
cd /mnt/g/work/multiwfn2vesta/project
PYTHONPATH=src python -m multiwfn2vesta.vesta_atom_coloring \
  input.vesta values.csv output_colored.vesta \
  --vmin -1 --vmax 1 --center 0
```

Use `--non-strict` only when intentionally coloring a subset of sites.

ABACUS Mulliken shortcut:

```bash
cd /mnt/g/work/multiwfn2vesta/project
multiwfn2vesta abacus-mulliken-color \
  input.vesta mulliken.txt output_colored.vesta \
  --property charge \
  --vmin -1 --vmax 1
```

Use `--property magnetism` for `nspin=2` atomic spin populations and
`--property magnetism-x|magnetism-y|magnetism-z|magnetism-norm` for `nspin=4`.
The command uses the last ABACUS ionic step unless `--step N` is supplied and
maps values by one-based atom index.  Strict mode verifies exact VESTA
`STRUC`/Mulliken index agreement; use `--non-strict` only for an intentional
subset.

## Value tables

Ordered values:

```text
-0.12
0.30
-0.18
```

Label keyed:

```csv
label,charge
C1,-0.12
H1,0.30
```

Index keyed:

```text
index	value
1	-0.12
2	0.30
```

## API

```python
from multiwfn2vesta.vesta_atom_coloring import patch_vesta_atom_colors_file

patch_vesta_atom_colors_file(
    input_vesta,
    {"C1": -0.12, "H1": 0.30},
    output_vesta,
    vmin=-1.0,
    vmax=1.0,
    center=0.0,
)
```

## Checks

```bash
cd /mnt/g/work/multiwfn2vesta/project
PYTHONPATH=src python -m unittest tests.test_vesta_atom_coloring -v
```

Inspect the output:

```bash
rg -n "^SITET$|^[[:space:]]+[0-9]+[[:space:]]" output_colored.vesta
```

## Cautions

- Fixed `--vmin/--vmax` should be used for comparing multiple figures.
- VESTA will not generate a scalar legend from these patched RGB values.
- Existing `SITET` radii and alpha/style tail are preserved.  Missing `SITET`
  rows are inserted using `ATOMT` radius/alpha when available.
- If VESTA saves a multi-phase file, inspect the final `SITET` rows again
  before exporting publication images.
