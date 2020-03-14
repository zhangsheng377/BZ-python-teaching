from pymongo import MongoClient, errors  # 树莓派只能通过pip安装3.2版本
import pandas as pd
import re

from BlackList import blackList

# 模糊匹配查询
# 在mongo中这样实现
# {'filed':/value/}


p = re.compile(r'^((?!小米).)*$')
# p = re.compile(r'^(?!.*小米)')
print(p.search("error123abc"))
print(p.search("小米error123abc"))
print(p.search("error1小米23abc"))
print(p.search("小米error123abc小米"))

with MongoClient() as client:
    databese = client["xueqiu"]
    sheet = databese["comments"]
    for blackUserId in blackList:
        # print(sheet.find_one({'user_id': blackUserId,
        #                   'text': {'$regex': '小米'}}, {'text': 1}))
        # try:
        #print(sheet.find_one({'user_id': blackUserId,'text': {'$regex': '(!小米)'}}, {'text': 1}))
        #print(sheet.find_one({'user_id': blackUserId,'text': {'$regex': p}}, {'text': 1}))
        #   pass
        # except:
        #   print('不包含小米的 user_id:{} 清理完成.'.format(blackUserId))
        data_list = list(sheet.find({'user_id': blackUserId}))
        print(len(data_list))
        # print(type(data_list[0]))
        # print(data_list[0]['_id'],data_list[0]['text'])
        #coutn =0
        for data in data_list:
            if '小米' not in data['text']:
             #       coutn+=1
              #      print(data['_id'])
                sheet.delete_one({'_id': data['_id']})
        # print(coutn)
        data_list = list(sheet.find({'user_id': blackUserId}))
        print(len(data_list))
