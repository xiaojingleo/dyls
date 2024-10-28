# -*- coding: utf-8 -*-
# @Time    : 2024/10/23 上午11:47
# @Author  : xiaojing
# @File    : dyls.py
# @Software: PyCharm
import datetime
import json
import random
import time
from asyncio import as_completed
from concurrent.futures import ThreadPoolExecutor, as_completed

import Utils
import MyMongodb_Utils
import MySql_Utils


class Dyls:
    def __init__(self):
        self.utils = Utils.Utils()
        self.mogo_utils = MyMongodb_Utils.MongoDBUtil()
        self.mysql_utils = MySql_Utils.MysqlUtil()

    def get_movies(self, page):
        result = self.utils.get_list("36", page)
        json_data = json.loads(result)
        print(json_data['data']['list'])

    def get_work_info(self, type_id, page):
        response = self.utils.get_list(type_id, page)
        return type_id, response

    def get_work_detail(self, type_id):
        result = self.mysql_utils.query("select count(id) from movies where type_name=%s ", type_id)
        count = result[0][0]
        return count

    def parse_work_info(self, type_name, response, db_type="mongodb"):
        try:
            response = json.loads(response)
        except Exception as e:
            print(e)
            return None
        works = response['data']['list']
        if works is None:
            print("下载完成")
            return None
        # print(works)
        match db_type:
            case "mongodb":
                # 写入mongoDb
                self.seve_to_mongo(works)
            case _:
                # 写入mysql
                sql = 'insert ignore into movies (id,name,cover,dinamic,type_name,label) value (%s,%s,%s,%s,%s,%s)'
                datas = []
                for work_info in works:
                    type_name = work_info['type_name'] if work_info['type_name'] else type_name
                    name = work_info['name'] if work_info['name'] else ''
                    id = work_info['id'] if work_info['id'] else ''
                    dynamic = work_info['dynamic'] if work_info['dynamic'] else ''
                    cover = work_info['cover'] if work_info['cover'] else ' '
                    label = work_info['label'] if work_info['label'] else ' '
                    datas.append((id, name, cover, dynamic, type_name, label))

                self.save_work_info(sql, datas)

    def parse_work_detail(self, type_id):
        result = self.mysql_utils.query("select id from movies where type_name=%s ", type_id)
        for row in result:
            id = row[0]
            response = self.utils.get_detail(id)
            response = json.loads(response)
            sql = 'insert into details (id,name,area,cover,year,score,dynamic,content,type_name,tags,play_from) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
            if response['msg'] == '获取成功':
                json_data = response['data']
                if json_data is not None:
                    id = json_data['id']
                    name = json_data['name']
                    area = json_data['area']
                    cover = json_data['cover']
                    year = json_data['year']
                    score = json_data['score']
                    dynamic = json_data['dynamic']
                    content = json_data['content']
                    type_name = json_data['type_name']
                    tags = json.dumps(json_data['tags'])
                    play_from = json.dumps(json_data['play_from'])
                    print(id, name, area, cover, year, score, dynamic, content, type_name, tags, play_from)
                    self.mysql_utils.insert_one(sql, (id, name, area, cover, year, score, dynamic, content, type_name, tags, play_from))

            time.sleep(random.randint(1, 3)/100)

    def save_work_info(self, sql, datas):
        # sql = 'insert into movies values ("%s","%s","%s","%s","%s","%s")'
        # sql = sql % args
        self.mysql_utils.insert_Many(sql, datas)

    def seve_to_mongo(self, datas):
        self.mogo_utils.insert_many(datas)

    def create_table(self):
        self.mysql_utils.create_table()

    def main(self):
        self.create_table()
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = [pool.submit(self.get_work_info, "26", page) for page in range(50, 100)]
            for future in as_completed(futures):
                pool.submit(self.parse_work_info, future.result()[0], future.result()[1], "mongodb")

    def get_detail(self):
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = [pool.submit(self.parse_work_detail, type_id) for type_id in ["1", "2", "3", "4", "36", "26"]]
            # for future in as_completed(futures):
            #     pool.submit(self.parse_work_detail, future.result())
            #     print(future.result())


if __name__ == '__main__':
    dyls = Dyls()
    # dyls.create_table()
    # dyls.get_detail()
    print(dyls.utils.get_play_url("An1Mp", "heimuer","parse_30a8f9bcff2a0772ffd1fc257e25375369c575a517c1d124f6350a2e27dd386afdf9c0833ba60f38da48b31f79d2d7fadbf90cbe",'13283680'))
