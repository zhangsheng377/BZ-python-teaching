from pymongo import MongoClient, errors # 树莓派只能通过pip安装3.2版本
from snownlp import SnowNLP
import re

with MongoClient() as client:
    databese = client["xueqiu"]
    sheet = databese["comments"]
    for data in sheet.find():
        print(data)

