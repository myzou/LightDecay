#encoding=utf-8
"""this is not thread-safe"""
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
            print(e)
            return 'login fail'
        
    def send_cmd_to_device(self,cmd):
        stdin, stdout, stderr = self.targethost.exec_command(cmd) 
        if len(stderr.readlines()) >= 0:
            a=stdout.read()
            return a
            
def test():
    user = "op1768"
    pwd = "Abc1015"
    test_def=login_class()
    test_def.login_ggw(user,pwd)
    print(test_def.login_device(user,pwd,'218.96.243.2','show version'))

if __name__ == '__main__':
    test()