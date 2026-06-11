# example 模板

把本模板复制到 `examples/<example_id>/README_zh.md` 后再填写。正式 example
应尽量轻量；大 cube、mp4、完整 smoke 目录不要直接提交，改用 manifest 或
`examples --verify-smoke` 引用本地路径。

## 体系价值

- 体系：
- 对应功能：
- 为什么值得作为示例：
- 不适合说明的问题：

## 输入文件

| 文件 | 来源 | 是否提交 | 备注 |
| --- | --- | --- | --- |
| `input.ext` |  |  |  |

## 推荐命令

```bash
cd /mnt/g/work/multiwfn2vesta/project
export PATH=/mnt/g/work/multiwfn2vesta/project/bin:$PATH

multiwfn2vesta <command> ...
```

## 输出文件

| 文件 | 作用 | 是否应提交 |
| --- | --- | --- |
| `products/*.cub` | 体数据 | 通常不提交 |
| `products/*.vesta` | VESTA 可打开文件 | 小文件可提交；大批量 frame 不提交 |
| `products/*recipe.md` | 复现记录 | 建议提交 |
| `docs/assets/gallery/<example_id>_*.png` | 效果图 | 建议提交精选图 |

## 效果图

把精选 PNG 放到 `docs/assets/gallery/`，并在这里用相对路径引用。模板中先用
普通文本占位，正式 example 再改成真实 markdown 图片链接。

- placeholder: `../../docs/assets/gallery/<example_id>_view.png`

## 验证命令

```bash
multiwfn2vesta examples --id <example_id> --verify
multiwfn2vesta examples --id <example_id> --verify-smoke
```

## 已知问题

- 当前状态：
- 还缺什么：
- 后续可复用建议：
