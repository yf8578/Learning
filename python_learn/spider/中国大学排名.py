# -*-encoding:utf-8-*-
"""
Author: zhangyifan1
Date: 2023-07-30 18:46:41
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2023-07-31 09:10:22
FilePath: //spider//中国大学排名.py
Description: 

"""
import requests
from bs4 import BeautifulSoup
import bs4


def getHTMLText(url):  # 访问网址
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()  # 如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        print(r.status_code)
        return r.text
    except:
        return "wrong"


def fillUnivList(ulist, html):  # 获取关键信息，添加到列表中
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find("tbody").children:
        if isinstance(tr, bs4.element.Tag):  # 因为标签中会存在字符串，所以需要过滤掉非标签类型的其他信息
            td = tr("td")
            print(td.string)
            # print(type(td))
        #     tds = tr("td")  # 对tr标签中的td标签进行筛选
        #     ulist.append([tds[0].string,tds[1].string,tds[2].string])


# def printUnivList(ulist, num):
#     print("{:^10}\t{:^6}\t{:^10}".format("排名", "学校名称", "总分"))
#     for i in range(num):
#         u = ulist[i]
#         print(u)
#     print("{:^10}\t{:^6}\t{:^10}".format(u[0], u[1], u[2]))
#     print("Suc" + str(num))


def main():
    unifo = []
    url = r"http://www.chinaxy.com/2022index/news/news.jsp?information_id=1930"
    html = getHTMLText(url)
    print("step1")
    # print(html)
    fillUnivList(unifo, html)
    # printUnivList(unifo, 20)  # get 20 universities


main()
