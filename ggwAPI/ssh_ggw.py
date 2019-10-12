#encoding=utf-8
"""this is not thread-safe"""
import datetime
import traceback
from time import strftime, localtime
from datetime import datetime
import paramiko

def aa():
    aa=""

class login_class():
    def login_ggw(self,username,password):
        jumperip = '203.85.80.30'
        jumperuser = username
        jumperpass = password
        jumper=paramiko.SSHClient()
        jumper.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        jumper.connect(jumperip,username=jumperuser,password=jumperpass)
        self.jumpertransport = jumper.get_transport()
        self.local_addr = (jumperip, 22)
        
    def login_device(self,username,password,device_ip,cmd):
        dest_addr = (device_ip, 22)
        try:
            jumperchannel = self.jumpertransport.open_channel("direct-tcpip", dest_addr, self.local_addr)
            self.targethost=paramiko.SSHClient()
            self.targethost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.targethost.connect(device_ip, username=username, password=password, sock=jumperchannel)
            return self.send_cmd_to_device(cmd)
        except Exception as e:
            print(traceback.format_exc())
            return 'login fail'
        
    def send_cmd_to_device(self,cmd):
        stdin, stdout, stderr = self.targethost.exec_command(cmd) 
        if len(stderr.readlines()) >= 0:
            a=str(stdout.read())[2:-1].replace('\\n', '\n')
            # a = str(stdout.read()).split('\"')[1]
            return a


# 打印当前时间
def getNowTime():
    nowTime=strftime("%Y-%m-%d %H:%M:%S", localtime())
    return nowTime

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
def get_restul(*args, **kwargs):
    test( *args, **kwargs)


def test(ip='218.96.240.95', command='ping interface ge-0/0/0.3  rapid source 218.96.231.213 218.96.231.214 count 100'):
    user = "op1768"
    pwd = "Abc1015"
    test_def=login_class()
    test_def.login_ggw(user,pwd)
    print(str(test_def.login_device(user,pwd,ip,command)))

if __name__ == '__main__':
    # test()
    ip = '202.76.8.226'
    command = ' show interfaces descriptions '
    get_restul(ip,command)