# -*- coding: utf-8 -*-
# @time:2019/4/25 15:24
# Author:殇殇
# @file:study_reflect.py
# @fuction: 学习反射机制

class People:
    eyes = 2
    def __init__(self,name,age):
        self.name=name
        self.age =age

if __name__ == '__main__':
    p = People('yh','18')
    print(p.eyes)
    print(p.name)
    print(p.age)
    print (People.eyes) # 类属性 对象与类都可以调用  类不可以调用实例属性
    # 添加属性
    print(hasattr(People,'legs')) # 没有返回false
    print (hasattr (People, 'eyes')) # 有返回 true
    setattr(People,'legs',2)
    print(hasattr(People,'legs'))
    print(getattr(People,'legs')) # 获取属性值
    print(People.legs) # 类名调用类属性
    print(p.legs)     # 对象调用类属性

    setattr(People,'dance',True)
    print(People.dance)
    # 添加属性 setattr
    # 获取属性 getattr
    # 删除属性 delattr
    # 判断是否有该属性： hasattr
    # setattr ()，不需要判断是否有该属性
    # getattr ()，需要判断是否有该属性
    delattr(People,'dance')
    # getattr(People,'dance')
    setattr(p,'name','huahau')
    print(getattr(p,'name')) # 存在该属性
    # print(getattr(p,'dance')) # 没有该属性





