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
