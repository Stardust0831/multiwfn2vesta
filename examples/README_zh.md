# multiwfn2vesta examples 规划

当前 `examples/` 目录还没有把所有 smoke 产物整理成可复跑的正式算例。本文件先作为中文入口，说明哪些
真实体系已经有证据、哪些适合作为下一批正式 examples。

可以用统一 CLI 查看当前 curated examples：

```bash
multiwfn2vesta examples
multiwfn2vesta examples --status ready
multiwfn2vesta examples --coverage
multiwfn2vesta examples --needs-render
multiwfn2vesta examples --command grid-run
multiwfn2vesta examples --gallery-assets
multiwfn2vesta examples --systems
multiwfn2vesta examples --verify
```

新增正式 example 时先参考 `_template/README_zh.md`。每个 example 应尽量有独立
`examples/<example_id>/README_zh.md`，不要长期只挂在本总规划文件下；大体积 cube、
mp4、临时 `.vesta` 留在 `smoke/`，项目内只提交 runbook、manifest、小输入和精选 PNG。

## 可先整理成正式 example 的体系

| 优先级 | 体系 | 目标功能 | 现有证据 | 下一步 |
| --- | --- | --- | --- | --- |
| 1 | Ag(111)+benzene | ABACUS Molden -> Multiwfn IGMH+AIM -> VESTA 三视图 | `../../smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/`，已复制 gallery 图 | 整理输入清单、命令记录、输出说明；后续重渲染更紧凑视角 |
| 2 | GC 碱基对 | AIM paths/BCP overlay | `../../smoke/20260605_sob445_more_aim_examples/gc/`，已复制 gallery 图 | 做一个轻量 AIM 教程 example |
| 3 | benzene | AIM 基础例和 NICS/vector misc | `../../smoke/20260605_sob445_more_aim_examples/benzene/`，`../../smoke/20260605_nics_vesta_vectors/` | AIM 可入主线；NICS/vector 仅放 misc |
| 4 | Cd/Cl 轨迹 | XYZ/extXYZ trajectory -> VESTA frames -> PNG -> mp4 | `../../smoke/vesta_trajectory_video_1608/ase_nvt_refstyle_stride20_cdcl3p50/`，`cdcl_trajectory_video/cdcl_tiny.extxyz` | 已有 `trajectory-frames` 和 `trajectory-video`；下一步补 ASE `.traj` 读取和 VESTA PNG 渲染 |
| 5 | Ag(111)+benzene 扩展场 | vdW/ESP/electric-field/steric/SBL/STM | `ag111_benzene_igmh_aim` 已有三视图 | 见 `ag111_benzene_extended_fields/README_zh.md`，复用同一相机补 scalar-field 图 |
| 6 | benzene dimer | IRI/RDG/DORI/Delta-g、RoSE/SEDD、vdW、on-top pair density | 当前只有 CLI/preset/test；暂无正式 smoke 图 | 见 `benzene_dimer_scalar_suite/README_zh.md`，用 validated Molden 渲染 paired figure |
| 7 | GC 碱基对扩展 | IRI/RDG、ESP-on-density、surface extrema、on-top pair density | `gc_aim` 已有 AIM overlay | 见 `gc_weak_interaction_suite/README_zh.md`，在同一体系上补弱相互作用图 |
| 8 | COF_12000N2 单层 | ABACUS direct density/potential/ELF/partial charge/wfc norm | 当前只有体系规划 | 见 `cof_direct_cube_suite/README_zh.md`，只提交轻量 runbook/PNG |
| 9 | 杂原子芳香分子 | Fukui/dual descriptor、cube-arith、atom coloring | 当前缺三态同网格 cube | 见 `fukui_dual_reactivity/README_zh.md` |
| 10 | open-shell/磁性体系 | spin density、Mulliken magnetism、atom table coloring | 只有 Fe toy smoke | 见 `spin_atom_coloring_suite/README_zh.md`，换真实体系 |
| 11 | H2O 小体系 | domain-run、density/ESP/KED baseline | 当前有本地 domain 探针经验 | 见 `h2o_domain_baseline/README_zh.md`，注意不要提交根目录 `domain.cub` / `domain.pdb` |
| 12 | 短轨迹体系 | aIGM/amIGM trajectory-average weak interaction | 轨迹视频主例是 Cd/Cl，但 aIGM 仍缺图 | 见 `short_aigm_trajectory/README_zh.md` |

## 暂不作为完成 example 的体系

| 体系 | 原因 | 后续要求 |
| --- | --- | --- |
| H2O-HF IRI+AIM | 当前图更像 surface/texture 调试证据，IRI 等值面和 AIM 叠图还不够清楚 | 继续解析 VESTA `SURFS`/`SECTS`/`TEX3P` 并重渲染 |
| phenanthrene AIM | 当前视角信息量弱，接近边看 | 重新设平面/斜视视角后再放入手册 |
| ABACUS Mulliken coloring Fe toy | 只是解析和 SITET 着色 smoke，不是有化学意义展示 | 换真实磁性或带电体系，补 PNG、色标和图例 |

## 功能到 example 的当前映射

`multiwfn2vesta examples --coverage` 是权威索引。当前未闭环功能先映射到这些
planned examples，等真实 PNG 生成后再把状态提升为 `ready`：

| example id | 覆盖功能 |
| --- | --- |
| `ag111_benzene_extended_fields` | Ag(111)+benzene 上的 ESP、电场、vdW、steric/SBL、STM |
| `benzene_dimer_scalar_suite` | IRI/RDG/DORI/Delta-g、RoSE/SEDD、vdW、on-top pair density |
| `gc_weak_interaction_suite` | GC AIM 扩展到 IRI/RDG、ESP、surface extrema、on-top pair density |
| `cof_direct_cube_suite` | ABACUS direct density/potential/ELF/partial charge/wfc norm |
| `fukui_dual_reactivity` | `fukui-run`、`cube-arith`、dual descriptor、atom scalar coloring |
| `spin_atom_coloring_suite` | spin density、Mulliken magnetism、atom value coloring |
| `h2o_domain_baseline` | `domain-run` 和小分子 density/ESP/KED baseline |
| `short_aigm_trajectory` | `aigm-run` / `amigm-run` |

## 文档入口

- 中文手册: `../docs/manual_zh.md`
- 效果图库: `../docs/example_gallery_zh.md`
- 功能 example 状态矩阵: `../docs/example_status_matrix_zh.md`
- 功能到算例闭环索引: `../docs/feature_examples_zh.md`
