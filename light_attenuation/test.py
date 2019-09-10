#!/usr/bin/python
# -*- coding: UTF-8 -*-

from time import strftime, localtime

# 打印当前时间
def getNowTime():
    nowTime=strftime("%Y-%m-%d %H:%M:%S", localtime())
    return nowTime

if __name__ == '__main__':
    print(getNowTime())