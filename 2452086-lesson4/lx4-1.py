# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 14:25:46 2025

@author: lzx
"""

def cnt(honglou):
    text = honglou.read()
    
    #统计
    lin = text.count('林黛玉')  + text.count('黛玉') 
    jia = text.count('贾宝玉') + text.count('宝玉')
    
    #输出
    print(f'林黛玉出现次数：{lin}')
    print(f'贾宝玉出现次数:{jia}')
    
if __name__ == '__main__':
    honglou = open("红楼梦.txt", encoding = 'utf-8')
    cnt(honglou)
