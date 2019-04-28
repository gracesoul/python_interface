# -*- coding: utf-8 -*-
# @time:2019/4/18 9:30
# Author:yh
# @file:test_withdraw.py

import unittest
from ddt import ddt,data
from interface_practice.common.do_excel import DoExcel
from interface_practice.common.do_request import HttpRequest
from interface_practice.common.contants import *
from interface_practice.common.my_log import MyLog
from interface_practice.common.do_mysql import DoMysql
from interface_practice.common.re_context import replace

my_log = MyLog (__name__)

do_excel = DoExcel(case_file,'withdraw')
withdraw_cases = do_excel.get_data()

@ddt
class WithdrawTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_log.info('---测试用例开始执行---')
        cls.do_request = HttpRequest()
        cls.mysql = DoMysql()

    @data(*withdraw_cases)
    def test_withdraw(self,case):
        my_log.info('开始执行第{}条测试用例:{}'.format(case.case_id,case.title))
        case.data = replace(case.data)
        if case.check_sql:
            case.check_sql = replace(case.check_sql)
            sql = eval(case.check_sql)['sql1']
            sql_result = self.mysql.fetch_one(sql)
            withdraw_before = sql_result['leaveamount']
            print('取现之前的金额为：',withdraw_before)
        resp = self.do_request.http_request(case.method,case.url,case.data)
        try:
            self.assertEqual(case.expected,resp.json()['msg'])
            write_result = 'Pass'
            if case.check_sql:
                case.check_sql = replace (case.check_sql)
                sql = eval (case.check_sql)['sql1']
                sql_result = self.mysql.fetch_one (sql)
                withdraw_after = sql_result['leaveamount']
                print ('取现之前的金额为：', withdraw_after)
                withdraw_amount = eval(case.data)['amount']
                self.assertEqual(withdraw_before,withdraw_after+int(withdraw_amount))
        except AssertionError as e:
            write_result='Failed'
            print('断言出错:{}'.format(e))
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