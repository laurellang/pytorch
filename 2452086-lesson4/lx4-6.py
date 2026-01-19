# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 16:58:21 2025

@author: 29370
"""

class sfz:
    def __init__(self, id):
        self.id = id
        
    def getyear(self):
        # 提取18位身份证中的出生年份（第7-10位）
        return int(self.id[6:10])
    
    def disp(self):
        print(f"身份证号码为:{self.id}")

if __name__ == "__main__":    
    # 注意：身份证号码应以字符串形式传递（加上引号）
    sfz_id = sfz("440304200606111234")
    sfz_id.disp()
    print(f"出生年份:{sfz_id.getyear()}")
        