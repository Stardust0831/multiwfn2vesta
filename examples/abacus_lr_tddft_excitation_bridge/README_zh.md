# ABACUS LR-TDDFT 到 Multiwfn 电子-空穴桥接算例

状态：H2O-smoke-verified。目录已给出 ABACUS LR-TDDFT 输入样本；真实 H2O
LCAO/Gamma-only smoke 已跑通到 `ABACUS_Multiwfn.molden`、Multiwfn excitation
plain text，并在 Multiwfn 主功能 18 中读入验证。

## 目标

先用小体系 H2O 超胞跑通 ABACUS LR-TDDFT 的输出文件，再把 `Excitation_Energy_*` 和 `Excitation_Amplitude_*` 转为 Multiwfn plain text 激发文件。H2O 不是最终材料体系，只用于确认字段、归一化和轨道编号；后续再迁移到 COF 单层、Ag(111)+benzene 或其它周期体系。

## 文件

- `INPUT.scf`: 先跑普通 LCAO SCF，输出电荷和 LCAO 波函数。
- `INPUT.lr`: LR-TDDFT 输入，关键是 `esolver_type ks-lr` 和 `out_wfc_lr 1`。
- `STRU`: ABACUS 官方 LR-TDDFT H2O 示例的超胞结构。
- `KPT`: Gamma-only。
- `sample_lr/`: 不依赖 ABACUS 的离线最小样例，包含一组
  `Excitation_Energy_singlet.dat`、`Excitation_Amplitude_singlet_0.dat`、
  `INPUT.lr` 以及已生成的 Multiwfn plain text 输出。

## 运行草案

在有完整 ABACUS、PP/ORB 文件和模块环境的目录下：

```bash
cp INPUT.scf INPUT
abacus > scf.log 2>&1

cp INPUT.lr INPUT
abacus > lr.log 2>&1
```

预期输出：

```text
OUT.abacus_h2o_lr/Excitation_Energy_*.dat
OUT.abacus_h2o_lr/Excitation_Amplitude_*_*.dat
OUT.abacus_h2o_lr/running_*.log
```

之后再用最新 ABACUS `tools/molden.py` 生成 Multiwfn 可读 Molden：

```bash
multiwfn2vesta abacus-molden . ABACUS_Multiwfn.molden --with-Nval true
```

## 桥接策略

短期不要伪造 CP2K 输出。当前第一版直接输出 Multiwfn plain text：

```bash
multiwfn2vesta abacus-lr-to-multiwfn OUT.abacus_h2o_lr h2o_singlet.excit.txt \
  --label singlet \
  --coeff-threshold 0.01
```

默认会把 ABACUS LR 振幅乘以 `1/sqrt(2)` 后写出，因为 Multiwfn 对闭壳层
TDDFT 的 hole/electron 分析期望激发系数平方和约为 `0.5`。如果要保留 ABACUS
原始振幅，可显式加 `--coefficient-scale 1.0`，但 Multiwfn 可能给出明显的归一化警告。

Multiwfn plain text 大致形如：

```text
 Excited State     1   1    7.250000
  5 -> 6 0.53
  4 -> 7 -0.18

```

每个 excited state 后的空行不能省略，Multiwfn 用它判断当前态的跃迁列表结束。
这条 plain text 路线适合空穴-电子、NTO 和跃迁密度图，但不携带振子强度；
UV-Vis 谱相关信息应保存在内部 excitation-record，或后续做 Multiwfn 原生
ABACUS parser。

## 离线 sample

仓库内 `sample_lr/` 可直接验证转换格式，不需要真的跑 ABACUS：

```bash
multiwfn2vesta abacus-lr-to-multiwfn \
  examples/abacus_lr_tddft_excitation_bridge/sample_lr \
  examples/abacus_lr_tddft_excitation_bridge/sample_lr/h2o_singlet.excit.txt \
  --label singlet \
  --coeff-threshold 0.05
```

输入文件：

```text
sample_lr/INPUT.lr
sample_lr/OUT.abacus_h2o_lr/Excitation_Energy_singlet.dat
sample_lr/OUT.abacus_h2o_lr/Excitation_Amplitude_singlet_0.dat
```

输出文件：

```text
sample_lr/h2o_singlet.excit.txt
sample_lr/h2o_singlet.excit.txt.recipe.md
```

这个 sample 设置 `nocc=2, nvirt=3`，两条 singlet 激发；能量文件单位按
默认 Ry 转 eV，系数默认乘 `1/sqrt(2)`，并用 `--coeff-threshold 0.05`
丢掉接近 0 的跃迁项。

## 迁移到周期体系

H2O smoke 稳定后，再做：

1. COF 单层或小二维材料超胞，保留足够真空。
2. `abs_gauge velocity`。
3. 先限制 Gamma/single-k，避免多 k 相位和复轨道系数问题。
4. 用 ABACUS Molden 的 `[Cell]`、`[Nval]` 与 LR 振幅文件共同喂给 Multiwfn。

## 风险

- ABACUS LR-TDDFT 文档和源码输出名有漂移，必须以真实 run 的文件为准。
- `Excitation_Amplitude_*` 不写 `nocc/nvirt`；转换器会从 ABACUS LR 日志或输入自动推断，推断失败时再显式传 `--nocc/--nvirt`。
- 当前转换器按 ABACUS 源码 `iocc * nvirt + ivirt` 排序解释单 rank 输出，并默认拒绝多 rank amplitude；多 rank 需要 ABACUS `Parallel_2D` gather 元数据，不能直接拼接。
- 现有 ABACUS Molden 路线主要适合 LCAO、Gamma/single-k、`nspin=1/2`；SOC 和多 k 暂不作为第一阶段目标。
- H2O smoke 中，`nbands=28` 会因 `NLOCAL < NBANDS` 失败；实际验证使用 `nbands=20, nocc=4, nvirt=16`。
- 同一 H2O smoke 的 LCAO/GPU LR 路径在服务器 ABACUS LTS v3.10.1 上触发 `gint_rho_gpu.cu` illegal memory access；已验证路线是显式 `device cpu`。

## 已验证产物

本地真实产物位于：

```text
smoke/abacus_h2o_lr_bridge_20260626/products/
```

关键文件：

```text
ABACUS_Multiwfn.molden
h2o_singlet.excit.txt
h2o_singlet.excit.txt.recipe.md
multiwfn_function18_he_probe.log
```

Multiwfn 验证菜单流：

```text
18
1
h2o_singlet.excit.txt
1
0
0
q
```

验证结果：Multiwfn 将该文件识别为 plain text，读入 5 个 singlet 态；S1 的
系数平方和为 `0.499713`，相对期望 `0.5` 的偏差为 `0.000287`。
