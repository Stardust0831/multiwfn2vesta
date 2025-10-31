# Multiwfn-VESTA Interface 使用指南

## 安装
```bash
pip install -e .
```

## 基本使用
```bash
# 处理单个文件
python -m multiwfn_vesta molecule.fchk

# 批量处理
python -m multiwfn_vesta *.fchk --batch

# 指定格点类型
python -m multiwfn_vesta molecule.fchk --grid-type spin
```

## 输出
程序会在 `output/` 目录生成：
- 格点文件 (.cube)
- 多个视角的渲染图片 (.png)