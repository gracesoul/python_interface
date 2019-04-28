# -*- coding: utf-8 -*-
# @time:2019/4/19 10:28
# Author:殇殇
# @file:test_audit.py
# @fuction: 测试审核功能

import unittest
from ddt import ddt,data
from interface_practice.common.do_excel import DoExcel
from interface_practice.common.do_request import HttpRequest
from interface_practice.common.contants import *
from interface_practice.common.my_log import MyLog
from interface_practice.common.re_context import replace

my_log = MyLog(__name__)  # 对象实例化

do_excel = DoExcel(case_file,'audit')
audit_cases = do_excel.get_data()


@ddt
class AuditTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_log.info('-----测试用例开始执行-----')
        cls.do_request = HttpRequest()

    @data(*audit_cases)
    def test_audit(self,case):
        # 替换参数化的值
        case.data = replace(case.data)
        my_log.info('开始执行第{}条用例：{}'.format(case.case_id,case.title))
        resp = self.do_request.http_request(case.method,case.url,case.data)
        try:
            self.assertEqual(case.expected,resp.json()['msg'])
            write_result = 'Pass'
        except AssertionError as e:
            write_result = 'Failed'
            print('断言出错：{}'.format(e))
            raise e
        finally:
            do_excel.write_back(case.case_id+1,7,resp.text)
            do_excel.write_back(case.case_id+1,8,write_result)

    @classmethod
    def tearDownClass(cls):
        my_log.info('-----用例执行完毕-----')
        cls.do_request.close()


if __name__ == '__main__':
    unittest.main()

