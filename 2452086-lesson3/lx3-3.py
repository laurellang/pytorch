# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 20:26:12 2025

@author: lzx
"""

import pandas as pd
import numpy as np
import unicodedata

# 计算字符串的显示宽度
def get_display_width(text):
    width = 0
    for char in str(text):
        # 判断字符是否为全宽
        width += 2 if unicodedata.east_asian_width(char) in ('F', 'W', 'A') else 1
    return width

# 读取 Excel 文件中的三张表
schedule = pd.read_excel("st2025.xlsx", sheet_name="shedule")
info = pd.read_excel("st2025.xlsx", sheet_name="info")
xueke = pd.read_excel("st2025.xlsx", sheet_name="xueke")

# 清洗数据：删除 info 表的全空列，删除 xueke 表的第28列
info_clean = info.dropna(axis=1, how='all')
xueke_clean = xueke.drop(xueke.columns[28], axis=1)

# 获取学科名称
xueke_pure = xueke_clean.columns

# 合并 info 和 xueke 表
stu_info = pd.merge(info_clean, xueke_clean, on='学号', how='outer')

# 创建课表副本并清空课程内容
kebiao = schedule.copy()
kebiao.iloc[:, 1:6] = np.nan

# 请求用户输入学号并验证
stu_num = int(input("请输入要查询的学号："))
if stu_num not in info_clean['学号'].values:
    print("错误：学号不存在！")
    exit()

# 找到学号对应的行索引
stu_row = np.where(info_clean['学号'] == stu_num)[0][0]

# 获取学生姓名
stu_name = info_clean.loc[info_clean['学号'] == stu_num, '姓名'].iloc[0] if '姓名' in info_clean.columns else "学生"

# 根据学生选课信息填充课表
for xuekes in xueke_pure[1:]:
    xk_col = stu_info.columns.get_loc(xuekes)
    if pd.notna(stu_info.iloc[stu_row, xk_col]):  # 如果学生选了这门课
        for i in range(schedule.shape[0]):
            for j in range(schedule.shape[1]):
                cell_value = schedule.iloc[i, j]
                if pd.isna(cell_value):
                    continue
                if xuekes in cell_value:
                    if pd.isna(kebiao.iloc[i, j]):
                        kebiao.iloc[i, j] = xuekes
                    else:
                        kebiao.iloc[i, j] = kebiao.iloc[i, j] + ',' + xuekes
'''revised ver'''
'''将课表先转化为str，再replace掉没有选择的课程'''
str_kebiao = str(schedule)
for xuekes in xueke_pure[1:]:
    xk_col = stu_info.columns.get_loc(xuekes)
    if pd.isna(stu_info.iloc[stu_row, xk_col]): #如果学生没有选这门课
        str_kebiao = str_kebiao.replace(xuekes, '')
        str_kebiao = str_kebiao.replace(','+xuekes, '')
        str_kebiao = str_kebiao.replace(xuekes + ',', '')
        
# 动态调整列宽和内容间隔
days = ['周一', '周二', '周三', '周四', '周五']
time_slots = kebiao.iloc[:, 0].tolist()  # 假设第一列为时间段
time_col_width = 15  # “上课时间”列固定宽度
min_cell_width = 15  # 每列最小宽度
max_cell_width = 25  # 每列最大宽度

# 计算每列的最大显示宽度（考虑中文）
col_widths = []
for j, day in enumerate(days):
    max_length = max(
        get_display_width(kebiao.iloc[i, j + 1]) if pd.notna(kebiao.iloc[i, j + 1]) else 0
        for i in range(len(time_slots))
    )
    max_length = max(max_length, get_display_width(day))  # 确保列标题宽度也考虑
    col_widths.append(min(max(max_length + 4, min_cell_width), max_cell_width))  # 加4留缓冲

# 计算总表格宽度
total_width = time_col_width + sum(col_widths) + 15
separator_line = '*' * total_width

# 动态调整标题居中
title = f"{stu_name}的课表"
title_padding = (total_width - get_display_width(title)) // 2

# 打印标题和分隔线
print(f"\n{' ' * title_padding}{title}\n")
print(separator_line)

# 打印表头
print(f"{'上课时间':<{time_col_width}}", end='')
for day, width in zip(days, col_widths):
    print(f"{day:^{width}}", end='')
print(f"\n{'-' * total_width}")

# 打印课表内容，动态调整内容间隔以居中
for i, time_slot in enumerate(time_slots):
    print(f"{time_slot:<{time_col_width}}", end='')
    for j, width in enumerate(col_widths):
        cell_content = kebiao.iloc[i, j + 1]  # +1 跳过时间段列
        cell_content = str(cell_content) if pd.notna(cell_content) else ''
        # 如果内容过长，截断并添加省略号
        if get_display_width(cell_content) > width - 2:
            # 逐步截断直到显示宽度合适
            while get_display_width(cell_content + '...') > width - 2 and cell_content:
                cell_content = cell_content[:-1]
            cell_content = cell_content + '...' if cell_content else '...'
        print(f"{cell_content:^{width}}", end='')
    print()
