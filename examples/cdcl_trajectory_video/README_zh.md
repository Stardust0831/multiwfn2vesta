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
- 项目内 artifact manifest:
  `artifact_manifest.json`

## 查询和验证

仓库内可提交资源检查：

```bash
multiwfn2vesta examples --id cdcl_trajectory_video --verify
```

本机 smoke 证据检查：

```bash
multiwfn2vesta examples --id cdcl_trajectory_video --verify-smoke
```

`--verify-smoke` 会检查 mp4、PNG frame 和 patched VESTA frame 目录是否存在，但这些大文件仍然不进入
Git。若换机器或清理过 `smoke/`，这个检查失败是合理的，重新跑轨迹渲染或恢复 smoke 目录即可。

## 关键经验

- 参考样式来自保存过的 `.vesta`，后续 frame 复用 style、视角、Boundary 和成键判据。
- Cd-Cl 成键判据需要比默认更宽；现有 `cdcl3p50` 版本就是为这个问题保留的。
- VESTA 逐帧渲染时需要及时关闭或复用窗口，否则可能出现保存失败和抢焦点。
- 大 mp4 不提交到仓库，只在 smoke 目录记录；仓库内只保留 poster frame。
- `artifact_manifest.json` 记录项目内 poster/runbook 和工作区 smoke 大文件的对应关系，后续正式
  `trajectory-video` CLI 应复用这个产物契约。

## 当前质量判断

- 状态: `ready`
- 适合作为轨迹视频章节的当前证据。
- 已知缺口: 需要把轨迹读取、VESTA frame 写入、渲染和 ffmpeg 合成整理为一个稳定 CLI；当前已有
  `examples --id cdcl_trajectory_video --verify-smoke` 可验证历史 smoke 证据是否齐全。
