# multiwfn2vesta examples 规划

当前 `examples/` 目录还没有把所有 smoke 产物整理成可复跑的正式算例。本文件先作为中文入口，说明哪些
真实体系已经有证据、哪些适合作为下一批正式 examples。

可以用统一 CLI 查看当前 curated examples：

```bash
multiwfn2vesta examples
multiwfn2vesta examples --status ready
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

## 暂不作为完成 example 的体系

| 体系 | 原因 | 后续要求 |
| --- | --- | --- |
| H2O-HF IRI+AIM | 当前图更像 surface/texture 调试证据，IRI 等值面和 AIM 叠图还不够清楚 | 继续解析 VESTA `SURFS`/`SECTS`/`TEX3P` 并重渲染 |
| phenanthrene AIM | 当前视角信息量弱，接近边看 | 重新设平面/斜视视角后再放入手册 |
| ABACUS Mulliken coloring Fe toy | 只是解析和 SITET 着色 smoke，不是有化学意义展示 | 换真实磁性或带电体系，补 PNG、色标和图例 |

## 文档入口

- 中文手册: `../docs/manual_zh.md`
- 效果图库: `../docs/example_gallery_zh.md`
- 功能 example 状态矩阵: `../docs/example_status_matrix_zh.md`
