# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 22:48:16 2025

@author: lzx
"""

#找出1000以内所有素数
prime = []
def prime_whithin_onethousand():
    for i in range(2, 997):
        is_prime = 1
        for j in range(2, int(i ** 0.5) + 1):
            if i % j == 0:
                is_prime = 0
                break
        if is_prime:
            prime.append(i)
'''revised ver from lzh'''
'''lt = [x for x in range(2, 1000) if 0 not in [x % y for y in range(2, int(x**0.5) + 1]]'''

#对于一个偶数，找到它由哪两个素数组成
def even_makeup(x):
    for i in prime:
        k = x - i
        if k in prime:
            print(f"{x}={i}+{k}")
            break
            
if __name__ == "__main__":
    prime_whithin_onethousand()
    try:
        user_number = int(input("请输入一个1000以内的偶数："))
        if user_number > 2 and user_number < 1000:
            even_makeup(user_number)
        else:
            print("数字不在范围内！")
        
    except ValueError:
        print("无效输入")