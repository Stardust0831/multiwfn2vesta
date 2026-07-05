# VESTA `.vesta` Field Reference

This is a project reverse-engineering reference, not an official VESTA
specification. Preserve unknown fields and prefer format-preserving edits.

Confidence labels:

- `confirmed`: directly verified by local samples or project tests.
- `inferred`: matches local samples and VESTA behavior but still needs more
  GUI diff samples.
- `unknown`: preserve only; do not invent semantics.

## High-Value Directives

| Field | Meaning | Confidence | Project practice |
| --- | --- | --- | --- |
| `TITLE` | Structure or phase title. | confirmed | Use meaningful workflow names. |
| `CELLP` | Unit-cell lengths and angles. | confirmed | Preserve for periodic cube/ABACUS workflows. |
| `STRUC` | Site list: index, element/label, occupancy, fractional or Cartesian coordinates depending on structure type. | inferred | Keep site order aligned with `SITET` and atom-value tables. |
| `THERI` | Thermal/extra per-site values. | inferred | Preserve labels when relabeling BCP/site names. |
| `BOUND` | Display boundary ranges, usually x/y/z min/max. | inferred | Common useful boundary is `-0.05 1.05` for all axes. |
| `SBOND` | Bond search/display rules. | inferred | Structure phases need nonempty rules; AIM path/BCP phases should usually be empty. |
| `SITET` | Per-site radius/color/style and label flag. | inferred | Used for atom scalar coloring and BCP label visibility. |
| `ATOMT` | Per-element atom style. | inferred | Preserve unless intentionally changing global element colors. |
| `SCENE` | Global camera/view matrix and shift/zoom-like values. | inferred | Copy `SCENE` to reuse a manually tuned view. |
| `STYLE` | Start of global display style region. | inferred | Shared across phases; changes can affect all layers. |
| `BONDS` | Global bond display flag. | inferred | `BONDS 1` alone is insufficient without `SBOND`. |
| `ISURF` | Isosurface settings and values. | inferred | `cube-preset` writes density/signed/texture workflows here. |
| `TEX3P` | Texture color scaling in normalized/percentage-like coordinates. | inferred | Do not write physical values directly; convert from cube/reference range. |
| `SECTS` | Section/cut-plane display control. | inferred | Most project workflows set sections off. |
| `COMPS` | Native VESTA compass/component display. | inferred | Set off before post-processing one custom compass. |
| `LABEL` | Global label mode/style; first value selects element/site label in local tests. | inferred | For BCP numbering use site names plus `LABEL 1`. |
| `PHASON` | Per-phase matrix seen in VESTA-saved multi-phase files. | unknown | Do not use as visibility control without GUI hidden-phase diff. |
| `QCORIG` | Per-phase origin-like record in multi-phase files. | unknown | Do not edit for visibility; it may affect alignment. |

## Bond Display

VESTA needs two layers for structure bonds:

1. `BONDS   1`
2. one or more `SBOND` rules with element pairs and distance windows

For AIM topology layers, write an empty `SBOND` sentinel to avoid VESTA
connecting dense path points or BCP pseudo-atoms.

## Texture Scaling

`TEX3P` stores VESTA's normalized texture range, not the physical cube range.
For an ESP surface:

1. Align the electrostatic potential cube to a vacuum plateau.
2. Pick physical color limits, for example `-0.08..0.08`.
3. Convert those limits against the selected texture reference range.
4. Write the normalized values to `TEX3P`.

Use `tex_range_source=surface-band` or nearest-surface sampling when the full
cube range is dominated by off-surface values.

## Multi-Phase Files

Observed facts:

- A multi-phase `.vesta` has one shared `STYLE` block.
- Current local samples show one global `SCENE`.
- Phase show/hide state has not been reliably identified.

Safe layer strategies:

- `remove`: create a render copy with only visible phases.
- `style`: set inactive sites small/transparent and clear inactive `SBOND`;
  validate with a render.
- Do not edit `QCORIG`/`PHASON` for visibility until hidden-phase GUI diffs
  prove their role.

## Camera and Views

For three-view exports, prefer one VESTA load and command-line rotations
instead of writing persistent front/right/top `.vesta` files. If view sign is
wrong, correct camera rotations, not atomic coordinates.

For oversized scenes, copy a tuned `SCENE` from a manually saved reference
file and adjust zoom-like scene values only on a render copy.
