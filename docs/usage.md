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
multiwfn2vesta examples --help
multiwfn2vesta examples --coverage
multiwfn2vesta abacus-molden --help
multiwfn2vesta molden-check --help
multiwfn2vesta cube-vesta --help
multiwfn2vesta cube-preset --help
multiwfn2vesta surface-extrema --help
multiwfn2vesta cube-arith --help
multiwfn2vesta iri-run --help
multiwfn2vesta igmh-run --help
multiwfn2vesta igm-run --help
multiwfn2vesta migm-run --help
multiwfn2vesta aigm-run --help
multiwfn2vesta amigm-run --help
multiwfn2vesta grid-run --help
multiwfn2vesta fukui-run --help
multiwfn2vesta stm-run --help
multiwfn2vesta domain-run --help
multiwfn2vesta abacus-mulliken-color --help
multiwfn2vesta multiwfn-atom-color --help
multiwfn2vesta aim-run --help
multiwfn2vesta aim-pdb --help
multiwfn2vesta aim-igmh --help
multiwfn2vesta trajectory-frames --help
multiwfn2vesta trajectory-video --help
```

已维护的子命令：

- `discover`: 报告 Multiwfn 和 VESTA 可执行文件候选，以及当前会选择的路径
- `examples`: 列出当前已整理的真实算例、gallery 图、runbook、状态矩阵；支持
  `--status ready/needs-work/misc`、`--id`、`--json`、`--verify` 和
  `--verify-smoke`；`--coverage` 按功能列出推荐真实体系、runbook、效果图状态和下一步；
  `--needs-render` 只列出缺手册级渲染或缺真实体系的功能；`--verify` 检查仓库内
  runbook/gallery/manifest，`--verify-smoke` 检查工作区本地大文件或历史渲染证据
- `abacus-molden`: 从 ABACUS LCAO 计算目录调用最新
  `interfaces/Multiwfn_interface/molden.py`，生成并验证给 Multiwfn 用的
  Molden 文件
- `molden-check`: 在调用 Multiwfn 前检查 Molden 文件是否含有必要段；ABACUS
  模式会要求 `[Cell]` 和 `[Nval]`
- `cube-vesta`: 从 ABACUS/Multiwfn scalar cube 直接生成 `.vesta`，可选
  texture/color cube，默认关闭 section plane
- `cube-preset`: 在 `cube-vesta` 后端上套用常见分析默认值，例如 density、
  orbital/signed、spin density、Laplacian、K(r)/G(r)、ABACUS direct
  potential、partial charge、wavefunction norm、ELF/LOL、IRI/RDG/NCI、DORI、
  EDR(r;d)、D(r)、IGM/IGMH/aIGM、ESP/MEP、electron-only ESP、positive/negative ESP、
  electric-field magnitude、ALIE/LEA/LEAE、userfunc/iuserfunc、selected KED variants、standalone vdW total/repulsion/
  dispersion potential、vdW map
- `surface-extrema`: 把 Multiwfn `surfanalysis.pdb` 的分子表面极值点作为
  atoms-only phase 叠加到已有 `.vesta` 文件中
- `cube-arith`: 对兼容 cube 做线性组合，用于 density difference、
  alpha-minus-beta spin density、Fukui function、dual descriptor 等后处理，
  并可直接接 `cube-preset` 写 `.vesta`
- `iri-run`: 从 Multiwfn 可读波函数文件调用 IRI/RDG 弱相互作用菜单，
  生成 `func1.cub`/`func2.cub`，处理成 VESTA 可用的 `IRI1`/`IRI2` cube，
  再通过 `cube-preset iri` 写 mapped-surface `.vesta`
- `igmh-run` / `igm-run` / `migm-run`: 从 Multiwfn 可读波函数文件和片段定义调用 IGMH、IGM 或 mIGM 菜单，
  导出 `dg_inter.cub`/`sl2r.cub`，保留可选 `dg_intra.cub`/`dg.cub`，
  再通过 `cube-preset igmh` 或 `cube-preset igm` 写 mapped-surface `.vesta`
- `aigm-run` / `amigm-run`: 从 Multiwfn 可读轨迹文件和片段定义调用 aIGM
  或 amIGM 轨迹平均菜单，导出 `avgdg_inter.cub`/`avgsl2r.cub`，可选
  `avgRDG.cub`、`thermflu.cub`、`output.txt`，再通过 `cube-preset aigm`
  或 `cube-preset aigm-tfi` 写 mapped-surface `.vesta`
- `trajectory-frames`: 从标准 XYZ 或 extXYZ 轨迹直接写逐帧 `.vesta`
  frame、manifest 和 recipe；支持 extXYZ `Lattice`、手动 cell vectors、
  Boundary、可重复 `SBOND` 规则和参考 `.vesta` 的 `SCENE`/`STYLE` 尾段；
  不启动 VESTA、不渲染 PNG
- `trajectory-video`: 从已经渲染好的 VESTA 轨迹 PNG 帧准备或执行高码率
  mp4 合成；默认只写 ffmpeg frame list 和 markdown recipe，不启动 VESTA
- `grid-run`: 从 Multiwfn 可读波函数文件调用主菜单 `5` 的 real-space
  function grid，导出 density、MO/orbital、Laplacian、K(r)/G(r)、ELF/LOL
  及其 `ELFLOL_type` 变体、
  ESP/MEP、electron-only ESP、positive/negative ESP、电场强度、ALIE、EDR(r;d)、D(r)、RDG/IRI-like、
  promolecular RDG/sign(lambda2)rho、function-100 alpha/beta density 和
  FOD、Thomas-Fermi/Weizsacker/Pauli KED 等单 cube，并可自动接
  `cube-preset` 写 `.vesta`
- `fukui-run`: 从中性、阴离子、阳离子波函数分别生成共享格点的 density
  cube，再调用 `cube-arith` 生成 Fukui+/Fukui-/dual descriptor cube 和
  可选 `.vesta`
- `stm-run`: 从含 GTO/GTF 信息的 Multiwfn 可读波函数文件调用主菜单 `300`
  的 STM 功能，切到 constant-current 模式，导出 `STM.cub`，并可自动接
  `cube-preset stm` 写 `.vesta`
- `domain-run`: 从已有 cube/grid 文件调用 Multiwfn 主菜单 `200` 的
  domain analysis，按 `<0.5` 这类判据导出 `domain.cub`/`domain.pdb`，
  并可自动接 `cube-preset domain` 写二值域等值面 `.vesta`
- `abacus-mulliken-color`: 读取 ABACUS `out_mul 1` 生成的 `mulliken.txt`，
  按原子 Mulliken 电荷或磁矩给 VESTA `SITET` 原子颜色赋值
- `multiwfn-atom-color`: 读取 Multiwfn 复制/导出的原子标量表，或手工整理
  的 CSV/TSV/空白表，按原子序号、VESTA label 或结构顺序给 VESTA `SITET`
  原子颜色赋值
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
multiwfn2vesta examples --status ready
multiwfn2vesta examples --coverage
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

`aim-run`、`iri-run`、`igmh-run`、`aigm-run`、`amigm-run`、`grid-run`、`fukui-run`、`stm-run` 和 `domain-run` 本身只启动 Multiwfn，不启动 VESTA；
VESTA 只在 `aim-igmh --render-three-views` 这种显式渲染命令里被调用。

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

如果只是想处理常见分析产物，推荐优先使用预设入口：

```bash
multiwfn2vesta cube-preset --list-presets
multiwfn2vesta cube-preset density density.cub cube_products
multiwfn2vesta cube-preset orbital orbital.cub cube_products
multiwfn2vesta cube-preset gradient-norm gradient.cub cube_products
multiwfn2vesta cube-preset orbital-density orbdens.cub cube_products
multiwfn2vesta cube-preset spin-density spindensity.cub cube_products
multiwfn2vesta cube-preset spin-polarization spindensity.cub cube_products
multiwfn2vesta cube-preset laplacian laplacian.cub cube_products
multiwfn2vesta cube-preset hamiltonian-ked 'K(r).cub' cube_products
multiwfn2vesta cube-preset lagrangian-ked 'G(r).cub' cube_products
multiwfn2vesta cube-preset kinetic-energy-density userfunc.cub cube_products
multiwfn2vesta cube-preset local-information-entropy infoentro.cub cube_products
multiwfn2vesta cube-preset electron-delocalization-range EDR.cub cube_products
multiwfn2vesta cube-preset orbital-overlap-distance EDRDmax.cub cube_products
multiwfn2vesta cube-preset pair-function fermihole.cub cube_products
multiwfn2vesta cube-preset source-function srcfunc.cub cube_products
multiwfn2vesta cube-preset user-function userfunc.cub cube_products
multiwfn2vesta cube-preset becke-weight Becke.cub cube_products
multiwfn2vesta cube-preset hirshfeld-weight Hirshfeld.cub cube_products
multiwfn2vesta cube-preset rdg-scalar RDG.cub cube_products
multiwfn2vesta cube-preset promolecular-rdg RDGprodens.cub cube_products
multiwfn2vesta cube-preset promolecular-delta-g Delta_g.cub cube_products
multiwfn2vesta cube-preset hirshfeld-delta-g griddata.cub cube_products
multiwfn2vesta cube-preset iri-scalar IRI.cub cube_products
multiwfn2vesta cube-preset dori-scalar userfunc.cub cube_products
multiwfn2vesta cube-preset vdw-potential vdWpot.cub cube_products
multiwfn2vesta cube-preset vdw-repulsion-potential userfunc.cub cube_products
multiwfn2vesta cube-preset vdw-dispersion-potential userfunc.cub cube_products
multiwfn2vesta cube-preset potential pot_es.cube cube_products
multiwfn2vesta cube-preset electron-esp userfunc.cub cube_products
multiwfn2vesta cube-preset partial-charge pchg.cube cube_products
multiwfn2vesta cube-preset wavefunction-norm wfc_norm.cube cube_products
multiwfn2vesta cube-preset elf ELF.cub cube_products
multiwfn2vesta cube-preset rdg IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub
multiwfn2vesta cube-preset dori DORI.cub cube_products \
  --texture-cube sl2r.cub
multiwfn2vesta cube-preset stm STM.cub cube_products
multiwfn2vesta cube-preset domain domain.cub cube_products
multiwfn2vesta cube-preset basin basin0001.cub cube_products
multiwfn2vesta cube-preset basin-type basinsyn.cub cube_products
multiwfn2vesta cube-preset igmh dg_inter.cub cube_products \
  --texture-cube sl2r.cub
multiwfn2vesta cube-preset esp density.cub cube_products \
  --texture-cube esp.cub \
  --tex-physical -0.05 0.05
multiwfn2vesta cube-preset alie density.cub cube_products \
  --texture-cube avglocion.cub \
  --surfanalysis-pdb surfanalysis.pdb
multiwfn2vesta cube-preset vdw-surface density.cub cube_products \
  --texture-cube vdW.cub
```

`cube-preset` 只负责选择默认值，实际写 `.vesta` 的逻辑仍走
`cube-vesta`。当前预设：

- `density`：单等值面，默认 `--isosurface 0.01`
- `gradient-norm`：单正值等值面，别名包括 `gradient`、`rho-gradient`、
  `grad-rho`，用于 Multiwfn `gradient.cub`；默认等值面 `0.05` 来自
  Multiwfn main-function-5 全局 `sur_value`，通常需要按体系微调
- `signed`：正/负等值面，别名包括 `orbital`、`wavefunction`、
  `density-difference` 和 `dual-descriptor`
- `orbital-density`：单正值等值面，别名包括 `orbdens`、`mo-density`，
  用于 Multiwfn `orbdens.cub`，默认等值面 `0.005`
- `spin-density`：正/负等值面，别名包括 `spin`、`spindensity`，用于
  Multiwfn `spindensity.cub` 或兼容的 signed spin-density cube，默认幅值
  `0.02`
- `spin-polarization`：正/负等值面，别名包括
  `spin-polarization-parameter`、`spin-pol`，用于 Multiwfn 函数 `5` 在
  `ipolarpara=1` 时导出的 `spindensity.cub`；物理量是
  `(rho_alpha-rho_beta)/(rho_alpha+rho_beta)`，默认幅值 `0.5`
- `laplacian`：正/负等值面，别名包括 `lap`、`laplacian-rho`，用于
  Multiwfn `laplacian.cub`，默认幅值 `0.05`，通常需要按体系微调
- `hamiltonian-ked`：正/负等值面，别名包括 `k(r)`、`kinetic-k`，用于
  Multiwfn `K(r).cub`，默认幅值 `0.01`
- `lagrangian-ked`：单正值等值面，别名包括 `g(r)`、`kinetic-g`，用于
  Multiwfn `G(r).cub`，默认等值面 `0.01`
- `kinetic-energy-density`：单正值等值面，别名包括
  `thomas-fermi-ked`、`weizsacker-ked`、`vw-ked`、`pauli-ked`，用于
  function-100 导出的 KED 派生 `userfunc.cub`；默认等值面 `0.01`。
  这些量通常按正标量场显示，但需要检查数据范围并按体系微调
- `local-information-entropy`：正/负等值面，别名包括
  `information-entropy`、`infoentro`、`local-info-entropy`，用于
  Multiwfn `infoentro.cub`；Multiwfn 函数 `11` 计算局部信息熵
  `-rho/N*ln(rho/N)`，源码没有重设等值面，因此默认幅值沿用全局
  `sur_value=0.05`
- `electron-delocalization-range`：单正值等值面，别名包括 `edr`、
  `edr-r-d`，用于 Multiwfn 函数 `20` 的 `EDR.cub`；`grid-run` 需要
  `--edr-length D_BOHR`，因为 Multiwfn 在格点设置前询问 EDR 长度标度
  `d`，单位 Bohr；源码没有重设等值面，因此默认沿用全局
  `sur_value=0.05`
- `orbital-overlap-distance`：单正值等值面，别名包括
  `orbital-overlap-length`、`edrdmax`、`edr-dmax`、`d(r)`，用于
  Multiwfn 函数 `21` 的 `EDRDmax.cub`；不传 `--edr-exponents` 时使用
  Multiwfn 默认指数集合 `20, 2.50, 1.50`，也可传
  `--edr-exponents COUNT START INCREMENT` 手动控制
- `pair-function`：正/负等值面，别名包括 `fermihole`、`fermi-hole`、
  `correlation-hole`、`correlation-factor`、`exchange-correlation-density`、
  `pair-density`，用于 Multiwfn 函数 `17` 的 `fermihole.cub`；`grid-run`
  需要 `--reference-point X Y Z`，默认 Bohr，若坐标为 Angstrom 则加
  `--reference-unit angstrom`；`--pair-function-type` patch Multiwfn
  `pairfunctype`，`--pair-correlation-type` patch `paircorrtype`；runner
  优先复制所选 Multiwfn 同目录的 `settings.ini`，只 patch 这两个键后写入
  run-local `multiwfn_grid_settings.ini` 并通过 `-set` 传给 Multiwfn
- `source-function`：正/负等值面，别名包括 `source`、`srcfunc`、
  `source-func`，用于 Multiwfn 函数 `19` 的 `srcfunc.cub`；`grid-run`
  需要 `--reference-point X Y Z`，默认 Bohr，若坐标为 Angstrom 则加
  `--reference-unit angstrom`；`--source-function-mode` 会让 runner 优先复制
  所选 Multiwfn 同目录的 `settings.ini`，patch `srcfuncmode` 后写入
  run-local `multiwfn_grid_settings.ini` 并通过 `-set` 传给 Multiwfn；
  找不到 base settings 时才写最小 settings 文件，不修改全局
  `settings.ini`；默认幅值沿用全局 `sur_value=0.05`
- `user-function`：正/负等值面，cube-preset 别名包括 `userfunc`、
  `user-defined-function`、`custom-function`、`lea-function`、
  `leae-function`、`shannon-entropy-density`、`fisher-information-density`；
  用于 Multiwfn 函数 `100` 的 `userfunc.cub`；通用
  `grid-run --function user-function` 需要
  `--user-function-index IUSERFUNC`。命名路由 `alpha-density`、
  `beta-density`、`dori`、
  `local-electron-affinity`、`local-electron-attachment-energy`、
  `local-mulliken-electronegativity`、`local-hardness`、
  `vdw-repulsion-potential`、`vdw-dispersion-potential`、
  `electron-esp`、`positive-esp`、`negative-esp`、`electric-field-magnitude`、
  `thomas-fermi-ked`、`weizsacker-ked`、`pauli-ked`、
  `orbital-weighted-fukui-plus`、`orbital-weighted-fukui-minus`、
  `orbital-weighted-fukui-zero`、`orbital-weighted-dual-descriptor`、
  `fractional-occupation-density`、
  `information-gain-density`、`shannon-entropy-density`、
  `fisher-information-density`、`second-fisher-information-density` 会分别
  自动 patch `iuserfunc=1/2/14/20/27/-27/28/29/93/94/101/102/103/90/1200/114/95/96/97/98/49/50/51/52`。
  KED 变体还会额外 patch run-local `iKEDsel`。
  runner 优先复制所选 Multiwfn 同目录的 `settings.ini`，只 patch
  当前路线需要的 run-local 键后通过 `-set` 传入；
  `-1/-3` 外部格点插值和 `57/58/59` Shubin 特殊模式暂不走这个通用路线
- `becke-weight`：单正值等值面，别名包括 `becke`、
  `becke-overlap-weight`、`becke-atomic-weight`，用于 Multiwfn 函数
  `111` 的 `Becke.cub`；`grid-run` 需要 `--becke-atoms I J`，其中
  `I J` 计算 Becke overlap weight，`I 0` 计算 Becke atomic weight；
  默认等值面为适合 `0..1` 权重场的 `0.5`
- `hirshfeld-weight`：单正值等值面，别名包括 `hirshfeld`、
  `hirshfeld-atomic-weight`、`hirshfeldwei`，用于 Multiwfn 函数 `112`
  的 `Hirshfeld.cub`；`grid-run` 需要 `--hirshfeld-atoms ATOMS`，例如
  `2,3,7-10`；当前维护的命令流固定选择 Multiwfn 内置原子密度，暂不自动化
  额外 atomic `.wfn` 文件提示；默认等值面为适合 `0..1` 权重场的 `0.5`
- `rdg-scalar`：单正值等值面，别名包括 `rdg-cube`、
  `reduced-density-gradient`，用于单 cube 的 Multiwfn `RDG.cub`，默认
  等值面 `0.5`；双 cube 的 RDG/NCI 染色图仍用 `cube-preset iri`
- `promolecular-rdg`：单正值等值面，别名包括 `rdg-pro`、`prodens-rdg`，
  用于 Multiwfn `RDGprodens.cub`，默认等值面 `0.4`
- `promolecular-delta-g`：单正值等值面，别名包括 `delta-g`、`deltag`、
  `delta_g`，用于 Multiwfn 函数 `22` 的 `Delta_g.cub`；这是
  promolecular approximation 的 standalone Delta-g，不是 IGM/IGMH 里的
  `dg_inter.cub` surface+texture 路线；源码没有重设等值面，因此默认沿用
  全局 `sur_value=0.05`
- `hirshfeld-delta-g`：单正值等值面，别名包括 `delta-g-hirshfeld`、
  `deltag-hirshfeld`、`delta_g_hirshfeld`、`igmh-scalar`，用于 Multiwfn
  函数 `23` 的 Hirshfeld partition Delta-g；Multiwfn 2026.6.2 源码中
  此函数导出通用 `griddata.cub`，`grid-run` 会把处理后文件稳定命名为
  `<stem>_hirshfeld-delta-g.cub`；它是 standalone 全体系标量，不是
  IGM/IGMH 的 `dg_inter.cub` mapped-surface 路线
- `iri-scalar`：单正值等值面，别名包括 `iri-cube`、`standalone-iri`，
  用于单 cube 的 Multiwfn `IRI.cub`，默认等值面 `1.0`；双 cube 的
  IRI/RDG/NCI 染色图仍用 `cube-preset iri`
- `dori-scalar`：单正值等值面，别名包括 `standalone-dori`、`dori-cube`，
  用于 `grid-run --function dori` 生成的 function-100 `userfunc.cub`
  (`iuserfunc=20`)，默认等值面 `0.95`，跟随 Multiwfn 自带
  `DORIfill.vmd`
- `vdw-potential`：正/负等值面，别名包括 `vdw`、`vdwpot`、
  `vdw-potential-cube`、`van-der-waals-potential`，用于 Multiwfn 函数
  `25` 的 `vdWpot.cub`；Multiwfn 源码中此函数按 UFF 参数计算 vdW
  potential，单位 kcal/mol，并把 main-function-5 `sur_value` 设为
  `1.0`；通过 `grid-run` 生成时默认写 run-local `ivdwprobe=6`，即 C
  探针，也可用 `--vdw-probe O`、`--vdw-probe Cl` 或原子序数改探针元素；
  如果是把 vdW potential 染色到 density/surface cube 上，用 `vdw-map`
- `vdw-repulsion-potential`：单正值等值面，别名包括 `vdw-repulsion`、
  `repulsion-potential`、`repul`，用于 Multiwfn function-100
  `userfunc.cub` 或 vdW 模块导出的 `repul.cub`；`grid-run` 会写
  run-local `iuserfunc=93` 和 `ivdwprobe`，默认 `+1.0` kcal/mol 等值面
- `vdw-dispersion-potential`：单负值等值面，别名包括
  `vdw-dispersion`、`dispersion-potential`、`disp`，用于 Multiwfn
  function-100 `userfunc.cub` 或 vdW 模块导出的 `disp.cub`；`grid-run`
  会写 run-local `iuserfunc=94` 和 `ivdwprobe`，默认 `-1.0` kcal/mol
  等值面。色散项通常为负，所以这里不是 signed 双等值面；若要改这个
  单负值等值面的颜色，仍使用 single surface 的 `--positive-rgb`
- `potential`：正/负等值面，别名包括 `abacus-potential`、`out-pot`、
  `pot-es`，用于 ABACUS `out_pot` 直接势场 cube；如果是密度表面按电势染色，
  用 `esp`
- `partial-charge`：单正值等值面，别名包括 `pchg`、`out-pchg`、
  `band-density`，用于 ABACUS `calculation get_pchg` / `out_pchg` 态密度
- `wavefunction-norm`：单正值等值面，别名包括 `out-wfc-norm`、
  `wavefunction-magnitude`，用于 ABACUS `out_wfc_norm` 非负波函数模/模方；
  对 `out_wfc_re_im` 的实部/虚部 signed cube 仍用 `signed`/`orbital`
- `elf` / `lol`：局域化函数等值面；通过 `grid-run` 生成时默认会复制所选
  Multiwfn `settings.ini` 并写本地 `ELFLOL_type=0`，固定为 Becke ELF/LOL
  定义。用 `--elflol-type tsirelson` 或 `--elflol-type tian-lu` 可以生成其它
  Multiwfn 支持的 ELF/LOL 变体；`--elflol-type d-over-d0` 只适用于 ELF 的
  D/D0 项，且不改全局 settings
- `stm`：别名包括 `ldos`、`stm-ldos`、`tunneling-current`，用于
  Multiwfn 常电流 STM 导出的 `STM.cub`，默认等值面 `0.001`
- `domain`：别名包括 `domain-cube`、`domain-analysis`、`binary-domain`，
  用于 Multiwfn domain analysis 导出的二值 `domain.cub`，默认等值面
  `0.5`
- `basin`：别名包括 `basin-cube`、`binary-basin`、`aim-basin`、
  `elf-basin`，用于 Multiwfn basin analysis option `-5` 导出的单个
  二值 `basinNNNN.cub`，默认等值面 `0.5`
- `basin-type`：别名包括 `basinsyn`、`basin-synaptic`、
  `elf-basin-type`，用于 `basinsyn.cub`，以 signed mode 同时画
  单突触 `-1` 和双突触 `+1` basin 区域
- `iri`：别名 `rdg`、`nci`，需要 `--texture-cube`，默认
  `--tex-physical -0.04 0.04` 和 `--tex-range-source surface-band`
- `igmh`：别名包括 `igm`、`igm-inter`、`igmh-inter`，用 `dg_inter.cub`
  加 `sl2r.cub`，默认等值面 `0.01`，染色范围 `-0.05` 到 `0.05`，对齐
  Multiwfn `IGM_inter.vmd`
- `dori`：别名包括 `dori-map`、`dori-fill`，用 DORI `userfunc.cub` 加
  sign(lambda2)rho cube，默认等值面 `0.95`，染色范围 `-0.04` 到
  `0.02`，对齐 Multiwfn `DORIfill.vmd`；注意这里 DORI 是 surface cube，
  sign(lambda2)rho 是 `--texture-cube`
- `igm-intra`：用 `dg_intra.cub` 加 `sl2r.cub`，默认等值面 `0.2`，对齐
  Multiwfn `IGM_intra.vmd`
- `aigm` / `aigm-tfi`：用 `avgdg_inter.cub` 分别加 `avgsl2r.cub` 或
  `thermflu.cub`，默认等值面 `0.008`
- `esp`：别名 `mep`，需要 `--texture-cube`，建议为可比较图显式给
  `--tex-physical`
- `surface-map`：通用 density/surface cube 加 mapped-property texture cube，
  默认等值面 `0.01`，默认染色范围 `0.0` 到 `0.002`，对齐 Multiwfn
  `molsurfmap.vmd`
- `alie`：density.cub 加 avglocion.cub，默认等值面 `0.0005`，默认染色范围
  `0.32` 到 `0.36` a.u.
- `lea` / `leae`：density.cub 加 userfunc.cub，默认等值面分别为 `0.01` 和
  `0.004`
- `vdw-map`：别名 `vdw-surface`，density.cub 加 vdW.cub/vdWpot.cub，默认
  等值面 `0.0001`，默认染色范围 `-0.3` 到 `0.3` kcal/mol

生成的 recipe 会追加 `Cube Preset` 段，记录请求的预设名、规范预设名、
有效等值面、surface mode、texture 缩放来源和用户覆盖参数。

如果 Multiwfn 分子表面分析已经导出了 `surfanalysis.pdb`，可以让
`cube-preset` 直接把极值点写进同一个 `.vesta`：

```bash
multiwfn2vesta cube-preset surface-map density.cub cube_products \
  --texture-cube mapped.cub \
  --surfanalysis-pdb surfanalysis.pdb \
  --surf-extrema all
```

Multiwfn 源码约定 `surfanalysis.pdb` 中 C 是 surface maximum，O 是
surface minimum，B-factor 字段是 mapped value。维护代码会把极值点作为一个
新的 atoms-only phase 插到 `SCENE` 前，默认半径 `0.10`，maxima 红色、
minima 蓝色，overlay phase 的 `SBOND` 为空，并默认把 `COMPS` 改为 `0`。
`--surf-extrema auto` 时，`alie`/`leae` 只显示 minima，`lea` 只显示 maxima，
其他 mapped-surface 预设显示全部；也可以手动指定 `all|maxima|minima`。

已有 `.vesta` 文件可以单独补极值点：

```bash
multiwfn2vesta surface-extrema input.vesta surfanalysis.pdb output.vesta \
  --surface-cube density.cub \
  --selection minima
```

## Cube 算术：密度差 / spin density / Fukui / dual descriptor

`cube-arith` 是兼容 cube 的线性组合工具。它适合把 ABACUS 或 Multiwfn 已经
生成好的同网格密度/波函数/差分 cube 组合成新的 cube，再交给 `cube-preset`
画 VESTA 等值面。它不负责生成带电态波函数本身；带电态、中性态、激发态或
不同自旋通道的 cube 要先由 ABACUS、Multiwfn 或 `grid-run` 产生。

任意线性组合：

```bash
multiwfn2vesta cube-arith cube_arith_products \
  --term 1.0 rho_a.cub \
  --term -1.0 rho_b.cub \
  --stem density_difference
```

spin density、Fukui 和 dual descriptor 快捷入口：

```bash
multiwfn2vesta cube-arith cube_arith_products \
  --operation spin-density \
  --plus-cube alpha_density.cub \
  --minus-cube beta_density.cub \
  --stem spin_density

multiwfn2vesta cube-arith cube_arith_products \
  --operation fukui-plus \
  --anion-cube density_Nplus1.cub \
  --neutral-cube density_N.cub

multiwfn2vesta cube-arith cube_arith_products \
  --operation fukui-minus \
  --neutral-cube density_N.cub \
  --cation-cube density_Nminus1.cub

multiwfn2vesta cube-arith cube_arith_products \
  --operation dual-descriptor \
  --anion-cube density_Nplus1.cub \
  --neutral-cube density_N.cub \
  --cation-cube density_Nminus1.cub
```

公式：

- `density-difference`: `plus - minus`
- `spin-density`: `alpha/spin-up density - beta/spin-down density`
- `fukui-plus`: `rho(N+1) - rho(N)`
- `fukui-minus`: `rho(N) - rho(N-1)`
- `dual-descriptor`: `rho(N+1) - 2*rho(N) + rho(N-1)`

默认输出：

- `<stem>.cub`
- `<stem>_cube_arith_recipe.md`
- 默认 `--preset auto`：`fukui-plus/minus` 用 `density`，`spin-density` 用
  `spin-density`，`density-difference`、`dual-descriptor` 和任意 `linear`
  组合用 `signed`

兼容性规则：

- 所有输入 cube 必须有相同 grid origin、grid vectors、点数和 cube 单位约定；
  默认 `--cube-units auto` 下正 grid count 视为 Bohr，负 grid count 视为
  Angstrom，混用会被拒绝
- 默认还要求 atom list 一致；确认只需要共用格点时可用 `--no-strict-atoms`
- 程序拒绝把输出 cube 写到任何输入 cube 路径上，避免覆盖原始数据
- 若只想生成 cube，不写 VESTA，用 `--no-vesta`

## 波函数文件到 Fukui / dual descriptor VESTA

如果已经有中性态、N+1 态、N-1 态的 Multiwfn 可读波函数文件，可以用
`fukui-run` 一次性完成密度 cube 生成和差分后处理：

```bash
multiwfn2vesta fukui-run fukui_products \
  --neutral neutral.molden \
  --anion anion.molden \
  --cation cation.molden \
  --operation all \
  --grid-mode points \
  --grid-points 80 80 80
```

执行逻辑：

- 先对 `--neutral` 调用 `grid-run --function density`，生成中性态 density
  cube
- 再对需要的 charged state 调用 `grid-run --function density --grid-mode cube
  --grid-cube <neutral_density.cub>`，强制复用中性态 cube 的格点
- 最后用 `cube-arith` 生成 `fukui-plus`、`fukui-minus` 或
  `dual-descriptor`

只算亲核/亲电 Fukui 的一个方向时，可以少给不需要的带电态：

```bash
multiwfn2vesta fukui-run fplus_products \
  --neutral neutral.fch \
  --anion anion.fch \
  --operation fukui-plus

multiwfn2vesta fukui-run fminus_products \
  --neutral neutral.fch \
  --cation cation.fch \
  --operation fukui-minus
```

默认输出：

- `multiwfn_fukui_recipe.md`：顶层 manifest，记录 caveat、子任务路径和
  差分结果
- `neutral_density/`、`anion_density/`、`cation_density/`：普通 `grid-run`
  子目录，含 Multiwfn 命令流、stdout/stderr、raw cube 和处理后的 density
  cube
- `fukui_plus/`、`fukui_minus/`、`dual_descriptor/`：普通 `cube-arith` 子目录，
  含差分 cube、recipe 和可选 VESTA 文件

这个流程主要面向有限体系和可比较的几何。带电周期性超胞、金属 slab 或带
背景电荷的体系在物理解释上要谨慎；如果三个 density cube 已经由别的流程
生成好，直接用 `cube-arith` 更透明。

如果没有可靠的 N+1/N/N-1 波函数，或周期带电态不适合直接比较，可以先用
Multiwfn 的 orbital-weighted Fukui/dual descriptor 单波函数近似：

```bash
multiwfn2vesta grid-run input.molden ow_dual_products \
  --function orbital-weighted-dual-descriptor \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.molden ow_dual_map \
  --function ow-dd \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub \
  --tex-physical -0.04 0.04 \
  --tex-range-source surface-band
```

这不是 `fukui-run` 的替代品，而是 function `100` 的
`iuserfunc=95/96/97/98` 路线。源码里要求完整轨道信息；更适合闭壳层、
single-determinant、HOMO/LUMO 能量和虚轨道信息可信的体系。当前 runner
只通过 run-local settings patch `iuserfunc`，不改 Multiwfn 的
`orbwei_delta`；本地 2026.6.2 源码默认值为 `0.1` a.u.

## 波函数文件到 Multiwfn 单 cube / VESTA

如果起点是 Molden/FCHK/WFN/WFX 等 Multiwfn 可读波函数文件，而目标是一个
real-space function cube，可以用 `grid-run`。它走 Multiwfn 主菜单 `5`
(`study3dim`)，选择函数、设置格点、再在后处理菜单用 `2` 导出 cube：

```bash
multiwfn2vesta grid-run \
  input.molden \
  grid_products \
  --function density \
  --grid-points 40 40 40 \
  --timeout 300
```

查看当前维护的函数表：

```bash
multiwfn2vesta grid-run --list-functions
```

常用函数：

- `density` / `rho`：Multiwfn 函数 `1`，原始输出 `density.cub`，默认接
  `cube-preset density`
- `gradient` / `rho-gradient`：函数 `2`，原始输出 `gradient.cub`，默认接
  `cube-preset gradient-norm`，按单正值等值面显示；默认 `0.05` 是
  Multiwfn 全局等值面初值，建议按体系调参
- `orbital` / `mo`：函数 `4`，原始输出 `MOvalue.cub`，默认接 `signed`；
  单轨道用 `--orbital h`，多轨道批量用 `--orbitals h l l+1`
- `orbital-density` / `orbdens`：函数 `44`，原始输出 `orbdens.cub`，
  默认接 `cube-preset orbital-density`；单轨道用 `--orbital`，多轨道批量
  用 `--orbitals`
- `laplacian` / `lap`：函数 `3`，原始输出 `laplacian.cub`，默认接
  `cube-preset laplacian`
- `spin-density` / `spin`：函数 `5`，原始输出 `spindensity.cub`，默认接
  `cube-preset spin-density`；运行时会写本地
  `multiwfn_grid_settings.ini` 并通过 `-set` 固定 `ipolarpara=0`，避免被
  全局 Multiwfn 设置误切到 spin-polarization parameter
- `spin-polarization` / `spin-pol`：函数 `5`，原始输出同样是
  `spindensity.cub`，默认接 `cube-preset spin-polarization`；运行时通过
  本地 `-set` 文件固定 `ipolarpara=1`，Multiwfn 计算
  `(rho_alpha-rho_beta)/(rho_alpha+rho_beta)`
- `hamiltonian-ked` / `k(r)`：函数 `6`，原始输出 `K(r).cub`，默认接
  `cube-preset hamiltonian-ked`
- `lagrangian-ked` / `g(r)`：函数 `7`，原始输出 `G(r).cub`，默认接
  `cube-preset lagrangian-ked`
- `thomas-fermi-ked` / `tf-ked`、`weizsacker-ked` / `vw-ked`、
  `pauli-ked`：函数 `100`，原始输出 `userfunc.cub`，默认接
  `cube-preset kinetic-energy-density`。Thomas-Fermi 和 Weizsacker KED
  自动写 run-local `iuserfunc=1200` 且分别设置 `iKEDsel=3` / `4`；Pauli
  KED 自动写 `iuserfunc=114` 和 `iKEDsel=2`，即本地 Multiwfn 源码里的
  Lagrangian KED minus Weizsacker KED。ABACUS 路线依赖 Molden 轨道及其
  导数，不是 ABACUS 原生 KED cube；建议限于已验证的 LCAO Molden，并按
  体系调 `--isosurface`
- `local-information-entropy` / `information-entropy`：函数 `11`，原始
  输出 `infoentro.cub`，默认接 `cube-preset local-information-entropy`，
  按正/负等值面显示，默认幅值 `0.05`
- `pair-function` / `fermihole` / `correlation-hole`：函数 `17`，原始
  输出 `fermihole.cub`，默认接 `cube-preset pair-function`，按正/负等值面
  显示；必须传 `--reference-point X Y Z`，默认 Bohr，Angstrom 坐标用
  `--reference-unit angstrom`；`--pair-function-type` 控制 `pairfunctype`，
  `--pair-correlation-type` 控制 `paircorrtype`，两者都通过本次运行目录里的
  run-local settings 文件和 Multiwfn `-set` 传入
- `source-function` / `source` / `srcfunc`：函数 `19`，原始输出
  `srcfunc.cub`，默认接 `cube-preset source-function`，按正/负等值面显示；
  必须传 `--reference-point X Y Z`，默认 Bohr，Angstrom 坐标用
  `--reference-unit angstrom`；`--source-function-mode` 通过本次运行目录里的
  run-local settings 文件和 Multiwfn `-set` 控制 `srcfuncmode`，该文件优先
  从所选 Multiwfn 的 `settings.ini` 复制后 patch
- `user-function` / `userfunc`：函数 `100`，原始输出 `userfunc.cub`，
  默认接 `cube-preset user-function`，按正/负等值面显示；通用路由必须传
  `--user-function-index IUSERFUNC`。也可直接用命名路由
  `alpha-density`、`beta-density`、`dori`、
  `local-electron-affinity`、`local-electron-attachment-energy`、
  `local-mulliken-electronegativity`、`local-hardness`、
  `vdw-repulsion-potential`、`vdw-dispersion-potential`、
  `electron-esp`、`positive-esp`、`negative-esp`、`electric-field-magnitude`、
  `thomas-fermi-ked`、`weizsacker-ked`、`pauli-ked`、
  `orbital-weighted-fukui-plus`、`orbital-weighted-fukui-minus`、
  `orbital-weighted-fukui-zero`、`orbital-weighted-dual-descriptor`、
  `fractional-occupation-density`、
  `information-gain-density`、`shannon-entropy-density`、
  `fisher-information-density`、`second-fisher-information-density`，这些会
  自动设置 `iuserfunc=1/2/14/20/27/-27/28/29/93/94/101/102/103/90/1200/114/95/96/97/98/49/50/51/52`；
  KED 变体还会额外设置 run-local `iKEDsel`；
  LEA/LEAE 若要画成 density surface 上的染色图，可在 `grid-run` 中加
  `--surface-cube density.cub` 自动选 `lea` / `leae` mapped preset，也可
  手动用 `cube-preset lea` / `cube-preset leae`；局域 Mulliken
  electronegativity、local hardness、alpha/beta density 默认走通用
  `surface-map`，需要时用 `--tex-physical` 或 `--tex-percent` 调整色标
- `electron-delocalization-range` / `edr`：函数 `20`，原始输出
  `EDR.cub`，默认接 `cube-preset electron-delocalization-range`，按单正值
  等值面显示；必须传 `--edr-length D_BOHR`
- `orbital-overlap-distance` / `edrdmax`：函数 `21`，原始输出
  `EDRDmax.cub`，默认接 `cube-preset orbital-overlap-distance`，按单正值
  等值面显示；默认使用 Multiwfn 指数集合 `20, 2.50, 1.50`，可用
  `--edr-exponents COUNT START INCREMENT` 覆盖
- `becke-weight` / `becke`：函数 `111`，原始输出 `Becke.cub`，默认接
  `cube-preset becke-weight`，按单正值 `0.5` 等值面显示；必须传
  `--becke-atoms I J`，其中 `I J` 是 overlap weight，`I 0` 是 atomic
  weight
- `hirshfeld-weight` / `hirshfeld`：函数 `112`，原始输出
  `Hirshfeld.cub`，默认接 `cube-preset hirshfeld-weight`，按单正值
  `0.5` 等值面显示；必须传 `--hirshfeld-atoms ATOMS`，例如
  `2,3,7-10`；当前自动化路径使用 Multiwfn 内置原子密度
- `esp`、`nuclear-esp`、`signlambda2rho`：默认按 signed scalar 处理；配合
  `--surface-cube` 时，ESP/nuclear ESP 默认走 `cube-preset esp`，
  sign(lambda2)rho 默认走 `cube-preset iri`
- `electron-esp` / `electronic-esp`：函数 `100`，原始输出
  `userfunc.cub`，自动 patch run-local `iuserfunc=14`；Multiwfn 源码中
  该 route 调用 `eleesp(x,y,z)`，也就是电子贡献 ESP。按通常 ESP 约定它
  主要为负，因此 standalone VESTA 默认用单负 `-0.05` a.u. 等值面；若加
  `--surface-cube density.cub`，则作为 texture 走 `surface-map`，建议显式
  给 `--tex-physical` 以固定跨体系色标
- `positive-esp` / `positive-mep`、`negative-esp` / `negative-mep`、
  `electric-field-magnitude` / `electric-field`：函数 `100`，原始输出
  `userfunc.cub`，分别 patch run-local `iuserfunc=101/102/103`。Multiwfn
  源码中 101/102 会把总 ESP 裁剪为正值部分/负值部分，103 由 ESP 梯度得到
  电场强度。standalone VESTA 默认分别用单正 `+0.05`、单负 `-0.05`、单正
  `0.05` 等值面；若加 `--surface-cube density.cub`，则作为 texture 走
  `surface-map`，建议显式给 `--tex-physical` 便于跨体系比较。
- `vdw-potential` / `vdw`：函数 `25`，原始输出 `vdWpot.cub`，默认接
  `cube-preset vdw-potential`，按正/负 `1.0` kcal/mol 等值面显示；配合
  `--surface-cube` 时默认走 `cube-preset vdw-map`，把生成的 vdW potential
  cube 作为已有 density/surface cube 的 texture；`--vdw-probe` 可选择
  UFF 探针元素，默认 C/6
- `vdw-repulsion-potential` / `repul`、`vdw-dispersion-potential` /
  `disp`：函数 `100`，原始输出 `userfunc.cub`，分别自动写 run-local
  `iuserfunc=93` / `94` 和 `ivdwprobe`；默认接
  `cube-preset vdw-repulsion-potential` / `vdw-dispersion-potential`。排斥项
  按单正值 `+1.0` kcal/mol 显示，色散项通常为负，按单负值 `-1.0`
  kcal/mol 显示；配合 `--surface-cube` 时也可走 `vdw-map`，但建议显式调
  `--tex-physical` 或 `--tex-percent`。色散 standalone preset 是 single
  mode，改色时用 `--positive-rgb`
- `alie` / `avglocion`：函数 `18`，原始输出 `avglocion.cub`；常规 ALIE
  表面图可以用 `--surface-cube density.cub` 自动把生成的 ALIE cube 作为
  `cube-preset alie` 的 texture
- `local-electron-affinity` / `local-electron-attachment-energy`：函数
  `100`，原始输出 `userfunc.cub`；配合 `--surface-cube density.cub` 时，
  自动把生成的 LEA/LEAE cube 作为 `cube-preset lea` / `cube-preset leae`
  的 texture
- `local-mulliken-electronegativity` / `local-hardness`：函数 `100`，原始
  输出 `userfunc.cub`，自动写 run-local `iuserfunc=28` / `29`；配合
  `--surface-cube density.cub` 时默认走 `cube-preset surface-map`，可以用
  `--tex-physical MIN MAX`、`--tex-percent MIN MAX`、
  `--tex-range-source surface-band`、`--surface-band` 和
  `--surface-nearest` 直接控制 texture 色标
- `alpha-density` / `beta-density`：函数 `100`，原始输出
  `userfunc.cub`，自动写 run-local `iuserfunc=1` / `2`，默认接
  `density` preset；Multiwfn 源码调用 `fspindens(x,y,z,'a')` /
  `fspindens(x,y,z,'b')`，适合检查自旋通道密度。如果目标是
  alpha-minus-beta 差值，则继续用 `grid-run --function spin-density`。
  闭壳层体系中两个通道通常只是总密度的一半；对 ABACUS 来说主要面向
  最新 `molden.py` 正确导出的 `nspin=2` LCAO Molden。`nspin=4`、SOC、
  多 k 点和金属分数占据仍需要谨慎解释。Multiwfn 源码里 `fspindens`
  路径不像 `fdens` 那样覆盖所有 EDF 密度贡献，因此特殊 EDF/ECP 输入中
  alpha+beta 未必严格等于 total density
- `fractional-occupation-density` / `fod` /
  `fractional-occupancy-density`：函数 `100`，原始输出 `userfunc.cub`，
  自动写 run-local `iuserfunc=90`，默认接 `density` preset；Multiwfn
  源码把分数占据权重乘到轨道振幅平方上。整数占据的单参考波函数通常会
  给接近零的 FOD；它主要用于分数占据有物理意义或被有意使用的体系。
  ABACUS 路线需要确认最新 `molden.py` 正确写出占据数；金属 smearing、
  多 k 点、SOC/noncollinear 结果要谨慎解释。`density` preset 默认
  等值面 `0.01` 对 FOD 可能偏高，看不到时先试 `--isosurface 0.001`，
  再按体系调节
- `thomas-fermi-ked` / `tf-ked`、`weizsacker-ked` / `vw-ked`、
  `pauli-ked`：函数 `100`，原始输出 `userfunc.cub`，自动接
  `kinetic-energy-density` preset。前两者设置 `iuserfunc=1200` 并分别
  设置 `iKEDsel=3` / `4`，Pauli KED 设置 `iuserfunc=114` 和 `iKEDsel=2`。
  这些量通常作为正标量场显示，但需要检查实际数据范围；数值尺度依
  体系、占据、NAO-to-GTO 转换和赝势价电子定义而变。对 ABACUS Molden
  结果建议显式调 `--isosurface`
- `orbital-weighted-fukui-plus` / `orbital-weighted-fukui-minus` /
  `orbital-weighted-fukui-zero`：函数 `100`，原始输出 `userfunc.cub`，
  自动写 run-local `iuserfunc=95` / `96` / `97`，默认接 `density`
  preset；Multiwfn 按 HOMO/LUMO 化学势附近的轨道权重构造 Fukui
  近似，`orbwei_delta` 在本地源码中的默认值为 `0.1` a.u.
- `orbital-weighted-dual-descriptor`：函数 `100`，原始输出
  `userfunc.cub`，自动写 run-local `iuserfunc=98`，默认接 `signed`
  preset，别名包括 `ow-dual` 和 `ow-dd`；配合 `--surface-cube` 时走通用
  `surface-map`，建议显式给 `--tex-physical MIN MAX`，例如
  `--tex-physical -0.04 0.04`
- `dori`：函数 `100`，原始输出 `userfunc.cub`，自动写 run-local
  `iuserfunc=20`，默认接 `cube-preset dori-scalar`，按单正值 `0.95`
  等值面显示；若要 DORI surface 按 sign(lambda2)rho 染色，显式运行
  `cube-preset dori DORI.cub ... --texture-cube sl2r.cub`
- `elf` / `lol`：局域化函数等值面
- `rdg` / `promolecular-rdg`：函数 `13` / `14`，原始输出 `RDG.cub` /
  `RDGprodens.cub`，默认分别接 `cube-preset rdg-scalar` /
  `cube-preset promolecular-rdg`；如果要 IRI/RDG/NCI 那种 surface+texture
  双 cube 图，优先用 `iri-run` 或显式 `cube-preset iri`
- `delta-g` / `deltag`：函数 `22`，原始输出 `Delta_g.cub`，默认接
  `cube-preset promolecular-delta-g`，按单正值等值面显示；它是
  promolecular approximation 的单 cube Delta-g，和 IGM/IGMH 的
  `dg_inter.cub` mapped-surface 文件分开维护
- `hirshfeld-delta-g` / `delta-g-hirshfeld`：函数 `23`，原始输出
  `griddata.cub`，默认接 `cube-preset hirshfeld-delta-g`，按单正值
  等值面显示；Multiwfn 没有为此导出路径设置专名，项目侧给处理后 cube
  使用稳定 `<stem>_hirshfeld-delta-g.cub` 命名
- `iri` / `interaction-region-indicator`：函数 `24`，原始输出 `IRI.cub`，
  默认接 `cube-preset iri-scalar`，按单正值等值面显示，默认等值面
  `1.0`
- `signlambda2rho` / `promolecular-signlambda2rho`：其它单标量 cube，其中
  sign(lambda2)rho 配合 `--surface-cube` 可作为 `cube-preset iri` 的
  texture

轨道例子：

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function orbital \
  --orbital h \
  --grid-mode points \
  --grid-points 80 80 80

multiwfn2vesta grid-run input.fch grid_products \
  --function edr \
  --edr-length 0.85 \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function edrdmax \
  --edr-exponents 12 3.0 1.2 \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function pair-function \
  --reference-point 0 0 0 \
  --pair-function-type 1 \
  --pair-correlation-type 3 \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function source-function \
  --reference-point 0 0 0 \
  --source-function-mode 1 \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function local-electron-affinity \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function user-function \
  --user-function-index 49 \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function becke \
  --becke-atoms 1 4 \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function hirshfeld \
  --hirshfeld-atoms '2,3,7-10' \
  --grid-mode points \
  --grid-points 120 120 120

multiwfn2vesta grid-run input.fch grid_products \
  --function hirshfeld-delta-g \
  --grid-mode points \
  --grid-points 120 120 120
```

批量导出多个轨道：

```bash
multiwfn2vesta grid-run input.fch orbital_products \
  --orbitals h l l+1 \
  --grid-mode points \
  --grid-points 80 80 80 \
  --no-vesta
```

批量模式未显式给 `--function` 时默认等价于 `--function orbital`。若要导出
轨道密度，用 `--function orbital-density --orbitals h l`。这个批量功能不是
Multiwfn 内部一次性批处理，而是多次隔离的单轨道运行：每个轨道都有独立子目录、
命令流、stdout/stderr、raw cube 目录、处理后的 cube 和可选 VESTA 文件。

批量默认输出：

- `multiwfn_grid_batch_recipe.md`：顶层 manifest，记录 requested orbital、
  safe label、status、失败数和 skipped 数
- `001_orbital_h/`、`002_orbital_l/`、`003_orbital_lplus1/` 等子目录
- 每个子目录内仍是单次 `grid-run` 输出：`multiwfn_grid_input.txt`、
  `multiwfn_grid.stdout.txt`、`multiwfn_grid.stderr.txt`、
  `multiwfn_grid_raw/<Multiwfn默认文件名>.cub`、`<stem>_<orbital>_<function>.cub`
  和可选 VESTA recipe

默认遇到第一个失败轨道就停止，后续轨道在 batch recipe 中标为 `skipped`。
如果希望继续尝试后续轨道，加 `--keep-going`。批量模式会拒绝 `--orbital`、
`--commands-file`、`--expected-cube`、`--raw-dir`、`--surface-cube`、参考点、
pair/source/user-function 等非轨道专用选项，因为每个子任务需要独立的命令流
和 raw 目录。

复用已有 cube 的格点，便于后续做双 cube 或多图层叠加：

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function esp \
  --grid-mode cube \
  --grid-cube density.cub \
  --no-vesta
```

如果这个已有 cube 本身就是要显示的 density/surface cube，可以直接让
`grid-run` 把新生成的 cube 当作 texture 写成 mapped-surface VESTA：

```bash
multiwfn2vesta grid-run input.fch esp_map \
  --function esp \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub

multiwfn2vesta grid-run input.fch alie_map \
  --function alie \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub

multiwfn2vesta grid-run input.fch lea_map \
  --function local-electron-affinity \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub

multiwfn2vesta grid-run input.fch hardness_map \
  --function local-hardness \
  --surface-cube density.cub \
  --grid-mode cube \
  --grid-cube density.cub \
  --tex-physical -0.2 0.2 \
  --tex-range-source surface-band \
  --surface-band 0.25
```

`--preset auto` 时，ESP/nuclear ESP 选 `esp`，ALIE 选 `alie`，
LEA/LEAE 选 `lea`/`leae`，sign(lambda2)rho 选 `iri`，vdW potential 选
`vdw-map`，local electronegativity、local hardness 和其它函数回退到
`surface-map`。`grid-run --surface-cube` 会把 `--tex-physical`、
`--tex-percent`、`--tex-range-source`、`--surface-band` 和
`--surface-nearest` 透传给 `cube-preset`，因此不必手动再跑一遍
`cube-preset` 也能调整 mapped surface 色标。`--surface-band` 是围绕目标
等值面的非负半宽，`--surface-nearest` 必须为正数。批量轨道导出暂不支持
`--surface-cube`。

默认输出：

- `multiwfn_grid_input.txt`：实际喂给 Multiwfn 的命令流
- `multiwfn_grid.stdout.txt` / `multiwfn_grid.stderr.txt`
- `multiwfn_grid_raw/<Multiwfn默认文件名>.cub`
- `<stem>_<function>.cub`
- `multiwfn_grid_recipe.md`
- 默认还会写 `<stem>_<function>_<preset>_cube.vesta` 和 recipe；只要 cube
  时用 `--no-vesta`

真实 H2O noGUI smoke：

```bash
bin/multiwfn2vesta grid-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_density/products \
  --function density \
  --grid-points 12 12 12 \
  --stem h2o \
  --timeout 180
```

该 smoke 返回 `0`，生成 raw `density.cub`、`h2o_density.cub`、
`h2o_density_density_cube.vesta` 和两个 recipe。另一个真实 smoke 用
`--function elf --no-vesta` 生成 raw `ELF.cub` 和 `h2o_elf.cub`：
`/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_elf/products/`。
普通 `elf`/`lol` 会固定 `ELFLOL_type=0`；`tsirelson`/`tian-lu` 可用于
ELF 和 LOL，`d-over-d0` 是 ELF-only。显式变体示例：

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function lol \
  --elflol-type tsirelson \
  --grid-points 80 80 80
```

新增 mapped-surface smoke：
`/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_surface_cube_map_20260610/h2o_esp_map/`。
它复用已有 `h2o_density.cub` 的格点，生成 `h2o_esp.cub`，并写出
`h2o_esp_esp_cube.vesta`；recipe 中 Surface Cube 是 density，Texture Cube
是 ESP。

注意：`grid-run` 的每个子任务仍然只生成一个新的 scalar cube。若这个 cube
要给已有 surface 染色，用 `--surface-cube`；其它更特殊的双 cube 图仍可显式
走 `cube-preset`/`cube-vesta`。IRI/RDG/NCI 和 IGM/IGMH 已有专门的
`iri-run`、`igmh-run`/`igm-run` 流程。
`cube-preset igmh` 仍可单独用于把已有 `dg_inter.cub`/`sl2r.cub` 写成
VESTA。

## 波函数文件到 STM/LDOS VESTA

如果波函数文件含有 GTO/GTF 信息，可以用 `stm-run` 调用 Multiwfn 主菜单
`300`、子功能 `4`。维护路径固定用于常电流图：进入 STM 菜单后先用选项
`1` 从默认 constant-distance 切到 constant-current，再计算 3D
tunneling-current/LDOS grid，并在后处理菜单用选项 `2` 导出 `STM.cub`：

```bash
multiwfn2vesta stm-run input.molden stm_products \
  --bias -1.0 \
  --fermi -4.8 \
  --grid-points 120 120 60 \
  --x-range -6 6 \
  --y-range -6 6 \
  --z-range 2 8
```

ABACUS 金属/slab 的 Molden 如果带 smearing 或非整数占据，可先试
`--prepare-fermi-temperature 298.15`，它会在 STM 前插入 Multiwfn
`300 -> 9` 的 Fermi/占据准备步骤。`stm-run` 维护的是 `STM.cub` 三维等值面
路线，不生成 Multiwfn GUI 里的 2D 平面 STM 图。

默认输出：

- `multiwfn_stm_input.txt`：实际喂给 Multiwfn 的命令流
- `multiwfn_stm.stdout.txt` / `multiwfn_stm.stderr.txt`
- `multiwfn_stm_raw/STM.cub`
- `<stem>_stm.cub`
- `multiwfn_stm_recipe.md`
- 默认还会写 `<stem>_stm_cube.vesta` 和 recipe；只要 cube 时用 `--no-vesta`

真实 H2O noGUI smoke：

```bash
bin/multiwfn2vesta stm-run \
  /mnt/g/work/multiwfn2vesta/smoke/20260605_iri_aim_h2o/H2O.fch \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_stm_run_smoke_20260610/h2o \
  --grid-points 10 10 6 \
  --stem h2o \
  --timeout 300
```

该 smoke 返回 `0`，生成 `h2o_stm.cub`、`h2o_stm_cube.vesta` 和 recipe。
`h2o_stm.cub` 有 600 个格点，数值范围是 `3.7332e-13` 到 `0.0151741`；
默认 `cube-preset stm` 等值面 `0.001` 落在数据范围内。

## Cube/Grid 到 Domain VESTA

如果起点已经是 ABACUS、Multiwfn `grid-run` 或其他程序给出的 scalar
cube，可以用 `domain-run` 调 Multiwfn 主菜单 `200`、子功能 `14`，按阈值
把当前 grid data 聚成 domain：

```bash
multiwfn2vesta domain-run density.cub domain_products \
  --criterion '<0.5' \
  --domain-index 1 \
  --timeout 300
```

默认命令流：

```text
200
14
3
<criterion>
-1
10
<domain_index>
11
<domain_index>
0
0
q
```

其中 `3` 设置 `<0.5` 或 `>0.001` 这类 domain 判据，`-1` 表示基于输入
cube 已在内存中的 grid data 聚类，`10` 导出 `domain.cub`，`11` 导出
边界格点 `domain.pdb`。导出的 `domain.cub` 是二值 cube：选中 domain 内为
`1`，外部为 `0`，所以 `cube-preset domain` 默认用 `0.5` 等值面。

默认输出：

- `multiwfn_domain_input.txt`
- `multiwfn_domain.stdout.txt`
- `multiwfn_domain.stderr.txt`
- `multiwfn_domain_raw/domain.cub`
- `multiwfn_domain_raw/domain.pdb`
- `<stem>_domain.cub`
- `<stem>_domain.pdb`
- `multiwfn_domain_recipe.md`
- `<stem>_domain_cube.vesta`
- `<stem>_domain_cube_vesta_recipe.md`

真实 H2O density-cube noGUI smoke：

```bash
bin/multiwfn2vesta domain-run \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_density/products/h2o_density.cub \
  /mnt/g/work/multiwfn2vesta/smoke/multiwfn_domain_run_smoke_20260610/h2o_density \
  --criterion '<0.5' \
  --domain-index 1 \
  --stem h2o_density \
  --timeout 300
```

该 smoke 返回 `0`，生成 `h2o_density_domain.cub`、
`h2o_density_domain.pdb`、`h2o_density_domain_cube.vesta` 和 recipe。

## Basin Cube 到 VESTA

Multiwfn basin analysis 本身先保持半手动：生成 basin 时要先选实空间函数、
网格策略，以及是否复用内存里的 cube/grid data。项目当前维护的是 basin
analysis option `-5` 已导出 cube 之后的显示层。

单个二值 basin cube，例如 `basin0001.cub`：

```bash
multiwfn2vesta cube-preset basin basin0001.cub basin_products
```

`basinsyn.cub` 里 Multiwfn 用 `-1` 表示 monosynaptic basin，用 `+1`
表示 disynaptic basin，可以用 signed preset 同时画两类区域：

```bash
multiwfn2vesta cube-preset basin-type basinsyn.cub basin_products
```

`cube-preset basin` 会拒绝文件名正好是 `basin.cub` 的输入，因为这个总
文件的格点值是 basin index，不是 `0/1` 成员关系。需要画单个 basin
边界时，应使用 `basinNNNN.cub`。

## 波函数文件到 IRI/RDG VESTA

如果起点是 Molden/FCHK/WFN/WFX 等 Multiwfn 可读波函数文件，可以直接调用
Multiwfn 的弱相互作用 IRI/RDG 菜单，并把输出接到 VESTA：

```bash
multiwfn2vesta iri-run \
  input.molden \
  iri_products \
  --timeout 300
```

默认流程：

- 自动发现 Multiwfn；也可用 `--multiwfn /path/to/Multiwfn_noGUI` 显式指定
- 写 `multiwfn_iri_input.txt`，记录实际喂给 Multiwfn 的命令流
- 在 `multiwfn_iri_raw/` 保存 Multiwfn 原始 `func1.cub`、`func2.cub` 和
  `output.txt`
- 把 `func1.cub` 处理成 `<stem>_IRI1.cub`，作为 sign(lambda2)rho 类染色 cube
- 把 `func2.cub` 复制成 `<stem>_IRI2.cub`，作为 IRI/RDG 等值面 cube
- 默认调用 `cube-preset iri` 生成 `<stem>_iri_cube.vesta` 和 recipe

常用参数：

```bash
multiwfn2vesta iri-run input.fch iri_products \
  --multiwfn /mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI \
  --nthreads 6 \
  --stem h2o \
  --surface-band 0.25
```

如果只需要处理后的 cube 文件，不写 VESTA：

```bash
multiwfn2vesta iri-run input.fch iri_products --no-vesta
```

如果要替换默认 Multiwfn 菜单流，准备一行一个响应的文本文件，然后传
`--commands-file commands.txt`。`iri-run` 启动 Multiwfn 时会同步设置
`Multiwfnpath`、`MULTIWFNPATH` 和 `MultiwfnPATH`。Multiwfn 非零退出、
超时、或返回 0 但缺 `func1.cub`/`func2.cub` 时，CLI 会保留 stdout/stderr
日志并返回非零码。

## 波函数文件到 IGM/IGMH VESTA

如果起点是 Molden/FCHK/WFN/WFX 等 Multiwfn 可读波函数文件，并且已经知道
片段的原子序号，可以直接调用 Multiwfn IGMH、IGM 或 mIGM 菜单并把输出接到 VESTA。
`igmh-run` 默认跑 IGMH，`igm-run` 和 `migm-run` 会分别自动注入
`--method igm` 和 `--method migm`。`igm-run`/`migm-run` 不接受用户再传
`--method` 覆盖，避免命令名和实际 Multiwfn 命令流不一致；需要显式选方法时用
`igmh-run --method igm|migm|igmh`：

```bash
multiwfn2vesta igmh-run \
  input.molden \
  igmh_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --grid-mode spacing \
  --grid-spacing 0.25 \
  --timeout 600

multiwfn2vesta igm-run \
  input.molden \
  igm_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --sl2r-source actual \
  --grid-mode spacing \
  --grid-spacing 0.25
```

默认流程：

- 自动发现 Multiwfn；也可用 `--multiwfn /path/to/Multiwfn_noGUI` 显式指定
- 写 `multiwfn_<method>_input.txt`，记录实际喂给 Multiwfn 的命令流
- 在 `multiwfn_<method>_raw/` 保存 Multiwfn 原始 `dg_inter.cub` 和 `sl2r.cub`
- 如果 Multiwfn 同时写出 `dg_intra.cub`、`dg.cub`、`output.txt`，也会复制到输出目录
- 把 `dg_inter.cub` 作为表面 cube、`sl2r.cub` 作为染色 cube
- IGMH 默认调用 `cube-preset igmh`，IGM/mIGM 默认调用 `cube-preset igm`
  生成 `<stem>_<method>_cube.vesta` 和 recipe

片段参数直接使用 Multiwfn 片段提示可接受的字符串，例如 `1-48`、
`1,4,9`、`49-60` 或补集 `c`。至少需要传两个 `--fragment`，除非用
`--commands-file` 完全替换默认命令流。

`points` 网格模式只适合有限、非周期分子。对于含 `[Cell]` 的 ABACUS/周期性
Molden，Multiwfn PBC 菜单会把选项 `4` 读成 grid spacing，而不是 `NX,NY,NZ`；
因此 `igmh-run` 会在启动 Multiwfn 前拒绝这种组合。周期体系请用
`--grid-mode spacing --grid-spacing 数值`，或用 `--grid-mode pbc-cell` 显式
设置 origin、box length 和 spacing。

IGM/mIGM 在有波函数时会多问一次 sign(lambda2)rho 来源；默认
`--sl2r-source actual`，也可以传 `--sl2r-source promolecular`。IGMH 按
Multiwfn 源码固定使用 actual density，不接受 promolecular。

常用参数：

```bash
multiwfn2vesta igmh-run input.fch igmh_products \
  --multiwfn /mnt/g/work/multiwfn2vesta/tools/Multiwfn_2026.6.2_bin_Linux_noGUI/Multiwfn_noGUI \
  --fragment 1 \
  --fragment 2-3 \
  --grid-mode spacing \
  --grid-spacing 0.15 \
  --nthreads 6 \
  --stem h2o
```

如果只需要 Multiwfn cube 文件，不写 VESTA：

```bash
multiwfn2vesta igmh-run input.fch igmh_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --no-vesta
```

`igmh-run`/`igm-run`/`migm-run` 启动 Multiwfn 时会同步设置 `Multiwfnpath`、`MULTIWFNPATH`
和 `MultiwfnPATH`。Multiwfn 非零退出、超时、或返回 0 但缺
`dg_inter.cub`/`sl2r.cub` 时，CLI 会保留 stdout/stderr 日志并返回非零码。
顶层 `multiwfn2vesta igmh` 仍是 AIM+IGMH overlay 的历史别名；脚本化跑
Multiwfn IGM/IGMH 请用 `igmh-run`、`igm-run` 或 `migm-run`。

## 轨迹到 aIGM/amIGM VESTA

aIGM/amIGM 是 Multiwfn 弱相互作用菜单里的轨迹平均分析，适合 MD/AIMD
这类多帧结构，而不是单帧 ABACUS Molden 波函数分析。默认命令流进入主菜单
`20`，选择 `12` 或 `-12`，输入片段、帧范围和网格，然后用 post-processing
选项 `3` 导出 `avgdg_inter.cub` 和 `avgsl2r.cub`。

```bash
multiwfn2vesta aigm-run trajectory.xyz aigm_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --frame-range 1 200 \
  --periodic \
  --grid-mode spacing \
  --grid-spacing 0.25 \
  --timeout 1200

multiwfn2vesta amigm-run trajectory.xyz amigm_products \
  --fragment 1-48 \
  --fragment c \
  --export-tfi \
  --tfi-vesta
```

默认流程：

- 自动发现 Multiwfn；也可用 `--multiwfn /path/to/Multiwfn_noGUI` 显式指定
- 写 `multiwfn_<method>_input.txt`，记录实际喂给 Multiwfn 的命令流
- 在 `multiwfn_<method>_raw/` 保存原始 `avgdg_inter.cub` 和 `avgsl2r.cub`
- 复制为 `<stem>_avgdg_inter.cub` 和 `<stem>_avgsl2r.cub`
- 默认调用 `cube-preset aigm` 写 `<stem>_<method>_cube.vesta`
- `--export-rdg` 额外导出 `<stem>_avgRDG.cub`
- `--export-tfi` 额外导出 `<stem>_thermflu.cub`
- `--tfi-vesta` 在已有 `--export-tfi` 时额外调用 `cube-preset aigm-tfi`
- `--export-scatter` 额外导出 `<stem>_multiwfn_<method>_output.txt`

`aigm-run` 是通用入口，可用 `--method aigm|amigm` 显式选择方法；
`amigm-run` 固定为 amIGM 并拒绝额外 `--method`，避免命令名和实际菜单流不一致。
片段参数直接使用 Multiwfn 片段提示可接受的字符串，例如 `1-48`、`1,4,9`、
`49-60` 或补集 `c`。帧序号从 1 开始；不传 `--frame-range` 时，程序向
Multiwfn 发送空行，让 Multiwfn 读取全部帧。

周期性轨迹应使用 `--periodic --grid-mode spacing --grid-spacing VALUE`
或 `--grid-mode pbc-cell`。程序会轻量识别 `Lattice=`、`pbc=`、`CRYST1`
这类常见周期标记，并在周期轨迹下拒绝 `--grid-mode points`，因为 Multiwfn
PBC 网格菜单的选项 `4` 读取的是 spacing，而不是 `NX,NY,NZ`。

这个 runner 只负责调用 Multiwfn 并生成 VESTA 文件，不启动 VESTA 图形界面。
Multiwfn 非零退出、超时、或返回 0 但缺 `avgdg_inter.cub`/`avgsl2r.cub` 时，
CLI 会保留 stdout/stderr 日志并返回非零码。

## XYZ/extXYZ 轨迹到 VESTA frame

`trajectory-frames` 负责轨迹视频工作流的上游 frame 生成。它读取标准
XYZ 或 extXYZ 轨迹，写逐帧 `.vesta` 文件和一个 manifest/recipe，不依赖
ASE，不启动 VESTA，也不输出 PNG。

最小 Cd/Cl example：

```bash
multiwfn2vesta trajectory-frames examples/cdcl_trajectory_video/cdcl_tiny.extxyz \
  /tmp/cdcl_vesta_frames \
  --bond Cd Cl 0 3.5 \
  --boundary -0.05 1.05 -0.05 1.05 -0.05 1.05
```

如果有一个手动调好视角、style 和成键显示的 `.vesta`，可以复用它的
`SCENE`/`STYLE` 尾段：

```bash
multiwfn2vesta trajectory-frames traj.extxyz frame_products \
  --reference-vesta nvt_frame_0001_saved.vesta \
  --bond Cd Cl 0 3.5 \
  --boundary -0.05 1.05 -0.05 1.05 -0.05 1.05 \
  --stride 20
```

输出：

- `vesta/frame_0001.vesta` 等逐帧 VESTA 文件。
- `frame_trajectory_frames_manifest.json`: 源轨迹、帧序号、Boundary、bond
  rules、reference `.vesta` 等参数。
- `frame_trajectory_frames_recipe.md`: 下一步渲染 PNG 和调用
  `trajectory-video` 的说明。

当前明确边界：

- extXYZ `Lattice="..."` 会自动转为晶体结构；普通 XYZ 可用
  `--cell-vectors` 手动给晶胞。
- ASE `.traj` 还没有直接读取入口，需先转 XYZ/extXYZ。
- VESTA PNG 渲染仍是外部步骤，避免自动打开 GUI 抢焦点。

## 已渲染轨迹帧到 MP4

`trajectory-video` 是 VESTA 轨迹视频工作流里已经维护的合成层。它读取已渲染的
PNG 序列，按自然顺序排序，写 ffmpeg concat 清单和 recipe，默认不执行
ffmpeg：

```bash
multiwfn2vesta trajectory-video png_frames trajectory.mp4 \
  --fps 24 \
  --bitrate 20M
```

如果已经使用 curated example manifest 记录了 smoke 证据，可以直接从 manifest
定位 PNG 帧目录，并用 `--output` 指定新视频路径：

```bash
multiwfn2vesta trajectory-video \
  --manifest examples/cdcl_trajectory_video/artifact_manifest.json \
  --output /tmp/cdcl_trajectory.mp4 \
  --fps 24 \
  --bitrate 20M
```

输出：

- `<output>_frames.txt`: ffmpeg concat 输入清单。
- `<output>_trajectory_video_recipe.md`: 帧目录、帧数、首尾帧、编码参数和完整命令。
- `<output>.mp4`: 只有加 `--run` 且 ffmpeg 成功时才生成。

常用选项：

- `--run`: 立即执行 ffmpeg。
- `--overwrite`: 允许替换已有输出视频。
- `--crf N`: 使用 CRF 质量模式，替代固定 `--bitrate`。
- `--extra-ffmpeg-arg ARG`: 追加单个 ffmpeg 参数，可重复。

这个命令不启动 VESTA。XYZ/extXYZ 到 `.vesta` frame 已由 `trajectory-frames`
维护；仍待补的是 ASE `.traj` 直接读取和不抢焦点的 VESTA PNG 渲染层。

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

## Multiwfn 原子表着色

当 Multiwfn 给出的是原子电荷、Fukui-like 原子指标、轨道/片段原子贡献等
原子标量表，而不是 ABACUS `mulliken.txt` 这种固定格式时，用通用入口：

```bash
multiwfn2vesta multiwfn-atom-color \
  structure.vesta \
  atom_values.txt \
  structure_atom_values.vesta \
  --value-column charge \
  --vmin -1 --vmax 1 \
  --write-values parsed_atom_values.csv
```

输入可以是 CSV、TSV 或空白分隔文本。常见格式示例：

```text
Atom Label Charge
1 C1 -0.12
2 H1  0.08
```

`Atom`、`index`、`label`、`charge`、`value`、`fukui`、`dual`、
`contribution`、`weight` 等表头会被自动识别。一个表有多个数值列时，
用 `--value-column` 指定要着色的列；key 列不明显时用 `--key-column`。
没有表头的一列数据会被当作 VESTA `STRUC` 顺序值。默认严格模式要求表格
原子序号、label 或有序行数与选中的 VESTA 结构完全一致；只有明确给子集
着色时才用 `--non-strict`。

## ABACUS 计算到 Multiwfn Molden

ABACUS LCAO 波函数分析的上游入口是：

```bash
multiwfn2vesta abacus-molden \
  /path/to/abacus_calc \
  /path/to/ABACUS_Multiwfn.molden
```

这个命令默认从
`/mnt/g/work/multiwfn2vesta/downloads/abacus_latest_molden/abacus-develop`
的 `origin/develop` 导出
`interfaces/Multiwfn_interface/molden.py`，把脚本副本放在输出 Molden 同目录，
再运行 ABACUS converter。运行结束后会写：

- `<stem>_abacus_molden.py`: 实际使用的 ABACUS converter 副本
- `<stem>_abacus_molden.stdout.txt`
- `<stem>_abacus_molden.stderr.txt`
- `<stem>_abacus_molden_recipe.md`: 记录 ABACUS repo、git ref、commit、
  source path、SHA256、命令行和 Molden 检查结果
- 输出 Molden 文件本身

ABACUS upstream converter 需要运行它的 Python 环境里有 `numpy`、`scipy` 和
`matplotlib`。`abacus-molden` 默认会先检查这三个模块；如果当前
`python3` 环境不满足，用 `--python /path/to/python` 指向对应环境。
`--no-dependency-check` 只跳过预检查，不会移除 upstream converter 的真实依赖。

常用参数：

```bash
multiwfn2vesta abacus-molden abacus_calc ABACUS_Multiwfn.molden \
  --fetch \
  --git-ref origin/develop \
  --python /path/to/python-with-numpy-scipy-matplotlib \
  --ngto 7 \
  --rel-r 2 \
  --with-cell true \
  --with-Nval true \
  --with-pseudo false
```

ABACUS 当前 latest `develop` 的 converter 要求计算目录里有字面文件
`INPUT`、`KPT`、`STRU` 和对应的 `OUT.<suffix>`。推荐 ABACUS 设置：

```text
basis_type lcao
gamma_only 1
out_wfc_lcao 1
```

当前 converter 只支持 `nspin=1/2` 和 Gamma/单 k 点；不支持 `nspin=4`/SOC
和多 k。`--with-Nval true` 是默认值，也是赝势体系给 Multiwfn 使用时应保留
的设置。ABACUS 的 NAO2GTO 过程可能会在 `orbital_dir` 旁边写 `.gto` 和
`.gto.png` 副产物，因此该目录需要可写。

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
