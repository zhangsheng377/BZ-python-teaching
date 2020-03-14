from pymongo import MongoClient, errors  # 树莓派只能通过pip安装3.2版本
import pandas as pd
import re

# 模糊匹配查询
# 在mongo中这样实现
# {'filed':/value/}


with MongoClient() as client:
    databese = client["xueqiu"]
    sheet = databese["comments"]

    data_list = list(sheet.find())
    print(len(data_list))

    sheet.find_one_and_delete({'text': ""})

    data_list = list(sheet.find())
    print(len(data_list))
