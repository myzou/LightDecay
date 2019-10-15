import base64
import rsa
import time
from urllib.request import urlopen
import json

"""
Test some condition by using command.
"""
PUB_FILE = 'public.pem'


def str2fill(string):
    """
    fill the blank by using '%20',aim to submit the URL in browser.
    :param string: some command string include the blank.
    :return:no blank string.
    """
    return str(string).replace(' ', '%20')


class Professional_Work:
    # device ip
    __ip = ''

    def __init__(self, username=None, password=None, sign='123456'):
        """
        init the class
        :param username:login user op
        :param password: login user password
        :param sign: login sign,everyone can use 6 sign to login at the same time.
        """
        message = 'username=%s&&password=%s&&sign=%s&&timestamp=%s' % (username, password, sign, str(int(time.time())))
        with open(PUB_FILE, 'r') as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
        self.__crypto_sign = str(base64.b64encode(rsa.encrypt(message.encode(), pubkey)), 'utf-8')

    def submit_command(self, command):
        """
        using a URL to submit command.
        :param command: the command will use.
        :return: a URL.
        """
        return 'http://10.180.5.135:48888/ExecuteCommand/RSA?crypto_sign=' + self.__crypto_sign + '&&command=' + \
               command + '&&ip=' + self.__ip

    def encode_rsa(self):
        """
        logging in the GGW。
        :return: logging state by json.
        """
        login = 'http://10.180.5.135:48888/GetLoginSession/RSA?crypto_sign=' + self.__crypto_sign
        return self.call_package(login)

    # 命令测试
    def interfaces(self, interface):
        """
        show interfaces <<Interface>> extensive
        :param interface:interface.
        :return:command string.
        """
        return str2fill('show interfaces ' + interface + ' extensive')

    def firewall(self, input_filter):
        """
        show firewall filter <<input filter>>
        :param input_filter:input_filter.
        :return:command string.
        """
        return str2fill('show firewall filter ' + input_filter)

    def interfaces_queue_match_drop(self, interface):
        """
         show interfaces queue <<Interface>> | match drop
        :param interface:
        :return:
        """
        return str2fill(self.interfaces_queue(interface) + ' | match drop')

    def PE2CE(self, interface, pe_wan, ce_wan, numb=1000):
        """
        ping interface <<Interface>> rapid source <<PE WAN>> <<CE WAN>> count <<numb>>
        :param interface:
        :param pe_wan:
        :param ce_wan:
        :param numb:
        :return:
        """
        return str2fill(
            'ping interface ' + interface + ' rapid source ' + pe_wan + ' ' + ce_wan + ' count ' + str(numb))

    def PE2CE_not_fragment(self, interface, pe_wan, ce_wan, numb=1000):
        """
        ping interface <<Interface>> rapid source <<PE WAN>> <<CE WAN>> count <<numb>> size 1472 do-not-fragment
        :param interface:
        :param pe_wan:
        :param ce_wan:
        :param numb:
        :return:
        """
        return str2fill(self.PE2CE(interface, pe_wan, ce_wan, numb) + ' size 1472 do-not-fragment')

    def state_bgp(self, ce_wan):
        """
        show bgp summary | match <<ce_wan>>
        :param ce_wan:
        :return:
        """
        return str2fill('show bgp summary | match ' + ce_wan)

    def get_bgp_result(self, bgp_note=''):
        """
        get the bgp result from note.
        :param bgp_note: the note from 'show bgp summary | match <<ce_wan>>'.
        :return: string include the state of bgp and connect time.
        """
        if bgp_note.strip() == '':
            return '未建立BGP连接'
        else:
            notes = bgp_note.strip().split()
            if notes[-1].strip() != 'Establ':
                return 'BGP连接中断'
            else:
                if 'd' in notes[-3].strip():
                    return 'BGP连接,时长: ' + notes[-3].strip() + ' ' + notes[-2].strip()
                else:
                    return 'BGP连接,时长: ' + notes[-2].strip()

    # 散装接入
    # PE直接接入\sw散装介入
    def interface_match_error(self, physical_interface):
        """
        show interfaces <<Physical Interface>> extensive | match error
        :param physical_interface:
        :return:
        """
        return str2fill(self.interfaces(physical_interface) + ' | match error')

    def interface_match_link(self, physical_interface):
        """
        show interfaces <<Physical Interface>> extensive | match link
        :param physical_interface:
        :return:
        """
        return str2fill(self.interfaces(physical_interface) + ' | match link')

    # A-B丢包
    # PE-PE WAN-WAN测试
    def interfaces_queue(self, interface):
        """
         show interfaces queue <<Interface>>
        :param interface:
        :return:
        """
        return str2fill('show interfaces queue ' + interface)

    # internet
    # HK ISP
    def traceroute_interface(self, interface, pe_wan, dst_ip):
        """
        traceroute interface <<Interface>> source <<PE WAN>> <<Dst_IP>>
        :param interface:
        :param pe_wan:
        :param dst_ip:
        :return:
        """
        return str2fill('traceroute interface ' + interface + ' source ' + pe_wan + ' ' + dst_ip)

    # other
    def call_package(self, url):
        """
        call URL through the browser to get information by json, and replace the '\\n' to '\n' in the json string.
        :param url: the method submit_command() include the  command and device ip.
        :return: json data.
        """
        return str(urlopen(url).read(), 'utf-8').replace('\\n', '\n')

    def get_input_filter(self, str_interfaces=None):
        """
        get the Input Filters data.
        :param str_interfaces: the note by 'show interfaces <<Interface>> extensive'.
        :return: Input Filters data, or nothing.
        """
        if 'Input Filters:' in str_interfaces:
            return str_interfaces.split('Input Filters:', 1)[1].split('\n')[0].strip()
        else:
            return ''

    def deal_json(self, json_data):
        """
        get the data by  'data' label in json string.
        :param json_data:
        :return:'data'label log.
        """
        return str(json.loads(json_data, strict=False)['data'])

    def interface2physical_interface(self, interface=''):
        """
        interface to physical_interface
        :param interface: interface as 'ge-0/1/0.206'
        :return: physical_interface as 'ge-0/1/0'
        """
        return interface.split('.')[0].strip()

    def get_pe2cp_ip(self, str_interfaces=''):
        """
        get the pe_wan and pe_wan ,judge the 30/31.
        pe/ceIP,30:flag=1,!30:flag=0
        :param str_interfaces:note from 'show interfaces <<Interface>> extensive'
        :return:pe_ip,ce_ip,flag(Destination:30:flag=1,!30:flag=0) or '0,0,0'
        """
        if 'Destination:' in str_interfaces:
            tmps = str_interfaces.split('Destination:', 1)[1].split(',')
            destination_sign = int(tmps[0].split('/')[1].strip())
            pe_ip = tmps[1].split(':')[1].strip().split('.')
            pe_ip_end = int(pe_ip[-1])
            flag = 0
            if destination_sign == 30:
                flag = 1
                if pe_ip_end % 2 == 1:
                    pe_ip[-1] = str(pe_ip_end + 1)
                else:
                    pe_ip[-1] = str(pe_ip_end - 1)
            elif destination_sign == 31:
                if pe_ip_end % 2 == 1:
                    pe_ip[-1] = str(pe_ip_end - 1)
                else:
                    pe_ip[-1] = str(pe_ip_end + 1)
            ce_ip = pe_ip[0] + '.' + pe_ip[1] + '.' + pe_ip[2] + '.' + pe_ip[3]
            return tmps[1].split(':')[1].strip(), ce_ip, flag
        else:
            return 0, 0, 0

    def judge_ping(self, ping_str=''):
        """
        judge ping package loss, if package loss ==100% return False,
        else return True.
        :param ping_str: string from  'ping interface <<Interface>> rapid source \
        <<PE WAN>> <<CE WAN>> count 100' or other ping command.
        :return:True or False.
        """
        loss_package = ping_str.split('packet loss')[0].split(',')[-1].strip('% ')
        if loss_package == '100':
            return False, 'package all loss.'
        else:
            return True, 'loss package: ' + loss_package + '%.'

    def call_package_submit_command(self, command):
        """
        call_package() and submit_command() combine.
        :param command: command.
        :return:json string.
        """
        return self.call_package(self.submit_command(command))

    # 情景：丢包：
    # 本地线路丢包
    def local_line_loss(self, interface, login_ip, number=1000, types=1):
        """
        normal test.
        :param interface:
        :param login_ip:device ip.
        :param number: int ping count.
        :param types: 1:cmd3_1; 2:cmd3_2.
        :return:
        cmd1 = show interfaces <<Interface>> extensive
        cmd2 = show firewall filter <<input filter>>
        cmd3_1 = show interfaces queue <<Interface>> | match drop
        cmd3_2 = show interfaces queue <<Interface>>
        cmd4 =  ping interface <<Interface>> rapid source <<PE WAN>> <<CE WAN>> count <<number>>
        cmd5 = ping interface <<Interface>> rapid source <<PE WAN>> <<CE WAN>> count <<number>> size 1472 do-not-fragment
        """
        self.__ip = login_ip
        cmd1 = self.call_package_submit_command(self.interfaces(interface))
        cmd2 = self.call_package_submit_command(self.firewall(self.get_input_filter(cmd1)))
        if types == 1:
            cmd3 = self.call_package_submit_command(self.interfaces_queue_match_drop(interface))
        elif types == 2:
            cmd3 = self.call_package_submit_command(self.interfaces_queue(interface))
        else:
            cmd3 = ''
        pe_wan, ce_wan, flag = self.get_pe2cp_ip(cmd1)
        cmd4 = self.judge_ping(self.call_package_submit_command(self.PE2CE(interface, pe_wan, ce_wan, numb=10)))
        if cmd4[0]:
            cmd4 = self.judge_ping(
                self.call_package_submit_command(self.PE2CE(interface, pe_wan, ce_wan, number)))
        cmd5 = self.judge_ping(
            self.call_package_submit_command(self.PE2CE_not_fragment(interface, pe_wan, ce_wan, numb=10)))
        if cmd5[0]:
            cmd5 = self.judge_ping(self.call_package_submit_command(self.PE2CE_not_fragment(interface, pe_wan, ce_wan,
                                                                                            number)))
        cmd6 = self.get_bgp_result(self.deal_json(self.call_package_submit_command(self.state_bgp(ce_wan))))
        return cmd1, cmd2, cmd3, cmd4[1], cmd5[1], cmd6

    # 散装接入：
    def bulk_access(self, physical_interface, login_ip):
        """
        :param physical_interface:
        :param login_ip:
        :return:
        cmd1 = show interfaces <<Physical Interface>> extensive | match error
        cmd2 = show interfaces <<Physical Interface>> extensive | match link
        """
        self.__ip = login_ip
        cmd1 = self.call_package_submit_command(self.interface_match_error(physical_interface))
        cmd2 = self.call_package_submit_command(self.interface_match_link(physical_interface))
        return cmd1, cmd2

    def pe2pe_wan2wan(self, interface, pe_wan1, pe_wan2, login_ip, numb=1000):
        """
        :param interface:
        :param pe_wan1:
        :param pe_wan2:
        :param login_ip:
        :param numb:
        :return:
        cmd1 = ping interface <<Interface>> rapid source <<PE WAN>> <<Dst_IP>> count <<numb>>
        cmd2 = ping interface <<Interface>> rapid source <<PE WAN>> <<Dst_IP>> count <<numb>> size 1472 do-not-fragment
        """
        self.__ip = login_ip
        cmd1 = self.judge_ping(self.call_package_submit_command(self.PE2CE(interface, pe_wan1, pe_wan2, 10)))
        if cmd1[0]:
            cmd1 = self.judge_ping(
                self.call_package_submit_command(self.PE2CE(interface, pe_wan1, pe_wan2, numb)))
        cmd2 = self.judge_ping(
            self.call_package_submit_command(self.PE2CE_not_fragment(interface, pe_wan1, pe_wan2, 10)))
        if cmd2[0]:
            cmd2 = self.judge_ping(
                self.call_package_submit_command(self.PE2CE_not_fragment(interface, pe_wan1, pe_wan2, numb)))
        return cmd1[1], cmd2[1]

    def internet_flow(self, interface, dst_ip, login_ip, numb=100):
        """
        internet flowing state.
        :param interface:
        :param dst_ip:
        :param login_ip:
        :param numb:
        :return:
        cmd1 = show interfaces <<Interface>> extensive
        /30: ---- cmd2 = ping interface <<Interface>> rapid source <<PE WAN>> <<CE WAN>> count <<numb>>
        not /30:--cmd2 = ''
        cmd3 = ping interface <<Interface>> rapid source <<PE WAN>> <<Dst_IP>> count <<numb>>
        cmd4 = traceroute interface <<Interface>> source <<PE WAN>> <<Dst_IP>>
        """
        self.__ip = login_ip
        cmd1 = self.call_package_submit_command(self.interfaces(interface))
        pe_wan, ce_wan, flag = self.get_pe2cp_ip(cmd1)
        if flag == 1:
            cmd2 = self.judge_ping(self.call_package_submit_command(self.PE2CE(interface, pe_wan, ce_wan, 10)))
            if cmd2[0]:
                cmd2 = self.judge_ping(self.call_package_submit_command(self.PE2CE(interface, pe_wan, ce_wan, numb)))
        else:
            cmd2 = ['', '']
        cmd3 = self.judge_ping(self.call_package_submit_command(self.PE2CE(interface, pe_wan, dst_ip, 10)))
        if cmd3[0]:
            cmd3 = self.judge_ping(self.call_package_submit_command(self.PE2CE(interface, pe_wan, dst_ip, numb)))
        cmd4 = self.call_package_submit_command(self.traceroute_interface(interface, pe_wan, dst_ip))
        return cmd1, cmd2[1], cmd3[1], cmd4

    def set_ip(self, ip):
        self.__ip = ip


if __name__ == '__main__':
    user = Professional_Work(username='op1768', password='Abc1015')
    user.encode_rsa()
    cmd1 = user.local_line_loss('ge-0/1/0.206', '218.96.240.96', 100, 2)
    cmd2 = user.bulk_access('ge-0/1/0', '218.96.240.96')
    # # cmd3 = user.pe2pe_wan2wan(interface='', pe_wan1='', pe_wan2='', login_ip='', numb=100)
    # # cmd4 = user.internet_flow(interface='', dst_ip='', login_ip='', numb=100)
    # a = user.deal_json(cmd2[1])
    # user.set_ip('218.96.240.95')
    # cmd6 = user.get_bgp_result(user.deal_json(user.call_package(user.submit_command(user.state_bgp('72.17.50.53')))))
