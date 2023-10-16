"""
@Author: Zhangyifan
@Date: 2023-10-12 10:35:10
@LastEditors: Zhangyifan 1069624549@qq.com
@LastEditTime: 2023-10-15 16:45:43
@FilePath: //youdao_words//youdao_words//pipelines.py
@Description: 
@
"""
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import csv
class YoudaoWordsPipeline:
    # 打开文件
    def open_spider(self, spider):
        self.output = open("main_words.txt", "w", encoding="utf-8")
        #item就是yield返回的word_item对象
        
    def process_item(self, item, spider):
        word_title = item["word_title"]
        word_store = item["word_store"]
        word_store = str(word_store).replace(']', '').replace('[', '').replace("'", '')
        self.output.write(str(word_title) +'\t'+ word_store +"\n")
        return item

    # 关闭文件
    def close_spider(self, spider):
        self.output.close()
