# VESTA `.vesta` Format Notes

This note records observations from `sj/C.vesta` and the lossless parser shape
used by `multiwfn2vesta.vesta_parser`.

## Sample Structure

The sample is UTF-8-compatible text with CRLF newlines. It has 198 lines and
starts with a three-line preamble:

- `#VESTA_FORMAT_VERSION 3.5.4`
- blank line
- blank line

After that, directive records are introduced by uppercase section names. Some
headers carry inline arguments, for example `TRANM 0`, `THERI 1`, `HBOND 0 2`,
`DISPF 37753794`, and `LIGHT0 1`.

Observed record boundaries in `sj/C.vesta`:

| Lines | Name | Body lines | Terminator candidate |
| --- | --- | ---: | --- |
| 4-5 | CRYSTAL | 1 | |
| 6-8 | TITLE | 2 | |
| 9-10 | GROUP | 1 | |
| 11-24 | SYMOP | 13 | `-1.0 -1.0 -1.0  0 0 0  0 0 0  0 0 0` |
| 25-26 | TRANM | 1 | |
| 27-29 | LTRANSL | 2 | |
| 30-33 | LORIENT | 3 | |
| 34-39 | LMATRIX | 5 | |
| 40-42 | CELLP | 2 | |
| 43-48 | STRUC | 5 | `0 0 0 0 0 0 0` |
| 49-52 | THERI | 3 | `0 0 0` |
| 53-54 | SHAPE | 1 | fixed-size candidate |
| 55-57 | BOUND | 2 | fixed-size candidate |
| 58-60 | SBOND | 2 | `0 0 0 0` |
| 61-64 | SITET | 3 | `0 0 0 0 0 0` |
| 65-66 | VECTR | 1 | `0 0 0 0 0` |
| 67-68 | VECTT | 1 | `0 0 0 0 0` |
| 69-70 | SPLAN | 1 | `0   0   0   0` |
| 71-80 | LBLAT/LBLSP/DLATM/DLBND/DLPLY | 1 each | `-1` |
| 81-82 | PLN2D | 1 | `0   0   0   0` |
| 83-85 | ATOMT | 2 | `0 0 0 0 0 0` |
| 86-93 | SCENE | 7 | fixed-size candidate |
| 94-95 | HBOND | 1 blank | inline count candidate |
| 96-136 | STYLE through DPTHQ | mixed | style directives |
| 137-176 | LIGHT0-LIGHT3 | 9 each | fixed-size candidate |
| 177-180 | SECCL/TEXCL | 1 blank each | inline count candidate |
| 181-198 | ATOMM/BONDM/POLYM/SURFM/FORMM/HKLPM | 2 each | fixed-size candidate |

The parser treats every directive as a record rather than modeling `CRYSTAL`
and `STYLE` as nested containers. This is deliberate: it gives stable edit
targets while preserving all whitespace and line endings.

## Parser Data Model

`VestaDocument` stores:

- `preamble_lines`: all lines before the first directive.
- `sections`: ordered `VestaSection` records.
- `encoding`: used for byte serialization.

`VestaSection` stores:

- `name`: first token of the directive line.
- `header_line`: original directive line including its newline.
- `body_lines`: original following lines until the next directive.
- `start_line` and derived `end_line`.
- `args`: tokens after the directive name on the header line.
- `terminator_line`: a conservative candidate for known sentinel-terminated
  list records.

`document.to_bytes()` is expected to reproduce the original bytes when no
edits are made.

## Current Limits

- The known directive list is seeded from `sj/C.vesta`; unfamiliar VESTA
  directives will be treated as body text until added to the directive set.
- The prototype does not validate numeric field counts or VESTA semantics.
- Terminator detection is conservative and only marks known list-like records.
- It does not yet model nested containers such as `CRYSTAL` and `STYLE`.
- It assumes the caller knows the correct text encoding; the sample works with
  UTF-8.

## Integration Direction

Use this parser as the base layer for format-preserving edits. Higher-level
helpers can later parse specific bodies such as `CELLP`, `STRUC`, `SITET`,
`SCENE`, or `LIGHT*`, but should keep the raw section lines as the source of
truth for serialization.
