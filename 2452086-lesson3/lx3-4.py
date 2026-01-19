# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 22:16:02 2025

@author: lzx
"""

import pandas as pd
import numpy as np

# 读取 Excel 文件中的三张表
schedule = pd.read_excel("st2025.xlsx", sheet_name="shedule")
info = pd.read_excel("st2025.xlsx", sheet_name="info")
xueke = pd.read_excel("st2025.xlsx", sheet_name="xueke")

# 清洗数据：删除 info 表的全空列，删除 xueke 表的第28列
info_clean = info.dropna(axis=1, how='all')
xueke_clean = xueke.drop(xueke.columns[28], axis=1)

# 获取学科名称
xueke_pure = xueke_clean.columns

# 合并 info 和 xueke 表，以学号为键
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

# 获取学生信息
stu_name = info_clean.loc[info_clean['学号'] == stu_num, '姓名'].iloc[0] if '姓名' in info_clean.columns else "未知"
stu_english_name = info_clean.loc[info_clean['学号'] == stu_num, '英文姓名'].iloc[0] if '英文姓名' in info_clean.columns else "Unknown"
stu_gender = info_clean.loc[info_clean['学号'] == stu_num, '性别'].iloc[0] if '性别' in info_clean.columns else "未知"

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

# 检测选课冲突
days = ['周一', '周二', '周三', '周四', '周五']
time_slots = kebiao.iloc[:, 0].tolist() 
conflicts = []

for i, time_slot in enumerate(time_slots):
    for j, day in enumerate(days):
        cell_content = kebiao.iloc[i, j + 1]  # +1 跳过时间段列
        if pd.notna(cell_content) and ',' in str(cell_content):  # 如果有多个课程
            conflicts.append({
                '上课时间': time_slot,
                '日期': day,
                '冲突课程': cell_content
            })

# 构建输出字典
result = {
    '学号': stu_num,
    '姓名': stu_name,
    '英文姓名': stu_english_name,
    '性别': stu_gender,
    '选课冲突': conflicts
}

# 打印字典
print(result)