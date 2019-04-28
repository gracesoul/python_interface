# -*- coding: utf-8 -*-
# @time:2019/4/19 21:47
# Author:殇殇
# @file:do_mysql.py
# @fuction: 数据库的操作与封装,从配置文件中读取
import pymysql
# from interface_practice.common.mysql_config import ReadConfig
from interface_practice.common.config import ReadConfig
config = ReadConfig()
'''
1.建立连接：数据库的连接信息（host,user,password,port）
2.新建一个查询页面
3.编写SQL
4.执行SQL
5.查看结果
6.关闭查询
7.关闭数据库连接
'''
class DoMysql:

    def __init__(self):
        # host='test.lemonban.com'
        # db_username = 'test'
        # db_password = 'test'
        # db_name = 'future'
        # db_port = 3306
        host = config.get_strvalue('db_test','db_host')
        db_username = config.get_strvalue('db_test','db_username')
        db_password = config.get_strvalue ('db_test', 'db_password')
        db_name = config.get_strvalue ('db_test', 'db_name')
        db_port = config.get_intvalue ('db_test', 'db_port')
        # 打开数据库连接
        self.db = pymysql.connect(host=host,
                             user= db_username,
                             password=db_password,
                             database= db_name,port=db_port,charset = 'utf8')
        # 使用 cursor() 方法创建一个游标对象 cursor 设置返回字典
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor) # 创建字典类型的游标

    def fetch_one(self,sql):
        # 使用 execute()
        #
        # 方法执行 SQL 查询
        self.cursor.execute (sql)
        self.db.commit()
        return self.cursor.fetchone ()

    def fetch_all(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()  #关闭游标
        self.db.close()      #关闭链接


if __name__ == '__main__':
    my_sql = DoMysql()
    sql='select max(mobilephone) from future.member'
    data = my_sql.fetch_one(sql)
    print(type(data),data)

    sql1 = 'select * from future.member limit 10'
    data1 = my_sql.fetch_all(sql1)
    print(type(data1),data1)
    my_sql.close()

    # {"mobilephone": "17786426991", "pwd": "123456"}