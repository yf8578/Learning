"""
@Author: Zhangyifan
@Date: 2023-10-12 10:35:10
@LastEditors: Zhangyifan 1069624549@qq.com
@LastEditTime: 2023-10-14 16:13:44
@FilePath: //youdao_words//youdao_words//items.py
@Description: 
@
"""
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YoudaoWordsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    word_title = scrapy.Field()
    word_store = scrapy.Field()
