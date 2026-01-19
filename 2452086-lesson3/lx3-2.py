# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 23:04:55 2025

@author: lzx
"""

def f(x):
    return 2 * x**3 - 4 * x**2 + 3 * x - 6

def bisection(a, b, max_iter=100, tol=1e-6):
    if f(a) * f(b) >= 0:
        return None, "f(a) 和 f(b) 必须异号"
    
    iter_count = 0
    while iter_count < max_iter:
        # 计算中点
        c = (a + b) / 2
        fc = f(c)
        
        # 判断误差是否满足精度要求
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c, iter_count
        
        # 更新区间
        if f(a) * fc < 0:
            b = c
        else:
            a = c
        
        iter_count += 1
    
    return c, iter_count

if __name__ == "__main__":
    # 在 [-10, 10] 内分段检查根
    roots = []
    if f(-10) * f(10) < 0:  # 存在根的区间
        root, iterations = bisection(-10, 10)
        if root is not None:
            roots.append((root, iterations))
    
    # 输出结果
    print("在区间 [-10, 10] 内的根：")
    for i, (root, iterations) in enumerate(roots, 1):
        print(f"根 {i}: x ≈ {root:.6f}, 迭代次数: {iterations}")