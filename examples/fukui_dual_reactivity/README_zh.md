# Fukui and dual-descriptor reactivity suite

## 体系价值

- 体系：coronene、nitro/hetero aromatic 或其它带清晰反应位点的芳香分子，需有中性、阳离子、阴离子三态。
- 对应功能：`fukui-run`、`cube-arith`、orbital-weighted Fukui/dual descriptor、Multiwfn atom table coloring。
- 为什么值得作为示例：能把体数据反应性、原子凝聚 Fukui 值和颜色映射串起来，是按数值给原子染色的主线应用之一。coronene 适合展示多中心芳香体系的 condensed Fukui/颜色映射；含硝基或杂原子芳香体系更适合展示正负区域差异。
- 不适合说明的问题：不适合只用单个中性波函数完成；三态必须同网格或可严格对齐。

## 输入文件

| 文件 | 来源 | 是否提交 | 备注 |
| --- | --- | --- | --- |
| `neutral.cub` | 中性态 density cube | 否 | 和其他态同网格 |
| `cation.cub` | 阳离子 density cube | 否 | 和其他态同网格 |
| `anion.cub` | 阴离子 density cube | 否 | 和其他态同网格 |
| `atom_values.csv` | condensed Fukui 或电荷表 | 可提交小表 | 用于 atom coloring |

第一版建议先固定一个体系，不要在一个 tutorial 里混用多个分子。验收图至少需要 dual descriptor signed surface 和同一结构上的 atom-value coloring。

## 推荐命令

```bash
cd /mnt/g/work/multiwfn2vesta/project
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH

multiwfn2vesta fukui-run products/fukui \
  --neutral neutral.molden \
  --anion anion.molden \
  --cation cation.molden \
  --grid-points 80 80 80

# 如果已经有同网格三态 density cube，可直接走 cube-arith 分支：
multiwfn2vesta cube-arith products/dual_descriptor \
  --operation dual-descriptor \
  --neutral-cube neutral.cub \
  --anion-cube anion.cub \
  --cation-cube cation.cub \
  --preset signed \
  --isosurface 0.002

multiwfn2vesta cube-preset signed products/dual_descriptor/dual_descriptor.cub products/dual_vesta \
  --isosurface 0.002

multiwfn2vesta multiwfn-atom-color structure.vesta atom_values.csv products/atom_colored.vesta
```

## 输出文件

| 文件 | 作用 | 是否应提交 |
| --- | --- | --- |
| `products/fukui/*.cub` | Fukui+/Fukui-/dual cube | 否 |
| `products/dual_vesta/*.vesta` | dual descriptor 可视化 | 小文件可选 |
| `products/atom_colored.vesta` | 原子数值染色结构 | 小文件可选 |
| `docs/assets/gallery/fukui_dual_reactivity_*.png` | 反应性效果图 | 是，生成后再加入 |

## 效果图状态

尚无正式 PNG。第一版应至少包含 dual descriptor 正负等值面和一张按 condensed value 着色的原子结构图。

## 验收条件

```bash
multiwfn2vesta examples --id fukui_dual_reactivity --verify
multiwfn2vesta examples --command fukui-run --json
multiwfn2vesta examples --command atom-color --json
```

升为 `ready` 前需要记录三态电荷/自旋、网格一致性检查和原子染色色标。
