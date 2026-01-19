# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 16:11:11 2025

@author: lzx
"""

import jieba
from collections import Counter

def count_top_three(text):
    words = jieba.cut(text)
    # 过滤单字符词和标点符号
    word_list = [word for word in words if len(word) > 1 and word not in '，。！？、；：（）']
    word_freq = Counter(word_list)
    top_three = word_freq.most_common(3)
    return top_three


if __name__ == "__main__":
    with open("tj.txt", encoding="utf-8") as file:
        text = file.read()
   
    top_three = count_top_three(text)
    for word, freq in top_three:
        print(f"{word}, {freq}")
        
