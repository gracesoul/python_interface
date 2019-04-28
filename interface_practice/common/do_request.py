# -*- coding: utf-8 -*-
# @time:2019/4/17 11:22
# Author:yh
# @file:do_request.py

import requests
from interface_practice.common.config import ReadConfig
from interface_practice.common.my_log import MyLog
my_log = MyLog(__name__)
config=ReadConfig()#实例化对象

class HttpRequest:
    def __init__(self):
        self.session = requests.session()  #放在初始化中,保证调用是同一个session

    def http_request(self,method,url,data=None,json=None):
        method = method.lower() #强制转化为小写

        if type (data) == str:
            data = eval (data) #将字符串转为字典形式
        url = config.get_strvalue('api','pre_url') + url  #读取配置文件的前部分
        my_log.debug('请求的url:{}'.format(url))
        my_log.debug('请求的data:{}'.format(data))

        if method == 'get':
            resp = self.session.request(method=method,url=url,params=data)
        elif method == 'post':
            if json:
                resp = self.session.request(method=method,url=url,json=json)
            else:
                resp = self.session.request(method=method,url=url,data=data)
        else:
            my_log.error('暂不支持除get/post以外的请求方式!')
        my_log.debug('请求的响应文本:{}'.format(resp.text))
        return resp

    def close(self):
        self.session.close() # 用完记得关闭


if __name__ == '__main__':
    # 登录接口
    login_url = 'http://test.lemonban.com/futureloan/mvc/api/member/login'
    params1 = {'mobilephone': '17786426991', 'pwd': '123456'}
    # 添加标的
    loan_add_url = 'http://test.lemonban.com/futureloan/mvc/api/loan/add'
    params2 = {'memberId': '1083', 'title': '借钱买房', 'amount': '90000', 'loanRate': '18.0',
               'loanTerm': 6, 'loanDateType': 0, 'repaymentWay': 10, 'biddingDays': 5}

    do_request = HttpRequest()
    resp = do_request.http_request('post',url=login_url,data=params1)
    # print('登录的响应文本:{}'.format(resp.text))

    resp = do_request.http_request('post',url=loan_add_url,data=params2)
    # print ('添加标的的响应文本:{}'.format (resp.text))
    # print(resp.status_code)