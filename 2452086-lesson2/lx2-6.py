import random

def generate_matrix(rows, cols):
    """生成指定大小的随机0-1矩阵"""
    return [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]

def print_matrix(matrix):
    """打印矩阵，元素间用空格分隔"""
    for row in matrix:
        print(' '.join(map(str, row)))
    print()

def largest_rectangle_area(heights, row):
    """计算直方图中最大矩形的面积，返回7元素元组"""
    stack = []
    max_area = 0
    max_info = None
    n = len(heights)
    
    for i in range(n + 1):
        h = heights[i] if i < n else 0
        
        while stack and h < heights[stack[-1]]:
            height_idx = stack.pop()
            height = heights[height_idx]
            width = i if not stack else i - stack[-1] - 1
            area = height * width
            
            top_row = row - height + 1
            left_col = stack[-1] + 1 if stack else 0
            right_col = i - 1  # 右列索引
            
            if area > max_area:
                max_area = area
                # 元组结构：(面积, 顶行, 左列, 底行, 右列, 高度, 宽度)
                max_info = (area, top_row, left_col, row, right_col, height, width)
        
        stack.append(i)
    
    return max_info

def find_max_rectangle_dp(matrix):
    """使用DP方法查找最大全1矩形"""
    if not matrix or not matrix[0]:
        return None
    
    rows = len(matrix)
    cols = len(matrix[0])
    max_info = None
    dp_heights = [0] * cols
    
    for i in range(rows):
        for j in range(cols):
            dp_heights[j] = dp_heights[j] + 1 if matrix[i][j] == 1 else 0
        
        current_max = largest_rectangle_area(dp_heights, i)
        if current_max and (not max_info or current_max[0] > max_info[0]):
            max_info = current_max
    
    return max_info

def replace_max_rectangle(matrix, max_info):
    """将最大矩形中的1替换为*号"""
    if not max_info:
        return [row.copy() for row in matrix]
    
    new_matrix = [row.copy() for row in matrix]
    _, top_row, left_col, bottom_row, right_col, _, _ = max_info  # 解包7个元素
    
    for i in range(top_row, bottom_row + 1):
        for j in range(left_col, right_col + 1):
            if new_matrix[i][j] == 1:
                new_matrix[i][j] = '*'
    
    return new_matrix

# 主程序
if __name__ == "__main__":
    # 生成10x10的随机0-1矩阵
    matrix = generate_matrix(10, 10)
    
    # 输出原始矩阵
    print("原始10x10矩阵：")
    print_matrix(matrix)
    
    # 查找最大全1矩形
    max_rect_info = find_max_rectangle_dp(matrix)
    
    # 替换最大矩形中的1为*号（提前准备好替换后的矩阵）
    modified_matrix = replace_max_rectangle(matrix, max_rect_info)
    
    # 先显示最大矩形信息，再显示替换后的矩阵
    if max_rect_info:
        # 解包并提取需要的信息
        area, top_row, left_col, _, _, height, width = max_rect_info
        print("找到最大全1矩形：")
        print(f"面积={area}，位置：顶行={top_row}，左列={left_col}，高度={height}，宽度={width}")
        print("替换后的矩阵：")
        print_matrix(modified_matrix)
    else:
        print("未找到全1矩形")
