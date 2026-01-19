# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 14:45:03 2025

@author: lzx
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei'] #设置中文字体

def draw_mean():
    score = pd.read_excel("st_data.xlsx", sheet_name = "score")
    info = pd.read_excel("st_data.xlsx", sheet_name = "info")
    
    #合并两张表
    all_info = pd.merge(score, info, on = "学号")
    
    #groupby
    gender_mean = all_info.groupby('性别')['高数'].mean()
    
    #绘制柱状图
    plt.figure(figsize = (10,10))
    bars = plt.bar(gender_mean.index, gender_mean.values)
    
    #添加标题
    plt.title("男女生高数平均成绩", fontsize = 20)
    plt.xlabel("性别", fontsize = 20)
    plt.ylabel("平均成绩", fontsize = 20)
    
    categories = ['男', '女']
    plt.xticks(np.arange(len(categories)), categories, fontsize = 20)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.2f}", ha = 'center', va='bottom', fontsize=20)
    
    plt.show()
    plt.savefig('2452086.jpg', dpi = 72)
    
if __name__ == '__main__':
    draw_mean()