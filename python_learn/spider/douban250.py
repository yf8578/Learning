"""
Author: zhangyifan1
Date: 2023-08-24 22:23:43
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2023-08-26 09:45:27
FilePath: //spider//douban250.py
Description: 爬取豆瓣电影top250

"""
# import libs
import requests
from bs4 import BeautifulSoup
from lxml import etree
import csv


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()  # 如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        print("success")
        return r.text
    except:
        print("error")  # 异常处理
        return "产生异常"


def getMovieList(lst, movielist):
    return ""


def getMovieInfo(lst, movielist, path):
    return ""


def main():
    url = r"https://movie.douban.com/top250"
    getHTMLText(url)


if __name__ == "__main__":
    main()
