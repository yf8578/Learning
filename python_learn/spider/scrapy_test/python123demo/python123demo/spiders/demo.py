"""
Author: Zhangyifan
Date: 2023-09-09 23:40:43
LastEditors: Zhangyifan 1069624549@qq.com
LastEditTime: 2023-09-10 11:19:25
FilePath: //spider//scrapy_test//python123demo//python123demo//spiders//demo.py
Description: 

"""
import scrapy


class DemoSpider(scrapy.Spider):
    name = "demo"
    allowed_domains = ["python123.io"]
    start_urls = ["https://python123.io/ws/demo.html"]

    def parse(self, response):  # 解析函数
        fname = response.url.split("/")[-1]  # 提取网页文件名
        with open(fname, "wb") as f:
            f.write(response.body)
        self.log("Saved file %s." % fname)  # 日志文件
        pass
