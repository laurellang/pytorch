# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 13:36:21 2025

@author: lzx
"""
'''
n = 64
def mychar():
    global n
    if n == 90:
        n = 64
    n += 1
    return (chr(n))

    
def triangle_layer(x, n): #打印第x层三角形
    print(' ' * (n - x), end = '')
    for i in range (2 * x - 1):
        print(mychar(), end = '')
        
total_layer = int(input('请输入三角形的行数（1-26）：'))
x= 1
for i in range(total_layer):
    triangle_layer(x, total_layer)
    x += 1
    print()
''' 
    
    
'''revised version'''
n = int(input('请输入三角形的行数（1-26）：'))
for i in range(1, n + 1):
    letter_num = 2 * i - 1
    space = n - i
    current_line = ""
    for j in range(letter_num):
        letter = chr(ord('A') + ((i - 1) ** 2 + j) % 26)
        current_line += letter
    print(' ' * space + current_line)