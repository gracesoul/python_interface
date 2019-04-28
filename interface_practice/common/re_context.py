# -*- coding: utf-8 -*-
# @time:2019/4/21 22:22
# Author:殇殇
# @file:re_context.py
# @fuction: 封装一个匹配的方法
import re
import configparser
from interface_practice.common.config import ReadConfig
from interface_practice.common.my_log import MyLog

my_log = MyLog (__name__)

config = ReadConfig()

class Context:
    load_add_id = None



def replace(data):
    p = '#(.*?)#'  #正则表达式
    while re.search(p,data):
        find_original_data = re.search(p,data) #从任意位置开始找，找第一个就返回Match object,如果没找到，就返回None
        find_key = find_original_data.group(1) #拿到参数化的KEY
        #.group(1)  只返回指定组的内容，-》normal_user
        #.group(0) 返回表达式和组里面的内容 #normal_user#
        try:
            find_value = config.get_strvalue('data',find_key) #根据KEY取配置文件里面的值
        except configparser.NoOptionError as e:
            # 如果配置文件里面没有，就去Context这个类里面去找
            if hasattr(Context,find_key):
                find_value = getattr(Context,find_key)
            else:
                my_log.info('找不到参数化的值')
                raise e
        # print(find_value)
        #替换后的内容，依旧用data接收
        data = re.sub(p,find_value,data,count=1) #查找替换，count 替换的次数
    # print('替换后的data：',data)
    return data


