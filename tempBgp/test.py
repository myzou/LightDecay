# coding:utf-8

import configparser

config = configparser.ConfigParser()
config.read('config.conf')
lists_header = config.sections()  # 配置组名, ['luzhuo.me', 'mysql'] # 不含'DEFAULT'
print(lists_header)
print(config['login'])
print(config['default_config'])

loginOP=config.get('login','loginOP')
loginOPPassword=config.get('login','loginOPPassword')
ggwApiUrl=config.get('default_config','')
sign=config.get('default_config','sign');
command1=config.get('default_config','command1');

