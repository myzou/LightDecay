import base64
import rsa
import time
from urllib.request import urlopen
import json

PUB_FILE = 'public.pem'


class Parameter:
    def __init__(self, username=None, password=None):
        self.__username = username
        self.__password = password
        self.__local_ip = None
        self.__target_ip = None
        self.__input_Filters = None
        self.__port = None
        self.__crypto_sign = None
        self.__ip = None

    def set_local_ip(self, local_ip):
        self.__local_ip = local_ip

    def set_target_ip(self, target_ip):
        self.__target_ip = target_ip

    def set_port(self, port):
        self.__port = port

    def set_ip(self, ip):
        self.__ip = ip

    def set_crypto_sign(self):
        message = 'username=%s&&password=%s&&sign=%s&&timestamp=%s' % (
        self.__username, self.__password, '123456', str(int(time.time())))
        with open(PUB_FILE, 'r') as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
        crypto_sign = str(base64.b64encode(rsa.encrypt(message.encode(), pubkey)), 'utf-8')
        self.__crypto_sign = crypto_sign

    def encode_rsa(self):
        # 登录GGW
        login = 'http://10.180.5.135:48888/GetLoginSession/RSA?crypto_sign=' + self.__crypto_sign
        return login

    def show_interfaces(self):
        # 登录PE并执行命令
        show_interfaces = 'http://10.180.5.135:48888/ExecuteCommand/RSA?crypto_sign=' + self.__crypto_sign + \
                          '&&command=show%20interfaces%20{0}%20extensive&&ip={1}'.format(self.__port, self.__ip)
        return show_interfaces

    def show_ping(self):
        show_ping = 'http://10.180.5.135:48888/ExecuteCommand/RSA?crypto_sign=' + self.__crypto_sign + \
                    '&&command=%20ping%20interface%20{0}%20rapid%20{1}%20source%20{2}%20count%20100&&ip={3}'.format(
                        self.__port, self.__target_ip, self.__local_ip, self.__ip)
        return show_ping

    def show_queue(self):
        show_queue = 'http://10.180.5.135:48888/ExecuteCommand/RSA?crypto_sign=' + self.__crypto_sign + \
                     '&&command=show%20interfaces%20queue%20{0}%20egress%20|match%20drop&&ip={1}'.format(self.__port,
                                                                                                         self.__ip)
        return show_queue

    def show_firewall(self, input_filter):
        show_firewall = 'http://10.180.5.135:48888/ExecuteCommand/RSA?crypto_sign=' + self.__crypto_sign + \
                        '&&command=show%20firewall%20filter%20{0}&&ip={1}'.format(input_filter, self.__ip)
        return show_firewall

    def call_package(self, url):
        return str(urlopen(url).read(), 'utf-8').replace('\\n','\n')

    def get_input_filter(self, str_interfaces=''):
        if 'Input Filters:' in str_interfaces:
            return str_interfaces.split('Input Filters:',1)[1].split('\n')[0].strip()
        else:
            return ''
    def deal_json(self, json_data):
        return str(json.loads(json_data, strict=False)['data'])

if __name__ == '__main__':
    user = Parameter(username='op1768', password='Abc1015')
    user.set_ip('218.96.240.96')
    user.set_port('ge-0/1/0.206')
    user.set_local_ip('192.168.102.5')
    user.set_target_ip('192.168.102.6')
    user.set_crypto_sign()
    a = user.call_package(user.encode_rsa())
    b = user.call_package(user.show_interfaces())
    c = user.call_package(user.show_ping())
    d = user.call_package(user.show_interfaces())
    e = user.call_package(user.show_firewall(user.get_input_filter(b)))
    print(user.deal_json(a),'------------------------\n',user.deal_json(b),'----------------------------\n',
          user.deal_json(c),'------------------------\n',user.deal_json(d),'----------------------------\n',
          user.deal_json(e))