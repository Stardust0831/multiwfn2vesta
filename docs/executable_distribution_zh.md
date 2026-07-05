# multiwfn2vesta 可执行程序说明

本项目的用户入口是数字菜单式 CLI：

```bash
multiwfn2vesta tools interactive --lang zh
```

预发布版会提供三类产物：

- `multiwfn2vesta-linux-x86_64`：Linux x86_64 单文件程序，内置 Python 运行时和本项目依赖。
- `multiwfn2vesta-windows-x86_64.exe`：Windows x86_64 单文件程序，内置 Python 运行时和本项目依赖。
- `multiwfn2vesta-portable-python.zip`：轻量 Python zipapp，要求系统已有 Python 和 `numpy`，适合调试或不能运行 PyInstaller 二进制的环境。

运行示例：

```bash
./multiwfn2vesta-linux-x86_64 tools --lang zh
./multiwfn2vesta-linux-x86_64 tools interactive --lang zh
```

Windows PowerShell 示例：

```powershell
.\multiwfn2vesta-windows-x86_64.exe tools --lang zh
.\multiwfn2vesta-windows-x86_64.exe tools interactive --lang zh
```

这个可执行程序只打包 `multiwfn2vesta` 本身；Multiwfn、VESTA、ABACUS、`ffmpeg` 等外部程序仍需要用户自己安装，并通过 `PATH`、`MultiwfnPATH`、`VESTA` 或对应命令行参数提供路径。

当前稳定入口主要用于：

- 查看稳定工具列表和需要的输入/输出文件。
- 通过交互菜单调用已验证工具。
- 生成 `.vesta`、处理 cube、桥接 ABACUS 激发态、处理 AIM/IGMH、轨迹帧/视频辅助脚本等。

如果只是想先看功能，不需要准备输入文件：

```bash
./multiwfn2vesta-linux-x86_64 tools --lang zh
```
