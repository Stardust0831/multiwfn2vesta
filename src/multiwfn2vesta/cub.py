import numpy as np
from scipy.interpolate import RegularGridInterpolator

class CubeFileInterpolator:
    def __init__(self):
        self.density_data = None
        self.potential_data = None
        self.isodensity_value = 0.001
    
    def read_cube_file(self, filename):
        """读取cub文件"""
        with open(filename, 'r') as f:
            # 读取头两行注释
            comment1 = f.readline().strip()
            comment2 = f.readline().strip()
            
            # 读取原子数和原点坐标
            line = f.readline().split()
            natoms = int(line[0])
            origin = np.array([float(x) for x in line[1:4]])
            
            # 读取网格信息
            grid_info = []
            for i in range(3):
                line = f.readline().split()
                npoints = int(line[0])
                step = np.array([float(x) for x in line[1:4]])
                grid_info.append((npoints, step))
            
            # 读取原子信息
            atoms = []
            for i in range(natoms):
                line = f.readline().split()
                atoms.append({
                    'atomic_number': int(line[0]),
                    'charge': float(line[1]),
                    'coords': np.array([float(x) for x in line[2:5]])
                })
            
            # 读取格点数据
            data = []
            for line in f:
                data.extend([float(x) for x in line.split()])
            
            # 重塑数据为3D数组
            nx, ny, nz = grid_info[0][0], grid_info[1][0], grid_info[2][0]
            expected_points = nx * ny * nz
            
            if len(data) < expected_points:
                print(f"警告: 数据点数({len(data)})少于预期({expected_points})")
                data.extend([0.0] * (expected_points - len(data)))
            elif len(data) > expected_points:
                print(f"警告: 数据点数({len(data)})多于预期({expected_points})，进行截断")
                data = data[:expected_points]
            
            data_array = np.array(data).reshape(nx, ny, nz)
            
            return {
                'comment1': comment1,
                'comment2': comment2,
                'origin': origin,
                'grid_info': grid_info,
                'atoms': atoms,
                'data': data_array,
                'shape': (nx, ny, nz)
            }
    
    def create_grid_coordinates(self, origin, grid_info):
        """创建格点坐标"""
        nx, dx_vector = grid_info[0]
        ny, dy_vector = grid_info[1] 
        nz, dz_vector = grid_info[2]
        
        # 使用向量的主要分量
        dx = dx_vector[0]
        dy = dy_vector[1] 
        dz = dz_vector[2]
        
        x_coords = origin[0] + np.arange(nx) * dx
        y_coords = origin[1] + np.arange(ny) * dy
        z_coords = origin[2] + np.arange(nz) * dz
        
        return x_coords, y_coords, z_coords
    
    def interpolate_potential_to_density_grid(self):
        """将势能数据插值到密度网格上"""
        print("开始势能插值...")
        
        # 创建势能网格坐标
        pot_x, pot_y, pot_z = self.create_grid_coordinates(
            self.potential_data['origin'], 
            self.potential_data['grid_info']
        )
        
        print(f"势能网格: {len(pot_x)} x {len(pot_y)} x {len(pot_z)}")
        print(f"势能数据形状: {self.potential_data['data'].shape}")
        
        # 验证维度匹配
        if (len(pot_x), len(pot_y), len(pot_z)) != self.potential_data['data'].shape:
            print("警告: 势能坐标和数据形状不匹配，尝试转置...")
            # 尝试转置数据
            if (len(pot_y), len(pot_x), len(pot_z)) == self.potential_data['data'].shape:
                self.potential_data['data'] = self.potential_data['data'].T
                print("数据转置完成")
            else:
                raise ValueError("无法匹配势能坐标和数据形状")
        
        # 创建插值器
        try:
            pot_interpolator = RegularGridInterpolator(
                (pot_x, pot_y, pot_z), 
                self.potential_data['data'],
                method='linear',
                bounds_error=False,
                fill_value=0.0
            )
            print("插值器创建成功")
        except Exception as e:
            print(f"创建插值器失败: {e}")
            raise
        
        # 创建密度网格坐标
        dens_x, dens_y, dens_z = self.create_grid_coordinates(
            self.density_data['origin'],
            self.density_data['grid_info']
        )
        
        print(f"密度网格: {len(dens_x)} x {len(dens_y)} x {len(dens_z)}")
        
        # 创建完整的网格点坐标
        xx, yy, zz = np.meshgrid(dens_x, dens_y, dens_z, indexing='ij')
        grid_points = np.stack([xx.ravel(), yy.ravel(), zz.ravel()], axis=1)
        
        print(f"插值点总数: {len(grid_points)}")
        
        # 分批插值以避免内存问题
        batch_size = 100000
        interpolated_values = []
        
        for i in range(0, len(grid_points), batch_size):
            batch_end = min(i + batch_size, len(grid_points))
            batch_points = grid_points[i:batch_end]
            
            batch_interpolated = pot_interpolator(batch_points)
            interpolated_values.append(batch_interpolated)
            
            progress = batch_end / len(grid_points) * 100
            if i % (10 * batch_size) == 0:
                print(f"插值进度: {progress:.1f}%")
        
        # 合并结果
        interpolated_array = np.concatenate(interpolated_values)
        interpolated_array = interpolated_array.reshape(
            len(dens_x), len(dens_y), len(dens_z)
        )
        
        print("插值完成")
        return interpolated_array
    
    def create_isosurface_mask(self, search_radius=0.3):
        """创建等密度表面附近的掩膜"""
        print("创建等密度表面掩膜...")
        
        density_data = self.density_data['data']
        data_shape = density_data.shape
        
        # 创建二进制掩膜
        mask = density_data >= self.isodensity_value
        
        # 使用形态学操作扩展掩膜
        from scipy.ndimage import binary_dilation
        
        # 根据搜索半径确定膨胀次数
        # 假设网格步长约为0.56（根据你的示例数据）
        grid_spacing = 0.56
        dilation_radius = int(np.ceil(search_radius / grid_spacing))
        
        if dilation_radius > 0:
            structure = np.ones((2*dilation_radius+1, 2*dilation_radius+1, 2*dilation_radius+1))
            mask = binary_dilation(mask, structure=structure)
        
        print(f"掩膜创建完成，非零点数: {np.sum(mask)}")
        return mask
    
    def apply_isosurface_mask(self, potential_data, mask):
        """应用等密度表面掩膜"""
        print("应用等密度表面掩膜...")
        
        # 将掩膜外的势能值设为零
        masked_potential = np.where(mask, potential_data, 0.0)
        
        # 统计信息
        total_points = np.prod(potential_data.shape)
        non_zero_points = np.sum(mask)
        efficiency = (1 - non_zero_points / total_points) * 100
        
        print(f"总格点数: {total_points}")
        print(f"非零点数: {non_zero_points}")
        print(f"计算效率提升: {efficiency:.2f}%")
        
        return masked_potential
    
    def write_cube_file(self, data, output_filename, template_data):
        """写入cub格式文件"""
        print(f"写入cub文件: {output_filename}")
        
        with open(output_filename, 'w') as f:
            # 写入注释行
            f.write(template_data['comment1'] + '\n')
            f.write(template_data['comment2'] + '\n')
            
            # 写入原子数和原点坐标
            natoms = len(template_data['atoms'])
            origin = template_data['origin']
            f.write(f"{natoms:5d} {origin[0]:12.6f} {origin[1]:12.6f} {origin[2]:12.6f}\n")
            
            # 写入网格信息
            grid_info = template_data['grid_info']
            for i in range(3):
                npoints = grid_info[i][0]
                step = grid_info[i][1]
                f.write(f"{npoints:5d} {step[0]:12.6f} {step[1]:12.6f} {step[2]:12.6f}\n")
            
            # 写入原子信息
            for atom in template_data['atoms']:
                f.write(f"{atom['atomic_number']:5d} {atom['charge']:12.6f} "
                       f"{atom['coords'][0]:12.6f} {atom['coords'][1]:12.6f} {atom['coords'][2]:12.6f}\n")
            
            # 写入数据
            flat_data = data.flatten()
            count = 0
            for value in flat_data:
                f.write(f" {value:13.5E}")
                count += 1
                if count % 6 == 0:
                    f.write('\n')
            
            # 如果最后一行不满6个，也需要换行
            if count % 6 != 0:
                f.write('\n')
        
        print(f"cub文件写入完成: {output_filename}")
    
    def process(self, density_file, potential_file, output_file, 
                search_radius=0.3, apply_mask=True):
        """主处理函数：将势能插值到密度网格并可选地应用等密度表面掩膜"""
        print("=" * 60)
        print("电子势能cub文件插值处理")
        print("=" * 60)
        
        # 读取文件
        print("1. 读取密度文件...")
        self.density_data = self.read_cube_file(density_file)
        print(f"   密度网格: {self.density_data['shape']}")
        
        print("2. 读取势能文件...")
        self.potential_data = self.read_cube_file(potential_file)
        print(f"   势能网格: {self.potential_data['shape']}")
        
        # 检查网格是否匹配
        density_shape = self.density_data['shape']
        potential_shape = self.potential_data['shape']
        
        if density_shape == potential_shape:
            print("3. 网格匹配，无需插值")
            interpolated_potential = self.potential_data['data']
        else:
            print("3. 网格不匹配，进行插值...")
            interpolated_potential = self.interpolate_potential_to_density_grid()
        
        # 可选：应用等密度表面掩膜
        if apply_mask:
            print("4. 应用等密度表面掩膜...")
            mask = self.create_isosurface_mask(search_radius)
            final_potential = self.apply_isosurface_mask(interpolated_potential, mask)
        else:
            print("4. 跳过掩膜应用...")
            final_potential = interpolated_potential
        
        # 写入结果
        print("5. 写入结果文件...")
        self.write_cube_file(final_potential, output_file, self.density_data)
        
        # 统计信息
        print("\n" + "=" * 60)
        print("处理完成 - 结果统计")
        print("=" * 60)
        print(f"输出文件: {output_file}")
        print(f"势能值范围: [{np.min(final_potential):.6E}, {np.max(final_potential):.6E}]")
        print(f"非零势能点数: {np.sum(final_potential != 0)}")
        
        if apply_mask:
            total_points = np.prod(final_potential.shape)
            non_zero_points = np.sum(final_potential != 0)
            efficiency = (1 - non_zero_points / total_points) * 100
            print(f"计算效率提升: {efficiency:.2f}%")
        
        return final_potential


# 简化使用函数
def interpolate_cube_potential(density_file, potential_file, output_file, 
                              search_radius=0.3, apply_mask=True):
    """简化接口：将势能cub文件插值到密度网格"""
    processor = CubeFileInterpolator()
    
    try:
        result = processor.process(
            density_file, 
            potential_file, 
            output_file,
            search_radius=search_radius,
            apply_mask=apply_mask
        )
        return result
    except Exception as e:
        print(f"处理过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return None


# 使用示例
if __name__ == "__main__":
    # 替换为你的实际文件路径
    density_file = "density.cub"
    potential_file = "esp.cub"
    output_file = "potential_interpolated.cube"
    
    # 执行插值处理
    result = interpolate_cube_potential(
        density_file, 
        potential_file, 
        output_file,
        search_radius=0.3,  # 搜索半径，单位与格点相同
        apply_mask=True     # 是否应用等密度表面掩膜
    )
    
    if result is not None:
        print("处理成功完成!")