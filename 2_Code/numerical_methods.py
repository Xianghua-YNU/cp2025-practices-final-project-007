#############################################################
# 核心算法模块
#############################################################

class MooringSystemSolver:
    def __init__(self, params):
        self.params = params
        
    def calculate_wind_force(self, v, h):
        """计算风荷载"""
        # 确保吃水深度不超过浮标高度
        h = min(h, self.params.buoy_height)
        exposed_area = self.params.buoy_diameter * (self.params.buoy_height - h)
        return 0.625 * exposed_area * v**2
    
    def calculate_buoyancy(self, diameter, h):
        """计算浮力"""
        radius = diameter / 2
        return self.params.rho_water * self.params.g * np.pi * radius**2 * h
    
    def calculate_net_weight(self, mass, volume):
        """计算净湿重"""
        return mass * self.params.g - self.params.rho_water * self.params.g * volume
    
    def calculate_pipe_volume(self):
        """计算钢管体积"""
        return np.pi * (self.params.pipe_diameter/2)**2 * self.params.pipe_length
    
    def calculate_barrel_volume(self):
        """计算钢桶体积"""
        return np.pi * (self.params.barrel_diameter/2)**2 * self.params.barrel_length
    
    def calculate_initial_draft(self):
        """计算静水浮标初始吃水深度"""
        buoy_area = np.pi * (self.params.buoy_diameter/2)**2
        return self.params.buoy_mass / (self.params.rho_water * buoy_area)
    
    def catenary_equation(self, s, a, phi, H, w):
        """
        计算悬链线参数方程
        s: 链条长度参数
        a: 悬链线参数 a = H/w
        phi: 锚点处角度
        H: 水平张力
        w: 单位长度有效重量
        返回: x, z 坐标
        """
        # 锚点处垂直张力
        V_a = H * np.tan(phi)
        
        # 参数方程
        x = a * (np.arcsinh((V_a + w*s)/H) - np.arcsinh(V_a/H))
        z = self.params.water_depth - a * (np.cosh(np.arcsinh((V_a + w*s)/H)) - np.cosh(np.arcsinh(V_a/H)))
        
        return x, z
    
    def find_catenary_parameters(self, P_start, P_end, L, w, H):
        """
        求解满足端点条件的悬链线参数
        P_start: (x_start, z_start) 起点坐标
        P_end: (x_end, z_end) 终点坐标
        L: 链条总长度
        w: 单位长度有效重量
        H: 水平张力
        返回: (a, phi) 悬链线参数和锚点角度
        """
        x_start, z_start = P_start
        x_end, z_end = P_end
        
        # 调整坐标使锚点在原点
        x_span = x_end - x_start
        z_span = z_end - z_start
        
        def objective(params):
            a, phi = params
            
            # 计算链条终点位置
            s_end = L
            V_a = H * np.tan(phi)
            
            # 计算悬链线方程预测的终点位置
            x_pred = a * (np.arcsinh((V_a + w*s_end)/H) - np.arcsinh(V_a/H))
            z_pred = -a * (np.cosh(np.arcsinh((V_a + w*s_end)/H)) - np.cosh(np.arcsinh(V_a/H)))
            
            # 计算预测位置与实际位置的误差
            err_x = x_pred - x_span
            err_z = z_pred - z_span
            
            # 总误差
            return err_x**2 + err_z**2
        
        # 初始猜测值
        a_init = H / w
        phi_init = np.deg2rad(5)  # 5度
        
        # 约束条件
        bounds = [(a_init*0.1, a_init*10), (0.001, np.deg2rad(16))]
        
        # 优化求解
        result = minimize(objective, [a_init, phi_init], bounds=bounds, method='L-BFGS-B')
        
        if result.success:
            a, phi = result.x
            # 验证结果
            s_check = L
            V_a = H * np.tan(phi)
            x_check = a * (np.arcsinh((V_a + w*s_check)/H) - np.arcsinh(V_a/H))
            z_check = -a * (np.cosh(np.arcsinh((V_a + w*s_check)/H)) - np.cosh(np.arcsinh(V_a/H)))
            
            # 打印验证信息
            print(f"悬链线拟合: 目标位置=({x_span:.2f}, {z_span:.2f}), 计算位置=({x_check:.2f}, {z_check:.2f})")
            
            return a, phi
        else:
            print("警告: 悬链线参数优化失败，使用初始估计值")
            return a_init, min(phi_init, np.deg2rad(16))
    
    def compute_catenary_shape(self, P_start, P_end, L, w, H, n_points=100):
        """
        计算完整悬链线形状
        P_start: 起点坐标 (锚点)
        P_end: 终点坐标 (钢桶底部)
        L: 链条长度
        w: 单位长度有效重量
        H: 水平张力
        n_points: 离散点数量
        返回: 悬链线形状坐标数组
        """
        x_start, z_start = P_start
        x_end, z_end = P_end
        
        # 找到满足条件的悬链线参数
        a, phi = self.find_catenary_parameters((0, 0), (x_end - x_start, z_end - z_start), L, w, H)
        
        # 计算完整悬链线形状
        s = np.linspace(0, L, n_points)
        x_rel, z_rel = self.catenary_equation(s, a, phi, H, w)
        
        # 调整到实际坐标系
        x = x_start + x_rel
        z = z_start + (z_rel - self.params.water_depth)
        
        return x, z, phi
    
    def solve_for_wind_speed(self, wind_speed):
        """求解特定风速下的系统状态"""
        # 1. 计算初始吃水深度
        h = self.calculate_initial_draft()
        print(f"初始吃水深度: {h:.3f} m")
        
        # 2. 计算风荷载
        F_wind = self.calculate_wind_force(wind_speed, h)
        print(f"风速 {wind_speed} m/s 下的风荷载: {F_wind:.3f} N")
        
        # 3. 浮标受力平衡
        F_b = self.calculate_buoyancy(self.params.buoy_diameter, h)
        V_0 = self.params.buoy_mass * self.params.g - F_b
        
        # 确保垂直张力为正值
        V_0 = max(V_0, 10.0)
        
        # 水平张力等于风荷载
        H = F_wind
        
        # 4. 计算钢管受力和倾斜角度
        pipe_volume = self.calculate_pipe_volume()
        W_pipe_net = self.calculate_net_weight(self.params.pipe_mass, pipe_volume)
        
        # 计算垂直张力传递
        V_1 = V_0 + W_pipe_net
        V_2 = V_1 + W_pipe_net
        V_3 = V_2 + W_pipe_net
        V_4 = V_3 + W_pipe_net
        
        # 计算角度
        theta1 = np.arctan(H / V_0)
        theta2 = np.arctan(H / V_1)
        theta3 = np.arctan(H / V_2)
        theta4 = np.arctan(H / V_3)
        
        # 5. 计算钢桶倾斜角度
        barrel_volume = self.calculate_barrel_volume()
        W_barrel_net = self.calculate_net_weight(self.params.barrel_mass, barrel_volume)
        
        # 钢桶底部垂直张力（加上重物球重量）
        V_5 = V_4 + W_barrel_net + self.params.ball_mass * self.params.g
        
        theta_t = np.arctan(H / V_4)
        
        # 6. 计算各部件坐标
        x_0, z_0 = 0, h  # 浮标底部
        x_1 = x_0 + self.params.pipe_length * np.sin(theta1)
        z_1 = z_0 + self.params.pipe_length * np.cos(theta1)
        x_2 = x_1 + self.params.pipe_length * np.sin(theta2)
        z_2 = z_1 + self.params.pipe_length * np.cos(theta2)
        x_3 = x_2 + self.params.pipe_length * np.sin(theta3)
        z_3 = z_2 + self.params.pipe_length * np.cos(theta3)
        x_4 = x_3 + self.params.pipe_length * np.sin(theta4)
        z_4 = z_3 + self.params.pipe_length * np.cos(theta4)
        x_5 = x_4 + self.params.barrel_length * np.sin(theta_t)
        z_5 = z_4 + self.params.barrel_length * np.cos(theta_t)
        
        # 7. 计算锚链
        # 锚链单位长度的有效重量
        w_chain = self.params.chain_mass_per_m * self.params.g * (1 - self.params.rho_water/self.params.rho_steel)
        
        # 8. 确定锚点位置和计算锚链形状
        # 锚点位置 (位于海底，x坐标需要确定)
        x_anchor = -5.0  # 锚点水平位置（负值表示在浮标左侧）
        z_anchor = self.params.water_depth  # 锚点在海底
        
        # 使用悬链线方程求解锚链形状
        chain_x, chain_z, phi = self.compute_catenary_shape(
            (x_anchor, z_anchor),  # 起点(锚点)
            (x_5, z_5),            # 终点(钢桶底部)
            self.params.chain_length,  # 锚链长度
            w_chain,               # 单位长度有效重量
            H                      # 水平张力
        )
        
        # 输出角度(度数)
        angles = np.degrees([theta1, theta2, theta3, theta4, theta_t])
        phi_deg = np.degrees(phi)
        
        return {
            'h': h,
            'angles': angles,
            'phi': phi_deg,
            'x_movement': x_5,
            'chain_shape': (chain_x, chain_z),
            'system_shape': ([x_0, x_1, x_2, x_3, x_4, x_5], [z_0, z_1, z_2, z_3, z_4, z_5]),
            'tension': {'H': H, 'V0': V_0, 'V5': V_5}
        }
