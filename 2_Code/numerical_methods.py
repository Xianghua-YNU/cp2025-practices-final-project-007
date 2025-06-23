"""
核心数值算法模块：包含各种数值方法实现。
"""
import numpy as np

def calculate_system(v_wind, verbose=False):
    """计算给定风速下的系统状态"""
    # 1. 浮标初始参数
    h_guess = 0.5  # 初始吃水深度(m)
    
    # 2. 浮标受力和力矩
    def float_equations(h):
        # 浮标投影面积 (圆柱侧面积)
        A_float = d_float * (h_float - h)
        F_wind = 0.625 * A_float * v_wind**2
        
        # 浮力
        V_displaced = np.pi * (d_float/2)**2 * h
        F_buoy = rho_sea * g * V_displaced
        
        # 重力
        W_float = m_float * g
        
        # 平衡方程 (只考虑垂直方向平衡)
        return F_buoy - W_float
    
    # 求解吃水深度
    h_sol = fsolve(float_equations, h_guess)[0]
    
    # 浮标水平位移估计
    x_float_sol = 1.0 + 0.1 * v_wind
    
    if verbose:
        print(f"风速 {v_wind} m/s 时浮标状态:")
        print(f"吃水深度: {h_sol:.3f} m")
        print(f"水平位移: {x_float_sol:.3f} m")
    
    # 3. 钢管和钢桶倾斜角度
    pipe_angles = []
    for i in range(n_pipes):
        # 角度计算：基础角度 + 风速影响 + 位置影响
        angle = 0.5 + 0.15 * v_wind + 0.1 * i
        pipe_angles.append(min(angle, 15))  # 限制最大角度
        if verbose and i == 0:
            print(f"第{i+1}节钢管倾斜角: {pipe_angles[i]:.2f}°")
    
    # 钢桶倾斜角
    drum_angle = 1.0 + 0.25 * v_wind
    if verbose:
        print(f"钢桶倾斜角: {drum_angle:.2f}°")
    
    # 4. 锚链形状 (悬链线模型)
    def catenary(x, a):
        return a * np.cosh(x / a) - a  # 减去a使曲线通过原点
    
    # 锚链参数 - 根据风速调整
    a_param = 100 - 3 * v_wind  # 悬链线参数
    x_chain = np.linspace(0, chain_len, 50)
    y_chain = catenary(x_chain, a_param)
    
    # 5. 锚链末端角度
    end_angle = 8 + 0.6 * v_wind  # 简化计算
    if verbose:
        print(f"锚链末端角度: {end_angle:.2f}°")
        print("="*50)
    
    return {
        'h_float': h_sol,
        'x_float': x_float_sol,
        'pipe_angles': pipe_angles,
        'drum_angle': drum_angle,
        'end_angle': end_angle,
        'chain_shape': (x_chain, y_chain)
    }

# 可以添加更多数值方法，如积分、求根、矩阵运算等
