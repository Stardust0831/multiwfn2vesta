# main.py - 主入口点
import argparse
from pathlib import Path
from multiwfn2vesta import MultiwfnController, VestaController, BatchProcessor

def main():
    parser = argparse.ArgumentParser(description='Multiwfn-VESTA Interface')
    parser.add_argument('input_files', nargs='+', help='Input files for Multiwfn')
    parser.add_argument('--multiwfn-path', default='Multiwfn', help='Path to Multiwfn executable')
    parser.add_argument('--vesta-path', default='vesta', help='Path to VESTA executable')
    parser.add_argument('--config', help='Configuration file')
    args = parser.parse_args()
    
    # 初始化控制器
    multiwfn = MultiwfnController(args.multiwfn_path)
    vesta = VestaController(args.vesta_path)
    processor = BatchProcessor(multiwfn, vesta)
    
    # 处理文件
    processor.process_files(args.input_files)

if __name__ == '__main__':
    main()