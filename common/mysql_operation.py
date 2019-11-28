# -*-coding:utf-8-*-
"""
@Desc:
@version: 1.0
@author:
@file name: mysql_operation.py
@date: 2019/10/24 14:08
"""

from common.read_config import ReadConfig
from common.log import logger
import pymysql


class ConnMysql:
    readeConfigObj = ReadConfig("\\data\\db.ini")

    def __init__(self):
        self.host = self.readeConfigObj.get_config('db', 'db_host')
        self.port = self.readeConfigObj.get_config('db', 'db_post')
        self.user = self.readeConfigObj.get_config('db', 'db_user')
        self.passwd = self.readeConfigObj.get_config('db', 'db_password')
        self.datatable = self.readeConfigObj.get_config('db', 'db_datatable')
        self.log = logger
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=int(self.port),
                user=self.user,
                passwd=self.passwd,
                db=self.datatable)
            self.cur = self.conn.cursor()
        except pymysql.err.OperationalError as e:
            logger.error('数据库连接错误', e)

    def do_execute(self, query):
        """
        查询操作
        :param query: 相关sql
        :return:
        """
        try:
            result_db = self.cur.execute(query)
            return result_db
        except Exception as e:
            self.log.error('查询命令错误', e)

    def fetch_all_rows(self):
        """接收全部的返回结果行"""
        return self.cur.fetchall()

    def fetch_one_row(self):
        """获取下一个查询结果集.
        如果select本身取的时候有多条数据时,将只取最上面的第一条结果，返回单个元组如('id','title')，
        然后多次使用cursor.fetchone()，依次取得下一条结果，直到为空。
        """
        return self.cur.fetchone()[0]

    def close(self):
        """关闭数据库"""
        self.conn.close()

    def get_info(self, query):
        try:
            self.do_execute(query)
            return self.cur.fetchone()[0]
        except Exception as e:
            self.log.error("*** Fetchone failure ***")
            raise e

    def get_infos(self, query):
        """获取所有的查询结果"""
        # _tmp = []
        try:
            self.do_execute(query)
            # for item in self.cur.fetchall():
            #     _tmp.append(item[0])
            # return _tmp
            return self.cur.fetchall()
        except Exception as e:
            self.log.error("*** Fetchall failure ***")
            raise e


if __name__ == '__main__':
    conn = ConnMysql()
    from data import sql_constants
    result_tmp = conn.get_infos(sql_constants.risk_on_address('3下905里工作面'))
    print(tuple(result_tmp))
    address_list_db = []  # 将获取到的数据转化为list
    for items in result_tmp:
        for item in items:
            address_list_db.append(item)
    print(address_list_db)
