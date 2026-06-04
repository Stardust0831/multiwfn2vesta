# VESTA `.vesta` multi-structure notes

Date: 2026-06-04

## Short answer

VESTA supports multiple overlaid structures as multiple **phases/layers** in one
Graphics Area, but the `.vesta` storage observed here is **not** a simple
concatenation of multiple complete files:

```text
#VESTA_FORMAT_VERSION ...
CRYSTAL
...
STYLE
...
#VESTA_FORMAT_VERSION ...
CRYSTAL
...
STYLE
...
```

The observed saved multi-phase file has one file preamble, then multiple phase
records beginning with `CRYSTAL`, followed by one shared style/rendering tail:

```text
#VESTA_FORMAT_VERSION 3.5.4

CRYSTAL
TITLE
...
PLN2D

CRYSTAL
TITLE
...
HBOND 0 2

STYLE
DISPF ...
...
```

In the VESTA-saved experiment, the second phase did not start with a second
`#VESTA_FORMAT_VERSION`, and there was only one `STYLE` block for the whole
saved data set.

## Official documentation checked

Official VESTA online manual:

- Main documentation: <https://www.jp-minerals.org/vesta/en/doc.html>
- Chapter 6, "GIVING PHASE DATA":
  <https://www.jp-minerals.org/vesta/en/doc/VESTAch6.html>
- Chapter 7, "OVERLAYING MULTIPLE DATA":
  <https://www.jp-minerals.org/vesta/en/doc/VESTAch7.html>
- Chapter 17, "COMMAND LINE INTERFACE":
  <https://www.jp-minerals.org/vesta/en/doc/VESTAch17.html>

Relevant manual findings:

- Chapter 6 says the Edit Data dialog has a `Phase` tab, and that in this tab
  users can add, delete, copy, or import phase data overlaid on the same
  Graphics Area. It also says single-phase data normally needs no work in this
  tab except editing the title.
- Chapter 7 says multiple data in one Graphics Area are multiple-phase data.
  It describes positioning and orientation per phase, and treats "phase" and
  "layer" as the relevant concepts. Layer 0 is the internal Cartesian coordinate
  system, not a structure loaded from file.
- Chapter 4 says `Save`/`Save As` saves the current data to `*.vesta` with the
  VESTA format. Chapter 17 says `-open file` opens/visualizes a file, `-i file`
  reads a file without visualization, and `-save file` saves data to a file.

I did not find an official textual `.vesta` file-format specification that
documents phase-block grammar directly.

## Local VESTA experiments

Experiment directory:

```text
smoke/20260604_task_j_vesta_multistructure/
```

Inputs:

- `sj/C.vesta`
- `project/examples/output_files/synthetic_aim_paths.vesta`

### Direct concatenation

Generated:

```text
smoke/20260604_task_j_vesta_multistructure/concat_two_complete_blocks.vesta
```

This file is just `sj/C.vesta` plus
`project/examples/output_files/synthetic_aim_paths.vesta`.

Observed headers:

```text
4:CRYSTAL
6:TITLE
96:STYLE
202:CRYSTAL
204:TITLE
290:STYLE
```

Command:

```text
VESTA.exe -open concat_two_complete_blocks.vesta -save saved_from_concat.vesta -close
```

Result:

- Return code recorded as `5`.
- No `products/saved_from_concat.vesta` was produced.
- This does not prove every concatenated file will fail, but this direct
  "two complete files in sequence" form was not accepted/saved by the tested
  VESTA Windows build.

### Two `-open` commands

Command:

```text
VESTA.exe -open C.vesta -open synthetic_aim_paths.vesta -save saved_from_two_open.vesta -close
```

Result:

- `products/saved_from_two_open.vesta` was produced.
- It contains one `CRYSTAL` and one `STYLE`.
- Its title is `synthetic_aim_paths`, so this saved the current/last opened tab,
  not a merged multi-phase data set.
- The output was 200 lines, not the sum of both input files.

Conclusion: multiple `-open` commands are tab/window behavior, not
multi-phase composition.

### `-open` plus `-i`

Command:

```text
VESTA.exe -open C.vesta -i synthetic_aim_paths.vesta -save saved_open_then_i.vesta -close
```

Result:

- `products/saved_open_then_i.vesta` was produced despite the GUI command
  timing out after save.
- The file has one `#VESTA_FORMAT_VERSION`, two `CRYSTAL` records, two
  `TITLE` records, and one `STYLE` record.
- Header outline:

```text
4:CRYSTAL
6:TITLE
40:PHASON
62:QCORIG
90:CRYSTAL
92:TITLE
115:PHASON
143:QCORIG
184:STYLE
```

The first phase runs from `CRYSTAL` at line 4 through `PLN2D` at line 88. The
second phase starts at `CRYSTAL` line 90 and runs through `HBOND 0 2` at line
182. The shared `STYLE` block starts at line 184.

This is the strongest local evidence for actual multi-phase `.vesta` layout.

## Observed multi-phase file structure

From `products/saved_open_then_i.vesta`, each imported phase starts with
`CRYSTAL`, then has structure directives such as:

```text
TITLE
GROUP
SYMOP
TRANM
LTRANSL
LORIENT
LMATRIX
PHASON
CELLP
STRUC
THERI
SHAPE
BOUND
QCORIG
SBOND
SITET
VECTR
VECTT
SPLAN
LBLAT
LBLSP
DLATM
DLBND
DLPLY
PLN2D
```

The last phase in this sample also contains:

```text
ATOMT
SCENE
HBOND 0 2
```

Then the file has one global/shared style tail:

```text
STYLE
DISPF
MODEL
SURFS
...
```

So the practical grammar is closer to:

```text
file_preamble
phase_block+
global_style_block
```

not:

```text
complete_vesta_file+
```

## Parser impact

Current parser:

```text
project/src/multiwfn2vesta/vesta_parser.py
```

Observed behavior on the VESTA-saved multi-phase file:

- It can preserve bytes on round trip.
- It sees repeated `CRYSTAL` and `TITLE` directives as repeated flat sections.
- `document.section("CRYSTAL")` raises `KeyError` because `CRYSTAL` is not
  unique.
- Current parser revisions include `PHASON` and `QCORIG` in
  `DEFAULT_SECTION_NAMES`, so they are parsed as standalone directives.
- Later H2O overlay testing showed molecule/structure overlays may use a
  `MOLECULE` phase followed by a `CRYSTAL` phase and one shared `STYLE` block;
  `MOLECULE` is also in `DEFAULT_SECTION_NAMES`.

This means the current flat parser is acceptable only as a raw lossless layer.
For multi-phase editing it needs at least:

- Keep adding known directives seen in VESTA output, probably including
  format/import directives from VESTA strings such as `BEGIN_BLOCK_DATA`,
  `BEGIN_BLOCK_DATAGRID`, `IMPORT_STRUCTURE`, `IMPORT_DENSITY`,
  `IMPORT_TEXTURE`, and `IMPORT_ORFFE`.
- Add a phase grouping helper that splits sections at each `CRYSTAL` or
  `MOLECULE` before the shared `STYLE` block.
- Avoid using `section(name)` for directives that can repeat per phase; use
  `sections_named(name)` or a phase-scoped accessor.
- Treat `STYLE` as global/shared unless further samples prove phase-specific
  style blocks can appear.

## Uncertainties

- I did not find official `.vesta` grammar documentation, so the exact required
  directive order and which directives are per-phase versus global are still
  inferred from VESTA output.
- The sample used two `.vesta` structures with the same element symbol (`C`).
  `ATOMT` behavior may differ when phases contain different elements.
- I did not manually use the GUI Phase tab. The command-line `-open` plus `-i`
  path produced a valid multi-phase save and matches the manual's import/read
  concept, but GUI-created multi-phase files should still be sampled if exact
  production parity matters.
