# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 16:43:17 2025

@author: lzx
"""

def four_color_map(graph):
    # 定义可用的四种颜色
    colors = ['红', '黄', '蓝', '绿']
    # 初始化省份颜色分配字典
    color_assignment = {}
    
    def is_safe(node, color):
        # 检查当前颜色是否安全（邻省没有相同颜色）
        for neighbor in graph[node]:
            if neighbor in color_assignment and color_assignment[neighbor] == color:
                return False
        return True
    
    def color_map(node_list, index):
        # 递归终止条件：所有省份都已着色
        if index == len(node_list):
            return True
        
        node = node_list[index]
        # 尝试为当前省份分配每种颜色
        for color in colors:
            if is_safe(node, color):
                color_assignment[node] = color
                # 递归为下一个省份着色
                if color_map(node_list, index + 1):
                    return True
                # 回溯：移除当前颜色，尝试其他颜色
                color_assignment.pop(node)
        
        return False
    
    # 获取所有省份列表
    provinces = list(graph.keys())
    # 开始着色
    color_map(provinces, 0)
    
    return color_assignment

# 省份邻接关系数据
graph = {
    '河北': ['内蒙古', '辽宁', '山东', '河南', '山西'],
    '山西': ['河北', '河南', '陕西', '内蒙古'],
    '内蒙古': ['黑龙江', '吉林', '辽宁', '河北', '山西', '陕西', '宁夏', '甘肃'],
    '辽宁': ['内蒙古', '河北', '吉林'],
    '吉林': ['黑龙江', '内蒙古', '辽宁'],
    '黑龙江': ['内蒙古', '吉林'],
    '山东': ['河北', '河南', '安徽', '江苏'],
    '河南': ['河北', '山东', '安徽', '湖北', '陕西', '山西'],
    '安徽': ['山东', '河南', '湖北', '江西', '江苏', '浙江'],
    '江苏': ['山东', '安徽', '浙江'],
    '浙江': ['江苏', '安徽', '江西', '福建'],
    '福建': ['浙江', '江西', '广东'],
    '广东': ['福建', '江西', '湖南', '广西'],
    '广西': ['广东', '湖南', '贵州', '云南'],
    '云南': ['广西', '贵州', '四川', '西藏'],
    '西藏': ['新疆', '青海', '四川', '云南'],
    '四川': ['陕西', '甘肃', '青海', '西藏', '云南', '贵州'],
    '贵州': ['四川', '云南', '广西', '湖南'],
    '湖南': ['湖北', '贵州', '广西', '广东', '江西'],
    '湖北': ['河南', '陕西', '湖南', '江西', '安徽'],
    '江西': ['安徽', '湖北', '湖南', '广东', '福建', '浙江'],
    '陕西': ['山西', '河南', '湖北', '四川', '甘肃', '宁夏', '内蒙古'],
    '甘肃': ['新疆', '内蒙古', '宁夏', '陕西', '四川', '青海'],
    '青海': ['新疆', '甘肃', '四川', '西藏'],
    '宁夏': ['内蒙古', '陕西', '甘肃'],
    '新疆': ['西藏', '青海', '甘肃'],
}

# 获取并打印着色方案
result = four_color_map(graph)
for province, color in result.items():
    print(f"{province}: {color}")