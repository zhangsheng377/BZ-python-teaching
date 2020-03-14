from pymongo import MongoClient, errors  # 树莓派只能通过pip安装3.2版本

from ._DataBase import DataBase


class DataBasePyMongo(DataBase):
    def __init__(self, database_name, sheet_name):
        self._client = MongoClient()
        self._databese = self._client[database_name]
        self._sheet = self._databese[sheet_name]

    def insert(self, document):
        ''' pymongo sheet.insert_one里面用_id表示key
        '''
        try:
            self._sheet.insert_one(document=document)
            return True
        except errors.DuplicateKeyError as e:
            pass
        return False

    def find(self, filter=None, sort=None):
        return self._sheet.find(filter=filter, sort=sort)

    def find_one(self, filter=None, sort=None):
        return self._sheet.find_one(filter=filter, sort=sort)

    # 未经测试
    def update_one(self, filter, update):
        return self._sheet.insert_one(filter=filter, update=update)

    def delete(self, filter):
        return self._sheet.delete_many(filter=filter)
