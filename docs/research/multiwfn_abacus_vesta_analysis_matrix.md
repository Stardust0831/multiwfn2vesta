# Multiwfn, ABACUS, and VESTA Analysis Matrix

Date: 2026-06-10

This note ranks Multiwfn wavefunction analyses by how useful they are for
VESTA visualization and how realistically ABACUS can provide the required
input.  The focus is practical project planning, not a complete Multiwfn
manual.

## Evidence Snapshot

Multiwfn evidence:

- Local version: `tools/Multiwfn_2026.6.2_*`.
- Real-space function menu in `function.f90` lists electron density,
  gradient norm, Laplacian, orbital wavefunction, orbital density, ELF, LOL,
  ESP, RDG, promolecular RDG, IRI, vdW potential, and other grid functions.
- Multiwfn `function.f90`/`0123dim.f90` explicitly list Hamiltonian and
  Lagrangian kinetic energy densities as functions `6` and `7`, exporting
  `K(r).cub` and `G(r).cub`; ALIE is function `18`, exporting
  `avglocion.cub`.
- Weak-interaction module `visweak.f90` exports `sl2r.cub`, `dg_inter.cub`,
  `dg_intra.cub`, `dg.cub`, `avgRDG.cub`, `avgsl2r.cub`, and related scatter
  data.
- AIM topology module `topology.f90` exports `CPs.pdb`, `paths.pdb`,
  `CPprop.txt`, and path/CP summaries.
- Bundled scripts show intended visual products: `showorb.vmd`,
  `showcub.vmd`, `AIM.vmd`, `ALIE.vmd`, `molsurfmap.vmd`,
  `local_EA/*.vmd`, and `vdWpot/vdWpot.vmd`.
- Bundled ALIE/LEA/LEAE/vdW surface scripts use the same VESTA-compatible
  pattern: a density/surface cube plus a mapped-property texture cube, with
  optional `surfanalysis.pdb` extrema points.
- Multiwfn `surfana.f90` writes `surfanalysis.pdb` from molecular surface
  analysis post-processing.  Carbon records are surface maxima, oxygen records
  are surface minima, and the PDB B-factor field stores the mapped function
  value when available.

ABACUS evidence:

- Latest checked remote: `deepmodeling/abacus-develop` `origin/develop`
  `707f09266842c3340a0d5f7a21d3224306aafd58` on 2026-06-10.
- Molden converter moved at ABACUS commit
  `19511fd68bebb5fb44b5d7d89bd1d7262023df34` to
  `interfaces/Multiwfn_interface/molden.py`.
- Latest converter writes `[Cell]`, `[Atoms] AU`, `[GTO]`, `[MO]`, and by
  default `[Nval]`; optional `[Pseudo]` is available.
- Latest converter explicitly restricts the Molden route to LCAO, `nspin=1`
  or `nspin=2`, and one Gamma/single k point.  It rejects `nspin=4/SOC`
  spinor wavefunctions and raises on non-single-k `KPT`.
- ABACUS documentation exposes direct cube outputs: `out_chg`, `out_pot`,
  `out_pchg`, `out_wfc_norm`, `out_wfc_re_im`, and `out_elf`.
- ABACUS latest `origin/develop` Mulliken output writes `mulliken.txt` blocks
  headed by `--- Ionic Step N ---`; each atom block records
  `Atom N is LABEL`, `total charge on atom N`, and for spinful calculations
  `total magnetism on atom N`.

Local smoke evidence:

- ABACUS Ag(111)+benzene Molden with `[Nval]`:
  `smoke/abacus_server_artifacts_20260606/ag111_benzene/ag111_benzene_lcao_cont3_nval.molden`.
- Multiwfn IGMH from ABACUS Molden produced `dg_inter.cub` and `sl2r.cub`.
- Multiwfn AIM from ABACUS Molden produced AIM CP/path PDBs and VESTA overlay
  products under `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/`.
- Multiwfn noGUI IRI/RDG from H2O FCHK produced raw `func1.cub`/`func2.cub`,
  processed `h2o_IRI1.cub`/`h2o_IRI2.cub`, and `h2o_iri_cube.vesta` under
  `smoke/multiwfn_iri_run_smoke_20260610/`.
- Multiwfn noGUI IGMH from H2O FCHK, fragments `1` and `2-3`, grid
  `8 x 8 x 8`, produced `dg_inter.cub`, `sl2r.cub`, optional
  `dg_intra.cub`/`dg.cub`, and `h2o_igmh_cube.vesta` under
  `smoke/multiwfn_igmh_run_smoke_20260610/h2o/`.

## ABACUS Input Routes

| Route | ABACUS requirement | Multiwfn/VESTA use | Status |
| --- | --- | --- | --- |
| Latest LCAO Molden | `basis_type lcao`, `out_wfc_lcao 1`, Gamma/single k, `nspin=1/2`, current `interfaces/Multiwfn_interface/molden.py` | Full Multiwfn wavefunction analyses: AIM, IGMH, IRI/RDG, ELF/LOL, orbitals, density-derived functions | Highest priority |
| ABACUS charge cube | `out_chg 1`; current files include `chgs*.cube`; older docs mention `SPIN*_CHG.cube` | VESTA density isosurfaces/slices; Multiwfn grid post-processing only | Direct VESTA route |
| ABACUS potential cube | `out_pot 1` for local potential `pots*.cube`, `out_pot 2` for electrostatic `pot_es.cube`, `out_pot 3` for initial potential too | VESTA potential maps/slices/isosurfaces; surface context | Direct VESTA route |
| ABACUS partial charge cube | `calculation get_pchg`, `out_pchg` state mask | Band/state density isosurfaces, STM-like images | Good VESTA route |
| ABACUS real-space wavefunction cube | `calculation get_wf`, `out_wfc_norm` or `out_wfc_re_im` | Band wavefunction magnitude or real/imaginary isosurfaces | Good VESTA route; `cube-preset orbital` uses signed positive/negative surfaces |
| ABACUS ELF cube | `out_elf` | ELF isosurfaces without Multiwfn | Good direct route; `cube-preset elf` is implemented |
| ABACUS Mulliken | `out_mul 1`, produces `mulliken.txt` | Per-atom scalar coloring in VESTA | Implemented as `multiwfn2vesta abacus-mulliken-color` |
| ABACUS density matrices | `out_dmk` or `out_dmr` | Possible future population/bond/order tooling, not directly VESTA | Lower priority |

Important constraint: ABACUS cube-only routes are not a replacement for a full
Molden wavefunction.  They support VESTA visualization and Multiwfn grid-data
processing, but not wavefunction analyses such as AIM/IGMH that need orbitals,
occupations, and density derivatives from the wavefunction representation.

## Analysis Priority Matrix

### P0: Build First

| Analysis | Multiwfn input | ABACUS feasibility | Multiwfn output | VESTA representation | Project action |
| --- | --- | --- | --- | --- | --- |
| Generic cube visualizer | Any `.cub` from Multiwfn or ABACUS | Strong: `out_chg`, `out_pot`, `out_pchg`, `out_wfc_*`, `out_elf` | Cube | Density/texture import, isosurface, section off by default | Implemented as `multiwfn2vesta cube-vesta`; `cube-preset` adds common analysis defaults |
| Molecular orbitals and band wavefunctions | Full wavefunction Molden/FCH/WFN, or ABACUS real-space `get_wf` cubes | Strong for Gamma LCAO Molden; direct cube route for selected bands | `orb*.cub`, `MOvalue.cub`, `orbdens.cub`, or ABACUS `wfi*.cube` | Positive/negative isosurfaces; magnitude as single surface | `cube-preset orbital` implemented; `grid-run --function orbital --orbital ...` covers one MO cube and `grid-run --orbitals ...` covers isolated batch orbital export |
| Electron density, spin density, Laplacian, kinetic density | Full wavefunction, or ABACUS density cubes for density only | Strong for density cube; Molden route for derivatives | `density.cub`, `spindensity.cub`, `laplacian.cub`, `K(r).cub`, `G(r).cub` | Single/positive-negative isosurfaces or slices | `grid-run` now covers density, spin density, Laplacian, and K(r)/G(r) single cubes |
| ELF/LOL | Full wavefunction; ABACUS direct `out_elf` for ELF | Strong for ELF direct; Molden route for Multiwfn ELF/LOL | `ELF.cub`, `LOL.cub`, ABACUS `elf*.cube` | Isosurfaces around localized regions | `grid-run` now covers Multiwfn ELF/LOL; `cube-preset elf/lol` remains the VESTA writer |
| AIM/QTAIM topology | Full wavefunction Molden/FCH/WFN/WFX | Feasible for Gamma LCAO Molden with `[Nval]`; validated on Ag(111)+benzene | `CPs.pdb`, `paths.pdb`, `CPprop.txt`, `mol.pdb` | Atoms-only pseudo-sites, no AIM bonds, optional labels | Already partly implemented; add ABACUS-aware recipes |
| IGMH + AIM overlay | Full wavefunction and fragment definitions | Feasible for Gamma LCAO Molden; validated on Ag(111)+benzene | `dg_inter.cub`, `sl2r.cub`, AIM PDBs | Multi-phase VESTA density/texture plus AIM pseudo-sites | `igmh-run` now automates the standard Multiwfn IGMH fragment stream and calls `cube-preset igmh`; saved AIM+IGMH overlay styling is implemented |

### P1: High Value, Needs More Glue

| Analysis | Multiwfn input | ABACUS feasibility | Multiwfn output | VESTA representation | Project action |
| --- | --- | --- | --- | --- | --- |
| IRI/NCI/RDG | Full wavefunction, or promolecular approximation from structure | Molden route feasible; promolecular route can avoid wavefunction | `IRI.cub`, `RDG.cub`, `sl2r.cub`, `func1.cub`, `func2.cub` | Isosurface plus texture cube; section planes off | `multiwfn2vesta iri-run` implemented for the two-cube weak-interaction stream; `grid-run` can also export single RDG/IRI/sign(lambda2)rho cubes |
| ESP/MEP on density surface | Full wavefunction or ABACUS `out_pot` plus density cube | Strong direct cube route; Molden route for Multiwfn ESP | `density.cub`, `totesp.cub`, `pot_es.cube`, `pots*.cube` | Density isosurface colored by potential texture | `grid-run --function esp` can export Multiwfn ESP; `cube-preset esp` still combines density surface plus potential texture |
| Molecular surface mapped properties | Full wavefunction or cube pair | Feasible through Molden; ABACUS can provide density/potential cubes | `surf.cub`, `mapfunc.cub`, `density.cub`, `avglocion.cub`, `surfanalysis.pdb` | Surface cube plus texture; extrema as atoms-only overlay phase | `cube-preset surface-map` covers surface+texture display using `molsurfmap.vmd` defaults; `--surfanalysis-pdb` and `surface-extrema` overlay surface extrema |
| ALIE / LEA / LEAE | Full wavefunction, occupied/virtual orbitals | Feasible only if ABACUS Molden orbitals/energies are adequate; virtual levels in metals risky | `avglocion.cub`, `userfunc.cub`, `surfanalysis.pdb` | Colored density surface plus extrema points | `cube-preset alie/lea/leae` covers density-surface texture maps and auto-selects minima/maxima extrema overlays from `surfanalysis.pdb` |
| vdW/repulsion/dispersion potential | Structure and/or wavefunction depending option | Feasible, often structure driven | `vdW.cub`, `repul.cub`, `disp.cub`, `density.cub`, `vdWpot.cub` | Potential surfaces/slices, density surface context | `grid-run --function vdw-potential` covers single vdW potential cubes; `cube-preset vdw-map` covers density-surface texture maps |
| Atom scalar coloring | Per-atom values from Multiwfn or ABACUS `mulliken.txt` | Strong for ABACUS `out_mul`; also charges/Fukui from Multiwfn | CSV/table, `mulliken.txt` | Patch `SITET` RGB values | ABACUS Mulliken parser implemented; generic Multiwfn atom table parser implemented as `multiwfn2vesta multiwfn-atom-color` |

### P2: Specialized, Useful Later

| Analysis | Multiwfn input | ABACUS feasibility | Multiwfn output | VESTA representation | Project action |
| --- | --- | --- | --- | --- | --- |
| Basin analysis | Wavefunction or grid data | Molden route possible; accuracy depends on NAO2GTO fit | `basin.cub`, `basin0001.cub`, `basinsel.cub`, attractor PDB/PQR | Separate colored basin isosurfaces | Needs cube splitting/color strategy |
| Excited-state hole/electron/CDD/transition density | Wavefunction plus excited-state information | Not a primary ABACUS ground-state route; LR-TDDFT outputs need separate study | `hole.cub`, `electron.cub`, `CDD.cub`, `transdens.cub` | Positive/negative isosurfaces | Defer until ABACUS excited-state interface is clear |
| ETS-NOCV / AdNDP / EDA-related orbitals | Specialized wavefunctions/fragments | Weak for ABACUS periodic slabs; possible for molecule-like cases | `NOCV_*.cub`, `NOCVpair.cub`, `AdNDPorb*.cub` | Orbital-like positive/negative surfaces | Defer |
| Fukui / dual descriptor | Multiple charge-state wavefunctions or orbital-weighted approximation | Possible for finite molecules or charged supercells; periodic charged systems risky | `userfunc.cub`, density-difference cubes | Positive/negative surfaces and atom scalar coloring | Cube arithmetic bottom layer implemented as `multiwfn2vesta cube-arith`; charged-state cube generation remains separate |
| NICS/current/arrows | Magnetic-response data | Not main maintained route | vector/text data, if available | Arrows/text overlays | Keep as misc, not main code |

## ABACUS Molden Rules

Use latest ABACUS `interfaces/Multiwfn_interface/molden.py`, not the older
`tools/molden/molden.py` path.

Recommended ABACUS settings for the Molden route:

```text
basis_type lcao
gamma_only 1
out_wfc_lcao 1
```

The converter requires `STRU`, `INPUT`, `KPT`, the corresponding `OUT.*`
directory, UPF pseudopotentials, and orbital files.  Use the maintained
project wrapper:

```bash
multiwfn2vesta abacus-molden \
  /path/to/abacus/calc \
  /path/to/ABACUS_Multiwfn.molden
```

The wrapper exports `interfaces/Multiwfn_interface/molden.py` from the
selected ABACUS git ref, records source path/commit/SHA256, runs the converter
with an absolute `-o`, writes stdout/stderr logs and a recipe, and validates
the output with `molden-check --abacus`.

The ABACUS converter is a Python script that imports `numpy`, `scipy`, and
`matplotlib`.  The maintained wrapper checks those imports before launching
the converter; use `--python /path/to/python` when the default Python
environment is not the scientific environment used for ABACUS post-processing.

Default behavior now writes `[Cell]` and `[Nval]`.  Keep `[Nval]` enabled for
pseudopotential systems.  Without `[Nval]`, Multiwfn may interpret valence
pseudopotential wavefunctions with all-electron nuclear charges, which breaks
charge-sensitive AIM/IGMH/ESP analysis.

Known limitations:

- Only LCAO is supported.
- Only `nspin=1/2` is supported; `nspin=4` and SOC spinors are rejected.
- Only one Gamma/single k point is supported by the KPT parser.
- NAO2GTO is an approximation.  Near-nucleus quantities, heavy elements, CP
  values, and quantitative electron counts should be treated conservatively.
- Metals and smeared occupations can confuse HOMO/LUMO-style interpretation.
  Prefer density/interaction visualization over frontier-orbital narratives
  for metal slabs.

## Recommended Development Roadmap

1. Extend the generic `cube-vesta`/`cube-preset` CLI with more real-system
   templates and optional render hooks.  Core analysis display presets now
   exist, including ALIE/LEA/LEAE/vdW surface-map presets and
   `surfanalysis.pdb` extrema overlays; the remaining work is coverage,
   optional render hooks, and richer real-system templates.
2. Extend the implemented `abacus-molden` wrapper with more real-calculation
   smoke coverage and optional copy-to-scratch handling for converter
   side-products.
3. Extend the implemented `iri-run` command stream to more real IRI/RDG/NCI
   templates and downstream chaining; use `grid-run --function esp` plus
   `cube-preset esp` for Multiwfn ESP-on-density templates.
4. Add more atom-scalar parsers.  ABACUS `mulliken.txt` now feeds VESTA atom
   coloring directly, and generic Multiwfn atom tables now feed the same
   backend through `multiwfn2vesta multiwfn-atom-color`.  Remaining work is
   more specialized parsers for raw Multiwfn menu transcripts when they prove
   stable enough to support directly.
5. Extend `grid-run` beyond the initial main-function-5 table where useful:
   more real-system orbital batch smokes, possible future Multiwfn main
   function `200` integration if it proves more reliable than repeated
   isolated runs, end-to-end Fukui/dual-descriptor cube generation on shared
   grids.  K(r)/G(r), ALIE, and
   promolecular RDG/sign(lambda2)rho table entries are now maintained.  The
   cube arithmetic foundation for density-difference/Fukui/dual-descriptor
   maps now exists as `multiwfn2vesta cube-arith`.
6. Extend `igmh-run` beyond the standard IGMH stream if needed: IGM, mIGM,
   aIGM, and more real ABACUS slab smokes should be added only after their
   prompt streams are stable.
7. Keep headless/no-focus VESTA rendering as a separate backend concern.
   Visualization products should remain useful as `.vesta` even when rendering
   is skipped.

## Current Project Coverage

Implemented or partly implemented:

- `multiwfn2vesta discover`
- `multiwfn2vesta abacus-molden`
- `multiwfn2vesta cube-vesta`
- `multiwfn2vesta cube-preset`
- `multiwfn2vesta cube-arith`
- `multiwfn2vesta iri-run`
- `multiwfn2vesta igmh-run`
- `multiwfn2vesta grid-run`
- `multiwfn2vesta aim-run`
- `multiwfn2vesta aim-pdb`
- `multiwfn2vesta aim-igmh`
- IRI color cube scalar remapping helpers and the maintained Multiwfn
  IRI/RDG runner
- K(r)/G(r), ALIE, and promolecular RDG/sign(lambda2)rho entries in the
  maintained `grid-run` function table
- ALIE/LEA/LEAE, generic molecular surface-map, and vdW density-surface
  texture presets in `cube-preset`
- VESTA atom scalar RGB patching
- ABACUS `mulliken.txt` charge/magnetism atom coloring
- Generic Multiwfn atom scalar table coloring
- VESTA camera/layer/three-view utilities

Main gaps:

- Generic cube-to-VESTA CLI now exists as `multiwfn2vesta cube-vesta`, and
  common analysis defaults now exist as `multiwfn2vesta cube-preset`;
  remaining work is real-system smoke/template coverage and optional render
  hooks.
- ABACUS Molden wrapper now exists; remaining work is real-system smoke
  coverage and tighter integration with downstream Multiwfn command streams.
- Generic Multiwfn atom table parsing now exists for CSV/TSV/whitespace
  tables; remaining work is direct parsers for specialized raw Multiwfn menu
  transcripts.
- Maintained Multiwfn command streams now exist for AIM, IRI/RDG, and
  IGMH, plus main-function-5 grid cubes as `multiwfn2vesta grid-run`,
  including repeated isolated batch orbital/orbital-density export through
  `--orbitals`.  Remaining gaps are higher-level Fukui/dual-descriptor
  generation, IGM/mIGM/aIGM command streams, molecular-surface extrema
  overlays, and more real-system templates.
- Dual-cube surface texture workflows now have a preset entry point for
  IRI/RDG/NCI, IGM/IGMH/aIGM, ESP/MEP, ALIE/LEA/LEAE, generic surface maps,
  and vdW maps.  Standard IGMH now has an end-to-end fragment runner; IGM,
  mIGM, and aIGM still need their own maintained prompt streams.
- Fukui/dual-descriptor visualization now has the cube-arithmetic bottom
  layer, but still needs higher-level charged-state generation templates and
  real chemistry smoke cases.
