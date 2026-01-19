# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 14:33:24 2025

@author: lzx
"""
import numpy as np
import matplotlib.pyplot as plt

def draw_curve():
    H = 200
    W = 200
    t = np.arange(0, 2 * np.pi, 0.01)
    x = (2/3) * W * (np.cos(t)**3 + np.sin(t))
    y = (2/3) * H * (np.sin(t)**3 + np.cos(t))
    
    #绘制
    plt.figure(figsize = (10, 10))
    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.show()
    plt.savefig("curve.jpg", dpi = 72)
    print("你好")
if __name__ == '__main__':
    draw_curve()
