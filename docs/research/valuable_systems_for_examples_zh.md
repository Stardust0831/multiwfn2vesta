# 真实算例体系选择依据

本文件记录当前 example 队列为什么优先这些体系。它不是文献综述，只用于避免后续为了补图而回到 toy
体系。

## 选择原则

- 一个体系优先覆盖多条维护流程，例如 ABACUS Molden、Multiwfn grid、AIM/IGMH 和 VESTA 三视图。
- 体系本身要有清楚物理问题：吸附、氢键、芳香堆积、二维多孔材料、反应性或自旋/电荷分布。
- 项目内只提交轻量 runbook、manifest、小输入和精选 PNG；大 wavefunction、cube、mp4 和临时 `.vesta`
  留在 `smoke/` 或本地计算目录。
- 没有真实 PNG 前保持 `needs-render` / `needs-example`，不把 toy 或调试图提升成手册级图。

## 当前优先体系

| 体系 | 对应 example | 主要闭环功能 | 选择依据 |
| --- | --- | --- | --- |
| Ag(111)+benzene | `ag111_benzene_igmh_aim` / `ag111_benzene_extended_fields` | ABACUS LCAO Molden、Molden `[Nval]` 检查、IGMH、AIM、vdW/ESP/steric/SBL/STM、三视图 | 芳香分子在金属 (111) 面上的吸附是表面科学典型问题；benzene on metals 的 DFT/vdW 研究明确讨论了从 Ag/Au 弱吸附到 Pt/Rh 强吸附的差异，适合展示吸附界面的弱相互作用和电性场。 |
| GC 碱基对 | `gc_aim` / `gc_weak_interaction_suite` | AIM 键径/BCP、IRI/RDG、ESP-on-density、surface extrema、on-top pair density、USI/BNI | GC 有三个氢键，是紧凑且可解释的分子间相互作用体系；AIM 路径和 BCP 能直接对应氢键拓扑，后续 IRI/ESP/信息论场也有明确解释对象。 |
| benzene dimer / phenol dimer | `benzene_dimer_scalar_suite` | IRI/RDG/DORI/Delta-g、RoSE/SEDD、vdW components、on-top pair density、information-density、USI/BNI | 芳香二聚体是弱相互作用和 pi-stacking 的经典小体系，比 H2O 玩具体系更适合作 paired scalar panel；phenol dimer 可作为有氢键和芳香面的公开 fallback。 |
| COF_12000N2 单层 | `cof_direct_cube_suite` | ABACUS direct density/potential/ELF/partial-charge/wfc norm、原子电荷染色、周期 cell/真空层 | COF 是二维/多孔晶态共价材料，能同时测试周期结构、孔道、真空层、direct cube 和原子染色，适合作材料侧手册图。 |
| 杂原子芳香分子或 coronene | `fukui_dual_reactivity` | neutral/anion/cation density cube、Fukui+/Fukui-/dual descriptor、condensed atom coloring | 反应性图需要电荷态和同网格 cube；带杂原子或大芳香体系能比小 toy 分子更清楚地展示反应位点差异。 |
| open-shell/磁性体系 | `spin_atom_coloring_suite` | spin density、alpha/beta density、spin-polarization、Mulliken charge/magnetism coloring | 只有真实自旋或磁矩分布时，原子颜色和 spin-density 才有解释价值；当前 Fe toy 只能保留为 parser smoke。 |
| Cd/Cl 轨迹 | `cdcl_trajectory_video` | trajectory frames、Boundary、SBOND、reference VESTA style、高码率 MP4 | 这个体系已经有真实 NVT/NPT frame 和视频证据，适合作 VESTA 批处理与视频合成的维护基线。 |

## 外部资料

- Benzene on metal (111) surfaces: https://arxiv.org/abs/1209.4345
- Larger aromatics on Ag(111) and vdW effects: https://arxiv.org/abs/1612.06612
- Benzene dimer / S22 weak-interaction benchmark context: https://arxiv.org/abs/1404.2585
- GC base-pair background: https://en.wikipedia.org/wiki/Base_pair
- COF background and applications: https://en.wikipedia.org/wiki/Covalent_organic_framework

这些资料只用于体系优先级判断；项目最终 example 的权威状态仍以
`multiwfn2vesta examples --summary`、`multiwfn2vesta examples --coverage`
和 `docs/example_status_matrix_zh.md` 为准。
