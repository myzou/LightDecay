# -*- coding: utf-8 -*-

import rsa

# 生成密钥
(pubkey, privkey) = rsa.newkeys(2048)
# =================================
# 场景〇：密钥保存导入
# =================================

# 保存密钥
with open('public.pem' ,'w+') as f:
    f.write(pubkey.save_pkcs1().decode())
with open('private.pem' ,'w+') as f:
    f.write(privkey.save_pkcs1().decode())

#导入密钥
with open('public.pem' ,'r') as f:
    pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())

with open('private.pem','r') as f:
    privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

# with open('./rsa_public_key.pem','r') as f:
#     pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
#
# with open('./rsa_private_key.pem','r') as f:
#     privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

"""
加密 RSA
"""
def rsa_encrypt(message):
    crypto_email_text = rsa.encrypt(message.encode(), pubkey)
    return crypto_email_text

# message = "这是商机：..."
# print(pubkey,"\n")
# crypto_email_text = rsa.encrypt(message.encode(), pubkey)
# print(crypto_email_text)

text = rsa_encrypt("hello world")
print("加密前:hello world")
print("加密后:"+text.decode('utf8','ignore'))


"""
解密
"""
def rsa_decrypt(message):
    message_str = rsa.decrypt(message,privkey).decode('utf8','ignore')
    return message_str

message = rsa_decrypt(text)
print("解密前:"+text.decode('utf8','ignore'))
print("解密后:"+message)


"""
签名
"""
# message = '这是重要指令：...'
# crypto_email_text = rsa.sign(message.encode(), privkey, 'SHA-1')

"""
验证
"""
# 收到指令明文、密文，然后用公钥验证，进行身份确认
# rsa.verify(message.encode(), crypto_email_text, pubkey)
