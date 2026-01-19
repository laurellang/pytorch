# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 14:37:56 2025

@author: lzx
"""

def gdp_increase(file):
    lines = file.readlines()
    
    years = []
    gdp = []
    for line in lines:
        parts = line.split()
        years.append(parts[0])
        gdp.append(int(parts[1]))
    
    move_gdp = []
    move_gdp.extend(gdp[1:])
    
    gdp_change = [round((a - b) / b, 2) for a, b in zip(move_gdp, gdp)]
    
    for i in range(0, len(years) - 1):
        print(f"{years[i]}的增长率是：{gdp_change[i]}")
        
if __name__ == '__main__':
    # 读取 GDP.txt 文件
    file = open('GDP.txt', 'r', encoding='gbk')
    gdp_increase(file)
    