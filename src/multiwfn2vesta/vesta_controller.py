import subprocess
from pathlib import Path

class VestaController:
    def __init__(self, vesta_path="vesta.exe"):
        self.vesta_path = Path(vesta_path)
        self.commands = []
    
    def open(self, file_path):
        self.commands.extend(["-open", str(file_path)])
        return self
    
    def export_image(self, output_path, scale=3):
        self.commands.extend(["-export_img", f"scale={scale}", str(output_path)])
        return self
    
    def save(self, output_path):
        self.commands.extend(["-save", str(output_path)])
        return self

    def rotate_x(self, degrees):
        self.commands.extend(["-rotate_x", str(degrees)])
        self.commands.append("-flush")
        return self
    
    def rotate_y(self, degrees):
        self.commands.extend(["-rotate_y", str(degrees)])
        self.commands.append("-flush")
        return self
    
    def rotate_z(self, degrees):
        self.commands.extend(["-rotate_z", str(degrees)])
        self.commands.append("-flush")
        return self

    def close(self):
        self.commands.extend(["-close"])
        return self
    
    def execute(self):
        full_command = [str(self.vesta_path)] + self.commands
        result = subprocess.run(full_command, capture_output=True, text=True)
        self.commands = []
        return result.returncode == 0

if __name__ == "__main__":
    vesta = VestaController("vesta.exe")
    success = (vesta
        .open("GC_IRI.vesta")
        .export_image("test_1.png", scale=3)
        .rotate_x(90)
        .export_image("test_2.png", scale=3)
        .rotate_y(90)
        .export_image("test_3.png", scale=3)
        .execute()
    )

    print(f"执行{'成功' if success else '失败'}")