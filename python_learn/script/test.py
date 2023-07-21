# -*- coding: UTF-8 -*-
import argparse
import sys
import os
import json

parser = argparse.ArgumentParser(
    # prog="test.py", # 程序名，默认为sys.argv[0]
    # usage="%(prog)s [options] [arg]",  # 描述程序用途的字符串
    formatter_class=argparse.RawTextHelpFormatter,  # 让desscription支持换行
    description="""
    ##################################
    # Cell Free RNA Analysis Pipeline#
    ##################################
    """,
    # description=line1 + "\n" + line2 + "\n" + line3,  # help时显示的开始文字
    epilog="See more at http://www.baidu.com",  # help时显示的结尾文字
)
parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
parser.add_argument("-j", "--json", type=str, help="流程配置文件", required=True)
parser.add_argument("-i", "--inputfile", type=str, help="输入文件", required=True)
parser.add_argument("-o", "--outputfile", type=str, help="输出文件", required=True)
# 解析参数
args = parser.parse_args()

jsonfile = args.json
inputfile = args.inputfile

##handle with jsonfile
with open(jsonfile, "r") as con_file:
    conf_json = json.load(con_file)


## handle with inputfile

with open(inputfile, "r") as f:
    for line in f.readlines():
        line = line.strip()
        sample, input1, input2 = line.split(" ")

        # Filter
print(conf_json["Software"]["bwa"])
# print(type(con_file))
print(type(f))

# ##pipeline
# ## 1.1 fastp cut adapter
