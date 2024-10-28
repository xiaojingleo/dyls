# -*- coding: utf-8 -*-
# @Time    : 2024/10/24 下午8:27
# @Author  : xiaojing
# @File    : sql_test.py
# @Software: PyCharm
import pymysql

data01 = [['1', 'Ada', '23'],
          ['2', 'Black', '19'],
          ['3', 'Tim', '30']]

data02 = [('4', 'Green', '25'), ('5', 'Bai', '32')]

db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     password='123456',
                     database='dyls',
                     charset='utf8')

cur = db.cursor()

try:
    sql = 'select * from test;'
    cur.execute(sql)
    print(cur.fetchall())
    sql = 'insert into test values(%s, %s, %s);'
    # cur.executemany(sql, data01)
    cur.executemany(sql, data02)

    db.commit()
    print('成功...')
except Exception as e:
    db.rollback()
    print("错误信息:", e)
cur.close()
db.close()