# Short trajectory-averaged IGM suite

## 体系价值

- 体系：benzene dimer 短轨迹或 Ag(111)+benzene AIMD 片段。
- 对应功能：`aigm-run`、`amigm-run`、trajectory-average weak interaction、`cube-preset aigm`。
- 为什么值得作为示例：它补齐“轨迹平均弱相互作用”路线，和 Cd/Cl 的结构视频路线互补。
- 不适合说明的问题：不适合作为几何轨迹视频示例；那一类继续用 `cdcl_trajectory_video`。

## 输入文件

| 文件 | 来源 | 是否提交 | 备注 |
| --- | --- | --- | --- |
| `benzene_dimer_traj.xyz` 或其它 Multiwfn 可读轨迹文件 | 短轨迹 | 否 | 每帧需要相同 fragment 定义 |
| `fragments.txt` | 片段定义记录 | 可提交小文本 | 例如两行：`1-12` 和 `13-24`，命令里仍用重复 `--fragment` 传入 |
| `reference.vesta` | 可选相机/style 参考 | 可提交小文件 | 便于和单帧 IGMH 保持一致 |

## 推荐命令

```bash
cd /mnt/g/work/multiwfn2vesta/project
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH

multiwfn2vesta aigm-run benzene_dimer_traj.xyz products/aigm \
  --fragment 1-12 \
  --fragment 13-24

multiwfn2vesta amigm-run benzene_dimer_traj.xyz products/amigm \
  --fragment 1-12 \
  --fragment 13-24

multiwfn2vesta cube-preset aigm products/aigm/benzene_dimer_traj_avgdg_inter.cub products/aigm_vesta \
  --texture-cube products/aigm/benzene_dimer_traj_avgsl2r.cub
```

## 输出文件

| 文件 | 作用 | 是否应提交 |
| --- | --- | --- |
| `products/aigm/*.cub` | trajectory-average IGM cube | 否 |
| `products/aigm_vesta/*.vesta` | VESTA mapped surface | 小文件可选 |
| `products/aigm/*recipe.md` | 参数记录 | 是 |
| `docs/assets/gallery/short_aigm_trajectory_*.png` | 平均弱相互作用效果图 | 是，生成后再加入 |

## 效果图状态

尚无正式 PNG。第一版建议用 benzene dimer 短轨迹，保证计算和图像足够轻；Ag(111)+benzene AIMD 可作为后续高价值周期体系版本。

## 验收条件

```bash
multiwfn2vesta examples --id short_aigm_trajectory --verify
multiwfn2vesta examples --command aigm-run --json
```

升为 `ready` 前需要记录帧数、fragment 定义、平均 cube 范围和至少一张 mapped-surface PNG。
