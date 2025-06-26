#############################################################
# 数据分析模块
#############################################################

class MooringSystemAnalyzer:
    def __init__(self, params):
        self.params = params
    
    def analyze_results(self, results_12, results_24):
        """分析两种风速下的计算结果"""
        analysis = {
            'wind_12ms': {
                '吃水深度': results_12['h'],
                '游动区域': results_12['x_movement'],
                '钢管角度': results_12['angles'][:-1],
                '钢桶角度': results_12['angles'][-1],
                '锚链角度': results_12['phi']
            },
            'wind_24ms': {
                '吃水深度': results_24['h'],
                '游动区域': results_24['x_movement'],
                '钢管角度': results_24['angles'][:-1],
                '钢桶角度': results_24['angles'][-1],
                '锚链角度': results_24['phi']
            }
        }
        
        # 检查钢桶角度是否超过5度
        if analysis['wind_12ms']['钢桶角度'] > 5:
            print(f"警告: 风速12m/s时钢桶角度为 {analysis['wind_12ms']['钢桶角度']:.2f}°，超过了5°的工作效果标准")
        
        if analysis['wind_24ms']['钢桶角度'] > 5:
            print(f"警告: 风速24m/s时钢桶角度为 {analysis['wind_24ms']['钢桶角度']:.2f}°，超过了5°的工作效果标准")
        
        return analysis
