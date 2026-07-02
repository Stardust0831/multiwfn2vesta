# ABACUS LR-TDDFT To Multiwfn Excitation Recipe

- label: `singlet`
- energy_file: `OUT.abacus_h2o_lr/Excitation_Energy_singlet.dat`
- amplitude_file: `OUT.abacus_h2o_lr/Excitation_Amplitude_singlet_0.dat`
- output_file: `h2o_singlet.excit.txt`
- nocc: `2`
- nvirt: `3`
- dimension_source: `INPUT.lr`
- coefficient_scale: `0.7071067811865475`
- states: `2`
- skipped_coefficients: `6`

## Format

ABACUS amplitude pair index is interpreted as `iocc * nvirt + ivirt`, matching
`source_lcao/module_lr/lr_spectrum.cpp`. Multiwfn MO indices are 1-based, so
the exporter writes `iocc + 1 -> nocc + ivirt + 1`.
A blank line is inserted after every excited state because Multiwfn's plain-text
parser uses the blank line to terminate that state's transition list.
ABACUS LR amplitudes are scaled by `coefficient_scale` before writing. The default
`1/sqrt(2)` matches Multiwfn's closed-shell TDDFT normalization convention, where
the sum of squared excitation coefficients is expected to be about 0.5.
