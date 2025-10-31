import subprocess
from pathlib import Path

class VestaController:
    def __init__(self, vesta_path="vesta.exe"):
        self.vesta_path = Path(vesta_path)
        self.commands = []
    
    def open(self, file_path):
        self.commands.extend(["-open", str(file_path)])
        return self
    
    def flush(self):
        self.commands.append("-flush")
        return self
    
    def export_image(self, output_path, scale=3):
        self.commands.extend(["-export_img", f"scale={scale}", str(output_path)])
        return self
    
    def rotate_x(self, degrees):
        self.commands.extend(["-rotate_x", str(degrees)])
        return self
    
    def rotate_y(self, degrees):
        self.commands.extend(["-rotate_y", str(degrees)])
        return self
    
    def execute(self):
        full_command = [str(self.vesta_path)] + self.commands
        result = subprocess.run(full_command, capture_output=True, text=True)
        self.commands = []
        return result.returncode == 0

# 使用示例
vesta = VestaController("vesta.exe")
success = (vesta
    .open("FAPbI3.cif")
    .flush()
    .export_image("test_1.png", scale=3)
    .rotate_x(90)
    .flush()
    .export_image("test_2.png", scale=3)
    .rotate_y(90)
    .flush()
    .export_image("test_3.png", scale=3)
    .execute()
)

print(f"执行{'成功' if success else '失败'}")