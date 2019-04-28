# -*- coding: utf-8 -*-
# @time:2019/4/18 16:57
# Author:殇殇
# @file:test_addloan.py
# @fuction: 添加标的

import unittest
from ddt import ddt,data
from interface_practice.common.do_excel import DoExcel
from interface_practice.common.do_request import HttpRequest
from interface_practice.common.contants import *
from interface_practice.common.my_log import MyLog
from interface_practice.common.config import ReadConfig
from interface_practice.common.re_context import replace
from interface_practice.common.do_mysql import DoMysql
config = ReadConfig()

my_log = MyLog(__name__)

do_excel = DoExcel(case_file,'add_loan')
addload_cases = do_excel.get_data()

@ddt
class AddloanTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_log.info('-----测试用例开始执行-----')
        cls.do_request = HttpRequest()
        cls.mysql = DoMysql()

    @data(*addload_cases)
    def test_addload(self,case):

        # 方法一
        # print(case.data)
        # case.data = eval(case.data)  #变成字典
        # if 'mobilephone' in case.data and case.data['mobilephone']=='normal_user':
        #     case.data['mobilephone']= config.get_value('data','normal_user')
        #     #拿到配置文件中的option的值 赋值给 Excel中的值
        # if 'pwd' in case.data and case.data['pwd'] == 'normal_pwd':
        #     case.data['pwd'] = config.get_value ('data','normal_pwd')
        #
        # if 'memberId' in case.data and case.data['memberId']=='loan_member_id':
        #     case.data['memberId']= config.get_value('data','loan_member_id')

        # 方法二  在请求之前替换参数化的值
        case.data = replace(case.data)
        my_log.info('开始执行第{}条测试用例：{}'.format(case.case_id,case.title))
        print('case.data的数据类型：',type(case.data)) # <class 'str'>
        print('case.data的数据：',case.data)
        # 在请求之前 先判断是否需要执行SQL
        if case.check_sql:
            case.check_sql = replace(case.check_sql)
            print(case.check_sql)
            sql = eval(case.check_sql)['sql1']
            sql_result = self.mysql.fetch_one(sql)
            addloan_before = sql_result['count(id)']
            print('添加标的之前，有：{}条数据'.format(addloan_before))
        resp = self.do_request.http_request(case.method,case.url,case.data)
        try:
            self.assertEqual(case.expected,resp.json()['msg'])
            write_result = "Pass"
            # 在成功之后 先判断是否需要执行SQL
            if case.check_sql:
                sql = eval (case.check_sql)['sql1']
                sql_result = self.mysql.fetch_one(sql)
                addloan_after = sql_result['count(id)']
                print ('添加标的之前，有：{}条数据'.format (addloan_after))
                self.assertEqual(addloan_before+1,addloan_after)
        except AssertionError as e:
            write_result='Failed'
            print('断言出错：{}'.format(e))
            raise e
        finally:
            do_excel.write_back(case.case_id+1,7,resp.text)
            do_excel.write_back(case.case_id+1,8,write_result)

    @classmethod
    def tearDownClass(cls):
        my_log.info('-----测试用例执行完毕-----')
        cls.do_request.close()
        cls.mysql.close()

if __name__ == '__main__':
    unittest.main()
