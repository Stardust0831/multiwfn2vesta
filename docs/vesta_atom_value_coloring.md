# VESTA per-site atom value coloring

VESTA `.vesta` files have not shown a native atom scalar-to-colormap field in
local evidence.  The maintained implementation therefore colors atoms by
patching each target site's `SITET` RGB values.

This is suitable for scalar values such as Mulliken/RESP/Bader charge, Fukui
index, atom contribution, or any per-site signed property.

## Command line

Run from the project root:

```bash
PYTHONPATH=src python -m multiwfn2vesta.vesta_atom_coloring \
  input.vesta charges.csv output_colored.vesta \
  --vmin -1.0 --vmax 1.0 --center 0.0
```

The default colormap is a diverging blue-white-red scale:

- negative values: blue
- `center` value: near white
- positive values: red

If `--vmin` and `--vmax` are omitted, the code chooses a symmetric range around
`--center` from the supplied values.  Fixed ranges are recommended for comparing
multiple figures.

Use `--non-strict` to color only supplied sites and leave other `SITET` rows
unchanged.  Strict mode is the default and requires one value per `STRUC` site.

## ABACUS Mulliken shortcut

For ABACUS LCAO calculations with `out_mul 1`, use the maintained shortcut
instead of manually extracting a value table:

```bash
multiwfn2vesta abacus-mulliken-color \
  input.vesta mulliken.txt output_colored.vesta \
  --property charge \
  --vmin -1 --vmax 1
```

Available properties are `charge`, `magnetism`, `magnetism-x`,
`magnetism-y`, `magnetism-z`, and `magnetism-norm`.  The command reads all
ionic steps in `mulliken.txt`, uses the last one by default, maps values by
one-based atom index, and then calls the same `SITET` RGB patching logic
documented here.  Strict mode also requires the selected VESTA `STRUC` site
indices to match the Mulliken atom indices exactly, so a wrong structure file
or section fails before writing output.  Use `--non-strict` only for deliberate
subset coloring.  Use `--write-values selected.csv` to save the extracted
per-atom values for inspection or reuse.

## Value table formats

Ordered values, one row per site in `STRUC` order:

```text
-0.12
+0.35
-0.08
```

CSV/TSV keyed by label:

```csv
label,charge
H1,0.21
O1,-0.42
```

CSV/TSV keyed by one-based site index:

```text
index	value
1	0.21
2	-0.42
```

Accepted value column headers include `value`, `scalar`, `charge`, and `q`.

## Python API

```python
from multiwfn2vesta.vesta_atom_coloring import patch_vesta_atom_colors_file

patch_vesta_atom_colors_file(
    input_vesta,
    {"O1": -0.42, "H1": 0.21, "H2": 0.21},
    output_vesta,
    vmin=-1.0,
    vmax=1.0,
    center=0.0,
)
```

For text-level workflows:

```python
from multiwfn2vesta.vesta_atom_coloring import patch_vesta_atom_colors_text

colored_text = patch_vesta_atom_colors_text(vesta_text, [-0.1, 0.2, -0.1])
```

## Implementation notes

- The patcher reads `STRUC` site index/element/label records and edits the
  matching `SITET` section.
- Existing `SITET` radius, alpha, and tail fields are preserved.
- If a colored site lacks a `SITET` row, a new row is inserted before the
  `SITET` sentinel.  The row inherits radius/alpha from `ATOMT` for the site's
  element when possible; otherwise it uses radius `0.5000` and alpha `204`.
- Other `.vesta` sections are serialized through the existing lossless parser
  and are not intentionally changed.
- Multi-phase files can be targeted with `--section-index N`, where `N` is the
  zero-based `STRUC`/`SITET` pair index.

## Limitations

This is a per-site RGB patch, not VESTA native scalar-field coloring.  VESTA
will not know the original scalar values or draw a colorbar automatically.
Create a separate legend/colorbar if a figure needs one.

The two `SITET` RGB triplets and tail fields are still inferred from local
VESTA files.  Current project practice duplicates the RGB triplet and preserves
the existing alpha/style tail.
