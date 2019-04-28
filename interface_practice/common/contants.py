# -*- coding: utf-8 -*-
# @time:2019/4/17 13:59
# Author:yh
# @file:contants.py

import os
'''
os.path.abspath(__file__)  结果:F:\work\python_15\interface_practice\common\contants.py
os.path.dirname(os.path.abspath(__file__)) 结果: F:\work\python_15\interface_practice\common
os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 结果:F:\work\python_15\interface_practice

'''





base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
case_file = os.path.join(base_dir,'data','cases.xlsx')  #data-->cases.xlsx文件
# print(case_file)

global_config_file = os.path.join(base_dir,'config','global.cfg')
# print(global_config_file)

online_config_file =os.path.join(base_dir,'config','online.cfg')
# print(online_config_file)

test_config_file =os.path.join(base_dir,'config','test.cfg')
# print(test_config_file)

mysql_file = os.path.join(base_dir,'config','db_mysql.cfg')

mylog_file = os.path.join(base_dir,'log')

case_dir = os.path.join(base_dir,'testcases')
report_dir = os.path.join(base_dir,'report')
print(report_dir)



# memberId = 1083 (用户id) --->17786426991
# loanId = 532  (标id)   (自己添加的)

# memberId = 279  --->  18871362015


# memberId = 1021 (用户id) --->17786426991
# loanId = 2621  (标id)   (自己添加的)

# memberId = 1023  --->  18871362015
# 管理员id(自己设置的)
# memberid = 1676 ---->  18871362019
