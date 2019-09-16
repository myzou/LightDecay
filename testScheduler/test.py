#!/usr/bin/python
# -*- coding: UTF-8 -*-


from apscheduler.schedulers.blocking import BlockingScheduler
import time





# 打印当前时间
def getNowTime():
    nowTime= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(nowTime)


if __name__ == '__main__':
    # 实例化一个调度器
    scheduler = BlockingScheduler()
    # 添加任务并设置触发方式为3s一次
    scheduler.add_job(getNowTime, 'interval', seconds=3)

    # 开始运行调度器
    scheduler.start()