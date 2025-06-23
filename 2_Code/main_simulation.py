"""
主程序入口：用于运行主要的物理模拟。
"""
import numpy as np
# from .numerical_methods import solve_ode
# from .data_analysis import analyze_data
# from .visualization import plot_results

def run_simulation():
    """
    运行整个模拟流程。
    """
    print("Running main simulation...")
  import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

# 常量定义
g = 9.81  # 重力加速度(m/s²)
rho_sea = 1025  # 海水密度(kg/m³)
depth = 18  # 水深(m)

# 浮标参数
d_float = 2.0  # 直径(m)
h_float = 2.0  # 高度(m)
m_float = 1000  # 质量(kg)

# 钢管参数 (4节)
n_pipes = 4
l_pipe = 1.0  # 每节长度(m)
d_pipe = 0.05  # 直径(m)
m_pipe = 10  # 单节质量(kg)

# 钢桶参数
l_drum = 1.0  # 长度(m)
d_drum = 0.3  # 直径(m)
m_drum = 100  # 总质量(kg)

# 重物球
m_ball = 1200  # 质量(kg)

# 锚链参数 (II型)
chain_type = "II"
chain_len = 22.05  # 长度(m)
chain_mass_per_m = 7  # 单位质量(kg/m)

# 锚参数
m_anchor = 600  # 质量(kg)

# 计算两种风速情况
results_12m = calculate_system(12, verbose=True)
results_24m = calculate_system(24, verbose=True)
    print("Simulation finished.")

# 绘制锚链形状
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
plot_chain(ax1, results_12m, '风速 12m/s 锚链形状')
plot_chain(ax2, results_24m, '风速 24m/s 锚链形状')
plt.tight_layout()
plt.savefig('mooring_chain_shape.png')
plt.show()

# 输出详细结果表
print("\n汇总结果:")
print(f"{'参数':<20} | {'12m/s':<20} | {'24m/s':<20}")
print("-"*60)
print(f"{'浮标吃水深度(m)':<20} | {results_12m['h_float']:.3f}{'':<15} | {results_24m['h_float']:.3f}")
print(f"{'浮标位移(m)':<20} | {results_12m['x_float']:.3f}{'':<15} | {results_24m['x_float']:.3f}")
print(f"{'钢桶倾斜角(°)':<20} | {results_12m['drum_angle']:.2f}{'':<15} | {results_24m['drum_angle']:.2f}")
for i in range(n_pipes):
    print(f"{'钢管'+str(i+1)+'倾斜角(°)':<20} | {results_12m['pipe_angles'][i]:.2f}{'':<15} | {results_24m['pipe_angles'][i]:.2f}")
print(f"{'锚链末端角(°)':<20} | {results_12m['end_angle']:.2f}{'':<15} | {results_24m['end_angle']:.2f}")

if __name__ == "__main__":
    run_simulation()
