# Multiwfn-VESTA Interface 使用指南

## 安装
```bash
pip install -e .
```

## 基本使用
当前包名是 `multiwfn2vesta`。下面旧命令中的 `multiwfn_vesta` 是早期草稿名，
当前批处理主入口仍在施工中，`multiwfn2vesta.main` 还不能作为稳定 CLI 使用。

当前已验证可用的命令是 AIM paths/CPs 到 atoms-only VESTA 的转换器：

```bash
PYTHONPATH=src python -m multiwfn2vesta.aim_vesta \
  paths.pdb \
  aim_atoms_only.vesta \
  --cps-pdb CPs.pdb \
  --title "AIM paths and CPs"
```

如果这个 AIM 图层要叠到 VESTA 直接打开的 Multiwfn/Gaussian cube 上，需要加
cube-frame 平移；当前实现按 cube header origin 单位为 Bohr 处理：

```bash
PYTHONPATH=src python -m multiwfn2vesta.aim_vesta \
  paths.pdb \
  aim_atoms_only_cube_frame.vesta \
  --cps-pdb CPs.pdb \
  --cube-frame-from-cube molecule_IRI2.cub
```

默认半径按 Multiwfn 自带 `AIM.vmd` 的比例：路径点 `0.02`，四类 CP
包括 BCP 都是 `0.07`。若某张图确实需要强化某类点，可以显式传：

```bash
PYTHONPATH=src python -m multiwfn2vesta.aim_vesta \
  paths.pdb \
  aim_atoms_only_emphasis.vesta \
  --cps-pdb CPs.pdb \
  --path-radius 0.04 \
  --cp-radius 0.14 \
  --bcp-radius 0.20
```

## AIM paths 到无键 VESTA

这会生成 atoms-only `.vesta`：`SBOND` 为空，`BONDS   0`，避免 VESTA 对
Multiwfn `paths.pdb` 中密集的伪 C 原子自动成键。

旧草稿命令 `python -m multiwfn_vesta ...` 和 `python -m multiwfn2vesta.main ...`
暂不应使用，直到入口模块和包导出完成修复。

## 输出
旧批处理目标计划在 `output/` 目录生成：
- 格点文件 (.cube)
- 多个视角的渲染图片 (.png)

当前 AIM converter 的输出路径由命令行第二个参数指定，例如
`aim_atoms_only.vesta`。

## AIM 叠层样式后处理

VESTA 把 AIM `.vesta` 作为第二 phase 导入并保存后，可能只保留基底分子
的全局 `ATOMT` 表，导致 AIM 的 C/N/O/F 伪原子颜色回退。保存 merged 文件
后可运行：

```bash
PYTHONPATH=src python -m multiwfn2vesta.vesta_aim_style \
  merged.vesta \
  merged_aim_style.vesta
```

此外，BCP 通常靠近原子核。若基底分子使用 VDW 大球显示，BCP 会被原子球
遮挡；AIM 图建议使用较小的基底原子/键半径。

## AIM+IGMH 可复用叠层流程

对于已经在 VESTA 中保存好的结构/IGMH cube + AIM path/BCP 多 phase
`.vesta`，现在有稳定的高层 CLI：

```bash
PYTHONPATH=src python -m multiwfn2vesta.aim_igmh_vesta \
  input_overlay.vesta \
  output_dir
```

默认会生成：

- `<output_dir>/<stem>_styled.vesta`
- `<output_dir>/<stem>_aim_igmh_recipe.md`
- 复制到输出目录的相对 cube 依赖，例如 `dg_inter.cub` 和 `sl2r.cub`

默认样式来自 Ag(111)+苯 IGMH+AIM 的已验证经验：

- AIM 键径点统一用黄色 `Xe`，半径 `0.0600`
- BCP 用橙色 `Rn`，半径 `0.1800`
- 默认清空 AIM phase 的 `SBOND`，但保留真实结构的 `BONDS   1`
- 默认把 BCP 拆到最后一个 phase；不移动坐标，不删除和 BCP 重合的路径点
- 默认写 markdown recipe，记录样式参数、cube 依赖和渲染命令

需要编号 BCP 时：

```bash
PYTHONPATH=src python -m multiwfn2vesta.aim_igmh_vesta \
  input_overlay.vesta \
  output_dir \
  --label-bcp-sites
```

这会把 BCP site 名改成 `BCP1`、`BCP2` 等，并启用 VESTA `LABEL 1`。
VESTA 原生 label 可能重叠，正式图仍可考虑 PNG/SVG 后处理标注。

需要导出三视图时必须显式开启，因为 Windows VESTA 自动化仍会抢鼠标：

```bash
PYTHONPATH=src python -m multiwfn2vesta.aim_igmh_vesta \
  input_overlay.vesta \
  output_dir \
  --render-three-views \
  --initial-view top \
  --extra-rotate top x -8 \
  --scale 2
```

三视图主流程遵守“一个 `.vesta` 载入一次”的约束：调用
`scripts/vesta_three_views.py` 的 `cli-rotate` 模式，通过 VESTA CLI
`-rotate_*`、`-flush` 和 `-export_img` 导出 front/right/top。不会把三个
持久化 front/right/top `.vesta` 文件作为主产物。

Ag(111)+苯 dry smoke 产物：

```text
smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/reusable_cli_smoke_20260610/
```

这次 smoke 只验证样式、cube 复制和 manifest，没有启动 VESTA 渲染。
