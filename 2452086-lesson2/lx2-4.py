# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 14:30:39 2025

@author: lzx
"""
dic = {}
user_input = input("请输入字符串")
for char in user_input:
    dic[char] = dic.get(char, 0) + 1

#输出
print("每个字母出现次数")    
for key in sorted(dic.keys()):
    print(f"{key} : {dic[key]}")