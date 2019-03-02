# #-*-coding=utf8-*-
from lxml import etree
import requests
from bs4 import BeautifulSoup


# 1.获取股票编号且URL
def gethtml(url, count):
    count = count
    try:
        # 获取url
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"
        }
        Html = requests.get(url=url, headers=headers, timeout=30)
        # 检查状态码
        print(Html.status_code)
        Html.raise_for_status()
        # 解决编码问题
        if count == 0:
            return Html.text
        if count == 1:
            return Html.content.decode('utf-8')
    except:
        return "获取失败"


# 2.解析获取后的URL的高开低收
def html_list(text, item):
    soup = BeautifulSoup(text, 'html.parser')

    for i in soup.find_all("div", attrs={"class": "quotebody"}):
        for x in i.find_all('a')[3:-1]:
            try:
                # 保存到字典里
                # {'sh201000': 'http://quote.eastmoney.com/sh201000.html'}
                item[(x['href'].split('/')[-1]).split('.')[0]] = x['href']
            except:
                continue
                # 获取单个url的信息

# 解析每个URL返回的数据且编辑类型
def Html_item(item):
    new_list = []
    for k, v in item.items():
        text = gethtml(url=v, count=1)
        soup = BeautifulSoup(text, 'html.parser')
        for i in soup.find_all('div', attrs={"class", "box-x1 line24"}):
            for j, y in i.find_all('td'):
                # < span class ="zxj" > - < / span >
                # 获取span的内容
                new_list.append([k + j, y.span])

    return print(new_list)


def main():
    item = {}
    url = 'http://quote.eastmoney.com/stocklist.html'
    Html = gethtml(url, count=0)
    html_list(Html, item)
    Html_item(item)


main()
