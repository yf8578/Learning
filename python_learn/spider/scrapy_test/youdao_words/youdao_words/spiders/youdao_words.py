"""
@Author: Zhangyifan
@Date: 2023-10-12 10:36:56
@LastEditors: Zhangyifan 1069624549@qq.com
@LastEditTime: 2023-10-15 16:45:48
@FilePath: //youdao_words//youdao_words//spiders//youdao_words.py
@Description: 
@
"""
# import libs
import time
import random
from bs4 import BeautifulSoup
import scrapy
from scrapy.loader import *
from scrapy.loader.processors import *
from youdao_words.items import YoudaoWordsItem


class YoudaoWordsSpider(scrapy.Spider):
    """爬取有道词典单词释义"""

    # sleep random time
    name = "youdao_words"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
        "537.36(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }

    def start_requests(self):
        with open(
            r"D:\000zyf\Master\Learning\英语A\main_words.txt",
            "r",
            encoding="utf-8",
        ) as f:
            words = f.readlines()
            for word in words:
                word = word.strip()
                url = f"https://www.youdao.com/result?word={word}&lang=en"
                yield scrapy.Request(
                    url=url, headers=self.headers, callback=self.parse_youdao
                )

    def parse_youdao(self, response):
        """解析单词释义"""
        # word_item = YoudaoWordsItem()
        # 要返回YoudaoWordsItem对象的数组
        items = []
        word_dict = {}
        word_store = []
        soup = BeautifulSoup(response.text, "lxml")
        word_list = soup.select("#catalogue_author > div.dict-book > div > div > ul")
        word_title = soup.select(
            "#searchLayout > div > div.search_result.center_container > div > div > section > "
            "div.simple-explain > div > div > div > div > div.title"
        )
        word_title = word_title[0].text.split("语速")[0]
        # 获取ul标签下的所有li 属性为word-exp的标签
        word_list = word_list[0].find_all("li", attrs={"class": "word-exp"})
        if len(word_list) == 0:
            yield "错误：未找到单词列表"
        else:
            for word in word_list:
                try:
                    word_class = word.find("span", attrs={"class": "pos"}).string
                    word_trans = word.find("span", attrs={"class": "trans"}).string
                    # 将word_class和word_trans储存到word_store列表中
                    word_store.append((word_class, word_trans))
                except AttributeError:
                    print(
                        f"{word_title}--错误：未找全单词释义"
                    )  # 我们指定了 AttributeError 异常类型，这是由于在 try 语句块中
                    # 使用了 find() 方法，如果找不到指定的标签，它将引发 AttributeError 异常
                    continue
            word_dict["word_store"] = str(word_store).replace("[", "").replace("]", "")
            word_dict["word_title"] = word_title
            # print(word_dict)
            # print(word_store)
            word_item = YoudaoWordsItem(word_title=word_title, word_store=word_store)
            # 获取一个word_item对象,就将其传入pipeline.py中
            yield word_item

            time.sleep(random.randint(1, 5))
