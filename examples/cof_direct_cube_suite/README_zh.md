# COF monolayer direct-cube suite

状态：planned / ready-to-run input。这个 example 现在专门面向“COF 单层 `rho=0.001` 电子密度范德华表面 + ABACUS electrostatic potential texture 染色”。当前仓库没有真实 ABACUS direct cube 输出，因此还不能标为 ready/gallery。

## 体系价值

- 体系：COF_12000N2 单层加真空层，或同类二维 COF。
- 对应功能：`cube-vesta`、`cube-preset`、ABACUS direct density/potential/ELF/partial charge/wavefunction norm、atom coloring。
- 为什么值得作为示例：二维多孔材料能展示周期性 cell、真空层、孔道、静电势和电荷分布，比小分子 cube 更接近材料计算需求。
- 不适合说明的问题：不适合作为快速 smoke；ABACUS 输出文件较大。

## 输入文件

| 文件 | 来源 | 是否提交 | 备注 |
| --- | --- | --- | --- |
| `STRU` | `COF_12000N2.cif` 转 ABACUS STRU，单层，25 A 真空 | 是 | `z=0.5`，cell c=25 A |
| `INPUT.esp` | ABACUS direct cube 输入 | 是 | PW 路线，`out_chg 1 8` 和 `out_pot 2 8` |
| `sample_esp/` | 离线最小 cube workflow | 是 | 小 cube 输入、真空归零输出和 VESTA `.vesta`，用于测试命令格式 |
| `OUT.cof12000n2_esp/chg.cube` | ABACUS direct density | 否 | `rho=0.001` 作范德华表面 |
| `OUT.cof12000n2_esp/potes.cube` | ABACUS electrostatic potential | 否 | 需真空平台归零后作 texture |
| `OUT.*/*elf*.cube` | ABACUS ELF 或 Multiwfn ELF | 否 | 用 `cube-preset elf` |

## ABACUS 运行

```bash
cd /mnt/g/work/multiwfn2vesta/project
cd examples/cof_direct_cube_suite

cp INPUT.esp INPUT
abacus > abacus_esp.log 2>&1
```

如果 PP 不在 `../../../downloads/abacus_latest_molden/abacus-develop/tests/PP_ORB`，需要改 `INPUT.esp` 的 `pseudo_dir`。这个 ESP example 默认使用 `basis_type pw`，避免依赖元素齐全的数值原子轨道文件；如果改回 LCAO，需要同时准备 C/H/N/O 的 `.orb` 并设置 `orbital_dir`。

服务器实跑记录：

- 远端目录：`~/multiwfn2vesta_runs/cof_esp_20260621`
- ABACUS：`abacus/v3.11.0-beta4-sm70-avx512`
- Slurm 作业：`533613`
- 启动命令：`mpirun --bind-to none --map-by slot -np 8 abacus`
- 经验：该集群 `4V100PX` 分区单 GPU 作业需要 `--qos=rush-1o2gpu --gres=gpu:1`，不要显式写 `--cpus-per-task`；直接 `srun abacus` 会启动 8 个互相覆盖的串行 ABACUS 实例，不能用于这个作业。

## ESP 表面图命令

ABACUS 当前 develop 输出名应为：

```text
OUT.cof12000n2_esp/chg.cube
OUT.cof12000n2_esp/potes.cube
```

先把电势按真空平台归零：

```bash
multiwfn2vesta abacus-esp-align \
  OUT.cof12000n2_esp/potes.cube \
  products/potes_vacuum0.cube \
  --axis z \
  --vacuum-side both \
  --vacuum-fraction 0.12 \
  --profile-csv products/potes_profile.csv \
  --report-md products/potes_alignment.md
```

再用 `rho=0.001` 电子密度表面染 ESP：

```bash
multiwfn2vesta cube-preset density \
  OUT.cof12000n2_esp/chg.cube \
  products/esp_surface \
  --texture-cube products/potes_vacuum0.cube \
  --isosurface 0.001 \
  --tex-physical -0.06 0.06 \
  --tex-range-source surface-band \
  --structure crystal
```

## 离线 sample

`sample_esp/` 提供一个 2x2x2 的小 cube workflow，可直接验证 ESP 真空归零
和 VESTA surface texture 写法：

```bash
multiwfn2vesta abacus-esp-align \
  examples/cof_direct_cube_suite/sample_esp/potes_demo.cube \
  examples/cof_direct_cube_suite/sample_esp/potes_demo_vacuum0.cube \
  --axis z \
  --vacuum-side high \
  --vacuum-fraction 0.5 \
  --profile-csv examples/cof_direct_cube_suite/sample_esp/potes_demo_profile.csv \
  --report-md examples/cof_direct_cube_suite/sample_esp/potes_demo_alignment.md

multiwfn2vesta cube-preset esp \
  examples/cof_direct_cube_suite/sample_esp/rho_demo.cube \
  examples/cof_direct_cube_suite/sample_esp/vesta_demo \
  --texture-cube examples/cof_direct_cube_suite/sample_esp/potes_demo_vacuum0.cube \
  --isosurface 0.001 \
  --tex-physical -3.5 1.5 \
  --stem rho_demo_esp
```

sample 输出文件：

```text
sample_esp/potes_demo_vacuum0.cube
sample_esp/potes_demo_profile.csv
sample_esp/potes_demo_alignment.md
sample_esp/vesta_demo/rho_demo_esp_cube.vesta
sample_esp/vesta_demo/rho_demo_esp_cube_vesta_recipe.md
```

真实 COF 图仍应使用 ABACUS 输出的 `chg.cube` 和 `potes.cube`，sample 只用于
检查命令、文件格式和 VESTA texture pipeline。

其它 direct cube 可视化：

```bash
multiwfn2vesta cube-preset potential products/potes_vacuum0.cube products/potential
multiwfn2vesta cube-preset elf ELF.cub products/elf
multiwfn2vesta cube-preset partial-charge partial_charge.cube products/partial_charge
multiwfn2vesta cube-preset wavefunction-norm wfc_norm.cube products/wfc_norm
```

## 输出文件

| 文件 | 作用 | 是否应提交 |
| --- | --- | --- |
| `products/*/*.vesta` | VESTA 场景 | 小文件可选 |
| `products/*/*recipe.md` | 复现参数 | 是 |
| `docs/assets/gallery/cof_direct_cube_suite_*.png` | COF direct cube 效果图 | 是，生成后再加入 |

## 效果图状态

尚无正式 PNG。第一张正式图应为 `rho=0.001` density surface colored by vacuum-aligned `potes.cube`，优先渲染 top view 和一个倾斜 view，展示孔道边缘的正/负电势分布。

## 验收条件

```bash
multiwfn2vesta examples --id cof_direct_cube_suite --verify
multiwfn2vesta examples --command cube-preset --json
```

升为 `ready` 前必须记录 COF 单层生成方式、真空层厚度、ABACUS 输出 cube 名称、真空归零窗口、`rho=0.001` 等值面、ESP 色标范围和 VESTA Boundary。
