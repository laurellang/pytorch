# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 16:08:13 2025

@author: lzx
"""

from PIL import Image, ImageFilter

def process_signature():
    # 打开图像
    with Image.open(r"signature.jpg") as img:
        # 转为灰度图
        gray_img = img.convert('L')
        
        #filter
        denoised_img = gray_img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # 将灰度转为黑白
        threshold = 150  # 阈值：高于此值的像素设为白色，否则为黑色
        binary_img = denoised_img.point(lambda p: 255 if p > threshold else 0)
        
        # 保存处理后的图像
        binary_img.save(r"processed_sig.jpg")

# 使用示例
if __name__ == "__main__":
    process_signature()