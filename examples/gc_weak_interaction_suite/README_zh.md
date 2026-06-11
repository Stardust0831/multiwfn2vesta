# GC base-pair weak-interaction extension

## 体系价值

- 体系：GC 碱基对。
- 对应功能：`aim-run`、`aim-pdb`、`iri-run`、ESP-on-density、surface extrema、on-top pair density。
- 为什么值得作为示例：GC AIM 图已经能展示氢键 BCP，继续在同一体系上补 IRI/ESP/极值点能形成完整弱相互作用教程。
- 不适合说明的问题：不覆盖周期性吸附界面，也不适合做金属 STM 例子。

## 输入文件

| 文件 | 来源 | 是否提交 | 备注 |
| --- | --- | --- | --- |
| `gc.molden` | 可被 Multiwfn 读入的 GC 波函数 | 否 | 需要和 AIM smoke 中结构一致 |
| `paths.pdb` / `CPs.pdb` | Multiwfn AIM 输出 | 否 | 已有 GC AIM 经验 |
| `examples/gc_aim/README_zh.md` | 现有正式 AIM runbook | 是 | 复用视角和 BCP 样式 |

## 推荐命令

```bash
cd /mnt/g/work/multiwfn2vesta/project
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH

multiwfn2vesta aim-run gc.molden products/aim

multiwfn2vesta iri-run gc.molden products/iri \
  --grid-points 120 120 100

multiwfn2vesta grid-run gc.molden products/esp \
  --function esp \
  --surface-cube products/iri/IRI2_surface.cub \
  --tex-physical -0.05 0.05

multiwfn2vesta grid-run gc.molden products/ontop_pair \
  --function on-top-pair-density \
  --pair-correlation-type 3
```

## 输出文件

| 文件 | 作用 | 是否应提交 |
| --- | --- | --- |
| `products/aim/paths.pdb` / `CPs.pdb` | AIM 键径和临界点 | 否 |
| `products/iri/*.cub` | IRI/RDG cube | 否 |
| `products/esp/*.cub` | ESP cube | 否 |
| `products/ontop_pair/userfunc.cub` | on-top pair density cube | 否 |
| `docs/assets/gallery/gc_weak_interaction_suite_*.png` | 扩展效果图 | 是，生成后再加入 |

## 效果图状态

已有 GC AIM 主图：

- `../../docs/assets/gallery/gc_aim_overlay.png`

扩展图尚未生成，状态保持 `needs-work`。正式图应避免重复坐标箭头，并保留 BCP 和关键相互作用区域。

## 验收条件

```bash
multiwfn2vesta examples --id gc_weak_interaction_suite --verify
multiwfn2vesta examples --id gc_aim --verify
multiwfn2vesta examples --command surface-extrema --json
```

升为 `ready` 前需要至少一张 IRI/ESP/extrema/on-top pair density 的项目内 PNG，并在 runbook 中记录与 GC AIM 图的对齐方式。

