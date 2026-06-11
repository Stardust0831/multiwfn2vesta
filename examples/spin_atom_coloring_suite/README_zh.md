# Spin and atom-value coloring suite

## 体系价值

- 体系：open-shell 小分子、磁性氧化物或自旋极化吸附体系。
- 对应功能：spin density、alpha/beta density、spin polarization、`abacus-mulliken-color`、`multiwfn-atom-color`。
- 为什么值得作为示例：它能把体相自旋密度和原子局域磁矩/电荷颜色联系起来，替代当前 Fe toy smoke。
- 不适合说明的问题：不适合 closed-shell 体系；没有自旋或电荷差异时图像信息量很低。

## 输入文件

| 文件 | 来源 | 是否提交 | 备注 |
| --- | --- | --- | --- |
| `spin_system.molden` | 自旋极化波函数 | 否 | 可由 ABACUS LCAO Molden 或其他程序给出 |
| `mulliken.txt` | ABACUS Mulliken 电荷/磁矩 | 可提交小型脱敏片段 | 用于 `abacus-mulliken-color` |
| `atom_values.csv` | Multiwfn 原子表或整理后的数值 | 可提交小表 | 用于 generic atom coloring |

## 推荐命令

```bash
cd /mnt/g/work/multiwfn2vesta/project
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH

multiwfn2vesta grid-run spin_system.molden products/spin_density \
  --function spin-density

multiwfn2vesta grid-run spin_system.molden products/spin_polarization \
  --function spin-polarization

multiwfn2vesta abacus-mulliken-color structure.vesta mulliken.txt products/mulliken_colored.vesta \
  --column magnetism

multiwfn2vesta multiwfn-atom-color structure.vesta atom_values.csv products/atom_colored.vesta
```

## 输出文件

| 文件 | 作用 | 是否应提交 |
| --- | --- | --- |
| `products/spin_density/*.cub` | 自旋密度 cube | 否 |
| `products/*colored.vesta` | 原子数值染色结构 | 小文件可选 |
| `docs/assets/gallery/spin_atom_coloring_suite_*.png` | 自旋/原子染色效果图 | 是，生成后再加入 |

## 效果图状态

尚无正式 PNG。正式图需要同时展示 signed spin-density surface 和原子磁矩/电荷颜色，最好带色标或在图注中写清数值范围。

## 验收条件

```bash
multiwfn2vesta examples --id spin_atom_coloring_suite --verify
multiwfn2vesta examples --command spin-density --json
multiwfn2vesta examples --command mulliken-color --json
```

升为 `ready` 前需要替换当前 toy smoke，选用真实自旋体系并记录 atom-value mapping 规则。

