# -*- coding: utf-8 -*-


import pymongo


class LianJiaWangPipeline(object):
    def __init__(self):
        # 连接
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        # 数据库
        db = client['LianJiaWang']
        # 集合
        self.collection = db['ErShouFang']

    def process_item(self, item, spider):
        # 存入数据库
        self.collection.insert_one(item)
        return item
