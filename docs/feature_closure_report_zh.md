# multiwfn2vesta 功能闭环报告

更新时间：2026-06-12 07:09 CST

本报告回答三个问题：

1. 现有功能应该用哪个真实体系作为 example。
2. 哪些功能已经有项目内真实 VESTA PNG，可以展示。
3. 哪些功能只有代码/测试/经验，还必须补真实渲染或真实输入链路。

命令入口：

```bash
multiwfn2vesta examples --closure-report
multiwfn2vesta examples --closure-report --json
multiwfn2vesta examples --coverage
multiwfn2vesta examples --needs-render
multiwfn2vesta examples --gallery-assets
```

当前原则：

- `ready` 只给真实体系、runbook 和项目内 PNG 都存在的功能。
- `linked` 表示功能被某个 ready workflow 间接覆盖，但还没有独立教程图。
- `needs-render` 表示 CLI、preset、测试或 smoke 经验存在，但缺手册级真实 PNG。
- `needs-example` 表示还缺完整真实输入链路。
- H2O-HF IRI+AIM、phenanthrene AIM、toy Mulliken coloring 只能作为调试或经验，不升级为 ready。

## 当前效果图

这张图只由已经提交的真实 VESTA 渲染 PNG 拼接而成，不包含 placeholder：

![ready feature closure map](assets/gallery/feature_closure_ready_map.png)

更紧凑的手册展示图：

![feature closure showcase](assets/gallery/feature_closure_showcase.png)

## 已有 ready/linked 功能

| 功能 | 状态 | 推荐 example | 代表体系 | 项目内图 |
| --- | --- | --- | --- | --- |
| `discover` | linked | 全部本地 workflow | 本工作区 Multiwfn/VESTA | 无，需要时记录命令输出 |
| `abacus-molden` | linked | `ag111_benzene_igmh_aim` | Ag(111)+benzene | `assets/gallery/ag111_benzene_igmh_aim_front.png` |
| `molden-check` | linked | `ag111_benzene_igmh_aim` | Ag(111)+benzene Molden，保留 `[Nval]` | Ag 三视图间接覆盖 |
| `cube-vesta` | linked | `h2o_hf_iri_aim_debug` / `cof_direct_cube_suite` | H2O-HF IRI cube，后续换 COF direct cube | `assets/gallery/h2o_iri_aim_overlay.png` 仅作调试证据 |
| `cube-preset` | linked | `ag111_benzene_igmh_aim` / `h2o_hf_iri_aim_debug` | Ag IGMH、H2O-HF IRI | Ag 三视图、IRI 调试图 |
| `igmh-run` / `igm-run` / `migm-run` | ready | `ag111_benzene_igmh_aim` | Ag(111)+benzene | Ag 三视图 |
| `aim-run` | ready | `gc_aim` | GC 碱基对 | `assets/gallery/gc_aim_overlay.png` |
| `aim-pdb` | ready | `gc_aim` / `benzene_aim` | Multiwfn `paths.pdb` / `CPs.pdb` | GC、benzene AIM 图 |
| `aim-igmh` | ready | `ag111_benzene_igmh_aim` | Ag(111)+benzene | Ag 三视图 |
| `trajectory-frames` | ready | `cdcl_trajectory_video` | Cd/Cl extXYZ 轨迹 | `assets/gallery/cdcl_nvt_trajectory_frame.png` |
| `trajectory-video` | ready | `cdcl_trajectory_video` | Cd/Cl VESTA PNG 帧序列 | Cd/Cl poster frame |
| `examples` | ready | 项目 example index | 当前 gallery | `assets/gallery/current_feature_overview.png` / `feature_closure_showcase.png` |

## 已有入口但缺真实渲染

这些功能已经有代码、测试、CLI 或 VESTA 经验，但不能标为 ready；下一步必须生成真实体系 PNG。

| 功能 | 推荐 example | 优先体系 | 下一步 |
| --- | --- | --- | --- |
| `surface-extrema` | `gc_weak_interaction_suite` | GC、phenol、氟/硝基芳香物、吸附界面 | 生成真实 `surfanalysis.pdb`，渲染 ALIE/LEA/LEAE extrema |
| `iri-run` | `h2o_hf_iri_aim_debug` / `benzene_dimer_scalar_suite` / `gc_weak_interaction_suite` | benzene dimer、GC、H2O-HF | 重渲染可见 IRI/RDG surface，确认 texture range |
| `grid-run` | `ag111_benzene_extended_fields` / `benzene_dimer_scalar_suite` / `h2o_domain_baseline` | Ag(111)+benzene、benzene dimer、H2O | 按 density/orbital/KED/ESP/vdW/FOD 等函数组补图 |
| `grid-run --function ked diagnostics` | `h2o_domain_baseline` / `benzene_dimer_scalar_suite` | H2O、benzene、Ag(111)+benzene | 渲染 selected KED、KED difference、local temperature、KED potential |
| `grid-run --function rose/sedd` | `benzene_dimer_scalar_suite` / `gc_weak_interaction_suite` | benzene dimer、GC | 用同一体系出 RoSE/SEDD paired figure |
| `grid-run --function steric/sbl` | `ag111_benzene_extended_fields` | Ag(111)+benzene、benzene dimer、GC | 渲染 steric/SBL potential、force、charge、energy-density |
| `grid-run --function on-top-pair-density` | `benzene_dimer_scalar_suite` / `gc_weak_interaction_suite` | benzene dimer、GC | 比较 `paircorrtype`，记录 cube range 后出单正值图 |
| `grid-run --function information-theory` | `benzene_dimer_scalar_suite` / `gc_weak_interaction_suite` / `cof_direct_cube_suite` | benzene dimer、GC、COF | 分开 signed 与单正值信息论场，记录等值面 |
| `grid-run --function usi/bni` | `benzene_dimer_scalar_suite` / `gc_weak_interaction_suite` / `ag111_benzene_extended_fields` | weak interaction 或 adsorption interface | 处理低密度尖峰后渲染 USI/BNI |
| `grid-run --function bonding/energy diagnostics` | `benzene_dimer_scalar_suite` / `gc_weak_interaction_suite` / `ag111_benzene_extended_fields` | benzene/phenol dimer、GC、Ag(111)+benzene | 渲染 shape function、average local ESP、bond metallicity、SCI/stiffness 等 |
| `stm-run` | `ag111_benzene_extended_fields` | Ag(111)+benzene 或表面芳香物 | 选 LDOS 能窗，渲染 constant-current surface |
| `domain-run` | `h2o_domain_baseline` | H2O density domain | 渲染二值 domain surface |
| `abacus-mulliken-color` | `spin_atom_coloring_suite` / `cof_direct_cube_suite` | 真实磁性或带电 ABACUS 体系 | 替换 toy Fe，补色标和 PNG |
| `multiwfn-atom-color` | `fukui_dual_reactivity` / `spin_atom_coloring_suite` | condensed Fukui、电荷或自旋原子表 | 接真实 atom scalar table 并渲染 |

## 还缺真实输入链路

| 功能 | 推荐 example | 需要准备什么 |
| --- | --- | --- |
| `cube-arith` | `fukui_dual_reactivity` | 同网格 neutral/anion/cation density cube 或 spin-resolved cube |
| `aigm-run` / `amigm-run` | `short_aigm_trajectory` | benzene dimer 或 Ag(111)+benzene AIMD 片段、fragment 定义、平均 IGM cube |
| `fukui-run` | `fukui_dual_reactivity` | neutral/anion/cation 三态波函数和统一网格 |

## 下一批最值得补成正式图的体系

1. Ag(111)+benzene：已经有 ABACUS Molden、IGMH+AIM、三视图相机，适合继续补 ESP/vdW/steric/SBL/STM 和 bonding/energy diagnostics。
2. GC 碱基对：AIM 已 ready，适合补 IRI/RDG、surface extrema、on-top pair density、SCI/stiffness。
3. benzene dimer 或 phenol dimer：适合弱相互作用标量场、RoSE/SEDD、vdW、USI/BNI、on-top pair density。
4. COF_12000N2 单层：适合 ABACUS direct density/potential/ELF/partial charge/wavefunction norm。
5. hetero aromatic 三态体系：适合 Fukui、dual descriptor、atom value coloring。
6. open-shell 或磁性体系：适合 spin density、Mulliken magnetism、generic atom-value coloring。

## 后续源码扩展候选

只读源码审计建议的后续增量，不属于本轮已有功能闭环：

- 偶极矩密度积分核 `iuserfunc=21/22/23`：适合极性芳香分子、GC、COF 官能团。
- 应力张量派生标量 `iuserfunc=116/117/118`：适合 GC、benzene dimer、Ag(111)+benzene 接触区。
- 能量密度梯度/拉普拉斯 `iuserfunc=79/80`：适合 Ag(111)+benzene、GC、COF 孔边缘。
- 方向 KED `iuserfunc=81-86`：适合 COF 单层或 slab，但坐标系依赖强。
- 局域 `|V(r)|/G(r)` 比值 `iuserfunc=35`：适合 H2O/benzene baseline、GC、Ag 界面，但要警惕低密度/节点。

这些候选进入代码前仍需补 preset、测试、真实体系说明和 `needs-render` 状态，不应直接标 ready。
