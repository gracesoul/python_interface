# -*- coding: utf-8 -*-
# @time:2019/4/17 14:44
# Author:yh
# @file:test_login.py

import unittest
from ddt import ddt,data
from interface_practice.common.do_request import HttpRequest
from interface_practice.common.do_excel import DoExcel
from interface_practice.common.contants import case_file
from interface_practice.common.my_log import MyLog
from interface_practice.common.re_context import replace

my_log = MyLog (__name__)#实例化

do_excel = DoExcel(case_file,'login')
login_cases = do_excel.get_data()

@ddt
class LoginTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_log.info('-----开始执行测试用例-----')
        cls.do_request = HttpRequest()

    @data(*login_cases)
    def test_login(self,case):
        my_log.info('开始执行第{}条测试用例:{}'.format(case.case_id,case.title))
        case.data = replace(case.data)
        resp = self.do_request.http_request(case.method,case.url,case.data)
        try:
            self.assertEqual(case.expected,resp.text)
            write_result = 'Pass'
        except AssertionError as e:
            write_result = 'Failed'
            my_log.error('断言出错:{}'.format(e))
            raise e
        finally:
            do_excel.write_back(case.case_id+1,7,resp.text)
            do_excel.write_back(case.case_id+1,8,write_result)
        my_log.info('结束测试用例:{}'.format(case.title))

    @classmethod
    def tearDownClass(cls):
        my_log.info('-----测试用例执行完毕-----')
        cls.do_request.close()


if __name__ == '__main__':
    unittest.main()