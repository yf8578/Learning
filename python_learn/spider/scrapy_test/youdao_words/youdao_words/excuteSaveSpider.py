"""
@Author: Zhangyifan
@Date: 2023-10-13 15:24:03
@LastEditors: Zhangyifan 1069624549@qq.com
@LastEditTime: 2023-10-14 16:54:56
@FilePath: //youdao_words//youdao_words//excuteSaveSpider.py
@Description: 
@
"""
from scrapy import cmdline

cmdline.execute("scrapy crawl youdao_words -o word_transtext.csv".split())

# print(123)
# print(123412)
