# -*- coding: utf-8 -*-
# @Time    : 2024/10/24 下午3:56
# @Author  : xiaojing
# @File    : MySql_Utils.py
# @Software: PyCharm

import pymysql
from dbutils.pooled_db import PooledDB


class MysqlUtil(object):

    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示无限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和mysqldb的模块都不支持共享链接
            blocking=True,  # 连接池中如果没有可用链接后，是否阻塞等待。False，不等待直接报错；True，等待直到有可用链接，再返回。
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            database='dyls',
            charset='utf8'
        )
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.pool.close()
        # self.db.close()

    def query(self, sql, param):
        # 从数据库连接池中获取一个链接
        conn = self.pool.connection()
        # # 获取游标
        cursor = conn.cursor()
        cursor.execute(sql, param)
        return cursor.fetchall()

    def insert_one(self, sql, data):
        # 从数据库连接池中获取一个链接
        conn = self.pool.connection()
        cursor = conn.cursor()
        # 获取游标
        try:
            cursor.execute(sql, data)
            conn.commit()
            print('数据保存成功:')
        except Exception as e:
            print('数据保存失败:', e, data)
            conn.rollback()

    def insert_Many(self, sql, datas):
        # 从数据库连接池中获取一个链接
        conn = self.pool.connection()
        cursor = conn.cursor()
        # 获取游标
        try:
            cursor.executemany(sql, datas)
            conn.commit()
            print('数据保存成功:')
        except Exception as e:
            print('数据保存失败:', e, datas)
            conn.rollback()

    def create_table(self):
        sql = """
            create table if not exists movies(
                id varchar(20) primary key,
                name varchar(100) not null,
                cover varchar(200),
                dinamic varchar(100),
                type_name varchar(100),
                label varchar(20)
            );
        """
        try:
            # 从数据库连接池中获取一个链接
            # self.conn = self.pool.connection()
            # self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            print('表创建成功...')
        except Exception as e:
            print('表创建失败:', e)

        sql = """
                    create table if not exists details(
                        id varchar(20) primary key,
                        name varchar(100) not null,
                        area varchar(50),
                        cover varchar(200),
                        year varchar(10),
                        score varchar(10),
                        dynamic varchar(50),
                        content varchar(1000),
                        type_name varchar(20),
                        tags text,
                        play_from text
                    );
                """
        try:
            # 从数据库连接池中获取一个链接
            self.cursor.execute(sql)
            self.conn.commit()
            print('表details创建成功...')
        except Exception as e:
            print('表details创建失败:', e)


if __name__ == '__main__':
    mysql = MysqlUtil()
    retusn = mysql.query("select * from movies")
    print(retusn)
    mysql.excute_sql(
        'insert into movies values ("dfad", "消失的厨神", "https://t1.021huaying.com/uploads/2024-10-19/2f/a804b9bde895e38abb55905ead06467d.webp", "更新全集","" ,"多人收藏")')
    # mysql.create_table()
