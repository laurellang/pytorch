# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 15:34:14 2025

@author: lzx
"""
import PIL as p
im = p.Image.open(r'2452086.jpg')
width, height = im.size


def huihua():
    for x in range(width):
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            temp = int((r + g + b) / 3)
            if y > height >> 1:
                m = (temp, temp, temp)
                im.putpixel((x, y), m)
    im.show()
    
    im_format = im.format
    im_mode = im.mode
    print(f"宽度是{width}像素")
    print(f"高度是{height}像素")
    print(f"格式是{im_format}")
    print(f"模式是{im_mode}")        
                
if __name__ == '__main__':
    huihua()