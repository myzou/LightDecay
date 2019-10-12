#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import json
import threading

import numpy as np
import ssh_gateway_batch
import error_db
import rsa
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

login_status={}
decode_rsa_param=['crypto_sign']
login_param=['username','password','sign','timestamp']
execute_param=['username','password','sign','timestamp','ip','command']


with open('mykeys/my_private_key.pem','r') as f:
     privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())


#定期清除过期session
def del_timeout_channel():
    try:
        for i in login_status:
            print(i)
            for j in login_status[i]:
                print(j)
                if login_status[i][j]['time'] + 70 < int(time.time()):
                    try:
                        del login_status[i][j]
                    except:
                        pass
    except:
        pass
    time.sleep(60)

#将urlget参数转换为json格式
def url_to_json(data):
    data_group=data.split('&&')
    tmp_dict={}
    for i in data_group:
        try:
            tmp_dict[i.split('=')[0]]=i.split('=')[1].replace('[object%20HTMLInputElement]','')
        except:
            tmp_dict[i.split('=')[0]]=''
    return json.dumps(tmp_dict)


def decode_rsa(param):
    crypto_sign=param['crypto_sign']
    if len(crypto_sign)%4 != 0:
        for i in range(0,4-len(crypto_sign)%4):
            crypto_sign=crypto_sign+'='
    try:
        return rsa.decrypt(base64.b64decode(crypto_sign),privkey).decode()
    except:
        return json.dumps(error_db.error_code('10301'))



def check_param(param_group,next_jump,datas):
    if '?' not in datas:
        return json.dumps(error_db.error_code('9999'))
    if 'Decryption failed' in datas:
        return json.dumps(error_db.error_code('10301'))
    param=json.loads(url_to_json(datas.split('?')[1]))
    for i in param_group:
        if param.get(i,None) is None:
            return json.dumps(error_db.error_code('10201'))
        if len(param.get(i)) == 0:
            return json.dumps(error_db.error_code('10202'))
    return next_jump(param)
    

def login(param):
    if int(time.time()) -150 > int(param['timestamp']) or int(param['timestamp']) > int(time.time()) +150:
        return json.dumps(error_db.error_code('10102'))
    if login_status.get(param['username'],None) is None:
        login_status[param['username']]={}
    if len(login_status[param['username']]) < 6 and login_status[param['username']].get(param['sign'],None) is None:
        try:
            login_to_ggw(param)
        except:
            del login_status[param['username']][param['sign']]
            return json.dumps(error_db.error_code('10001'))
        return json.dumps({'code':0,'data':'success'})
    elif login_status[param['username']][param['sign']]['time'] is not None:
        if login_status[param['username']][param['sign']]['time'] + 600 < int(time.time()):
            try:
                login_to_ggw(param)
            except:
                del login_status[param['username']][param['sign']]
                return json.dumps(error_db.error_code('10001'))
        else:
            return json.dumps(error_db.error_code('10003'))
    else:
        return json.dumps(error_db.error_code('10002'))

def login_to_ggw(param):
    print(str(int(time.time())) + ' ' + param['username'] + 'login ggw' )
    login_status[param['username']][param['sign']]={}
    login_status[param['username']][param['sign']]['login_tunnle']=ssh_gateway_batch.login_class()
    login_status[param['username']][param['sign']]['time']=int(time.time())
    login_status[param['username']][param['sign']]['targethost']={}
    login_status[param['username']][param['sign']]['login_tunnle'].login_ggw(param['username'],param['password'])
    
def login_to_device(param):
    print( str(int(time.time())) + ' ' + 'login device' + param['ip'])
    login_status[param['username']][param['sign']]['targethost'][param['ip']]={}
    login_status[param['username']][param['sign']]['targethost'][param['ip']]['login_tunnle']=login_status[param['username']][param['sign']]['login_tunnle'].login_fggw_tdevice(param['username'],param['password'],param['ip'])
    login_status[param['username']][param['sign']]['targethost'][param['ip']]['time']=int(time.time())

def execute(param):
    if int(time.time()) -150 > int(param['timestamp']) or int(param['timestamp']) > int(time.time()) +150:
        return json.dumps(error_db.error_code('10102'))
    return_data={}
    return_data['code']=0
    if login_status.get(param['username'],None) is None:
        return json.dumps(error_db.error_code('10103'))
    if login_status[param['username']].get(param['sign'],None) is None:
        return json.dumps(error_db.error_code('10101'))
    if login_status[param['username']][param['sign']]['time'] + 600 < int(time.time()):
        del login_status[param['username']][param['sign']]
        return json.dumps(error_db.error_code('10103'))
    if login_status[param['username']][param['sign']]['targethost'].get(param['ip'],None) is None :
        login_to_device(param)
    if login_status[param['username']][param['sign']]['targethost'][param['ip']]['time'] + 600 < int(time.time()):
        login_to_device(param)
    try:
        return_data['data']=login_status[param['username']][param['sign']]['login_tunnle'].send_cmd_to_device_quick(
            login_status[param['username']][param['sign']]['targethost'][param['ip']]['login_tunnle'],
            param['command'].replace('%20',' ').replace('%7C','|'))
    except:
        return json.dumps(error_db.error_code('10004'))
    print(str(int(time.time())) + ' command ' + param['command'] + ' ' + param['ip'])
    login_status[param['username']][param['sign']]['time']=int(time.time())
    login_status[param['username']][param['sign']]['targethost'][param['ip']]['time']=int(time.time())
    return json.dumps(return_data,cls=MyEncoder)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)



class proxyHandler(BaseHTTPRequestHandler):
    def show_html(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(self.login_html)))
        self.end_headers()
        self.wfile.write(self.login_html.encode(encoding='utf-8'))


    def do_GET(self):
        datas = self.path
        type = self.path.split('/')[1]
        if '/RSA' in datas:
            datas = datas + '&&'+check_param(decode_rsa_param,decode_rsa,datas)
        if '/test_lab' in type:
            if 'GetLoginSession' in type:
                print(1)
        else:
            if 'GetLoginSession' in type:
                self.login_html = check_param(login_param,login,datas)
            elif 'ExecuteCommand' in type:
                self.login_html = check_param(execute_param,execute,datas)
            else:
                self.login_html = json.dumps(error_db.error_code('10202'))
        self.show_html()

def test():
    host='0.0.0.0'
    port=48888
    try:
        server = socketserver.ThreadingTCPServer((host, port), proxyHandler)
        print('Welcome to the Server HTTP On %s  Port %d...' %(host,port))
        server.serve_forever()
    except KeyboardInterrupt as e:
        #logging.error(e)
        #print '^C received, shutting down server'
        server.socket.close()
 
if __name__ == '__main__':
    threading.Thread(target=del_timeout_channel,).start()
    test()