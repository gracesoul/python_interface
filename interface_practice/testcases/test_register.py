# -*- coding: utf-8 -*-
# @time:2019/4/17 14:44
# Author:yh
# @file:test_register.py

import unittest
from ddt import ddt,data
from interface_practice.common.do_request import HttpRequest
from interface_practice.common.do_excel import DoExcel
from interface_practice.common.contants import case_file
from interface_practice.common.my_log import MyLog
from interface_practice.common.do_mysql import DoMysql
import random

my_log = MyLog (__name__)

do_excel = DoExcel(case_file,'register')
register_cases = do_excel.get_data()
@ddt
class RegisterTest(unittest.TestCase):
    '''
    setup(self)每个测试用例之前都加载一次,
    setUpClass(cls) 类方法 所有用例 执行一次
    '''
    @classmethod
    def setUpClass(cls):
        my_log.info('-----测试用例开始执行-----')
        cls.do_request = HttpRequest()
        cls.db = DoMysql()

    @data(*register_cases)  # data里面放数据类型: -->可迭代,列表,字典,元组
    def test_register(self,case):
        my_log.info ('开始执行第{}条测试用例：{}'.format (case.case_id, case.title))

        # 在请求之前 先判断是否需要执行SQL
        if case.check_sql:
            sql = eval (case.check_sql)['sql1']  # 转化为字典格式 方便后期操作多个SQL语句
            sql_result = self.db.fetch_one (sql)
            register_before = sql_result['count(id)']  # 拿到数据后，要保存数据
            print(type(register_before))  # <class 'int'>
            print ('注册之前数据库的总数有：',register_before)

        if case.data.find('register_mobile')>-1:
            sql = 'select max(mobilephone) from future.member'
            max_phone = self.db.fetch_one(sql)  # 查询最大的手机号码
            print (type (max_phone))  # <class 'dict'>
            print ('取到的值：', max_phone)  # {'max(mobilephone)': '18999999999'}
            max_phone=max_phone['max(mobilephone)']
            print(type(max_phone)) # <class 'str'>
            print('最大：',max_phone)  #18999999999
            max_phone = int(max_phone)- random.randint(100,10000) # 最大手机号+1（保证手机号在数据库中不存在）
            print('最大的手机号码：',max_phone)
            # replace()函数 是替换之后重新返回一个新的字符串，有返回值 需要变量去接收
            case.data = case.data.replace('register_mobile',str(max_phone)) # 替换参数值

        resp = self.do_request.http_request(case.method,case.url,case.data)
        try:
            self.assertEqual(case.expected,resp.text)
            write_result='PAss'
            # 在成功之后，先判断是否需要执行SQL
            if case.check_sql:
                sql = eval (case.check_sql)['sql1']  # 转化为字典格式 方便后期操作多个SQL语句
                sql_result = self.db.fetch_one (sql)
                register_after = sql_result['count(id)']  # 拿到数据后，要保存数据
                print ('注册之后数据库的总数有:',register_after)
                self.assertEqual(register_before +1 ,register_after)
        except AssertionError as e:
            write_result='Failed'
            print('断言出错:{}'.format(e))
            raise e
        finally:
            do_excel.write_back(case.case_id+1,7,resp.text)
            do_excel.write_back(case.case_id+1,8,write_result)

    @classmethod
    def tearDownClass(cls):
        my_log.info('测试用例执行完毕')
        cls.do_request.close()
        cls.db.close()

if __name__ == '__main__':
    unittest.main()