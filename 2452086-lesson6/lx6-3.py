# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 15:34:37 2025

@author: lzx
"""

import re
import matplotlib.pyplot as plt
from collections import defaultdict
import chardet
import matplotlib.font_manager as fm
import os

# 字体配置：尝试系统中常见的中文字体，优先级排序
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "WenQuanYi Micro Hei", "Heiti TC", "Arial", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

def get_available_fonts():
    """获取系统中可用的字体列表"""
    font_list = fm.findSystemFonts()
    available = []
    for font in font_list:
        try:
            font_name = fm.FontProperties(fname=font).get_name()
            available.append(font_name.lower())
        except:
            continue
    return available

def set_compatible_font():
    """根据系统可用字体自动设置兼容字体"""
    available = get_available_fonts()
    preferred_fonts = [
        "simhei", "microsoft yahei", "wenquanyi micro hei", "heiti tc", "simsun", "arial"
    ]
    for font in preferred_fonts:
        if any(font in font_name for font_name in available):
            plt.rcParams["font.family"] = [font]
            print(f"使用系统可用字体：{font}")
            return
    plt.rcParams["font.family"] = ["sans-serif"]
    print("使用默认字体")

def detect_file_encoding(filename):
    """自动检测文件编码"""
    try:
        with open(filename, 'rb') as f:
            raw_data = f.read(10000)  # 读取前10000字节
        result = chardet.detect(raw_data)
        encoding = result['encoding'] or 'utf-8'
        confidence = result['confidence']
        print(f"检测到文件 {filename} 的编码：{encoding}（置信度：{confidence:.2f}）")
        if confidence < 0.7:
            print(f"警告：编码置信度较低，可能不准确，尝试使用 gbk 或 gb18030")
            return 'gb18030' if '三国演义' in filename else 'gbk'
        return encoding
    except Exception as e:
        print(f"检测编码出错：{e}，默认使用 gbk")
        return 'gbk'

def load_person_names(filename):
    """加载人名汇总并去重"""
    try:
        encoding = detect_file_encoding(filename)
        with open(filename, 'r', encoding=encoding, errors='ignore') as f:
            person_names = []
            for line in f:
                # 清理名字，去除替换字符和无效字符
                line = line.replace('\ufffd', '').strip()
                names = line.split()
                person_names.extend(names)
        # 去重并过滤空名字
        unique_names = [name for name in set(person_names) if name and not re.search(r'[^\u4e00-\u9fff]', name)]
        print(f"加载人名 {len(unique_names)} 个（去重后）")
        if unique_names:
            print("前5个名字：", unique_names[:5])
        return unique_names
    except FileNotFoundError:
        print(f"错误：未找到人名文件 {filename}")
        return []
    except Exception as e:
        print(f"加载人名出错：{e}")
        return []

def load_novel_content(filename):
    """加载小说内容"""
    try:
        encoding = detect_file_encoding(filename)
        with open(filename, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()
        # 移除替换字符
        content = content.replace('\ufffd', '')
        print("小说内容加载完成")
        return content
    except FileNotFoundError:
        print(f"错误：未找到小说文件 {filename}")
        return ""
    except Exception as e:
        print(f"加载小说出错：{e}")
        return ""

def count_name_occurrences(names, content):
    """统计人名出现次数"""
    count_dict = defaultdict(int)
    for name in names:
        if not name.strip():
            continue
        # 使用正则表达式匹配，确保只匹配中文名字
        pattern = re.compile(re.escape(name))
        count = len(pattern.findall(content))
        count_dict[name] = count
    # 打印前10个非零计数
    non_zero = [(name, count) for name, count in count_dict.items() if count > 0]
    non_zero.sort(key=lambda x: x[1], reverse=True)
    print("人名出现次数统计完成")
    if non_zero:
        print("前10个非零计数：")
        for name, count in non_zero[:10]:
            print(f"{name}: {count} 次")
    else:
        print("没有名字在小说中出现")
    return count_dict

def filter_high_frequency(count_dict, threshold=100):
    """筛选高频人物"""
    high_freq = {k: v for k, v in count_dict.items() if v > threshold}
    return sorted(high_freq.items(), key=lambda x: x[1], reverse=True)

def plot_high_frequency(high_freq_list, output_file="sg.jpg"):
    """绘制柱状图，确保中文显示"""
    if not high_freq_list:
        print("没有符合条件的高频人物（阈值=100）")
        return

    names = [item[0] for item in high_freq_list]
    counts = [item[1] for item in high_freq_list]

    plt.figure(figsize=(12, 8))
    bars = plt.bar(names, counts, color='lightgreen')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 2,
                 f"{height}", ha='center', va='bottom', fontsize=9)

    plt.title('《三国演义》中出现次数超过100次的人物', fontsize=14)
    plt.xlabel('人物名称', fontsize=12)
    plt.ylabel('出现次数', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()

    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"图表已保存为 {output_file}")
    plt.close()

def main():
    set_compatible_font()
    person_names = load_person_names("三国人名汇总.txt")
    novel_content = load_novel_content("三国演义.txt")
    if not person_names or not novel_content:
        return
    count_dict = count_name_occurrences(person_names, novel_content)
    high_freq_list = filter_high_frequency(count_dict, threshold=100)
    plot_high_frequency(high_freq_list)

if __name__ == "__main__":
    try:
        import chardet
    except ImportError:
        print("安装 chardet 库...")
        os.system("pip install chardet")
        import chardet
    main()