# COF monolayer direct-cube suite

## 体系价值

- 体系：COF_12000N2 单层加真空层，或同类二维 COF。
- 对应功能：`cube-vesta`、`cube-preset`、ABACUS direct density/potential/ELF/partial charge/wavefunction norm、atom coloring。
- 为什么值得作为示例：二维多孔材料能展示周期性 cell、真空层、孔道、静电势和电荷分布，比小分子 cube 更接近材料计算需求。
- 不适合说明的问题：不适合作为快速 smoke；ABACUS 输出文件较大。

## 输入文件

| 文件 | 来源 | 是否提交 | 备注 |
| --- | --- | --- | --- |
| `COF_12000N2_monolayer.cif` | 原始 COF CIF 改成单层并加真空 | 可提交小结构，需确认版权/来源 | 需要记录 vacuum 和 cell |
| `OUT.*/*rho*.cube` | ABACUS direct density | 否 | 用 `cube-preset density` |
| `OUT.*/*pot*.cube` | ABACUS electrostatic potential | 否 | 用 `cube-preset potential` |
| `OUT.*/*elf*.cube` | ABACUS ELF 或 Multiwfn ELF | 否 | 用 `cube-preset elf` |

## 推荐命令

```bash
cd /mnt/g/work/multiwfn2vesta/project
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH

multiwfn2vesta cube-preset density rho.cube products/rho
multiwfn2vesta cube-preset potential electrostatic_potential.cube products/potential
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

尚无正式 PNG。第一张图建议选 electrostatic potential 或 ELF，因为孔道和带电官能团的信息量高；density 可作为结构参考。

## 验收条件

```bash
multiwfn2vesta examples --id cof_direct_cube_suite --verify
multiwfn2vesta examples --command cube-preset --json
```

升为 `ready` 前必须记录 COF 单层生成方式、真空层厚度、ABACUS 输出 cube 名称和 VESTA Boundary。

