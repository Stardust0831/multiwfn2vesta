# Multiwfn-VESTA Interface 使用指南

## 安装
```bash
pip install -e .
```

## 基本使用
当前推荐入口是工作区内的统一 CLI。只需要把项目的 `bin` 目录加入 `PATH`：

```bash
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH
```

之后可以直接运行交互式向导：

```bash
multiwfn2vesta
```

也可以用子命令脚本化调用当前维护的流程：

```bash
multiwfn2vesta discover
multiwfn2vesta molden-check --help
multiwfn2vesta cube-vesta --help
multiwfn2vesta abacus-mulliken-color --help
multiwfn2vesta aim-run --help
multiwfn2vesta aim-pdb --help
multiwfn2vesta aim-igmh --help
```

已维护的子命令：

- `discover`: 报告 Multiwfn 和 VESTA 可执行文件候选，以及当前会选择的路径
- `molden-check`: 在调用 Multiwfn 前检查 Molden 文件是否含有必要段；ABACUS
  模式会要求 `[Cell]` 和 `[Nval]`
- `cube-vesta`: 从 ABACUS/Multiwfn scalar cube 直接生成 `.vesta`，可选
  texture/color cube，默认关闭 section plane
- `abacus-mulliken-color`: 读取 ABACUS `out_mul 1` 生成的 `mulliken.txt`，
  按原子 Mulliken 电荷或磁矩给 VESTA `SITET` 原子颜色赋值
- `aim-run`: 从 `.molden`、`.fch`、`.wfn` 等波函数文件调用 Multiwfn AIM，
  再把生成的 `paths.pdb`/`CPs.pdb` 转成 atoms-only `.vesta`
- `aim-pdb`: Multiwfn `paths.pdb`/`CPs.pdb` 转 atoms-only `.vesta`
- `aim-igmh`: 已保存的 AIM+IGMH 多 phase `.vesta` 叠层样式化，可选三视图导出

如果使用 editable 安装，也会安装同名 console script：

```bash
cd /mnt/g/work/multiwfn2vesta/project
pip install -e .
multiwfn2vesta --help
```

当前包名是 `multiwfn2vesta`。下面旧命令中的 `multiwfn_vesta` 是早期草稿名，
`multiwfn2vesta.main` 仍不是稳定入口；请使用 `multiwfn2vesta` 统一 CLI 或
明确的子命令模块。

## 可执行文件发现

先检查当前会调用哪个 Multiwfn 和 VESTA：

```bash
multiwfn2vesta discover
```

Multiwfn 查找顺序：

1. 命令行显式 `--multiwfn /path/to/Multiwfn_noGUI`
2. 环境变量：`MULTIWFN_PATH`、`MULTIWFNPATH`、`Multiwfnpath`、
   `MultiwfnPATH`、`MultiwfnPath`、`MULTIWFN_EXECUTABLE`
3. 工作区内已下载工具，优先 noGUI：
   `/mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI`
4. shell 的 `PATH`

VESTA 查找顺序：

1. 命令行显式 `--vesta-dir` 或相关渲染命令的显式路径
2. 环境变量：`VESTA_PATH`、`VESTA_DIR`、`VESTAPATH`、`VestaPATH`、
   `Vestapath`、`VESTA_EXECUTABLE`
3. 工作区内 VESTA：`tools/VESTA-win64/VESTA.exe` 和 Linux VESTA
4. shell 的 `PATH`

`aim-run` 本身只启动 Multiwfn，不启动 VESTA；VESTA 只在
`aim-igmh --render-three-views` 这种显式渲染命令里被调用。

## Cube 文件到 VESTA

ABACUS 的 `out_chg`、`out_pot`、`out_elf`、`out_pchg`、`out_wfc_*`，
以及 Multiwfn 导出的 density、ELF、IRI/RDG、ESP 等 cube，可以先走
通用 cube 入口：

```bash
multiwfn2vesta cube-vesta \
  density.cub \
  cube_products \
  --isosurface 0.01
```

对于实值轨道、实空间波函数、密度差、Fukui/dual descriptor 这类有正负号的
cube，可以直接写 VESTA 正负两张等值面：

```bash
multiwfn2vesta cube-vesta \
  orbital.cub \
  cube_products \
  --surface-mode signed \
  --isosurface 0.02
```

`--surface-mode signed` 会把 `--isosurface X` 当成幅值，分别写
`+abs(X)` 和 `-abs(X)` 两条 `ISURF` 记录。默认正值为黄色，负值为蓝色；
两条等值面都必须落在 cube 数据最小/最大值范围内。需要调色时可用
`--positive-rgb R G B`、`--negative-rgb R G B` 和
`--surface-opacity O1 O2`。

如果有一个表面 cube 和一个兼容的染色/texture cube：

```bash
multiwfn2vesta cube-vesta \
  IRI2_surface.cub \
  cube_products \
  --texture-cube IRI1_color.cub \
  --isosurface 1.0 \
  --tex-physical -0.04 0.04
```

如果颜色只应该按实际等值面附近的 texture 值缩放，而不是按整张 texture cube
的最大最小值缩放，可以显式开启 surface-band 参考范围：

```bash
multiwfn2vesta cube-vesta \
  IRI2_surface.cub \
  cube_products \
  --texture-cube IRI1_color.cub \
  --isosurface 1.0 \
  --tex-physical -0.04 0.04 \
  --tex-range-source surface-band
```

默认行为：

- 生成 `<output_dir>/<stem>_cube.vesta`
- 复制 surface/texture cube 到输出目录，避免 VESTA 渲染时找不到相对依赖
- 写 `<stem>_cube_vesta_recipe.md`
- 用 `IMPORT_DENSITY 1` 放表面 cube，用 `IMPORT_TEXTURE` 放染色 cube
- 用 `SECTS 0 0` 关闭 section plane
- 从 cube header 生成一个结构 phase；`--structure auto` 会在 origin 为零且
  原子落在 cube cell 内时用 `CRYSTAL`，否则用 `MOLECULE`

注意：`TEX3P` 在 VESTA 里按百分比/归一化状态处理，不是物理标量范围。
传 `--tex-physical -0.04 0.04` 时，程序会根据整张 texture cube 的最小/最大值
换算成百分比写入。传 `--tex-range-source surface-band` 时，程序会按
`abs(surface - isosurface)` 在一个窄带内筛选 texture 值来换算；如果窄带内没有
非退化范围，会用离等值面最近的一批格点作为 fallback。recipe markdown 会记录
实际采用的参考范围和采样点数。

## ABACUS Mulliken 原子着色

ABACUS LCAO 计算设置：

```text
out_mul 1
```

会在输出目录写 `mulliken.txt`。这个文件按 ionic step 和原子顺序给出每个
原子的 Mulliken population；当前 latest ABACUS `origin/develop` 格式中，
每个 step 以 `--- Ionic Step N ---` 开头，每个原子块含有
`Atom N is LABEL`、`total charge on atom N`，自旋体系还含有
`total magnetism on atom N`。

把最后一个 ionic step 的 Mulliken 电荷映射到 VESTA 原子颜色：

```bash
multiwfn2vesta abacus-mulliken-color \
  structure.vesta \
  mulliken.txt \
  structure_mulliken_charge.vesta \
  --property charge \
  --vmin -1 --vmax 1
```

对 `nspin=2` 的自旋极化输出，可按原子磁矩着色：

```bash
multiwfn2vesta abacus-mulliken-color \
  structure.vesta \
  mulliken.txt \
  structure_mulliken_mag.vesta \
  --property magnetism \
  --vmin -4 --vmax 4 \
  --write-values mulliken_values.csv
```

对 `nspin=4` 非共线输出，可选择 `magnetism-x`、`magnetism-y`、
`magnetism-z` 或 `magnetism-norm`。默认读取最后一个 ionic step；用
`--step N` 可指定某一步。映射默认按一基原子序号，而不是按元素名，因此
多个 Fe、Si、H 等重复标签不会产生歧义。底层仍是修改 VESTA `SITET` RGB，
不会让 VESTA 自动知道原始标量值或生成 colorbar。默认严格模式会要求所选
VESTA `STRUC` site index 与 Mulliken atom index 完全一致；只有明确想给
子集着色时才使用 `--non-strict`。

## 波函数文件到 AIM VESTA

ABACUS 生成的 Molden 文件建议先检查：

```bash
multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus
```

`--abacus` 会要求 `[Cell]`、`[Atoms]`、`[GTO]`、`[MO]` 和 `[Nval]`。对于
赝势体系，`[Nval]` 是关键段；缺失时 Multiwfn 可能把价电子波函数按全电子
核电荷解释。

从 Molden/FCHK/WFN 等 Multiwfn 可读波函数文件开始：

```bash
multiwfn2vesta aim-run \
  input.molden \
  aim_out \
  --timeout 180
```

默认输出写在 `aim_out/`：

- `multiwfn_aim_input.txt`: 实际喂给 Multiwfn 的 AIM 命令流
- `multiwfn.stdout.txt` / `multiwfn.stderr.txt`: Multiwfn 日志
- `paths.pdb`、`CPs.pdb`、`CPprop.txt`、`mol.pdb`: Multiwfn AIM 输出
- `aim_atoms_only.vesta`: 本项目转换出的无 AIM 键 `.vesta`

显式指定 Multiwfn：

```bash
multiwfn2vesta aim-run \
  input.fch \
  aim_out \
  --multiwfn /mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI
```

传入相对 `--multiwfn ./Multiwfn_noGUI` 时，程序会在启动 Multiwfn 前解析为
绝对路径；随后即使 Multiwfn 的 `cwd` 切到输出目录，也不会找错可执行文件。

Multiwfn 源码读取 `Multiwfnpath` 来找 `settings.ini`。本项目启动 Multiwfn
时会把 `Multiwfnpath`、`MULTIWFNPATH`、`MultiwfnPATH` 同步设置为所选
Multiwfn 可执行文件所在目录，避免外部环境残留路径影响本次运行。

如果 Multiwfn 返回 0 但没有生成 `paths.pdb`，`aim-run` 默认返回 CLI 退出码
`3` 并提示检查日志。确实只想保留 Multiwfn 原始退出码时，显式加：

```bash
multiwfn2vesta aim-run input.fch aim_out --allow-missing-paths
```

真实 H2O smoke：

```text
/mnt/g/work/multiwfn2vesta/smoke/multiwfn_aim_cli_smoke_20260610/h2o/
```

这次使用 `H2O.fch` 和工作区 noGUI Multiwfn，成功生成
`paths.pdb`、`CPs.pdb`、`mol.pdb` 和 `aim_atoms_only.vesta`。

当前已验证可用的命令是 AIM paths/CPs 到 atoms-only VESTA 的转换器：

```bash
multiwfn2vesta aim-pdb \
  paths.pdb \
  aim_atoms_only.vesta \
  --cps-pdb CPs.pdb \
  --title "AIM paths and CPs"
```

如果这个 AIM 图层要叠到 VESTA 直接打开的 Multiwfn/Gaussian cube 上，需要加
cube-frame 平移；当前实现按 cube header origin 单位为 Bohr 处理：

```bash
multiwfn2vesta aim-pdb \
  paths.pdb \
  aim_atoms_only_cube_frame.vesta \
  --cps-pdb CPs.pdb \
  --cube-frame-from-cube molecule_IRI2.cub
```

默认半径按 Multiwfn 自带 `AIM.vmd` 的比例：路径点 `0.02`，四类 CP
包括 BCP 都是 `0.07`。若某张图确实需要强化某类点，可以显式传：

```bash
multiwfn2vesta aim-pdb \
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
multiwfn2vesta aim-igmh \
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
multiwfn2vesta aim-igmh \
  input_overlay.vesta \
  output_dir \
  --label-bcp-sites
```

这会把 BCP site 名改成 `BCP1`、`BCP2` 等，并启用 VESTA `LABEL 1`。
VESTA 原生 label 可能重叠，正式图仍可考虑 PNG/SVG 后处理标注。

需要导出三视图时必须显式开启，因为 Windows VESTA 自动化仍会抢鼠标：

```bash
multiwfn2vesta aim-igmh \
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
