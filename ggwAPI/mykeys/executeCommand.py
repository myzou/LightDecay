#!/usr/bin/python
# -*- coding: UTF-8 -*-

import base64
import traceback

import rsa
import time
from time import strftime, localtime
from datetime import datetime
from urllib.request import urlopen
import json
import pymysql

from cryptography.hazmat.backends import openssl



# 打印当前时间
def getNowTime():
    nowTime=strftime("%Y-%m-%d %H:%M:%S", localtime())
    return nowTime

def encode_rsa(message, APIURL,ip,command):
    # publicKey="-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAh/hChlpkRA+zkkEB8ZoCrVcsYsbFSXYoTBKlrdCu0LiGeKs2T+U7\nkyZ/WZ8GP498PIucz6GYN03BWOOPe5nHWfwO05XqTid6+0ni+Bfy4Ev0FyCOQsod\nmQpH4ytgn0UOp8BZyJTwdN4rtMcuY/FFnyAsFpg9+F0DtlM/dVMj/UcWaMiZIBaa\n35XkXoPa+ng8Z7ORVOPiRHXfMGrlb9gZWF5XHN1SHNBKha1uF3wexDHVm4+k3Hvb\naZFkHrgLndaYuCPPtetnSNUOw2iaiNo7Nfze1Y4ACyfvRczHEGxFEC9X7tj/Rcy2\ngmC9JCErxDQAHitX8DJrKtoeSJN8GvZZJQIDAQAB\n-----END RSA PUBLIC KEY-----\n"
    # pubkey = rsa.PublicKey.load_pkcs1(publicKey)
    # #公钥从文件中读取
    with open('dickson_pkcs1_public.pem', 'r') as f: \
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())

    temp = str(base64.b64encode(rsa.encrypt(message.encode(), pubkey)),'utf-8')
    # 登录GGW
    login = APIURL+'/GetLoginSession/RSA?crypto_sign=' + temp
    command=command.replace(' ','%20').replace('|','%7C')
    #登录PE并执行命令
    exec = APIURL + '/ExecuteCommand/RSA?crypto_sign=' + temp + \
          '&&command='+command+'&&ip={0}'.format(ip)
    return login,exec



##组装密码验证字段
def get_message(username,password,sign):
    message='username=%s&&password=%s&&sign=%s&&timestamp=%s' % (username, password, sign, str(int(time.time())))
    return message

#访问
def get_result_page(url):
    res = urlopen(url).read()
    return str(res,'utf-8')


def ggwAPI(ip,command,APIURL='http://10.180.5.13:48888',username='op1768',password='Abc1015',sign='123456'):
    mg = get_message(username, password, sign)
    login, exec = encode_rsa(mg, APIURL, ip, command)
    print("login:", login)
    print("exec:", exec)
    try:
        login_str = get_result_page(login)
        print(getNowTime()+"  login_str:"+login_str)
        if str(json.loads(login_str)['code']) in ['10003', '0']:
            returnExec = get_result_page(exec)
            if str(json.loads(returnExec)['code']) in ['10003', '0']:
                returnExecStr = json.loads(returnExec)['data']
                print(getNowTime()+'  data:'+returnExecStr)
                return returnExecStr
        else:
            print('登录失败,请检查账号和密码是否正确')
            return '登录失败,请检查账号和密码是否正确'
    except Exception as e:
        print(str(traceback.format_exc()))
        return '登录查询信息失败'

def start_end_time(f):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        print('开始时间：'+getNowTime())
        f(*args, **kwargs)
        end_time=datetime.now()
        print('结束时间：'+getNowTime())
        print("用时"+str((end_time-start_time).seconds)+"秒")
    return wrapper

@start_end_time
def get_restul( *args, **kwargs):
    ggwAPI(*args, **kwargs)


if __name__ == '__main__':
    ip = '218.96.240.82'
    command = 'show interfaces descriptions | match trunk'
    # APIURL='http://210.5.3.30:8083'
    APIURL = 'http://10.180.5.13:48888'
    APIURL = 'http://210.5.3.177:48888'

    ggwAPI(ip,command,APIURL=APIURL)
    # print(get_restul(ip,command,APIURL=APIURL))


