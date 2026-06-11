# Ag(111)+benzene extended scalar-field suite

## 体系价值

- 体系：Ag(111)+benzene 周期性吸附 slab。
- 对应功能：`abacus-molden`、`molden-check`、`grid-run` 的 ESP、电场、vdW component、steric/SBL、bonding/energy diagnostics，以及后续 `stm-run`。
- 为什么值得作为示例：它已经有 ABACUS LCAO Molden、IGMH+AIM 三视图和周期性 VESTA 经验，是最适合继续补界面标量场的真实体系。
- 不适合说明的问题：不适合作为快速单元测试；ABACUS/Multiwfn 中间文件较大，不应直接提交。

## 输入文件

| 文件 | 来源 | 是否提交 | 备注 |
| --- | --- | --- | --- |
| `ABACUS_Multiwfn.molden` | Ag(111)+benzene ABACUS LCAO 结果，经最新 ABACUS `molden.py` 转换 | 否 | 需要保留 `[Nval]` |
| `density.cub` 或 `dg_inter.cub` | Multiwfn/ABACUS 生成 | 否 | 可作为 mapped surface 的结构/表面参考 |
| `examples/ag111_benzene_igmh_aim/README_zh.md` | 已有正式例 | 是 | 复用相机和三视图经验 |

## 推荐命令

```bash
cd /mnt/g/work/multiwfn2vesta/project
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH

multiwfn2vesta molden-check ABACUS_Multiwfn.molden --abacus

multiwfn2vesta grid-run ABACUS_Multiwfn.molden products/esp \
  --function esp \
  --surface-cube density.cub \
  --tex-physical -0.05 0.05

multiwfn2vesta grid-run ABACUS_Multiwfn.molden products/efield \
  --function electric-field-magnitude \
  --grid-points 120 120 80

multiwfn2vesta grid-run ABACUS_Multiwfn.molden products/vdw_disp \
  --function vdw-dispersion-potential \
  --vdw-probe C

multiwfn2vesta grid-run ABACUS_Multiwfn.molden products/sbl \
  --function sbl-total-potential

multiwfn2vesta grid-run ABACUS_Multiwfn.molden products/bond_metallicity \
  --function dimensionless-bond-metallicity

multiwfn2vesta grid-run ABACUS_Multiwfn.molden products/local_energy \
  --function energy-density-per-electron
```

## 输出文件

| 文件 | 作用 | 是否应提交 |
| --- | --- | --- |
| `products/*/*.cub` | 标量场 cube | 否 |
| `products/bond_metallicity/userfunc.cub` | dimensionless bond metallicity cube | 否 |
| `products/local_energy/userfunc.cub` | local energy density per electron cube | 否 |
| `products/*/*.vesta` | VESTA 场景 | 小文件可选；正式推荐只提交 recipe |
| `products/*/*recipe.md` | 参数和命令记录 | 是 |
| `docs/assets/gallery/ag111_benzene_extended_fields_*.png` | 精选效果图 | 是，生成后再加入 |

## 效果图状态

当前 `ag111_benzene_igmh_aim` 已有三视图效果图：

- `../../docs/assets/gallery/ag111_benzene_igmh_aim_front.png`
- `../../docs/assets/gallery/ag111_benzene_igmh_aim_right.png`
- `../../docs/assets/gallery/ag111_benzene_igmh_aim_top.png`

本扩展例尚缺 ESP/vdW/steric/SBL/bonding-energy diagnostics 的手册级 PNG。生成前保持 `needs-work`。

## 验收条件

```bash
multiwfn2vesta examples --id ag111_benzene_extended_fields --verify
multiwfn2vesta examples --command steric --json
multiwfn2vesta examples --command bond-metallicity --json
multiwfn2vesta examples --command vdw --json
```

正式升为 `ready` 前需要至少一张同相机、同 Boundary 的 scalar-field PNG，并在图注中写明等值面或 `tex-physical` 范围。
