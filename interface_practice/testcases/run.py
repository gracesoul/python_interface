# -*- coding: utf-8 -*-
# @time:2019/4/18 13:32
# Author:yh
# @file:run.py
import sys
sys.path.append('./')
# print(sys.path)

import unittest
from HTMLTestRunnerNew import HTMLTestRunner
from interface_practice.common.contants import *

discover = unittest.defaultTestLoader.discover(case_dir,pattern='test_*.py')

with open(report_dir+'/report.html','wb+') as file:
    runner = HTMLTestRunner(stream=file,verbosity=2,
                            title='前程贷测试报告',
                            description='这是一个前程贷项目有关注册,登录,充值,取现的接口测试',
                            tester='殇殇')
    runner.run(discover)

