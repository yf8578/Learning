"""
Author: zhangyifan1
Date: 2023-07-30 18:46:41
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2023-07-31 11:39:00
FilePath: //spider//中国大学排名.py
Description: 

"""
# -*-encoding:utf-8-*-
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
    # text = soup.tbody.tr.td.p
    # print(text)
    for tr in soup.find("tbody").children:
        # print(tr)
        #     print("next line")
        # print(tr)
        if isinstance(tr, bs4.element.Tag):  # 因为标签中会存在字符串，需要过滤掉非标签类型的其他信息
            td = tr("td")
            # print(td[1].p.string)
            # print(t)
            ulist.append(
                [td[0].p.string, td[1].p.string, td[2].p.string, td[3].p.string]
            )


def printUnivList(ulist, num):
    # print("{:^10}\t{:^6}\t{:^10}".format("排名", "学校名称", "总分"))
    for i in range(num):
        u = ulist[i]
        # print(u)
        print("{:^10}\t{:^6}\t{:^10}\t{:^6}".format(u[0], u[1], u[2], u[3]))
    print("Suc" + str(num - 1))


def main():
    unifo = []
    url = r"http://www.chinaxy.com/2022index/news/news.jsp?information_id=1930"
    html = getHTMLText(url)
    print("step1")
    # print(html)
    fillUnivList(unifo, html)
    printUnivList(unifo, 21)  # get 20 universitiesasf


if __name__ == "__main__":
    main()
