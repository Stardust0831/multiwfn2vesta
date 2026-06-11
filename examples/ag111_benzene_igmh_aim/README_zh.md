# Ag(111)+benzene IGMH+AIM 三视图 example

这是当前最重要的 ABACUS -> Multiwfn -> VESTA 闭环示例。它展示周期性 Ag(111) 表面吸附苯的
IGMH 弱相互作用等值面、sign(lambda2)rho 染色、AIM 键径和 BCP 叠图。

## 现有证据

- ABACUS LCAO Molden:
  `../../../smoke/abacus_server_artifacts_20260606/ag111_benzene/ag111_benzene_lcao_cont3_nval.molden`
- IGMH cubes:
  `../../../smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/products/dg_inter.cub`
  和 `sl2r.cub`
- 最终三视图:
  `../../../smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_cli_rotate_split_bcp_final_20260609/`
- 手册图:
  `../../docs/assets/gallery/ag111_benzene_igmh_aim_front.png`,
  `../../docs/assets/gallery/ag111_benzene_igmh_aim_right.png`,
  `../../docs/assets/gallery/ag111_benzene_igmh_aim_top.png`

## 命令形态

实际重跑时应从 ABACUS Molden 先生成 IGMH 和 AIM 产物，再用 `aim-igmh` 样式化已保存叠图：

```bash
multiwfn2vesta igmh-run ag111_benzene_lcao_cont3_nval.molden igmh_products \
  --fragment 1-48 \
  --fragment 49-60 \
  --grid-mode spacing \
  --grid-spacing 0.25

multiwfn2vesta aim-run ag111_benzene_lcao_cont3_nval.molden aim_products

multiwfn2vesta aim-igmh input_overlay.vesta three_views \
  --label-bcp-sites \
  --render-three-views \
  --initial-view top \
  --extra-rotate top x -8 \
  --scale 2
```

## 当前质量判断

- 状态: `ready`
- 适合作为主线展示图。
- 已知缺口: 当前三视图留白偏大，下一轮应基于同一 `.vesta` 重渲染更紧凑的 camera/zoom。
- 渲染时 Windows VESTA 仍可能抢焦点；不需要渲染时只生成 `.vesta`。
