# Benzene dimer weak-interaction scalar suite

## 体系价值

- 体系：benzene dimer 或取代芳香二聚体。
- 对应功能：`iri-run`、RDG/DORI/Delta-g、RoSE/SEDD、vdW component、on-top pair density。
- 为什么值得作为示例：pi-stacking/色散相互作用直观，体系比 Ag slab 小，适合做弱相互作用标量场的快速教程。
- 不适合说明的问题：不覆盖周期性边界和金属表面吸附。

## 输入文件

| 文件 | 来源 | 是否提交 | 备注 |
| --- | --- | --- | --- |
| `benzene_dimer.molden` | Gaussian/ORCA/ABACUS LCAO 等可被 Multiwfn 读入的波函数 | 否 | 需要几何和电子态稳定 |
| `density.cub` | Multiwfn density 或 ABACUS direct cube | 否 | 可用于 mapped-surface |

## 推荐命令

```bash
cd /mnt/g/work/multiwfn2vesta/project
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH

multiwfn2vesta iri-run benzene_dimer.molden products/iri \
  --grid-points 120 120 120

multiwfn2vesta grid-run benzene_dimer.molden products/rose \
  --function rose

multiwfn2vesta grid-run benzene_dimer.molden products/sedd \
  --function sedd

multiwfn2vesta grid-run benzene_dimer.molden products/ontop_pair \
  --function on-top-pair-density \
  --pair-correlation-type 3

multiwfn2vesta grid-run benzene_dimer.molden products/vdw \
  --function vdw-potential \
  --vdw-probe C
```

## 输出文件

| 文件 | 作用 | 是否应提交 |
| --- | --- | --- |
| `products/iri/*cub` | IRI/RDG surface 和 texture cube | 否 |
| `products/rose/userfunc.cub` | RoSE cube | 否 |
| `products/sedd/userfunc.cub` | SEDD cube | 否 |
| `products/ontop_pair/userfunc.cub` | on-top pair density cube | 否 |
| `products/*/*.vesta` | VESTA 场景 | 小文件可选 |
| `docs/assets/gallery/benzene_dimer_scalar_suite_*.png` | 配对效果图 | 是，生成后再加入 |

## 效果图状态

尚无正式 PNG。正式图建议至少包含两列：IRI/RDG 或 DORI 用于弱相互作用直观展示，RoSE/SEDD 或 on-top pair density 用于电子结构诊断对照。

## 验收条件

```bash
multiwfn2vesta examples --id benzene_dimer_scalar_suite --verify
multiwfn2vesta examples --command on-top-pair --json
multiwfn2vesta examples --command rose --json
```

升为 `ready` 前需要记录 cube 最小/最大值、选定等值面、VESTA sections 是否关闭，以及至少一张项目内 PNG。

