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
- Weak-interaction module `visweak.f90` exports `sl2r.cub`, `dg_inter.cub`,
  `dg_intra.cub`, `dg.cub`, `avgRDG.cub`, `avgsl2r.cub`, and related scatter
  data.
- AIM topology module `topology.f90` exports `CPs.pdb`, `paths.pdb`,
  `CPprop.txt`, and path/CP summaries.
- Bundled scripts show intended visual products: `showorb.vmd`,
  `showcub.vmd`, `AIM.vmd`, `ALIE.vmd`, `molsurfmap.vmd`,
  `local_EA/*.vmd`, and `vdWpot/vdWpot.vmd`.

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

Local smoke evidence:

- ABACUS Ag(111)+benzene Molden with `[Nval]`:
  `smoke/abacus_server_artifacts_20260606/ag111_benzene/ag111_benzene_lcao_cont3_nval.molden`.
- Multiwfn IGMH from ABACUS Molden produced `dg_inter.cub` and `sl2r.cub`.
- Multiwfn AIM from ABACUS Molden produced AIM CP/path PDBs and VESTA overlay
  products under `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/`.

## ABACUS Input Routes

| Route | ABACUS requirement | Multiwfn/VESTA use | Status |
| --- | --- | --- | --- |
| Latest LCAO Molden | `basis_type lcao`, `out_wfc_lcao 1`, Gamma/single k, `nspin=1/2`, current `interfaces/Multiwfn_interface/molden.py` | Full Multiwfn wavefunction analyses: AIM, IGMH, IRI/RDG, ELF/LOL, orbitals, density-derived functions | Highest priority |
| ABACUS charge cube | `out_chg 1`; current files include `chgs*.cube`; older docs mention `SPIN*_CHG.cube` | VESTA density isosurfaces/slices; Multiwfn grid post-processing only | Direct VESTA route |
| ABACUS potential cube | `out_pot 1` for local potential `pots*.cube`, `out_pot 2` for electrostatic `pot_es.cube`, `out_pot 3` for initial potential too | VESTA potential maps/slices/isosurfaces; surface context | Direct VESTA route |
| ABACUS partial charge cube | `calculation get_pchg`, `out_pchg` state mask | Band/state density isosurfaces, STM-like images | Good VESTA route |
| ABACUS real-space wavefunction cube | `calculation get_wf`, `out_wfc_norm` or `out_wfc_re_im` | Band wavefunction magnitude or real/imaginary isosurfaces | Good VESTA route |
| ABACUS ELF cube | `out_elf` | ELF isosurfaces without Multiwfn | Good direct route |
| ABACUS Mulliken | `out_mul 1`, produces `mulliken.txt` | Per-atom scalar coloring in VESTA | Needs parser/glue |
| ABACUS density matrices | `out_dmk` or `out_dmr` | Possible future population/bond/order tooling, not directly VESTA | Lower priority |

Important constraint: ABACUS cube-only routes are not a replacement for a full
Molden wavefunction.  They support VESTA visualization and Multiwfn grid-data
processing, but not wavefunction analyses such as AIM/IGMH that need orbitals,
occupations, and density derivatives from the wavefunction representation.

## Analysis Priority Matrix

### P0: Build First

| Analysis | Multiwfn input | ABACUS feasibility | Multiwfn output | VESTA representation | Project action |
| --- | --- | --- | --- | --- | --- |
| Generic cube visualizer | Any `.cub` from Multiwfn or ABACUS | Strong: `out_chg`, `out_pot`, `out_pchg`, `out_wfc_*`, `out_elf` | Cube | Density/texture import, isosurface, section off by default | Add reusable VESTA cube style/template CLI |
| Molecular orbitals and band wavefunctions | Full wavefunction Molden/FCH/WFN, or ABACUS real-space `get_wf` cubes | Strong for Gamma LCAO Molden; direct cube route for selected bands | `orb*.cub`, `MOvalue.cub`, `orbdens.cub`, or ABACUS `wfi*.cube` | Positive/negative isosurfaces; magnitude as single surface | Add `orbital-cube` and `cube-vesta` workflows |
| Electron density, spin density, Laplacian, kinetic density | Full wavefunction, or ABACUS density cubes for density only | Strong for density cube; Molden route for derivatives | `density.cub`, `spindensity.cub`, `laplacian.cub`, `K(r).cub`, `G(r).cub` | Single/positive-negative isosurfaces or slices | Add generic scalar cube presets |
| ELF/LOL | Full wavefunction; ABACUS direct `out_elf` for ELF | Strong for ELF direct; Molden route for Multiwfn ELF/LOL | `ELF.cub`, `LOL.cub`, ABACUS `elf*.cube` | Isosurfaces around localized regions | Add ELF preset and ABACUS direct input route |
| AIM/QTAIM topology | Full wavefunction Molden/FCH/WFN/WFX | Feasible for Gamma LCAO Molden with `[Nval]`; validated on Ag(111)+benzene | `CPs.pdb`, `paths.pdb`, `CPprop.txt`, `mol.pdb` | Atoms-only pseudo-sites, no AIM bonds, optional labels | Already partly implemented; add ABACUS-aware recipes |
| IGMH + AIM overlay | Full wavefunction and fragment definitions | Feasible for Gamma LCAO Molden; validated on Ag(111)+benzene | `dg_inter.cub`, `sl2r.cub`, AIM PDBs | Multi-phase VESTA density/texture plus AIM pseudo-sites | Already implemented for saved overlays; automate Multiwfn command streams next |

### P1: High Value, Needs More Glue

| Analysis | Multiwfn input | ABACUS feasibility | Multiwfn output | VESTA representation | Project action |
| --- | --- | --- | --- | --- | --- |
| IRI/NCI/RDG | Full wavefunction, or promolecular approximation from structure | Molden route feasible; promolecular route can avoid wavefunction | `IRI.cub`, `RDG.cub`, `sl2r.cub`, `func1.cub`, `func2.cub` | Isosurface plus texture cube; section planes off | Existing IRI cube code; generalize to NCI/RDG |
| ESP/MEP on density surface | Full wavefunction or ABACUS `out_pot` plus density cube | Strong direct cube route; Molden route for Multiwfn ESP | `density.cub`, `totesp.cub`, `pot_es.cube`, `pots*.cube` | Density isosurface colored by potential texture | Add dual-cube surface mapping presets |
| Molecular surface mapped properties | Full wavefunction or cube pair | Feasible through Molden; ABACUS can provide density/potential cubes | `surf.cub`, `mapfunc.cub`, `density.cub`, `avglocion.cub`, `surfanalysis.pdb` | Surface cube plus texture; extrema as pseudo-sites | Extend VESTA texture and point overlay code |
| ALIE / LEA / LEAE | Full wavefunction, occupied/virtual orbitals | Feasible only if ABACUS Molden orbitals/energies are adequate; virtual levels in metals risky | `avglocion.cub`, `userfunc.cub`, `surfanalysis.pdb` | Colored density surface plus extrema points | Prototype on molecules/insulators first |
| vdW/repulsion/dispersion potential | Structure and/or wavefunction depending option | Feasible, often structure driven | `vdW.cub`, `repul.cub`, `disp.cub`, `density.cub` | Potential surfaces/slices, density surface context | Add low-risk cube preset |
| Atom scalar coloring | Per-atom values from Multiwfn or ABACUS `mulliken.txt` | Strong for ABACUS `out_mul`; also charges/Fukui from Multiwfn | CSV/table, `mulliken.txt` | Patch `SITET` RGB values | Parser for ABACUS Mulliken is next useful small feature |

### P2: Specialized, Useful Later

| Analysis | Multiwfn input | ABACUS feasibility | Multiwfn output | VESTA representation | Project action |
| --- | --- | --- | --- | --- | --- |
| Basin analysis | Wavefunction or grid data | Molden route possible; accuracy depends on NAO2GTO fit | `basin.cub`, `basin0001.cub`, `basinsel.cub`, attractor PDB/PQR | Separate colored basin isosurfaces | Needs cube splitting/color strategy |
| Excited-state hole/electron/CDD/transition density | Wavefunction plus excited-state information | Not a primary ABACUS ground-state route; LR-TDDFT outputs need separate study | `hole.cub`, `electron.cub`, `CDD.cub`, `transdens.cub` | Positive/negative isosurfaces | Defer until ABACUS excited-state interface is clear |
| ETS-NOCV / AdNDP / EDA-related orbitals | Specialized wavefunctions/fragments | Weak for ABACUS periodic slabs; possible for molecule-like cases | `NOCV_*.cub`, `NOCVpair.cub`, `AdNDPorb*.cub` | Orbital-like positive/negative surfaces | Defer |
| Fukui / dual descriptor | Multiple charge-state wavefunctions or orbital-weighted approximation | Possible for finite molecules or charged supercells; periodic charged systems risky | `userfunc.cub`, density-difference cubes | Positive/negative surfaces and atom scalar coloring | Defer; implement as cube arithmetic first |
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
directory, UPF pseudopotentials, and orbital files.  For current develop:

```bash
python interfaces/Multiwfn_interface/molden.py \
  -f /path/to/abacus/calc \
  -o ABACUS_Multiwfn.molden
```

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

1. Add a generic `cube-vesta` CLI that accepts one density cube and optional
   texture cube, turns off `SECTS`, sets `ISURF`, patches `TEX3P`, copies cube
   dependencies, and optionally renders three views.
2. Add ABACUS-oriented discovery/docs for the latest
   `interfaces/Multiwfn_interface/molden.py` and validate `[Nval]` in input
   Molden headers before running Multiwfn wavefunction analyses.
3. Generalize current IRI color-cube logic to NCI/RDG/ESP mapped surfaces.
4. Add parsers that convert ABACUS `mulliken.txt` and Multiwfn atom tables into
   the existing VESTA atom scalar coloring CSV format.
5. Add command-stream wrappers for Multiwfn orbital cube, density/ELF/LOL cube,
   IRI/RDG, and IGMH fragment workflows, following the existing `aim-run`
   logging pattern.
6. Keep headless/no-focus VESTA rendering as a separate backend concern.
   Visualization products should remain useful as `.vesta` even when rendering
   is skipped.

## Current Project Coverage

Implemented or partly implemented:

- `multiwfn2vesta discover`
- `multiwfn2vesta aim-run`
- `multiwfn2vesta aim-pdb`
- `multiwfn2vesta aim-igmh`
- IRI color cube scalar remapping helpers
- VESTA atom scalar RGB patching
- VESTA camera/layer/three-view utilities

Main gaps:

- No generic cube-to-VESTA CLI yet.
- No direct ABACUS Molden converter wrapper yet.
- No ABACUS `mulliken.txt` parser yet.
- No maintained Multiwfn command streams for orbital/density/ELF/RDG/IRI cube
  generation outside AIM.
- Dual-cube surface texture workflows are still reverse-engineered from smoke
  tests and need a cleaner template API.
