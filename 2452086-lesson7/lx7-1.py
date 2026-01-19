# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
import re
import os
from urllib.parse import urljoin
from openpyxl import load_workbook
#import sys

# 配置
base_url = "https://see.tongji.edu.cn"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
LINKS_CSV = "news_links.csv"
DATA_CSV = "news_data.csv"

def append_to_excel(data: list, file_path: str, columns: list):
    """将数据追加到已有的excel中"""
    # 先将list转换为DataFrame
    df = pd.DataFrame(data, columns=columns)
    
    if os.path.exists(file_path):
        try:
            # 加载现有文件
            book = load_workbook(file_path)
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                # 获取现有数据的最后一行
                existing_df = pd.read_excel(file_path)
                start_row = len(existing_df) + 1  # 从下一行开始
                
                # 追加数据（不包含header）
                df.to_excel(writer, sheet_name='Sheet1', startrow=start_row, index=False, header=False)
        except Exception as e:
            print(f"追加Excel时出错: {e}")
            # 如果追加失败，重新创建文件
            df.to_excel(file_path, index=False)
    else:
        # 创建新文件
        df.to_excel(file_path, index=False)
            
def get_news_links(force_update=False):
    """
    获取所有新闻链接并保存到CSV
    Args:
        force_update (bool): 是否强制重新爬取
    Returns:
        list: 新闻链接列表
    """
    # 如果已有CSV且不强制更新
    if not force_update and os.path.exists(LINKS_CSV):
        df = pd.read_csv(LINKS_CSV)
        print(f"从 {LINKS_CSV} 加载 {len(df)} 条历史链接")
        return df['url'].tolist()
    
    news_links = []
    page = 1
    max_page = 193  # 根据实际情况调整
    
    while page <= max_page:
        if page - 1 > 0:
            list_url = f"{base_url}/index/xyxw/{page - 1}.htm" 
        else:
            list_url = "https://see.tongji.edu.cn/index/xyxw.htm"
            
        print(f"正在抓取列表页: {list_url}")
        
        try:
            response = requests.get(list_url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 多模式匹配新闻链接
            news_items = (
                soup.select('ul.list-news li a') or
                soup.select('div.news-list a') or
                soup.select('div.list li a') or
                [a for a in soup.find_all('a', href=True) 
                 if re.search(r'info/\d+/\d+\.htm', a['href'])]
            )
            
            if not news_items:
                print(f"第 {page} 页未找到新闻链接，终止爬取")
                break

            # 提取并处理链接
            page_links = []
            for item in news_items:
                href = item.get('href')
                if href:
                    full_url = urljoin(base_url, href)
                    if full_url not in news_links and full_url not in page_links:
                        page_links.append(full_url)
            
            news_links.extend(page_links)
            print(f"第 {page} 页获取到 {len(page_links)} 条链接 (累计: {len(news_links)})")
            
            # 每5页保存一次进度
            if page % 5 == 0:
                pd.DataFrame({'url': news_links}).to_csv(LINKS_CSV, index=False)
            
            page += 1
            time.sleep(1.5)  # 礼貌爬取
            
        except Exception as e:
            print(f"第 {page} 页抓取失败: {str(e)[:100]}...")
            time.sleep(5)  # 失败后延长等待
    
    # 最终保存
    pd.DataFrame({'url': news_links}).to_csv(LINKS_CSV, index=False)
    return news_links

def crawl_news_page(use_cached_links=True, resume=False):
    """
    爬取新闻详情页
    Args:
        use_cached_links (bool): 是否使用已保存的链接
        resume (bool): 是否从上次中断处继续
    Returns:
        pd.DataFrame: 包含所有新闻数据的DataFrame
    """
    # 定义列名
    COLUMNS = ['标题', '编辑', '发布时间', '浏览量', '正文', '链接', '抓取时间']
    EXCEL_FILE = 'tjnews.xlsx'
    
    # 加载或获取新闻链接
    news_links = pd.read_csv('news_links.csv')
    news_links = news_links['url'].tolist()
    
    data = []
    total = len(news_links)
    
    # 如果是从中断处继续，先加载已有数据
    if resume and os.path.exists(EXCEL_FILE):
        try:
            existing_df = pd.read_excel(EXCEL_FILE)
            processed_urls = existing_df['链接'].tolist()
            news_links = [url for url in news_links if url not in processed_urls]
            print(f"从上次中断处继续，剩余 {len(news_links)} 条待处理")
        except Exception as e:
            print(f"无法读取现有Excel文件，重新开始爬取: {e}")
    
    # 设置 Selenium WebDriver（使用 Headless 模式）
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 启用 Headless 模式
    options.add_argument("--disable-gpu")  # 禁用 GPU（可选，解决某些兼容性问题）
    options.add_argument("--no-sandbox")  # 避免沙箱模式（可选，视系统而定）
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for i, url in enumerate(news_links, 1):
        print(f"[{i}/{total}] 正在抓取: {url[:60]}...")
        
        try:
            # 使用 Selenium 加载页面
            driver.get(url)
            
            # 等待动态元素加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[id*="dynclicks"]'))
            )
            
            # 获取渲染后的页面源代码
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # 标题提取
            title = soup.find('h3').get_text(strip=True) if soup.find('h3') else "无标题"
            
            # 信息栏提取
            info_div = soup.find('div', style="text-align:center; margin-top:10px;")
            editor = "未找到"
            publish_time = "未找到"
            views = "未找到"
            
            if info_div:
                full_text = info_div.get_text(strip=True, separator=' ')
                
                # 提取编辑信息
                editor_match = re.search(r'编辑：\s*((?!发)[\u4e00-\u9fa5]+)', full_text)
                editor = editor_match.group(1) if editor_match else "未找到"

                # 提取发表时间
                time_match = re.search(r'发表时间：\s*(\d{4}-\d{2}-\d{2})', full_text)
                publish_time = time_match.group(1) if time_match else "未找到"
                
                # 提取浏览次数
                views_span = info_div.find('span', id=re.compile(r'dynclicks.*'))
                if views_span:
                    views = views_span.get_text(strip=True)
                    print(f"提取到的浏览量：{views}")
                else:
                    print("未找到 <span> 元素")
                    print("info_div 内容：")
                    print(info_div.prettify())  # 打印以调试
            
            # 正文清理
            content_div = soup.find("div", class_="v_news_content")
            if content_div:
                for elem in content_div.select('script, style, iframe, .ad, img, .footer'):
                    elem.decompose()
                content = content_div.get_text('\n', strip=True)
            else:
                content = "无正文"
            
            data.append({
                '标题': title,
                '编辑': editor,
                '发布时间': publish_time,
                '浏览量': views,
                '正文': content,
                '链接': url,
                '抓取时间': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            # 每5条保存一次到Excel
            if i % 5 == 0 and data:
                append_to_excel(data, EXCEL_FILE, COLUMNS)
                print(f"已保存 {len(data)} 条数据到 {EXCEL_FILE}")
                data = []  # 清空临时数据
            
            time.sleep(1.2)
            
        except Exception as e:
            print(f"抓取失败 [{url[:30]}...]: {str(e)[:100]}...")
            time.sleep(5)
    
    # 保存剩余的数据
    if data:
        append_to_excel(data, EXCEL_FILE, COLUMNS)
        print(f"已保存剩余 {len(data)} 条数据到 {EXCEL_FILE}")
    
    # 关闭 WebDriver
    driver.quit()
    
    print("所有数据已保存到 tjnews.xlsx")
    return pd.read_excel(EXCEL_FILE)

if __name__ == "__main__":
    
    #生成全部连接的csv
    get_news_links()
    
    #从csv中提取链接，将爬取内容保存到tjnews.xlsx 中
    df = crawl_news_page()
    

    print("爬取完成！结果已保存到 tjnews.xlsx")