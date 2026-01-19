# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 15:13:17 2025

@author: lzx
"""
from PIL import Image
import numpy as np

def process_image(input_file='tj.jpg', output_file='tj.txt', char_set='@#S%?*+;:,.'):
    # 定义字符集
    s = char_set

    # 打开并处理图片
    try:
        img = Image.open(input_file).convert('L')  # 转换为灰度图
        img_array = np.array(img)
        
        # 将像素值映射为字符
        height, width = img_array.shape
        output = ''
        
        for i in range(height):
            for j in range(width):
                # 将灰度值除以25，用结果作为字符集s的索引
                index = img_array[i, j] // 25
                output += s[index]
            output += '\n'
        
        # 保存为tj.txt
        with open(output_file, 'w') as f:
            f.write(output)
        
        return True

    except Exception as e:
        print(f"处理图片出错: {e}")
        return False

if __name__ == '__main__':
    # 执行主程序
    if process_image():
        print("图片处理成功，输出已保存为tj.txt")
    else:
        print("图片处理失败")
