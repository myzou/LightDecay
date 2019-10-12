#encoding=utf-8
"""this is not thread-safe"""

import paramiko

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
        except paramiko.AuthenticationException:
            print ("%s Authentication failed" % (device_ip))
        except:
            print('fail')
        
    def send_cmd_to_device(self,cmd):
        print(cmd)
        stdin, stdout, stderr = self.targethost.exec_command(cmd) 
        if len(stderr.readlines()) >= 0:
            a=str(stdout.read(),encoding='utf-8')[2:-1].replace('\\n', '\n')
            return a
            
            
    def login_fggw_tdevice(self,username,password,device_ip):
        dest_addr = (device_ip, 22)
        try:
            jumperchannel = self.jumpertransport.open_channel("direct-tcpip", dest_addr, self.local_addr)
            self.targethost=paramiko.SSHClient()
            self.targethost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.targethost.connect(device_ip, username=username, password=password, sock=jumperchannel)
            return self.targethost
        except paramiko.AuthenticationException:
            print("%s Authentication failed" % (device_ip))
        except:
            print('fail')
            
            
            
    @staticmethod
    def login_device_long(username,password,device_ip):
        try:
            targethost=paramiko.SSHClient()
            targethost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            targethost.connect(device_ip, username=username, password=password)
            return targethost
        except paramiko.AuthenticationException:
            print ("%s Authentication failed" % (device_ip))
            
    @staticmethod
    def send_cmd_to_device_quick(targethost,cmd):
        stdin, stdout, stderr = targethost.exec_command(cmd) 
        aa=stderr.read()
        if len(aa) > 0:
            a=aa+stdout.read()
        else:
            a=stdout.read()
        return a
            


def test():
    test_def=login_class()
    test_def.login_device('cpcnet','cpc123','202.76.80.208',"show interfaces terse")



if __name__ == '__main__':
    test()