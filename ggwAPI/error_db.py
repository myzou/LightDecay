# encoding: UTF-8
# -*- coding: utf-8 -*-

def error_code(code):
    error_list={
    10001:{'code':10001,'data':'Username or password invalid'},
    10002:{'code':10002,'data':'Login limit reached'},
    10003:{'code':10003,'data':'Do not repeat login'},
    10004:{'code':10004,'data':'Permission denied or ip is not exist'},
    10103:{'code':10103,'data':'GGW channel has timed out'},
    10101:{'code':10101,'data':'Channel does not exist or has timed out'},
    10102:{'code':10102,'data':'Crypto sign has timed out'},
    10201:{'code':10201,'data':'Parameter missing'},
    10202:{'code':10202,'data':'Parameter is invalid'},
    10301:{'code':10301,'data':'Decryption failed'},
    9999:{'code':9999,'data':'Bad request'}
    }
    return error_list[int(code)]