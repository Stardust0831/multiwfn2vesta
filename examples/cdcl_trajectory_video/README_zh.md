# Cd/Cl 轨迹视频 example

这个 example 记录 ASE trajectory 到 VESTA frame、PNG 序列和 mp4 的现有证据。它目前是“可展示证据”，
但还没有收敛成稳定主 CLI。

## 现有证据

- NVT 高码率视频:
  `../../../smoke/vesta_trajectory_video_1608/ase_nvt_refstyle_stride20_cdcl3p50/ase_nvt_refstyle_stride20_cdcl3p50_hq20m.mp4`
- NVT poster frame:
  `../../../smoke/vesta_trajectory_video_1608/ase_nvt_refstyle_stride20_cdcl3p50/png/frame_0001.png`
- patched VESTA frames:
  `../../../smoke/vesta_trajectory_video_1608/ase_nvt_refstyle_stride20_cdcl3p50/patched/`
- 手册图:
  `../../docs/assets/gallery/cdcl_nvt_trajectory_frame.png`

## 关键经验

- 参考样式来自保存过的 `.vesta`，后续 frame 复用 style、视角、Boundary 和成键判据。
- Cd-Cl 成键判据需要比默认更宽；现有 `cdcl3p50` 版本就是为这个问题保留的。
- VESTA 逐帧渲染时需要及时关闭或复用窗口，否则可能出现保存失败和抢焦点。
- 大 mp4 不提交到仓库，只在 smoke 目录记录；仓库内只保留 poster frame。

## 当前质量判断

- 状态: `ready`
- 适合作为轨迹视频章节的当前证据。
- 已知缺口: 需要把轨迹读取、VESTA frame 写入、渲染和 ffmpeg 合成整理为一个稳定 CLI。
