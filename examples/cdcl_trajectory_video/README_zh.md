# Cd/Cl 轨迹视频 example

这个 example 记录 Cd/Cl 轨迹到 VESTA frame、PNG 序列和 mp4 的现有证据。当前已经有维护态
`trajectory-frames` 入口负责“XYZ/extXYZ 轨迹 -> `.vesta` frame”的生成层，也有 `trajectory-video`
入口负责“已渲染 PNG 序列 -> mp4”的合成层；仍待继续收敛的是 ASE `.traj` 直接读取和不抢焦点的
VESTA PNG 渲染层。

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
- 可提交的最小 extXYZ 输入:
  `cdcl_tiny.extxyz`

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

## 生成 VESTA frame dry-run

项目内最小 extXYZ 输入可用于验证 Boundary、Cd-Cl 放宽成键判据和 manifest/recipe 写出：

```bash
multiwfn2vesta trajectory-frames examples/cdcl_trajectory_video/cdcl_tiny.extxyz \
  /tmp/cdcl_vesta_frames \
  --bond Cd Cl 0 3.5 \
  --boundary -0.05 1.05 -0.05 1.05 -0.05 1.05
```

若已经有手动保存好的参考 `.vesta`，例如从 smoke 中挑出的首帧样式，可以额外加：

```bash
--reference-vesta /path/to/nvt_frame_0001_saved.vesta
```

输出目录会包含 `vesta/frame_0001.vesta`、`frame_trajectory_frames_manifest.json`
和 `frame_trajectory_frames_recipe.md`。这一步不启动 VESTA，也不渲染 PNG。

## 合成视频 dry-run

默认只写 frame list 和 recipe，不执行 ffmpeg：

```bash
multiwfn2vesta trajectory-video \
  --manifest examples/cdcl_trajectory_video/artifact_manifest.json \
  --output /tmp/cdcl_trajectory.mp4 \
  --fps 24 \
  --bitrate 20M
```

确认 recipe 后执行：

```bash
multiwfn2vesta trajectory-video \
  --manifest examples/cdcl_trajectory_video/artifact_manifest.json \
  --output ../../../smoke/vesta_trajectory_video_1608/ase_nvt_refstyle_stride20_cdcl3p50/cdcl_trajectory_rebuilt.mp4 \
  --fps 24 \
  --bitrate 20M \
  --run
```

如果目标 mp4 已存在，需要显式加 `--overwrite`。

## 关键经验

- 参考样式来自保存过的 `.vesta`，后续 frame 复用 style、视角、Boundary 和成键判据。
- 对可提交/可测试的最小输入，使用 `cdcl_tiny.extxyz` 和 `trajectory-frames`；对历史 ASE `.traj`
  smoke，当前需要先导出 XYZ/extXYZ，后续再补直接读取。
- Cd-Cl 成键判据需要比默认更宽；现有 `cdcl3p50` 版本就是为这个问题保留的。
- VESTA 逐帧渲染时需要及时关闭或复用窗口，否则可能出现保存失败和抢焦点。
- 大 mp4 不提交到仓库，只在 smoke 目录记录；仓库内只保留 poster frame。
- `artifact_manifest.json` 记录项目内 poster/runbook 和工作区 smoke 大文件的对应关系，`trajectory-video`
  会复用这个产物契约定位 PNG 帧目录。

## 当前质量判断

- 状态: `ready`
- 适合作为轨迹视频章节的当前证据。
- 已维护: XYZ/extXYZ 到 VESTA frame 的 `trajectory-frames`，以及 PNG frame 到 mp4 的
  `trajectory-video`、frame list、recipe 和 manifest dry-run。
- 已知缺口: 还需要把 ASE `.traj` 直接读取、VESTA 渲染 PNG、及时关窗/不抢焦点整理为稳定 CLI。
