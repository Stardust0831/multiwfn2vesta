# Cube VESTA Recipe

## Generated

- time: `2026-07-02T14:46:35`
- output_vesta: `examples/cof_direct_cube_suite/sample_esp/vesta_demo/rho_demo_esp_cube.vesta`
- title: `rho_demo (esp)`

## Surface Cube

- path: `examples/cof_direct_cube_suite/sample_esp/rho_demo.cube`
- unit: `bohr`
- atoms: `1`
- grid: `2 x 2 x 2`
- data_range: `0.0005` to `0.0018`
- isosurface: `0.001`
- surface_mode: `single`
- isosurface_levels: `0.001`

## Texture Cube

- path: `examples/cof_direct_cube_suite/sample_esp/potes_demo_vacuum0.cube`
- data_range: `-3.5` to `1.5`
- tex_percent_range: `0.0` to `1.0`
- tex_physical_range: `-3.5` to `1.5` converted from selected texture reference range
- tex_reference_source: `full-cube`
- tex_reference_range: `-3.5` to `1.5`
- tex_reference_sample_count: `8`

## VESTA Fields

- `IMPORT_DENSITY 1` is used for the surface cube.
- `IMPORT_TEXTURE` is used only when a texture cube is supplied.
- `SECTS` mode: `off`.
- `TEX3P` stores VESTA percentage/normalized values, not direct physical scalar values.
- structure_phase: `crystal`.

## Copied Cubes

- `examples/cof_direct_cube_suite/sample_esp/rho_demo.cube` -> `examples/cof_direct_cube_suite/sample_esp/vesta_demo/rho_demo.cube`
- `examples/cof_direct_cube_suite/sample_esp/potes_demo_vacuum0.cube` -> `examples/cof_direct_cube_suite/sample_esp/vesta_demo/potes_demo_vacuum0.cube`

## Cube Preset

- requested_preset: `esp`
- canonical_preset: `esp`
- description: `Density surface colored by electrostatic potential texture cube.`
- surface_cube: `examples/cof_direct_cube_suite/sample_esp/rho_demo.cube`
- texture_cube: `examples/cof_direct_cube_suite/sample_esp/potes_demo_vacuum0.cube`
- preset_surface_mode: `single`
- effective_surface_mode: `single`
- preset_isosurface: `0.001`
- effective_isosurface: `0.001`
- texture_required: `true`
- preset_tex_range_source: `full-cube`
- effective_tex_range_source: `full-cube`
- effective_tex_physical: `-3.5` to `1.5`
- notes: `Use density as surface cube and ESP/MEP/potential as texture cube; set --tex-physical for comparable figures.`
