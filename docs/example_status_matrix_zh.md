# multiwfn2vesta 功能 example 状态矩阵

状态含义：

- 已闭环: 有真实体系、命令路线、VESTA 文件和 PNG 效果图。
- 有 VESTA/cube: 已有真实或 smoke 产物，但缺可展示 PNG。
- 有入口: CLI/测试/文档已存在，但还缺真实体系 smoke。
- 暂存/杂项: 用户要求暂不进主代码或只作为经验保留。

## 顶层 CLI 功能

| 功能 | 代表命令 | 推荐体系 | 当前证据 | 状态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| 可执行文件发现 | `multiwfn2vesta discover` | 本工作区 Multiwfn/VESTA | README/usage/CLI smoke | 有入口 | 加一个中文截图或命令输出片段 |
| ABACUS Molden 生成 | `abacus-molden` | Ag(111)+benzene | `smoke/abacus_molden_wrapper_smoke_20260610/`，Ag Molden 文件 | 有 VESTA/cube | 给真实 ABACUS 目录做完整转换记录 |
| Molden 检查 | `molden-check --abacus` | Ag(111)+benzene | README 记录 60 atoms/566 MO/[Nval] | 有入口 | 加中文手册中的成功输出片段 |
| cube 到 VESTA | `cube-vesta` | H2O IRI cube | `smoke/cube_vesta_cli_smoke_20260610/` | 有 VESTA/cube | 渲染一个通用 cube-vesta PNG |
| cube preset | `cube-preset` | IRI/IGMH/vdW/ELF 等 | 多个 smoke 目录 | 有 VESTA/cube | 挑 ABACUS direct cube 补 PNG |
| cube arithmetic | `cube-arith` | density difference / spin density | `smoke/cube_arith_smoke_20260610/` | 有 VESTA/cube | 用真实 charged/spin 体系补图 |
| grid-run | `grid-run --function ...` | H2O、Ag(111)+benzene、未来 COF | 多个单元测试和 smoke | 有 VESTA/cube | 按函数组补真实图 |
| Fukui runner | `fukui-run` | 小分子亲核/亲电反应性 | 测试和文档 | 有入口 | 准备中性/阴/阳离子真实体系 |
| IRI/RDG runner | `iri-run` | H2O-HF 或后续二聚体 | `smoke/20260605_iri_aim_h2o_hf/` 有调试 PNG/cube | 有 VESTA/cube | 当前图不够清楚，需继续修 VESTA surface/texture 样式后再作为手册成品 |
| IGM/IGMH/mIGM runner | `igmh-run` / `igm-run` / `migm-run` | Ag(111)+benzene，H2O | Ag(111)+benzene 三视图；H2O smoke | 已闭环 | 保留 Ag 作为主展示，H2O 作为快速测试 |
| aIGM/amIGM runner | `aigm-run` / `amigm-run` | 轨迹平均弱相互作用 | 文档/测试，部分轨迹经验 | 有入口 | 准备短 XYZ 轨迹并渲染平均 IGM |
| STM runner | `stm-run` | 表面/分子轨道态 | `smoke/multiwfn_stm_run_smoke_20260610/` | 有 VESTA/cube | 选有物理意义的表面或分子轨道补 PNG |
| domain runner | `domain-run` | H2O density domain | `smoke/multiwfn_domain_run_smoke_20260610/` | 有 VESTA/cube | 渲染二值域等值面 |
| AIM runner | `aim-run` | GC 碱基对、benzene | Sob/AIM smoke PNG | 已闭环 | `gc` 作为手册主例，benzene 作基础例；phenanthrene 需重调视角 |
| AIM PDB conversion | `aim-pdb` | Multiwfn `paths.pdb`/`CPs.pdb` | AIM overlay PNG | 已闭环 | 增加 CP 类型颜色说明 |
| AIM+IGMH styler | `aim-igmh` | Ag(111)+benzene | 高清三视图 | 已闭环 | 稳定无抢焦点渲染仍待做 |
| Surface extrema overlay | `surface-extrema` | ALIE/LEA/LEAE 分子表面极值 | 文档/测试 | 有入口 | 需要 ALIE/LEA 真实图 |
| ABACUS Mulliken coloring | `abacus-mulliken-color` | Fe toy / 后续磁性体系 | `smoke/abacus_mulliken_color_smoke_20260610/` | 有 VESTA/cube | 当前只是解析和 SITET 着色 smoke，需真实 ABACUS 体系 PNG、色标/图例 |
| Multiwfn atom table coloring | `multiwfn-atom-color` | 原子电荷/Fukui 表 | `smoke/multiwfn_atom_color_smoke_20260610/` | 有 VESTA/cube | 接 Multiwfn population 输出补图 |

## 已有真实 PNG 的展示组

| 功能组 | 代表图 | 原始 smoke 路径 | 项目内图 |
| --- | --- | --- | --- |
| 周期性 IGMH+AIM 三视图 | Ag(111)+benzene front/right/top | `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_cli_rotate_split_bcp_final_20260609/` | `docs/assets/gallery/ag111_benzene_igmh_aim_*.png` |
| AIM overlay 主图 | GC 碱基对 | `smoke/20260605_sob445_more_aim_examples/gc/products/gc_mol_plus_aim_overlay.png` | `docs/assets/gallery/gc_aim_overlay.png` |
| AIM overlay | benzene | `smoke/20260605_sob445_more_aim_examples/benzene/products/benzene_mol_plus_aim_overlay.png` | `docs/assets/gallery/benzene_aim_overlay.png` |
| AIM overlay 待重调视角 | phenanthrene | `smoke/20260605_sob445_more_aim_examples/phenanthrene/products/phenanthrene_mol_plus_aim_overlay.png` | `docs/assets/gallery/phenanthrene_aim_overlay.png` |
| 轨迹视频 poster | Cd/Cl NVT | `smoke/vesta_trajectory_video_1608/ase_nvt_refstyle_stride20_cdcl3p50/png/frame_0001.png` | `docs/assets/gallery/cdcl_nvt_trajectory_frame.png` |
| 轨迹帧补充 | Cd/Cl NPT | `smoke/vesta_trajectory_video_1608/ase_npt_refstyle/png/frame_0008.png` | `docs/assets/gallery/cdcl_trajectory_frame.png` |
| IRI+AIM 调试证据 | H2O-HF | `smoke/20260605_iri_aim_h2o_hf/products/1h2o_hf_iri2_plus_aim_cube_frame_irifill_small_nosect_texrange.png` | `docs/assets/gallery/h2o_iri_aim_overlay.png` |
| NICS/vector misc | benzene | `smoke/20260605_nics_vesta_vectors/benzene_nics_vector_smoke.png` | `docs/assets/gallery/benzene_nics_vector.png` |

## grid-run 函数组覆盖

| 函数组 | 当前入口 | 推荐示例体系 | 状态 | 备注 |
| --- | --- | --- | --- | --- |
| 基础密度/梯度/Laplacian | `density`, `gradient`, `laplacian` | H2O、benzene、Ag slab | 有入口 | density 可作为大多数 mapped surface 的 surface cube |
| 轨道/轨道密度 | `orbital`, `orbital-density` | benzene HOMO/LUMO，ABACUS band | 有入口 | 需要轨道编号和 HOMO/LUMO 发现辅助 |
| spin | `spin-density`, `spin-polarization`, `alpha-density`, `beta-density` | 磁性 Fe/O 或 open-shell 小分子 | 有入口 | 缺真实自旋体系效果图 |
| KED | `hamiltonian-ked`, `lagrangian-ked`, `thomas-fermi-ked`, `weizsacker-ked`, `pauli-ked` | benzene/H2O | 有入口 | 缺物理解释型示例 |
| ELF/LOL | `elf`, `lol`, `--elflol-type` | COF/Ag/benzene | 有入口 | ABACUS direct ELF 也可走 `cube-preset elf` |
| ESP/ALIE/LEA/LEAE | `esp`, `alie`, `local-electron-affinity`, `local-electron-attachment-energy` | 芳香分子、极性分子 | 有 VESTA/cube | ESP H2O smoke 已有，缺 PNG 和 surface extrema 图 |
| vdW | `vdw-potential`, `vdw-repulsion-potential`, `vdw-dispersion-potential` | Ag(111)+benzene 或分子复合物 | 有入口 | 适合做吸附相互作用外围图 |
| 弱相互作用标量 | `rdg`, `iri`, `dori`, `delta-g`, `hirshfeld-delta-g` | H2O dimer、benzene dimer、Ag adsorbate | IGMH 已闭环；IRI 有调试图 | IRI/DORI/Delta-g standalone 缺手册级图 |
| 反应性 | `fod`, `orbital-weighted-fukui-*`, `orbital-weighted-dual-descriptor` | 小分子反应位点 | 有入口 | 需要真实 closed-shell 测试体系 |
| 信息论密度 | `local-information-entropy`, `information-gain-density`, `shannon-entropy-density`, `fisher-information-density` | 小分子/COF | 有入口 | 缺图，默认 isosurface 需调 |
| 分区权重 | `becke`, `hirshfeld` | 分子内片段边界 | 有入口 | 缺图 |
| pair/source function | `pair-function`, `source-function` | 选参考点的键/孤对电子区域 | 有入口 | 缺交互式参考点选择体验 |

## cube-preset 预设覆盖

| 预设组 | 代表 preset | 状态 | 补图建议 |
| --- | --- | --- | --- |
| density/signed/orbital | `density`, `signed`, `orbital-density` | 有 VESTA/cube | benzene HOMO/LUMO |
| spin/potential/KED | `spin-density`, `potential`, `kinetic-energy-density` | 有入口 | open-shell 和 ABACUS out_pot |
| ABACUS direct cube | `partial-charge`, `wavefunction-norm`, `elf` | 有入口 | 准备 ABACUS 小体系 direct cube |
| IRI/DORI/IGMH/aIGM | `iri`, `dori`, `igmh`, `aigm` | IGMH 已闭环；IRI 有调试图 | IRI/DORI/aIGM 补手册级图 |
| ESP/ALIE/LEA/vdW map | `esp`, `alie`, `lea`, `leae`, `vdw-map` | 有 VESTA/cube | 先补 ESP/ALIE surface extrema |
| domain/basin | `domain`, `basin`, `basin-type` | 有 VESTA/cube | 渲染 H2O domain 和 basin 示例 |
| vdW components | `vdw-potential`, `vdw-repulsion-potential`, `vdw-dispersion-potential` | 有入口 | 用同一体系展示 total/repul/disp |

## 近期闭环优先级

1. 把 Ag(111)+benzene IGMH+AIM 整理成 `examples/ag111_benzene_igmh_aim/`，包含命令、输入清单、输出清单和图；后续重渲染更紧凑的 camera/zoom。
2. 把 GC AIM 和 benzene AIM 整理成轻量 examples；GC 作氢键/分子间 AIM 主图，benzene 作基础例。
3. 把 Cd/Cl NVT 高码率 mp4 轨迹例子整理出 summary、poster frame 和复用视角说明。
4. 继续完善 IRI+AIM，当前 H2O-HF 只作为调试证据，不能作为最终展示图。
5. 给 `cube-vesta`/`cube-preset` 基础功能补一张 direct cube PNG。
6. 给 `grid-run` 选 3 个代表图：ESP-on-density、ELF、vdW potential 或 KED。
7. 给 `domain-run`/`stm-run` 补真实渲染 PNG。
8. 给 atom coloring 补一张按电荷/磁矩染色的对比图。
9. 再考虑新增 Multiwfn 源码功能路线；在中文手册闭环前，不优先扩展新功能。
