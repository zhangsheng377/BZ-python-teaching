from UA import agents

import time
import requests
import random
import pickle
import json
import re
from pymongo import MongoClient, errors  # 树莓派只能通过pip安装3.2版本
import pandas as pd

index_url = 'https://xueqiu.com/'
api_url = 'https://xueqiu.com/statuses/search.json?sort=time&source=all&q=01810&count=10&page=1'


def get_and_save_cookis(session, headers):
    first_request = session.get(url=index_url, headers=headers, timeout=10)
    with open("COOKIES", 'wb') as f:
        pickle.dump(first_request.cookies, f)
    return first_request.cookies


def scrapy_xueqiu(needSaveToCsv=False):
    headers = {
        'User-Agent': random.choice(agents)
    }

    session = requests.session()

    try:
        with open("COOKIES", 'rb') as f:
            cookie_ = pickle.load(f)
    except:
        cookie_ = get_and_save_cookis(session, headers)

    session.cookies = cookie_

    api_request = session.get(url=api_url, headers=headers, timeout=10)
    if api_request.status_code != 200:
        session.cookies = get_and_save_cookis(session, headers)
        api_request = session.get(url=api_url, headers=headers, timeout=10)

    json_api_request = json.loads(api_request.text)
    list_data = json_api_request['list']

    with MongoClient() as client:
        databese = client["xueqiu"]
        sheet = databese["comments"]
        for comment in list_data:
            sub_text = re.sub(u"<.*?>|\\$.*?\\$|\\&nbsp\\;",
                              "", comment['text'])
            sub_text = sub_text.strip()
            last_record_text = sheet.find_one(sort=[('_id', -1)])['text']
            if sub_text == last_record_text:
                print('丢弃重复最新内容\n')
                continue

            try:
                # sheet.insert_one里面用_id表示key
                sheet.insert_one({'_id': comment['id'], 'user_id': comment['user_id'],
                                  'time': comment['created_at'], 'text': sub_text, 'raw': str(comment)})
                print(sub_text)
                print(comment['id'], '评论插入成功\n')
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
        time.sleep(gapSecond + random.randint(0, 300))


if __name__ == '__main__':
    timedTask()
