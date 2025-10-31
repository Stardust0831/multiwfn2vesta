import os
import re
import subprocess
from pathlib import Path

# 更面向对象的实现方式
class QuantumFileProcessor:
    def __init__(self, nprocs: int = 4, maxcore: int = 1000):
        self.nprocs = nprocs
        self.maxcore = maxcore
    
    def process_file(self, inf: str, file_extension: str = "log") -> bool:
        """处理单个文件"""
        print(f"Getting the structure from {inf}")
        
        # 生成输出文件名
        output_file = inf.replace(f'.{file_extension}', '_preopt.inp')
        
        # Multiwfn 输入命令序列
        commands = [
            "oi",                           # 选择 Orbital Information
            output_file,                    # 输出文件名
            "-10",                          # 退出 Orbital Information
            str(self.nprocs),               # 进程数
            str(self.maxcore),              # 内存大小
            "1",                            # 确认并执行
            "q"                             # 退出 Multiwfn
        ]
        
        input_content = "\n".join(commands) + "\n"
        
        # 执行 Multiwfn
        try:
            with open("log.txt", "w") as log_file:
                result = subprocess.run(
                    ["Multiwfn", inf],
                    input=input_content,
                    stdout=log_file,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=300  # 5分钟超时
                )
            
            if result.returncode != 0:
                print(f"Multiwfn 执行失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("错误: Multiwfn 执行超时")
            return False
        except FileNotFoundError:
            print("错误: 找不到 Multiwfn 程序")
            return False
        
        # 修改生成的文件
        return self._modify_output_file(output_file)
    
    def _modify_output_file(self, filename: str) -> bool:
        """修改输出文件内容"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换文本内容
            new_content = content.replace(
                'B97-3c noautostart miniprint', 
                'xtb2 opt'
            )
            
            # 如果内容有变化才写回
            if new_content != content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"已更新文件: {filename}")
            else:
                print(f"文件无需修改: {filename}")
            
            return True
            
        except FileNotFoundError:
            print(f"错误: 找不到文件 {filename}")
            return False
        except Exception as e:
            print(f"修改文件时出错: {e}")
            return False
    
    def process_multiple_files(self, file_pattern: str = "*.log"):
        """批量处理多个文件"""
        import glob
        
        files = glob.glob(file_pattern)
        if not files:
            print(f"找不到匹配的文件: {file_pattern}")
            return
        
        success_count = 0
        for file in files:
            print(f"\n处理文件: {file}")
            if self.process_file(file):
                success_count += 1
        
        print(f"\n处理完成: {success_count}/{len(files)} 个文件成功")


# 使用示例
if __name__ == "__main__":

    processor = QuantumFileProcessor(nprocs=4, maxcore=1000)

    processor.process_multiple_files("*.log")
