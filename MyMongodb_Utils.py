# -*- coding: utf-8 -*-
# @Time    : 2024/10/24 下午4:36
# @Author  : xiaojing
# @File    : MyMongodb_Utils.py
# @Software: PyCharm
import pymongo


class MongoDBUtil(object):
    def __init__(self):
        self.client_mongo = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client_mongo['dyls']['movies']

    def insert_one(self, data):
        return self.db.insert_one(data)

    def insert_many(self, datas):
        return self.db.insert_many(datas)

    def find_one(self, query):
        return self.db.find_one(query)

    def find(self, query):
        return self.db.find(query)

    def update_one(self, query, new_data):
        return self.db.update_one(query, new_data)

    def update_many(self, query, new_data):
        return self.db.update_many(query, new_data)

    def delete_one(self, query):
        return self.db.delete_one(query)

    def delete_many(self, query):
        return self.db.delete_many(query)

    def close(self):
        self.client_mongo.close()