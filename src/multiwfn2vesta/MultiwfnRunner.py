import subprocess
import os
import logging
import glob
import shutil

class MultiwfnRunner:
    """Multiwfn 运行器"""
    
    def __init__(self, multiwfn_path="Multiwfn"):
        self.multiwfn_path = multiwfn_path
        os.environ['MULTIWFNPATH'] = os.path.dirname(shutil.which('Multiwfn'))
    
    def run_commands(self, input_file, commands, nproc=1):
        """
        运行 Multiwfn 并输入命令
        
        Args:
            input_file: 输入文件路径
            commands: 命令列表，如 ["5", "1", "10", "0"]
        
        Returns:
            bool: 是否成功执行
        """
        # 构建命令行参数
        cmd_args = [self.multiwfn_path, input_file]
        if nproc > 1:
            cmd_args.extend(["-nt", str(nproc)])

        # 构建完整的输入文本（自动添加退出命令）
        input_text = "\n".join(commands + ["q"])
        
        # 执行 Multiwfn
        result = subprocess.run(
            cmd_args,
            input=input_text,
            capture_output=True,
            text=True,
            timeout=None
        )
        
        with open("Multiwfn_out.log", "a", encoding="utf-8") as f:
            f.write(f"\n=== Multiwfn 执行结果 ===\n")
            f.write(f"命令: {' '.join(cmd_args)}\n")
            f.write(f"返回码: {result.returncode}\n")
            if result.stdout:
                f.write(f"输出:\n{result.stdout}\n")
            if result.stderr:
                f.write(f"错误:\n{result.stderr}\n")
        
        return 0

def get_file_basename(filename):
    """获取文件名（最后一个点之前的部分）"""
    return filename.rsplit('.', 1)[0]

def IRI():
    Multiwfn = MultiwfnRunner()
    # 设置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # 查找所有波函数文件（支持多种后缀）
    wavefunction_files = []
    for ext in ['*.fchk', '*.molden.input', '*.fch', '*.molden']:  # 可以添加其他波函数格式
        wavefunction_files.extend(glob.glob(ext))
    
    if not wavefunction_files:
        logging.warning("未找到任何波函数文件 (*.fchk, *.molden.input, *.fch, *.molden)")
        return
    
    logging.info(f"找到 {len(wavefunction_files)} 个波函数文件")
    
    for inf in wavefunction_files:
        basename = get_file_basename(inf)
        logging.info(f"正在处理: {inf}")
        
        # 第一步：产生 func1.cub 和 func2.cub
        commands_step1 = [
            "20",  
            "4",   
            "4",   
            "0.13",
            "3",   
            "2",   
            "0",   
            "0",
            "q"    
        ]
        
        if Multiwfn.run_commands(inf, commands_step1):
            logging.error(f"第一步处理失败: {inf}")
            continue
        
        # 第二步：处理 func1.cub 来等效满足 midpoint 颜色要求并处理上下限
        commands_step2 = [
            "13",
            "11",
            "13",
            "11",
            "7",
            "3",
            "11",
            "2",
            "func1.cub",
            "11",
            "5",
            "1.5",
            "15",
            "-0.1000000E+99,-0.04",
            "-0.04",
            "15",
            "0.04,0.1000000E+99",
            "0.04",
            "0",
            f"{basename}_IRI1.cub", 
            "-1",  
            "q"    
        ]
        
        if Multiwfn.run_commands("func1.cub", commands_step2):
            logging.error(f"第二步处理失败: {inf}")
            # 继续处理，但记录错误
        
        # 清理和重命名文件
        try:
            # 删除 func1.cub
            if os.path.exists("func1.cub"):
                os.remove("func1.cub")
            
            # 重命名 output.txt（强制覆盖）
            if os.path.exists("output.txt"):
                shutil.move("output.txt", f"{basename}_output.txt")

            # 重命名 func2.cub（强制覆盖）
            if os.path.exists("func2.cub"):
                shutil.move("func2.cub", f"{basename}_IRI2.cub")
                
            logging.info(f"完成处理: {inf} -> {basename}_IRI1.cub, {basename}_IRI2.cub")
            
        except OSError as e:
            logging.error(f"文件操作失败: {e}")
    
    logging.info("所有文件处理完成")

if __name__ == "__main__":
    IRI()