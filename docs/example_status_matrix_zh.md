# multiwfn2vesta 功能 example 状态矩阵

状态含义：

- 已闭环: 有真实体系、命令路线、VESTA 文件和 PNG 效果图。
- 有 VESTA/cube: 已有真实或 smoke 产物，但缺可展示 PNG。
- 有入口: CLI/测试/文档已存在，但还缺真实体系 smoke。
- 暂存/杂项: 用户要求暂不进主代码或只作为经验保留。

正式 example 的最低要求：

- 有一个明确 `examples/<example_id>/README_zh.md` 或等价 runbook。
- 写清输入来源、完整命令、关键参数、主要输出文件和验证命令。
- 至少有一个项目内轻量 gallery PNG；大 cube、mp4、临时 `.vesta` 可以留在 `smoke/`，通过 manifest 或 `examples --verify-smoke` 引用。
- 若图仍只是调试证据，状态必须保持 `needs-work` 或 `有 VESTA/cube`，不能标为 `已闭环`。

按功能反查推荐体系、runbook、效果图和下一步见 `feature_examples_zh.md`，也可以运行：

```bash
multiwfn2vesta examples --summary
multiwfn2vesta examples --coverage
multiwfn2vesta examples --needs-render
multiwfn2vesta examples --command aim-igmh
multiwfn2vesta examples --gallery-assets
multiwfn2vesta examples --systems
```

本轮审计后的使用原则：

- `ready` 只给已经有真实体系、runbook 和项目内 PNG 的功能；目前主力是 Ag(111)+benzene、GC AIM 和 Cd/Cl 轨迹。
- `linked` 表示功能已被某个 ready workflow 间接覆盖，但还没有独立教程图。
- `needs-render` 表示代码路径或 smoke 经验存在，但还必须真实渲染后才能进入手册主图。
- `needs-example` 表示还缺真实输入链路；只能先给推荐体系和 runbook 计划。
- 新功能闭环时先运行 `multiwfn2vesta examples --systems` 选体系，再用 `--command` 检查同类功能已有状态。
- 需要快速汇报当前闭环度时先运行 `multiwfn2vesta examples --summary`；它会统计 ready/linked/needs-render/needs-example，
  并列出当前 gallery 是否齐全和下一批优先体系。

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
| trajectory frame writer | `trajectory-frames` | Cd/Cl extXYZ 轨迹 | `examples/cdcl_trajectory_video/cdcl_tiny.extxyz`、单元测试、gallery poster 和 smoke 命令 | 已闭环 | 补 ASE `.traj` 直接读取，并把 reference `.vesta` 到 PNG 渲染层串起来 |
| trajectory video encoder | `trajectory-video` | Cd/Cl VESTA PNG frame 序列 | Cd/Cl manifest dry-run、frame list/recipe 测试、gallery poster 和本地 mp4 证据 | 已闭环 | 与 `trajectory-frames` manifest 和后续 PNG 渲染层衔接 |
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
| 轨迹视频 poster | Cd/Cl NVT | `smoke/vesta_trajectory_video_1608/ase_nvt_refstyle_stride20_cdcl3p50/png/frame_0001.png`；可用 `multiwfn2vesta examples --id cdcl_trajectory_video --verify-smoke` 检查本地证据 | `docs/assets/gallery/cdcl_nvt_trajectory_frame.png` |
| 轨迹帧补充 | Cd/Cl NPT | `smoke/vesta_trajectory_video_1608/ase_npt_refstyle/png/frame_0008.png` | `docs/assets/gallery/cdcl_trajectory_frame.png` |
| IRI+AIM 调试证据 | H2O-HF | `smoke/20260605_iri_aim_h2o_hf/products/1h2o_hf_iri2_plus_aim_cube_frame_irifill_small_nosect_texrange.png` | `docs/assets/gallery/h2o_iri_aim_overlay.png` |
| NICS/vector misc | benzene | `smoke/20260605_nics_vesta_vectors/benzene_nics_vector_smoke.png` | `docs/assets/gallery/benzene_nics_vector.png` |

## grid-run 函数组覆盖

| 函数组 | 当前入口 | 推荐示例体系 | 状态 | 备注 |
| --- | --- | --- | --- | --- |
| 基础密度/梯度/Laplacian | `density`, `gradient`, `laplacian` | H2O、benzene、Ag slab | 有入口 | density 可作为大多数 mapped surface 的 surface cube |
| 轨道/轨道密度 | `orbital`, `orbital-density` | benzene HOMO/LUMO，ABACUS band | 有入口 | 需要轨道编号和 HOMO/LUMO 发现辅助 |
| spin | `spin-density`, `spin-polarization`, `alpha-density`, `beta-density` | 磁性 Fe/O 或 open-shell 小分子 | 有入口 | 缺真实自旋体系效果图 |
| KED 和扩展 KED diagnostics | `hamiltonian-ked`, `lagrangian-ked`, `thomas-fermi-ked`, `weizsacker-ked`, `pauli-ked`, `tf-minus-lagrangian-ked`, `lagrangian-local-temperature`, `thomas-fermi-ked-potential` 等 | benzene/H2O/Ag(111)+benzene | 有入口 | 已有 `iuserfunc=1201/1202/1203/1204/1210` 路由和 preset，缺物理解释型示例图 |
| ELF/LOL | `elf`, `lol`, `--elflol-type` | COF/Ag/benzene | 有入口 | ABACUS direct ELF 也可走 `cube-preset elf` |
| ESP/ALIE/LEA/LEAE | `esp`, `electron-esp`, `positive-esp`, `negative-esp`, `electric-field-magnitude`, `alie`, `local-electron-affinity`, `local-electron-attachment-energy` | 芳香分子、极性分子、Ag(111)+benzene | 有 VESTA/cube | ESP H2O smoke 已有；电子贡献 ESP、正/负分量和电场强度路由已维护，缺正式 PNG 和 surface extrema 图 |
| vdW | `vdw-potential`, `vdw-repulsion-potential`, `vdw-dispersion-potential` | Ag(111)+benzene 或分子复合物 | 有入口 | 适合做吸附相互作用外围图 |
| 弱相互作用标量 | `rdg`, `iri`, `dori`, `delta-g`, `hirshfeld-delta-g` | H2O dimer、benzene dimer、Ag adsorbate | IGMH 已闭环；IRI 有调试图 | IRI/DORI/Delta-g standalone 缺手册级图 |
| 慢电子/指数衰减标量 | `rose`, `sedd` | benzene dimer、GC 碱基对 | 有入口 | 已有 source-backed `iuserfunc=18/19` 路由和 preset，缺真实 paired render |
| steric/SBL/Pauli/quantum 诊断场 | `steric-*`, `pauli-*`, `quantum-*`, `electrostatic-*`, `sbl-*` | Ag(111)+benzene、benzene dimer、GC 碱基对 | 有入口 | 已有 source-backed `iuserfunc=40-43/60-69/-69/110-113` 路由和 preset，缺真实界面/弱相互作用 render |
| 电子对密度 | `on-top-pair-density` | benzene dimer、GC 碱基对 | 有入口 | 已有 source-backed `iuserfunc=36` 路由、`paircorrtype` 控制和 preset，缺真实 pair-density render |
| 信息论/Ghosh/Renyi/disequilibrium | `information-gain-density`, `shannon-entropy-density`, `fisher-information-density`, `second-fisher-information-density`, `ghosh-entropy-density`, `renyi-quadratic-density`, `disequilibrium-density` | benzene dimer、GC 碱基对、H2O 或 COF | 有入口 | 已有 source-backed `iuserfunc=49/50/51/52/53/54/55/56/70/100` 路由和 preset；information gain 自动做 promolecular 初始化，second-Fisher 为 signed preset，缺真实解释型 render |
| USI/BNI 相互作用指标 | `usi`, `bni` | benzene/phenol dimer、GC 碱基对、Ag(111)+benzene | 有入口 | 已有 source-backed `iuserfunc=819/820` 路由和 preset，低密度尖峰需真实 cube range 调参后再出图 |
| 反应性 | `fod`, `orbital-weighted-fukui-*`, `orbital-weighted-dual-descriptor` | 小分子反应位点 | 有入口 | 需要真实 closed-shell 测试体系 |
| 局部信息熵 | `local-information-entropy` | 小分子/COF | 有入口 | 缺图，默认 isosurface 需调 |
| 分区权重 | `becke`, `hirshfeld` | 分子内片段边界 | 有入口 | 缺图 |
| pair/source function | `pair-function`, `source-function` | 选参考点的键/孤对电子区域 | 有入口 | 缺交互式参考点选择体验 |

## cube-preset 预设覆盖

| 预设组 | 代表 preset | 状态 | 补图建议 |
| --- | --- | --- | --- |
| density/signed/orbital | `density`, `signed`, `orbital-density` | 有 VESTA/cube | benzene HOMO/LUMO |
| spin/potential/KED | `spin-density`, `potential`, `kinetic-energy-density`, `ked-difference`, `ked-local-temperature`, `ked-potential` | 有入口 | open-shell、ABACUS out_pot 和 H2O/benzene KED diagnostics |
| ABACUS direct cube | `partial-charge`, `wavefunction-norm`, `elf` | 有入口 | 准备 ABACUS 小体系 direct cube |
| IRI/DORI/IGMH/aIGM | `iri`, `dori`, `igmh`, `aigm` | IGMH 已闭环；IRI 有调试图 | IRI/DORI/aIGM 补手册级图 |
| RoSE/SEDD | `rose`, `sedd` | 有入口 | 用 benzene dimer 或 GC 配对渲染慢电子/SEDD 等值面 |
| information/Ghosh/Renyi/USI/BNI | `information-gain-density`, `shannon-entropy-density`, `fisher-information-density`, `second-fisher-information-density`, `ghosh-entropy-density`, `renyi-entropy-density`, `usi`, `bni` | 有入口 | 用 benzene dimer、GC、COF 或 Ag(111)+benzene 调 cube range 后补图 |
| ESP/ALIE/LEA/vdW map | `esp`, `alie`, `lea`, `leae`, `vdw-map` | 有 VESTA/cube | 先补 ESP/ALIE surface extrema |
| domain/basin | `domain`, `basin`, `basin-type` | 有 VESTA/cube | 渲染 H2O domain 和 basin 示例 |
| vdW components | `vdw-potential`, `vdw-repulsion-potential`, `vdw-dispersion-potential` | 有入口 | 用同一体系展示 total/repul/disp |

## 近期闭环优先级

1. `ag111_benzene_extended_fields`: 复用已 ready 的 Ag(111)+benzene Molden、cell 和三视图相机，补 ESP/vdW/electric-field/steric/SBL/STM 至少一张 scalar-field PNG。
2. `benzene_dimer_scalar_suite`: 用 benzene dimer 或 phenol dimer 一次性覆盖 IRI/RDG/DORI/Delta-g、RoSE/SEDD、vdW 和 on-top pair density 的弱相互作用图。
3. `gc_weak_interaction_suite`: 在已 ready 的 GC AIM 上补 IRI/ESP/surface-extrema/on-top pair density，形成完整氢键教程。
4. `cof_direct_cube_suite`: 给 COF_12000N2 单层补 ABACUS direct density/potential/ELF/partial-charge/wavefunction-norm 的真实材料 cube 图。
5. `fukui_dual_reactivity`: 准备 coronene、nitro/hetero aromatic 或类似三态反应性体系的同网格 neutral/anion/cation density cube，闭合 `fukui-run`、`cube-arith` 和 atom coloring 主线。
6. `spin_atom_coloring_suite`: 用 C4H8 diradical、triplet 小分子、磁性氧化物或 spin-polarized adsorbate 替换 toy Fe smoke，补 spin-density 和原子电荷/磁矩染色图。
7. `h2o_domain_baseline`: 作为低风险 quick win，渲染 H2O density domain 和一张基础 density/ESP/KED 图；继续保护根目录未跟踪 `domain.cub` / `domain.pdb`，不把它们误提交。
8. Cd/Cl 轨迹: 继续补 ASE `.traj` 直接读取和不抢焦点 VESTA PNG 渲染层；现有 `trajectory-frames` 和 `trajectory-video` 已可作为 ready 基线。
9. 再考虑新增 Multiwfn 源码功能路线；在中文手册闭环前，不优先扩展新功能。
