# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 13:56:02 2025

@author: lzx
"""
cnt_chicken = 0
cnt_rabbit = 0

try:
    head, feet = map(int,input("请输入总头数、总脚数（用空格隔开）").split())
    if feet % 2 == 1:
        print("总脚数必须为偶数！")
    else:
        #计算个数
        cnt_rabbit = feet // 2 - head
        cnt_chicken = head - cnt_rabbit
        
        #处理负数情况
        if cnt_rabbit < 0 or cnt_chicken < 0:
            print("输入的总头数或总脚数有误，计算出负数！")
        
        elif (type(cnt_rabbit) != int) or (type(cnt_chicken) != int):
            print("输入的总头数或总脚数有误，结果不为整数！")
            
        else:
            print(f"鸡有{cnt_chicken}只，兔有{cnt_rabbit}只")
except ValueError:
    print("请输入两个用空格隔开的数字！")
        
