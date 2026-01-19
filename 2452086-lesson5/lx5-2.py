# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 08:19:18 2025

@author: lzx
"""
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']

def count_and_draw():
    #读入
    score = pd.read_excel("st_data.xlsx", sheet_name = "score")
    
    #设定范围
    bins = [0, 60, 70, 80, 90, 100]
    labels = ['不及格', '及格', '中', '良', '优秀']
    
    c_score = score['C语言']
    python_score = score['Python']
    
    score_cnt_c = pd.cut(c_score, bins = bins, labels = labels, include_lowest = True).value_counts()
    score_cnt_p = pd.cut(python_score, bins = bins, labels = labels, include_lowest = True).value_counts()
    
    plt.figure(figsize = (10, 10))
    plt.subplot(121)
    wedges_c, texts_c, autotexts_c = plt.pie(score_cnt_c,labels = labels, autopct = '%1.1f%%', startangle = 90, 
                                       colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF66CC'] )
    plt.legend(wedges_c, labels, title="分数范围", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
               fontsize=8, handlelength=1.5, handleheight=1.0)
    plt.title('C语言成绩分布')
    
    plt.subplot(122)
    wedges_p, texts_p, autotexts_p = plt.pie(score_cnt_p,labels = labels, autopct = '%1.1f%%', startangle = 90, 
            colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF66CC'] )
    plt.legend(wedges_p, labels, title="分数范围", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
               fontsize=8, handlelength=1.5, handleheight=1.0)
    plt.title('Python成绩分布')
    
    plt.show()
    plt.savefig('pie_2452086.jpg', dpi = 72)
    
if __name__ == '__main__':
    count_and_draw()
    
    
