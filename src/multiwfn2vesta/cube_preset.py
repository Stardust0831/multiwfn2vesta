"""Analysis-oriented presets for cube-to-VESTA workflows."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from . import cube_vesta, surface_extrema_vesta


RGB = Tuple[int, int, int]


@dataclass(frozen=True)
class CubePreset:
    name: str
    aliases: Tuple[str, ...]
    description: str
    surface_mode: str
    isosurface: float
    positive_rgb: RGB = (255, 255, 0)
    negative_rgb: RGB = (0, 80, 255)
    surface_opacity: Tuple[int, int] = (127, 255)
    tex_physical: Optional[Tuple[float, float]] = None
    tex_range_source: str = "full-cube"
    texture_required: bool = False
    structure: str = "auto"
    sections: str = "off"
    notes: str = ""


PRESETS: Tuple[CubePreset, ...] = (
    CubePreset(
        name="density",
        aliases=("rho", "charge-density", "scalar"),
        description="Single positive isosurface for density-like scalar cubes.",
        surface_mode="single",
        isosurface=0.01,
        positive_rgb=(255, 220, 80),
        notes="Use for ABACUS out_chg cubes or Multiwfn electron-density cubes.",
    ),
    CubePreset(
        name="gradient-norm",
        aliases=("gradient", "rho-gradient", "grad-rho", "density-gradient-norm"),
        description="Single positive isosurface for electron-density gradient norm cubes.",
        surface_mode="single",
        isosurface=0.05,
        positive_rgb=(120, 210, 255),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn gradient.cub from real-space function 2. "
            "Multiwfn does not reset sur_value for this function, so the default follows "
            "the global main-function-5 sur_value=0.05 and usually needs system-specific tuning."
        ),
    ),
    CubePreset(
        name="signed",
        aliases=("orbital", "mo", "wavefunction", "abacus-wfc", "density-difference", "dual-descriptor"),
        description="Positive/negative isosurfaces for signed real scalar cubes.",
        surface_mode="signed",
        isosurface=0.02,
        notes="Use for molecular orbitals, real wavefunction cubes, density differences, or dual-descriptor cubes.",
    ),
    CubePreset(
        name="spin-density",
        aliases=("spin", "spindensity", "magnetization-density", "spin-polarization-density"),
        description="Positive/negative isosurfaces for alpha-minus-beta spin density cubes.",
        surface_mode="signed",
        isosurface=0.02,
        positive_rgb=(255, 80, 80),
        negative_rgb=(70, 130, 255),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn spindensity.cub or compatible signed spin-density cubes; "
            "positive and negative signs follow the source cube convention. "
            "The default magnitude follows Multiwfn main-function-5 sur_value for spin density."
        ),
    ),
    CubePreset(
        name="spin-polarization",
        aliases=("spin-polarization-parameter", "spin-pol", "spin-polarisation"),
        description="Positive/negative isosurfaces for dimensionless spin polarization parameter cubes.",
        surface_mode="signed",
        isosurface=0.5,
        positive_rgb=(255, 95, 80),
        negative_rgb=(80, 145, 255),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn function 5 spindensity.cub generated with ipolarpara=1. "
            "The field is (rho_alpha-rho_beta)/(rho_alpha+rho_beta), so it is normally "
            "dimensionless and bounded near +/-1 where the total density is meaningful."
        ),
    ),
    CubePreset(
        name="orbital-density",
        aliases=("orbdens", "mo-density", "orbital-density-cube"),
        description="Single positive isosurface for orbital density cubes.",
        surface_mode="single",
        isosurface=0.005,
        positive_rgb=(180, 140, 255),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn orbdens.cub from real-space function 44; "
            "the default isosurface follows Multiwfn main-function-5 sur_value."
        ),
    ),
    CubePreset(
        name="laplacian",
        aliases=("lap", "laplacian-rho", "laplacian-density"),
        description="Positive/negative isosurfaces for the Laplacian of electron density.",
        surface_mode="signed",
        isosurface=0.05,
        positive_rgb=(255, 165, 40),
        negative_rgb=(60, 130, 255),
        surface_opacity=(125, 255),
        notes=(
            "Use for Multiwfn laplacian.cub from real-space function 3; "
            "the sign convention is the raw Laplacian of rho and the isosurface often needs system-specific tuning."
        ),
    ),
    CubePreset(
        name="hamiltonian-ked",
        aliases=("k-r", "k(r)", "kinetic-k", "hamiltonian-kinetic-density", "ked-k"),
        description="Positive/negative isosurfaces for Hamiltonian kinetic energy density K(r).",
        surface_mode="signed",
        isosurface=0.01,
        positive_rgb=(255, 195, 55),
        negative_rgb=(80, 110, 255),
        surface_opacity=(130, 255),
        notes=(
            "Use for Multiwfn K(r).cub from real-space function 6; "
            "K(r) can be signed, so positive and negative isosurfaces are shown by default."
        ),
    ),
    CubePreset(
        name="lagrangian-ked",
        aliases=("g-r", "g(r)", "kinetic-g", "lagrangian-kinetic-density", "ked-g"),
        description="Single positive isosurface for Lagrangian kinetic energy density G(r).",
        surface_mode="single",
        isosurface=0.01,
        positive_rgb=(90, 210, 150),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn G(r).cub from real-space function 7; "
            "G(r) is normally nonnegative and is displayed as a single positive scalar field."
        ),
    ),
    CubePreset(
        name="kinetic-energy-density",
        aliases=(
            "positive-ked",
            "ked",
            "ked-scalar",
            "thomas-fermi-ked",
            "tf-ked",
            "weizsacker-ked",
            "weizsaecker-ked",
            "von-weizsacker-ked",
            "vw-ked",
            "pauli-ked",
        ),
        description="Single positive isosurface for selected kinetic-energy-density variants.",
        surface_mode="single",
        isosurface=0.01,
        positive_rgb=(120, 220, 130),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn function-100 userfunc.cub routes that export selected "
            "KED variants such as Thomas-Fermi, Weizsacker, and Pauli kinetic energy density. "
            "These are normally displayed as positive scalar fields; inspect the range and "
            "tune the isosurface per system."
        ),
    ),
    CubePreset(
        name="steric-energy-density",
        aliases=("steric-density", "steric-energy", "steric-ked"),
        description="Single positive isosurface for Multiwfn steric energy density cubes.",
        surface_mode="single",
        isosurface=0.01,
        positive_rgb=(145, 220, 130),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn function-100 userfunc.cub with iuserfunc=40. "
            "The local source maps this route to weizsacker(x,y,z), i.e. a positive "
            "steric/Weizsacker-like energy-density field.  Inspect the range and tune "
            "the isosurface for the selected system."
        ),
    ),
    CubePreset(
        name="sbl-energy-density",
        aliases=(
            "sbl-electrostatic-energy-density",
            "sbl-quantum-energy-density",
            "sbl-quantum-energy-density-lagrangian",
            "sbl-total-energy-density",
            "sbl-energy",
            "sbl-density",
        ),
        description="Signed isosurfaces for SBL energy-decomposition density cubes.",
        surface_mode="signed",
        isosurface=0.05,
        positive_rgb=(255, 190, 75),
        negative_rgb=(80, 135, 255),
        surface_opacity=(135, 255),
        notes=(
            "Use for Multiwfn function-100 SBL energy-density userfunc.cub routes: "
            "iuserfunc=68 for electronic electrostatic energy density, 69/-69 for "
            "Hamiltonian/Lagrangian quantum energy density, and 110 for total SBL "
            "energy density.  These fields may be signed, so the default writes +/-0.05 "
            "surfaces and should be retuned after inspecting the cube range."
        ),
    ),
    CubePreset(
        name="sbl-potential",
        aliases=(
            "steric-potential",
            "pauli-potential",
            "quantum-potential",
            "sbl-total-potential",
            "sbl-pot",
        ),
        description="Signed isosurfaces for steric/Pauli/quantum/SBL potential cubes.",
        surface_mode="signed",
        isosurface=0.05,
        positive_rgb=(255, 115, 75),
        negative_rgb=(70, 130, 255),
        surface_opacity=(135, 255),
        notes=(
            "Use for Multiwfn function-100 potential-style userfunc.cub routes: "
            "iuserfunc=41 steric potential, 60 Pauli potential, 63 quantum potential, "
            "and 111 total SBL potential.  The standalone preset is signed; for "
            "surface coloring, use the corresponding grid-run route with --surface-cube "
            "and tune --tex-physical."
        ),
    ),
    CubePreset(
        name="sbl-force-magnitude",
        aliases=(
            "force-magnitude",
            "steric-force-magnitude",
            "pauli-force-magnitude",
            "quantum-force-magnitude",
            "electrostatic-force-magnitude",
            "sbl-total-force-magnitude",
        ),
        description="Single positive isosurface for force-magnitude diagnostic cubes.",
        surface_mode="single",
        isosurface=0.05,
        positive_rgb=(110, 210, 255),
        surface_opacity=(135, 255),
        notes=(
            "Use for Multiwfn function-100 force-magnitude userfunc.cub routes: "
            "iuserfunc=43 steric, 61 Pauli, 64 quantum, 66 electrostatic, and 112 "
            "total SBL force magnitude.  These fields are nonnegative diagnostic "
            "magnitudes and usually need system-specific isosurface tuning."
        ),
    ),
    CubePreset(
        name="sbl-charge",
        aliases=(
            "steric-charge",
            "pauli-charge",
            "quantum-charge",
            "electrostatic-charge",
            "sbl-total-charge",
        ),
        description="Signed isosurfaces for steric/Pauli/quantum/electrostatic/SBL charge cubes.",
        surface_mode="signed",
        isosurface=0.05,
        positive_rgb=(255, 205, 75),
        negative_rgb=(75, 145, 255),
        surface_opacity=(135, 255),
        notes=(
            "Use for Multiwfn function-100 charge-style userfunc.cub routes: "
            "iuserfunc=42 steric charge, 62 Pauli charge, 65 quantum charge, "
            "67 electrostatic charge, and 113 total SBL charge.  These are signed "
            "Laplacian-derived diagnostics; inspect the range before final figures."
        ),
    ),
    CubePreset(
        name="potential",
        aliases=("potential-cube", "abacus-potential", "out-pot", "local-potential", "pot-es", "mep-cube"),
        description="Positive/negative isosurfaces for direct potential cubes.",
        surface_mode="signed",
        isosurface=0.05,
        positive_rgb=(255, 90, 60),
        negative_rgb=(60, 120, 255),
        surface_opacity=(120, 255),
        notes=(
            "Use for direct ABACUS out_pot cubes such as pots*.cube or pot_es.cube, "
            "or other signed potential scalar fields. For potential mapped on a density surface, use preset `esp`."
        ),
    ),
    CubePreset(
        name="electron-esp",
        aliases=(
            "electronic-esp",
            "electron-mep",
            "electronic-mep",
            "electron-electrostatic-potential",
            "electronic-electrostatic-potential",
        ),
        description="Single negative isosurface for electrostatic potential from electrons only.",
        surface_mode="single",
        isosurface=-0.05,
        positive_rgb=(70, 125, 255),
        surface_opacity=(130, 255),
        notes=(
            "Use for Multiwfn function-100 userfunc.cub with iuserfunc=14. "
            "Multiwfn evaluates the electron contribution to ESP through eleesp(x,y,z), "
            "which is normally negative for the usual electrostatic-potential convention. "
            "The standalone preset therefore uses a single -0.05 a.u. isosurface; "
            "because this is a single-surface preset, color overrides use --positive-rgb. "
            "For density-surface texture maps, use `grid-run --function electron-esp --surface-cube density.cub` "
            "and tune --tex-physical for the selected system."
        ),
    ),
    CubePreset(
        name="positive-esp",
        aliases=("positive-mep", "esp-positive", "mep-positive", "esp-pos", "mep-pos"),
        description="Single positive isosurface for the positive part of electrostatic potential.",
        surface_mode="single",
        isosurface=0.05,
        positive_rgb=(255, 95, 60),
        surface_opacity=(130, 255),
        notes=(
            "Use for Multiwfn function-100 userfunc.cub with iuserfunc=101. "
            "The source clips total ESP below zero, leaving only positive potential regions. "
            "For potential mapped on a density surface, use preset `surface-map` or `esp` "
            "with an explicit texture cube."
        ),
    ),
    CubePreset(
        name="negative-esp",
        aliases=("negative-mep", "esp-negative", "mep-negative", "esp-neg", "mep-neg"),
        description="Single negative isosurface for the negative part of electrostatic potential.",
        surface_mode="single",
        isosurface=-0.05,
        positive_rgb=(65, 125, 255),
        surface_opacity=(130, 255),
        notes=(
            "Use for Multiwfn function-100 userfunc.cub with iuserfunc=102. "
            "The source clips total ESP above zero, leaving only negative potential regions. "
            "Because this is a single-surface preset, color overrides use --positive-rgb."
        ),
    ),
    CubePreset(
        name="electric-field-magnitude",
        aliases=("electric-field", "efield", "e-field", "esp-gradient-magnitude", "mep-gradient-magnitude"),
        description="Single positive isosurface for the magnitude of the electrostatic field.",
        surface_mode="single",
        isosurface=0.05,
        positive_rgb=(120, 210, 255),
        surface_opacity=(135, 255),
        notes=(
            "Use for Multiwfn function-100 userfunc.cub with iuserfunc=103. "
            "Multiwfn obtains the ESP gradient and writes the electric-field magnitude as a nonnegative scalar. "
            "This is useful as a standalone field-strength isosurface or as a texture on a density surface."
        ),
    ),
    CubePreset(
        name="vdw-potential",
        aliases=("vdw", "vdwpot", "vdw-potential-cube", "van-der-waals-potential", "vdw-total-potential"),
        description="Positive/negative isosurfaces for standalone van der Waals potential cubes.",
        surface_mode="signed",
        isosurface=1.0,
        positive_rgb=(255, 120, 60),
        negative_rgb=(70, 150, 255),
        surface_opacity=(130, 255),
        notes=(
            "Use for Multiwfn vdWpot.cub from real-space function 25. "
            "Multiwfn evaluates the UFF van der Waals potential in kcal/mol and sets "
            "main-function-5 sur_value=1.0 for this function. "
            "grid-run defaults the Multiwfn ivdwprobe probe atom to carbon/6 and "
            "accepts --vdw-probe for other elements. "
            "For vdW potential mapped on a density/surface cube, use preset `vdw-map`."
        ),
    ),
    CubePreset(
        name="vdw-repulsion-potential",
        aliases=("vdw-repulsion", "repulsion-potential", "repul", "repul-potential", "repul-cub"),
        description="Single positive isosurface for standalone UFF vdW repulsion potential cubes.",
        surface_mode="single",
        isosurface=1.0,
        positive_rgb=(255, 150, 70),
        surface_opacity=(130, 255),
        notes=(
            "Use for Multiwfn function-100 userfunc.cub with iuserfunc=93, or repul.cub "
            "from the vdW potential module.  Multiwfn evaluates the UFF repulsion "
            "component in kcal/mol; grid-run defaults ivdwprobe to carbon/6 and "
            "accepts --vdw-probe for other elements.  For mapped density/surface "
            "figures, use preset `vdw-map` and tune the texture range per system."
        ),
    ),
    CubePreset(
        name="vdw-dispersion-potential",
        aliases=("vdw-dispersion", "dispersion-potential", "disp", "disp-potential", "disp-cub"),
        description="Single negative isosurface for standalone UFF vdW dispersion potential cubes.",
        surface_mode="single",
        isosurface=-1.0,
        positive_rgb=(70, 145, 255),
        surface_opacity=(130, 255),
        notes=(
            "Use for Multiwfn function-100 userfunc.cub with iuserfunc=94, or disp.cub "
            "from the vdW potential module.  Multiwfn evaluates the attractive UFF "
            "dispersion component in kcal/mol, which is normally negative; the default "
            "single isosurface is therefore -1.0 kcal/mol.  Because this is still a "
            "single-surface preset, color overrides use --positive-rgb.  For mapped "
            "density/surface figures, use preset `vdw-map` and tune the texture range "
            "per system."
        ),
    ),
    CubePreset(
        name="partial-charge",
        aliases=("pchg", "abacus-pchg", "out-pchg", "band-density", "state-density", "partial-density"),
        description="Single positive isosurface for ABACUS partial charge/state density cubes.",
        surface_mode="single",
        isosurface=0.001,
        positive_rgb=(130, 210, 255),
        surface_opacity=(150, 255),
        notes=(
            "Use for ABACUS calculation get_pchg / out_pchg partial charge cubes. "
            "Tune the isosurface for the selected state, band, or energy window."
        ),
    ),
    CubePreset(
        name="wavefunction-norm",
        aliases=("wfc-norm", "abacus-wfc-norm", "out-wfc-norm", "wavefunction-magnitude", "wfc-abs"),
        description="Single positive isosurface for nonnegative wavefunction norm/magnitude cubes.",
        surface_mode="single",
        isosurface=0.001,
        positive_rgb=(180, 120, 255),
        surface_opacity=(145, 255),
        notes=(
            "Use for ABACUS out_wfc_norm nonnegative wavefunction norm or magnitude cubes. "
            "For signed real/imaginary wavefunction cubes from out_wfc_re_im, use preset `signed` or alias `orbital`."
        ),
    ),
    CubePreset(
        name="elf",
        aliases=("abacus-elf",),
        description="ELF localization isosurface.",
        surface_mode="single",
        isosurface=0.80,
        positive_rgb=(255, 190, 60),
        notes=(
            "Use for ABACUS out_elf cubes or Multiwfn ELF cubes; tune the isosurface for each system. "
            "grid-run defaults Multiwfn function 9 to ELFLOL_type=0 (Becke) and can patch "
            "Tsirelson, Tian-Lu, or ELF-only D/D0 definitions with --elflol-type."
        ),
    ),
    CubePreset(
        name="lol",
        aliases=(),
        description="LOL localization isosurface.",
        surface_mode="single",
        isosurface=0.50,
        positive_rgb=(120, 210, 120),
        notes=(
            "Use for Multiwfn LOL cubes; tune the isosurface for each system. "
            "grid-run defaults Multiwfn function 10 to ELFLOL_type=0 (Becke) and can patch "
            "Tsirelson or Tian-Lu definitions with --elflol-type."
        ),
    ),
    CubePreset(
        name="local-information-entropy",
        aliases=("information-entropy", "infoentro", "local-info-entropy", "local-shannon-entropy"),
        description="Positive/negative isosurfaces for Multiwfn local information entropy cubes.",
        surface_mode="signed",
        isosurface=0.05,
        positive_rgb=(245, 190, 70),
        negative_rgb=(80, 150, 255),
        surface_opacity=(135, 255),
        notes=(
            "Use for Multiwfn infoentro.cub from real-space function 11. "
            "Multiwfn evaluates local information entropy as -rho/N*ln(rho/N); "
            "the field is shown as signed because dense regions can be negative depending on units/system. "
            "Multiwfn does not reset sur_value for this function, so the default follows "
            "the global main-function-5 sur_value=0.05."
        ),
    ),
    CubePreset(
        name="electron-delocalization-range",
        aliases=("edr", "edr-r-d", "electron-delocalization-range-function"),
        description="Single positive isosurface for Multiwfn EDR(r;d) cubes.",
        surface_mode="single",
        isosurface=0.05,
        positive_rgb=(105, 210, 180),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn EDR.cub from real-space function 20. "
            "Multiwfn asks for the EDR length scale d in Bohr before grid setup. "
            "The source does not reset sur_value for this function, so the default follows "
            "the global main-function-5 sur_value=0.05."
        ),
    ),
    CubePreset(
        name="orbital-overlap-distance",
        aliases=("orbital-overlap-length", "edrdmax", "edr-dmax", "d-r", "d(r)"),
        description="Single positive isosurface for Multiwfn orbital-overlap distance D(r) cubes.",
        surface_mode="single",
        isosurface=0.05,
        positive_rgb=(115, 170, 255),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn EDRDmax.cub from real-space function 21. "
            "Multiwfn can use its default EDR exponent set 20, 2.50, 1.50 or manually supplied "
            "exponent count/start/increment values. The source does not reset sur_value for this function, "
            "so the default follows the global main-function-5 sur_value=0.05."
        ),
    ),
    CubePreset(
        name="source-function",
        aliases=("source", "srcfunc", "source-func"),
        description="Positive/negative isosurfaces for Multiwfn source function cubes.",
        surface_mode="signed",
        isosurface=0.05,
        positive_rgb=(255, 210, 80),
        negative_rgb=(70, 130, 255),
        surface_opacity=(135, 255),
        notes=(
            "Use for Multiwfn srcfunc.cub from real-space function 19. "
            "The source function depends on a reference point and srcfuncmode; "
            "grid-run sets the reference point through main menu 1000 -> 1, "
            "copies the selected Multiwfn settings.ini when available, patches "
            "srcfuncmode, and passes the run-local settings file with -set. "
            "Multiwfn does not reset sur_value for this function, so the default follows "
            "the global main-function-5 sur_value=0.05."
        ),
    ),
    CubePreset(
        name="pair-function",
        aliases=(
            "fermihole",
            "fermi-hole",
            "correlation-hole",
            "corr-hole",
            "correlation-factor",
            "corr-factor",
            "exchange-correlation-density",
            "xc-density",
            "pair-density",
        ),
        description="Positive/negative isosurfaces for Multiwfn pair/correlation function cubes.",
        surface_mode="signed",
        isosurface=0.05,
        positive_rgb=(255, 185, 90),
        negative_rgb=(85, 145, 255),
        surface_opacity=(135, 255),
        notes=(
            "Use for Multiwfn fermihole.cub from real-space function 17. "
            "The function depends on a reference point plus pairfunctype and paircorrtype; "
            "grid-run sets the reference point through main menu 1000 -> 1, copies the selected "
            "Multiwfn settings.ini when available, patches pairfunctype/paircorrtype, and passes "
            "the run-local settings file with -set. Pair-density modes can be displayed with "
            "--preset density when a single positive surface is preferred."
        ),
    ),
    CubePreset(
        name="on-top-pair-density",
        aliases=(
            "ontop-pair-density",
            "on-top-pair",
            "ontop-pair",
            "pair-density-ontop",
            "pair-density-on-top",
        ),
        description="Single positive isosurface for Multiwfn on-top pair density cubes.",
        surface_mode="single",
        isosurface=0.01,
        positive_rgb=(255, 185, 90),
        surface_opacity=(135, 255),
        notes=(
            "Use for Multiwfn function-100 userfunc.cub with iuserfunc=36. "
            "The inspected source evaluates the r1=r2 case of all-electron pair density "
            "by temporarily setting pairfunctype=12; paircorrtype still controls whether "
            "exchange only, Coulomb correlation only, or exchange plus Coulomb correlation "
            "is included.  This diagnostic is normally displayed as a positive scalar field, "
            "but the default 0.01 isosurface is only a starting value."
        ),
    ),
    CubePreset(
        name="user-function",
        aliases=(
            "userfunc",
            "user-defined-function",
            "custom-function",
            "lea-function",
            "leae-function",
            "information-gain-density",
            "relative-shannon-entropy",
            "shannon-entropy-density",
            "fisher-information-density",
        ),
        description="Generic positive/negative isosurfaces for Multiwfn userfunc.cub.",
        surface_mode="signed",
        isosurface=0.05,
        positive_rgb=(255, 205, 80),
        negative_rgb=(75, 135, 255),
        surface_opacity=(135, 255),
        notes=(
            "Use for Multiwfn userfunc.cub from real-space function 100. "
            "The generated scalar is selected by iuserfunc in settings.ini; grid-run copies the "
            "selected Multiwfn settings.ini when available, patches iuserfunc into a run-local "
            "multiwfn_grid_settings.ini, and passes it with -set. "
            "This generic standalone preset uses signed +/-0.05 surfaces and usually needs "
            "system- and function-specific tuning. For LEA/LEAE colored density surfaces, "
            "use preset `lea` or `leae` with density.cub as the surface and userfunc.cub as texture."
        ),
    ),
    CubePreset(
        name="becke-weight",
        aliases=("becke", "becke-overlap-weight", "becke-atomic-weight", "beckewei"),
        description="Single positive isosurface for Multiwfn Becke atomic/overlap weight cubes.",
        surface_mode="single",
        isosurface=0.5,
        positive_rgb=(180, 220, 120),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn Becke.cub from real-space function 111. "
            "Becke weights are dimensionless and normally span 0..1; "
            "atom pair I,J gives Becke overlap weight, while I,0 gives Becke atomic weight."
        ),
    ),
    CubePreset(
        name="hirshfeld-weight",
        aliases=("hirshfeld", "hirshfeld-atomic-weight", "hirshfeldwei"),
        description="Single positive isosurface for Multiwfn Hirshfeld weight cubes.",
        surface_mode="single",
        isosurface=0.5,
        positive_rgb=(120, 205, 170),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn Hirshfeld.cub from real-space function 112. "
            "Hirshfeld weights are dimensionless and normally span 0..1; "
            "grid-run currently uses Multiwfn's built-in atomic densities "
            "rather than prompting for separate atomic .wfn files."
        ),
    ),
    CubePreset(
        name="rdg-scalar",
        aliases=("rdg-cube", "scalar-rdg", "reduced-density-gradient"),
        description="Single positive isosurface for standalone RDG scalar cubes.",
        surface_mode="single",
        isosurface=0.5,
        positive_rgb=(130, 220, 170),
        surface_opacity=(145, 255),
        notes=(
            "Use for standalone Multiwfn RDG.cub from real-space function 13. "
            "For RDG/NCI surfaces colored by sign(lambda2)rho, keep using preset `iri` with --texture-cube."
        ),
    ),
    CubePreset(
        name="promolecular-rdg",
        aliases=("rdg-pro", "prodens-rdg", "promolecular-rdg-scalar", "rdgprodens"),
        description="Single positive isosurface for promolecular RDG scalar cubes.",
        surface_mode="single",
        isosurface=0.4,
        positive_rgb=(100, 200, 200),
        surface_opacity=(145, 255),
        notes=(
            "Use for standalone Multiwfn RDGprodens.cub from real-space function 14. "
            "The default isosurface follows Multiwfn main-function-5 sur_value."
        ),
    ),
    CubePreset(
        name="promolecular-delta-g",
        aliases=("delta-g", "deltag", "delta_g", "promolecular-deltag", "delta-g-promol"),
        description="Single positive isosurface for standalone promolecular Delta-g cubes.",
        surface_mode="single",
        isosurface=0.05,
        positive_rgb=(255, 185, 70),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn Delta_g.cub from real-space function 22 "
            "Delta-g (promolecular approximation). "
            "This standalone cube is distinct from IGM/IGMH fragment dg_inter.cub mapped-surface routes. "
            "Multiwfn does not reset sur_value for function 22, so the default follows "
            "the global main-function-5 sur_value=0.05."
        ),
    ),
    CubePreset(
        name="hirshfeld-delta-g",
        aliases=("delta-g-hirshfeld", "deltag-hirshfeld", "delta_g_hirshfeld", "igmh-scalar"),
        description="Single positive isosurface for standalone Hirshfeld-partition Delta-g cubes.",
        surface_mode="single",
        isosurface=0.05,
        positive_rgb=(255, 135, 80),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn function 23 Delta-g (Hirshfeld partition). "
            "In main-function-5 3D export, Multiwfn writes this as the generic griddata.cub "
            "rather than a dedicated filename; grid-run renames the processed product. "
            "This is a standalone full-system scalar cube and is distinct from IGM/IGMH "
            "fragment dg_inter.cub mapped-surface routes."
        ),
    ),
    CubePreset(
        name="iri-scalar",
        aliases=("iri-cube", "standalone-iri", "interaction-region-indicator"),
        description="Single positive isosurface for standalone IRI scalar cubes.",
        surface_mode="single",
        isosurface=1.0,
        positive_rgb=(120, 210, 190),
        surface_opacity=(145, 255),
        notes=(
            "Use for standalone Multiwfn IRI.cub from real-space function 24. "
            "For IRI/RDG/NCI surfaces colored by sign(lambda2)rho, keep using preset `iri` with --texture-cube. "
            "The default isosurface follows Multiwfn main-function-5 sur_value."
        ),
    ),
    CubePreset(
        name="dori-scalar",
        aliases=("standalone-dori", "dori-cube", "density-overlap-regions-indicator-scalar"),
        description="Single positive isosurface for standalone DORI scalar cubes.",
        surface_mode="single",
        isosurface=0.95,
        positive_rgb=(140, 210, 190),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn function-100 userfunc.cub with iuserfunc=20 (DORI). "
            "For DORI surfaces colored by sign(lambda2)rho, use preset `dori` with --texture-cube. "
            "The default isosurface follows the bundled DORIfill.vmd template."
        ),
    ),
    CubePreset(
        name="rose",
        aliases=(
            "region-of-slow-electrons",
            "region-slow-electrons",
            "slow-electron-region",
            "slow-electrons",
            "rose-function",
        ),
        description="Single positive isosurface for Region of Slow Electrons (RoSE) cubes.",
        surface_mode="single",
        isosurface=0.5,
        positive_rgb=(255, 190, 85),
        surface_opacity=(135, 255),
        notes=(
            "Use for Multiwfn function-100 userfunc.cub with iuserfunc=18. "
            "Multiwfn evaluates RoSE as (Dh-G)/(Dh+G), where Dh is the homogeneous-electron-gas "
            "kinetic-energy term and G is Lagrangian kinetic energy density. "
            "The maintained display uses a single positive 0.5 isosurface to highlight slow-electron regions; "
            "inspect the value range and tune --isosurface per system."
        ),
    ),
    CubePreset(
        name="sedd",
        aliases=(
            "single-exponential-decay-detector",
            "single-exponential-decay",
            "single-exponential-decay-detection",
            "sedd-function",
        ),
        description="Single positive isosurface for the single exponential decay detector.",
        surface_mode="single",
        isosurface=0.5,
        positive_rgb=(120, 200, 255),
        surface_opacity=(135, 255),
        notes=(
            "Use for Multiwfn function-100 userfunc.cub with iuserfunc=19. "
            "Multiwfn's SEDD implementation evaluates log(1+epsilon) from density gradients and Hessians, "
            "so the field is nonnegative. The default 0.5 isosurface is a starting point and should be "
            "adjusted after inspecting the cube range."
        ),
    ),
    CubePreset(
        name="stm",
        aliases=("ldos", "stm-ldos", "tunneling-current"),
        description="Constant-current STM/LDOS tunneling-current isosurface.",
        surface_mode="single",
        isosurface=0.001,
        positive_rgb=(80, 210, 255),
        notes="Use for Multiwfn STM.cub exported by the constant-current STM workflow; tune the isosurface for each bias/system.",
    ),
    CubePreset(
        name="domain",
        aliases=("domain-cube", "domain-analysis", "binary-domain"),
        description="Binary Multiwfn domain.cub isosurface.",
        surface_mode="single",
        isosurface=0.5,
        positive_rgb=(255, 170, 0),
        surface_opacity=(160, 255),
        notes="Use for Multiwfn domain.cub from main function 200/14; values are 1 inside the selected domain and 0 outside.",
    ),
    CubePreset(
        name="basin",
        aliases=("basin-cube", "binary-basin", "aim-basin", "elf-basin"),
        description="Binary Multiwfn basinNNNN.cub isosurface.",
        surface_mode="single",
        isosurface=0.5,
        positive_rgb=(100, 180, 255),
        surface_opacity=(150, 255),
        notes=(
            "Use for individual Multiwfn basinNNNN.cub files exported by basin analysis option -5; "
            "values are 1 inside the selected basin and 0 outside. "
            "The all-index basin.cub file is not binary and should not use this preset directly."
        ),
    ),
    CubePreset(
        name="basin-type",
        aliases=("basinsyn", "basin-synaptic", "elf-basin-type"),
        description="Signed Multiwfn basinsyn.cub mono-/disynaptic basin map.",
        surface_mode="signed",
        isosurface=0.5,
        positive_rgb=(255, 180, 40),
        negative_rgb=(80, 160, 255),
        surface_opacity=(145, 255),
        notes=(
            "Use for Multiwfn basinsyn.cub from basin analysis option -5; "
            "monosynaptic basin regions are -1 and disynaptic regions are +1."
        ),
    ),
    CubePreset(
        name="iri",
        aliases=("rdg", "nci", "weak-interaction"),
        description="IRI/RDG/NCI surface colored by sign(lambda2)rho-like texture cube.",
        surface_mode="single",
        isosurface=1.0,
        tex_physical=(-0.04, 0.04),
        tex_range_source="surface-band",
        texture_required=True,
        notes="Use the IRI/RDG scalar as surface cube and sign(lambda2)rho-like cube as texture cube.",
    ),
    CubePreset(
        name="dori",
        aliases=("dori-map", "dori-fill", "density-overlap-regions-indicator"),
        description="DORI surface colored by sign(lambda2)rho texture cube.",
        surface_mode="single",
        isosurface=0.95,
        tex_physical=(-0.04, 0.02),
        tex_range_source="surface-band",
        texture_required=True,
        notes=(
            "Use DORI userfunc.cub as surface cube and sign(lambda2)rho cube as texture cube; "
            "defaults follow the bundled DORIfill.vmd template."
        ),
    ),
    CubePreset(
        name="igmh",
        aliases=("igm", "igm-inter", "igmh-inter", "interfragment-igm", "interfragment-igmh"),
        description="IGM/IGMH interfragment delta-g surface colored by sign(lambda2)rho.",
        surface_mode="single",
        isosurface=0.01000,
        tex_physical=(-0.05, 0.05),
        texture_required=True,
        notes=(
            "Use Multiwfn dg_inter.cub as surface cube and sl2r.cub as texture cube; "
            "defaults follow the bundled IGM_inter.vmd template."
        ),
    ),
    CubePreset(
        name="igm-intra",
        aliases=("igmh-intra", "intrafragment-igm", "intrafragment-igmh"),
        description="IGM/IGMH intrafragment delta-g surface colored by sign(lambda2)rho.",
        surface_mode="single",
        isosurface=0.2000,
        tex_physical=(-0.05, 0.05),
        texture_required=True,
        notes=(
            "Use Multiwfn dg_intra.cub as surface cube and sl2r.cub as texture cube; "
            "defaults follow the bundled IGM_intra.vmd template."
        ),
    ),
    CubePreset(
        name="aigm",
        aliases=("average-igm", "averaged-igm", "avg-igm"),
        description="Averaged IGM delta-g surface colored by averaged sign(lambda2)rho.",
        surface_mode="single",
        isosurface=0.008,
        tex_physical=(-0.05, 0.05),
        texture_required=True,
        notes=(
            "Use Multiwfn avgdg_inter.cub as surface cube and avgsl2r.cub as texture cube; "
            "defaults follow the bundled aIGM.vmd template."
        ),
    ),
    CubePreset(
        name="aigm-tfi",
        aliases=("aigm-thermal-fluctuation-index", "tfi-igm", "aigm-tfi-map"),
        description="Averaged IGM delta-g surface colored by thermal fluctuation index.",
        surface_mode="single",
        isosurface=0.008,
        tex_physical=(0.0, 1.5),
        texture_required=True,
        notes=(
            "Use Multiwfn avgdg_inter.cub as surface cube and thermflu.cub as texture cube; "
            "defaults follow the bundled aIGM_TFI.vmd template."
        ),
    ),
    CubePreset(
        name="esp",
        aliases=("mep", "electrostatic-potential", "density-esp"),
        description="Density surface colored by electrostatic potential texture cube.",
        surface_mode="single",
        isosurface=0.001,
        texture_required=True,
        notes="Use density as surface cube and ESP/MEP/potential as texture cube; set --tex-physical for comparable figures.",
    ),
    CubePreset(
        name="surface-map",
        aliases=("molsurfmap", "mapped-surface", "density-surface-map"),
        description="Generic density surface colored by a compatible mapped-property cube.",
        surface_mode="single",
        isosurface=0.01,
        tex_physical=(0.0, 0.002),
        texture_required=True,
        notes=(
            "Use density/surface cube as the surface and a mapped-property cube as texture; "
            "defaults follow the bundled molsurfmap.vmd template."
        ),
    ),
    CubePreset(
        name="alie",
        aliases=("average-local-ionization-energy", "avglocion"),
        description="Density surface colored by Multiwfn average local ionization energy (ALIE).",
        surface_mode="single",
        isosurface=0.0005,
        tex_physical=(0.32, 0.36),
        texture_required=True,
        notes=(
            "Use Multiwfn density.cub as surface cube and avglocion.cub as texture cube; "
            "default color range follows the bundled ALIE.vmd example in a.u."
        ),
    ),
    CubePreset(
        name="lea",
        aliases=("local-electron-affinity",),
        description="Density surface colored by Multiwfn local electron affinity (LEA).",
        surface_mode="single",
        isosurface=0.01,
        tex_physical=(-0.8, -0.3),
        texture_required=True,
        notes=(
            "Use Multiwfn density.cub as surface cube and userfunc.cub as texture cube; "
            "default color range follows the bundled LEA VMD example in a.u."
        ),
    ),
    CubePreset(
        name="leae",
        aliases=("local-electron-attachment-energy",),
        description="Density surface colored by Multiwfn local electron attachment energy (LEAE).",
        surface_mode="single",
        isosurface=0.004,
        tex_physical=(-0.03, 0.0),
        texture_required=True,
        notes=(
            "Use Multiwfn density.cub as surface cube and userfunc.cub as texture cube; "
            "default color range follows the bundled LEAE VMD example in a.u."
        ),
    ),
    CubePreset(
        name="vdw-map",
        aliases=("vdw-surface", "vdw-density-surface", "vdw-potential-map"),
        description="Density surface colored by Multiwfn van der Waals potential.",
        surface_mode="single",
        isosurface=0.0001,
        tex_physical=(-0.3, 0.3),
        texture_required=True,
        notes=(
            "Use Multiwfn density.cub as surface cube and vdW.cub/vdWpot.cub as texture cube; "
            "default color range follows the bundled vdWpot.vmd example in kcal/mol."
        ),
    ),
)


PRESET_BY_NAME: Dict[str, CubePreset] = {}
for _preset in PRESETS:
    PRESET_BY_NAME[_preset.name] = _preset
    for _alias in _preset.aliases:
        PRESET_BY_NAME[_alias] = _preset


def preset_names() -> List[str]:
    return [preset.name for preset in PRESETS]


def resolve_preset(name: str) -> CubePreset:
    key = name.strip().lower()
    try:
        return PRESET_BY_NAME[key]
    except KeyError:
        known = ", ".join(sorted(PRESET_BY_NAME))
        raise ValueError(f"Unknown cube preset: {name}. Known presets/aliases: {known}")


def format_preset_list() -> str:
    lines = ["Available cube presets:", ""]
    for preset in PRESETS:
        alias_text = f" (aliases: {', '.join(preset.aliases)})" if preset.aliases else ""
        lines.append(f"- {preset.name}{alias_text}: {preset.description}")
        lines.append(f"  isosurface={preset.isosurface}, surface_mode={preset.surface_mode}")
        if preset.texture_required:
            lines.append("  requires --texture-cube")
        if preset.tex_physical is not None:
            lines.append(f"  tex_physical={preset.tex_physical[0]} {preset.tex_physical[1]}")
        if preset.notes:
            lines.append(f"  note: {preset.notes}")
    return "\n".join(lines) + "\n"


def default_surface_extrema_selection(preset: CubePreset) -> str:
    if preset.name in {"alie", "leae"}:
        return "minima"
    if preset.name == "lea":
        return "maxima"
    return "all"


def _float_pair(values: Optional[Sequence[float]]) -> Optional[Tuple[float, float]]:
    if values is None:
        return None
    if len(values) != 2:
        raise ValueError("Expected exactly two values")
    return float(values[0]), float(values[1])


def _float_six(values: Optional[Sequence[float]]) -> Tuple[float, float, float, float, float, float]:
    if values is None:
        return 0.0, 1.0, 0.0, 1.0, 0.0, 1.0
    if len(values) != 6:
        raise ValueError("Boundary requires six values: xmin xmax ymin ymax zmin zmax")
    return tuple(float(value) for value in values)  # type: ignore[return-value]


def _rgb(values: Optional[Sequence[int]], default: RGB, label: str) -> RGB:
    if values is None:
        return default
    if len(values) != 3:
        raise ValueError(f"{label} RGB requires exactly three values")
    rgb = tuple(int(value) for value in values)
    if any(value < 0 or value > 255 for value in rgb):
        raise ValueError(f"{label} RGB values must be between 0 and 255")
    return rgb  # type: ignore[return-value]


def _opacity(values: Optional[Sequence[int]], default: Tuple[int, int]) -> Tuple[int, int]:
    if values is None:
        return default
    if len(values) != 2:
        raise ValueError("Surface opacity requires exactly two values")
    opacity = tuple(int(value) for value in values)
    if any(value < 0 or value > 255 for value in opacity):
        raise ValueError("Surface opacity values must be between 0 and 255")
    return opacity  # type: ignore[return-value]


def _append_preset_manifest(
    manifest: Path,
    *,
    requested_preset: str,
    preset: CubePreset,
    surface_cube: Path,
    texture_cube: Optional[Path],
    surface_mode: str,
    isosurface: float,
    tex_percent: Optional[Tuple[float, float]],
    tex_physical: Optional[Tuple[float, float]],
    tex_range_source: str,
) -> None:
    text = manifest.read_text(encoding="utf-8")
    lines = [
        "",
        "## Cube Preset",
        "",
        f"- requested_preset: `{requested_preset}`",
        f"- canonical_preset: `{preset.name}`",
        f"- description: `{preset.description}`",
        f"- surface_cube: `{surface_cube}`",
        f"- texture_cube: `{texture_cube}`" if texture_cube is not None else "- texture_cube: `None`",
        f"- preset_surface_mode: `{preset.surface_mode}`",
        f"- effective_surface_mode: `{surface_mode}`",
        f"- preset_isosurface: `{preset.isosurface}`",
        f"- effective_isosurface: `{isosurface}`",
        f"- texture_required: `{str(preset.texture_required).lower()}`",
        f"- preset_tex_range_source: `{preset.tex_range_source}`",
        f"- effective_tex_range_source: `{tex_range_source}`",
    ]
    if tex_percent is not None:
        lines.append(f"- effective_tex_percent: `{tex_percent[0]}` to `{tex_percent[1]}`")
        lines.append("- tex_range_note: `explicit --tex-percent was used; physical texture scaling was not applied`")
    if preset.tex_physical is not None:
        lines.append(f"- preset_tex_physical: `{preset.tex_physical[0]}` to `{preset.tex_physical[1]}`")
    if tex_physical is not None:
        lines.append(f"- effective_tex_physical: `{tex_physical[0]}` to `{tex_physical[1]}`")
    if preset.notes:
        lines.append(f"- notes: `{preset.notes}`")
    manifest.write_text(text.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


def run_preset(
    preset_name: str,
    surface_cube: Path,
    output_dir: Path,
    *,
    texture_cube: Optional[Path] = None,
    stem: Optional[str] = None,
    output_vesta: Optional[Path] = None,
    manifest: Optional[Path] = None,
    write_manifest: bool = True,
    title: Optional[str] = None,
    isosurface: Optional[float] = None,
    surface_mode: Optional[str] = None,
    positive_rgb: Optional[Sequence[int]] = None,
    negative_rgb: Optional[Sequence[int]] = None,
    surface_opacity: Optional[Sequence[int]] = None,
    tex_percent: Optional[Sequence[float]] = None,
    tex_physical: Optional[Sequence[float]] = None,
    tex_range_source: Optional[str] = None,
    surface_band: Optional[float] = None,
    surface_nearest: int = 1024,
    cube_units: str = "auto",
    structure: Optional[str] = None,
    boundary: Optional[Sequence[float]] = None,
    sections: Optional[str] = None,
    copy_cubes: bool = True,
    strict: bool = True,
    strict_compatible: bool = True,
    show_structure_bonds: bool = True,
    surfanalysis_pdb: Optional[Path] = None,
    surf_extrema: str = "auto",
    extrema_radius: float = surface_extrema_vesta.DEFAULT_EXTREMA_RADIUS,
    maxima_rgb: Optional[Sequence[int]] = None,
    minima_rgb: Optional[Sequence[int]] = None,
    label_extrema: bool = False,
    keep_comps: bool = False,
) -> cube_vesta.CubeVestaResult:
    surface_cube = Path(surface_cube)
    output_dir = Path(output_dir)
    texture_cube = Path(texture_cube) if texture_cube is not None else None
    surfanalysis_pdb = Path(surfanalysis_pdb) if surfanalysis_pdb is not None else None
    preset = resolve_preset(preset_name)
    if preset.texture_required and texture_cube is None:
        raise ValueError(f"Cube preset `{preset.name}` requires --texture-cube")
    if preset.name == "basin" and surface_cube.name.lower() == "basin.cub":
        raise ValueError(
            "Cube preset `basin` is for individual binary basinNNNN.cub files; "
            "Multiwfn basin.cub stores basin indices, not a binary basin mask."
        )

    effective_isosurface = preset.isosurface if isosurface is None else float(isosurface)
    effective_surface_mode = surface_mode or preset.surface_mode
    effective_tex_percent = _float_pair(tex_percent)
    effective_tex_physical = None if effective_tex_percent is not None else preset.tex_physical
    if tex_physical is not None:
        effective_tex_physical = _float_pair(tex_physical)
    backend_tex_range_source = tex_range_source or preset.tex_range_source
    manifest_tex_range_source = "explicit-percent" if effective_tex_percent is not None else backend_tex_range_source
    effective_title = title or f"{surface_cube.stem} ({preset.name})"
    effective_stem = stem or f"{surface_cube.stem}_{preset.name}"

    result = cube_vesta.run_workflow(
        surface_cube,
        output_dir,
        texture_cube=texture_cube,
        stem=effective_stem,
        output_vesta=output_vesta,
        manifest=manifest,
        write_manifest=write_manifest,
        title=effective_title,
        isosurface=effective_isosurface,
        surface_mode=effective_surface_mode,
        positive_rgb=_rgb(positive_rgb, preset.positive_rgb, "positive surface"),
        negative_rgb=_rgb(negative_rgb, preset.negative_rgb, "negative surface"),
        surface_opacity=_opacity(surface_opacity, preset.surface_opacity),
        tex_percent=effective_tex_percent,
        tex_physical=effective_tex_physical,
        tex_range_source=backend_tex_range_source,
        surface_band=surface_band,
        surface_nearest=surface_nearest,
        cube_units=cube_units,
        structure=structure or preset.structure,
        boundary=_float_six(boundary),
        sections=sections or preset.sections,
        copy_cubes=copy_cubes,
        strict=strict,
        strict_compatible=strict_compatible,
        show_structure_bonds=show_structure_bonds,
    )
    if result.manifest_path is not None:
        _append_preset_manifest(
            result.manifest_path,
            requested_preset=preset_name,
            preset=preset,
            surface_cube=surface_cube,
            texture_cube=texture_cube,
            surface_mode=effective_surface_mode,
            isosurface=effective_isosurface,
            tex_percent=effective_tex_percent,
            tex_physical=effective_tex_physical,
            tex_range_source=manifest_tex_range_source,
        )
    if surfanalysis_pdb is not None:
        selection = default_surface_extrema_selection(preset) if surf_extrema == "auto" else surf_extrema
        max_rgb = _rgb(maxima_rgb, surface_extrema_vesta.DEFAULT_MAXIMA_RGB, "surface maxima")
        min_rgb = _rgb(minima_rgb, surface_extrema_vesta.DEFAULT_MINIMA_RGB, "surface minima")
        overlay_structure = structure or preset.structure
        if overlay_structure == "none":
            overlay_structure = "auto"
        overlay = surface_extrema_vesta.overlay_surface_extrema_file(
            result.vesta_path,
            surfanalysis_pdb,
            result.vesta_path,
            surface_cube=surface_cube,
            selection=selection,
            title=f"{effective_title} surface extrema",
            structure=overlay_structure,
            boundary=_float_six(boundary),
            radius=extrema_radius,
            maxima_rgb=max_rgb,
            minima_rgb=min_rgb,
            label_extrema=label_extrema,
            set_comps_off=not keep_comps,
            cube_units=cube_units,
            strict=strict,
        )
        if result.manifest_path is not None:
            surface_extrema_vesta.append_overlay_manifest(
                result.manifest_path,
                surfanalysis_pdb=surfanalysis_pdb,
                result=overlay,
                radius=extrema_radius,
                maxima_rgb=max_rgb,
                minima_rgb=min_rgb,
                label_extrema=label_extrema,
                set_comps_off=not keep_comps,
            )
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create a VESTA file from a cube using an analysis-oriented preset."
    )
    parser.add_argument("preset", nargs="?", help="Preset name or alias; use --list-presets to inspect options")
    parser.add_argument("surface_cube", nargs="?", type=Path)
    parser.add_argument("output_dir", nargs="?", type=Path)
    parser.add_argument("--list-presets", action="store_true")
    parser.add_argument("--texture-cube", type=Path)
    parser.add_argument("--stem")
    parser.add_argument("--output-vesta", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--no-manifest", action="store_true")
    parser.add_argument("--title")
    parser.add_argument("--isosurface", type=float)
    parser.add_argument("--surface-mode", choices=["single", "signed"])
    parser.add_argument("--positive-rgb", nargs=3, type=int, metavar=("R", "G", "B"))
    parser.add_argument("--negative-rgb", nargs=3, type=int, metavar=("R", "G", "B"))
    parser.add_argument("--surface-opacity", nargs=2, type=int, metavar=("O1", "O2"))
    parser.add_argument("--tex-percent", nargs=2, type=float, metavar=("MIN", "MAX"))
    parser.add_argument("--tex-physical", nargs=2, type=float, metavar=("MIN", "MAX"))
    parser.add_argument("--tex-range-source", choices=["full-cube", "surface-band"])
    parser.add_argument("--surface-band", type=float)
    parser.add_argument("--surface-nearest", type=int, default=1024)
    parser.add_argument("--cube-units", choices=["auto", "bohr", "angstrom"], default="auto")
    parser.add_argument("--structure", choices=["auto", "none", "molecule", "crystal"])
    parser.add_argument("--boundary", nargs=6, type=float, metavar=("XMIN", "XMAX", "YMIN", "YMAX", "ZMIN", "ZMAX"))
    parser.add_argument("--sections", choices=["off", "keep"])
    parser.add_argument("--no-copy-cubes", action="store_true")
    parser.add_argument("--non-strict", action="store_true", help="Allow cube data count mismatch")
    parser.add_argument("--no-strict-compatible", action="store_true", help="Do not require texture grid to match surface grid")
    parser.add_argument("--structure-bonds-off", action="store_true")
    parser.add_argument("--surfanalysis-pdb", type=Path, help="Overlay Multiwfn surface extrema from surfanalysis.pdb")
    parser.add_argument("--surf-extrema", choices=["auto", "all", "maxima", "minima"], default="auto")
    parser.add_argument("--extrema-radius", type=float, default=surface_extrema_vesta.DEFAULT_EXTREMA_RADIUS)
    parser.add_argument("--maxima-rgb", nargs=3, type=int, metavar=("R", "G", "B"))
    parser.add_argument("--minima-rgb", nargs=3, type=int, metavar=("R", "G", "B"))
    parser.add_argument("--label-extrema", action="store_true")
    parser.add_argument("--keep-comps", action="store_true", help="Do not force COMPS 0 after adding extrema phase")
    args = parser.parse_args(argv)

    if args.list_presets:
        print(format_preset_list(), end="")
        return 0
    if args.preset is None or args.surface_cube is None or args.output_dir is None:
        parser.error("preset, surface_cube, and output_dir are required unless --list-presets is used")

    try:
        result = run_preset(
            args.preset,
            args.surface_cube,
            args.output_dir,
            texture_cube=args.texture_cube,
            stem=args.stem,
            output_vesta=args.output_vesta,
            manifest=args.manifest,
            write_manifest=not args.no_manifest,
            title=args.title,
            isosurface=args.isosurface,
            surface_mode=args.surface_mode,
            positive_rgb=args.positive_rgb,
            negative_rgb=args.negative_rgb,
            surface_opacity=args.surface_opacity,
            tex_percent=args.tex_percent,
            tex_physical=args.tex_physical,
            tex_range_source=args.tex_range_source,
            surface_band=args.surface_band,
            surface_nearest=args.surface_nearest,
            cube_units=args.cube_units,
            structure=args.structure,
            boundary=args.boundary,
            sections=args.sections,
            copy_cubes=not args.no_copy_cubes,
            strict=not args.non_strict,
            strict_compatible=not args.no_strict_compatible,
            show_structure_bonds=not args.structure_bonds_off,
            surfanalysis_pdb=args.surfanalysis_pdb,
            surf_extrema=args.surf_extrema,
            extrema_radius=args.extrema_radius,
            maxima_rgb=args.maxima_rgb,
            minima_rgb=args.minima_rgb,
            label_extrema=args.label_extrema,
            keep_comps=args.keep_comps,
        )
    except ValueError as exc:
        print(f"cube-preset: {exc}")
        return 2

    print(result.vesta_path)
    if result.manifest_path is not None:
        print(result.manifest_path)
    if result.copied_cubes:
        for _, destination in result.copied_cubes:
            print(f"copied {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
