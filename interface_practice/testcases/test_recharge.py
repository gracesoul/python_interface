# -*- coding: utf-8 -*-
# @time:2019/4/17 14:44
# Author:yh
# @file:test_recharge.py

import unittest
from ddt import ddt,data
from interface_practice.common.do_excel import DoExcel
from interface_practice.common.do_request import HttpRequest
from interface_practice.common.contants import case_file
from interface_practice.common.my_log import MyLog
from interface_practice.common.do_mysql import DoMysql
from interface_practice.common.re_context import replace

my_log = MyLog (__name__)

do_excel = DoExcel(case_file,'recharge')
recharge_cases = do_excel.get_data()

@ddt
class RechargeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_log.info('-----开始执行测试用例-----')
        cls.do_request = HttpRequest()
        cls.mysql = DoMysql()

    @data(*recharge_cases)
    def test_recharge(self,case):
        my_log.info('开始执行第{}条测试用例：{}'.format(case.case_id,case.title))
        case.data = replace(case.data)
        print(type(case.data))
        # 在请求之前 先判断是否需要执行SQL
        if case.check_sql:
            case.check_sql = replace(case.check_sql)
            sql= eval(case.check_sql)['sql1'] # 转化为字典格式 方便后期操作多个SQL语句
            sql_result = self.mysql.fetch_one(sql)
            recharge_before = sql_result['leaveamount'] # 拿到数据后，要保存数据
            print('充值前的金额为：',recharge_before)
        resp = self.do_request.http_request(case.method,case.url,case.data)
        try:
            self.assertEqual(case.expected,resp.json()['msg'])
            write_result = 'Pass'
            # 在成功之后 先判断是否需要执行SQL
            if case.check_sql:
                case.check_sql = replace(case.check_sql)
                sql = eval (case.check_sql)['sql1']  # 转化为字典格式 方便后期操作多个SQL语句
                sql_result = self.mysql.fetch_one (sql)
                recharge_after = sql_result['leaveamount']  # 拿到数据后，要保存数据
                print ('充值后的金额为：',recharge_after)
                recharge_amount = int(eval(case.data)['amount'])
                self.assertEqual(recharge_before+recharge_amount,recharge_after)
        except AssertionError as e:
            write_result = 'Fail'
            print('断言出错:{}'.format(e))
            raise e
        finally:
            do_excel.write_back(case.case_id+1,7,resp.text)
            do_excel.write_back(case.case_id+1,8,write_result)

    @classmethod
    def tearDownClass(cls):  # 用例全部执行完 才关闭session(保证所有的用例都同用一个session)
        my_log.info('-----测试用例执行完毕-----')
        cls.do_request.close()

if __name__ == '__main__':
    unittest.main()