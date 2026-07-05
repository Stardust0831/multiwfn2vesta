# Project Kanban

## Current Request: 2026-07-05 GitHub Prerelease Object Via SSH/GH

- [x] 需求入板: 用户确认本机可 SSH 到 GitHub，要求继续尝试创建 GitHub prerelease；所有操作继续限制在 `/mnt/g/work/multiwfn2vesta` 内。
- [x] Git/SSH 状态: `origin` 使用 `Github:Stardust0831/multiwfn2vesta.git`，SSH 配置此前已确认可通过 `Github` host 认证；tag `v0.1.0-rc.1` 和 main 已推送。
- [ ] GH API 认证: 当前 `gh auth status --hostname github.com` 仍显示未登录；Release 对象需要 GitHub API 认证，SSH key 只能覆盖 git 传输。首次 `gh auth login --web` 得到设备码 `1465-443D`，但等待期间未完成浏览器授权，最终 GitHub 返回 `slow_down`。
- [x] GitHub Actions 旁路: 因本机无 `gh` API token，新增 `.github/workflows/create-rc1-prerelease.yml`，用远端仓库 `GITHUB_TOKEN` 在 push/workflow_dispatch 时创建 prerelease；若 release 已存在则跳过。
- [ ] 创建 prerelease: 推送 workflow 后等待 GitHub Actions 执行；若 Actions 未启用或 `contents: write` 权限受限，则仍需本机 `gh auth login` 或 `GH_TOKEN`。

## Current Request: 2026-07-02 Human-Friendly Tools And Skills Packaging

- [x] 需求入板: 评估当前项目是否足够人类易用，是否应将常用功能打包成 tools，并把 VESTA/Multiwfn/ABACUS 经验沉淀为可触发 skill。
- [x] 现状审计: 已检查 `docs/skills/`、CLI 入口、中文手册和 VESTA 相关文档；当前功能覆盖较多，但 skills 偏维护者 runbook，普通用户仍需要知道很多命令名和 VESTA 内部字段。
- [x] 新需求入板: 用户确认开始实施；目标是把测试过且用户明确认可可用的功能整理成 tools，把项目规范和 VESTA 字段经验提炼成 skill，并补中文/英文 CLI 交互入口。
- [x] 范围收敛: 只把明确跑通过的功能标为 stable tools；未验证或仍有风险的路线保留为 experimental/runbook。
- [x] Tools 实现: 已新增 `multiwfn2vesta tools` 高层命令、`tools run` 转发入口和 `esp-surface` 组合工具，内部复用现有底层 CLI，不重复实现算法。
- [x] Skill/Reference 实现: 已新增项目内 Codex skill `docs/codex_skills/multiwfn2vesta-operator/`，含项目操作规范、稳定 tools、VESTA 字段 reference 和打包规则。
- [x] 双语 UX: `multiwfn2vesta tools --lang zh/en`、`tools interactive --lang zh` 和全局 `--lang zh --help` 已可用；默认英文底层脚本用法保持兼容。
- [x] 验证与同步: 已新增 `tests/test_tools.py` / `tests/test_project_skill.py`，更新 CLI 测试；`unittest tests.test_tools tests.test_project_skill tests.test_cli tests.test_abacus_esp_align tests.test_abacus_lr_to_multiwfn tests.test_cube_preset` 共 139 tests OK；`tools run esp-surface` 和 `tools run excitation-bridge` sample smoke 均通过；scoped diff check 通过。
- [x] 提交/推送: 已提交并推送 `d28622a Add stable tools layer and project skill` 与 `3af9dda Add guided stable tools interaction` 到 GitHub。
- [x] 新需求入板: 将 stable tools 的交互入口升级为类似 Multiwfn 的数字菜单和逐项输入/输出文件提示；完成后发布 prerelease。
- [x] Guided CLI: `multiwfn2vesta tools interactive --lang zh` 支持按编号选择功能，并根据功能逐项询问输入文件、输出目录/文件和常用选项，最后显示参数并确认执行；仍保留手动参数行模式。
- [x] Prerelease tag: 已提交 `db9716d Document v0.1.0 rc1 prerelease`，推送 `main`，并推送 annotated tag `v0.1.0-rc.1` 到 GitHub；release notes 在 `docs/releases/v0.1.0-rc.1.md`。
- [ ] GitHub prerelease object: 本机没有 `gh` CLI，也没有 `GH_TOKEN`/`GITHUB_TOKEN`，无法自动调用 GitHub Release API；需要在 GitHub 网页用 tag `v0.1.0-rc.1` 创建 prerelease，或提供 token 后再自动创建。

## Current Request: 2026-07-02 Excited-State Bridge And ESP VdW Surface Closure

- [x] 需求入板: 补齐 ABACUS LR-TDDFT 激发态转换入口和 ABACUS ESP 范德华表面染色流程，要求给出测试用例、输入输出文件和完整文档。
- [x] 激发态入口审计: 已有 `abacus-lr-to-multiwfn` CLI、console script 和单元测试；补上 example 输入/输出样本和文档后即可闭环。
- [x] ESP 流程审计: 已有 `abacus-esp-align`、COF direct cube 输入和单元测试；补上 example 输入/输出样本、VESTA recipe 和文档后即可闭环。
- [x] 补齐缺口: 已生成 sample LR 输入/输出与 sample ESP 输入/输出，并把 example README 和文档说明接上。
- [x] 验证: `abacus-lr-to-multiwfn` sample、`abacus-esp-align` sample、`cube-preset esp` sample 均可由 CLI 重新生成；`compileall`、`unittest tests.test_abacus_lr_to_multiwfn tests.test_abacus_esp_align tests.test_cli tests.test_cube_preset` 共 132 tests OK；`examples --id cof_direct_cube_suite --verify` 通过。
- [x] 提交前检查: scoped diff check 和 cached diff check 通过；暂存范围仅包含 LR bridge / ESP workflow 闭环相关文件。
- [x] 提交: 已提交 `f34ef60 Close ABACUS LR and ESP workflows`。
- [x] 推送: 已推送到远端 `origin/main`，最新远端提交 `1216034`。

## Current Request: 2026-07-02 VESTA Export Bond Display Fields

- [x] 需求入板: 检查当前 `.vesta` 导出是否包含成键信息，并修正 `SBOND` / 结构 bond 显示字段，让 VESTA 载入后能正确显示结构成键。
- [x] 生成器审计: 已检查 cube/cube-preset 后端、trajectory-frames、AIM/IGMH overlay 等 `.vesta` writer；AIM path/BCP phase 保持空 `SBOND` 是有意避免伪键，结构 phase 需要非空 `SBOND`。
- [x] 参考文件对照: 已与 VESTA 原生保存文件对照，确认 `BONDS   1` 只是显示开关，`SBOND` 规则行还需要 `0  1  1  0  1  radius width RGB` 等字段。
- [x] 实现修复: `cube-vesta` / `cube-preset` 现在按 1-118 号元素 covalent radius 表为结构 phase 自动写默认 `SBOND`；`trajectory-frames --bond` 复用同一 VESTA 兼容格式；`--structure-bonds-off` 写 `BONDS 0` 且保持空 `SBOND`。
- [x] 验证: `unittest tests.test_cube_vesta tests.test_trajectory_frames tests.test_cube_preset` 80 tests OK；`compileall` 和 `git diff --check` 通过；临时 H2O cube 导出含 O-O/O-H/H-H `SBOND`。
- [x] 文档同步: 已同步 usage、中文手册和 cube/ESP VESTA skills。

## Current Request: 2026-06-26 ABACUS Gamma-Only LR-TDDFT To Multiwfn Bridge

- [x] 需求入板: 实际运行一次 ABACUS `gamma_only` 电子激发计算，基于 ABACUS 结果生成 Molden 和激发组态文本，并交给 Multiwfn；重点关注 `Excitation_Energy_*` / `Excitation_Amplitude_*` 到 Multiwfn 主功能 18 plain text 的转换过程。
- [x] 算例准备: 已选 H2O LCAO/Gamma-only smoke；服务器 PP/ORB 位于 `/opt/apps/abacus/abacus-develop-LTSv3.10.1/tests/PP_ORB`。首版 `nbands=28` 因 `NLOCAL < NBANDS` 被 ABACUS 拒绝；已改用 `nbands=20, nocc=4, nvirt=16` 并提交新作业。
- [x] ABACUS 计算: `565015` 显式 `device cpu` 的 H2O LCAO/Gamma-only SCF+LR 已完成，输出 `OUT.abacus_h2o_lr/Excitation_Energy_singlet.dat` 和 `Excitation_Amplitude_singlet_0.dat`；`565005` 的 GPU LR 失败经验保留为 LCAO/GPU `gint_rho_gpu.cu` illegal memory access/segfault 记录。
- [x] Molden 导出: 已用本地最新 `origin/develop` 可用的 `interfaces/Multiwfn_interface/molden.py` 生成 `smoke/abacus_h2o_lr_bridge_20260626/products/ABACUS_Multiwfn.molden`，包含 `[Cell]`/`[Nval]`，`molden-check --abacus` 通过；当前 latest develop 仍未提供 `tools/molden/molden.py` 路径。
- [x] 激发转换: `abacus-lr-to-multiwfn` 已支持从 ABACUS `running*.log` 或 `INPUT`/`INPUT.lr` 自动推断 `nocc/nvirt`，默认将 ABACUS LR 系数乘 `1/sqrt(2)` 以匹配 Multiwfn 闭壳层 TDDFT 归一化；focused tests、CLI help、compileall 和 diff check 已通过。
- [x] Multiwfn 验证: `Multiwfn_noGUI` 已载入 ABACUS Molden，并在主功能 `18 -> 1` 中读入转换后的 `h2o_singlet.excit.txt`；识别 5 个 singlet 态，S1 系数平方和 `0.499713`，到期望 `0.5` 的偏差 `0.000287`。
- [ ] 代码与文档: 将转换经验、命令、测试和必要代码提交到 multiwfn2vesta 项目合适位置，并用 `Stardust0831` 身份 commit/push。

## Current Request: 2026-06-26 Real Excited-State Hole/Electron Case From Sobereva 634

- [x] 需求入板: 参考 `sobereva.com/634` 的周期体系 UV-Vis/电子-空穴对分析思路，跑一个真实 case，目标是从 ABACUS 或可转换输入得到参考波函数和激发组态，再进入 Multiwfn 主功能 18 生成 hole/electron/transition-density 产物。
- [x] 资料抓取: 已保存 Sobereva 634 页面和附件包到 `smoke/sobereva634_excited_state_case_20260626/`。附件含 `bulk.cif`、`bulk_TDDFT.inp/out`、已补晶胞的 `bulk_TDDFT-MOS-1_0.molden`、`hole.cub`、`electron.cub`、`CDD.cub`、`transdens.cub`、`supercell.pdb`。原文重点分析 S13: 1.92496 eV、f=4.13484，是强吸收的电荷转移激发。
- [x] 算例选择: 本轮先复用 Sobereva 634 原文真实 CP2K+Multiwfn 产物闭环可视化和 Multiwfn 电子-空穴分析流程；ABACUS 同结构 LR-TDDFT 作为后续迁移任务，需另行准备 PP/ORB 和验证 ABACUS LR 输出。
- [ ] 计算执行: 在干净目录准备 SCF/LR 输入，运行 ABACUS，收集 `Excitation_Energy_*`、`Excitation_Amplitude_*`、Molden 和日志；必要时在服务器上跑，所有本地记录仍写入工作区。
- [x] CP2K/Multiwfn 真实复现: 本地 `Multiwfn_noGUI` 在设置 `OMP_STACKSIZE=2G`、`KMP_STACKSIZE=2G` 和 `ulimit -s unlimited` 后，可载入原文 `bulk_TDDFT-MOS-1_0.molden` 与 `bulk_TDDFT.out`，进入主功能 18 分析 S13，并复现关键数值：最高涉及 `HOMO+28`、激发能 `1.925 eV`、hole/electron/transition-density 积分等。未设置栈时会在生成密度矩阵阶段 segfault。
- [x] VESTA 可视化: 已用原文附件中同一计算导出的真实 `hole.cub`、`electron.cub`、`CDD.cub`、`transdens.cub` 生成 VESTA 文件；路径位于 `smoke/sobereva634_excited_state_case_20260626/products/*_vesta/`，另生成无 GUI 投影预览 `products/s13_cube_projection_preview.png`。CDD 用 `±0.001`，transition density 用 `±0.0005`。
- [x] 经验沉淀: 已新增 `docs/research/sobereva634_real_excited_state_case_20260626.md` 和 project 镜像，记录体系、S13 结论、Multiwfn 栈设置、VESTA 命令、产物路径和 ABACUS 迁移限制。
- [ ] ABACUS 迁移: 尚未对 192 原子晶体运行 ABACUS LR-TDDFT；后续需要先准备 H/C/N/F PP/ORB、验证 ABACUS LCAO+LR 输出，并用 `abacus-lr-to-multiwfn` 生成 Multiwfn 激发组态文本。

## Current Request: 2026-06-25 ABACUS Molden + Multiwfn Excitation Bridge

- [x] 需求入板: 继续推进 ABACUS + latest Molden + Multiwfn 的电子激发桥接，先把能稳定复用的基态参考波函数导出路径和激发态输入缺口写清楚。
- [x] 路径兼容: `abacus-molden` 现在默认尝试 `tools/molden/molden.py`，并自动回退到 `interfaces/Multiwfn_interface/molden.py`，避免老/新 ABACUS checkout 目录搬家导致导出失败。
- [x] 入口审计: 已重新确认 Multiwfn 主功能 18 需要“参考波函数 + 激发组态文件”，而不是只靠 Molden；ABACUS LR-TDDFT 仍需把 `Excitation_Energy_*` / `Excitation_Amplitude_*` 转成 Multiwfn 可读的 plain text 激发文件。
- [x] 桥接解析器需求细化: 需要把 ABACUS LR-TDDFT `Excitation_Energy_*` / `Excitation_Amplitude_*` 转成 Multiwfn plain text 激发组态文件，让 Multiwfn 主功能 18 能读取 ABACUS 激发信息。
- [x] 桥接解析器: 已新增 `abacus-lr-to-multiwfn`，把 ABACUS `Excitation_Energy_<label>.dat` / `Excitation_Amplitude_<label>_0.dat` 转成 Multiwfn 主功能 18 可读的 plain text 激发组态；第一版支持单 rank、Gamma-only、LCAO、`singlet/triplet` label；多 rank amplitude 默认拒绝，避免缺 BLACS/Parallel_2D 分布映射时误拼。
- [x] 格式验证: 已按 Multiwfn `excittrans.f90` plain-text parser 补齐每个 excited state 后的空行终止符，并按 ABACUS `lr_spectrum.cpp` 的 `iocc * nvirt + ivirt` 规则写 1-based MO pair。focused unit tests、模块 `--help`、统一 CLI `--help` 和 compileall 已通过。
- [x] 文档同步: usage、README、research note、CLI skill、ABACUS analysis skill 和 project/root docs 镜像已记录 `nocc/nvirt` 自动推断/显式覆盖、能量单位、空行规则、多 rank 限制和 Multiwfn 主功能 18 使用方式。
- [x] 真实算例: 已跑通 H2O bridge smoke，导出 `ABACUS_Multiwfn.molden` 和 Multiwfn 可读激发文本；本轮验证到主功能 18 能进入目标激发态，未继续生成 hole/electron cube。

## Current Request: 2026-06-24 COF ESP VdW Surface With LCAO Explicit GPU

- [x] 需求入板: 将之前 VESTA 的 COF ESP 范德华表面染色图改用 ABACUS `basis_type lcao`，并显式写 `device gpu` 重跑；目标仍是电子密度等值面作 vdW surface，静电势 cube 作 texture coloring。
- [x] 现有流程审计: 已核对 `project/examples/cof_direct_cube_suite/`、上次 `smoke/cof_esp_abacus_20260621/` 产物、`abacus-esp-align` / `cube-preset density` 后处理入口；服务器 `/opt/apps/abacus/abacus-develop-LTSv3.10.1/tests/PP_ORB` 有 COF 所需 C/H/N/O PP/ORB。
- [x] 服务器计算: 已在干净目录准备 LCAO/GPU 输入并多次尝试。v3.11.0-beta4 的 `np=8` 在 ELPA/OpenMPI/UCX 路径失败，`np=1` 在 ELPA GPU 路径 segfault/kill；成功路径为 `abacus/LTSv3.10.1-sm70-auto`、显式 `device gpu`、coarse `ecutwfc=35`、`np=8` 作业 `556999`，输出 `SPIN1_CHG.cube` 和 `ElecStaticPot.cube`，密度积分 `233.9994 e` 接近预期 `234 e`。
- [x] 后处理和渲染: 已用 `rho=0.001 a.u.` 电子密度等值面 + 真空归零 ESP texture 生成 VESTA 文件；VESTA CLI/no-focus 导出仅得到 `40x40` 无效 PNG，Linux VESTA 缺 `libGLU.so.1`，因此另生成 cube 数据 top-view 诊断 PNG。主要产物在 `smoke/cof_esp_lcao_gpu_20260624/products/`。
- [x] 追加解释: v3.11.0-beta4 的 `np=1` 失败不是 k 点/pool/MPI rank 拆分问题，而是单 rank 下仍调用 GPU ELPA 对角化库；COF 的 744 维 LCAO 广义本征问题在该 v3.11 GPU/ELPA 组合中触发 `libelpa_openmp.so` 的 segfault/kill。LTS 同输入成功，说明更像 v3.11 构建/ELPA/GPU 求解器路径回归或兼容性问题。
- [x] 追加测试: 完整矩阵 job `559510` 已完成。`cusolver np=1/8` 成功，default reset 为 `cusolver` 且 `np=1/8` 成功，`elpa np=1/8` 成功，`genelpa np=1/8` 失败。因此 v3.11 LCAO/GPU 问题集中在 `genelpa` 路径，不是 cuSolver 或 native `elpa` 普遍坏。
- [x] 并行策略回答: 已总结 Gamma-only 大体系策略。LCAO/GPU default/cusolver 可跑但 Gamma-only 下按 k 点分配无法有效多卡；`ks_solver=elpa` 的 native ELPA 分布式 dense solver 才是 LCAO Gamma-only 多 rank/潜在多 GPU方向。PW/GPU Gamma-only 仍需要 pool 内分布式 FFT/G-space/grid 并行，不能靠 KPAR 解决。
- [ ] 多卡 ELPA 测试: 在 `abacus/v3.11.0-beta4-sm70-avx512` 下用 COF coarse、Gamma-only、LCAO、显式 `device gpu`、`ks_solver=elpa` 申请多张 GPU，测试 `np=2`/`np=8` 的稳定性与日志中 GPU 识别情况。
- [x] 术语修正: 已区分 `ks_solver=genelpa`、`ks_solver=elpa` 与 GPU ELPA 支持。源码中 `genelpa` 走 `DiagoElpa`/`module_genelpa::ELPA_Solver`，未直接设置 `nvidia-gpu`；`elpa` 走 `DiagoElpaNative`，会在 `ELPA_WITH_NVIDIA_GPU_VERSION` 且 `device=gpu` 时设置 `nvidia-gpu` 和 `ELPA_2STAGE_REAL_NVIDIA_GPU`。

## Current Request: 2026-06-24 ABACUS Issue Draft And H2O Reproducer Bundle

- [x] 需求入板: 整理英文 Markdown issue 草稿，并同步中文翻译；把 H2O 相关测试文件整理到单独文件夹，便于一并上传 upstream issue。
- [x] H2O 复现包: 已新建 `issue_assets/abacus_device_auto_kpar_h2o/`，包含显式 GPU、no-device、CPU 对照输入、STRU/KPT、分析脚本、Slurm/README；并打包为 `issue_assets/abacus_device_auto_kpar_h2o.tar.gz`，便于一并上传 issue。
- [x] Issue 文档: 已新增英文 issue draft `docs/research/abacus_device_auto_kpar_issue_draft_en.md` 和中文翻译 `docs/research/abacus_device_auto_kpar_issue_draft_zh.md`，并同步到 `project/docs/research/`。
- [x] Issue 语气补充: 已在中英文 issue 草稿中说明我愿意在维护者商定 input 参数优先级/依赖关系修复策略后，贡献相应 PR。

## Current Request: 2026-06-24 Brief ABACUS Bug Report For Developers

- [x] 需求入板: 长报告过长；需要面向开发者反馈的简洁版，凝练 bug 触发条件、表现、影响范围、根因和修改建议，不堆本地路径。
- [x] 文档撰写: 已新增 `docs/research/abacus_device_auto_kpar_bug_brief_zh.md`，同步到 `project/docs/research/abacus_device_auto_kpar_bug_brief_zh.md`；同时生成 3 页 brief PDF `docs/research/abacus_device_auto_kpar_bug_brief_zh.pdf` 和 project 镜像。该版本面向开发者反馈，去掉本地路径细节，重点凝练触发条件、表现、影响范围、根因和修改建议。

## Current Request: 2026-06-24 ABACUS Device-Auto KPAR Bug Report

- [x] 需求入板: 把当前 `device auto`/PW-GPU/`kpar` bug 的原因整理成中文 Markdown 文档，并附带当前测试用例说明和修改建议；可同步渲染 PDF。
- [x] 文档撰写: 已新增 `docs/research/abacus_device_auto_kpar_bug_zh.md`，并同步到 `project/docs/research/abacus_device_auto_kpar_bug_zh.md`。内容包括摘要、H2O/H2/LTS 测试证据、源码原因、非孤立风险、修改建议、回归测试矩阵和 upstream issue 摘要。
- [x] PDF 渲染: 本机无 `pandoc/weasyprint/wkhtmltopdf`，但可用 PIL + Noto CJK 字体生成图片型 PDF；已输出 `docs/research/abacus_device_auto_kpar_bug_zh.pdf` 和 `project/docs/research/abacus_device_auto_kpar_bug_zh.pdf`，均为 8 页 PDF 1.4。

## Current Request: 2026-06-24 ABACUS Input Dependency Audit Beyond Device

- [x] 需求入板: 判断会被其它参数依赖的 input 是否只有 `basis_type` 和 `device`，以及同类解析顺序错误是否可能影响其它参数。
- [x] 源码审计: 已扫描 `read_input_item_*.cpp` 的 `reset_value`。依赖关系不止 `basis_type/device`：`calculation` 会被 `esolver_type=lr` 改写并被 `symmetry/init_chg/scf_nmax/scf_thr` 等依赖；`basis_type/device` 被 `kpar/ks_solver/scf_thr/scf_thr_type/out_*` 依赖；`kpar` 还依赖 `bndpar`，但 `bndpar` reset 在 `kpar` 之后；`ks_solver` 也可能被后续 reset 得到，影响 `bndpar` 逻辑。
- [x] 结论沉淀: 同类解析顺序错误有可能影响其它参数。当前最明确的风险除 `device auto -> kpar` 外，还有 `kpar` 使用尚未 finalized 的 `bndpar`，以及 `bndpar` 使用尚未 finalized 的 `ks_solver`。建议把 `basis_type/device/calculation/esolver_type/ks_solver/bndpar` 这类会影响并行、solver 和默认阈值的核心参数放进显式 finalize/derived-default 阶段，或至少为 no-device GPU、explicit GPU、bndpar+ks_solver、esolver_type=lr、basis-dependent scf defaults 建回归测试。

## Current Request: 2026-06-24 ABACUS Basis-Type Meaning

- [x] 需求入板: 解释 ABACUS `basis_type` 有哪些选择，以及 `lcao_in_pw` 是什么。
- [x] 结论沉淀: 源码中 `basis_type` 可选值为 `pw`、`lcao`、`lcao_in_pw`；`lcao_in_pw` 表示把局域/数值原子轨道放到平面波框架里展开或求解的混合路线。源码注释说明它用于在平面波基中展开 localized atomic set，scf 流程偏 PW，Wannier/nscf 某些接口又偏 LCAO；当前 GPU 不支持，因此会影响 `device` 解析。

## Current Request: 2026-06-24 Why Basis-Type Before Device Finalize

- [x] 需求入板: 解释为什么 `basis_type` 也需要在 `device` finalize 前先得到规范化值。
- [x] 结论沉淀: `basis_type` 是 `device` finalize 的输入依赖；当前源码中 `get_device_flag(device, basis_type)` 会在 `result=="gpu" && basis_type=="lcao_in_pw"` 时直接拒绝，因此应先确定 canonical basis type，再解析 device。否则可能用还没规范化的 basis 判断 GPU 合法性，产生过早拒绝或错误放行。对当前 bug 的最小修复可只保证 `basis_type` read/default 已完成；更稳的设计是先做轻量 basis canonicalization，再做 device finalization。

## Current Request: 2026-06-24 Robustness Of Pre-Reset Finalize Design

- [x] 需求入板: 评估 pre-reset 是否会变成“人为选取优先 reset 参数”的新脆弱点，并说明如何保证工程化和鲁棒性。
- [x] 设计结论: 不能把 pre-reset 设计成随手挑参数提前 reset 的白名单；应区分 `read raw input -> finalize primitive state -> apply derived defaults/reset -> validate/init`。`finalize primitive state` 只允许无副作用、低成本、其它 reset 会依赖的规范化，例如 `basis_type` 归一和 `device auto -> cpu/gpu` 字符串解析；不允许分配资源或做计算 setup。更完整实现可给 input item 增加 phase/depends_on 并做拓扑排序；最小 PR 可用小型 `finalize_core_input()` 加清晰注释、invariant check 和 no-device/explicit-device 回归测试来锁住行为。

## Current Request: 2026-06-24 Explain Pre-Reset Finalize Stage

- [x] 需求入板: 用工程化语言解释明确的 pre-reset/finalize 阶段在 ABACUS input 读取流程里做什么、为什么比依赖 item 顺序更稳。
- [x] 结论沉淀: pre-reset/finalize 是“把其它 reset 会依赖的基础输入先规范化”的阶段。例如先把 `basis_type` 的简单别名/派生状态归一，再把 `device=auto` 解析成最终 `cpu/gpu` 字符串；它不做重计算、不初始化 GPU、不分配 FFT/波函数，也不做完整物理 setup。后续普通 reset hook 可以稳定读取这些 finalized 基础状态，而不是依赖 item 注册顺序。

## Current Request: 2026-06-24 ABACUS Device-Auto Early Resolution Design

- [x] 需求入板: 判断让 `device auto` 优先解析是否合理、是否存在不能优先解析的 case，并给出最优雅的源码修复方案。
- [x] 源码审计: `device` 最终解析调用 `get_device_flag(device, basis_type)`，只依赖原始 `device`、`basis_type` 和硬件探测；`read_txt_input()` 先读完用户显式给出的所有参数，再进入 reset loop，因此显式 `basis_type` 已经可用，未显式给出时默认 `pw` 也可用。GPU context 初始化仍在 `read_parameters()` 的 bcast 之后，不能提前。
- [x] 设计结论: 让 `device auto` 优先解析是合理的，但应只提前解析字符串，不提前初始化 GPU。最优雅方案是引入一个 pre-reset/finalize-device pass，在通用 reset hook 之前把 `auto/cpu/gpu` 归一化；再让 `kpar` 和其它 reset 逻辑只看最终 device。备选是把 `device` item 移到 `kpar` item 前，但这继续依赖 item 顺序，扩展性较差。还需回归覆盖 no-device GPU allocation、显式 `device gpu`、显式 `device cpu`、无 GPU 环境 `auto->cpu`、`lcao_in_pw` 禁用 GPU、Gamma-only `KPAR>nkstot` 早停，以及 GPU/PW `poolnproc>1` 早停。

## Current Request: 2026-06-24 ABACUS Explicit GPU Vs No-Device Source Audit

- [x] 需求入板: 解释为什么显式写 `device gpu` 和不写 `device` 会影响 ABACUS v3.11.0-beta4 的计算行为；要求从源码里说明 `device` 默认值、输入读取、PW/GPU 自动并行重置和 `nks == 0` 早停差异。
- [x] 源码审计: 已检查本地 `downloads/abacus_latest_molden/abacus-develop/source`。`device` 在 `input_parameter.h` 默认是 `auto`；`read_input.cpp` 先读用户显式给出的 item，再按注册顺序跑所有 item 的 `reset_value`；`read_input_item_system.cpp` 中 `kpar` item 位于 `device` item 之前，且 PW/GPU 自动 `kpar=NPROC/bndpar` 只在当时 `device=="gpu" && basis_type=="pw"` 时触发。
- [x] 结论沉淀: 已更新看板和 ABACUS skill。解释: 显式 `device gpu` 在 `kpar` reset 时已经是 `gpu`，所以 `np=2` 被改成 `KPAR=2`，Gamma-only `nkstot=1` 触发 `nks == 0` 早停；不写 `device` 时 `kpar` reset 看到的是默认 `auto`，不改 `KPAR=1`，随后 `device auto` 才解析成 `gpu`，两个 rank 留在同一个 pool，进入 GPU PW FFT 中 `assert(poolnproc==1)` 所代表的未支持路径，release build 可静默写坏 cube。建议修复方向: 先解析最终 device 再做 kpar reset，另加 `KPAR>nkstot` 与 GPU/PW `poolnproc>1` 的 fail-fast。

## Current Request: 2026-06-24 H2O PW No-Device Probe For ABACUS v3.11 Default Path

- [x] 需求入板: 验证 ABACUS v3.11.0-beta4 的 H2O PW case 在不写 `device gpu` 时的行为；重点回答日志里只显示 `RUNNING WITH DEVICE : CPU` 是否可能仍部分走 GPU，以及 no-device/default 路径是否会复现 H2 的 silent bad cube。
- [x] 本地输入准备: 已在 `smoke/abacus_h2o_pw_gpu_2rank_probe_20260624_inputs/` 添加 `INPUT.nodevice` 和 `run_h2o_nodevice_probe.slurm`；输入保留 PW/Gamma/out_chg/out_pot/H2O 18 A 盒子，只移除 `device` 行；Slurm 仍申请 `--gres=gpu:2` 并分别跑 `np=1`、`np=2`。
- [x] 服务器执行: 已同步 no-device 输入到 `SAI-saiuser01:~/multiwfn2vesta_runs/h2o_pw_gpu_2rank_probe_20260624`，提交作业 `551908` 并拉回结果到 `smoke/abacus_h2o_pw_gpu_2rank_probe_20260624_results/nodevice/`。`np=1` 正常，`chg.cube` 积分 `7.999953955320376 e`，能量 `-460.6065895528702 eV`；`np=2` 静默写坏 cube，积分 `6.434633317900327 e`，最小密度 `-0.015059193886`，能量 `-9.684406411563097 eV`。
- [x] 结论沉淀: 已更新 H2O reproducer README、ABACUS direct cube trust-boundary 技能记录和看板。结论: ABACUS 设备报告要看完整块，第一行 `RUNNING WITH DEVICE : CPU` 后面可能还有 `GPU / Tesla...`；no-device/default 在 GPU allocation 下不是安全 CPU fallback，反而绕过了显式 `device gpu` 的 `nks == 0` 早停，能写出错误 direct cubes。

## Current Request: 2026-06-21 ABACUS ESP Surface Coloring And Periodic Excitation Analysis

- [x] 需求入板: 收集 ABACUS 计算周期体系静电势/Hartree 势的算例，用于 VdW 表面静电势染色图；重点处理势能零点任意性，优先研究真空区平面平均势归零。
- [x] 新需求入板: 展示 ESP 当前效果；同时开始筹备 ABACUS 周期/材料激发态算例，为后续 Multiwfn 空穴-电子分析桥接准备输入、runbook 和预期产物。
- [x] 调研 ABACUS direct cube / Hartree potential / electrostatic potential 输出选项、示例输入、输出文件命名和单位；形成可复用 runbook。结论: 当前 ABACUS develop 源码 `out_pot 2` 输出 electrostatic potential 到 `OUT.{suffix}/potes.cube`，单位 Ry；旧/漂移文档可能写 `pot_es.cube` 或 `ElecStaticPot.cube`；`out_pot 1` 是 total local potential，额外含 XC 等项，不应直接当 ESP。
- [x] 设计并实现 cube 后处理：新增 `multiwfn2vesta abacus-esp-align` / `multiwfn2vesta-abacus-esp-align`，读取 ABACUS 势能 cube，按真空方向做平面平均，选择真空平台归零，并输出 shifted cube/profile/report；后续交给 `cube-preset density --texture-cube` 或 `cube-vesta` 做 VdW/密度表面染色。
- [x] ESP 效果展示: 本地未找到真实 ABACUS `potes.cube/chg.cube`，因此先生成 synthetic slab-like smoke demo，产物位于 `smoke/esp_vacuum_alignment_demo_20260621/`；`esp_demo_summary.png` 展示真空归零前后平面平均曲线和密度表面 ESP 染色代理图，`vesta/synthetic_chg_density_cube.vesta` 可用 VESTA 打开检查 texture workflow。
- [x] 用户纠偏: synthetic ESP demo 只能作为算法 smoke，不能作为科学效果图。真实目标应是 COF/晶体表面或 slab 的 `rho=0.001` 电子密度范德华表面，用 ABACUS direct `out_chg` 电子密度 cube 作 surface，用 `out_pot 2` 的 `potes.cube` 作 electrostatic-potential texture，并按真空平台归零。
- [x] 重新获取或计算真实 ABACUS direct cubes：服务器 `SAI-saiuser01` 上 COF 单层 PW fast job `533630` 已在 `~/multiwfn2vesta_runs/cof_esp_fast_20260621` 收敛，参数 `ecutwfc=35/scf_thr=1e-5`，第 9 电子步 density deviation `5.49334e-06`；已输出真实 `chg.cube` 和 `potes.cube`。严格 job `533613` 因 `scf_thr=1e-7` 在 `~1e-3` 附近振荡已取消并保留日志；preview job `533641` 在 fast 成功后已取消。
- [ ] ESP 单位/等值面修正: 用户确认 `rho=0.001 a.u.` 本身是目标阈值；本轮排查表明主线 `esp_surface_singlephase`、`esp_surface_tuned`、`esp_surface_rawgeom_iso_0.00675` 中的 `chg.cube` 与 raw ABACUS `chg.cube` sha256 完全一致，后处理未改坏 density cube。ABACUS develop 源码文档声称 `out_chg 1` 输出 Bohr^-3，`write_vdata_palgrid` 也不缩放数据；但这份 raw cube 用 ABACUS `cal_rho2ne=sum(rho)*omega/nxyz` 公式积分为 `81.33 e`，不是体系 `234 e`，且约 37% 网格点为负值。进一步逐层统计显示 `rho>=0.001` 只出现在 z=69..113 的 45 个完整平面，每个 `(x,y)` 柱恰好有 45 个点超过阈值；所有原子都在 z=0.5 单层平面，说明片状表面一部分来自二维 COF 本身的横向贯通电子密度，但积分不守恒仍说明该 `out_chg` 文件不能直接作为生产级 vdW density surface。已在服务器新建 `~/multiwfn2vesta_runs/outchg_probe_20260622` 做 H2 最小对照：同一 GPU/PW 输入下 `np=1` 的 `chg.cube` 积分 `1.99998849 e` 正常，而 `np=8` 积分 `0.24513058 e` 且总能量异常；追加 `device cpu` 后 `np=1` 和 `np=8` 均积分 `1.99998849 e`。因此问题归因到当前 ABACUS v3.11.0-beta4 PW/GPU 多 MPI rank 路径，COF 的 8-rank GPU `chg.cube` 不应作为生产级 vdW density surface，需重跑 `device cpu` 或验证单 rank GPU/其它版本。`chg_angstrom_density_eA3_for_vesta.cube` 仍仅保留为反例诊断，不作为主路线。
- [x] 真实 ESP 后处理与效果图: 原始 cube 已拉回 `smoke/cof_esp_abacus_20260621/raw/OUT.cof12000n2_esp_fast/`；`abacus-esp-align` 生成 `products/potes_vacuum0.cube`，真空 offset `4.670271116877 Ry`；`cube-preset density --isosurface 0.001 --texture-cube ...` 生成 VESTA。初始 `-0.06..0.06 Ry` 色标整片偏蓝，按 surface-nearest 范围改为 `--tex-physical -12.8 -1.6` 后得到 tuned 图 `smoke/cof_esp_abacus_20260621/products/cof_esp_surface_tuned.png`，对应 VESTA 文件 `products/esp_surface_tuned/chg_density_cube_nocomps.vesta`。
- [x] COF direct ESP 算例模板: `examples/cof_direct_cube_suite/` 已新增 `INPUT.esp` 和 `STRU`，用于跑 `out_chg 1 8` + `out_pot 2 8`；README 已改成 `rho=0.001` density surface + vacuum-aligned `potes.cube` texture workflow。2026-06-21 修正：默认模板改为 `basis_type pw`，避免 N `.orb` 缺失导致 LCAO direct cube 算例不可跑。
- [x] 服务器运行经验入板: SAI `4V100PX` 分区单 GPU 作业需 `--qos=rush-1o2gpu --gres=gpu:1` 且不要显式写 `--cpus-per-task`；`srun abacus` 会启动多个串行 ABACUS 实例互相覆盖输出，应使用 `mpirun --bind-to none --map-by slot -np 8 abacus`。
- [x] 调研 Sobereva 电子-空穴分析相关文章线索和 Multiwfn 对 CP2K/其它周期激发信息的读取需求；对照 ABACUS 周期激发/TDDFT 输出。当前证据见 `docs/research/abacus_esp_vacuum_alignment_and_excitation_zh.md`。
- [x] 初步评估 `abacus2cp2k` 或更通用 excitation-record 格式：不建议把伪 CP2K 输出作为主路线；短期原型优先 `ABACUS LR-TDDFT + ABACUS Molden -> Multiwfn plain text 激发文件`，适合空穴-电子/NTO/跃迁密度但不含振子强度；正式路线再定义内部 excitation-record 或给 Multiwfn 加 ABACUS 原生 parser。此项仅为设计完成，真实 ABACUS LR-TDDFT parser/周期电子-空穴 cube 尚未跑通，不能标为功能 ready。
- [x] 激发态算例筹备: 新增 `examples/abacus_lr_tddft_excitation_bridge/`，用 H2O Gamma-only 超胞作为 ABACUS LR-TDDFT bridge smoke，包含 `INPUT.scf`、`INPUT.lr`、`STRU`、`KPT` 和中文 runbook；目标是先收集 `Excitation_Energy_*` / `Excitation_Amplitude_*`，再实现 Multiwfn plain text exporter。
- [x] 本轮验证: `tests.test_abacus_esp_align tests.test_cli tests.test_cube_preset` 共 123 tests 通过；`abacus-esp-align --help`、统一 CLI help、最小 cube smoke、`git diff --check` 和 root docs mirror dry-run 通过。未运行真实 ABACUS SCF/LR-TDDFT，也未生成 VESTA 渲染图。

Updated: 2026-06-21 21:36 CST

## Active Goal Continuation: 2026-06-12 Energy-Density Derivative Grid Routes

- [x] 需求入板: 继续长期目标，调研并实现更多 ABACUS LCAO Molden 可支撑、能由 VESTA 表达的 Multiwfn 波函数分析路线；本轮从上次源码审计 P1 候选中选择一个边界清晰的增量。
- [x] 审计当前仓库状态和覆盖: `main` 与 `origin/main` 对齐，工作树干净；`grid-run` / `cube-preset` 已覆盖 bonding/energy diagnostics、信息论、USI/BNI、steric/SBL、KED diagnostics 等路线，尚未维护能量密度梯度/拉普拉斯 `iuserfunc=79/80`。
- [ ] 审计本地 Multiwfn 2026.6.2 源码证据: 确认 function-100 `iuserfunc=79/80` 的物理含义、是否需要额外交互/设置、输出符号性质和适合 VESTA 的默认 preset。
- [ ] 实现 `grid-run` named routes、`cube-preset` presets、tests、README/中文手册/usage/feature/status/research/skill/worklog/kanban 文档；状态先保持 `needs-render`，推荐真实体系为 Ag(111)+benzene、GC、COF 孔边缘或 benzene/phenol dimer。
- [ ] 运行 focused/full no-GUI tests、CLI smokes、docs mirror、markdown/link checks、`git diff --check`；通过后用 `Stardust0831` 身份提交并推送。

## Current Request: 2026-06-12 Feature Closure Phase 9, Functional Examples, UX, Renders, And Chinese Manual

- [x] 需求入板: 把当前已有功能进一步闭环；每个维护态功能都要能从统一 CLI 找到 example、真实有价值体系、runbook、效果图或明确 `needs-render` / `needs-example` 原因；继续优化中文手册和使用体验。继续保护未跟踪 `domain.cub` / `domain.pdb`，不把大型 smoke/cube/mp4 误提交。
- [x] 盘点当前状态: `examples --summary --json` 显示 16 个 curated examples，其中 4 个 ready、11 个 needs-work、1 个 misc；29 条功能覆盖中 7 个 ready、5 个 linked、14 个 needs-render、3 个 needs-example；项目内 gallery PNG 12/12 present。已有真实手册级图仍主要是 Ag(111)+benzene IGMH+AIM、GC/benzene AIM 和 Cd/Cl 轨迹，H2O-HF IRI+AIM 仅作调试证据。
- [x] 补一个更直接的功能闭环报告入口: 已新增 `multiwfn2vesta examples --closure-report` 和 JSON 输出，从 CLI 导出 ready/linked/needs-render/needs-example 的功能清单、推荐体系、runbook、gallery 图和下一步；README、中文手册、usage、feature/status matrix、examples 规划、skill 和 worklog 已同步。
- [x] 准备本轮效果图产物: 已生成 `docs/assets/gallery/feature_closure_ready_map.png`，只复用已提交的 Ag(111)+benzene、GC/benzene AIM 和 Cd/Cl 真实 VESTA 渲染图；不使用 toy/placeholder 图冒充缺失功能，缺图功能继续保持 `needs-render`。
- [x] 吸收子 agent 只读审计: 源码候选增量优先级为偶极矩密度、应力张量派生标量、能量密度梯度/拉普拉斯、方向 KED、局域 virial ratio；这些作为后续扩展候选记录在 `docs/feature_closure_report_zh.md`，不阻塞本轮已有功能闭环。
- [x] 运行 focused/full no-GUI tests、CLI smokes、docs mirror、markdown/link checks、`git diff --check`；通过后用 `Stardust0831` 身份提交并推送。已通过 focused `tests.test_examples tests.test_cli` 89 tests、full 409 no-GUI tests、`examples --closure-report` / `--summary` / `--verify` smokes、ready-map PNG 尺寸检查、56-file markdown local-link check、`git diff --check` 和 docs mirror checksum dry-run；提交/push 结果由最终回复报告。

## Current Request: 2026-06-12 Feature Closure Phase 8, Real Examples, Renders, UX, And Chinese Manual

- [x] 需求入板: 继续把当前已有功能闭环；每个维护态功能都要配可发现 example、推荐真实有价值体系、可复现命令、效果图或明确 `needs-render` 原因，并进一步优化统一 CLI/中文手册体验。
- [x] 盘点当前代码/CLI/examples/docs/gallery 状态，确认哪些功能已有可复用真实图，哪些只有 planned runbook，哪些需要补真实算例或渲染产物。继续保护未跟踪 `domain.cub` / `domain.pdb`。当前真实项目内 PNG 资产 12/12 present；ready 主线仍是 Ag(111)+benzene IGMH+AIM、GC/benzene AIM 和 Cd/Cl 轨迹，H2O-HF IRI+AIM/phenanthrene/NICS 保持调试或杂项定位。
- [x] 选择优先级最高的一批真实体系补闭环：Ag(111)+benzene IGMH+AIM、GC/benzene weak interaction、COF 单层 direct cube、Cd/Cl 轨迹，以及信息论/USI/BNI/steric/KED 等标量场的手册级 examples。新增 `docs/research/valuable_systems_for_examples_zh.md` 记录体系选择依据，避免后续回退到 toy examples。
- [x] 优化用户体验：让 `examples` / 中文手册 / status matrix 更容易按功能找到命令、输入、输出、效果图和缺口；必要时补 CLI 子命令或校验脚本。新增 `multiwfn2vesta examples --summary` 和 JSON 输出，汇总 example/coverage/gallery 状态、ready ids 和下一批优先体系。
- [x] 吸收只读子 agent 审计：当前 ready 渲染仍集中在 Ag(111)+benzene IGMH+AIM、GC/benzene AIM 和 Cd/Cl 轨迹；新增 bonding/local-energy/density-anisotropy diagnostics 需要独立 coverage，不能标成 ready。
- [x] 补 source-backed bonding/energy diagnostics 闭环入口：`grid-run` / `cube-preset` 已新增 `iuserfunc=8/9/10/11/-11/12/13/15/16/17/25/30/31/32/37/115` 路线，`examples --command bond-metallicity`、`--command shape-function`、`--command sci` 可反查到 `needs-render` coverage；README、中文手册、usage、feature/status matrix、planned runbook、skills 和 worklog 已同步。
- [x] 尽可能渲染或复用真实效果图；不能在本轮稳定渲染的功能保持 `needs-render`，不使用 toy/placeholder 图冒充成品。本轮复用并索引已有真实 VESTA PNG，不新增假图；grid-run 标量场、surface-extrema、Fukui/cube-arith、atom coloring、STM、domain、aIGM/amIGM 仍明确待渲染或待真实体系。
- [x] 同步 README、中文手册、feature/status matrix、skills、worklog、看板和根 docs 镜像，运行 no-GUI regression/CLI smokes/docs checks 后用 `Stardust0831` 身份提交推送。当前已完成 bonding/energy diagnostics 代码、focused 165 tests、full 407 no-GUI tests、CLI smokes、`examples --verify`、markdown local-link check、`git diff --check` 和 docs mirror checksum dry-run；最终提交/push 哈希由本轮回复报告。

## Current Request: 2026-06-12 Feature Closure Phase 7, Information-Density Routes, Examples, And Manual

- [x] 需求入板: 继续把当前已有功能闭环；每个维护态功能都要能从统一 CLI 找到 example、推荐真实体系、效果图或明确 `needs-render` 原因，并同步中文手册/skill/worklog。继续保护未跟踪 `domain.cub` / `domain.pdb`。
- [x] 收口当前未提交的 source-backed 信息论/USI/BNI 增量: `grid-run` 和 `cube-preset` 已覆盖 `iuserfunc=49/50/51/52/53/54/55/56/70/100/819/820`，包括 information gain、Shannon/Fisher/Ghosh/Renyi、phase-space Fisher、disequilibrium、USI 和 BNI。
- [x] 补 examples coverage 和 CLI discoverability: 新增 `grid-run --function information-theory` 与 `grid-run --function usi/bni` 两条 coverage；`examples --command information-gain-density`、`--command ghosh-entropy-density`、`--command renyi`、`--command usi`、`--command bni` 可反查 planned examples。
- [x] 同步 README、中文手册、usage、feature/status matrices、research matrix、skills、worklog 和看板；新增路线全部保持 `needs-render`，推荐真实体系为 benzene/phenol dimer、GC 碱基对、COF 单层、H2O baseline 和 Ag(111)+benzene，不添加 toy/placeholder PNG。
- [x] 运行 focused/full no-GUI tests、CLI smokes、`examples --verify`、markdown/link 或 docs checks、`git diff --check` 和 docs 镜像 dry-run；审查前后均已验证，最终通过 focused 224 tests、full 403 no-GUI tests、`grid-run --list-functions`、`cube-preset --list-presets`、`examples --command information-gain-density/second-fisher-information-density/ghosh/renyi/usi/bni --json`、`examples --verify`、markdown local-link check、`git diff --check`。子 agent 只读审查已完成；阻塞点已处理：根目录 `domain.cub`/`domain.pdb` 加入 `.gitignore` 保护，`information-gain-density` 补 Multiwfn `1000 -> 17` promolecular 初始化，`second-fisher-information-density` 拆为 signed preset。待最终状态检查后用 `Stardust0831` 身份提交推送。

## Active Goal Continuation: 2026-06-12 Next ABACUS/Multiwfn VESTA Analysis Increment

- [x] 需求入板: 继续长期目标，调研 Multiwfn 中有价值且可由 VESTA 表达的波函数分析，重点关注 ABACUS LCAO Molden 或 ABACUS direct cube 可支撑的路线；本轮先审计当前覆盖和源码证据，再选择一个可测试、可文档化的功能增量。
- [ ] 审计当前 `grid-run`、`cube-preset`、example coverage、research matrix 和本地 Multiwfn 源码，避免重复实现已有路线。继续保护未跟踪 `domain.cub` / `domain.pdb`。
- [ ] 实现选定路线的代码、测试、README/中文手册/usage/skill/research/worklog/kanban，同步 docs，运行 no-GUI regression，提交并推送。

## Current Request: 2026-06-12 Feature Closure Phase 6, Examples, Renders, And Chinese Manual

- [x] 需求入板: 继续把已有功能闭环，要求每个维护态功能都有真实有价值体系的 example、可复现命令、效果图或明确待渲染原因，并优化统一 CLI/中文手册体验。
- [x] 收口当前未完成的 extended KED diagnostics 增量: 修复 local-temperature 测试失败，确认 `uservar`/`iKEDsel` 只用于源码支撑的路线；提交前 review 发现的 stale global `uservar` 继承风险已修复为维护态 KED 默认 run-local `uservar=0`，并补齐 README、usage、中文手册、skills、research matrix 和 worklog。
- [x] 重新盘点 examples/gallery/status matrix: 只读子 agent 确认 ready 图集中在 Ag(111)+benzene IGMH+AIM、GC/benzene AIM 和 Cd/Cl 轨迹；grid-run/cube/domain/STM/atom-coloring 仍保持 `needs-render` 或 `needs-example`。
- [x] 对已有真实体系优先补效果图索引和可验证 artifact；不能无 GUI 稳定重渲染的项目保留 `needs-render`，不使用 toy/placeholder 图冒充正式效果图。本轮新增 KED diagnostics coverage，但明确无手册级 PNG。
- [x] 修正子 agent 审计发现的 stale runbook 和入口缺口: `domain-run` 改为 cube 输入，`fukui-run` 改为 `--neutral/--anion/--cation`，aIGM/amIGM 改为重复 `--fragment`，并补 `multiwfn2vesta-abacus-mulliken-color` console script。
- [x] 继续收口用户最新要求: 新增可复用 gallery showcase 生成脚本 `scripts/build_gallery_showcase.py`，生成由真实 VESTA PNG 组成的 `docs/assets/gallery/feature_closure_showcase.png`，并接入 `examples --gallery-assets`、中文手册、gallery 和 feature coverage 文档。
- [x] 吸收两个只读子 agent 结果: ready 主线仍是 Ag(111)+benzene、GC/benzene AIM 和 Cd/Cl 轨迹；近期补图优先级固定为 Ag extended fields、benzene/phenol dimer scalar suite、GC weak-interaction suite、COF direct cube suite、Fukui/atom-coloring suite 和 spin coloring suite。
- [x] 运行 no-GUI regression、CLI smokes、docs mirror、提交前检查；用 `Stardust0831` 身份提交并推送，同时保护未跟踪 `domain.cub` / `domain.pdb`。已通过 focused 221 tests、full 400 no-GUI tests、`examples --verify`、`examples --gallery-assets`、`examples --systems --json`、`examples --needs-render`、markdown local-link check、showcase PNG 尺寸检查、py_compile、`git diff --check` 和 docs mirror dry-run；提交/push 结果由最终回复报告。

## Active Goal Continuation: 2026-06-12 Extended KED Diagnostics Increment

- [x] 需求入板: 继续长期目标，调研并实现更多适合 VESTA 的 Multiwfn 波函数分析，优先 ABACUS LCAO Molden 可支撑的路线；本轮选择本地源码已列出的扩展 KED diagnostics。
- [x] 审计当前仓库状态: `main` 与 `origin/main` 对齐在 `02cb480`；仅有未跟踪 `domain.cub` / `domain.pdb`，继续保护，不提交。
- [x] 审计本地 Multiwfn 2026.6.2 源码证据: function-100 `iuserfunc=1201/1202/1203/1204/1210` 分别为 selected KED 与 Weizsacker/Lagrangian KED 的差值、绝对差值、基于 `iKEDsel` 的 local temperature 和 KED potential。`KEDpot` 源码只显式处理 `iKEDsel=3/5/7`，本轮先维护 Thomas-Fermi KED potential。
- [x] 实现 named `grid-run` routes、VESTA presets、focused tests，并同步 README、中文手册、usage、research matrix、skills、worklog、看板。
- [ ] 运行 no-GUI regression、CLI smokes、docs 镜像、提交前检查；通过后用 `Stardust0831` 身份提交并推送。

## Current Request: 2026-06-12 Feature Closure Phase 5 With Valuable Systems

- [x] 需求入板: 把当前已有功能进一步闭环，按功能补可发现 example、真实有价值体系、效果图或明确待渲染状态，并继续优化统一 CLI 使用体验和中文手册。
- [x] 修复当前 on-top pair density 增量留下的 `examples --command on-top-pair --json` 过滤断点，确保新增功能能被统一 examples 入口发现；focused `tests.test_examples` 已覆盖。
- [x] 盘点所有维护态功能的 example/runbook/gallery 状态，优先选择 Ag(111)+benzene、GC 碱基对、benzene dimer、COF_12000N2 单层、Cd/Cl 轨迹等真实体系补闭环，不用 toy placeholder 冒充手册图；子 agent 只读复核确认 ready 图仍限于 Ag/GC/CdCl 主线。
- [x] 补中文手册与 example/status matrix：每个功能至少给出推荐命令、输入来源、代表体系、预期产物、效果图路径或 `needs-render` 原因；新增 8 个 `examples/<example_id>/README_zh.md` planned runbook，并把 coverage 的泛称 example 改成具体 example id。
- [x] 尽量生成或整理真实效果图；无法无 GUI 稳定渲染的项目保留为待渲染，并记录缺口、下一步和可复现实验路径。当前效果图总览仍使用 `docs/assets/gallery/current_feature_overview.png`，由已有真实 VESTA PNG 组成，未启动 VESTA GUI。
- [x] 运行 no-GUI regression、CLI smokes、docs 镜像、提交前检查；通过后用 `Stardust0831` 身份提交并推送。已通过 `py_compile`、396-test full no-GUI regression、`git diff --check`、54-file markdown local-link check、`examples --verify`、planned example/coverage/on-top pair/surface-extrema/gallery CLI smokes、grid-run/cube-preset route smokes，docs mirror checksum dry-run 为空；提交和 push 待最后执行。

## Active Goal Continuation: 2026-06-12 On-Top Pair Density Increment

- [x] 需求入板: 继续长期目标，调研并实现 ABACUS LCAO Molden 可支撑、能由 VESTA 表达的 Multiwfn 波函数分析路线；本轮选择电子对密度相关的 on-top pair density。
- [x] 审计当前仓库状态和候选路线: `main` 与 `origin/main` 对齐在 `4264ef1`；仅有未跟踪 `domain.cub` / `domain.pdb`，继续保护，不提交。源码候选中 `iuserfunc=36` 比扩展 KED 更独立，且无需 reference point。
- [x] 审计本地 Multiwfn 2026.6.2 源码证据: function `100` 的 `case (36)` 注释为 on-top pair density，即 pair density 的 `r1=r2` 情况；源码临时设置 `pairfunctype=12`，同时说明 `paircorrtype` 会影响结果。
- [x] 实现 named `grid-run --function on-top-pair-density` / `ontop-pair-density`，导出 `userfunc.cub`，通过 run-local settings patch `iuserfunc=36` 和 `paircorrtype`，并新增 `cube-preset on-top-pair-density` 单正值显示。已同步 README、中文手册、usage、research matrix、feature/status indices、skills 和 worklog。
- [x] 运行 no-GUI regression、CLI smokes、docs 镜像、提交前检查；通过后用 `Stardust0831` 身份提交并推送。Focused `tests.test_cube_preset tests.test_multiwfn_grid` 已通过 133 tests；本轮完整验证已通过 396-test full no-GUI regression、CLI smokes、`git diff --check`、markdown local-link check 和 docs mirror dry-run；提交和 push 待最后执行。

## Current Request: 2026-06-12 Existing Feature Closure, Valuable Examples, And Chinese Manual

- [x] 需求入板: 继续把当前已有功能闭环成可复用体验；每个维护态功能都要有 example/runbook、代表体系、效果图或明确的待补图状态，并优化统一 CLI 使用体验和中文手册。
- [x] 工作边界: 所有修改限制在 `/mnt/g/work/multiwfn2vesta`；继续保护未跟踪 `domain.cub` / `domain.pdb`，不提交大型 smoke 产物。
- [x] 审计当前 CLI 功能、examples registry、gallery PNG、status matrix 和 smoke 证据，拆出“已闭环 / 可低风险补文档 / 需要真实渲染”的功能清单；子 agent 只读审计确认 canonical commands 共 25 个，ready 主力仍是 Ag(111)+benzene、GC AIM、Cd/Cl 轨迹。
- [x] 为每个维护态功能补 example 索引和中文说明；优先体系记录为 Ag(111)+benzene、GC base pair、benzene dimer、H2O-HF、COF_12000N2 单层、open-shell/磁性体系、Cd/Cl 轨迹，不用 toy 图冒充成品。
- [x] 吸收两个只读子 agent 复核结果，补成下一批正式 example 队列：`ag111_benzene_extended_fields`、`benzene_dimer_scalar_suite`、`gc_weak_interaction_suite`、`cof_direct_cube_suite`、`fukui_dual_reactivity`、`spin_atom_coloring_suite`、`h2o_domain_baseline`、`short_aigm_trajectory`。
- [x] 补一个可验证的用户体验增量：`multiwfn2vesta examples --command` 按功能查 example，`--gallery-assets` 查项目内 PNG，`--systems` 查推荐真体系；README、中文手册、usage、feature/status/gallery、skill 已同步。
- [x] 渲染/刷新效果总览图: `docs/assets/gallery/current_feature_overview.png` 已由已有真实 VESTA PNG 拼成 1800x1478 总览图，未启动 VESTA GUI。
- [x] 运行 no-GUI tests、CLI smokes、markdown link check、docs 镜像；已通过 `py_compile`、focused tests、full 391 tests、CLI smokes、markdown local links、gallery image verification、`examples --verify`、`git diff --check`、docs mirror dry-run。提交前只读 review 发现的 `--command` alias/误匹配和 `examples` coverage 缺失已修复并补回归测试；之后用 `Stardust0831` 身份提交并推送。

## Active Goal Continuation: 2026-06-12 Steric/SBL Scalar Field Increment

- [x] 需求入板: 继续长期目标，调研并实现更多 ABACUS LCAO Molden 可支撑、能由 VESTA 表达的 Multiwfn 波函数分析路线；本轮优先考虑界面吸附/排斥解释有价值的 steric/SBL 标量场。
- [x] 审计当前工作树和远端状态: 本轮开始时 `main` 与 `origin/main` 对齐在 `466d74e`；仅有未跟踪 `domain.cub` / `domain.pdb`，继续保护，不提交。
- [x] 审计本地 Multiwfn 2026.6.2 源码中 function-100 steric/SBL 相关 `iuserfunc`，选择不需要额外交互点、可稳定导出 `userfunc.cub` 的核心子集：`40-43/60-69/-69/110-113`；damped steric `44-47` 暂不维护。
- [x] 实现 named `grid-run` routes、VESTA presets、focused tests，并同步 README、中文手册、usage、research matrix、skills、worklog、看板。新增 grouped presets: `steric-energy-density`, `sbl-energy-density`, `sbl-potential`, `sbl-force-magnitude`, `sbl-charge`。
- [x] 运行 no-GUI regression、CLI smokes、docs 镜像和提交前检查；通过后用 `Stardust0831` 身份提交并推送。验证通过：full no-GUI 393 tests、`git diff --check`、`grid-run --list-functions`、`cube-preset --list-presets`、`examples --verify`、`examples --needs-render`、`examples --command steric --json`、docs mirror dry-run。`grid-run --function steric/sbl` 仍明确标为 `needs-render`，等待 Ag(111)+benzene、benzene dimer 或 GC 碱基对真实手册级渲染，不用 toy/占位图冒充。

## Current Request: 2026-06-12 Feature Closure Phase 4 And RoSE/SEDD Closeout

- [x] 需求入板: 继续把已有功能闭环成可复用体验；每个维护态功能都要有 example/runbook、代表体系、效果图或明确的待补图状态，并继续准备中文手册。所有回复继续包含看板摘要。
- [x] 修复当前未完成的 RoSE/SEDD 增量测试失败: fake-run 使用的测试 cube 已调整为覆盖 `0.5` 等值面，focused `tests.test_cube_preset tests.test_multiwfn_grid` 已通过。
- [x] 完成只读盘点: 子 agent 和主线均确认当前真正可作为手册效果图的项目内 gallery 是 Ag(111)+benzene IGMH+AIM、GC/benzene AIM 和 Cd/Cl 轨迹；H2O-HF IRI+AIM 是调试图，RoSE/SEDD、grid-run 细分函数、surface-extrema、STM、domain、atom coloring 仍缺真实手册级渲染。
- [x] 同步代码索引、README、中文手册、usage、research matrix、skills、worklog 和看板，把 RoSE/SEDD 从候选路线提升为已有 CLI/preset/test 的维护路线，并把代表体系暂定为 benzene dimer 或 GC 碱基对。
- [x] 运行 full no-GUI regression、CLI smokes、markdown link check、docs 镜像，明确不提交 `domain.cub` / `domain.pdb` 和大型 smoke 产物。验证通过：focused 204 tests、full 383 tests、route/preset CLI smoke、examples coverage/needs-render/verify、markdown local links、gallery required PNG、`git diff --check`、docs mirror dry-run。提交和 push 待最后执行。

## Active Goal Continuation: 2026-06-12 Next Source-Backed VESTA Analysis Increment

- [x] 需求入板: 自动续跑长期目标，继续调研 Multiwfn 中有价值且可用 VESTA 表达的波函数分析，优先关注 ABACUS LCAO Molden 或 ABACUS direct cube 可支撑的路线。
- [x] 审计当前仓库状态: `main` 与 `origin/main` 当前对齐在 `52cf577`；本地仅有未跟踪 `domain.cub` / `domain.pdb`，继续保护，不提交。
- [ ] 审计现有研究矩阵、`grid-run`/`cube-preset` 覆盖和本地 Multiwfn 源码，选择一个边界清晰、可测试、能进入 VESTA 的下一个增量。
- [ ] 实现代码、测试、中文/英文文档、skill/worklog/kanban，同步 docs，验证后用 `Stardust0831` 身份提交并推送。

## Current Request: 2026-06-12 Existing Feature Closure With Valuable Examples

- [x] 需求入板: 把当前已有功能进一步闭环；每个维护态功能都要逐步配真实有价值体系、example/runbook、可验证效果图或产物路径，并优化统一 CLI/发现入口和中文手册。
- [x] 审计当前已维护功能、上轮未提交的 ESP component/electric-field route、已有 examples/gallery/smoke 图片和本地大文件；继续保护未跟踪 `domain.cub` / `domain.pdb`，不把大型 smoke 产物误提交。只读子 agent 确认正式 ready 图集中在 Ag(111)+benzene IGMH+AIM、GC AIM 和 Cd/Cl 轨迹，`grid-run`/atom coloring/IRI+AIM/STM/domain/surface-extrema 仍缺手册级图。
- [x] 收口上轮 ESP positive/negative/electric-field 增量的文档和测试，作为本轮“每个功能可发现、可示例化”的基础之一。代码已包含 `positive-esp`、`negative-esp`、`electric-field-magnitude` presets 和 `grid-run` route，文档已同步到 README、usage、manual、skill、research、status matrix、worklog。
- [x] 为当前维护态功能建立中文闭环矩阵：代表体系、命令、输入来源、效果图路径、状态等级、还缺什么；优先补真实有价值体系而不是 toy placeholder。已强化 `docs/example_status_matrix_zh.md` 的正式 example 验收标准，并新增 `examples/_template/README_zh.md`。
- [x] 选择一批最缺口大的功能补 example 和渲染效果图；无法本轮完整渲染的功能明确标为待维护，不假装闭环。Linux VESTA 当前缺 `libGLU.so.1`，本轮不强行启动 GUI 渲染；继续复用已验证 PNG，把 IRI+AIM、grid-run、atom coloring 等标为待补手册级图。
- [x] 优化用户体验入口和中文手册，验证后同步 `/mnt/g/work/multiwfn2vesta/docs/`，用 `Stardust0831` 身份提交并推送。已完成交互默认 examples、`setup.py` console scripts 对齐、中文手册“从零到第一张图”；验证已通过 focused 199-test set、378-test full no-GUI regression、CLI smokes、markdown local-link check、`examples --verify-smoke`、`git diff --check`、setup/pyproject console-script parity；docs 镜像 dry-run 为空。提交和 push 待本轮最后执行。

## Active Goal Continuation: 2026-06-12 Next ABACUS/Multiwfn VESTA Analysis Feature

- [x] 需求入板: 继续长期目标，调研并扩展有价值的 Multiwfn 波函数分析到 VESTA 可视化，优先选择 ABACUS LCAO Molden 或 ABACUS direct cube 可支撑的路线；本轮先审计当前矩阵和源码证据，再做一个可验证增量。
- [x] 审计当前工作区、已实现 `grid-run`/`cube-preset`/examples/manual 状态、未跟踪本地文件和现有分析矩阵；保护 `domain.cub` / `domain.pdb`。
- [x] 读取本地 Multiwfn 源码，选择一个尚未维护且适合 VESTA 的高价值分析路线。选定 function-100 `iuserfunc=101/102/103`：positive ESP、negative ESP 和 electric-field magnitude，可由 ABACUS LCAO Molden 经 Multiwfn 生成 `userfunc.cub`，再由 VESTA 显示为 standalone 等值面或 density-surface texture。
- [x] 实现代码、测试、中文/英文文档、skill/worklog/kanban，同步 docs，验证后用 `Stardust0831` 身份提交推送。实现、文档、验证和 docs 镜像已完成；提交和 push 待本轮最后执行。

## Current Request: 2026-06-12 Feature Closure With Examples, Renders, And Chinese Manual Phase 3

- [x] 需求入板: 把当前已有功能继续闭环成可复用体验；每个维护态功能需要有 example/runbook、代表性体系、可验证产物或效果图路径，并补中文手册与更顺手的 CLI 发现入口。
- [x] 审计上轮未提交的 trajectory frame 代码、已有 examples/gallery/manual/status matrix 和 smoke 渲染产物；保护未跟踪 `domain.cub` / `domain.pdb`，不提交大型本地产物。
- [x] 先补一个可验证的体验闭环增量：XYZ/extXYZ 轨迹直接生成 VESTA frame 文件，作为轨迹视频 workflow 的上游；同步 example、中文手册、状态矩阵和 skill。已实现 `trajectory-frames`、别名、交互入口、console scripts、`cdcl_tiny.extxyz` example、manifest/recipe 记录和 `vesta_trajectory_frames_skill.md`。
- [x] 汇总每个已有功能的代表体系和效果图现状，明确哪些已有图片可作为手册级效果图、哪些仍是待渲染/待维护；验证、镜像 docs、提交并推送。当前已同步 README、中文手册、usage、gallery、status matrix、Cd/Cl runbook、examples registry、artifact manifest 和 worklog；验证已过 focused tests、375-test no-GUI regression、`git diff --check`、markdown local-link check、Cd/Cl tiny extXYZ smoke、`examples --id cdcl_trajectory_video --verify` 和 docs 镜像 dry-run。本次提交推送完成后由最终回复报告 commit。

## Active Goal Continuation: 2026-06-12 Trajectory Frame Generation Increment

- [x] 需求入板: 继续长期目标，上一轮已维护 `trajectory-video` 的 PNG->MP4 合成层；本轮继续补上游轨迹可视化能力，优先把 XYZ/extXYZ 轨迹转成可批处理的 VESTA frame 文件，并与后续 PNG/MP4 工作流衔接。
- [x] 审计当前工作区、VESTA 写入工具、trajectory smoke/runbook 和测试；保护未跟踪 `domain.cub` / `domain.pdb`。
- [x] 实现一个不依赖 ASE/import 库的轨迹 frame 生成增量，支持真实轨迹常见输入，产出 recipe/manifest，避免启动 VESTA。
- [x] 同步 README/中文手册/usage/skill/worklog/kanban，镜像 docs，验证后用 `Stardust0831` 身份提交推送。代码/文档/测试已同步，提交推送完成后由最终回复报告 commit。

## Active Goal Continuation: 2026-06-12 Next Feature Closure Increment

- [x] 需求入板: 继续长期目标，调研并完善 Multiwfn/ABACUS 到 VESTA 的有价值可视化能力；在上一轮 examples artifact verification 后，继续补真实功能闭环，优先考虑 trajectory video 正式 CLI、atom value coloring 真体系图、IRI+AIM 成品图或 ABACUS 支撑的波函数分析路线。
- [x] 审计当前工作区、未提交文件、已有 trajectory/atom-color/IRI/AIM+IGMH 代码和 docs 状态；保护未跟踪 `domain.cub` / `domain.pdb`。当前只看到本轮 `docs/kanban.md` 修改和未跟踪 probe 文件，trajectory video 缺维护态 CLI，atom coloring/IRI+AIM 主要缺真实渲染图。
- [x] 选择本轮最能推进长期目标的可验证增量，避免只做文档表面整理。选定 `trajectory-video`：先维护“已渲染 VESTA PNG 帧 -> 高码率 MP4”的合成层，后续再接 ASE/XYZ -> VESTA/PNG 帧生成。
- [x] 实现代码/文档/测试，镜像 docs，验证后用 `Stardust0831` 身份提交推送。已新增 `src/multiwfn2vesta/trajectory_video.py`、统一 CLI/entry point、tests、README/中文手册/usage/runbook/gallery/status matrix/skill/worklog 更新；`trajectory-video` 已维护 PNG->MP4 合成层，上游轨迹->VESTA/PNG 帧渲染仍待做。验证通过：focused `py_compile`、`tests.test_trajectory_video tests.test_cli tests.test_examples`、Cd/Cl manifest dry-run、`bin/multiwfn2vesta --help`、365-test full no-GUI regression、`git diff --check`、markdown local-link check、`examples --id cdcl_trajectory_video --verify` 和 `--verify-smoke`。docs 镜像 dry-run 为空；功能提交 `9ae57cb`，最终看板同步提交和 push 由本轮回复报告。

## Current Request: 2026-06-12 Feature Closure Phase 2

- [x] 需求入板: 在已有 examples/gallery/manual 基础上继续闭环，把每个已有功能尽量配套真实有价值体系、example/runbook、效果图和中文手册入口，并优化用户发现与使用体验。
- [x] 审计当前 CLI、examples registry、runbook、gallery 和 smoke 渲染产物；保护未跟踪 `domain.cub` / `domain.pdb`，不把大型 smoke 产物误提交。子 agent 只读审计确认最高缺口是 trajectory video CLI、atom coloring 真体系图、IRI+AIM 成品图；AIM+IGMH 和 AIM 已基本闭环。
- [x] 选择本轮低风险增量，优先补“已有效果图但缺正式入口/验证”的功能；轨迹视频、AIM+IGMH、AIM、IRI、atom value coloring、VESTA three-views 都在矩阵中有明确状态。本轮选择 Cd/Cl 轨迹视频 artifact manifest + `examples --id` + `examples --verify-smoke`，避免把大型 smoke 产物提交进 Git。
- [x] 实现代码/文档/测试，镜像 docs，验证后用 `Stardust0831` 身份提交推送。已实现 `examples --id`、`--verify-smoke`、可选 example `manifest` 字段和 `examples/cdcl_trajectory_video/artifact_manifest.json`；README、中文手册、usage、gallery、状态矩阵、runbook、skill、worklog 已同步。验证通过：focused `py_compile`、`tests.test_examples`、`tests.test_cli`、`examples --id cdcl_trajectory_video --verify`、`examples --id cdcl_trajectory_video --verify-smoke`（检查 4 个本地 smoke 证据路径）、356-test full no-GUI regression、`git diff --check`、`bin/multiwfn2vesta --help`、markdown local-link check。docs 镜像 dry-run 为空；已提交并推送到 `origin/main`，最终提交信息由本轮回复报告。

## Active Goal Continuation: 2026-06-12 Trajectory Video Workflow Closure

- [x] 需求入板: 继续长期目标，把已有 Cd/Cl 轨迹 smoke 经验向正式可维护 workflow 收敛，优先审计已有脚本、VESTA frame/style 复用、Boundary/bond 参数和视频产物记录。
- [x] 审计当前工作区状态、trajectory 相关脚本/烟测/文档和测试覆盖，保护未跟踪 `domain.cub` / `domain.pdb`。
- [x] 选择一个低风险增量：先做可验证的 trajectory example manifest/validator 和中文 runbook 补强；正式轨迹视频 CLI 留给下一轮。
- [x] 实现代码/文档/测试，重新镜像 docs，验证后用 `Stardust0831` 身份提交推送。当前实现已完成，验证已通过；docs 镜像 dry-run 为空，提交推送完成。

## Active Goal Continuation: 2026-06-12 Formal Examples And CLI Discovery

- [x] 需求入板: 继续长期目标，在已有中文手册和 gallery 的基础上，把真实体系 examples 进一步正式化，并优化用户从 CLI 找到这些 examples/状态矩阵的体验。
- [x] 审计当前工作区、CLI、tests 和已新增中文文档，保护未跟踪 `domain.cub` / `domain.pdb`。
- [x] 设计一个轻量 examples 发现入口和正式 examples runbook 结构，优先覆盖 Ag(111)+benzene IGMH+AIM、GC AIM、Cd/Cl 轨迹视频。
- [x] 实现代码/文档/测试，重新镜像 docs，验证后用 `Stardust0831` 身份提交推送。已新增 `multiwfn2vesta examples`、`multiwfn2vesta-examples`、三个正式 runbook 和对应测试。验证通过：focused `py_compile`、focused `tests.test_examples tests.test_cli`、350-test no-GUI regression、markdown local-link check、`git diff --check`、`bin/multiwfn2vesta --help`、`bin/multiwfn2vesta examples --verify`、ready 文本列表和 needs-work JSON 列表。提交和推送仍在本轮最后执行。

## Current Request: 2026-06-12 Close Existing Features With Examples, Renders, And Chinese Manual

- [x] 需求入板: 把当前已有功能进一步闭环，准备有价值的真实体系算例，优化使用体验，准备中文手册；每个功能都要逐步配 example 和效果图。
- [x] 审计当前功能、已有 smoke/example/render 产物和可复用体系，避免重新造一套割裂流程。首批可复用真实图包括 Ag(111)+benzene IGMH+AIM 三视图、benzene/phenanthrene AIM、H2O-HF IRI+AIM、Cd/Cl 轨迹帧和 benzene NICS vector 杂项。
- [x] 设计中文手册与 example gallery 结构，给功能组指定代表体系、输入来源、命令、预期产物和渲染策略；已新增 `docs/manual_zh.md`、`docs/example_gallery_zh.md` 和 `docs/example_status_matrix_zh.md`。
- [x] 先落地一批高价值、可验证的闭环 examples 和渲染图；代表 PNG 已复制到 `docs/assets/gallery/`。不能当场完整渲染的功能在状态矩阵中标为 `有 VESTA/cube` 或 `有入口`，不假装已闭环。
- [x] 根据子 agent 只读审计修正示例质量判断：AIM 主图优先 `gc` 而非 phenanthrene；H2O/H2O-HF IRI+AIM 当前图只作为待完善/调试图，不标为手册级闭环；轨迹视频优先记录 NVT 高码率 mp4；Mulliken coloring 和 NICS arrows 只作为已打通/杂项。已新增 `examples/README_zh.md` 作为 smoke 正式化规划。
- [x] 优化统一 CLI/文档使用体验，补充 README 链接后验证、镜像 docs、提交推送。审计修正后已重跑并通过：markdown 本地链接检查、PNG file 检查、`git diff --check`、`bin/multiwfn2vesta --help`、`cube-preset --list-presets` 和 `grid-run --list-functions`；docs 镜像 dry-run 为空。提交和推送仍在本轮最后执行。

## Active Goal Continuation: 2026-06-12 Multiwfn/VESTA Analysis Route Expansion

- [x] 需求入板: 继续长期目标，调研并实现更多有价值的 Multiwfn 波函数分析到 VESTA 的可视化路线，优先关注 ABACUS LCAO Molden 或 ABACUS cube 能支撑的工作流。
- [x] 审计当前仓库、分支、README/docs 和已实现 `grid-run`/`cube-preset` 覆盖，保护未跟踪本地探针文件。
- [ ] 读取本地 Multiwfn 源码，选择一个边界清晰、对 VESTA 可视化有价值的下一增量。当前被用户新需求降级，优先闭环已有功能的 examples、效果图和中文手册。
- [ ] 实现代码、测试和文档，镜像 docs，验证后用 `Stardust0831` 身份提交并推送。

## Current Request: 2026-06-11 README Refresh And Main-Only Branch Closeout

- [x] Record the new user request immediately: refresh README, inspect the
  unusual-looking branch state, merge back to one maintained branch if needed,
  and use identity `Stardust0831`.
- [x] Recheck branch topology and identity before staging.  `git fetch
  --prune origin`, `git branch --all --verbose --no-abbrev`, and
  `git ls-remote --heads origin` show only local `main`, `origin/main`, and
  `origin/HEAD -> origin/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.  No real merge-back is needed.
- [x] Refresh README with the current branch snapshot, supported global CLI
  entry point, and latest vdW component-route validation summary.
- [x] Run documentation-focused validation: `git diff --check` passed,
  `bin/multiwfn2vesta --help` displayed the unified CLI, and branch recheck
  still showed only `main`, `origin/main`, and `origin/HEAD -> origin/main`.
  Mirror docs to the workspace docs folder, explicitly stage only maintained
  files, commit, push, and verify final `main`/`origin/main` alignment.
  Preserve untracked `domain.cub` and `domain.pdb`.

## Active Goal Continuation: 2026-06-11 Next ABACUS/Multiwfn VESTA Analysis Route

- 2026-06-11 继续项：自动续跑长期目标，继续调研并实现适合 VESTA 可视化的 Multiwfn 波函数分析，优先选择 ABACUS LCAO Molden 或 ABACUS cube 能支撑的路线；本轮先审计现有矩阵和源码，再做一个边界清晰的功能增量。
- [x] Record continuation immediately in the kanban before other work.
- [ ] Recheck repository state, current README/docs/analysis matrix, current `grid-run`/`cube-preset` route coverage, and local Multiwfn source evidence.  Preserve untracked `domain.cub` and `domain.pdb`.
- [ ] Select the next source-backed visualization route or control, implement focused code/tests/docs, mirror root docs, validate, commit, push, and verify branch state.

## Active Goal Continuation: 2026-06-11 Next ABACUS/Multiwfn VESTA Analysis Survey Increment
- 2026-06-11 继续项：收到 README 更新、分支归并检查、Git 身份统一为 Stardust0831 的需求；本轮先补 README/文档，再验证并合并回 main。
- 2026-06-11 子 agent 审查结果：无阻塞问题；建议提交前可选补强 `resolve_grid_function("100")` 回归断言，并在文档说明负值 single preset 改色仍使用 single-surface 的正色参数。

- [x] Record automatic continuation of the long-running objective: continue surveying and implementing valuable Multiwfn wavefunction analyses that can be visualized in VESTA, with priority for routes fed by ABACUS LCAO Molden files or direct ABACUS cube outputs.
- [x] Recheck current repository state, pushed branch alignment, existing analysis matrix, current `grid-run`/`cube-preset` coverage, and local Multiwfn source before selecting the next bounded source-backed increment.  Preserve untracked `domain.cub` and `domain.pdb`.  Current branch is `main` tracking `origin/main`; repository-local identity is `Stardust0831 <13862180016@163.com>`.  Selected increment: UFF vdW repulsion/dispersion component routes backed by local Multiwfn `iuserfunc=93/94` and `ivdwprobe`.
- [ ] Implement one additional valuable route or visualization control with focused tests, README/usage/skill/research/worklog/kanban notes, root-doc mirror, validation, commit, push, and branch verification.  Code/tests/docs now cover `grid-run --function repul` / `disp`, `cube-preset vdw-repulsion-potential` / `vdw-dispersion-potential`, run-local `iuserfunc=93/94`, run-local `ivdwprobe`, and preservation of generic `--function-index 100` behavior.  Subagent review found no blockers; its optional suggestions were handled by adding `resolve_grid_function("100")` coverage and documenting that the negative dispersion single-surface preset still uses `--positive-rgb` for color overrides.  Final validation passed: `py_compile`, 179 focused `tests.test_cube_preset tests.test_multiwfn_grid tests.test_cli` tests, 344 full no-GUI tests, CLI smokes, and `git diff --check`.  `git fetch --prune origin`, `git branch -a`, and `git ls-remote --heads origin` still show only `main`, `origin/main`, and `origin/HEAD -> origin/main`; no merge-back is needed.  Root-doc mirror checksum dry-run is empty.  Commit, push, and post-push verification are still pending.

## Current Request: 2026-06-11 README Refresh And Branch Consolidation For KED Routes

- [x] Record user request immediately: update README, resolve the unusual branch state back to one maintained branch if needed, and use repository-local Git identity `Stardust0831`.
- [x] Finish the selected kinetic-energy-density route increment already in progress: code, tests, README, usage docs, skill notes, research matrix, worklog, root-doc mirror, validation, commit, push, and branch verification.  Code/docs/tests are implemented; read-only subagent review found no blocking issue and low-priority wording refinements around `iKEDsel`/KED sign wording were handled.  Validation passed: `py_compile`, 122 focused `tests.test_cube_preset tests.test_multiwfn_grid` tests, 128 focused `tests.test_multiwfn_grid tests.test_cli` tests, 340 full no-GUI tests, CLI smokes, and `git diff --check`.  Root-doc mirror checksum dry-run is expected to be empty after this final kanban update; final commit hash, push result, and post-push branch verification are reported in the assistant response.
- [x] Confirm remote/local branch topology before commit; `git fetch --prune origin`, `git branch -a`, and `git ls-remote --heads origin` show only `main`, `origin/main`, and `origin/HEAD -> origin/main`, so no real merge-back is needed.

## Active Goal Continuation: 2026-06-11 Next Multiwfn/VESTA Wavefunction Analysis Increment

- [x] Record automatic continuation of the long-running objective: survey and implement valuable Multiwfn wavefunction analyses that can be visualized in VESTA, prioritizing routes fed by ABACUS LCAO Molden files or direct ABACUS cube outputs.
- [x] Recheck current repository state, existing analysis matrix, local Multiwfn source coverage, and remote branch state before selecting the next bounded source-backed increment. Current `main`, `origin/main`, and `origin/HEAD` are aligned at `374955f1e7ea5814c66a898224d87d0bb6b40ea7`; only this kanban update plus untracked `domain.cub` and `domain.pdb` are present. Selected increment: selected kinetic-energy-density function-100 routes backed by local Multiwfn `iuserfunc=1200` plus `iKEDsel`, and Pauli KED backed by `iuserfunc=114`.
- [x] Implement named `grid-run` routes for Weizsacker KED, Thomas-Fermi KED, and Pauli KED with focused tests, README/usage/skill/research/worklog/kanban notes, root-docs mirror, validation, commit, push, and branch verification.  The route mappings are `weizsacker-ked=iuserfunc=1200+iKEDsel=4`, `thomas-fermi-ked=iuserfunc=1200+iKEDsel=3`, and `pauli-ked=iuserfunc=114+iKEDsel=2`; each exports `userfunc.cub`, uses standalone `kinetic-energy-density`, and uses `surface-map` with `--surface-cube`.  Final commit/push details are reported in the assistant response.

## Current Request: 2026-06-11 README Refresh And One-Branch Closeout For FOD Route

- [x] Record user request immediately: update README, inspect the unusual
  branch state, converge back to one maintained branch if needed, and keep
  repository-local Git identity as `Stardust0831`.
- [x] Confirm local branch and identity before staging anything.  Current
  branch is `main`, tracking `origin/main`; remote tracking refs expose
  `origin/HEAD -> origin/main` and `origin/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.  Current uncommitted work is the
  function-100 fractional occupation density increment plus docs; local
  untracked `domain.cub` and `domain.pdb` must stay uncommitted.
- [x] Finish README/docs/tests/review for the FOD route, mirror root docs,
  fetch/prune and confirm whether any real merge-back is needed, then
  commit/push to the maintained branch.  Code/tests/docs now include the
  extra alias `fractional-occupancy-density`, standalone and mapped-surface
  fake-run coverage, and the caveat that FOD may need a lower standalone
  isosurface such as `--isosurface 0.001`.  Validation passed:
  `py_compile`, 74 focused `tests.test_multiwfn_grid` tests, 127 focused
  `tests.test_multiwfn_grid tests.test_cli` tests, 338 full no-GUI tests, and
  CLI smokes; `git diff --check` passed.  `git fetch --prune origin` found
  only `main`, `origin/main`, and `origin/HEAD -> origin/main`; no real
  merge-back is needed.  Root-docs mirror checksum dry-run is empty.  Final
  commit hash, push result, and post-push branch verification are reported in
  the assistant response.

## Active Goal Continuation: 2026-06-11 Next Function-100 Wavefunction Analysis Route

- [x] Record automatic continuation of the long-running objective: keep
  surveying valuable Multiwfn wavefunction analyses that can be visualized in
  VESTA, prioritizing ABACUS-compatible LCAO Molden or direct cube routes.
- [x] Recheck current repository state after the spin-channel density commit,
  preserve local untracked `domain.cub` and `domain.pdb`, and select the next
  bounded source-backed Multiwfn/VESTA increment.  Current `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `b565f4d4fe3dc021ad3dd3c744f1a0fbdffa431c`; only this kanban update plus
  untracked `domain.cub` and `domain.pdb` were present.  Selected increment:
  function-100 fractional occupation density FOD (`iuserfunc=90`), which local
  Multiwfn evaluates via `FODfunc(x,y,z)` and exports as `userfunc.cub`.
- [x] Implement the selected route with focused tests, README/usage/skill/
  research/worklog/kanban notes, root-docs mirror, validation, commit, push,
  and branch verification.  Code/tests/docs now include
  `grid-run --function fractional-occupation-density` / `fod` /
  `fractional-occupancy-density`, standalone `density` preset, mapped
  `surface-map`, and caveats for integer occupations, ABACUS Molden
  occupation export, metallic smearing, multi-k, SOC/noncollinear
  interpretation, and lowered FOD isosurfaces when needed.  Validation passed:
  `py_compile`, 74 focused `tests.test_multiwfn_grid` tests, 127 focused
  `tests.test_multiwfn_grid tests.test_cli` tests, 338 full no-GUI tests, and
  CLI smokes; `git diff --check` passed.  Root-docs mirror checksum dry-run is
  empty.  Final commit hash, push result, and branch verification are reported
  in the assistant response.

## Active Goal Continuation: 2026-06-11 Next ABACUS/Multiwfn VESTA Analysis Route

- [x] Record automatic continuation of the long-running objective: keep
  surveying valuable Multiwfn wavefunction analyses that can be visualized in
  VESTA, prioritizing routes that ABACUS can feed through current LCAO Molden
  files or direct cube outputs.
- [x] Recheck current repository state, pushed branch alignment, existing
  `grid-run`/`cube-preset`/analysis-matrix coverage, and local Multiwfn source
  before selecting the next bounded source-backed increment.  Current `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `c43d37ca0486be07ae8502256d0eaa5846fba615`; only this kanban update plus
  local untracked `domain.cub` and `domain.pdb` were present before the new
  increment.  Selected increment: function-100 alpha/beta density routes
  from local Multiwfn `iuserfunc=1/2`, which call
  `fspindens(x,y,z,'a'/'b')` and export `userfunc.cub`.
- [x] Implement one additional valuable route or visualization control with
  focused tests, README/usage/skill/research/worklog/kanban notes, root-docs
  mirror, validation, commit, push, and branch verification while preserving
  untracked `domain.cub` and `domain.pdb`.  Code/tests/docs now include
  `grid-run --function alpha-density` and `beta-density`, aliases
  `rho-alpha`/`alpha-rho`/`rho-beta`/`beta-rho`, standalone `density` preset,
  mapped `surface-map`, and caveats for closed-shell, EDF/ECP, and ABACUS
  `nspin=2` Molden usage.  Read-only subagent review supported the route and
  flagged alias/caveat refinements that were handled.  Validation passed:
  `py_compile`, 72 focused `tests.test_multiwfn_grid` tests, 125 focused
  `tests.test_multiwfn_grid tests.test_cli` tests, 336 full no-GUI tests,
  CLI smokes, and `git diff --check`.  Final root-docs mirror, commit hash,
  push result, and branch verification are reported in the assistant response.

## Current Request: 2026-06-11 README Refresh And Branch Closeout For Orbital-Weighted Fukui Routes

- [x] Record user request immediately: update README, inspect the unusual
  branch state, converge back to one maintained branch if needed, and keep
  repository-local Git identity as `Stardust0831`.
- [x] Confirm local branch and identity before staging anything.  Current
  branch is `main`, tracking `origin/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.  Current uncommitted work is the
  orbital-weighted Fukui/dual descriptor increment plus docs; local untracked
  `domain.cub` and `domain.pdb` must stay uncommitted.
- [x] Finish README/docs/tests/review for the orbital-weighted
  Fukui+/Fukui-/Fukui0/dual-descriptor route, mirror root docs, fetch/prune
  and confirm whether any real merge-back is needed, then commit/push to the
  maintained branch.  Code/tests/README/usage/skills/research/worklog now
  cover function-100 `iuserfunc=95/96/97/98`, aliases including `ow-dd`,
  standalone `density`/`signed` presets, mapped `surface-map`, and the
  source caveat that `orbwei_delta=0.1` a.u. remains a Multiwfn default.
  Validation passed: `py_compile`, 70 focused `tests.test_multiwfn_grid`
  tests, 123 focused `tests.test_multiwfn_grid tests.test_cli` tests, 334
  full no-GUI tests, CLI smokes, and `git diff --check`.  `git fetch --prune
  origin` still shows only the maintained `main` branch, so no merge-back is
  needed before committing.  Root docs checksum mirror dry-run is empty.
  Final commit hash, push result, and post-push branch verification are
  reported in the assistant response.

## Active Goal Continuation: 2026-06-11 Next ABACUS/Multiwfn VESTA Analysis Increment

- [x] Record automatic continuation of the long-running objective: keep
  surveying valuable Multiwfn wavefunction analyses that can be visualized in
  VESTA, prioritizing routes that ABACUS can feed through LCAO Molden files or
  direct cube outputs.
- [x] Recheck current repository state, existing analysis matrix, and local
  Multiwfn source/templates before selecting the next bounded increment.
  Current `main` is aligned with `origin/main`; only this kanban update plus
  untracked `domain.cub` and `domain.pdb` are present.  Selected increment:
  named orbital-weighted Fukui+/Fukui-/Fukui0/dual-descriptor routes from
  Multiwfn function `100` `iuserfunc=95/96/97/98`.
- [x] Implement one source-backed improvement that materially broadens the
  maintained ABACUS/Multiwfn/VESTA workflow, with focused tests and synced
  README/usage/skill/worklog/kanban notes.  Source evidence: local Multiwfn
  `function.f90` maps cases `95..98` to `orbwei_Fukui(1..4)` and exports
  function `100` as `userfunc.cub`; `define.f90` defaults `orbwei_delta` to
  `0.1` a.u.  Implementation/docs are now staged for validation: four named
  routes, short aliases, standalone and mapped presets, and focused resolver,
  command-stream, standalone, and mapped-surface tests are present.  Read-only
  subagent review confirmed the route and caveats, and validation passed.
- [x] Mirror root docs, commit, push, and verify `main` alignment while
  preserving untracked `domain.cub` and `domain.pdb`.  Root docs checksum
  mirror dry-run is empty; final commit hash and post-push branch verification
  are reported in the assistant response.

## Active Goal Continuation: 2026-06-11 Next ABACUS/Molden Visualization Increment

- [x] Record automatic continuation of the long-running objective: survey and
  implement valuable Multiwfn wavefunction analyses that can be visualized in
  VESTA, prioritizing analyses ABACUS can feed through LCAO Molden files or
  direct cube outputs.
- [x] Recheck current repository state, existing grid/preset coverage, and
  local Multiwfn source/templates before selecting the next bounded increment.
  Current branch is `main` aligned with `origin/main` after the DORI commit;
  only `docs/kanban.md` plus local untracked `domain.cub` and `domain.pdb`
  were present before this increment.  Source review found that
  function-100 `iuserfunc=28` is local Mulliken electronegativity and
  `iuserfunc=29` is local hardness, both exported as `userfunc.cub`; bundled
  examples provide generic `molsurfmap.vmd` but no dedicated color scale.
- [ ] Select and implement one source-backed route that moves the project
  closer to broad Multiwfn-to-VESTA coverage.  Selected increment:
  `grid-run --surface-cube` mapped texture controls plus named local
  reactivity routes.  Implementation now adds `local-mulliken-
  electronegativity` and `local-hardness` (`iuserfunc=28/29`), forwards
  `--tex-physical`, `--tex-percent`, `--tex-range-source`, `--surface-band`,
  and `--surface-nearest` from `grid-run` to `cube-preset`, records these
  controls in recipes, and exposes them in the interactive CLI.  Focused
  validation passed with `tests.test_multiwfn_grid tests.test_cli` (121
  tests), full no-GUI validation passed with 332 tests, CLI smokes and
  `git diff --check` passed, read-only subagent review found no blocker, and
  root docs are queued for a final checksum mirror.  Remaining: commit, push,
  and verify branch alignment while preserving untracked `domain.cub` and
  `domain.pdb`.

## Current Request: 2026-06-11 README Refresh And One-Branch Closeout For Local Reactivity Route

- [x] Record user request immediately: update README, inspect the unusual
  branch state, converge back to one maintained branch if needed, and keep
  repository-local Git identity as `Stardust0831`.
- [x] Confirm branch topology and identity before staging.  Current branch is
  `main`; upstream is `origin/main`; `origin/HEAD` points to `origin/main`;
  after `git fetch --prune origin`, `git ls-remote --heads origin` exposes
  only `refs/heads/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.  There is no feature branch that
  needs a real merge-back right now.
- [x] Finish the in-progress local reactivity / mapped texture route on
  `main`: README/usage/skills/research/worklog are synchronized; focused
  `py_compile`, focused 121-test grid/CLI validation, full 332-test no-GUI
  validation, CLI smokes, `git diff --check`, and read-only subagent review
  have passed.  Root docs are queued for final checksum mirror.  Final commit
  hash, push result, and branch verification are reported in the assistant
  response.  Preserve untracked `domain.cub` and `domain.pdb`.

## Current Request: 2026-06-11 README Refresh And One-Branch Closeout For DORI

- [x] Record user request immediately: update README, inspect the unusual
  branch state, converge back to one maintained branch if needed, and keep
  repository-local Git identity as `Stardust0831`.
- [x] Confirm branch topology and identity before staging.  Current branch is
  `main`; `origin/HEAD` points to `origin/main`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.  There is no feature branch that
  needs a real merge-back right now.
- [x] Finish the in-progress DORI route on `main`: README/usage/skills/
  research/worklog are synchronized; validation passed with focused
  `py_compile`, focused `tests.test_cube_preset tests.test_multiwfn_grid`
  with 111 tests, full no-GUI regression with 328 tests, CLI smoke, and
  `git diff --check`; read-only subagent review found no blocker or major
  issue and two documentation minor issues, both handled in this pass.  Root
  docs checksum mirror dry-run is empty.  Final commit hash, push result, and
  branch alignment are reported in the assistant response.  Preserve
  untracked `domain.cub` and `domain.pdb`.

## Active Goal Continuation: 2026-06-11 Next ABACUS-Compatible Visualization Route

- [x] Record automatic continuation of the long-running objective: survey
  valuable Multiwfn wavefunction analyses that can be visualized in VESTA,
  prioritizing routes that ABACUS can feed through LCAO Molden files or
  direct cube outputs.
- [x] Recheck current repository state before choosing the next increment.
  Current branch is `main` at `3e9657a0c65d0585a27d50b014021b8fda7f606f`,
  aligned with `origin/main` and `origin/HEAD`; only local untracked
  `domain.cub` and `domain.pdb` remain and must stay outside commits.
- [x] Re-audit existing `grid-run`/`cube-preset` coverage against local
  Multiwfn source, select one bounded source-backed analysis route or display
  setting that improves ABACUS-to-VESTA wavefunction visualization, then
  implement it with tests, README/usage/skill/research/worklog notes, root
  docs sync, review, commit, push, and branch verification.  Selected
  increment: DORI.  Source evidence: `function.f90` maps `iuserfunc=20` to
  `DORI(x,y,z)`, `0123dim.f90` exports function `100` as `userfunc.cub`,
  weak-interaction post-processing pairs DORI with sign(lambda2)rho, and
  bundled `DORIfill.vmd` uses DORI isosurface `0.95` with sign(lambda2)rho
  texture range `-0.04..0.02`.  Implementation added
  `grid-run --function dori`, `cube-preset dori-scalar`, and
  `cube-preset dori`.  Validation passed with focused `py_compile`,
  focused `tests.test_cube_preset tests.test_multiwfn_grid` with 111 tests,
  full no-GUI regression with 328 tests, CLI smoke, and `git diff --check`;
  review found no blocker or major issue.  Root docs checksum mirror dry-run
  is empty.  Final commit hash and post-push branch verification are reported
  in the assistant response.

## Current Request: 2026-06-11 README Refresh And Branch Consolidation For vdW Probe Route

- [x] Record user request immediately: update README, inspect the unusual
  branch state, converge back to one maintained branch if needed, and keep
  repository-local git identity as `Stardust0831`.
- [x] Confirm current branch and identity before staging anything.  Current
  branch is `main`; repository identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Finish the in-progress `grid-run --function vdw-potential
  --vdw-probe` route, including README/usage/skills/research/worklog notes,
  validation after the latest CLI/test changes, root docs sync, review-agent
  closeout, commit, push, and final branch verification.  Code/docs are
  updated and validation passed: focused `py_compile`,
  `tests.test_multiwfn_grid` with 64 tests,
  `tests.test_multiwfn_grid tests.test_cli` with 116 tests,
  `tests.test_multiwfn_grid tests.test_cube_preset` with 108 tests, full
  no-GUI regression with 325 tests, CLI smoke, and `git diff --check`.
  Root docs checksum mirror dry-run is empty.  Final commit/push and
  post-push branch verification are reported in the assistant response.
- [x] Recheck local/remote branch topology after fetch/prune and keep only
  the maintained `main` branch workflow unless a real remote side branch is
  found.  After `git fetch --prune origin`, local `main`, `origin/main`, and
  `origin/HEAD` are aligned at
  `e1ee45483eefc8cc9961994bb6ab4d2bfe02b26a`; `git ls-remote --heads origin`
  exposes only `refs/heads/main`, so no merge-back is needed.  Preserve local
  untracked probe files `domain.cub` and `domain.pdb` outside the commit.

## Active Goal Continuation: 2026-06-11 Next Wavefunction Analysis Survey

- [x] Record automatic continuation of the long-running objective: survey
  valuable Multiwfn wavefunction analyses that can be visualized in VESTA,
  prioritizing routes fed by ABACUS LCAO Molden files or ABACUS direct cube
  outputs.
- [x] Recheck current repository state, current `grid-run`/`cube-preset`
  coverage, and local Multiwfn source before selecting the next bounded
  feature increment.  Current `main` is aligned with `origin/main` at
  `e1ee45483eefc8cc9961994bb6ab4d2bfe02b26a`, with only local untracked
  `domain.cub` and `domain.pdb` probes plus this kanban update.  `grid-run`
  already covers main-function-5 functions `1-25`, `44`, `100`, `111`, and
  `112`; the next useful increment is run-local control of a source setting
  that changes an existing function's physical meaning.
- [x] Select and implement one source-backed analysis route that moves the
  project closer to broad Multiwfn-to-VESTA coverage, with tests, docs, root
  docs sync, validation, review, commit, push, and branch verification.
  Selected increment: expose `ivdwprobe` for `grid-run --function
  vdw-potential`.  Source evidence: local Multiwfn `settings.ini` defines
  `ivdwprobe=6` as the vdW potential probe atom; `function.f90` reports the
  selected probe in function `25` and `vdwpotfunc` uses it for UFF probe
  parameters; `0123dim.f90` exports `vdWpot.cub` and sets display
  `sur_value=1.0`.  Implementation in progress: default `ivdwprobe=6`,
  `--vdw-probe ELEMENT_OR_Z`, recipe recording, tests, README/usage/skill/
  research/worklog updates.  Validation passed after the final CLI/test
  patch: focused `py_compile`, `tests.test_multiwfn_grid` with 64 tests,
  `tests.test_multiwfn_grid tests.test_cli` with 116 tests, combined
  cube/grid tests with 108 tests, full no-GUI regression with 325 tests, CLI
  smoke, `git diff --check`, and root docs checksum mirror dry-run passed.
  Final commit hash and post-push branch alignment are reported in the
  assistant response to avoid a self-referential hash here.

## Active Goal Continuation: 2026-06-11 Next Wavefunction Visualization Increment

- [x] Record automatic continuation of the long-running objective: keep
  surveying Multiwfn analyses that can become VESTA products, prioritizing
  routes that ABACUS can feed through LCAO Molden files or direct cube
  outputs.
- [x] Recheck current branch and worktree before editing.  Local `main` is
  aligned with `origin/main` at
  `e5f9d7aa1016d2ffb7df5a60b1a63708a0b5008d`; only local untracked probes
  `domain.cub` and `domain.pdb` are present and must remain uncommitted.
- [x] Recheck current `grid-run` and `cube-preset` coverage against local
  Multiwfn source and select one bounded, source-backed next increment.
  Selected increment: expose run-local `ELFLOL_type` control for
  `grid-run --function elf/lol`.  Source evidence: Multiwfn `settings.ini`
  defines `ELFLOL_type=0/1/2/3`; `function.f90` changes function `9/10`
  labels between Becke, Tsirelson, and Tian Lu definitions according to this
  setting; `ELF_LOL` evaluates different formulae; and `0123dim.f90` still
  exports `ELF.cub`/`LOL.cub`.  The implementation should patch a run-local
  settings file and default ordinary `elf`/`lol` to Becke definitions so
  global Multiwfn settings do not silently change output semantics.
- [x] Implement the selected increment with tests, documentation, root docs
  sync, validation, review, commit, push, and branch verification.  The
  implementation and docs are complete; final commit hash and post-push
  branch alignment are reported in the assistant response to avoid a
  self-referential hash here.

## Current Request: 2026-06-11 README Update And Branch Consolidation With ELF/LOL Route

- [x] Record user request immediately: update README, inspect the unusual
  branch state, converge back to one maintained branch if needed, and keep
  git identity as `Stardust0831`.
- [x] Confirm current repository-local identity is already
  `Stardust0831 <13862180016@163.com>`.
- [x] Recheck local/remote branches and decide whether a merge is actually
  needed.  Local `main`, `origin/main`, and `origin/HEAD` are aligned at
  `e5f9d7aa1016d2ffb7df5a60b1a63708a0b5008d`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`, so there is no extra branch to
  merge back right now.
- [x] Preserve local untracked probe files `domain.cub` and `domain.pdb`;
  they are not part of the maintained branch state.
- [x] Finish the current uncommitted ELF/LOL run-local definition-control
  route, update README/usage/skill/research/worklog notes, sync root docs,
  validate, review, commit, push, and verify final one-branch alignment.
  Final pre-commit state: README and docs are updated, root docs checksum
  dry-run is empty, focused `py_compile` passed, `tests.test_multiwfn_grid`
  passed with 60 tests, combined cube/grid tests passed with 104 tests, full
  no-GUI regression passed with 320 tests, CLI smoke passed, and
  `git diff --check` is clean.  Read-only subagent review found one blocker
  (`LOL + d-over-d0`), which was fixed by making D/D0 ELF-only in code,
  docs, and tests.  Final commit hash and post-push branch alignment are
  reported in the assistant response.

## Active Goal Continuation: 2026-06-11 Spin Polarization Survey

- [x] Record automatic continuation of the long-running objective: keep
  surveying and implementing valuable Multiwfn wavefunction analyses for
  VESTA, prioritizing ABACUS LCAO Molden-compatible wavefunction routes.
- [x] Recheck repository state, current spin/grid coverage, and Multiwfn
  source evidence before editing.
- [x] Select whether the next bounded increment should expose Multiwfn's
  spin-polarization parameter route or defer it in favor of another
  ABACUS-compatible analysis.  Selected route: expose Multiwfn function `5`
  spin-polarization parameter as a named route because local `settings.ini`
  shows `ipolarpara=0/1`, `function.f90` changes function `5` display text
  and `fspindens` behavior according to `ipolarpara`, and `0123dim.f90`
  still exports `spindensity.cub`; the implementation should use run-local
  settings so global Multiwfn settings do not change.
- [x] Implement the selected increment with tests, docs, root docs sync,
  validation, review, commit, push, and branch verification.  Implementation,
  focused tests, README/usage/skill/research/worklog documentation, root docs
  sync, full validation, read-only review, commit, push, and final branch
  verification are complete; final commit hash is reported in the assistant
  response.

## Active Goal Continuation: 2026-06-11 Next ABACUS-Compatible Analysis Survey

- [x] Record automatic continuation of the long-running objective: keep
  surveying and implementing valuable Multiwfn wavefunction analyses that can
  become VESTA products, prioritizing ABACUS LCAO Molden-compatible routes
  and ABACUS direct cube products.
- [x] Recheck repository state, current `grid-run`/`cube-preset` coverage,
  and local Multiwfn 2026.6.2 source before selecting the next bounded
  feature increment.  Current worktree started from `main...origin/main`;
  only the new kanban edit plus local untracked `domain.cub`/`domain.pdb`
  were present.  Source review confirmed main-function-5 functions 1-25,
  44, 100, 111, and 112 coverage, and identified `iuserfunc` named analyses
  as the safest next ergonomics gap.
- [x] Select a source-backed analysis route that is useful for VESTA
  visualization and not already maintained.  Selected increment: dedicated
  named routes for high-value Multiwfn `iuserfunc` analyses already confirmed
  in `function.f90`, so `local-electron-affinity`, LEAE, information gain,
  Shannon entropy density, and Fisher information density can imply their
  `iuserfunc` values instead of requiring redundant manual indices.
- [x] Implement the selected route with focused tests and synchronized
  README/usage/research/worklog/skill notes.  Added per-route default
  `iuserfunc` handling for function-100 named analyses while preserving the
  generic `user-function --user-function-index` route; LEA/LEAE named routes
  auto-select mapped presets `lea`/`leae` when `--surface-cube` is supplied.
- [x] Sync root docs mirror, validate, review, and prepare explicit
  commit/push closeout.  Full no-GUI regression passed once with 312
  tests, CLI smoke passed, docs mirror dry-run was empty, and `git diff
  --check` passed.  Read-only subagent review found no blocker and three low
  follow-ups: mention LEA/LEAE in `--surface-cube` help, update mapped-default
  summary docs, and add tests for explicit `iuserfunc` override plus LEA/LEAE
  mapped preset selection; all three follow-ups were patched before final
  validation.  Final validation after those patches passed: focused
  `py_compile`, full 314-test no-GUI regression, `grid-run --list-functions`,
  `grid-run --help`, root docs checksum mirror dry-run, and
  `git diff --check`.  The actual pushed commit was
  `cc56b650b26a9138a93cd6a8386ec6d3c5e52870`
  (`Add named iuserfunc grid routes`), with local `main`, `origin/main`, and
  `origin/HEAD` aligned and only `domain.cub`/`domain.pdb` remaining
  untracked.

## Current Request: 2026-06-11 README Refresh And Branch Consolidation Recheck

- [x] Record user request immediately: update README, recheck the unusual
  branch state, converge back to one maintained branch if needed, and keep
  git identity as `Stardust0831`.
- [x] Audit current local/remote branch state and repository-local git
  identity before staging anything.
- [x] Refresh README and synchronized docs if the current branch state or CLI
  workflow needs clearer closeout text.
- [x] Validate and prepare an explicit closeout plan while preserving local
  untracked probe files.  Audit result before staging: after
  `git fetch --prune origin`, local `main`, `origin/main`, and `origin/HEAD`
  were aligned at `e1b3f866694e89d781f5722f0a4d18ca603c69ff`; remote heads
  exposed only `refs/heads/main`; repository-local identity was
  `Stardust0831 <13862180016@163.com>`.  Validation passed before staging:
  focused `py_compile`, full 311-test no-GUI regression, `grid-run
  --list-functions`, `cube-preset --list-presets`, `grid-run --help`,
  `bin/multiwfn2vesta --help`, root docs checksum mirror dry-run, and
  `git diff --check`; read-only subagent review found one documentation
  status problem about premature commit/push wording, fixed in this update.
- [x] Stage only intended tracked files, commit/push the real update, and
  verify `main`/`origin/main` alignment.  Final commit hash and post-push
  branch alignment were reported in the assistant response; the actual
  pushed commit was `0e587a076b136ad86fdba81fbd51939dc56f99d1`
  (`Add user-function grid preset`), with local `main`, `origin/main`, and
  `origin/HEAD` aligned and only `domain.cub`/`domain.pdb` remaining
  untracked.

## Active Goal Continuation: 2026-06-11 User-Function Grid Route

- [x] Record automatic continuation of the long-running objective: survey and
  implement valuable Multiwfn wavefunction analyses that can be visualized in
  VESTA, prioritizing analyses ABACUS can feed through LCAO Molden files or
  direct cube outputs.
- [x] Recheck current repository state, Multiwfn source evidence, and existing
  `grid-run`/`cube-preset` coverage before editing.  Source evidence:
  `settings.ini` defines `iuserfunc`, main menu `1000 -> 2` can set it,
  `function.f90` evaluates `userfunc(x,y,z)`, and `0123dim.f90` exports
  `userfunc.cub`.
- [x] Implement a maintained Multiwfn main-function-5 `ifuncsel=100`
  user-defined function route using run-local `iuserfunc` settings, with
  conservative exclusions for special external-grid modes.  Added
  `grid-run --function user-function --user-function-index IUSERFUNC`,
  `cube-preset user-function`, recipe fields, CLI help, and batch-mode
  rejection for non-orbital user-function options.
- [x] Add focused tests, README/usage/research/skill documentation, and
  worklog/skill notes.  Focused validation already passed for `py_compile`
  and 95 cube/grid tests; root docs mirror sync remains for final validation.
- [x] Validate, review, and prepare branch closeout on `main`;
  keep `domain.cub` and `domain.pdb` untracked.  Validation passed before
  review: focused `py_compile`, 95 focused cube/grid tests, full 311-test
  no-GUI regression, `grid-run --list-functions`, `cube-preset
  --list-presets`, `grid-run --help`, root docs checksum mirror dry-run, and
  `git diff --check`.  Pre-commit subagent review found no blocking issue and
  two low documentation mismatches; both were fixed by clarifying cube-preset
  versus grid-run aliases and batch-mode rejection docs.  Final validation
  passed again after the README branch refresh: focused `py_compile`, full
  311-test no-GUI regression, CLI smoke checks, root docs mirror dry-run, and
  `git diff --check`.  The final commit/push result is reported by the
  assistant response after it actually happens.

## Current Request: 2026-06-11 README Refresh And Main Branch Consolidation

- [x] Record user request: update README, inspect unusual branch state,
  consolidate back to one maintained branch if needed, and keep Git identity
  as `Stardust0831`.
- [x] Confirm repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Recheck branch state after `git fetch --prune origin`: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `13e657fb700cc8d4bbb4c126434d6762d0f4d5f5`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`.
- [x] Decide merge action: no merge-back is needed because there is no extra
  local or remote feature branch to consolidate.
- [x] Refresh README branch-status text to the current single-branch state
  and keep the pair-function closeout on `main`.
- [x] Sync root docs mirror and validate the documentation-only change.
  Passed checks: root docs checksum mirror dry-run, `git diff --check`,
  `bin/multiwfn2vesta --help`, remote-head audit, git identity audit, and
  read-only subagent review with no blocking issue.
- [x] Prepare explicit staging/commit/push closeout.  Final commit hash and
  post-push branch alignment are reported in the assistant response to avoid
  a self-referential docs loop; keep `domain.cub` and `domain.pdb` untracked.

## Active Goal Continuation: 2026-06-11 Next ABACUS-Compatible Wavefunction Visualization Increment

- [x] Record automatic continuation of the long-running objective: keep
  researching and implementing valuable Multiwfn wavefunction analyses that
  can become VESTA products, prioritizing workflows fed by ABACUS LCAO
  Molden files or direct ABACUS cube outputs.
- [x] Recheck current repository state before new edits: local `main` and
  `origin/main` are aligned at
  `c879f30c62e8361b6636f88504abed30bdce75b1`; local untracked probes
  `domain.cub` and `domain.pdb` remain outside version control.
- [x] Inspect current `grid-run`/`cube-preset` coverage and local Multiwfn
  2026.6.2 source for the next bounded, source-backed increment.
- [x] Selected increment: Multiwfn function `17` pair/correlation function.
  Source evidence: `function.f90` calls
  `pairfunc(refx,refy,refz,x,y,z)`, `settings.ini` controls the physical
  quantity through `pairfunctype`/`paircorrtype`, and `0123dim.f90` exports
  `fermihole.cub`.
- [x] Implement `grid-run --function pair-function` plus
  `cube-preset pair-function`, using `--reference-point`,
  `--reference-unit`, `--pair-function-type`, and
  `--pair-correlation-type`; preserve global Multiwfn settings by copying
  the selected `settings.ini` when available and patching a run-local
  `multiwfn_grid_settings.ini`.
- [x] Focused validation passed during implementation: `py_compile` for
  edited modules/tests and 90 tests across `tests.test_cube_preset` and
  `tests.test_multiwfn_grid`.
- [x] Finish README/usage/skills/research docs sync for the selected
  increment.
- [x] Sync root docs mirror and validate.  Passed checks: focused
  `py_compile`, 90 focused cube/grid tests, full 306-test no-GUI regression,
  `cube-preset --list-presets`, `grid-run --list-functions`,
  `grid-run --help`, `bin/multiwfn2vesta --help`, docs mirror dry-run,
  stale pair-function wording scan, and `git diff --check`.
- [x] Complete pre-commit review.  The delegated read-only subagent response
  was unrelated and not used as evidence; local review found no blocking
  issue in branch-status text, function-17 command stream, run-local
  settings handling, CLI validation, docs sync, or untracked probe handling.
- [x] Commit, push, and verify branch alignment for the pair-function feature:
  `13e657fb700cc8d4bbb4c126434d6762d0f4d5f5` is on local `main`,
  `origin/main`, and `origin/HEAD`; keep `domain.cub` and `domain.pdb`
  untracked.

## Current Request: 2026-06-10 README Refresh, Branch Check, Source Function Closeout

- [x] Record user request: update README, inspect unusual-looking branch
  state, converge back to one maintained branch if needed, and keep git
  identity as `Stardust0831`.
- [x] Confirm repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Recheck branch state after `git fetch --prune origin`: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `49a350619601fdff76c0e993b55b2c9c26024ccc`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`.
- [x] Decide merge action: no merge-back is needed because there is no extra
  local branch or remote feature branch to consolidate.
- [x] Refresh README branch-status text to the current single-branch state.
- [x] Preserve local untracked probes `domain.cub` and `domain.pdb` outside
  version control.
- [x] Run validation before review: focused `py_compile`; full
  `python3 -m unittest discover -s tests -v` with 302 tests; `cube-preset
  --list-presets`; `grid-run --list-functions`; `grid-run --help`;
  `bin/multiwfn2vesta --help`; and `git diff --check`.
- [x] Complete read-only subagent review.  No commit-blocking issue was
  found; the only non-blocking caveat was that a minimal `-set` file may
  bypass user-customized Multiwfn settings, so the implementation now copies
  and patches a base `settings.ini` when available.
- [x] Patch source-function settings generation to preserve base Multiwfn
  settings when possible.
- [x] Re-run validation after the settings-file patch: focused
  `py_compile`, 86 focused tests across `tests.test_cube_preset` and
  `tests.test_multiwfn_grid`, full 302-test no-GUI regression,
  `cube-preset --list-presets`, `grid-run --list-functions`,
  `grid-run --help`, `bin/multiwfn2vesta --help`, stale settings-wording
  scan, and `git diff --check`.
- [x] Complete final read-only review.  No commit-blocking issue was found;
  the only low item was this historical caveat wording, now cleaned up.
- [x] Prepare explicit staging/commit/push closeout.  Final commit hash and
  post-push branch alignment are reported in the assistant response to avoid
  a self-referential docs loop.

## Active Goal Continuation: 2026-06-10 Reference-Point Grid Function Resume

- [x] Record automatic continuation of the long-running objective: research
  and implement valuable Multiwfn wavefunction/grid analyses that can become
  VESTA products, especially workflows fed by ABACUS LCAO Molden files or
  direct ABACUS cube outputs.
- [x] Keep the previous README/branch closeout separated from this feature
  work: `main`, `origin/main`, and `origin/HEAD` were aligned at
  `49a350619601fdff76c0e993b55b2c9c26024ccc` after that documentation
  commit; local `domain.cub` and `domain.pdb` probes remain outside version
  control.
- [x] Inspect local Multiwfn 2026.6.2 source for reference-point dependent
  main-function-5 grid functions and choose the next bounded increment.
- [x] Implement the selected increment with focused tests and documentation,
  preserving existing standalone-cube, mapped-surface, and fragment-route
  separation.
- [x] Selected increment: Multiwfn function `19` source function.  Source
  evidence: `function.f90` calls `srcfunc(x,y,z,srcfuncmode)`, `srcfunc`
  depends on global `refx,refy,refz`, `0123dim.f90` exports `srcfunc.cub`,
  and main menu `1000 -> 1` sets the reference point.  Implementation uses
  run-local `multiwfn_grid_settings.ini` with `-set` for `srcfuncmode` and
  does not edit global Multiwfn settings.
- [x] Focused validation passed before full regression: `py_compile` for the
  edited modules/tests and `tests.test_cube_preset tests.test_multiwfn_grid`
  with 86 tests.
- [x] Validate implementation and CLI help before review.
- [x] Address subagent settings-file caveat by copying the selected
  Multiwfn `settings.ini` when available, patching `srcfuncmode` into a
  run-local `multiwfn_grid_settings.ini`, and keeping global settings
  untouched.
- [x] Re-run validation after the settings-file patch: focused
  `py_compile`, 86 focused tests across `tests.test_cube_preset` and
  `tests.test_multiwfn_grid`, full 302-test no-GUI regression, CLI smoke
  checks, stale settings-wording scan, and `git diff --check`.
- [x] Complete final read-only review.  No commit-blocking issue was found;
  the only low item was stale historical caveat wording in the kanban, now
  cleaned up.
- [x] Prepare explicit staging/commit/push closeout; keep `domain.cub` and
  `domain.pdb` untracked.  Final commit hash and post-push branch alignment
  are reported in the assistant response to avoid a self-referential docs
  loop.

## Current Request: 2026-06-10 README Refresh And Main Branch Consolidation At Delta-g Tip

- [x] Record user request before editing: update README, inspect the
  unusual-looking branch state, merge/converge back to one maintained branch
  if needed, and keep git identity as `Stardust0831`.
- [x] Confirm repository-local git identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Recheck current branch state after `git fetch --prune origin`: local
  `main`, `origin/main`, and `origin/HEAD` are aligned at
  `028a7caae9af6f10de3fa1639ce6fce6f136787d`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`.
- [x] Decide whether a merge-back is needed: no merge is needed because
  there is no extra local branch or remote feature branch to consolidate.
- [x] Refresh README and worklog with the current single-branch state,
  branch audit, git identity, and untracked probe-file handling.
- [x] Sync root docs mirror, validate, and complete read-only review before
  explicit staging.  Validation passed: root docs checksum mirror dry-run,
  `bin/multiwfn2vesta --help`, and `git diff --check`.  Review found no
  High/Medium/Low blocker and confirmed the README/worklog/kanban branch
  state is consistent, only `main` is exposed by the remote, and local
  `domain.cub`/`domain.pdb` probes remain untracked.  Final commit hash and
  post-push alignment are reported in the assistant response to avoid a
  self-referential docs loop.

## Active Goal Continuation: 2026-06-10 Next Reference-Point Grid Increment

- [x] Record automatic continuation of the long-running objective: keep
  enriching Multiwfn wavefunction analyses that can become VESTA products,
  prioritizing workflows fed by ABACUS LCAO Molden files or direct cube
  outputs.
- [x] Recheck current repository state before new edits: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `028a7caae9af6f10de3fa1639ce6fce6f136787d`; only local untracked probes
  `domain.cub` and `domain.pdb` remain outside version control.
- [ ] Deferred during the README/branch closeout so this pass remains a
  documentation-only maintenance update.
- [ ] Inspect local Multiwfn 2026.6.2 source for the next bounded,
  source-backed reference-point or real-space function increment.
- [ ] Implement the selected increment with focused tests and documentation,
  preserving existing standalone-cube, mapped-surface, and fragment-route
  separation.
- [ ] Sync root docs mirror, validate, review, commit, push, and verify
  branch alignment; keep `domain.cub` and `domain.pdb` untracked.

## Active Goal Continuation: 2026-06-10 Hirshfeld Delta-g And README Closeout

- [x] Record automatic continuation of the long-running objective: keep
  researching and implementing valuable Multiwfn wavefunction analyses that
  can be visualized in VESTA, prioritizing routes that ABACUS can feed via
  LCAO Molden wavefunction files or direct cube outputs.
- [x] Record user request: update README, inspect the unusual-looking branch
  state, converge back to one maintained branch if needed, and keep git
  identity as `Stardust0831`.
- [x] Recheck current repository state before new edits: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `9169e611a3ea3818b7f65d90ade6e45518322bde`; remote-visible branch state is
  only `refs/heads/main`, so no branch merge is needed; local untracked
  probes `domain.cub` and `domain.pdb` remain outside version control.
- [x] Inspect current `grid-run`/`cube-preset` coverage, local Multiwfn
  2026.6.2 source, and the analysis matrix.  Selected increment: Multiwfn
  main-function-5 function `23`, Delta-g with Hirshfeld partition, because
  `function.f90` calls `delta_g_Hirsh` and `0123dim.f90` leaves its cube
  export at generic `griddata.cub`.
- [x] Implement `cube-preset hirshfeld-delta-g` plus
  `grid-run --function hirshfeld-delta-g`, keeping function `22`
  `delta-g` aliases mapped to promolecular `Delta_g.cub` and keeping
  IGM/IGMH fragment `dg_inter.cub` mapped-surface routes separate.
- [x] Update focused tests, README, usage docs, skills, research matrix, and
  worklog with the `griddata.cub` raw-output behavior and single-branch
  closeout status.
- [x] Sync root docs mirror and validate before review.  Validation passed:
  root docs checksum mirror dry-run, focused `py_compile`, 81 focused tests
  across `tests.test_cube_preset` and `tests.test_multiwfn_grid`,
  `cube-preset --list-presets`, `grid-run --list-functions`,
  `grid-run --help`, `bin/multiwfn2vesta --help`, `git diff --check`, and
  full 297-test no-GUI regression.
- [x] Complete read-only review and prepare explicit staging/commit/push
  closeout; keep `domain.cub` and `domain.pdb` untracked.  Review found no
  High/Medium blocker and confirmed README branch status, function `22`
  promolecular `Delta_g.cub` separation, function `23` generic
  `griddata.cub` handling, docs/skills/worklog/kanban sync, and root docs
  mirror sync.  The only Low finding is to avoid `git add .` / `git add -A`
  because `domain.cub` and `domain.pdb` are local probes.  Final commit hash
  and post-push branch alignment are reported in the assistant response to
  avoid a self-referential docs loop.

## Active Goal Continuation: 2026-06-10 Hirshfeld Weight Grid Cube

- [x] Record automatic continuation of the long-running objective: keep
  researching and implementing valuable Multiwfn wavefunction/grid analyses
  that can become VESTA products, with priority on ABACUS LCAO
  Molden-compatible routes.
- [x] Recheck current repository state: local `main`, `origin/main`, and
  `origin/HEAD` are aligned at
  `e68ace19a4d2b155d8817cb3094dc9bba065ecb8`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`; only local untracked probes
  `domain.cub` and `domain.pdb` remain outside version control.
- [x] Inspect local Multiwfn 2026.6.2 source for the next bounded feature:
  main-function-5 function `112` asks for a Hirshfeld atom selection string,
  then asks how to generate atomic densities; choosing `2` uses built-in
  atomic densities and exports `Hirshfeld.cub`.
- [x] Implement `cube-preset hirshfeld-weight` and
  `grid-run --function hirshfeld-weight --hirshfeld-atoms ATOMS`, initially
  supporting the bounded built-in atomic-density mode.
- [x] Update tests, README, usage docs, skills, research matrix, and worklog.
- [x] Sync root docs mirror, validate, review, commit, push, and verify
  `main` remains aligned with `origin/main`; keep `domain.cub` and
  `domain.pdb` untracked.  Validation passed before commit: root docs
  checksum mirror dry-run, focused `py_compile`, 78 focused tests across
  `tests.test_cube_preset` and `tests.test_multiwfn_grid`, full 294-test
  no-GUI regression, `cube-preset --list-presets`,
  `grid-run --list-functions`, `grid-run --help`,
  `bin/multiwfn2vesta --help`, and `git diff --check`.  Read-only review
  found no High/Medium blocker and confirmed function `112` uses the
  `5,112,<selection>,2,<grid setup>,2,0,q` built-in-density command stream.
  Final commit hash and post-push branch alignment are reported in the
  assistant response to avoid a self-referential docs loop.

## Current Request: 2026-06-10 README Refresh And Single-Branch Closeout

- [x] Record user request before final edits: update README, check the
  unusual-looking branch state, converge to one maintained branch if needed,
  and keep git identity as `Stardust0831`.
- [x] Confirm current branch state: local `main`, `origin/main`, and
  `origin/HEAD` are aligned at
  `e68ace19a4d2b155d8817cb3094dc9bba065ecb8`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`; no extra branch needs merging.
- [x] Refresh README and docs with the current single-branch status plus the
  new Hirshfeld weight grid/preset workflow.
- [x] Sync root docs mirror, run validation, perform read-only review, commit
  and push to `origin/main`, then verify final branch alignment.  Validation
  passed before commit: root docs checksum mirror dry-run, focused
  `py_compile`, 78 focused tests, full 294-test no-GUI regression,
  `cube-preset --list-presets`, `grid-run --list-functions`,
  `grid-run --help`, `bin/multiwfn2vesta --help`, and `git diff --check`.
  Read-only review found no High/Medium blocker.  Final commit hash and
  post-push branch alignment are reported in the assistant response.

## Current Request: 2026-06-10 README Refresh And Branch Consolidation At Becke Tip

- [x] Record user request before editing: update README, inspect the
  unusual-looking branch state, merge/converge back to one maintained branch
  if needed, and keep git identity as `Stardust0831`.
- [x] Confirm the actual maintained repository for this workspace is
  `/mnt/g/work/multiwfn2vesta/project`; the workspace-level
  `/mnt/g/work/multiwfn2vesta/.git` is an empty metadata stub and is not the
  GitHub project checkout used for commits.
- [x] Recheck branch and identity state without destructive operations:
  after `git fetch --prune origin`, local `main`, `origin/main`, and
  `origin/HEAD` are aligned at
  `27065d0bf4b5f4096044065cd76a4eaa52735704`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Decide whether a branch merge is needed: no merge is needed because no
  extra local or remote feature branch exists; this closeout should stay on
  maintained `main`.
- [x] Refresh README and project docs with the current branch audit,
  one-branch policy, working checkout path, and untracked probe-file handling.
- [x] Sync root docs mirror, validate, review, commit, push, and verify
  `main` remains aligned with `origin/main`; keep `domain.cub` and
  `domain.pdb` untracked.  Validation passed before commit: root docs
  checksum mirror dry-run, `git diff --check`, and `bin/multiwfn2vesta
  --help`.  Final commit hash and post-push branch alignment are reported in
  the assistant response to avoid a self-referential docs loop.

## Active Goal Continuation: 2026-06-10 Next ABACUS-Molden Multiwfn Analysis

- [x] Record automatic continuation of the long-running objective: keep
  researching and implementing valuable Multiwfn wavefunction analyses that
  can become VESTA products, with priority on ABACUS LCAO Molden-compatible
  routes.
- [x] Re-inspect current `grid-run`/`cube-preset` coverage, local Multiwfn
  2026.6.2 source exports, and the research matrix for the next bounded
  source-backed increment.  Selected increment: Multiwfn main-function-5
  function `111` Becke atomic/overlap weight, because local source
  `0123dim.f90` prompts for atom indices before grid setup and exports
  `Becke.cub`; it is compatible with ABACUS LCAO Molden wavefunctions.
- [x] Implement `cube-preset becke-weight` plus `grid-run --function
  becke-weight --becke-atoms I J`, where `J=0` means Becke atomic weight and
  `I,J` means Becke overlap weight.
- [x] Update tests, README, usage docs, skills, research matrix, and worklog.
- [x] Implement the selected increment with tests and documentation while
  preserving existing mapped-surface and standalone-cube route separation.
  Focused validation passed: `py_compile` for changed modules/tests, 75
  focused tests across `tests.test_cube_preset tests.test_multiwfn_grid`, and
  `bin/multiwfn2vesta grid-run --help`.
- [x] Sync root docs mirror, validate, review, commit, push, and verify
  `main` remains aligned with `origin/main`; keep `domain.cub` and
  `domain.pdb` untracked.  Validation passed before commit: root docs
  checksum mirror dry-run, full 291-test no-GUI regression,
  `cube-preset --list-presets`, `grid-run --list-functions`,
  `grid-run --help`, `bin/multiwfn2vesta --help`, and `git diff --check`.
  Read-only review found no High blocker; the Medium reminder is to keep
  untracked `domain.cub` and `domain.pdb` out of staging.  Final commit hash
  and post-push branch alignment are reported in the assistant response.

## Active Goal Continuation: 2026-06-10 Next Multiwfn VESTA Analysis Gap

- [x] Record automatic continuation of the long-running objective: keep
  researching valuable Multiwfn wavefunction/grid analyses that can be
  visualized in VESTA, especially workflows that ABACUS can feed through
  LCAO Molden or direct cube outputs.
- [x] Inspect the current implemented coverage, local Multiwfn 2026.6.2
  source, and research matrix to choose the next source-backed, bounded
  feature increment.
- [x] Implement the selected increment with tests and documentation, keeping
  standalone single-cube routes separate from mapped surface/texture routes.
- [x] Sync root docs mirror, validate, review, commit, push, and verify
  `main` remains aligned with `origin/main`.

## Active Implementation: 2026-06-10 EDR and Orbital-Overlap Distance

- [x] Record user request: update README, inspect unusual branch state,
  merge/consolidate back to one branch where appropriate, and use identity
  `Stardust0831`.
- [x] Inspect current branch/remote/status without disturbing existing work:
  local `main`, `origin/main`, and `origin/HEAD` are aligned at
  `6de6b017d8fa8b66cde24731ca5403081201a0b4`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`; no extra branch needs merging.
- [x] Preserve local probes: `domain.cub` and `domain.pdb` remain untracked
  and must not be staged unless explicitly promoted later.
- [x] Select this bounded increment: Multiwfn 2026.6.2 source shows function
  `20` EDR(r;d) asks for length scale `d` in Bohr and exports `EDR.cub`;
  function `21` D(r) accepts default or manual EDR exponent parameters and
  exports `EDRDmax.cub`; both keep the global main-function-5
  `sur_value=0.05`.
- [x] Add `cube-preset electron-delocalization-range` and
  `cube-preset orbital-overlap-distance`.
- [x] Add `grid-run --function edr --edr-length D_BOHR` and
  `grid-run --function edrdmax [--edr-exponents COUNT START INCREMENT]`,
  including command-stream validation and recipe fields.
- [x] Update focused tests, README, usage docs, skills, research matrix, and
  worklog.
- [x] Sync root docs mirror, run full validation, collect read-only review,
  commit, push, and verify `main`/`origin/main` alignment.  Validation
  passed: focused `py_compile`, 72 focused tests across
  `tests.test_cube_preset tests.test_multiwfn_grid`, full 288-test no-GUI
  regression, `cube-preset --list-presets`, `grid-run --list-functions`,
  `grid-run --help`, `bin/multiwfn2vesta --help`, root-docs checksum
  mirror, and `git diff --check`.  Read-only review found no High blocker;
  the two Medium workflow notes were addressed by excluding `domain.cub` /
  `domain.pdb` from staging and syncing the root docs mirror.

## Active Implementation: 2026-06-10 Standalone vdW Potential Cube Preset

- [x] Record continuation request: keep enriching useful Multiwfn
  wavefunction/grid analyses that can be visualized in VESTA, especially
  workflows that ABACUS can feed through Molden or direct cube routes.
- [x] Record current user request: refresh README, audit the unusual-looking
  branch state, converge to one maintained branch if needed, and keep git
  identity as `Stardust0831 <13862180016@163.com>`.
- [x] Recheck current state: local `main` is aligned with `origin/main` at
  `fae7ac12d9a6d1fadbeda7a60c484752a643c23f`; untracked local probes
  `domain.cub` and `domain.pdb` remain uncommitted.
- [x] Recheck branch and identity state: local `main`, `origin/main`, and
  `origin/HEAD` are aligned at
  `fae7ac12d9a6d1fadbeda7a60c484752a643c23f`; `origin` points to
  `Github:Stardust0831/multiwfn2vesta.git`; remote-visible branch state is
  one maintained `main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Select this bounded increment: Multiwfn `function.f90` lists function
  `25` as van der Waals potential, `0123dim.f90` exports `vdWpot.cub`, and
  the export block sets `sur_value=1D0`; the project currently routes
  standalone `grid-run --function vdw-potential` through generic `signed`
  while only the `--surface-cube` route uses `vdw-map`.
- [x] Add a dedicated standalone `cube-preset vdw-potential` and map
  `grid-run --function vdw-potential` to it without changing `vdw-map`.
- [x] Update focused tests, README, usage docs, skills, research matrix, and
  worklog.
- [x] Sync root docs mirror, validate, and review: focused `py_compile`, 66
  focused tests across `tests.test_cube_preset tests.test_multiwfn_grid`,
  full 282-test no-GUI regression, `cube-preset --list-presets`,
  `grid-run --list-functions`, `bin/multiwfn2vesta --help`,
  root-docs checksum mirror, and `git diff --check` passed; read-only review
  found no High/Medium blocker and confirmed standalone `vdw-potential` plus
  mapped `vdw-map` routes stay separate.
- [x] Prepare explicit staging, commit, push, and post-push verification with
  `Stardust0831` identity.  Final commit hash and branch-alignment check are
  reported in the assistant response to avoid a self-referential docs loop.

## Active Implementation: 2026-06-10 Promolecular Delta-g Cube Preset

- [x] Record continuation request: keep enriching useful Multiwfn
  wavefunction/grid analyses that can be visualized in VESTA, especially
  workflows that ABACUS can feed through Molden or direct cube routes.
- [x] Recheck current state after README branch closeout: local `main` is
  aligned with `origin/main` at
  `4af3bec35b85fb9a5d1b49ab6770361de528ce16`; untracked local probes
  `domain.cub` and `domain.pdb` remain uncommitted.
- [x] Select this bounded increment: implement a dedicated VESTA preset for
  Multiwfn function `22` promolecular `Delta_g.cub`, keeping it separate
  from IGM/IGMH fragment `dg_inter.cub` mapped-surface routes.
- [x] Update source and focused tests for `cube-preset
  promolecular-delta-g` and `grid-run --function delta-g`.
- [x] Update README, usage docs, skills, research matrix, and worklog with
  the standalone `Delta_g.cub` route and the distinction from IGM/IGMH
  `dg_inter.cub`.
- [x] Sync root docs mirror.
- [x] Validate and review: focused `py_compile`, 63 focused tests across
  `tests.test_cube_preset tests.test_multiwfn_grid`, full 279-test no-GUI
  regression, `cube-preset --list-presets`, `grid-run --list-functions`,
  `bin/multiwfn2vesta --help`, and `git diff --check` passed; read-only
  review found no source/test blocker and confirmed IGM/IGMH plus IRI/RDG
  texture routes are not overwritten.
- [x] Prepare explicit staging, commit, push, and post-push verification with
  `Stardust0831` identity.  Final commit hash and branch-alignment check are
  reported in the assistant response to avoid a self-referential docs loop.

## Current Request: 2026-06-10 README Refresh And One-Branch Closeout

- [x] Record user request before editing: update README, inspect the
  unusual-looking branch state, merge or converge back to one maintained
  branch if needed, and use `Stardust0831` identity for git work.
- [x] Recheck branch and identity state without destructive operations:
  after `git fetch --prune origin`, local `main`, `origin/main`, and
  `origin/HEAD` are aligned at
  `764382c01698111f9d8b41932759a480233a272b`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Decide whether a branch merge is needed: no merge is needed in this
  pass because there is no extra local branch or remote feature branch to
  consolidate.
- [x] Refresh README and project docs so the current branch audit, single
  maintained `main` branch policy, and untracked local probe-file handling are
  explicit.
- [x] Sync root docs mirror, validate, and run read-only review: root docs
  mirror dry-run is clean; `git diff --check` and
  `bin/multiwfn2vesta --help` passed; the reviewer found no branch-status
  blocker and confirmed Promolecular Delta-g remains unfinished.
- [x] Prepare explicit staging, commit, push, and post-push verification with
  `Stardust0831` identity.  Final commit hash and branch-alignment check are
  reported in the assistant response to avoid a self-referential docs loop.

## Active Goal Continuation: 2026-06-10 Promolecular Delta-g Cube

- [x] Record continuation objective: keep expanding useful Multiwfn
  wavefunction/grid analyses that can become VESTA products, especially
  analyses ABACUS can feed through LCAO Molden or direct cube routes.
- [x] Recheck current state: local `main` is aligned with `origin/main` at
  `764382c01698111f9d8b41932759a480233a272b`; untracked local probes
  `domain.cub` and `domain.pdb` remain uncommitted.
- [x] Choose the next source-backed stable gap: Multiwfn 2026.6.2
  `function.f90` lists function `22` as Delta-g with promolecular
  approximation and `0123dim.f90` exports it as `Delta_g.cub`; at selection
  time, the project still routed `grid-run --function delta-g` through
  generic `density`.
- [x] Recheck source/template defaults, then add a maintained `cube-preset`
  and `grid-run` mapping for promolecular `Delta_g.cub` without changing
  IGM/IGMH fragment `dg_inter.cub` mapped-surface routes.
- [x] Sync root docs for the active implementation.
- [x] Validate, review, commit, push, and verify `main`
  remains aligned with `origin/main`; this is being completed by the active
  implementation section above, with final commit hash reported in the
  assistant response.

## Active Goal Continuation: 2026-06-10 Local Information Entropy Cube

- [x] Record continuation objective: keep expanding useful Multiwfn
  wavefunction analyses that can become VESTA products, especially analyses
  ABACUS can feed through LCAO Molden or direct cube routes.
- [x] Recheck current state: local `main` is aligned with `origin/main` at
  `287974cdd66db52b8f0f3581b63537d221980da1`; untracked local probes
  `domain.cub` and `domain.pdb` remain uncommitted.
- [x] Inspect current source-backed grid-function gaps: Multiwfn 2026.6.2
  `function.f90` lists function `11` as local information entropy and
  `0123dim.f90` exports it as `infoentro.cub`; reference-point and EDR
  routes were deferred at that time because they needed reference points or
  extra EDR parameters.  EDR/D(r) was later implemented in the 2026-06-10 EDR
  and orbital-overlap distance increment above; source function was later
  implemented in the 2026-06-10 source-function increment; pair/correlation
  functions were later implemented in the 2026-06-11 pair-function increment.
- [x] Add a maintained `cube-preset` and `grid-run` mapping for
  `infoentro.cub`, with focused tests and docs: implemented
  `cube-preset local-information-entropy`, mapped `grid-run --function
  information-entropy` to Multiwfn function `11`, documented the source
  evidence, and focused `py_compile` plus
  `tests.test_cube_preset tests.test_multiwfn_grid` passed with 61 tests.
- [x] Sync root docs, validate, review, then prepare commit/push on `main`:
  focused `py_compile`, 61 focused tests, full 277-test no-GUI regression,
  `cube-preset --list-presets`, `grid-run --list-functions`,
  `bin/multiwfn2vesta --help`, and `git diff --check` passed.  Commit/push
  and post-push branch verification are reported in the assistant response to
  avoid a self-referential hash loop.

## Current Request: 2026-06-10 README Refresh And Main Branch Closeout

- [x] Record user request: update README, inspect the unusual-looking branch
  state, merge back to one maintained branch if needed, and use
  `Stardust0831` identity.
- [x] Inspect branch and identity state without destructive operations:
  local `main`, `origin/main`, and `origin/HEAD` are aligned at
  `34b2b012ced5dd474874fecc55f74ac17e0c4caa`; `origin` points to
  `Github:Stardust0831/multiwfn2vesta.git`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Decide whether a branch merge is needed: no merge is needed because
  local and remote expose only the maintained `main` branch.
- [x] Refresh README repository-status wording to the current branch-audit
  baseline and keep the active IRI scalar increment on the same `main`
  branch.
- [x] Sync root docs, validate, review, then prepare commit/push on `main`:
  root docs mirror is clean; focused `py_compile`, 59 focused tests, full
  275-test no-GUI regression, `cube-preset --list-presets`,
  `grid-run --list-functions`, `bin/multiwfn2vesta --help`, remote-head
  audit, and `git diff --check` passed.  Commit/push and post-push branch
  verification are reported in the assistant response to avoid a
  self-referential hash loop.

## Current Continuation: 2026-06-10 IRI Scalar Cube Display

- [x] Record resumed objective: keep expanding maintained VESTA-ready
  Multiwfn/ABACUS wavefunction and cube analyses, prioritizing products that
  ABACUS can feed through Molden or direct cube routes.
- [x] Recheck current state: `main` is aligned with `origin/main` at
  `34b2b012ced5dd474874fecc55f74ac17e0c4caa`; untracked local probes
  `domain.cub` and `domain.pdb` remain uncommitted.
- [x] Inspect current `grid-run` and `cube-preset` coverage for real-space
  function `24` IRI scalar cubes: `grid-run` already generates `IRI.cub` but
  routes it through generic `density`; Multiwfn 2026.6.2 `0123dim.f90`
  confirms function `24` exports `IRI.cub` and sets `sur_value=1D0`.
- [x] Implement a standalone `iri-scalar` preset and map `grid-run
  --function iri` to it without changing the existing two-cube
  `cube-preset iri` / `rdg` texture route; focused `py_compile` and
  `tests.test_cube_preset tests.test_multiwfn_grid` currently pass with 59
  tests.
- [x] Sync root docs, validate, review, then prepare commit/push on `main`:
  root docs mirror is clean; focused and full no-GUI tests passed; CLI
  preset/function listings show `iri-scalar`; main-thread diff review found
  no blocker.  Commit/push and post-push verification are reported in the
  assistant response.

## Current Request: 2026-06-10 README Refresh At Spin-Density Tip

- [x] Record user request: update README, inspect the unusual-looking branch
  state, consolidate back to one maintained branch if needed, and use the
  `Stardust0831` git identity.
- [x] Inspect local/remote branches and repository identity without touching
  unrelated local probes: local `main`, `origin/main`, and `origin/HEAD` are
  aligned at `1a8bbc63cc785ec07b4b177078909971b8ac127b`
  (`Add spin-density cube arithmetic`); `git ls-remote --heads origin`
  exposes only `refs/heads/main`; repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Decide whether a branch merge is needed: no merge is needed because
  there is no extra local branch or remote feature branch to consolidate.
- [x] Refresh README repository-status wording so the single-branch state,
  SSH remote, commit identity, and branch-audit baseline are current.
- [x] Sync root docs mirror, validate the docs-only refresh, and run a
  read-only review: root docs mirror is clean; `git diff --check` and
  `bin/multiwfn2vesta --help` passed; read-only subagent review found no
  blocker.  Commit/push and post-push branch verification are reported in the
  assistant response to avoid another self-referential hash loop.

## Current Request: 2026-06-10 README Refresh And Branch Convergence

- [x] Record user request: update README, inspect the unusual branch state,
  converge the maintained work back to a single branch if needed, and use
  `Stardust0831` identity for commits.
- [x] Inspect local/remote branches, repository identity, and current
  uncommitted work without touching unrelated local probes: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `77c134e2d7cd844e6cc9c4dce59f316a90700192`; `origin` exposes only
  `refs/heads/main`; untracked `domain.cub` and `domain.pdb` remain local
  probes and must stay uncommitted.
- [x] Refresh README so current usage, maintained CLI entry points, docs
  locations, and branch policy are accurate.
- [x] Decide whether any branch merge is needed; no merge is needed because
  there is no extra local or remote feature branch to consolidate.
- [x] Sync root docs mirror, validate the documentation-only change, and run
  read-only subagent review: `git diff --check` and
  `bin/multiwfn2vesta --help` passed; subagent found no branch-status
  blockers.
- [x] Commit and push the README branch-convergence refresh with
  `Stardust0831` identity as `17b489348d229aae9fe63c74067b12eab8eefcb4`;
  post-push verification showed local `main`, `origin/main`, and
  `origin/HEAD` aligned at that commit, with only `refs/heads/main` exposed
  by the remote.  This docs-only closure records the verification; its final
  hash is reported in the assistant response to avoid a self-referential
  record loop.

## Current Continuation: 2026-06-10 Spin-Density Cube Arithmetic

- [x] Record resumed objective: keep expanding VESTA-ready Multiwfn/ABACUS
  wavefunction and cube analyses, especially where ABACUS can provide
  compatible cube inputs directly or through Molden.
- [x] Inspect current branch state: local `main` is aligned with
  `origin/main`; only untracked local probes `domain.cub` and `domain.pdb`
  are present and must stay uncommitted.
- [x] Choose the next bounded increment from the prior review: add an
  explicit `cube-arith` spin-density operation for alpha/beta or
  spin-up/spin-down density cubes, then route the result to
  `cube-preset spin-density`.
- [x] Implement CLI/tests/docs for `cube-arith --operation spin-density`
  without changing the existing generic `density-difference` behavior:
  `spin-density` uses `--plus-cube` alpha/spin-up density minus
  `--minus-cube` beta/spin-down density, and `--preset auto` routes the
  product to `cube-preset spin-density`.
- [x] Add focused tests for operation term construction, default
  `spin-density` VESTA preset selection, generated signed `ISURF` defaults,
  command-line execution, and interactive CLI argument construction; focused
  `tests.test_cube_arith` and `tests.test_cli` passed.
- [x] Update README, Chinese usage docs, worklog, skills, and the ABACUS
  analysis matrix with the new alpha/beta cube arithmetic route.
- [x] Sync root docs, validate, and review: root docs mirror is clean;
  `py_compile`, focused `tests.test_cube_arith tests.test_cli` with 63 tests,
  full 271-test no-GUI regression, `bin/multiwfn2vesta cube-arith --help`,
  `bin/multiwfn2vesta --help`, `git diff --check`, and read-only subagent
  review all passed.
- [x] Commit and push on `main` with `Stardust0831` identity as
  `1a8bbc63cc785ec07b4b177078909971b8ac127b`; post-push verification showed
  local `main`, `origin/main`, and `origin/HEAD` aligned at that commit with
  only `refs/heads/main` exposed by the remote.  This follow-up records the
  completed push before starting the next increment.

## Current Continuation: 2026-06-10 Gradient-Norm Cube Display

- [x] Record resumed objective: keep expanding maintained VESTA-ready
  Multiwfn/ABACUS wavefunction and cube analyses, prioritizing products that
  ABACUS can feed through Molden or direct cube routes.
- [x] Recheck current state: `main` is aligned with `origin/main` at
  `67a6e0f1a69f91b02481f5093477e32632f477de`; untracked local probes
  `domain.cub` and `domain.pdb` remain uncommitted.
- [x] Inspect current `grid-run` and `cube-preset` coverage for real-space
  function `2` gradient norm: `grid-run` already generated `gradient.cub` but
  routed it through generic `density`; Multiwfn 2026.6.2 `0123dim.f90`
  confirms function `2` exports `gradient.cub`, and `define.f90` provides the
  global default `sur_value=0.05D0`.
- [x] Implement tests/docs for the new preset/function mapping without
  changing existing density or signed presets: added `cube-preset
  gradient-norm`, mapped `grid-run --function gradient` to it, and focused
  `py_compile` plus `tests.test_cube_preset tests.test_multiwfn_grid` passed
  with 57 tests, including a fake Multiwfn integration-style run that writes
  `gradient.cub` and verifies the generated recipe/VESTA manifest uses
  `gradient-norm`.
- [x] Sync root docs, validate, and review: focused `py_compile` passed;
  focused `tests.test_cube_preset tests.test_multiwfn_grid` passed with 57
  tests; full no-GUI regression passed with 273 tests; `cube-preset
  --list-presets`, `grid-run --list-functions`, and `git diff --check`
  passed; read-only subagent review found no blocker, and its suggested
  integration-style gradient run test was added before closeout.  Commit/push
  and post-push branch verification are reported in the assistant response.

## Current Continuation: 2026-06-10 Grid Function Display Presets

- [x] Record resumed objective: keep enriching Multiwfn wavefunction analyses
  that ABACUS can feed through Molden or direct cubes, and express useful
  products in VESTA.
- [x] Inspect current branch state: local `main` is aligned with
  `origin/main`; only untracked local probes `domain.cub` and `domain.pdb`
  are present and must stay uncommitted.
- [x] Re-read the analysis matrix, CLI surface, `grid-run`, and `cube-preset`
  code to choose the next bounded high-value increment.
- [x] Add maintained VESTA display presets for common signed/scalar
  Multiwfn real-space grid functions that currently fall back to generic
  presets: spin density, Laplacian, Hamiltonian kinetic energy density
  `K(r)`, and Lagrangian kinetic energy density `G(r)`.
- [x] Process read-only subagent review: adjust `spin-density` default to
  Multiwfn `0123dim.f90` `sur_value=0.02`, and include adjacent standalone
  single-cube presets for `orbdens.cub`, `RDG.cub`, and `RDGprodens.cub`
  without changing the existing two-cube `rdg -> iri` texture route.
- [x] Add focused tests for preset listing, signed/single surface behavior,
  manifest notes, and `grid-run` function-to-preset resolution; focused
  validation currently passes 30 `cube-preset` tests and 25 `grid-run` tests.
- [x] Finish README/usage/skills/research/worklog sync and final validation:
  `py_compile`, 55 focused tests, full 268-test no-GUI regression,
  `bin/multiwfn2vesta --help`, `cube-preset --list-presets`,
  `grid-run --list-functions`, `git diff --check`, and stale-doc scan.
- [x] Mirror root docs and prepare the stable `main` closeout; final commit
  hash and post-push branch check are reported in the assistant response.

## Current Continuation: 2026-06-10 Multiwfn Analysis Expansion Sweep

- [x] Record resumed objective: keep surveying useful Multiwfn analyses that
  can become VESTA products, prioritizing wavefunction/cube workflows that
  ABACUS can produce directly or through the maintained Molden bridge.
- [x] Re-read the current analysis matrix, CLI surface, and local Multiwfn
  source evidence to choose the next high-value maintainable increment.
- [x] Implement or document the next bounded feature without touching files
  outside `/mnt/g/work/multiwfn2vesta`.
- [x] Add focused tests, update README/usage/skills/worklog, sync root docs,
  run review, and validate the direct ABACUS cube preset increment.
- [x] Prepare the stable `main` increment for commit and push; final commit
  hash and post-push branch check are reported in the assistant response.

## Current Request: 2026-06-10 README Refresh And One-Branch Closeout

- [x] Record user request: update README, inspect the unusual-looking branch
  state, converge work back to one branch if needed, and use
  `Stardust0831` identity.
- [x] Recheck repository state without destructive operations: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `809e2611aa51cd9a37fd5966b6d4e2e4673f9e44`; `git ls-remote --heads
  origin` exposes only `refs/heads/main`.
- [x] Confirm repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Refresh README branch/status wording so the recorded hash is the
  pre-increment branch-audit baseline and not a stale final commit claim.
- [x] Keep the new ABACUS direct cube preset docs and skills in the same
  maintained `main` increment.
- [x] Resync root docs after final metadata edits, then prepare the `main`
  commit/push closeout with final hash reported in the assistant response.

## Active Goal Continuation: 2026-06-10 Multiwfn Analysis Expansion

- [x] Record continuation request: keep researching and implementing useful
  Multiwfn wavefunction analyses that can become VESTA products, especially
  ABACUS-compatible wavefunction/cube workflows.
- [x] Resume the pending aIGM/amIGM feasibility task from local Multiwfn
  source evidence and current IGM/IGMH runner implementation.
- [x] Implement a maintained runner or document the source-level blocker,
  then update tests, README/usage/skills/worklog, and root docs mirror.
- [x] Validate, run review, commit, and push a stable `main` increment if the
  result is maintainable.

## Current Request: 2026-06-10 README Refresh, One-Branch Closeout, And aIGM/amIGM Runner

- [x] Record user request: update README, inspect unusual branch state, converge work back to one branch, and use `Stardust0831` git identity.
- [x] Inspect current branch/remotes and local git identity without destructive operations: local `main`, `origin/main`, and `origin/HEAD` are aligned at `0fd0517`; the remote exposes only `refs/heads/main`; repository-local identity is `Stardust0831 <13862180016@163.com>`.
- [x] Update README to reflect the current CLI/workflows, aIGM/amIGM runner scope, and single-branch status.
- [x] Sync documentation mirror after final doc edits and keep kanban/worklog current.
- [x] Validate docs/tests, review diff, commit, and push to single `main` with `Stardust0831`; final commit hash and post-push branch check are reported in the assistant response.

## Current Continuation: 2026-06-10 aIGM/amIGM Runner Feasibility

- [x] Record the continued long-running objective: keep expanding useful
  Multiwfn wavefunction analyses that can become VESTA products, especially
  ABACUS-compatible Molden workflows.
- [x] Re-read the existing IGM/mIGM/IGMH runner and local Multiwfn weak
  interaction source before deciding whether aIGM/amIGM prompt streams are
  stable enough for a maintained CLI.
- [x] Implement the smallest aIGM/amIGM runner increment as a trajectory
  workflow that reuses `cube-preset aigm`; source evidence shows Multiwfn
  exports `avgdg_inter.cub`, `avgsl2r.cub`, optional `avgRDG.cub`, and
  optional `thermflu.cub`.
- [x] Address read-only review PBC grid risk: the runner now accepts
  `--periodic`/`--nonperiodic`, detects common trajectory cell markers, and
  rejects `--grid-mode points` for periodic input because Multiwfn reads PBC
  option `4` as spacing rather than `NX,NY,NZ`.
- [x] Add focused tests/docs/skill updates and sync project/root docs.
- [x] Validate, review if needed, then commit and push on `main` if stable; final commit hash and post-push branch check are reported in the assistant response.

## Current Request: 2026-06-10 README Refresh, One-Branch Closeout, And Fukui Runner

- [x] Record the user's request before editing: update README, inspect the
  odd-looking branch state, consolidate back to one branch if needed, and keep
  Git identity as `Stardust0831`.
- [x] Recheck repository state without discarding in-progress runner work:
  local `main`, `origin/main`, and `origin/HEAD` are aligned at `e92d98a`,
  and `git ls-remote --heads origin` exposes only `refs/heads/main`.
- [x] Confirm repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Finish focused `fukui-run` CLI tests before documenting the new surface:
  `tests.test_multiwfn_fukui` plus `tests.test_cli` currently pass 52 tests.
- [x] Refresh README and docs so the front page records the current
  single-branch state and the new high-level Fukui/dual-descriptor runner.
- [x] Sync `project/docs/` to the root docs mirror and verify with
  `rsync -ani --checksum docs/ ../docs/`.
- [x] Run code/help validation before mirror sync and review: `py_compile`
  passed, 88 focused tests passed, the full 242-test no-GUI regression
  passed, `bin/multiwfn2vesta --help`,
  `bin/multiwfn2vesta fukui-run --help`,
  `bin/multiwfn2vesta cube-preset --list-presets`, and `git diff --check`
  passed.
- [x] Run read-only subagent review: no blocker.  The non-blocking P2 about
  VESTA failure after cube arithmetic was fixed by preserving cube-only
  output in the top-level recipe while returning nonzero for the VESTA
  failure; the P3 was to write final sync/review status back to this board.
- [x] Commit and push on `main`: `43e00d2` (`Add Multiwfn Fukui runner`).
- [x] Recheck local/remote branch state after push: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at `43e00d2`, and
  `git ls-remote --heads origin` exposes only `refs/heads/main`.

## Current Continuation: 2026-06-10 Fukui/Dual Descriptor Wavefunction Runner

- [x] Record the continued long-running objective: keep expanding
  Multiwfn analyses that can become VESTA products from ABACUS-compatible
  wavefunction or cube data.
- [x] Confirm that existing `grid-run` density generation and `cube-arith`
  operations can be composed into a maintained Fukui/dual-descriptor runner
  without reimplementing cube math.
- [x] Implement the smallest useful high-level runner for finite-system
  charged-state wavefunctions, with explicit periodic/charged-system caveats.
- [x] Add focused tests, CLI wiring, docs, and a skill note.
- [x] Sync project/root docs, validate, run read-only review, then commit and
  push on `main` if stable.

## Current Continuation: 2026-06-10 Basin Analysis VESTA Route Exploration

- [x] Record the continued long-running objective: keep enriching
  Multiwfn analyses that can become VESTA products, especially workflows
  compatible with ABACUS Molden or ABACUS/Multiwfn cube data.
- [x] Re-read the current analysis matrix and local Multiwfn `basin.f90`
  evidence before deciding whether this increment should be a full
  command-stream runner or a safer display/preset layer for existing basin
  cubes.
- [x] Inspect current `cube-vesta`/`cube-preset` capabilities for displaying
  one or more binary basin cubes without depending on VESTA UI automation.
- [x] Implement the smallest useful basin-related increment: `cube-preset
  basin` for individual binary `basinNNNN.cub` files and `cube-preset
  basin-type` for signed `basinsyn.cub`, plus focused preset tests.
- [x] Validate: `py_compile`, 20 focused `cube-preset` tests,
  `cube-preset --list-presets`, full 233-test no-GUI regression, and
  `git diff --check` passed.
- [x] Address read-only review residual risk by rejecting all-index
  `basin.cub` in the binary basin preset.
- [x] Sync project/root docs after the guard update.
- [x] Commit and push on `main` if stable; final commit hash is reported in
  the assistant response.

## Current Request: 2026-06-10 README Refresh And Branch Consolidation After Domain Runner

- [x] Record the user's request before editing: update README, inspect the
  odd-looking branch state, consolidate back to one branch if needed, and keep
  Git identity as `Stardust0831`.
- [x] Fetch/prune and recheck local/remote branches before deciding whether a
  merge-back is required: local `main`, `origin/main`, and `origin/HEAD` are
  aligned at `da7d4b7`, and `git ls-remote --heads origin` exposes only
  `refs/heads/main`.
- [x] Confirm repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Review the in-progress `domain-run` README/docs/code diff so the README
  reflects the actual maintained CLI surface.
- [x] Sync `project/docs/` to the root docs mirror after documentation edits.
- [x] Run validation: `py_compile`, 67 focused tests, 230-test full no-GUI
  regression, top-level help, `domain-run --help`,
  `cube-preset --list-presets`, docs mirror checksum checks, and
  `git diff --check` passed.
- [x] Run read-only review: no blocker; residual risks were limited to keeping
  local `domain.cub`/`domain.pdb` unstaged and Multiwfn menu-version drift.
- [x] Commit and push the feature increment on `main`: `73018ab`
  (`Add Multiwfn domain runner`).
- [x] Run post-push branch check: local `main`, `origin/main`, and
  `origin/HEAD` are aligned at `73018ab`; `git ls-remote --heads origin`
  returns only `refs/heads/main`.
- [x] Prepare README/kanban closeout so the front page records the
  post-domain-run branch state; this docs-only closeout is committed on the
  same `main` branch.

## Current Continuation: 2026-06-10 Domain Analysis Runner From Cube Data

- [x] Continue the broad Multiwfn/ABACUS/VESTA analysis-expansion objective by
  taking the confirmed domain-analysis candidate to a maintained runner.
- [x] Re-read Multiwfn `otherfunc2.f90` evidence: main function `200`,
  subfunction `14`, menu option `3` sets `<`/`>` domain criteria, `-1`
  yields domains from current grid data in memory, `10` exports
  `domain.cub`, and `11` exports `domain.pdb`.
- [x] Implement `multiwfn2vesta domain-run` for existing cube/grid input,
  plus `cube-preset domain`, unified CLI/interactive wiring, and console
  script entries.
- [x] Add focused tests for command streams, output copying, VESTA preset
  chaining, missing-output errors, and CLI dispatch.
- [x] Run real H2O density-cube noGUI smoke:
  `smoke/multiwfn_domain_run_smoke_20260610/h2o_density/`, generating
  `h2o_density_domain.cub`, `h2o_density_domain.pdb`, and
  `h2o_density_domain_cube.vesta`.
- [x] Update README, usage docs, research matrix, skill note, kanban, and
  worklog for the new domain route.
- [x] Sync project/root docs and run final validation.
- [x] Run final read-only review: no blocker.
- [x] Commit and push on `main`: `73018ab` (`Add Multiwfn domain runner`).

## Current Request: 2026-06-10 README Refresh at STM Runner Tip

- [x] Record the user's request before editing: update README, inspect the
  odd-looking branch state, consolidate back to a single branch if needed, and
  keep Git identity as `Stardust0831`.
- [x] Recheck branch state after `git fetch --prune origin`: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at
  `fdf85863ccb01c5783ce912163f1ec4a34060dd7`
  (`Add Multiwfn STM runner`).
- [x] Recheck remote heads: `git ls-remote --heads origin` returns only
  `refs/heads/main`, also at `fdf8586`, so no merge-back is needed in this
  pass.
- [x] Confirm repository-local identity is
  `Stardust0831 <13862180016@163.com>`.
- [x] Refresh `README.md` Repository Status so it records the current
  STM-runner tip rather than stale `bc462e1` branch-audit wording.
- [x] Sync project/root docs, run documentation validation, review, then
  commit and push on `main`: `1493c80` (`Refresh README branch status at STM
  tip`).

## Current Continuation: 2026-06-10 STM/LDOS Runner

- [x] Close the previous README refresh state: commit `bc462e1` was pushed to
  `origin/main`, and post-push branch checks showed only `refs/heads/main`.
- [x] Pick the next roadmap increment from the active goal: implement a
  maintained Multiwfn STM/LDOS constant-current cube runner that can feed
  VESTA.
- [x] Add `stm-run` to the unified CLI, package scripts, and cube preset layer.
- [x] Add focused tests for command-stream generation, output capture, VESTA
  chaining, CLI dispatch, and missing-cube failures.
- [x] Run a real H2O Multiwfn noGUI STM smoke and record the generated
  products.
- [x] Update README, usage docs, skills/worklog/research notes, and sync root
  docs.
- [x] Run validation: `py_compile`, 64 focused STM/preset/CLI tests,
  221-test full no-GUI regression, `stm-run --help`,
  `cube-preset --list-presets`, `git diff --check`, and root-doc checksum
  sync check all passed; optional `--prepare-fermi-temperature 298.15`
  STM smoke also returned 0 and generated `h2o_stm.cub`.
- [x] Run read-only review, then commit and push on `main`: `fdf8586`
  (`Add Multiwfn STM runner`).

## Current Request: 2026-06-10 README Refresh And Branch Consolidation

- [x] Record the user's request before editing: update README, inspect the
  odd-looking branch state, consolidate back to a single branch if needed, and
  keep Git identity as `Stardust0831`.
- [x] Inspect the current branch state: local `main`, `origin/main`, and
  `origin/HEAD` are aligned at `b99d80e`; no extra local or remote feature
  branch is visible, so no merge is currently required.
- [x] Confirm repository identity is `Stardust0831 <13862180016@163.com>`.
- [x] Refresh README so it reflects the current maintained CLI/workflows after
  the recent grid mapped-surface bridge.
- [x] Sync `project/docs/` to the root `docs/` mirror after documentation
  edits.
- [x] Validate documentation/branch state with `git diff --check`,
  `bin/multiwfn2vesta --help`, `rsync -ani --checksum project/docs/ docs/`,
  and post-fetch branch checks.
- [x] Run read-only pre-commit review: no blocker; reviewer confirmed branch
  audit, validation wording, kanban state, and root-doc mirror consistency.
- [x] Commit and push the README/docs update on `main`: `bc462e1`
  (`Refresh README branch status`).

## Current Continuation: 2026-06-10 STM/LDOS Candidate After Grid Surface Bridge

- [x] Record the resumed long-running objective: continue enriching
  ABACUS-compatible Multiwfn wavefunction analyses that can produce VESTA
  visualization products.
- [x] Re-read current project state and Multiwfn STM source prompts before
  choosing the exact implementation boundary.
- [x] Confirm the minimal STM command stream by a manual H2O noGUI probe:
  `300 -> 4 -> 1 -> 4 -> NX,NY,NZ -> 0 -> 2 -> 0 -> -1 -> 0 -> q`
  exports `STM.cub` in constant-current mode.
- [x] Implement the smallest reliable STM/LDOS increment if the prompt stream
  is stable enough, otherwise document the blocker and choose the next
  aligned increment.
- [x] Add tests, docs, and a no-GUI smoke scaled to the implemented boundary.
- [x] Sync project/root docs for the implemented STM/LDOS increment.
- [ ] Review, commit, and push the implemented STM/LDOS increment if stable.

## Current Continuation: 2026-06-10 Multiwfn Analysis Expansion After IGM/mIGM

- [x] Record the resumed long-running objective: continue researching and
  implementing valuable Multiwfn wavefunction analyses that can be visualized
  in VESTA, especially ABACUS-compatible Molden workflows.
- [x] Re-read the current roadmap, maintained CLI surface, and Multiwfn source
  evidence before choosing the next concrete increment.
- [x] Pick one increment that makes the requested end state more true without
  broad unrelated refactors: let `grid-run` use a generated Multiwfn grid cube
  as a texture on a provided density/surface cube through a new
  `--surface-cube` route, covering ESP/ALIE/vdW/sign(lambda2)rho mapped
  surfaces without hand-running `cube-preset`.
- [x] Implement the increment with tests, docs, and a smoke or no-GUI
  validation scaled to the risk: `grid-run --surface-cube` now maps the
  generated grid cube as texture on a provided surface cube, with mapped
  presets for ESP/ALIE/vdW/sign(lambda2)rho and a real H2O ESP mapped-surface
  smoke.
- [x] Validate the increment: `py_compile`, 65 focused grid/CLI tests,
  212-test full no-GUI regression, `git diff --check`, `grid-run --help`,
  `grid-run --list-functions`, and the real H2O ESP mapped-surface smoke
  passed.
- [x] Sync project/root docs and leave the board ready for the next
  continuation.
- [x] Run final read-only pre-commit review: no blockers; noted only that
  external positional unpacking of `MultiwfnGridResult` would see the added
  trailing fields.

## Current Request: 2026-06-10 README and Single-Branch Closure for IGM/mIGM

- [x] Record the user's request before continuing: update README, inspect the
  odd-looking branch state, merge/consolidate back to one branch if needed,
  and keep Git identity as `Stardust0831`.
- [x] Recheck local/remote branch state and repository identity without
  discarding the in-progress IGM/mIGM runner work: local `main`,
  `origin/main`, and `origin/HEAD` are aligned at `440feec`; remote exposes
  only `refs/heads/main`; identity is `Stardust0831 <13862180016@163.com>`.
- [x] Wait for the read-only pre-commit subagent review of the current
  IGM/mIGM diff, then fix real blockers: fixed wrapper `--method` override
  rejection, method-specific VESTA titles, and method-specific error prefixes.
- [x] Finalize README/docs so they describe the actual maintained CLI surface
  and branch state after this increment.
- [x] Run focused/full validation and real smoke checks again after the review
  code changes: `py_compile`, 55 focused tests, 210-test full regression,
  `git diff --check`, top-level/IGMH help, fixed-wrapper help/override checks,
  and real H2O noGUI IGM/mIGM smokes passed under
  `smoke/multiwfn_igm_migm_run_smoke_20260610_review_fix/`.
- [x] Run final read-only pre-commit review after the fixes: no code blocker;
  only root-doc synchronization remained, which is handled before commit.
- [ ] Commit and push on `main` with identity `Stardust0831`; report the final
  commit hash and post-push branch check.

## Current Continuation: 2026-06-10 IGM and mIGM Command Streams

- [x] Record the continued long-running objective: keep expanding maintained
  Multiwfn wavefunction-analysis workflows that can feed VESTA, especially
  ABACUS-compatible Molden routes.
- [x] Choose the next concrete increment from the current roadmap: extend the
  weak-interaction runner beyond standard IGMH to cover Multiwfn IGM and mIGM
  command streams where the source prompts are stable.
- [x] Re-read current `igmh-run`, unified CLI, tests, docs, and local
  Multiwfn `visweak.f90`/`grid.f90` evidence before editing.
- [x] Implement the smallest reliable method-selection extension with focused
  tests, preserving the just-added PBC grid guard.
- [x] Real noGUI H2O smokes passed for `igm-run` and `migm-run`, generating
  `h2o_igm_cube.vesta` and `h2o_migm_cube.vesta`.
- [x] Update README, usage, skill, research, worklog, and root docs with the
  new IGM/mIGM boundary.
- [x] Validate and review after the fixed-method wrapper changes.
- [ ] Commit and push when stable.

## Current Request: 2026-06-10 README and Branch Consolidation After IGMH Runner Draft

- [x] Record the user's request: update README, inspect the unusual branch state, consolidate back to one branch if needed, and keep Git identity as `Stardust0831`.
- [x] Audit current local/remote branch state after fetching/pruning, without discarding the in-progress `igmh-run` work.
- [x] Finish and validate the in-progress IGMH command-stream wrapper if it is already in the worktree, because README should describe the actual maintained CLI surface.
- [x] Refresh README and synchronized docs/work records so repository status, branch guidance, and usage notes are current.
- [x] Real noGUI H2O smoke passed for `igmh-run`, generating `dg_inter.cub`, `sl2r.cub`, optional `dg_intra.cub`/`dg.cub`, and `h2o_igmh_cube.vesta`.
- [x] Read-only pre-commit review found a PBC grid semantics risk; the runner now rejects `--grid-mode points` for Molden `[Cell]` inputs and docs steer periodic workflows to spacing or `pbc-cell`.
- [x] Run focused and full no-GUI validation where feasible, then do a read-only review pass before committing: `py_compile`, 48 focused tests, 203-test full no-GUI regression, `git diff --check`, and `igmh-run --help` passed after the review fix.
- [x] Prepare the stable commit and push on `main` as `Stardust0831`; final commit hash and post-push branch check are reported in the assistant response.

## Current Request: 2026-06-10 IGMH Command-Stream Foundation

- [x] Continue the long-running Multiwfn/ABACUS/VESTA objective after the
  IGMH/aIGM display preset increment.
- [x] Choose the next concrete increment: investigate and implement the first
  maintainable Multiwfn IGM/IGMH command-stream wrapper so ABACUS Molden files
  can produce `dg_inter.cub`/`sl2r.cub` without hand-driving Multiwfn.
- [x] Inspect existing `aim-run`, `iri-run`, and `grid-run` runners plus the
  Multiwfn IGMH source/menu prompts.
- [x] Implement the smallest reliable `igmh-run` workflow with tests and docs,
  then connect its output to `cube-preset igmh` when requested.
- [x] Validate and review the implementation, including the PBC grid guard.
- [x] Prepare the stable commit and push closure; final commit hash and post-push branch check are reported in the assistant response.

## Current Request: 2026-06-10 IGMH/aIGM Cube Presets

- [x] Continue the long-running Multiwfn/ABACUS/VESTA objective by closing the
  IGMH display-layer preset gap.
- [x] Implement `cube-preset` entries for `igmh`/`igm-inter`, `igm-intra`,
  `aigm`, and `aigm-tfi` from bundled Multiwfn VMD defaults.
- [x] Add focused tests, documentation, a dedicated skill note, and a real
  Ag(111)+benzene no-GUI smoke.
- [x] Read-only pre-commit review verified the template defaults and noted
  only that this current board heading needed refreshing.
- [x] Final post-review validation passed: `git diff --check`, `py_compile`,
  52 focused cube/CLI tests, full 192-test no-GUI regression, and
  `cube-preset --list-presets`.
- [x] Prepare the implementation, tests, docs, and new skill file for commit
  and push on `main`; final commit hash is reported in the assistant response.

## Current Request: 2026-06-10 README Branch Cleanup at 8bf115a

- [x] Record the user's request: update README, inspect the confusing branch
  state, merge/consolidate back to one branch if needed, and use identity
  `Stardust0831`.
- [x] Rechecked project branch state before the README cleanup commit after
  `git fetch --prune origin`:
  local `main`, `origin/main`, and `origin/HEAD` all point at
  `8bf115a3fa332e1008c370d48e70e5235e942ac5`
  (`Add surface extrema VESTA overlay`).
- [x] Rechecked remote heads: `git ls-remote --heads origin` returns only
  `refs/heads/main`, so no local or remote feature branch needs merging in
  this pass.
- [x] Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- [x] Refresh README so the Repository Status section records the current
  audited `main` tip, the one-branch remote state, and the future
  merge-back pattern.
- [x] Sync project/root work records with this README and branch audit.
- [x] Validate the docs update and CLI entry point before commit:
  `git diff --check` and `bin/multiwfn2vesta --help` passed.
- [x] Read-only pre-commit review verified the README branch-status claims;
  it also noted that the pre-existing IGMH planning block is unrelated to the
  README cleanup, so the final response should call out that it is board
  planning rather than a README feature change.
- [x] Prepare the docs refresh for commit and push on `main` with identity
  `Stardust0831`; report the final commit hash and post-push branch check in
  the assistant response.

## Current Continuation: 2026-06-10 Multiwfn Analysis Expansion

- [x] Record the resumed long-running objective: research valuable
  Multiwfn wavefunction analyses that can be visualized in VESTA, especially
  routes starting from ABACUS-compatible wavefunction/cube outputs.
- [x] Re-read the current roadmap, maintained CLI surface, and relevant
  Multiwfn source/examples before choosing the next concrete increment.
- [x] Implement one maintained increment that makes the requested final state
  more true, with tests and docs scaled to the change.
- [x] Sync README/usage/skill/research docs plus project/root work records.
- [x] Focused validation passed for the implementation draft: `py_compile`,
  33 tests across `tests.test_cube_preset` and `tests.test_multiwfn_grid`,
  `cube-preset --list-presets`, and `grid-run --list-functions`.
- [x] Real H2O noGUI smokes passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_surface_map_20260610/`:
  `grid-run --function hamiltonian-ked`, `grid-run --function alie`,
  aligned density export, and `cube-preset alie` VESTA generation.
- [x] Read-only pre-commit review found one non-blocking default mismatch:
  `surface-map`/`molsurfmap` originally used isosurface `0.001`.  The main
  thread fixed it to match Multiwfn `molsurfmap.vmd`: isosurface `0.01` and
  texture range `0.0` to `0.002`.
- [x] Final pre-commit validation passed: `py_compile`, 68 focused tests
  across cube/grid/CLI, full 182-test no-GUI regression, `git diff --check`,
  `cube-preset --list-presets`, and `grid-run --list-functions`.
- [x] Prepared this closure record for the final implementation/docs push.
  The final commit hash and post-push branch check are reported in the
  assistant response to avoid an infinite chain of "record the record"
  commits.

## Current Increment: 2026-06-10 IGMH VESTA Preset Foundation

- [x] Record the continued objective: keep enriching VESTA workflows for
  valuable Multiwfn analyses, especially those reachable from ABACUS LCAO
  Molden wavefunction files.
- [x] Choose the next concrete increment: inspect IGMH/IRI/RDG display
  templates and add the smallest maintained VESTA preset foundation before
  attempting full Multiwfn IGMH command-stream automation.
- [x] Resume this increment after the README branch cleanup: implement the
  preset-layer foundation first, then leave full Multiwfn IGMH command-stream
  automation as a later increment.
- [x] Inspect current `cube-preset`, IGMH docs/smokes, and bundled Multiwfn
  VMD scripts for `dg_inter.cub`/`sl2r.cub` display defaults.
- [x] Implement maintained weak-interaction cube presets with focused tests:
  `igmh`/`igm-inter`, `igm-intra`, `aigm`, and `aigm-tfi`.
- [x] Real no-GUI smoke passed on Ag(111)+benzene IGMH cubes under
  `/mnt/g/work/multiwfn2vesta/smoke/igmh_preset_20260610_1128/products/`,
  generating `dg_inter_igmh_cube.vesta` and recipe from `dg_inter.cub` plus
  `sl2r.cub`.
- [x] Sync README/usage/skill/research docs and root work records.
- [x] Validate, review, commit, and push when stable.  Final commit hash is
  reported in the assistant response.

## Current Increment: 2026-06-10 Surface-Map Extrema Overlay

- [x] Record the continued objective: enrich maintained VESTA workflows for
  valuable Multiwfn analyses that can start from ABACUS-compatible
  wavefunction/cube data.
- [x] Choose the next concrete increment: support Multiwfn molecular surface
  extrema from `surfanalysis.pdb` as an optional VESTA overlay for
  density-surface mapped-property workflows.
- [x] Start a read-only sub-agent review for `surfanalysis.pdb` evidence,
  reusable VESTA/AIM code paths, CLI shape, and test risks.
- [x] Inspect current `cube-preset`, `cube-vesta`, AIM PDB, and multi-phase
  VESTA style code locally.
- [x] Implement a maintained parser/overlay command path with focused tests:
  `surface-extrema` standalone patcher and `cube-preset --surfanalysis-pdb`.
- [x] Real CLI smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/surface_extrema_overlay_20260610/`,
  covering `cube-preset surface-map --surfanalysis-pdb` and standalone
  `surface-extrema --selection minima`.
- [x] Update README/usage/skill/research docs and root work records.
- [x] Read-only pre-commit review found no blockers; documentation follow-up
  corrected standalone `--radius` vs `cube-preset --extrema-radius` wording
  and recorded append behavior.
- [x] Final validation passed: `py_compile`, 52 focused tests, full
  189-test no-GUI regression, `git diff --check`, top-level help,
  `cube-preset --help`, and `surface-extrema --help`.
- [x] Prepared this increment for commit and push.  The final commit hash and
  post-push branch check are reported in the assistant response to avoid an
  infinite chain of "record the record" commits.

## Current Request: 2026-06-10 README Refresh at 19bd45d

- [x] Record the user's request: update README, make the branch state less
  confusing, merge back to one branch if needed, and keep commit identity as
  `Stardust0831`.
- [x] Rechecked project branch state after `git fetch --prune origin`:
  local `main`, `origin/main`, and `origin/HEAD` all point at
  `19bd45dfc33f29309c90d408b5672fb137043b9f`
  (`Add surface-map presets and grid functions`).
- [x] Rechecked remote heads: `git ls-remote --heads origin` returns only
  `refs/heads/main`, so no local or remote branch needs merging in this pass.
- [x] Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- [x] Refresh README so the Repository Status section records the current
  audited `main` tip and removes stale branch-audit wording.
- [x] Sync project/root work records with this README and branch audit.
- [x] Validate the docs update and CLI entry point before commit:
  `git diff --check` and `bin/multiwfn2vesta --help` passed.
- [x] Prepare the README refresh for commit and push on `main` with identity
  `Stardust0831`.  The final commit hash and post-push branch check are
  reported in the assistant response to avoid an infinite chain of "record
  the record" commits.

## Current Request: 2026-06-10 README Single-Branch Refresh

- [x] Record the user's request: refresh README, make the branch state easier
  to understand, merge back to one branch if needed, and use identity
  `Stardust0831`.
- [x] Recheck the real project Git state with fetch/prune, branch listing,
  remote-head listing, and repository-local identity.
- [x] Refresh README so the Repository Status section describes the audited
  `main` tip and the one-branch remote state without stale branch-audit
  wording.
- [x] Sync project/root work records with this README and branch audit.
- [x] Validation passed before commit: `git diff --check` and
  `bin/multiwfn2vesta --help`.
- [x] Prepared this closure record for the final README/docs push.  The final
  commit hash and post-push branch check are reported in the assistant
  response to avoid an infinite chain of "record the record" commits.

## Current Request: 2026-06-10 Multiwfn Atom Table Coloring

- [x] Record the continued long-running objective: turn valuable
  Multiwfn/ABACUS wavefunction analyses into maintained VESTA workflows.
- [x] Chosen next concrete increment from the roadmap: a generic Multiwfn
  atom scalar table parser that feeds the maintained VESTA atom-coloring
  backend.  This targets Multiwfn charges, Fukui-like atom contributions,
  orbital/composition atom tables, or hand-normalized atom values exported as
  text/CSV/TSV.
- [x] Inspect the existing `vesta_atom_coloring`, `abacus_mulliken`, unified
  CLI, package metadata, and tests before editing.
- [x] Implement `multiwfn2vesta multiwfn-atom-color` plus parser tests and CLI
  tests.
- [x] Sync README, usage docs, skill notes, research matrix, kanban, and
  worklog.
- [x] Focused validation passed after review fixes: `py_compile`, 45 tests across
  `tests.test_multiwfn_atom_table` and `tests.test_cli`, and
  `multiwfn2vesta multiwfn-atom-color --help`.
- [x] Read-only pre-commit review found and the main thread fixed the
  behavior risks before commit: ambiguous multi-value tables now require
  `--value-column`; `atom-color` remains the historical
  `abacus-mulliken-color` alias; strict keyed tables validate key sets and
  duplicate keys rather than row order.
- [x] Real CLI smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_atom_color_smoke_20260610/`,
  writing `colored_after_review.vesta` and `values_after_review.csv`.
- [x] Full validation passed: 178-test no-GUI regression and
  `git diff --check`.
- [x] Committed and pushed to GitHub `main` as
  `7b305ea5762b3e8444b53338aecec190cc331a7f`
  (`Add Multiwfn atom table coloring`) with repository-local identity
  `Stardust0831 <13862180016@163.com>`.
- [x] Post-push verification after `git fetch --prune origin`: project
  `HEAD`, `origin/main`, and `origin/HEAD` all point at `7b305ea`; the remote
  exposes only `refs/heads/main`; repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- [x] Prepared this closure record for the final docs-only push.  The closure
  commit hash and final branch check are reported in the assistant response to
  avoid an infinite chain of "record the record" commits.

## Current Request: 2026-06-10 README Branch Consolidation Refresh

- [x] Record the user's request: update README, simplify/merge the branch
  state if needed, and use identity `Stardust0831`.
- [x] Rechecked project branch state with `git fetch --prune`,
  `git status --short --branch`, `git branch --all --verbose --no-abbrev`,
  and `git ls-remote --heads origin`.
- [x] Confirmed no merge is needed in this pass: local `main`,
  `origin/main`, and `origin/HEAD` all point at
  `2481cf79c87666503ea8d8186b4b76fba05b2847`, and the GitHub remote exposes
  only `refs/heads/main`.
- [x] Confirmed repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- [x] Refresh README repository-status wording so the current single-branch
  state is clear and old branch-audit details do not read like competing
  active states.
- [x] Sync project/root work records with this branch audit.
- [x] Validated with `git diff --check`, `bin/multiwfn2vesta --help`,
  `git branch --all --verbose --no-abbrev`, `git ls-remote --symref origin
  HEAD`, and `git ls-remote --heads origin`.
- [x] Committed and pushed the README branch consolidation refresh to GitHub
  `main` as `500ffece49c42bcbb4a44d49bcd31044d915bce0`
  (`Refresh README branch consolidation status`).
- [x] Post-push verification after `git fetch --prune origin`: project
  `HEAD`, `origin/main`, and `origin/HEAD` all point at `500ffec`; the remote
  exposes only `refs/heads/main`; repository-local identity remains
  `Stardust0831 <13862180016@163.com>`.
- [x] Prepared this closure record for the final docs-only push.  The closure
  commit hash and final branch check are reported in the assistant response to
  avoid an infinite chain of "record the record" commits.

## Doing

- Continue the long-running objective: research and turn valuable
  Multiwfn wavefunction analyses into maintained VESTA workflows, especially
  routes that can start from ABACUS LCAO Molden files.  The current increment
  implements a generic Multiwfn atom scalar table parser for VESTA atom
  coloring; next likely targets after push are higher-level charged-state cube
  templates, IGMH fragment command streams, specialized raw Multiwfn atom
  transcript parsers, and more real ABACUS Molden smokes.
- Turn the 2026-06-10 Multiwfn/ABACUS/VESTA research into the next
  maintainable features: IGMH command streams, real-system `abacus-molden`
  smoke coverage, Multiwfn atom scalar parsers, and more real IRI/RDG
  templates.  The first maintained IRI/RDG runner now exists as
  `multiwfn2vesta iri-run`.
- Keep non-empty `LBLAT` generation out of maintained code until a GUI-saved
  VESTA diff proves the record syntax; the verified native route now uses
  `LABEL 1` plus site labels.
- Finish the full Ag(111)+benzene IGMH+AIM BCP visibility fix under the user's
  latest three-view constraint: one source `.vesta`, opened once by VESTA,
  then front/right/top images exported by command-line `-rotate_*` and
  `-flush`.  Persistent front/right/top `.vesta` files made by patching
  `SCENE` are compatibility/diagnostic material, not the main workflow.
- Find or build a real non-focus renderer.  Windows minimized/hidden/WSH
  launch routes and the current Linux wrapper are not yet usable.
- Continue improving non-disruptive rendering only after the maintained
  focus-stealing Windows route is documented as explicit/opt-in.

## Done

- Implemented batch `orbital`/`orbital-density` export on top of
  `multiwfn2vesta grid-run`.  Batch mode repeats isolated single-orbital
  Multiwfn main-function-5 runs with one child output directory per orbital
  plus a top-level `multiwfn_grid_batch_recipe.md`.
- `grid-run --orbitals h l l+1` now defaults to `--function orbital` when no
  explicit function is supplied.  `--function orbital-density --orbitals ...`
  exports orbital-density cubes.  `--keep-going` continues after failed
  orbitals; otherwise later orbitals are marked `skipped`.
- Hardened batch argument handling after read-only sub-agent review:
  `--orbitals` rejects `--orbital`, `--commands-file`, `--expected-cube`, and
  `--raw-dir`; `--keep-going` without `--orbitals` is rejected instead of
  being silently ignored.
- Validation for batch orbital export passed: `py_compile` for touched Python
  files, 52 focused tests across `tests.test_multiwfn_grid` and
  `tests.test_cli`, full 163-test no-GUI regression, `grid-run --help`,
  top-level `multiwfn2vesta --help`, and `git diff --check`.
- Committed and pushed batch orbital export to GitHub `main` as
  `dcf7bd3cac0684f48f16ebd06458345b929837fd`
  (`Add batch orbital grid export`).  Post-push verification after
  `git fetch --prune origin`: `HEAD`, `origin/main`, and `origin/HEAD` all
  pointed at `dcf7bd3`; `git ls-remote --heads origin` returned only
  `refs/heads/main`.
- Started `multiwfn2vesta cube-arith`, a maintained compatible-cube linear
  arithmetic workflow for density difference, Fukui functions, and dual
  descriptors.  It supports generic `--term COEFF CUBE` entries and named
  operations `density-difference`, `fukui-plus`, `fukui-minus`, and
  `dual-descriptor`, writes `<stem>.cub` plus a markdown recipe, and
  optionally calls `cube-preset`; `--preset auto` uses `density` for
  `fukui-plus/minus` and `signed` otherwise.
- Integrated `cube-arith` into the unified CLI, aliases `cube-math`,
  `density-diff`, and `fukui-cube`, the interactive menu as item `11`, and
  console script `multiwfn2vesta-cube-arith`.
- Focused validation for the cube arithmetic feature passed: 39
  tests across `tests.test_cube_arith` and `tests.test_cli`, plus
  `py_compile`.
- Real CLI smokes passed under
  `/mnt/g/work/multiwfn2vesta/smoke/cube_arith_smoke_20260610/products_auto_signed/`
  and
  `/mnt/g/work/multiwfn2vesta/smoke/cube_arith_smoke_20260610/products_auto_fukui/`,
  covering auto signed VESTA output and cube-only Fukui output.
- Read-only pre-commit review found and the main thread fixed a real unit
  compatibility issue: `cube-arith` now rejects mixed Bohr/Angstrom cube unit
  conventions by default.
- Full no-GUI regression passed for the cube arithmetic increment: 153 tests
  across the project test suite.
- Committed and pushed the cube arithmetic workflow to GitHub `main` as
  `4123d00ae051a710c954ed3c3712aa8b012c4bc0`
  (`Add cube arithmetic workflow`).  Post-push verification after
  `git fetch --prune origin`: local `main`, `origin/main`, and `origin/HEAD`
  all pointed at `4123d00`; `git ls-remote --heads origin` returned only
  `refs/heads/main`; repository-local identity remained
  `Stardust0831 <13862180016@163.com>`.
- Pushed the first documentation closure as
  `4800cf4b2dbab559d64023852cc3579e7696ad15`
  (`Record cube arithmetic push`).  This docs-only commit preserves the same
  single-branch layout.
- Added `multiwfn2vesta grid-run`, a maintained Multiwfn main-function-5
  (`study3dim`) real-space grid runner.  It discovers Multiwfn, writes the
  exact command stream, stdout/stderr logs, raw cube directory, processed
  `<stem>_<function>.cub`, a markdown recipe, and optionally calls
  `cube-preset`/`cube-vesta` for `.vesta` output.
- `grid-run` currently covers density, gradient, Laplacian, orbital/MO value,
  spin density, nuclear ESP, ELF, LOL, total ESP/MEP, RDG,
  sign(lambda2)rho, Delta-g, IRI, vdW potential, and orbital density.  Orbital
  and orbital-density functions require `--orbital`; unlisted functions can
  be driven with `--function-index` and `--expected-cube`.
- Integrated `grid-run` into the unified CLI, aliases `multiwfn-grid`,
  `scalar-cube-run`, and `function-cube`, the interactive menu as item `10`,
  and console script `multiwfn2vesta-grid-run`.
- Focused unit validation passed for the new runner and CLI entry points: 39
  tests across `tests.test_multiwfn_grid` and `tests.test_cli`.
- Final pre-commit validation passed: `py_compile`, 140-test no-GUI
  regression, `grid-run --list-functions`, `grid-run --help`, top-level
  `multiwfn2vesta --help`, and `git diff --check`.
- Read-only sub-agent review found no blocking issue; the main follow-up
  narrowed the interactive preset prompt to single-cube presets because
  `iri`/`esp` presets require a texture cube.
- Real H2O noGUI density smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_density/products/`.
  Command stream was `5 / 1 / 4 / 12,12,12 / 2 / 0 / q`; Multiwfn returned
  `0`, wrote raw `density.cub`, processed `h2o_density.cub`, and generated
  `h2o_density_density_cube.vesta` plus both recipe files without launching
  VESTA.
- Real H2O noGUI ELF smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_grid_run_smoke_20260610_h2o_elf/products/`
  with `--function elf --no-vesta`, producing raw `ELF.cub`,
  `h2o_elf.cub`, and a recipe.
- Synced README, usage docs, CLI/cube/ABACUS skill notes, new
  `docs/skills/multiwfn_grid_run_skill.md`, and the ABACUS/Multiwfn/VESTA
  research matrix with the maintained `grid-run` workflow.
- Committed and pushed `grid-run` to GitHub `main` as
  `3d192dc7ae9696dd433aae04e1a3bdb488b95482`
  (`Add Multiwfn grid runner`).  After `git fetch --prune`, `HEAD`,
  `origin/main`, and `origin/HEAD` pointed at that commit; the remote exposed
  only `refs/heads/main`, and repository-local identity remained
  `Stardust0831 <13862180016@163.com>`.
- Rechecked the branch state for the user's README/merge-back follow-up:
  local `main` and `origin/main` both point at
  `17667f2a1a7380fb7a2c2495f9df04ef633e0577`, and
  `git ls-remote --heads origin` returns only `refs/heads/main`.  There is
  no feature branch to merge back in this pass.
- Confirmed repository-local commit identity remains
  `Stardust0831 <13862180016@163.com>`.
- Updated README branch-maintenance notes with the current verified commit,
  expected one-branch remote state, maintainer identity commands, and the
  future fast-forward merge pattern for short-lived experiment branches.
- Committed and pushed the README branch follow-up to GitHub `main` as
  `41bfc9ce691b8de195a69566b56ac84df335947b`
  (`Refresh README branch follow-up`).  After push, `HEAD`, `origin/main`,
  and `origin/HEAD` pointed at that commit; the separate
  `src/multiwfn2vesta/multiwfn_grid.py` draft remained untracked and was not
  part of the branch-cleanup commit.
- Rechecked README/branch state for the user's 2026-06-10 cleanup request:
  after `git fetch --prune`, the project has local `main`, `origin/main`,
  and `origin/HEAD -> origin/main`; `git ls-remote --heads origin` reports
  only `refs/heads/main`.  There is no extra local or remote feature branch
  to merge back.
- Updated README repository-status notes so the current branch state is
  explicit: the historical experiment work is already represented as commits
  on `main`, future experiment branches should be short-lived, and
  repository-local commit identity remains
  `Stardust0831 <13862180016@163.com>`.
- Validated the README/docs-only update with `git diff --check` and
  `bin/multiwfn2vesta --help`, committed the README refresh as `dec8150`
  (`Refresh README branch status`), and pushed it to GitHub `main`.
  A final docs-only closure commit may sit after `dec8150`.
- Added `multiwfn2vesta iri-run`, a maintained Multiwfn IRI/RDG command-stream
  wrapper.  It discovers Multiwfn, writes the exact command stream and logs,
  runs in `multiwfn_iri_raw/`, preserves raw `func1.cub`/`func2.cub`, writes
  processed `<stem>_IRI1.cub` and `<stem>_IRI2.cub`, and calls
  `cube-preset iri` to write a mapped-surface `.vesta` unless `--no-vesta`
  is supplied.
- Integrated `iri-run` into the unified CLI, aliases `multiwfn-iri` and
  `rdg-run`, the interactive menu, and console script
  `multiwfn2vesta-iri-run`.
- Hardened `iri-run` failure handling after read-only pre-commit review:
  missing Multiwfn/input paths return a stable CLI error, Multiwfn nonzero
  exits report an `ERROR:` with log paths, and timeouts/launch failures write
  partial logs instead of traceback.
- Smoke-tested real H2O noGUI IRI/RDG under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_iri_run_smoke_20260610/`.
  The run generated raw `func1.cub`/`func2.cub`, processed `h2o_IRI1.cub` and
  `h2o_IRI2.cub`, and wrote `h2o_iri_cube.vesta` plus recipe without
  launching VESTA.
- Synced README, usage docs, IRI/cube/CLI skill notes, ABACUS/Multiwfn
  planning notes, research matrix, and root/project work records with the
  maintained IRI/RDG runner.
- Focused validation passed: 36 tests across `tests.test_multiwfn_iri`,
  `tests.test_cli`, and `tests.test_iri_cube`, plus `py_compile` for
  `multiwfn_iri.py` and `cli.py`.
- Full no-GUI regression passed: 118 tests across Molden checking, ABACUS
  Molden/Mulliken, cube preset, Multiwfn IRI, cube-to-VESTA, unified CLI,
  AIM+IGMH, executable discovery, Multiwfn AIM, IRI cube handling, AIM VESTA
  conversion, and VESTA atom coloring.  `multiwfn2vesta iri-run --help`,
  top-level `multiwfn2vesta --help`, and `git diff --check` also passed.
- Feature implementation commit was pushed to GitHub `main` at
  `16f345c76053454cdca026d707f885383d9122c3`
  (`Add Multiwfn IRI runner`), and `HEAD` matched `origin/main` after
  `git fetch origin main`.
- Added `multiwfn2vesta cube-preset`, a thin analysis-preset layer over the
  maintained `cube-vesta` backend.  Current presets cover density-like scalar
  cubes, signed orbital/wavefunction/density-difference cubes, ELF/LOL cubes,
  IRI/RDG/NCI mapped surfaces, and ESP/MEP mapped density surfaces.
- Integrated `cube-preset` into the unified CLI, interactive menu, aliases
  `preset` and `analysis-cube`, and console script
  `multiwfn2vesta-cube-preset`.
- Synced README, usage docs, cube workflow skill notes, CLI skill notes,
  ABACUS/Multiwfn planning notes, the analysis matrix, root/project kanban,
  and worklogs with the cube preset workflow.
- Smoke-tested the preset wrapper under
  `/mnt/g/work/multiwfn2vesta/smoke/cube_preset_smoke_20260610/`, generating
  a signed orbital-style `.vesta` from the `orbital` alias and an IRI/RDG
  texture-mapped `.vesta` from the `rdg` alias without launching VESTA.
- Validated the cube preset layer with 28 focused unit tests, `py_compile`,
  CLI help/list checks, `git diff --check`, and a 108-test no-GUI regression
  before commit.
- Addressed read-only pre-commit review findings before commit: explicitly
  staged the new implementation/test files, updated package Python metadata
  from `>=3.6` to `>=3.7`, and made `--tex-percent` recipe output record
  explicit percentage scaling instead of implying physical texture scaling.
- Feature implementation commit for cube preset was pushed to GitHub `main` at
  `c58600d3b4f276c43eef4095669b6402835df8ff`
  (`Add cube analysis presets`).
- Added `multiwfn2vesta abacus-molden`, a maintained wrapper around the
  latest ABACUS `interfaces/Multiwfn_interface/molden.py`.  It exports the
  converter from `origin/develop`, records source path/commit/SHA256, runs
  with an absolute `-o`, writes stdout/stderr logs and a markdown recipe, and
  validates successful output with `molden-check --abacus`.
- Hardened `abacus-molden` for real CLI use: the wrapper now preflights
  `numpy`, `scipy`, and `matplotlib` in the selected Python environment,
  supports `--python`, records missing-dependency errors in logs/recipe, treats
  missing output Molden files as failure even with `--no-check`, and writes
  partial logs/recipe on timeout instead of traceback.
- Validated the ABACUS Molden wrapper and README/CLI refresh with a 97-test
  no-GUI regression, `py_compile`, `git diff --check`, CLI help checks, and a
  git-export smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/abacus_molden_wrapper_smoke_20260610/`.
- Read-only pre-commit review checked the current diff; all findings were
  addressed before commit: dependency preflight, timeout handling, smoke
  evidence, test-count update, and CLI alias help consistency.
- Confirmed the branch layout for this README cleanup: project branch `main`
  tracks `origin/main`, repository-local identity is `Stardust0831
  <13862180016@163.com>`, and no extra feature branch is present locally.
- Added `multiwfn2vesta abacus-mulliken-color`, the first maintained
  ABACUS atom-scalar parser/glue workflow.  It parses ABACUS `out_mul 1`
  `mulliken.txt`, selects the last ionic step by default, supports exact
  `--step`, and maps `charge`, `magnetism`, `magnetism-x/y/z`, or
  `magnetism-norm` to VESTA `SITET` colors by one-based atom index.
- Confirmed ABACUS latest `origin/develop` Mulliken output shape from
  documentation, source, and test references: blocks begin with
  `--- Ionic Step N ---`, atom records use `Atom N is LABEL`, scalar totals
  use `total charge on atom N`, and spinful output adds
  `total magnetism on atom N`.  Multi-k output uses the same file structure
  after summing k-point contributions.
- Added tests for ABACUS Mulliken `nspin=1`, `nspin=2`, `nspin=4`, legacy
  documentation format, ionic-step selection, VESTA atom color patching, and
  selected-values CSV export.
- Validated the ABACUS Mulliken coloring workflow with focused parser/CLI
  tests, `py_compile`, and a real CLI smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/abacus_mulliken_color_smoke_20260610/`.
  The smoke colored Fe1 red and Fe2 blue from final-step magnetism
  `+4/-4` and wrote `values.csv`.
- Final pre-commit no-GUI regression for the README/Mulliken update passed:
  87 unit tests across Molden checking, ABACUS Mulliken parsing/coloring,
  cube-to-VESTA, unified CLI, AIM+IGMH, executable discovery, Multiwfn AIM,
  IRI cube handling, AIM VESTA conversion, and generic atom coloring.
- Read-only pre-commit review found and main thread fixed a strict-mode
  blocker: ABACUS Mulliken coloring now verifies that selected VESTA `STRUC`
  site indices exactly match Mulliken atom indices before patching colors, so
  a wrong `.vesta` file or section cannot silently color only a subset.
- Refreshed README for the current single-branch state and maintained CLI:
  after `git fetch --prune`, only local `main` and remote `origin/main` are
  present, with repository-local identity
  `Stardust0831 <13862180016@163.com>`.
- Added signed positive/negative isosurface support to
  `multiwfn2vesta cube-vesta`.  `--surface-mode signed --isosurface X` writes
  both `+abs(X)` and `-abs(X)` `ISURF` entries, defaults to yellow positive
  and blue negative surfaces, rejects zero magnitudes, and checks every level
  against the cube data range.
- Added focused signed-cube tests for the generated VESTA `ISURF` block,
  manifest `surface_mode`/`isosurface_levels`, zero-level rejection, and
  negative-level range validation.
- Updated README, usage docs, cube workflow skill notes, ABACUS/Multiwfn
  planning notes, and the analysis matrix so signed cube output is documented
  as implemented while Multiwfn command streams for generating those cubes
  remain future work.
- Validated the signed cube preset and README/docs refresh with 78 no-GUI
  regression tests, `py_compile`, `git diff --check`, and a real signed cube
  CLI smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_signed_smoke_20260610/`.
  The recipe records `surface_mode: signed` and isosurface levels
  `0.2, -0.2`.
- Checked branch/remote state for the user's README cleanup follow-up:
  `git fetch --prune` and `git ls-remote --heads origin` show only `main`,
  with `origin/HEAD -> origin/main`; there is no extra branch left to merge
  back.
- Confirmed repository-local Git identity remains `Stardust0831
  <13862180016@163.com>`.
- Validated the README/CLI/cube-to-VESTA changes before commit with 73
  no-GUI regression tests, `py_compile`, and `git diff --check`.
- Fixed the pre-commit review blocker where same-basename surface and texture
  cubes from different directories could overwrite each other in the generated
  VESTA dependency directory.
- Added `multiwfn2vesta cube-vesta`, the first generic ABACUS/Multiwfn cube
  to VESTA workflow.  It writes `IMPORT_DENSITY`, optional `IMPORT_TEXTURE`,
  `SECTS 0 0`, `ISURF`, percentage `TEX3P`, a cube-derived structure phase,
  copied cube dependencies, and a markdown recipe without launching VESTA.
- Real H2O-HF cube smoke passed under
  `/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_cli_smoke_20260610/`; output
  includes `h2o_hf_iri_cube.vesta`, copied surface/texture cubes, and a recipe.
- Added surface-band texture scaling to `multiwfn2vesta cube-vesta`.
  `--tex-range-source surface-band` converts `--tex-physical` limits using
  texture values from grid points near the requested isosurface, records the
  reference range/sample count in the recipe, and falls back to nearest grid
  points when the band is empty or degenerate.
- Validated surface-band texture scaling with 75 no-GUI regression tests and a
  real H2O-HF IRI smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/cube_vesta_surface_band_smoke_20260610/`.
  The recipe records `tex_reference_source: surface-band`, reference range
  `-0.04` to `-0.0331239`, and 29 sampled grid points.
- Added `multiwfn2vesta molden-check`, a no-GUI Molden sanity checker.
  Generic mode checks `[Atoms]`, `[GTO]`, and `[MO]`; ABACUS mode also
  requires `[Cell]` and `[Nval]` before Multiwfn wavefunction workflows.
- Real Ag(111)+benzene ABACUS Molden smoke passed with `--abacus`:
  60 atoms, 566 MO blocks, 3 `[Nval]` entries, 3 numeric `[Cell]` rows, and
  `[Nval]` detail `Ag=19, C=4, H=1`.
- Added the Multiwfn/ABACUS/VESTA analysis matrix under
  `docs/research/multiwfn_abacus_vesta_analysis_matrix.md`.  It ranks useful
  Multiwfn wavefunction/grid analyses by VESTA visualization value, ABACUS
  input feasibility, and project priority.
- Added `docs/skills/abacus_multiwfn_vesta_analysis_skill.md` as a reusable
  planning checklist for ABACUS direct-cube routes, latest ABACUS Molden
  generation, `[Nval]` validation, and VESTA representation choice.
- Confirmed ABACUS `develop` moved the Molden converter to
  `interfaces/Multiwfn_interface/molden.py` at commit `19511fd`; latest
  checked `origin/develop` is `707f092`.  The current converter writes
  `[Nval]` by default and restricts the Molden path to LCAO, `nspin=1/2`, and
  Gamma/single-k calculations.
- Refreshed the README repository-status section so the front page explicitly
  says `main` is the maintained branch, `origin` points to
  `Github:Stardust0831/multiwfn2vesta.git`, `origin/HEAD -> origin/main`, and
  commits use repository-local identity
  `Stardust0831 <13862180016@163.com>`.
- Updated the README so the repository front page now documents the maintained
  `multiwfn2vesta` CLI, executable discovery, wavefunction-to-AIM runner,
  AIM PDB conversion, AIM+IGMH overlay workflow, rendering caveats, validation,
  and documentation map.
- Consolidated the branch state: `main` was fast-forwarded to the verified
  `vesta-nofocus-render` work at commit `2c19cd8`, pushed to GitHub, and the
  merged `vesta-nofocus-render` branch was deleted locally and remotely.
- Confirmed commit identity is repository-local `Stardust0831
  <13862180016@163.com>`.
- Added Multiwfn/VESTA executable discovery to the maintained CLI.
  `multiwfn2vesta discover` reports selected and candidate paths from
  environment variables, workspace tools, and `PATH`.
- Added `multiwfn2vesta aim-run <wavefunction> <output_dir>`.  It accepts
  Molden/FCHK/WFN-style inputs, runs Multiwfn AIM in the output directory,
  writes the exact command stream and logs, and converts generated
  `paths.pdb`/`CPs.pdb` into `aim_atoms_only.vesta` by default.
- Real H2O noGUI smoke succeeded under
  `/mnt/g/work/multiwfn2vesta/smoke/multiwfn_aim_cli_smoke_20260610/h2o/`.
  It produced `paths.pdb`, `CPs.pdb`, `CPprop.txt`, `mol.pdb`, logs, and
  `aim_atoms_only.vesta` without launching VESTA.
- Validation completed for the Multiwfn/VESTA discovery and wavefunction AIM
  runner integration: focused no-GUI tests, `py_compile`, CLI help,
  `multiwfn2vesta discover`, real H2O smoke, and `git diff --check`.
- Pushed the Multiwfn/VESTA discovery and wavefunction AIM runner integration
  to GitHub branch `vesta-nofocus-render` at commit `ce0fecb`.
- Added an easier global/interactive CLI entry point.  The user can add only
  `/mnt/g/work/multiwfn2vesta/project/bin` to `PATH`, run `multiwfn2vesta`,
  choose maintained workflows interactively, or call scriptable subcommands
  such as `multiwfn2vesta aim-igmh ...` without manually setting
  `PYTHONPATH`.
- Added `multiwfn2vesta.cli`, `bin/multiwfn2vesta`, editable-install console
  scripts, no-GUI CLI tests, and skill documentation
  `docs/skills/multiwfn2vesta_cli_skill.md`.
- Ran a unified CLI dry smoke without VESTA rendering under
  `/mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/unified_cli_smoke_20260610/`.
- Closed the Ag(111)+benzene AIM+IGMH drawing experience into a reusable
  Python/CLI workflow: `multiwfn2vesta.aim_igmh_vesta`.  It patches AIM
  path/BCP styles with the maintained yellow `Xe` path and orange `Rn` BCP
  defaults, preserves coordinates and structure bonds, splits BCPs into the
  final phase by default, copies relative IGMH cube files beside the product,
  writes a markdown manifest, and calls the one-source/one-session VESTA
  three-view exporter only when explicitly requested.
- Added focused no-GUI tests for the reusable AIM+IGMH workflow in
  `tests/test_aim_igmh_vesta.py`.
- Added skill documentation for the closed-loop reusable workflow:
  `docs/skills/aim_igmh_vesta_skill.md`.
- Ran a non-rendered Ag(111)+benzene dry smoke under
  `/mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/reusable_cli_smoke_20260610/`.
  The output contains a styled `.vesta`, a recipe markdown file, and copied
  `dg_inter.cub`/`sl2r.cub`.
- Updated maintained AIM overlay styling so `Xe` bond-path sample spheres use
  radius `0.0600` Angstrom by default.
- Generated a non-rendered Ag(111)+benzene smoke check file with yellow `Xe`
  path style patched to radius `0.0600` Angstrom:
  `/mnt/g/work/multiwfn2vesta/smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/products/ag111_benzene_igmh_aim_paths_single_xe_yellow_bcp_splitphase_path006_periodic_overlay.vesta`.
- Verified the change with focused unit tests, `py_compile`, and
  `git diff --check`.
- Researched VESTA atom/site labels for BCP numbering and documented the
  current recommendation: use site labels plus VESTA label visibility for
  simple labels, or use post-render image annotation for robust publication
  numbering until non-empty `LBLAT` syntax is reverse-engineered.
- Implemented `--label-bcp-sites` in `multiwfn2vesta.vesta_aim_overlay_style`.
  It preserves coordinates, rewrites BCP labels across `STRUC`, `THERI`, and
  `SITET`, sets the BCP `SITET` label flag to `1`, and uses `LABEL 1` for
  site-name labels.
- Real-rendered BCP text diagnostics under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_text_label_experiment_20260610/`.
  `LABEL 1` displays `BCP1`/`BCP2`/`BCP3`; `LABEL 0` displays `Rn`.  Native
  labels work but can overlap for nearby BCPs.
- IRI color cube processing notes and skill were added in earlier work.
- AIM path/CP VESTA conversion and style patching were added in earlier work.
- Added experimental minimized Windows VESTA renderer:
  `scripts/render_vesta_nofocus.py`.
- Added `docs/vesta_nofocus_rendering.md` with the 2026-06-08 Ag(111)+benzene
  retest result and PowerShell quoting pitfall.
- Added `scripts/add_single_view_compass.py` for one VESTA-like lower-left
  compass after PNG export.
- Updated `docs/skills/vesta_camera_and_layers_skill.md` with the current
  `COMPS 0` plus post-render single-compass workflow.
- User confirmed the minimized Windows VESTA wrapper still steals focus; it is
  not a no-disruption renderer.
- Fixed the post-render compass arrowhead geometry so arrowheads no longer
  appear reversed.
- Reworked `scripts/vesta_three_views.py` so default `cli-rotate` mode starts
  from one `.vesta`, prepares at most one render input for `COMPS 0` and
  relative cube colocation, opens that input once in VESTA, and exports
  front/right/top PNGs by command-line `-rotate_*`, `-flush`, and
  `-export_img`.  The old `SCENE`-copy path is retained only as
  `--mode scene-copies`.
- Recorded AIM overlay style guidance: use one pseudo-element for path sample
  points and tune path/BCP radii before drawing AIM bonds.
- Added `multiwfn2vesta.vesta_aim_overlay_style` for post-processing
  multi-phase AIM overlays.  It keeps all path sample points, maps path samples
  to a single pseudo-element such as `Xe`, maps BCPs to a distinct
  pseudo-element such as `Rn`, clears AIM `SBOND`, and preserves global
  structure bonds by default.
- Real-rendered BCP visibility diagnostics with VESTA after explicit user
  request.  BCP-only front/right/top PNGs were generated under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_render_20260609/`,
  and a zoomed front diagnostic was generated under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/bcp_points_only_zoom_render_20260609/`.
  Visual inspection confirms three orange BCP points are displayed.
- Tested whether BCP visibility depends on VESTA atom naming or element
  symbols.  BCP-only controls using `N+CP000*_N`, `N+BCP*`, `Rn+CP*_N`,
  `Rn+RBCP*`, `Xe+CP*_N`, `C+CP*_N`, and `He+CP*_N` all rendered visible
  points.  The full-overlay BCP issue is therefore not explained by the
  `CP000*_N` label pattern or the tested element symbols.
- Added `--split-bcp-phase` to `multiwfn2vesta.vesta_aim_overlay_style`.  It
  keeps all AIM path samples, clears AIM-phase bonds, moves BCPs into a final
  dedicated phase, and is idempotent for already-split files.
- Real-rendered the final Ag(111)+benzene IGMH+AIM split-BCP three views under
  `smoke/ag111_benzene_igmh_aim_periodic_cell_20260607/three_views_cli_rotate_split_bcp_final_20260609/`.
  The output contains one `*_render_input.vesta`, the relative cube files, and
  three PNGs; it does not contain three view-specific `.vesta` files.
- Verified the final PNGs are valid `6096 x 3052` images and BCPs are visible
  in all views by orange-pixel counts: front `478`, right `363`, top `138`.
  The top view uses `--extra-rotate top x -8` as a temporary camera tilt before
  export, then undoes it; no BCP/path coordinates are moved.

## Next

- Try a non-activating launcher path or isolate rendering in a different
  desktop/session before using VESTA automation while the user is active.
- Add tests for `scripts/vesta_three_views.py` once script-level tests are
  organized for project utilities.
- If continuing Linux VESTA, add missing GUI libraries inside the workspace
  rather than modifying system packages.
- If the user asks for fresh PNGs, either run an explicitly accepted
  focus-stealing VESTA CLI export or continue the Linux/local-library
  non-focus route first.
## Active Goal: 2026-06-12 Close Existing Features With Examples, Figures, and Chinese Manual

- **User request:** Close the currently implemented feature set into reusable workflows, prepare valuable real-system examples for every maintained feature, improve CLI/user experience, write a Chinese manual, and render effect figures for the examples.
- **Scope guard:** All edits and generated artifacts stay under `/mnt/g/work/multiwfn2vesta`; preserve user files and avoid system-level changes.
- **Immediate plan:**
  - [x] Inventory maintained CLI/features and current examples. Current ready formal examples are Ag(111)+benzene IGMH+AIM, GC AIM, and Cd/Cl trajectory video; several other workflows have smoke/cube evidence but not hand-manual figures.
  - [x] Map each feature to at least one valuable chemistry/materials example. Added `docs/feature_examples_zh.md` and `multiwfn2vesta examples --coverage` / `--needs-render`.
  - [x] Fill missing examples with runnable smoke data or documented commands. Current pass records recommended systems and commands; workflows without real renders remain explicitly `needs-render` or `needs-example`.
  - [x] Render or regenerate representative effect figures where local assets/tools allow. Generated `docs/assets/gallery/current_feature_overview.png` from existing real VESTA-rendered PNG assets without launching VESTA.
  - [x] Improve rough UX surfaces found during example closure. Added feature-centric example discovery and top-level help examples.
  - [x] Expand Chinese manual and keep docs mirrored.
  - [x] Verify tests/examples and commit/push after review. Focused examples/CLI tests, full no-GUI regression, Markdown links, image check, `examples --verify`, `git diff --check`, and docs mirror dry-run passed; commit/push details are recorded in the final response.

## Active Goal Continuation: 2026-06-12 Next ABACUS-Compatible Multiwfn/VESTA Route

- **User request:** Continue surveying valuable Multiwfn wavefunction analyses that VESTA can visualize, especially routes fed by ABACUS LCAO Molden files, and keep enriching the project rather than stopping at example closure.
- **Scope guard:** Keep all edits under `/mnt/g/work/multiwfn2vesta`; preserve local untracked probe files such as `domain.cub` / `domain.pdb`; avoid system-level changes.
- **Immediate plan:**
  - [x] Record this continuation in the kanban before implementation.
  - [x] Recheck branch/worktree, current `grid-run`/`cube-preset` coverage, and local Multiwfn source evidence. Current branch started aligned with `origin/main`; only `docs/kanban.md` and untracked `domain.cub` / `domain.pdb` were present before this increment.
  - [x] Select one bounded source-backed route that is chemically useful, ABACUS Molden compatible, and VESTA friendly. Selected `electron-esp`: local Multiwfn `function.f90` maps function-100 `iuserfunc=14` to `eleesp(x,y,z)`, and function-100 exports `userfunc.cub`.
  - [x] Implement code, tests, docs, skill/worklog/status notes, mirror docs, validate, then commit and push with `Stardust0831` identity. Code and focused tests now cover `grid-run --function electron-esp` and `cube-preset electron-esp`; full no-GUI regression, Markdown link check, CLI route discovery, and `git diff --check` passed. Final commit/push details are reported in the assistant response.

## Active Goal Continuation: 2026-06-12 RoSE/SEDD Scalar Route Increment

- **User request:** Continue enriching ABACUS-compatible Multiwfn wavefunction analyses that can be rendered in VESTA.
- **Scope guard:** Keep edits under `/mnt/g/work/multiwfn2vesta`; preserve untracked `domain.cub` / `domain.pdb`; do not modify system files.
- **Immediate plan:**
  - [x] Record this continuation in the kanban before implementation.
  - [x] Recheck branch/worktree and source evidence for RoSE (`iuserfunc=18`) and SEDD (`iuserfunc=19`).  Local Multiwfn source maps function-100 `iuserfunc=18/19` to RoSE and SEDD, exported as `userfunc.cub`.
  - [x] Add named `grid-run` routes and VESTA presets with focused tests.  Current focused test set passes after using a fake cube whose range covers the default `0.5` isosurface.
  - [ ] Update docs/skills/research/worklog/status notes, mirror docs, validate, commit, and push with `Stardust0831` identity.  Documentation is being synchronized with the broader feature-closure audit; full validation is still pending.

## Active Diagnostic: 2026-06-22 ABACUS PW/GPU Multi-Rank Trust Boundary

- **User request:** Explain why the current server ABACUS `v3.11.0-beta.4`
  PW/GPU multi-MPI-rank path is not trustworthy, and inspect source for the
  likely failure point.
- **Current status:** [x] Empirical H2 probe shows GPU/default `np=1`
  integrates `chg.cube` to about `1.99999 e`, but GPU/default `np=8`
  integrates to about `0.24513 e` and also changes total energy.  CPU-only
  controls integrate to about `1.99999 e` for both `np=1` and `np=8`.
- **Source finding:** [x] ABACUS GPU PW FFT code in
  `source_basis/module_pw/pw_transform_gpu.cpp` and
  `source_basis/module_pw/pw_transform_k.cpp` asserts
  `poolnproc == 1` before full 3D FFT calls.  Density construction in
  `source_estate/elecstate_pw.cpp::rhoBandK()` reaches this GPU transform
  through `basis->recip_to_real(...)`.
- **Interpretation:** [x] The likely bug class is an unsupported multi-rank
  GPU/PW FFT path running silently when release builds disable `assert`, not a
  VESTA/cube post-processing bug.
- **Next:** [ ] Treat COF ESP direct cube images from GPU `np=8` as diagnostic
  only.  Production density/potential cubes should be regenerated with
  `device cpu`, validated single-rank GPU, LCAO, or another ABACUS build after
  a tiny electron-count regression passes.

## Active Diagnostic: 2026-06-24 ABACUS LCAO/PW Parallel Probe

- **User request:** Determine whether the PW/GPU multi-rank issue also affects
  LCAO, explain CPU PW parallelism, compare current `v3.11.0-beta.4` and LTS
  LCAO/PW behavior, and outline a fix direction.
- **Current status:** [x] Ran a remote H2 Gamma-only probe in
  `SAI-saiuser01:~/multiwfn2vesta_runs/abacus_parallel_probe_20260624`; local
  inputs are in `smoke/abacus_parallel_probe_20260624_inputs/`, results in
  `smoke/abacus_parallel_probe_20260624_results/`.
- **Results:** [x] `abacus/LTSv3.10.1-sm70-auto` LCAO/GPU is consistent for
  `np=1` and `np=8`: charge cube integrals are both `~1.9999964 e`, and final
  energies agree.  LTS PW/GPU `np=8` does not silently corrupt density; it
  aborts with `nks == 0, some processor have no k point!`.
- **Results:** [x] `abacus/v3.11.0-beta4-sm70-avx512` LCAO fails in this
  server module for both `device gpu` and `device cpu`: `np=1` reports
  `Integer overflow in xmallocarray`; `np=8` segfaults in the ELPA stack.  This
  appears separate from the PW/GPU k-pool dilution bug.
- **Interpretation:** [x] LCAO is not hit by the specific PW/GPU automatic
  `kpar=NPROC/bndpar` path; current source stores LCAO k parallelism in
  `kpar_lcao` and resets the main `kpar` to 1.  CPU PW supports pool-internal
  multi-rank FFT via distributed gather/scatter, while GPU PW currently asserts
  `poolnproc == 1`.
- **Fix direction:** [ ] Upstream should reject or cap invalid `kpar > nks`
  before pool construction, refuse Gamma-only GPU/PW multi-rank when
  distributed GPU FFT is unavailable, and eventually implement true multi-GPU
  intra-k-point FFT/grid parallelism.

## Active Diagnostic: 2026-06-24 H2O PW/GPU Two-Rank Reproducer

- **User request:** Prepare a more realistic single-H2O, vacuum-box, two-GPU
  Gamma-only reproducer to explain why PW/GPU cannot use k-point parallelism
  for Gamma-only systems, and advise whether to file an issue or PR.
- **Current status:** [x] Ran
  `SAI-saiuser01:~/multiwfn2vesta_runs/h2o_pw_gpu_2rank_probe_20260624` with
  `abacus/v3.11.0-beta4-sm70-avx512`; local inputs are in
  `smoke/abacus_h2o_pw_gpu_2rank_probe_20260624_inputs/`, results in
  `smoke/abacus_h2o_pw_gpu_2rank_probe_20260624_results/`.
- **Result:** [x] Single-rank PW/GPU is numerically sane for this H2O box:
  `chg.cube` integrates to `7.999953955320376 e` versus expected `8 e`, final
  energy `-460.6065895528702 eV`.
- **Result:** [x] Two-rank/two-GPU PW/GPU aborts with `nks == 0, some
  processor have no k points!`; no charge cube is written.  This is a compact
  reproducer for invalid `kpar > nks` in Gamma-only PW/GPU.
- **Recommendation:** [ ] File an upstream issue first with the H2O reproducer
  and the earlier H2 silent bad-cube evidence.  A minimal PR can then add a
  fail-fast guard; true distributed GPU FFT is a larger feature PR.

## Active Diagnostic: 2026-06-24 ABACUS LCAO/GPU Native ELPA Two-Card Probe

- **User request:** Try native `ks_solver elpa` for Gamma-only LCAO/GPU on two
  GPUs, preferably on `4v100pxn07`, which currently appears to have two idle
  V100 cards.
- **Current status:** [x] Submitted Slurm job `560212` in
  `SAI-saiuser01:~/multiwfn2vesta_runs/abacus_v311_lcao_gpu_elpa_2gpu_20260624`.
  Slurm accepted `--nodelist=4v100pxn07` with `--gres=gpu:2`; both `np=2` and
  `np=8` cases have finished.
- **Checkpoints:** [x] Confirmed `np=2` and `np=8` both finish with
  `abacus_rc=0`; ABACUS reports `GPU / Tesla V100-SXM2-16GB (x2)` on
  `4v100pxn07`.  Final energies agree within `~6.6e-5 eV`.  For this small
  `NBASE=744` probe, `np=8` is slower (`elpa_solve=11.14 s`) than `np=2`
  (`1.12 s`), so larger-basis scaling is still untested.
- **Clarification:** [ ] Explain why LCAO native ELPA can use two GPUs while
  earlier Gamma-only PW/GPU H2O/H2 tests either abort or produce bad charge
  cubes depending on whether `device gpu` is explicitly parsed early enough.
- **Clarification:** [ ] Clarify whether PW can use ELPA-style distributed
  diagonalization and why that does not solve the PW/GPU Gamma-only multi-rank
  FFT/grid problem.

## Active Workflow: 2026-06-25 COF ESP vdW Surface Rendering

- **User request:** Based on the current COF system, process ESP for a
  density-isosurface electrostatic-potential coloring workflow.
- **Current status:** [x] Rechecked existing COF LCAO/GPU direct cubes.  The
  density cube integrates to `233.99939580839157 e` versus expected `234 e`.
  The z-vacuum plateaus are stable (`~0.035137`), so a high-z 10% vacuum
  offset was subtracted from `ElecStaticPot.cube`.
- **Outputs:** [x] Generated
  `smoke/cof_esp_vdw_surface_20260625/products/ElecStaticPot_vacuum0_high10.cube`,
  VESTA scene
  `products/esp_vdw_surface/cof12000n2_esp_vdw_surface_cube.vesta`, and a
  data diagnostic PNG
  `products/cof12000n2_esp_vdw_surface_topview_diagnostic.png`.
- **Guardrails:** [x] All files stayed under `/mnt/g/work/multiwfn2vesta`;
  used the reliable LCAO/GPU density/ESP cubes, not the known-risk PW/GPU
  multi-rank cube path.
- **Render note:** [x] Initial Windows VESTA CLI/no-focus export produced
  invalid `60 x 60` icon-like PNGs.  Retrying with multiple `-flush` commands
  after `-open` produced valid `2432 x 1420` PNGs.  VESTA still exits with
  return code `255`, so output dimensions must be checked.
- **Retry:** [x] Valid renders:
  `products/cof12000n2_esp_vdw_surface_vesta_retry_flush2.png` and zoomed
  `products/cof12000n2_esp_vdw_surface_vesta_zoom_flush.png`.
- **User-adjusted style:** [x] Preserve the manually edited
  `cof12000n2_esp_vdw_surface_zoom_render.vesta`, verify/reconstruct its
  physical ESP texture limits from VESTA `TEX3P` percentages, support the
  requested `-0.08..0.08 a.u.` color scale, and ensure structure bonds are
  visible in the rendered scene.
- **User-adjusted style result:** [x] Preserved the user-edited file and added
  derived `cof12000n2_esp_vdw_surface_zoom_render_bonds.vesta` with C/H/N/O
  `SBOND` rules.  Rendered
  `products/cof12000n2_esp_vdw_surface_vesta_zoom_bonds.png`; bonds are
  visible.  `TEX3P -1 0.0209774 1.04690` plus known `-0.08..0.08 a.u.`
  implies texture reference `-0.0832715762378..0.0726856080566`.

## Active Workflow: 2026-06-25 ESP Runbook Closure

- **User request:** Treat the COF ESP workflow as mostly closed and distill the
  reusable experience.
- **Current status:** [ ] Convert the successful COF density-surface ESP
  workflow into a reusable skill/runbook, including vacuum alignment, VESTA
  `TEX3P` percentage inversion, delayed `-flush` image export, and bond
  display via `SBOND`.
- **Result:** [x] Added reusable skill
  `docs/skills/abacus_esp_vdw_surface_vesta_skill.md` and mirrored it under
  `project/docs/skills/`.  The skill records density-integral checks, vacuum
  ESP alignment, VESTA texture scaling, `TEX3P` inversion, `SBOND` bond rules,
  and delayed-flush PNG export.

## Active Workflow: 2026-06-25 ABACUS Molden Multiwfn Excited-State Preparation

- **User request:** Prepare an ABACUS + latest ABACUS `tools/molden.py` +
  Multiwfn electronic-excitation workflow.
- **Current status:** [ ] Inspect current local scripts/docs, fetch/verify the
  latest ABACUS `molden.py` interface expectations, and map the gap between
  ABACUS outputs and Multiwfn excited-state/electron-hole analysis input.
- **Guardrails:** [ ] Keep all local files under `/mnt/g/work/multiwfn2vesta`;
  use clean remote directories only if server calculations become necessary.
