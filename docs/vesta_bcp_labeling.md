# VESTA BCP Labeling Notes

Date: 2026-06-10

## Goal

Mark AIM bond critical point indices such as `BCP1`, `BCP2`, and `BCP3` in
VESTA figures without reintroducing AIM bonds or moving BCP coordinates.

## Evidence

- VESTA official manual chapter 12 says atom labels can use either element
  names or site names, and labels are displayed near atoms with a z-axis offset
  in Angstrom.
- The same chapter says the Objects tab atom table has columns `L`, `S`, and
  `V` for label visibility, selection, and object visibility.
- VESTA official manual chapter 6 says a structure parameter site label is up
  to nine characters.  Short labels such as `BCP1` or `B001` fit this
  constraint better than long explanatory text.
- Third-party VESTA input generation code in `aiida-crystal17` writes a
  per-site `SITET` tail field named `show_label`, but comments that it needs to
  be used together with `LBLAT`.
- Local VESTA files mostly contain empty label blocks:
  `LBLAT` followed by `-1` and `LBLSP` followed by `-1`.  No local generated
  file currently gives a trusted non-empty `LBLAT` example.

## Sources

- Official VESTA manual, atom label behavior and Objects tab:
  `https://jp-minerals.org/vesta/en/doc/VESTAch12.html`
- Local cache of the same manual:
  `/mnt/g/work/multiwfn2vesta/downloads/vesta_manual/VESTAch12.html`
- Official VESTA manual, site label length in structure parameters:
  `https://jp-minerals.org/vesta/en/doc/VESTAch6.html`
- Third-party VESTA writer evidence for `SITET` tail and `LBLAT` coupling:
  `https://aiida-crystal17.readthedocs.io/en/stable/_modules/aiida_crystal17/parsers/raw/vesta.html`

## Practical recommendation

1. Keep BCPs as real pseudo-sites in the final BCP overlay phase.
2. For simple native VESTA labels, write concise site labels such as `BCP1`,
   `BCP2`, and `BCP3` into the BCP `STRUC`, `THERI`, and `SITET` records, then
   enable atom labels as "Names of sites" in VESTA.  This uses VESTA's
   documented label model.
3. For publication-style numbering, prefer a post-render annotation step on
   the exported PNG/SVG.  It can place text in screen space, avoid occlusion,
   and does not depend on undocumented `.vesta` label block syntax.
4. Do not implement generated non-empty `LBLAT` records until a controlled
   VESTA GUI-save diff is available.  The diff should toggle one BCP site's
   label visibility and atom-label offset, save both files, then compare
   `LBLAT`, `SITET`, `LABEL`, and any `DLATM` changes.

## Notes For Future Implementation

- A robust BCP-label helper should preserve coordinates and phase order.
- If it renames BCP labels, it must update all matching records in that phase:
  `STRUC`, `THERI`, and `SITET`.
- If PNG post-processing is used, the labels should be driven by the same BCP
  site list used to generate the `.vesta`, but final placement should be view
  specific because VESTA projections can hide or overlap labels.
