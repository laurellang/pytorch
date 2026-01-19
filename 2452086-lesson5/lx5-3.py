# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 10:22:56 2025

@author: lzx
"""

import json
import matplotlib.pyplot as plt
import pandas as pd

def plot_weather_trend(json_file, output_file):

    plt.rcParams['font.sans-serif'] = ['SimHei']  # Use SimHei for Chinese
    plt.rcParams['axes.unicode_minus'] = False    # Fix minus sign display

    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    temps = data['wether data']  # List of [min_temp, max_temp]
    min_temps = [day[0] for day in temps]
    max_temps = [day[1] for day in temps]

    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')

    plt.figure(figsize=(12, 6))
    plt.plot(dates, min_temps, label='最低温', color='blue')
    plt.plot(dates, max_temps, label='最高温', color='red')

    plt.title('上海2023年最低温和最高温走势图')
    plt.xlabel('日期')
    plt.ylabel('温度 (°C)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(output_file, dpi=300, format='jpg')

    plt.close()

if __name__ == '__main__':
    plot_weather_trend('json_sh_wether.txt', 'wether.jpg')
    
    