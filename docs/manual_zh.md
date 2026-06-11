# multiwfn2vesta 中文手册

本手册面向实际使用：从 ABACUS 或 Multiwfn 结果出发，把波函数分析、cube、AIM/IGM/IRI 等结果整理成
VESTA 可打开、可渲染、可复用视角的文件。当前项目仍是实验性工具，但推荐统一入口已经收敛到
`multiwfn2vesta`。

## 1. 基本入口

在仓库内使用：

```bash
cd /mnt/g/work/multiwfn2vesta/project
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH
multiwfn2vesta --help
multiwfn2vesta examples
```

也可以 editable 安装：

```bash
pip install -e .
multiwfn2vesta --help
```

不要在 `src/multiwfn2vesta/` 目录里直接运行 `python -m aim_igmh_vesta` 这类模块。需要脚本化时使用：

```bash
multiwfn2vesta <command> [options]
```

## 2. 先检查 Multiwfn 和 VESTA

```bash
multiwfn2vesta discover
```

Multiwfn 查找顺序是显式参数、环境变量、工作区工具、`PATH`。常见环境变量包括：

- `MULTIWFN_PATH`
- `MULTIWFNPATH`
- `MultiwfnPATH`
- `Multiwfnpath`
- `MULTIWFN_EXECUTABLE`

VESTA 查找顺序同理，常见环境变量包括：

- `VESTA_PATH`
- `VESTA_DIR`
- `VESTAPATH`
- `VestaPATH`
- `VESTA_EXECUTABLE`

大部分命令只写 `.vesta` 文件，不启动 VESTA；只有显式渲染三视图或图片时才会调用 VESTA。

## 3. 查看已有算例和效果图

推荐先看 curated examples：

```bash
multiwfn2vesta examples
multiwfn2vesta examples --status ready
multiwfn2vesta examples --status needs-work
multiwfn2vesta examples --verify
```

`--verify` 只检查项目内已提交的 runbook 和 gallery 图片是否存在，不要求本机必须有完整 `smoke/`
历史目录。需要程序读取时可以用：

```bash
multiwfn2vesta examples --json
```

## 4. 推荐工作流总览

| 起点 | 推荐命令 | 产物 | 典型用途 |
| --- | --- | --- | --- |
| ABACUS LCAO 计算目录 | `abacus-molden` | Multiwfn 可读 Molden | AIM、IGMH、IRI、grid-run、STM |
| ABACUS/Multiwfn cube | `cube-vesta` / `cube-preset` | `.vesta` + recipe | 密度、势、ELF、轨道、弱相互作用等值面 |
| Multiwfn 可读波函数 | `grid-run` | scalar cube + `.vesta` | density、orbital、ESP、KED、ELF/LOL、vdW、FOD 等 |
| neutral/anion/cation 波函数 | `fukui-run` | Fukui/dual cube + `.vesta` | 反应性区域 |
| 已有多个 cube | `cube-arith` | 线性组合 cube + `.vesta` | density difference、spin density、dual descriptor |
| 波函数 + fragment | `igmh-run` / `igm-run` / `migm-run` | `dg_inter.cub` + `sl2r.cub` + `.vesta` | 弱相互作用和片段相互作用 |
| 轨迹 + fragment | `aigm-run` / `amigm-run` | averaged IGM cubes + `.vesta` | 动力学平均弱相互作用 |
| 波函数 | `iri-run` | IRI/RDG cube pair + `.vesta` | NCI/IRI 弱相互作用 |
| 波函数 | `aim-run` | `paths.pdb`/`CPs.pdb` + `.vesta` | AIM 键径和临界点 |
| 已有 AIM PDB | `aim-pdb` | atoms-only AIM `.vesta` | 防止 VESTA 自动画大量 bond |
| 已保存 AIM+IGMH 叠图 | `aim-igmh` | styled `.vesta`，可选三视图 PNG | 周期体系相互作用图 |
| VESTA + 原子标量表 | `abacus-mulliken-color` / `multiwfn-atom-color` | colored `.vesta` | 电荷/磁矩/原子 Fukui 值染色 |

## 5. ABACUS 到 Multiwfn

ABACUS 需要 LCAO、单 Gamma/单 k、`nspin=1/2`，并输出 LCAO 波函数。推荐用最新 ABACUS
`interfaces/Multiwfn_interface/molden.py`，项目命令会导出 converter 并记录来源。

```bash
multiwfn2vesta abacus-molden abacus_calc ABACUS_Multiwfn.molden
multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus
```

ABACUS 伪势体系必须保留 `[Nval]`，这样 Multiwfn 看到的是有效价电子核电荷，而不是全电子原子序数。

## 6. Cube 到 VESTA

最通用入口：

```bash
multiwfn2vesta cube-vesta density.cub cube_products --isosurface 0.01
```

带正负号的轨道/差分/dual descriptor：

```bash
multiwfn2vesta cube-vesta orbital.cub cube_products \
  --surface-mode signed \
  --isosurface 0.02
```

表面 cube + 染色 cube：

```bash
multiwfn2vesta cube-vesta IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub \
  --isosurface 1.0 \
  --tex-physical -0.04 0.04 \
  --tex-range-source surface-band
```

常见分析优先用预设：

```bash
multiwfn2vesta cube-preset --list-presets
multiwfn2vesta cube-preset igmh dg_inter.cub products --texture-cube sl2r.cub
multiwfn2vesta cube-preset elf ELF.cub products
multiwfn2vesta cube-preset vdw-potential vdWpot.cub products
```

## 7. Multiwfn grid-run

`grid-run` 驱动 Multiwfn 主功能 `5`，从波函数生成一个实空间函数 cube，然后可选接 VESTA preset：

```bash
multiwfn2vesta grid-run input.molden grid_products \
  --function density \
  --grid-points 80 80 80 \
  --timeout 300
```

列出当前维护函数：

```bash
multiwfn2vesta grid-run --list-functions
```

高价值函数建议：

- `density`, `orbital`, `orbital-density`
- `spin-density`, `spin-polarization`, `alpha-density`, `beta-density`
- `laplacian`, `hamiltonian-ked`, `lagrangian-ked`, `thomas-fermi-ked`, `weizsacker-ked`, `pauli-ked`
- `elf`, `lol`
- `esp`, `alie`, `local-electron-affinity`, `local-electron-attachment-energy`
- `vdw-potential`, `vdw-repulsion-potential`, `vdw-dispersion-potential`
- `iri`, `rdg`, `dori`
- `fod`, `orbital-weighted-fukui-plus/minus/zero`, `orbital-weighted-dual-descriptor`
- `becke`, `hirshfeld`, `hirshfeld-delta-g`
- `pair-function`, `source-function`

若要把生成的属性 cube 映射到已有 density/surface cube：

```bash
multiwfn2vesta grid-run input.molden esp_map \
  --function esp \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub \
  --tex-physical -0.05 0.05
```

## 8. AIM、IRI、IGMH 的组合图

单独 AIM：

```bash
multiwfn2vesta aim-run input.molden aim_out
multiwfn2vesta aim-pdb aim_out/paths.pdb aim_atoms_only.vesta --cps-pdb aim_out/CPs.pdb
```

单独 IRI：

```bash
multiwfn2vesta iri-run input.molden iri_products --timeout 300
```

IGMH：

```bash
multiwfn2vesta igmh-run input.molden igmh_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --grid-mode spacing \
  --grid-spacing 0.25
```

已有 AIM+IGMH 叠图的样式化和三视图：

```bash
multiwfn2vesta aim-igmh input_overlay.vesta products \
  --label-bcp-sites \
  --render-three-views \
  --initial-view top \
  --extra-rotate top x -8 \
  --scale 2
```

经验规则：

- AIM 键径点作为 pseudo-atom 画，不要给 AIM phase 画 bond。
- BCP 单独拆到最后一个 phase 更容易显示。
- 结构 phase 保留正常 bond；AIM phase 的 `SBOND` 清空。
- IGMH/IRI 的 section plane 通常关闭。
- 三视图应从同一个 `.vesta` 一次载入后旋转导出，而不是改三份坐标。

## 9. 真实效果图

当前已整理的效果图库见：

- `docs/example_gallery_zh.md`
- `docs/assets/gallery/`

重点示例：

- Ag(111)+benzene IGMH+AIM 三视图
- GC 碱基对 / benzene AIM overlay
- Cd/Cl NVT 轨迹视频 poster frame 和高码率 mp4 记录
- H2O-HF IRI+AIM 调试证据
- benzene NICS arrow 杂项

## 10. 每个功能的 example 状态

详见：

- `docs/example_status_matrix_zh.md`

原则：

- 有真实 PNG/VESTA 的标为“已闭环”。
- 只有 cube/VESTA 但没有图片的标为“缺渲染”。
- 只有命令设计或单元测试的标为“缺真实体系”。
- 图已存在但不够适合手册展示的标为调试证据或待重调视角，不算完成。
- 暂不维护的 NICS/箭头作为 misc，不进入主功能完成度。

## 11. 常见问题

### VESTA 抢鼠标

当前 Windows VESTA CLI 渲染仍可能抢焦点。写 `.vesta` 文件不需要启动 VESTA；只有 `--render-three-views`
这类显式渲染才会打开 VESTA。若正在使用电脑，建议先只生成 `.vesta`，稍后批量渲染。

### 看不到 IRI 颜色

检查 `--tex-physical` 和 `--tex-range-source surface-band`。VESTA 的 `TEX3P` 需要百分比，项目会把物理范围按
texture cube 的实际范围换算。若 cube 已经被裁剪，通常用 `--tex-physical -0.04 0.04`。

### BCP 看不见

优先用 `aim-igmh` 的默认拆分 BCP phase。不要移动 BCP 坐标来解决视角问题；先调视角、缩放、phase 顺序和半径。

### ABACUS Molden 不能读

先跑：

```bash
multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus
```

重点检查 `[Cell]`、`[Atoms]`、`[GTO]`、`[MO]` 和 `[Nval]`。

### 某个功能还没有效果图

先在 `example_status_matrix_zh.md` 里找对应功能组。若状态是“缺渲染”或“缺真实体系”，不要直接用于展示型结果；
先补一个真实 smoke 目录、生成 VESTA，再导出 PNG。
