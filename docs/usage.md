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
multiwfn2vesta abacus-molden --help
multiwfn2vesta molden-check --help
multiwfn2vesta cube-vesta --help
multiwfn2vesta cube-preset --help
multiwfn2vesta surface-extrema --help
multiwfn2vesta cube-arith --help
multiwfn2vesta iri-run --help
multiwfn2vesta grid-run --help
multiwfn2vesta abacus-mulliken-color --help
multiwfn2vesta multiwfn-atom-color --help
multiwfn2vesta aim-run --help
multiwfn2vesta aim-pdb --help
multiwfn2vesta aim-igmh --help
```

已维护的子命令：

- `discover`: 报告 Multiwfn 和 VESTA 可执行文件候选，以及当前会选择的路径
- `abacus-molden`: 从 ABACUS LCAO 计算目录调用最新
  `interfaces/Multiwfn_interface/molden.py`，生成并验证给 Multiwfn 用的
  Molden 文件
- `molden-check`: 在调用 Multiwfn 前检查 Molden 文件是否含有必要段；ABACUS
  模式会要求 `[Cell]` 和 `[Nval]`
- `cube-vesta`: 从 ABACUS/Multiwfn scalar cube 直接生成 `.vesta`，可选
  texture/color cube，默认关闭 section plane
- `cube-preset`: 在 `cube-vesta` 后端上套用常见分析默认值，例如 density、
  orbital/signed、ELF/LOL、IRI/RDG/NCI、IGM/IGMH/aIGM、ESP/MEP、
  ALIE/LEA/LEAE、vdW map
- `surface-extrema`: 把 Multiwfn `surfanalysis.pdb` 的分子表面极值点作为
  atoms-only phase 叠加到已有 `.vesta` 文件中
- `cube-arith`: 对兼容 cube 做线性组合，用于 density difference、Fukui
  function、dual descriptor 等后处理，并可直接接 `cube-preset` 写 `.vesta`
- `iri-run`: 从 Multiwfn 可读波函数文件调用 IRI/RDG 弱相互作用菜单，
  生成 `func1.cub`/`func2.cub`，处理成 VESTA 可用的 `IRI1`/`IRI2` cube，
  再通过 `cube-preset iri` 写 mapped-surface `.vesta`
- `grid-run`: 从 Multiwfn 可读波函数文件调用主菜单 `5` 的 real-space
  function grid，导出 density、MO/orbital、Laplacian、K(r)/G(r)、ELF、LOL、
  ESP/MEP、ALIE、RDG/IRI-like、promolecular RDG/sign(lambda2)rho 等单 cube，
  并可自动接 `cube-preset` 写 `.vesta`
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

`aim-run`、`iri-run` 和 `grid-run` 本身只启动 Multiwfn，不启动 VESTA；
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
multiwfn2vesta cube-preset elf ELF.cub cube_products
multiwfn2vesta cube-preset rdg IRI2_surface.cub cube_products \
  --texture-cube IRI1_color.cub
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
- `signed`：正/负等值面，别名包括 `orbital`、`wavefunction`、
  `density-difference` 和 `dual-descriptor`
- `elf` / `lol`：局域化函数等值面
- `iri`：别名 `rdg`、`nci`，需要 `--texture-cube`，默认
  `--tex-physical -0.04 0.04` 和 `--tex-range-source surface-band`
- `igmh`：别名包括 `igm`、`igm-inter`、`igmh-inter`，用 `dg_inter.cub`
  加 `sl2r.cub`，默认等值面 `0.01`，染色范围 `-0.05` 到 `0.05`，对齐
  Multiwfn `IGM_inter.vmd`
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

## Cube 算术：密度差 / Fukui / dual descriptor

`cube-arith` 是兼容 cube 的线性组合工具。它适合把 ABACUS 或 Multiwfn 已经
生成好的同网格密度/波函数/差分 cube 组合成新的 cube，再交给 `cube-preset`
画 VESTA 等值面。它不负责生成带电态波函数本身；带电态、中性态、激发态或
不同片段的 cube 要先由 ABACUS、Multiwfn 或 `grid-run` 产生。

任意线性组合：

```bash
multiwfn2vesta cube-arith cube_arith_products \
  --term 1.0 rho_a.cub \
  --term -1.0 rho_b.cub \
  --stem density_difference
```

Fukui 和 dual descriptor 快捷入口：

```bash
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
- `fukui-plus`: `rho(N+1) - rho(N)`
- `fukui-minus`: `rho(N) - rho(N-1)`
- `dual-descriptor`: `rho(N+1) - 2*rho(N) + rho(N-1)`

默认输出：

- `<stem>.cub`
- `<stem>_cube_arith_recipe.md`
- 默认 `--preset auto`：`fukui-plus/minus` 用 `density`，`density-difference`、
  `dual-descriptor` 和任意 `linear` 组合用 `signed`

兼容性规则：

- 所有输入 cube 必须有相同 grid origin、grid vectors、点数和 cube 单位约定；
  默认 `--cube-units auto` 下正 grid count 视为 Bohr，负 grid count 视为
  Angstrom，混用会被拒绝
- 默认还要求 atom list 一致；确认只需要共用格点时可用 `--no-strict-atoms`
- 程序拒绝把输出 cube 写到任何输入 cube 路径上，避免覆盖原始数据
- 若只想生成 cube，不写 VESTA，用 `--no-vesta`

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
- `orbital` / `mo`：函数 `4`，原始输出 `MOvalue.cub`，默认接 `signed`；
  单轨道用 `--orbital h`，多轨道批量用 `--orbitals h l l+1`
- `orbital-density` / `orbdens`：函数 `44`，原始输出 `orbdens.cub`，
  单轨道用 `--orbital`，多轨道批量用 `--orbitals`
- `hamiltonian-ked` / `k(r)`：函数 `6`，原始输出 `K(r).cub`；
  `lagrangian-ked` / `g(r)`：函数 `7`，原始输出 `G(r).cub`
- `laplacian`、`spin-density`、`esp`、`nuclear-esp`、
  `signlambda2rho`、`vdw-potential`：默认按 signed scalar 处理
- `alie` / `avglocion`：函数 `18`，原始输出 `avglocion.cub`；常规 ALIE
  表面图要再和 `density.cub` 通过 `cube-preset alie` 组合
- `elf` / `lol`：局域化函数等值面
- `rdg` / `promolecular-rdg` / `signlambda2rho` /
  `promolecular-signlambda2rho` / `iri` / `delta-g`：单标量 cube；如果要
  IRI/RDG/NCI 那种 surface+texture 双 cube 图，优先用 `iri-run` 或显式
  `cube-preset iri`

轨道例子：

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function orbital \
  --orbital h \
  --grid-mode points \
  --grid-points 80 80 80
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
`--commands-file`、`--expected-cube` 和 `--raw-dir`，因为每个子任务需要独立的
命令流和 raw 目录。

复用已有 cube 的格点，便于后续做双 cube 或多图层叠加：

```bash
multiwfn2vesta grid-run input.fch grid_products \
  --function esp \
  --grid-mode cube \
  --grid-cube density.cub \
  --no-vesta
```

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

注意：`grid-run` 的每个子任务仍然只生成一个 scalar cube。ESP-on-density、
IRI/RDG/NCI mapped surface、IGM/IGMH/aIGM 这类需要 surface cube +
texture cube 或 fragment 定义的图，仍然要通过 `cube-preset`/`cube-vesta`
组合，或使用专门的 `iri-run`、`aim-igmh` 流程。当前 `cube-preset igmh`
只负责把已有 `dg_inter.cub`/`sl2r.cub` 写成 VESTA；从波函数自动调用
Multiwfn IGMH fragment 菜单仍是后续任务。

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
