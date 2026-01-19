# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 15:24:16 2025

@author: lzx
"""
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io

# 设置宋体字体（SimSun 是宋体在 matplotlib 中的常见名称）
plt.rcParams['font.sans-serif'] = ['SimSun']  # 修改为宋体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def process_sales_data(product_file='产品信息', customer_file='客户信息', sales_file='销售记录',
                       output_image='sales.jpg', output_txt='sales_summary.txt'):
    # 读取Excel文件中的三个工作表
    try:
        products = pd.read_excel('销售数据.xlsx', sheet_name=product_file)
        customers = pd.read_excel('销售数据.xlsx', sheet_name=customer_file)
        sales = pd.read_excel('销售数据.xlsx', sheet_name=sales_file)
    except Exception as e:
        print(f"读取Excel文件出错: {e}")
        return False

    # 计算订单总金额（数量 * 售价）
    try:
        # 合并销售记录和产品信息以获取售价
        sales_with_price = sales.merge(products[['产品ID', '售价']], on='产品ID', how='left')
        sales_with_price['总金额'] = sales_with_price['数量'] * sales_with_price['售价']

        # 合并销售记录和客户信息以获取城市
        sales_with_city = sales_with_price.merge(customers[['客户ID', '城市']], on='客户ID', how='left')

        # 按城市统计总消费额，仅包括上海、北京、广州
        city_spending = sales_with_city[sales_with_city['城市'].isin(['上海', '北京', '广州'])]
        city_totals = city_spending.groupby('城市')['总金额'].sum().reset_index()

        # 检查数据是否为空
        if city_totals.empty:
            print("上海、北京、广州的销售数据为空")
            return False

        # 创建饼状图
        plt.figure(figsize=(8, 8))
        plt.pie(city_totals['总金额'], labels=city_totals['城市'], autopct='%1.1f%%',
                colors=['#ff9999', '#66b3ff', '#99ff99'])
        plt.title('2025-07-30三地消费总额对比')

        # 保存饼状图为PNG格式到内存
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        plt.close()

        # 使用PIL保存为JPG
        buffer.seek(0)
        image = Image.open(buffer).convert('RGB')
        image.save(output_image, 'JPEG')
        buffer.close()

        # 保存统计数据到 GB2312 编码的文本文件
        try:
            with open(output_txt, 'w', encoding='gb2312') as f:
                f.write("2025-07-30 三地消费总额统计\n")
                f.write("城市\t总金额\n")
                for _, row in city_totals.iterrows():
                    f.write(f"{row['城市']}\t{row['总金额']:.2f}\n")
            print(f"统计数据已保存到 {output_txt}，编码为 GB2312")
        except Exception as e:
            print(f"保存文本文件出错: {e}")
            return False

        return True

    except Exception as e:
        print(f"处理数据或生成图片出错: {e}")
        return False

if __name__ == '__main__':
    # 执行主程序
    if process_sales_data():
        print("饼状图生成成功，保存为sales.jpg")
        print("统计数据生成成功，保存为sales_summary.txt")
    else:
        print("饼状图或统计数据生成失败")