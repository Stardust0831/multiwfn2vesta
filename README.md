# Multiwfn-VESTA Interface

自动化Multiwfn计算和VESTA可视化的Python接口。
项目仍在施工中，非正式版.

## 特性
- 🔄 自动调用Multiwfn计算格点数据
- 🎨 批量VESTA渲染多个视角
- 📁 支持多种输入文件格式
- ⚡ 命令行和Python API两种使用方式

## 快速开始
```bash
git clone https://github.com/yourusername/multiwfn-vesta-interface
cd multiwfn-vesta-interface
pip install -e .

# 使用示例
python -m multiwfn_vesta molecule.fchk
