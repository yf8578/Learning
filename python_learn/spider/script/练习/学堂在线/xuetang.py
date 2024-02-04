'''
Author: zhangyifan1
Date: 2024-02-04 15:25:58
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-02-04 15:29:50
FilePath: //学堂在线//xuetang.py
Description: 

'''
from IPython.display import Image
from bs4 import BeautifulSoup
import requests
import os

# 访问网页部分
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}


def getHTMLText(url):
    try:
        r = requests.get(url, headers)
        r.encoding = r.apparent_encoding
        # print(r.status_code)#输出访问状态码
        r.raise_for_status()  # 访问成功时不会返回任何值，因此print输出内容为None；主要用途是在请求失败时抛出异常
        print("step one done!!")
        return r.text
    except requests.exceptions.HTTPError as e:
        print("Error" + str(e))


# 解析网页，开始make soup
# 使用xpath来解析
def getClassList(html):
    My_data = {}
    Mysoup = BeautifulSoup(html, "lxml")
    # //*[@id="app"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/p[1]
    # app > div > div.app-main_.appMain > div.universityAll > div.list > div:nth-child(1)
    # School_name = Mysoup.find_all("div", class_="list")
    School_name=Mysoup.select('#app > div > div.app-main_.appMain > div.universityAll > div.list > div:nth-child(1)')
    print(School_name)


def main():
    url = "https://www.xuetangx.com/university/all"
    # url='https://chat.openai.com/c/0d193613-ee38-443b-9dba-93a70d8eef01'
    html = getHTMLText(url)
    print(html)
    getClassList(html)


if __name__ == "__main__":
    main()
