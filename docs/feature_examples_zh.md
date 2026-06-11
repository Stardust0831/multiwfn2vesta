# multiwfn2vesta 功能到算例闭环索引

本索引用来回答“某个功能现在应该拿什么真实体系演示、有没有效果图、下一步缺什么”。它和
`multiwfn2vesta examples --coverage` 保持同一套状态语言。

状态含义：

- `ready`: 已有正式 runbook 和项目内 gallery PNG，可以作为手册级示例。
- `linked`: 功能被某个 ready workflow 间接覆盖，但还没有独立教程图。
- `needs-render`: 代码路径和 smoke/经验已存在，需要补一张手册级效果图。
- `needs-example`: 还缺真实体系或完整输入输出链路。
- `misc`: 用户要求暂存或暂不进主代码的探索项。

## 快速命令

```bash
multiwfn2vesta examples --summary
multiwfn2vesta examples --coverage
multiwfn2vesta examples --needs-render
multiwfn2vesta examples --command grid-run
multiwfn2vesta examples --gallery-assets
multiwfn2vesta examples --systems
multiwfn2vesta examples --coverage --coverage-status ready
multiwfn2vesta examples --coverage --json
```

## 顶层功能覆盖表

| 功能 | 推荐体系 | 当前状态 | 项目内图 | 下一步 |
| --- | --- | --- | --- | --- |
| `discover` | 本工作区 Multiwfn/VESTA | linked | 无 | 如需教学截图，记录一段成功输出即可 |
| `abacus-molden` | Ag(111)+benzene ABACUS LCAO | linked | `assets/gallery/ag111_benzene_igmh_aim_front.png` | 把真实 ABACUS 目录结构和成功输出片段补进 runbook |
| `molden-check` | Ag(111)+benzene Molden，保留 `[Nval]` | linked | Ag 三视图间接覆盖 | 在中文手册加入一段成功检查输出 |
| `cube-vesta` | H2O-HF IRI surface cube，后续换 direct density cube | linked | `assets/gallery/h2o_iri_aim_overlay.png` 仅作调试证据；IGMH/IRI workflow 已间接覆盖 cube 写入 | 补一张独立 standalone cube 等值面图 |
| `cube-preset` | Ag(111)+benzene IGMH、H2O-HF IRI、ABACUS direct cube | linked | Ag 三视图、IRI 调试图 | 补 ABACUS charge density/potential/ELF/wavefunction norm 图 |
| `surface-extrema` | 极性芳香分子或吸附界面 ALIE/LEA/LEAE | needs-render | 无 | 真实生成 `surfanalysis.pdb` 后叠加 extrema |
| `cube-arith` | 反应性分子的 Fukui/dual 或 open-shell spin density | needs-example | 无 | 准备 charged-state 或 spin-resolved cube |
| `iri-run` | H2O-HF、GC 碱基对或 benzene dimer | needs-render | H2O-HF 调试图 | 重渲染清楚的 IRI 等值面和染色范围 |
| `igmh-run` / `igm-run` / `migm-run` | Ag(111)+benzene | ready | Ag 三视图 | 保留 Ag 为周期体系主例，另补小分子快速例 |
| `aigm-run` / `amigm-run` | benzene dimer 轨迹或 Ag(111)+benzene AIMD 片段 | needs-example | 无 | 生成短轨迹平均 IGM cube 并渲染 |
| `grid-run` | H2O、benzene、Ag(111)+benzene、未来 COF | needs-render | 无手册级图 | 按函数组补 density/orbital/KED/ELF/ESP/vdW/FOD 等图 |
| `grid-run --function ked diagnostics` | H2O、benzene、Ag(111)+benzene | needs-render | 无 | 已有 `iuserfunc=1201/1202/1203/1204/1210` CLI 和 preset；下一步渲染 selected KED、KED 差值、local temperature 或 KED potential 对照图 |
| `grid-run --function rose/sedd` | benzene dimer、GC 碱基对或类似弱相互作用/芳香体系 | needs-render | 无 | 已有 RoSE/SEDD CLI 和 preset；下一步在同一真实体系中渲染 paired figure |
| `grid-run --function steric/sbl` | Ag(111)+benzene、benzene dimer、GC 碱基对 | needs-render | 无 | 已有 steric/SBL/Pauli/quantum/electrostatic CLI 和 preset；下一步在界面或弱相互作用体系中渲染成组图 |
| `grid-run --function on-top-pair-density` | benzene dimer、GC 碱基对 | needs-render | 无 | 已有 `iuserfunc=36` CLI 和 preset；下一步比较 `paircorrtype` 后渲染电子对密度图 |
| `grid-run --function information-theory` | benzene dimer、GC 碱基对、小极性分子或 COF | needs-render | 无 | 已有 `iuserfunc=49/50/51/52/53/54/55/56/70/100` CLI 和专用 preset；`information-gain-density` 会先执行 promolecular 初始化，second-Fisher 是 signed preset；下一步渲染信息增益、Shannon/Fisher/Ghosh/Renyi/disequilibrium 组合图 |
| `grid-run --function usi/bni` | benzene/phenol dimer、GC 碱基对或 Ag(111)+benzene | needs-render | 无 | 已有 `iuserfunc=819/820` CLI 和 preset；下一步在弱相互作用或吸附界面体系中调 cube 范围后出图 |
| `fukui-run` | 带杂原子的芳香分子，中性/阴/阳离子三态 | needs-example | 无 | 先固定同一网格的三态 density cube |
| `stm-run` | 表面吸附小分子或芳香分子局域态 | needs-render | 无 | 选择 LDOS 能窗并渲染 constant-current surface |
| `domain-run` | H2O density domain 或 COF 孔道区域 | needs-render | 无 | 渲染二值 domain surface 并记录 criterion |
| `abacus-mulliken-color` | 磁性或带电 ABACUS 体系 | needs-render | 无 | 用真实 `mulliken.txt` 生成电荷/磁矩染色 PNG 和图例 |
| `multiwfn-atom-color` | Multiwfn 原子电荷或 condensed Fukui 表 | needs-render | 无 | 接真实 atom scalar table 并渲染 |
| `aim-run` | GC 碱基对、benzene | ready | `assets/gallery/gc_aim_overlay.png` | GC 做氢键主例，benzene 做基础例 |
| `aim-pdb` | Multiwfn `paths.pdb` / `CPs.pdb` | ready | GC、benzene AIM 图 | 补 CP 类型颜色说明 |
| `aim-igmh` | Ag(111)+benzene | ready | Ag 三视图 | 继续改善不抢焦点渲染和 camera preset |
| `trajectory-frames` | Cd/Cl extXYZ 轨迹 | ready | `assets/gallery/cdcl_nvt_trajectory_frame.png` | 后续补 ASE `.traj` 直接读取 |
| `trajectory-video` | Cd/Cl VESTA PNG frame 序列 | ready | Cd/Cl poster frame | 后续补不抢焦点 PNG 渲染层 |
| `examples` | 文档/算例发现入口 | ready | `assets/gallery/current_feature_overview.png`、`assets/gallery/feature_closure_showcase.png` | 继续把 smoke 逐步提升为正式 example |

## 推荐真实体系组合

当前最有价值、且能覆盖最多功能的体系组合如下：
选择依据另见 [真实算例体系选择依据](research/valuable_systems_for_examples_zh.md)。

1. Ag(111)+benzene 周期性吸附体系：覆盖 ABACUS Molden、Molden 检查、IGMH、AIM、AIM+IGMH 三视图、vdW/ESP 类 grid-run 后续扩展。
2. GC 碱基对：覆盖 AIM 氢键拓扑，适合继续补 IRI/RDG、ESP-on-density、surface extrema。
3. H2O-HF、benzene dimer 或 phenol dimer：覆盖 IRI/RDG、DORI、Delta-g、RoSE/SEDD 和小分子弱相互作用快速调试；H2O-HF 保留为 fast debug，benzene/phenol dimer 更适合手册主图。
4. COF_12000N2 单层加真空层：适合 ABACUS direct cube、电子密度、静电势、ELF/LOL、原子电荷染色。
5. coronene、nitro/hetero aromatic 或其它反应性芳香体系：适合 Fukui、dual descriptor、condensed Fukui/电荷原子染色。
6. 真实 open-shell 或磁性体系：适合 spin density、ABACUS Mulliken magnetism coloring、Multiwfn atom table coloring；C4H8 diradical/triplet 小分子或磁性氧化物都比当前 toy Fe smoke 更有展示价值。
7. Cd/Cl NVT/NPT 轨迹：覆盖 trajectory frame、reference VESTA style、Boundary、成键判据和高码率视频。

## 下一批正式 example 队列

后续把 `needs-render` / `needs-example` 提升为 `ready` 时，优先按下面这些
example id 落地。每个 example 都应先满足 `examples/_template/README_zh.md`
的最低清单，再把轻量 PNG 放进 `docs/assets/gallery/`；大 cube、mp4、`.vesta`
和波函数文件仍留在 `smoke/` 或本地计算目录，通过 manifest 引用。
这些 example id 已在 `multiwfn2vesta examples --status needs-work` 中注册，
对应 runbook 位于 `examples/<example_id>/README_zh.md`。

| 计划 example id | 体系 | 主要覆盖功能 | 当前可复用资产 | 验收缺口 |
| --- | --- | --- | --- | --- |
| `ag111_benzene_extended_fields` | Ag(111)+benzene 周期 slab | `abacus-molden`, `molden-check`, `igmh-run`, `aim-igmh`, vdW/ESP/steric/SBL/STM | 已有 Ag 三视图、ABACUS Molden、IGMH/AIM smoke | 为 vdW/ESP/steric/SBL/STM 生成同一视角下的真实 PNG，并记录 cube 范围和等值面 |
| `benzene_dimer_scalar_suite` | benzene dimer；公开 fallback 可用 phenol dimer | `iri-run`, RDG/DORI/Delta-g, RoSE/SEDD, vdW components, on-top pair density, information-density, USI/BNI | 目前无正式图 | 准备轻量 Molden/cube，渲染 paired weak-interaction/scalar figures |
| `gc_weak_interaction_suite` | GC 碱基对 | `aim-run`, `aim-pdb`, IRI/RDG, ESP-on-density, on-top pair density, information-density, USI/BNI, `surface-extrema` | `gc_aim_overlay.png` 和 GC AIM runbook | 在同一 GC 体系补 IRI/ESP/ALIE、LEA extrema、information-density、USI/BNI 或 on-top pair density 图 |
| `cof_direct_cube_suite` | COF_12000N2 单层或小 COF | `cube-vesta`, `cube-preset`, ABACUS density/potential/ELF/partial charge/wfc norm | 仅有 COF CIF 经验记录 | 跑 ABACUS 单点或复用 direct cube，渲染 density/potential/ELF 等图 |
| `fukui_dual_reactivity` | coronene、nitro/hetero aromatic 或其它三态反应性分子 | `cube-arith`, `fukui-run`, orbital-weighted Fukui/dual, atom scalar coloring | 无正式图 | 准备同网格 neutral/anion/cation density cube 和 condensed atom values |
| `spin_atom_coloring_suite` | C4H8 diradical、triplet 小分子、磁性氧化物或 spin-polarized adsorbate | spin density, `abacus-mulliken-color`, `multiwfn-atom-color` | 只有 toy/coloring smoke | 换真实 `mulliken.txt` 或 Multiwfn atom table，补 PNG 和色标说明 |
| `h2o_domain_baseline` | H2O 或小极性分子 | `domain-run`, KED/ESP 快速回归 | H2O domain/grid smoke | 渲染二值 domain 和基础 scalar 图，只作为快速 baseline |
| `short_aigm_trajectory` | benzene dimer 或 Ag(111)+benzene AIMD 片段 | `aigm-run`, `amigm-run`, trajectory-average weak interaction | 轨迹经验和 Cd/Cl video workflow | 准备短轨迹平均 IGM cube，并给一张 mapped-surface PNG |

## grid-run 函数组到示例

`grid-run` 功能很多，不应要求每个函数都单独维护一个大算例；更可维护的闭环方式是按物理含义分组：

| 函数组 | 推荐体系 | 展示方式 |
| --- | --- | --- |
| density、gradient、Laplacian | H2O 或 benzene | standalone isosurface；density 也作为 surface cube |
| orbital、orbital-density | benzene HOMO/LUMO | signed 或 orbital-density preset |
| spin-density、spin-polarization、alpha/beta density | open-shell/磁性体系 | signed spin-density surface，另配 atom coloring |
| KED、Thomas-Fermi、Weizsacker、Pauli KED、KED diagnostics | H2O/benzene | positive KED isosurface、signed KED difference、local temperature 或 KED potential；可映射到 density surface |
| ELF/LOL | COF 或芳香分子 | ELF/LOL 等值面，必要时配 density frame |
| ESP、electron-only ESP、positive/negative ESP、electric field magnitude | 极性分子、Ag(111)+benzene | potential surface 或 density surface texture；`electron-esp` 可拆出电子贡献 |
| ALIE/LEA/LEAE | 芳香分子反应位点 | surface texture + `surface-extrema` |
| vdW total/repulsion/dispersion | Ag(111)+benzene | density/interaction surface texture 或 standalone field |
| steric/SBL/Pauli/quantum potential/force/charge | Ag(111)+benzene、benzene dimer | 界面/分子间排斥与势场诊断；standalone field 或映射到 density/interaction surface |
| IRI/RDG/DORI/Delta-g | H2O-HF、benzene dimer | mapped surface，关闭 sections |
| RoSE/SEDD | benzene dimer、GC 碱基对 | 单正值等值面，先试 `0.5` 后按 cube 范围调参 |
| on-top pair density | benzene dimer、GC 碱基对 | 单正值等值面；可比较 `paircorrtype=1/2/3` |
| information gain / Shannon / Fisher / Ghosh / Renyi / disequilibrium | benzene dimer、GC、H2O 或 COF | 信息增益和 Shannon 用 signed surface；second-Fisher 用 signed surface；normal/phase-space Fisher、Ghosh/Renyi/disequilibrium 用单正值 surface |
| USI/BNI | benzene/phenol dimer、GC 或 Ag(111)+benzene | USI signed、BNI 单正值；低密度尖峰需用真实 cube range 调等值面 |
| FOD、orbital-weighted Fukui/dual | 反应性分子 | signed/single surface，配 condensed atom value coloring |
| Becke/Hirshfeld weights | 小分子/COF | standalone diagnostic surface，先作为高级例 |
| pair/source function | 选定键或孤对电子参考点 | 需要更好的参考点交互说明后再正式化 |

## 已渲染效果图

当前项目内总览图：

![current feature overview](assets/gallery/current_feature_overview.png)

当前手册用的 6-panel 闭环展示图：

![feature closure showcase](assets/gallery/feature_closure_showcase.png)

单图入口见 `docs/example_gallery_zh.md`。

CLI 入口补充：

- `multiwfn2vesta examples --summary`：快速汇总当前闭环度、ready examples、gallery 完整性和下一批优先体系。
- `multiwfn2vesta examples --command <命令或关键词>`：从某个功能反查推荐体系、状态和下一步。
- `multiwfn2vesta examples --gallery-assets`：只列出已提交的项目内 PNG，不检查本地大文件。
- `multiwfn2vesta examples --systems`：列出当前推荐真体系，帮助新 example 避免 toy placeholder。

## 后续高价值扩展候选

只读源码审计建议的下一批 Multiwfn function-100 路线：

- 扩展 KED 已维护: `iuserfunc=1201/1202/1203/1204/1210`，适合 KED 差值、局域温度和 KED potential；仍缺真实手册级 render。
- steric/SBL 场已维护核心无额外交互路线：`iuserfunc=40-43/60-69/-69/110-113`，适合吸附排斥和界面相互作用解释；damped steric `44-47` 暂未维护。
- on-top pair density 已维护：`iuserfunc=36`，适合电子对密度相关展示；需要真实 `benzene dimer` 或 GC 渲染后再标 ready。
- 信息论/Ghosh/Renyi/USI/BNI 路线已维护：`iuserfunc=49/50/51/52/53/54/55/56/70/100/819/820`；需要 benzene dimer、GC、COF 或 Ag(111)+benzene 的真实 render 后再标 ready。

这些候选暂时不阻塞当前“已有功能闭环”。优先级仍是先把 ready/needs-render 的现有功能补成清晰可复用算例。
