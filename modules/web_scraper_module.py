# Module: web scraper
# Description: Scraping data from network
# Usage:
# Dependencies: 
import logging, aiohttp
from bs4 import BeautifulSoup
import json
import configs as Configs
#from library import sqlite_manager

log = logging.getLogger('web')

async def get_live_data():
    url = Configs.WEB_HOLOLIVE_SCHEDULE
    html_content = await get_data_from_url(url)
    if html_content:
        schedule_data = parse_html_to_schedule_data(html_content)
        # 在这里处理数据，可以传递给解析和处理HTML内容的方法

async def get_data_from_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html_content = await response.text(encoding='utf-8')
                return html_content
            else:
                # 请求失败，可以根据需要处理其他状态码
                return None  # 或者抛出异常等

def parse_html_to_schedule_data(html_content):
    print()
    soup = BeautifulSoup(html_content, 'html.parser')

    # 在这里根据HTML的结构和标签，编写代码以提取所需数据
    # 以下只是一个示例，请根据你的实际需求进行更改

    # 假设你想提取标题和链接
    data = []
    for article in soup.find_all('article'):
        title = article.find('h2').text
        link = article.find('a')['href']
        data.append({'title': title, 'link': link})

    return data

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)



