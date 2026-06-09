# `.vesta` Directive 字段逆向说明草稿

本文档基于 `sj/C.vesta`、`project/docs/vesta_format_notes.md` 和
`project/src/multiwfn2vesta/vesta_parser.py` 整理。它不是 VESTA 官方格式说明，
而是面向工程实现的样例逆向记录：字段含义主要由样例形态、VESTA 可视化功能语义、
以及当前解析器的保留格式策略推断得到。除非标为 `confirmed`，不要把字段解释当作
稳定事实。

置信度约定：

- `confirmed`: 可由样例内容、常见晶体学语义或当前解析器行为直接确认。
- `inferred`: 与 VESTA 功能语义高度吻合，但仍需更多 `.vesta` 样本验证。
- `unknown`: 样例不足，暂时只能描述字段形态。

当前解析器建议的总原则：底层继续将每个 directive 保存为原始 `header_line` 加
`body_lines`，保证 byte-for-byte 往返；高层编辑器只对少数字段建立结构化视图，
并保留未知字段、空白和哨兵行。

## 顶层与晶体结构区

| Directive | 样例位置 | 观察到的字段形态 | 推测含义 | 置信度 | 对解析器的处理建议 |
| --- | --- | --- | --- | --- | --- |
| `CRYSTAL` | `sj/C.vesta:4-5` | 无 header 参数；body 为空行。 | 开始晶体模型数据块。样例中的文件类型/显示上下文为晶体结构。 | inferred | 作为普通 directive 边界保存。暂不假设它包含嵌套范围，因为当前解析器按平铺 section 工作。 |
| `TITLE` | `sj/C.vesta:6-8` | body 第 1 个非空行为 `C`，后接空行。 | 结构标题或数据集名称。 | confirmed | 可提供 `title` 辅助访问器；编辑时保留尾随空行。 |
| `GROUP` | `sj/C.vesta:9-10` | 一行：`186 1 P 63 m c`。整数、选项位、Hermann-Mauguin 符号 token。 | 空间群信息；`186` 对应 `P 63 m c`。第二个整数可能是 setting/origin/choice 标记。 | inferred | 可解析首字段为空间群号，后续 token 作为原样符号和参数数组保存。 |
| `SYMOP` | `sj/C.vesta:11-24` | 12 行对称操作，每行 3 个平移浮点数 + 3x3 整数矩阵 + 末尾整数 `1`；最后一行为 `-1.0 -1.0 -1.0 ...` 哨兵。 | 空间群对称操作列表。前三列为平移，后九列为旋转矩阵，末尾可能为启用/类型标志。哨兵结束列表。 | inferred | 识别为哨兵结束列表；结构化解析时按 `translation[3]`, `matrix[3][3]`, `flag?` 读取，并保留哨兵原文。 |
| `TRANM 0` | `sj/C.vesta:25-26` | header 带整数参数 `0`；body 一行：3 个平移浮点数 + 3x3 矩阵。 | 全局/附加变换矩阵。header 参数可能是变换编号或启用状态。 | inferred | 保留 header 参数；可提供 3+9 数值矩阵解析，但不要改变格式化。 |
| `LTRANSL` | `sj/C.vesta:27-29` | body 第一行为 `-1`；第二行为 6 个 `0.000000`。 | 可能是局部平移/晶格平移限制或交互编辑状态。`-1` 似为未启用/无选择。 | unknown | 原样保存；若后续支持，按固定 2 行读取。 |
| `LORIENT` | `sj/C.vesta:30-33` | 第一行 5 个整数，首值 `-1`；后两行各 6 个浮点数，表现为两个 3D 向量对。 | 可能是局部取向/朝向约束或显示坐标基设置。 | unknown | 原样保存；可校验 3 行形态，但不要解释数值。 |
| `LMATRIX` | `sj/C.vesta:34-39` | 4 行 4x4 单位矩阵；第 5 行 3 个零。 | 局部或视图/对象变换矩阵，末行可能是平移/中心偏移。 | inferred | 可解析为 4x4 矩阵加 3D 向量；修改时保持五行固定格式。 |
| `CELLP` | `sj/C.vesta:40-42` | 第一行 6 个浮点数：`a b c alpha beta gamma`；第二行 6 个零。 | 晶胞参数；第二行可能为标准差/误差或附加 cell 参数。 | confirmed | 这是高价值结构化字段。解析第一行为 cell lengths/angles，第二行原样保留或作为 sigma[6]。 |
| `STRUC` | `sj/C.vesta:43-48` | 每个原子占两行：主行含序号、元素、标签、占位率、分数坐标、Wyckoff 位点、点群/位点对称；续行含 3 个零和末尾 `0.00`；最后 `0 0 0 0 0 0 0` 哨兵。 | 原子/晶体学 site 列表。样例有 `C1` 和 `C2` 两个 carbon site。 | inferred | 识别为哨兵结束列表；结构化读取 atom id、element、label、occupancy、frac coords。续行先作为 site 附加属性保存。 |
| `THERI 1` | `sj/C.vesta:49-52` | header 参数 `1`；每个 site 一行：序号、标签、浮点数；最后 `0 0 0`。 | 热位移/热椭球相关值。样例数值为 `-0.000000`，未显示各向异性矩阵。 | inferred | 作为列表加哨兵保存；不要把单个浮点强行命名为 B/U 值，除非有更多样本确认。 |
| `SHAPE` | `sj/C.vesta:53-54` | 一行 10 个数：4 个整数、一个浮点、一个整数、4 个 RGB/alpha 类整数。 | 全局形状或边界盒/对象外观设置。末 4 个 `192` 像颜色或透明度。 | unknown | 原样保存；可仅做 token 数量检查。 |
| `BOUND` | `sj/C.vesta:55-57` | 第一行 6 个数：`0 1 0 1 0 1`；第二行 5 个整数零。 | 晶胞显示范围或复制范围，三轴 min/max。第二行可能为边界/裁剪选项。 | inferred | 可结构化为 axis ranges；第二行保留为未知 options。 |
| `SBOND` | `sj/C.vesta:58-60` | 一条规则：id、元素1、元素2、最小/最大距离、若干标志、半径/宽度、RGB；最后 `0 0 0 0`。 | 自动成键规则。样例 C-C 距离 `0.00000` 到 `1.89002`，颜色灰色。 | inferred | 作为哨兵列表解析；高层可编辑元素对、距离范围、半径/颜色，其余 flags 原样保存。 |
| `SITET` | `sj/C.vesta:61-64` | 每个 site 一行：序号、标签、半径、两组三元 RGB、alpha/样式整数；最后 `0 0 0 0 0 0`。 | 特定 site 的原子球显示半径、颜色和材质/透明度。2026-06-10 BCP 标签 smoke 中，BCP 行末列设为 `1` 且配合 `LABEL 1` 可显示 `BCP1` 等 site 标签。 | inferred | 与 `STRUC` label 关联；保留未知尾字段。若要显示少数 site 标签，可同步 `STRUC`/`THERI`/`SITET` 标签并把目标 `SITET` 末列设为 `1`。 |
| `VECTR` | `sj/C.vesta:65-66` | 单行 `0 0 0 0 0` 哨兵。 | 矢量对象列表为空。 | inferred | 哨兵列表；支持未来多行矢量记录。 |
| `VECTT` | `sj/C.vesta:67-68` | 单行 `0 0 0 0 0` 哨兵。 | 矢量文本/样式列表为空。 | inferred | 哨兵列表；暂不结构化空列表以外内容。 |
| `SPLAN` | `sj/C.vesta:69-70` | 单行 `0 0 0 0`。 | 晶面/slab/section plane 列表为空。 | inferred | 哨兵列表；未来按 plane records 扩展。 |
| `LBLAT` | `sj/C.vesta:71-72` | 单行 `-1`。 | 原子/site 标签设置列表未启用或为空。VESTA 官方手册确认原子标签可显示元素名或 site 名并带 z 方向偏移；但公开资料和本地样例没有给出可靠的非空 `LBLAT` 记录格式。 | inferred | 保留为哨兵/空列表标记。生成非空记录前必须用 GUI 保存差分验证。 |
| `LBLSP` | `sj/C.vesta:73-74` | 单行 `-1`。 | 空间/平面标签设置列表未启用或为空。 | unknown | 原样保存；仅把 `-1` 视作 terminator candidate。 |
| `DLATM` | `sj/C.vesta:75-76` | 单行 `-1`。 | 删除/隐藏 atom 记录为空，或显示标签 atom delta 列表为空。 | unknown | 原样保存。 |
| `DLBND` | `sj/C.vesta:77-78` | 单行 `-1`。 | 删除/隐藏 bond 记录为空。 | unknown | 原样保存。 |
| `DLPLY` | `sj/C.vesta:79-80` | 单行 `-1`。 | 删除/隐藏 polyhedron 记录为空。 | unknown | 原样保存。 |
| `PLN2D` | `sj/C.vesta:81-82` | 单行 `0 0 0 0`。 | 2D 平面/截面对象列表为空。 | unknown | 原样保存；视作哨兵结束列表。 |
| `ATOMT` | `sj/C.vesta:83-85` | 一条元素类型规则：id、元素、半径、两组三元 RGB、alpha；最后 `0 0 0 0 0 0`。 | 元素级 atom 样式表。与 `SITET` 类似，但按元素而非 site label。 | inferred | 可解析元素、半径、颜色；未知尾字段保留。 |
| `SCENE` | `sj/C.vesta:86-93` | 4 行 4x4 浮点矩阵，后接 2D 偏移、单浮点、单浮点。 | 当前视图/相机场景矩阵、平移/缩放/透视参数。 | inferred | 可结构化读取 4x4 view matrix；额外三行保留命名为 scene parameters，避免强解释。 |
| `HBOND 0 2` | `sj/C.vesta:94-95` | header 两个整数；body 为空行。 | 氢键规则/显示设置。首参数可能为规则数量 `0`；第二参数可能为模式或版本。 | inferred | 解析 header args；body 可为空。不要用 body 行数推断规则数。 |

## `STYLE` 与显示参数区

| Directive | 样例位置 | 观察到的字段形态 | 推测含义 | 置信度 | 对解析器的处理建议 |
| --- | --- | --- | --- | --- | --- |
| `STYLE` | `sj/C.vesta:96` | 无 body，紧跟一批显示相关 directive。 | 显示样式块的起点。 | inferred | 当前按普通 directive 保存；可在高层 outline 中把其后样式 directive 归组显示。 |
| `DISPF 37753794` | `sj/C.vesta:97` | header 单个大整数。 | 显示功能开关位掩码。 | inferred | 保留整数；高层可命名为 bitmask，但不要拆 bit，除非有官方/样本映射。 |
| `MODEL   0  1  0` | `sj/C.vesta:98` | header 3 个整数。 | 结构模型显示模式，如 ball-and-stick/space-filling/polyhedral 等开关组合。 | inferred | 原样保存；可提供整数数组访问器。 |
| `SURFS   0  1  1` | `sj/C.vesta:99` | header 3 个整数。 | surface 显示开关/模式/透明或质量选项。 | unknown | 原样保存。 |
| `SECTS  32  1` | `sj/C.vesta:100` | header 2 个整数。 | section/cut plane 显示参数或位掩码。 | unknown | 原样保存。 |
| `FORMS   0  1` | `sj/C.vesta:101` | header 2 个整数。 | isosurface/form 显示开关或渲染模式。 | unknown | 原样保存。 |
| `ATOMS   0  0  1` | `sj/C.vesta:102` | header 3 个整数。 | atom 显示相关开关。 | inferred | 原样保存；不要与 `STRUC` 混淆。 |
| `BONDS   1` | `sj/C.vesta:103` | header 1 个整数。 | bond 显示开关。 | inferred | 可作为布尔/整数 flag。 |
| `POLYS   1` | `sj/C.vesta:104` | header 1 个整数。 | polyhedron 显示开关。 | inferred | 可作为布尔/整数 flag。 |
| `VECTS 1.000000` | `sj/C.vesta:105` | header 1 个浮点数。 | 矢量显示全局比例或开关值。 | inferred | 保留浮点格式。 |
| `FORMP` | `sj/C.vesta:106-107` | body 一行：`1 1.0 0 0 0`。 | form/isosurface 参数，如显示状态、缩放、flags。 | unknown | 原样保存固定一行。 |
| `ATOMP` | `sj/C.vesta:108-109` | body 一行：`24 24 0 50 2.0 0`。 | atom 绘制参数，如球面细分、边线、比例、质量。 | unknown | 原样保存；字段含义需样本验证。 |
| `BONDP` | `sj/C.vesta:110-111` | body 一行：`1 16 0.250 2.000 127 127 127`。 | bond 渲染参数：模式、分段数、半径/比例、颜色。 | inferred | 可解析末 3 个 RGB 和中间浮点，但保留未知整数。 |
| `POLYP` | `sj/C.vesta:112-113` | body 一行：`204 1 1.000 180 180 180`。 | polyhedron 渲染 alpha/模式/比例/RGB。 | inferred | 可解析颜色；其余字段保留。 |
| `ISURF` | `sj/C.vesta:114-115` | body 一行 4 个整数零。 | isosurface 控制参数，当前无 surface。 | unknown | 原样保存。 |
| `TEX3P` | `sj/C.vesta:116-117` | body 一行：整数 + 两个科学计数浮点。 | 3D texture/volume 参数，可能为启用和 min/max 范围。 | unknown | 原样保存；支持科学计数解析。 |
| `SECTP` | `sj/C.vesta:118-119` | body 一行：整数 + 6 个科学计数浮点。 | section/cut plane 参数，可能含范围和偏移。 | unknown | 原样保存。 |
| `CONTR` | `sj/C.vesta:120-126` | 6 行：第一行混合浮点/整数，第二行 4 整数，后四行各 3 整数零。 | contour/等值线显示参数。第一行可能含间隔、上下限、级数、样式等。 | inferred | 按多行原样保存；若结构化，先只解析数值数组和行数。 |
| `HKLPP` | `sj/C.vesta:127-128` | body 一行：`192 1 1.000 255 0 255`。 | Miller index/hkl plane 绘制参数，含 alpha/模式/比例/RGB。 | inferred | 可解析颜色；未知字段保留。 |
| `UCOLP` | `sj/C.vesta:129-130` | body 一行：`0 1 1.000 0 0 0`。 | unit cell color/线框显示参数。末 3 个为 RGB 黑色。 | inferred | 可解析颜色；保留前 3 字段。 |
| `COMPS 1` | `sj/C.vesta:131` | header 1 个整数。 | component/composition 面板或压缩样式开关。 | unknown | 原样保存 header args。 |
| `LABEL 1    12  1.000 0` | `sj/C.vesta:132` | header 4 个数：整数、字号样整数、比例浮点、整数。 | 全局 atom/site 标签显示样式。2026-06-10 BCP smoke 确认第一字段为标签类型：`1` 显示 site 名，`0` 显示元素名；第二字段控制字号样大小，第三字段影响 z 方向偏移/距离。它不是任意文本内容字段。 | inferred | 可作为 style flag 读取；不要丢失间距。写 BCP 编号时使用 `LABEL 1`，并避免生成未知非空 `LBLAT`。 |
| `PROJT 0  0.962` | `sj/C.vesta:133` | header 整数 + 浮点。 | 投影/相机模式与投影参数；`0` 可能为正交/透视模式，`0.962` 为缩放或视角参数。 | inferred | 原样保存；高层命名为 projection args。 |
| `BKGRC` | `sj/C.vesta:134-135` | body 一行 3 个整数：`255 255 255`。 | 背景 RGB 颜色，样例为白色。 | confirmed | 可结构化为 RGB。 |
| `DPTHQ 1 -0.5000  3.5000` | `sj/C.vesta:136` | header 整数 + 两个浮点。 | depth cue/depth clipping 设置，含启用状态和近/远范围。 | inferred | 保留 header 数值；可按 `enabled`, `min`, `max` 暴露但标注推测。 |
| `LIGHT0 1` | `sj/C.vesta:137-146` | header 参数 `1`；4x4 矩阵，4D 位置，3D 方向，三行 RGBA。 | 第 0 号光源，启用。三行 RGBA 可能为 ambient/diffuse/specular。 | inferred | 可作为 light record 解析：enabled flag、matrix、position、direction、colors[3]。 |
| `LIGHT1` | `sj/C.vesta:147-156` | 无 header 参数；同 `LIGHT0` body，但三行 RGBA 全零。 | 第 1 号光源，可能禁用。 | inferred | 与 `LIGHT0` 共用解析器；header args 可为空。 |
| `LIGHT2` | `sj/C.vesta:157-166` | 同 `LIGHT1`。 | 第 2 号光源，可能禁用。 | inferred | 与 `LIGHT0` 共用解析器。 |
| `LIGHT3` | `sj/C.vesta:167-176` | 同 `LIGHT1`。 | 第 3 号光源，可能禁用。 | inferred | 与 `LIGHT0` 共用解析器。 |
| `SECCL 0` | `sj/C.vesta:177-178` | header `0`；body 为空行。 | section clip/list 数量为 0，或 section color list 为空。 | unknown | 原样保存；允许空 body。 |
| `TEXCL 0` | `sj/C.vesta:179-180` | header `0`；body 为空行。 | texture color/clip/list 数量为 0。 | unknown | 原样保存；允许空 body。 |
| `ATOMM` | `sj/C.vesta:181-183` | body 两行：RGBA `204 204 204 255`，浮点 `25.600`。 | atom 材质参数，颜色/透明度和 shininess 或 specular 强度。 | inferred | 可解析 RGBA + 单浮点材质值。 |
| `BONDM` | `sj/C.vesta:184-186` | body 两行：RGBA `255 255 255 255`，浮点 `128.000`。 | bond 材质参数。 | inferred | 与 `ATOMM` 共用材质解析器。 |
| `POLYM` | `sj/C.vesta:187-189` | body 两行：RGBA + 浮点。 | polyhedron 材质参数。 | inferred | 与 `ATOMM` 共用材质解析器。 |
| `SURFM` | `sj/C.vesta:190-192` | body 两行：RGBA `0 0 0 255`，浮点 `128.000`。 | surface 材质参数。 | inferred | 与 `ATOMM` 共用材质解析器。 |
| `FORMM` | `sj/C.vesta:193-195` | body 两行：RGBA + 浮点。 | form/isosurface 材质参数。 | inferred | 与 `ATOMM` 共用材质解析器。 |
| `HKLPM` | `sj/C.vesta:196-198` | body 两行：RGBA + 浮点。 | hkl plane 材质参数。 | inferred | 与 `ATOMM` 共用材质解析器。 |

## 解析器实现备注

- `DEFAULT_SECTION_NAMES` 已覆盖本样例所有 directive，包括 `LIGHT0` 到 `LIGHT3`。
- `SENTINEL_TERMINATED_SECTIONS` 当前覆盖 `SYMOP`, `STRUC`, `THERI`, `SBOND`,
  `SITET`, `VECTR`, `VECTT`, `SPLAN`, `LBLAT`, `LBLSP`, `DLATM`, `DLBND`,
  `DLPLY`, `PLN2D`, `ATOMT`。这些在样例中确实都以哨兵或空列表标记收尾。
- 不建议在底层 parser 中硬编码所有字段语义。建议新增可选 typed accessors，例如
  `cell_parameters()`, `structure_sites()`, `style_colors()`, `lights()`，并让它们在失败时
  返回解析错误而不是改变原始 section。
- 任何写回逻辑都应优先保持原始字段宽度、科学计数格式、CRLF 换行和空行。

## 仍需更多样本验证的字段

最需要更多 `.vesta` 样本验证的 directive/字段包括：

- `LTRANSL`, `LORIENT`, `LMATRIX`: 局部变换和取向的准确语义、启用标志和行数是否固定。
- `THERI`: header 参数和每行浮点到底对应 isotropic B、U、半径还是热椭球显示参数。
- `SHAPE`: 十个字段的含义，尤其是末尾四个 `192` 是否为 RGBA。
- `BOUND`: 第二行五个整数的含义。
- `SBOND`: 距离后多个 flag 的语义，以及半径/宽度两个浮点的准确区别。
- `SITET` 与 `ATOMT`: 两组 RGB、alpha 和最后 flag 的完整渲染含义。`SITET` 末列配合 `LABEL 1` 可显示目标 site 标签，但它是否还控制其他 GUI 状态仍需更多样本。
- `LBLAT`: atom/site labels 的非空记录形态。VESTA 支持显示元素名或 site 名，但 `.vesta` 写法仍需 GUI 保存差分。
- `LBLSP`, `DLATM`, `DLBND`, `DLPLY`, `PLN2D`: `-1` 或 `0 0 0 0` 之外的非空记录形态。
- `DISPF`, `MODEL`, `SURFS`, `SECTS`, `FORMS`, `ATOMS`: 显示 bit/flag 的映射。
- `FORMP`, `ATOMP`, `BONDP`, `POLYP`, `ISURF`, `TEX3P`, `SECTP`, `CONTR`, `HKLPP`, `UCOLP`:
  样式参数字段顺序和单位。
- `COMPS`, `PROJT`, `DPTHQ`: header 参数的具体 GUI 对应项。`LABEL` 已确认 `0/1` 区分元素名/site 名，但其末字段仍需 GUI 差分。
- `LIGHT0` 到 `LIGHT3`: 三组 RGBA 是否分别为 ambient/diffuse/specular，以及 header 缺省值的含义。
- `SECCL`, `TEXCL`: header 计数与非空列表记录格式。
- `ATOMM`, `BONDM`, `POLYM`, `SURFM`, `FORMM`, `HKLPM`: 第二行浮点是否为 shininess、specular power 或透明/材质强度。
