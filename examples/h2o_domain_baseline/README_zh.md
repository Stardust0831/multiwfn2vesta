# H2O domain and basic scalar baseline

## 体系价值

- 体系：H2O 或另一个小极性分子。
- 对应功能：`domain-run`、density、gradient、Laplacian、ESP、基础 KED 和扩展 KED diagnostics 的 `grid-run`。
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

multiwfn2vesta grid-run h2o.molden products/ked_tf \
  --function thomas-fermi-ked

multiwfn2vesta grid-run h2o.molden products/ked_diff \
  --function tf-minus-lagrangian-ked

multiwfn2vesta grid-run h2o.molden products/ked_local_temperature \
  --function lagrangian-local-temperature \
  --ked-density-cutoff 1e-6

multiwfn2vesta grid-run h2o.molden products/ked_potential \
  --function thomas-fermi-ked-potential

multiwfn2vesta domain-run products/density/h2o_density.cub products/domain \
  --criterion '<0.5' \
  --domain-index 1

multiwfn2vesta cube-preset domain products/domain/domain.cub products/domain_vesta
```

## 输出文件

| 文件 | 作用 | 是否应提交 |
| --- | --- | --- |
| `products/density/*.cub` | density cube；同时作为 `domain-run` 输入 | 否 |
| `products/ked_tf/*userfunc*.cub` | Thomas-Fermi KED 或其它 selected KED cube | 否 |
| `products/ked_diff/*userfunc*.cub` | KED 差值诊断 cube | 否 |
| `products/ked_local_temperature/*userfunc*.cub` | KED-derived local temperature cube | 否 |
| `products/ked_potential/*userfunc*.cub` | KED functional potential cube | 否 |
| `products/domain/domain.cub` | domain binary cube | 否 |
| `products/domain_vesta/*.vesta` | domain VESTA 场景 | 小文件可选 |
| `docs/assets/gallery/h2o_domain_baseline_*.png` | domain/basic scalar 效果图 | 是，生成后再加入 |

## 效果图状态

尚无正式 PNG。`domain-run` 的输入是已有 cube/grid 文件，不是 `.molden` 波函数；本 runbook 先用 `grid-run --function density` 生成 density cube，再对该 cube 做 domain analysis。当前工作区根目录可能有未跟踪 `domain.cub` / `domain.pdb`，这些是本地探针文件，不能随本 example 提交。

KED diagnostics 的正式图建议只选 2-3 张进入手册：selected KED、一个 signed
KED difference、一个 local temperature 或 KED potential。`--ked-density-cutoff`
会覆盖 run-local Multiwfn `uservar`；不传时维护态 KED 路线会显式写
`uservar=0`，避免继承全局旧设置。源码里非零 `uservar` 也会影响 KED 评价本身，
因此它是稳定性参数，不是普通后处理遮罩；正式记录必须写明所用值。

## 验收条件

```bash
multiwfn2vesta examples --id h2o_domain_baseline --verify
multiwfn2vesta examples --command domain-run --json
multiwfn2vesta examples --command local-temperature-ked --json
```

升为 `ready` 前需要一张 domain surface PNG、一张基础 density/ESP 对照图，以及至少一张 KED/KED diagnostics 对照图，并记录 domain criterion、KED cube 范围和等值面。
