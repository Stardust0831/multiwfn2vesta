# H2O domain and basic scalar baseline

## 体系价值

- 体系：H2O 或另一个小极性分子。
- 对应功能：`domain-run`、density、gradient、Laplacian、ESP、KED 基础 grid-run。
- 为什么值得作为示例：体系小，适合快速回归和演示 domain/binary surface 的基本参数，不会替代真实材料/界面主图。
- 不适合说明的问题：不适合展示复杂弱相互作用或周期性边界。

## 输入文件

| 文件 | 来源 | 是否提交 | 备注 |
| --- | --- | --- | --- |
| `h2o.molden` | 任意可被 Multiwfn 读入的 H2O 波函数 | 可提交小输入需确认来源 | 适合轻量 smoke |
| `domain.cub` | Multiwfn domain 输出 | 否 | 本地未跟踪文件不要误提交 |

## 推荐命令

```bash
cd /mnt/g/work/multiwfn2vesta/project
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH

multiwfn2vesta grid-run h2o.molden products/density \
  --function density \
  --grid-points 80 80 80

multiwfn2vesta grid-run h2o.molden products/esp \
  --function esp \
  --surface-cube products/density/density.cub \
  --tex-physical -0.05 0.05

multiwfn2vesta domain-run h2o.molden products/domain

multiwfn2vesta cube-preset domain products/domain/domain.cub products/domain_vesta
```

## 输出文件

| 文件 | 作用 | 是否应提交 |
| --- | --- | --- |
| `products/density/*.cub` | density cube | 否 |
| `products/domain/domain.cub` | domain binary cube | 否 |
| `products/domain_vesta/*.vesta` | domain VESTA 场景 | 小文件可选 |
| `docs/assets/gallery/h2o_domain_baseline_*.png` | domain/basic scalar 效果图 | 是，生成后再加入 |

## 效果图状态

尚无正式 PNG。当前工作区根目录可能有未跟踪 `domain.cub` / `domain.pdb`，这些是本地探针文件，不能随本 example 提交。

## 验收条件

```bash
multiwfn2vesta examples --id h2o_domain_baseline --verify
multiwfn2vesta examples --command domain-run --json
```

升为 `ready` 前需要一张 domain surface PNG 和一张基础 density/ESP 对照图，并记录 domain criterion。

