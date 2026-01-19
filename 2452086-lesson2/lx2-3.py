# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 14:11:03 2025

@author: lzx
"""

try:
    a, b, c = map(float, input("请输入一元二次方程的三个系数").split())
    delta = b * b - 4 * a * c
    if delta < 0:
        print("无实根")
    elif delta == 0:
        x = - b/(2 * a)
        print(f"有两个相等实根, x1=x2={x}")
    else:
        x1 = (- b + delta ** 0.5)/(2 * a)
        x2 = (- b - delta ** 0.5)/(2 * a)
        print(f"有两个不等实根, x1={x1}, x2={x2}")

except ValueError:
    print("请输入数字！")