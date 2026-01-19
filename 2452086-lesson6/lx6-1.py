# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 13:05:53 2025

@author: lzx
"""
stu_num = ['2', '4', '5', '2', '0' ,'8', '6']
def draw_upper_rhombus(n): #n是上面三角形的行数
    for i in range(1, n + 1):
        letter_num = 2 * i - 1
        space = n - i
        current_line = ' ' * space
        for j in range(letter_num):
            letter = stu_num[((i - 1) **2 + j) % 7]
            current_line += letter
        print(current_line)
    
def draw_lower_rhombus(n):  
    for i in range(n - 1, 0, -1):
        letter_num = 2 * i - 1
        space = n - i
        current_line = ' ' * space
        for j in range(letter_num):
            letter = stu_num[ (n**2 + ( (n - 1)**2 - i**2 + j))% 7 ]
            current_line += letter
        print(current_line)
    
def draw_rhombus(n):
    draw_upper_rhombus(n)
    draw_lower_rhombus(n)
    
if __name__ == '__main__':
    try:
        n = int(input("请输入一个1至100范围内的数字："))
        if n > 0 and n <= 100:
            draw_rhombus(n)
        else:
            print("非法输入")
    except ValueError:
        print("请输入数字！")
    