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

从零到第一张图建议走这条顺序：

1. 运行 `multiwfn2vesta discover`，确认当前 Multiwfn 和 VESTA 候选路径。
2. 运行 `multiwfn2vesta examples --status ready`，只看已经有真实体系和效果图的算例。
3. 运行 `multiwfn2vesta examples --coverage`，按功能查推荐体系、runbook、效果图和缺口。
4. 运行 `multiwfn2vesta examples --id ag111_benzene_igmh_aim --verify`，检查项目内 runbook 和 gallery 图是否齐全。
5. 打开对应 `examples/<example_id>/README_zh.md`，先复用已有命令和输出目录。
6. 若只是查看效果，直接看 `docs/assets/gallery/` 下的 PNG；若要复跑，则按 runbook 重新生成 `.cub`、`.vesta`、recipe 和可选 PNG/MP4。

目前最适合先看的三个 ready examples 是：

- `ag111_benzene_igmh_aim`：ABACUS LCAO Molden -> Multiwfn IGMH/AIM -> VESTA 三视图。
- `gc_aim`：GC 碱基对 AIM 键径和 BCP 叠图。
- `cdcl_trajectory_video`：Cd/Cl 轨迹帧、Boundary/成键判据和高码率视频合成。

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
multiwfn2vesta examples --id cdcl_trajectory_video
multiwfn2vesta examples --coverage
multiwfn2vesta examples --needs-render
multiwfn2vesta examples --verify
multiwfn2vesta examples --id cdcl_trajectory_video --verify-smoke
```

`--verify` 只检查项目内已提交的 runbook 和 gallery 图片是否存在，不要求本机必须有完整 `smoke/`
历史目录。`--id` 可以只看一个算例；`--verify-smoke` 会检查工作区本地 `smoke/` 证据，例如高码率
mp4、PNG 序列或中间 VESTA frame，这些大文件默认不提交。需要程序读取时可以用：

```bash
multiwfn2vesta examples --json
multiwfn2vesta examples --coverage --json
```

`--coverage` 的粒度是功能，而不是单个体系。它会回答某个 CLI 命令现在应该用什么体系演示、
有没有手册级 PNG、缺的是渲染还是缺真实体系。只想看还没闭环的功能时用：

```bash
multiwfn2vesta examples --needs-render
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
| XYZ/extXYZ 轨迹 | `trajectory-frames` | per-frame `.vesta` + manifest + recipe | 不启动 VESTA 的轨迹 frame 生成 |
| 已渲染 PNG 轨迹帧 | `trajectory-video` | ffmpeg frame list + mp4 + recipe | VESTA 轨迹视频合成 |
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
- `esp`, `electron-esp`, `positive-esp`, `negative-esp`, `electric-field-magnitude`
- `alie`, `local-electron-affinity`, `local-electron-attachment-energy`
- `vdw-potential`, `vdw-repulsion-potential`, `vdw-dispersion-potential`
- `iri`, `rdg`, `dori`
- `rose`, `sedd`
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

若只想看电子贡献 ESP、ESP 的正/负区域或电场强度，不需要手工改 Multiwfn
`settings.ini`，直接用命名路由：

```bash
multiwfn2vesta grid-run input.molden esp_components --function electron-esp
multiwfn2vesta grid-run input.molden esp_components --function positive-esp
multiwfn2vesta grid-run input.molden esp_components --function negative-esp
multiwfn2vesta grid-run input.molden efield --function electric-field-magnitude
multiwfn2vesta grid-run input.molden slow_electron --function rose
multiwfn2vesta grid-run input.molden sedd_field --function sedd
```

这些命名路由都走 Multiwfn 函数 `100`，分别写 run-local
`iuserfunc=14/101/102/103` 或 RoSE/SEDD 的 `iuserfunc=18/19`，不会修改全局 Multiwfn 配置。`electron-esp`
调用 Multiwfn 源码中的 `eleesp(x,y,z)`，即电子贡献静电势，通常按单负
`-0.05` a.u. 等值面显示；正/负 ESP 分量适合在极性分子、吸附界面或电荷转移
体系中快速分开看静电正负区域；电场强度适合看局域强场区域。若要映射到 density
surface 上，再加
`--surface-cube density.cub --tex-physical MIN MAX`。
RoSE 用 `(Dh-G)/(Dh+G)` 描述慢电子区域，SEDD 用 `log(1+epsilon)` 描述单指数衰减偏离；
两者当前已有 CLI 和 VESTA preset，但还缺真正适合手册的效果图。后续优先用 benzene dimer、
GC 碱基对或类似弱相互作用/芳香体系生成 paired figure，而不是 toy cube。

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

## 9.1 XYZ/extXYZ 轨迹生成 VESTA frame

`trajectory-frames` 是轨迹视频工作流的上游维护入口：读取标准 XYZ 或带 `Lattice="..."`
的 extXYZ，直接写逐帧 `.vesta` 文件、manifest 和 recipe。它不依赖 ASE，不启动 VESTA，也不渲染 PNG，
因此适合先批量生成结构帧，再在方便时用 VESTA 或其它渲染层导出图片。

Cd/Cl 最小 example：

```bash
multiwfn2vesta trajectory-frames examples/cdcl_trajectory_video/cdcl_tiny.extxyz \
  /tmp/cdcl_vesta_frames \
  --bond Cd Cl 0 3.5 \
  --boundary -0.05 1.05 -0.05 1.05 -0.05 1.05
```

常用选项：

- `--reference-vesta saved.vesta`: 复用已保存 VESTA 的 `SCENE`/`STYLE` 尾段，适合继承视角和显示风格。
- `--bond E1 E2 MIN MAX`: 写 VESTA `SBOND` 成键规则，可重复；Cd-Cl 轨迹常用 `0 3.5` 放宽判据。
- `--boundary XMIN XMAX YMIN YMAX ZMIN ZMAX`: 扩展周期显示范围，例如三个方向都用 `-0.05 1.05`。
- `--cell-vectors ...`: 普通 XYZ 没有 extXYZ `Lattice` 时手动给 9 个晶胞向量分量。
- `--stride N`: 只输出部分帧，便于先做预览。

输出包括：

- `vesta/frame_0001.vesta` 等逐帧 VESTA 文件。
- `frame_trajectory_frames_manifest.json`: 记录源轨迹、帧序号、Boundary、bond rules 和参考 `.vesta`。
- `frame_trajectory_frames_recipe.md`: 记录下一步 PNG 渲染和 `trajectory-video` 合成提示。

当前限制：

- 还不直接读取 ASE `.traj`；如果只有 ASE `.traj`，先导出 XYZ/extXYZ。
- 还不启动 VESTA 渲染 PNG；这一步仍然单独维护，以免自动化窗口抢焦点。

## 9.2 已渲染轨迹帧合成视频

`trajectory-video` 只处理已经渲染好的 PNG 序列，不启动 VESTA，因此不会抢鼠标。默认只写 ffmpeg
frame list 和 recipe，并打印命令；只有加 `--run` 才真的执行 ffmpeg。

```bash
multiwfn2vesta trajectory-video png_frames trajectory.mp4 \
  --fps 24 \
  --bitrate 20M

multiwfn2vesta trajectory-video \
  --manifest examples/cdcl_trajectory_video/artifact_manifest.json \
  --output /tmp/cdcl_trajectory.mp4 \
  --fps 24 \
  --bitrate 20M
```

输出包括：

- `<output>_frames.txt`: ffmpeg concat 输入清单。
- `<output>_trajectory_video_recipe.md`: 帧数、首尾帧、编码参数和完整命令。
- `<output>.mp4`: 只有使用 `--run` 且 ffmpeg 成功时生成。

仍待维护的是 ASE `.traj` 直接读取和 VESTA PNG 自动渲染；XYZ/extXYZ 到 `.vesta` frame 的部分已经由
`trajectory-frames` 维护。

## 10. 每个功能的 example 状态

详见：

- `docs/example_status_matrix_zh.md`
- `docs/feature_examples_zh.md`

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
