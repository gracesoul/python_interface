# -*- coding: utf-8 -*-
# @time:2019/4/26 14:58
# Author:殇殇
# @file:run_new.py
# @fuction: 生成测试报告

import unittest
from BeautifulReport import BeautifulReport
from interface_practice.common.contants import *

suite = unittest.TestSuite()
# from interface_practice.testcases.test_login import LoginTest
# from interface_practice.testcases.test_register import RegisterTest
# from interface_practice.testcases.test_recharge import RechargeTest
# from interface_practice.testcases.test_withdraw import WithdrawTest
# from interface_practice.testcases.test_bidloan import BidloanTest
# from interface_practice.testcases.test_addloan import AddloanTest
# from interface_practice.testcases.test_audit import AuditTest

# loader = unittest.TestLoader()
# suite.addTest(loader.loadTestsFromTestCase(LoginTest))
# suite.addTest(loader.loadTestsFromTestCase(RegisterTest))



dicover = unittest.defaultTestLoader.discover(case_dir,pattern='test_*.py')

BeautifulReport(dicover).report(filename='前程贷测试报告',description='这是前程贷项目的部分接口的测试报告',
                              log_path=report_dir)




