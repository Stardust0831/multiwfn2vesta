# GC 碱基对 AIM example

GC 碱基对是当前推荐的分子 AIM 主图示例。它比单个 benzene 更能展示分子间氢键区域的 AIM 路径和
BCP，因此适合中文手册中解释 `paths.pdb` / `CPs.pdb` 到 VESTA 的流程。

## 现有证据

- AIM PDB 和 Multiwfn 输出:
  `../../../smoke/20260605_sob445_more_aim_examples/gc/paths.pdb`,
  `../../../smoke/20260605_sob445_more_aim_examples/gc/CPs.pdb`,
  `../../../smoke/20260605_sob445_more_aim_examples/gc/CPprop.txt`
- VESTA/PNG:
  `../../../smoke/20260605_sob445_more_aim_examples/gc/products/gc_mol_plus_aim_overlay.vesta`,
  `../../../smoke/20260605_sob445_more_aim_examples/gc/products/gc_mol_plus_aim_overlay.png`
- 手册图:
  `../../docs/assets/gallery/gc_aim_overlay.png`

## 命令形态

如果 Multiwfn 已经产生 `paths.pdb` 和 `CPs.pdb`：

```bash
multiwfn2vesta aim-pdb paths.pdb gc_aim_atoms_only.vesta \
  --cps-pdb CPs.pdb \
  --title "GC AIM paths and BCPs"
```

如果从波函数开始：

```bash
multiwfn2vesta aim-run gc.wfn gc_aim_products
```

## 当前质量判断

- 状态: `ready`
- 适合作为 AIM 主例。
- 已知缺口: 当前 PNG 有坐标轴/视角样式噪声；后续可重渲染一版更适合手册的图。
