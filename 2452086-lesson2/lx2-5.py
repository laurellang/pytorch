# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 14:45:30 2025

@author: lzx
"""

d = {'0' : 'zero',
     '1' : 'one',
     '2' : 'two',
     '3' : 'three',
     '4' : 'four',
     '5' : 'five',
     '6' : 'six',
     '7' : 'seven',
     '8' : 'eight',
     '9' : 'nine'}

user_input = input("请输入11位电话号码")
number = d[user_input[0]]
for char in user_input[1:]:
    number = number + '-' + d[char]

print(number)