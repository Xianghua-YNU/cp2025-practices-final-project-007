import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from scipy.optimize import root, fsolve, minimize
import matplotlib as mpl

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

#############################################################
# 参数设置模块
#############################################################

class MooringSystemParams:
    def __init__(self):
        # 环境参数
        self.g = 9.8  # 重力加速度 (m/s^2)
        self.rho_water = 1.025e3  # 海水密度 (kg/m^3)
        self.rho_steel = 7850  # 钢密度 (kg/m^3)
        self.water_depth = 18.0  # 水深 (m)
        
        # 浮标参数
        self.buoy_diameter = 2.0  # 浮标直径 (m)
        self.buoy_height = 2.0  # 浮标高度 (m)
        self.buoy_mass = 1000.0  # 浮标质量 (kg)
        
        # 钢管参数
        self.pipe_length = 1.0  # 钢管长度 (m)
        self.pipe_diameter = 0.05  # 钢管直径 (m)
        self.pipe_mass = 10.0  # 每节钢管质量 (kg)
        self.n_pipes = 4  # 钢管数量
        
        # 钢桶参数
        self.barrel_length = 1.0  # 钢桶长度 (m)
        self.barrel_diameter = 0.3  # 钢桶直径 (m)
        self.barrel_mass = 100.0  # 钢桶和设备总质量 (kg)
        
        # 重物球参数
        self.ball_mass = 1200.0  # 重物球质量 (kg)
        
        # 锚链参数
        self.chain_length = 22.05  # 锚链长度 (m)
        self.chain_mass_per_m = 7.0  # II型锚链单位长度质量 (kg/m)
        
        # 锚参数
        self.anchor_mass = 600.0  # 锚质量 (kg)
        
        # 风速参数 (两种情况)
        self.wind_speeds = [12.0, 24.0]  # 风速 (m/s)

#############################################################
# 主程序
#############################################################

def main():
    print("开始系泊系统计算...")
    
    # 初始化参数
    params = MooringSystemParams()
    
    # 初始化求解器
    solver = MooringSystemSolver(params)
    
    # 求解两种风速条件
    results = {}
    for wind_speed in params.wind_speeds:
        print(f"\n计算风速 {wind_speed} m/s 的系统状态...")
        results[wind_speed] = solver.solve_for_wind_speed(wind_speed)
    
    # 数据分析
    analyzer = MooringSystemAnalyzer(params)
    analysis = analyzer.analyze_results(results[12.0], results[24.0])
    
    # 输出结果
    print("\n=== 计算结果 ===")
    print("\n风速 12 m/s:")
    print(f"浮标吃水深度: {analysis['wind_12ms']['吃水深度']:.3f} m")
    print(f"浮标游动区域: {analysis['wind_12ms']['游动区域']:.3f} m")
    print(f"钢管倾斜角度: {[f'{angle:.2f}°' for angle in analysis['wind_12ms']['钢管角度']]}")
    print(f"钢桶倾斜角度: {analysis['wind_12ms']['钢桶角度']:.2f}°")
    print(f"锚链与海床夹角: {analysis['wind_12ms']['锚链角度']:.2f}°")
    
    print("\n风速 24 m/s:")
    print(f"浮标吃水深度: {analysis['wind_24ms']['吃水深度']:.3f} m")
    print(f"浮标游动区域: {analysis['wind_24ms']['游动区域']:.3f} m")
    print(f"钢管倾斜角度: {[f'{angle:.2f}°' for angle in analysis['wind_24ms']['钢管角度']]}")
    print(f"钢桶倾斜角度: {analysis['wind_24ms']['钢桶角度']:.2f}°")
    print(f"锚链与海床夹角: {analysis['wind_24ms']['锚链角度']:.2f}°")
    
    # 可视化
    visualizer = MooringSystemVisualizer(params)
    visualizer.plot_chain_shape(results[12.0], results[24.0])
    visualizer.plot_motion_range(results[12.0], results[24.0])
    
    print("\n系泊系统计算完成。")

if __name__ == "__main__":
    main()
