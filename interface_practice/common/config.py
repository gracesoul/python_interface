# -*- coding: utf-8 -*-
# @time:2019/4/17 17:12
# Author:yh
# @file:config.py

from configparser import ConfigParser
from interface_practice.common.contants import *

class ReadConfig:
    '''
    完成配置文件的读取
    '''
    def __init__(self,encoding='utf-8'):
        # 1.打开配置文件
        self.cf = ConfigParser()
        # 2.加载配置文件
        self.cf.read(global_config_file,encoding)  #先加载global.cfg文件
        switch = self.cf.getboolean('switch','on')
        if switch:  #on=True 开关打开的时候,加载的是线上环境的配置
            self.cf.read(online_config_file,encoding)
        else:       #on = false 开关关闭的时候,加载的是测试环境的配置
            self.cf.read(test_config_file,encoding)


    # def get_value(self,section,option):
    #     return self.cf.get(section,option)

    # 获取配置的数据
    def get_intvalue(self, section, option):  # 获取整数
        return self.cf.getint (section, option)

    def get_boolvalue(self, section, option):  # 获取布尔值
        return self.cf.getboolean (section, option)

    def get_strvalue(self, section, option):  # 获取字符串
        return self.cf.get (section, option)

    def get_floatvalue(self, section, option):  # 获取浮点数
        return self.cf.getfloat (section, option)

    def get_sections(self):  # 获取区域
        return self.cf.sections ()

    def get_options(self, section):  # 获取section下的option
        return self.cf.options (section)


if __name__ == '__main__':
    config = ReadConfig()
    value = config.get_value('api','pre_url')
    print(value)








