from UA import Agents
from COOKIES import Cookies
from SENTA import SentaFactory
from BLACKLIST import blackList

import time
import requests
import random
import json
import re
from pymongo import MongoClient, errors  # 树莓派只能通过pip安装3.2版本
import pandas as pd


api_url = 'https://xueqiu.com/statuses/search.json?sort=time&source=all&q=01810&count=10&page=1'


def scrapy_xueqiu(needSaveToCsv=False):
    headers = {
        'User-Agent': Agents().get_random_agent()
    }

    session = requests.session()

    session.cookies = Cookies(headers=headers).cookie

    api_request = session.get(url=api_url, headers=headers, timeout=10)
    if api_request.status_code != 200:
        print("api_request.status_code", api_request.status_code)
        return

    json_api_request = json.loads(api_request.text)
    list_data = json_api_request['list']

    senta = SentaFactory(model="snownlp")

    with MongoClient() as client:
        databese = client["xueqiu"]
        sheet = databese["comments"]
        for comment in list_data:
            sub_text = re.sub(u"<.*?>|\\$.*?\\$|\\&nbsp\\;",
                              "", comment['text'])
            sub_text = sub_text.strip()

            if sub_text == "":
                continue

            if comment['user_id'] in blackList and '小米' not in sub_text:
                continue

            last_record_text = sheet.find_one(sort=[('_id', -1)])['text']
            if sub_text == last_record_text:
                print('丢弃重复最新内容\n')
                continue

            senta_score = senta.sentiments(doc=sub_text)

            try:
                # sheet.insert_one里面用_id表示key
                sheet.insert_one({'_id': comment['id'], 'user_id': comment['user_id'], 'time': comment['created_at'],
                                  'text': sub_text, 'snownlp_senta': senta_score, 'raw': str(comment)})
                print(sub_text, senta_score)
                print(comment['id'], comment['user_id'], '评论插入成功\n')
            except errors.DuplicateKeyError as e:
                print(comment['id'], '已经存在于数据库\n')
                pass
        if needSaveToCsv:
            df = pd.DataFrame(list(sheet.find(sort=[('_id', -1)])))
            df.set_index(keys='_id', inplace=True)
            df.to_csv("data_pd.csv")


def timedTask(gapSecond=1200):
    while True:
        scrapy_xueqiu(needSaveToCsv=True)
        sleepSecond = gapSecond + random.randint(0, 300)
        print(time.asctime(time.localtime(time.time())),
              "    sleep {} s".format(sleepSecond))
        time.sleep(sleepSecond)


if __name__ == '__main__':
    timedTask()
