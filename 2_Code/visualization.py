"""
可视化函数模块：用于绘制模拟结果和分析数据。
"""
import matplotlib.pyplot as plt
import numpy as np

# 可视化结果
def plot_chain(ax, results, title):
    x, y = results['chain_shape']
    ax.plot(x, y, 'b-')
    ax.set_title(title)
    ax.set_xlabel('水平距离 (m)')
    ax.set_ylabel('高度 (m)')
    ax.grid(True)
    ax.set_ylim(0, 20)
    ax.set_xlim(0, 25)
    ax.hlines(y=0, xmin=0, xmax=25, colors='k', linestyles='--')  # 海床线

# 绘制锚链形状
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
plot_chain(ax1, results_12m, '风速 12m/s 锚链形状')
plot_chain(ax2, results_24m, '风速 24m/s 锚链形状')
plt.tight_layout()
plt.savefig('mooring_chain_shape.png')
plt.show()

# 可以添加更多绘图函数，如散点图、三维图等
