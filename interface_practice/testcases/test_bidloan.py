# -*- coding: utf-8 -*-
# @time:2019/4/19 10:44
# Author:殇殇
# @file:test_bidloan.py
# @fuction: 测试投资，竞标
import unittest
from ddt import ddt,data
from interface_practice.common.do_excel import DoExcel
from interface_practice.common.do_request import HttpRequest
from interface_practice.common.contants import *
from interface_practice.common.my_log import MyLog
from interface_practice.common.re_context import replace,Context
from interface_practice.common.do_mysql import DoMysql

my_log = MyLog(__name__) # 对象实例化
do_excel = DoExcel(case_file,'bidloan')
bidloan_cases = do_excel.get_data()


@ddt
class BidloanTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_log.info('-----开始执行测试用例-----')
        cls.do_request = HttpRequest()
        cls.mysql = DoMysql ()

    @data(*bidloan_cases)
    def test_bidloan(self,case):
        case.data = replace(case.data)
        my_log.info('开始执行第{}条测试用例：{}'.format(case.case_id,case.title))
        # 在发起请求前，先判断是否需要执行SQL
        if case.check_sql:
            case.check_sql = replace(case.check_sql)
            sql = eval(case.check_sql)['sql1']
            sql_result = self.mysql.fetch_one(sql)
            invest_before = sql_result['leaveamount']
            print('投资人投资前：余额为：{}'.format(invest_before))
        resp = self.do_request.http_request(case.method,case.url,case.data)
        try:
            self.assertEqual(str(case.expected),resp.json()['code'])
            write_result = 'Pass'
            # 判断加标成功后，查询数据库，取到load_add_id的值
            if resp.json()['msg'] == '加标成功':
                sql='select id from future.loan where memberid = 1021 order by id desc limit 1;'
                load_add_id = self.mysql.fetch_one(sql)['id']  # 返回字典（原因是：DoMysql里面的游标的设置）
                print('标的id:{}'.format(load_add_id))
                # 保存到类属性里面
                setattr(Context,'load_add_id',str(load_add_id))
                # 在发起请求前，先判断是否需要执行SQL
            if case.check_sql:
                case.check_sql = replace (case.check_sql)
                sql = eval (case.check_sql)['sql1']
                sql_result = self.mysql.fetch_one (sql)
                invest_after = sql_result['leaveamount']
                print ('投资人投资后：余额为：{}'.format (invest_after))
                invest_amount = eval(case.data)['amount']
                print('投资人投款金额为：{}'.format(invest_amount))
                self.assertEqual(invest_before,invest_after+int(invest_amount))
        except AssertionError as e:
            write_result = 'Failed'
            my_log.error(

                '断言出错：{}'.format(e))
            raise e
        finally:
            do_excel.write_back(case.case_id+1,7,resp.text)
            do_excel.write_back(case.case_id+1,8,write_result)

    @classmethod
    def tearDownClass(cls):
        my_log.info('-----测试用例执行完毕-----')
        cls.do_request.close()


if __name__ == '__main__':
    unittest.main()
