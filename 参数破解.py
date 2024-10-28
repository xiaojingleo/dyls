# -*- coding: utf-8 -*-
# @Time    : 2024/10/23 下午5:48
# @Author  : xiaojing
# @File    : 参数破解.py
# @Software: PyCharm
__all__ = ['get_pack', 'get_sign', ]

import datetime

import hmac
import hashlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

import base64




secret_key = "635a580fcb5dc6e60caa39c31a7bde48"
public_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA02F/kPg5A2NX4qZ5JSns+bjhVMCC6JbTiTKpbgNgiXU+Kkorg6Dj76gS68gB8llhbUKCXjIdygnHPrxVHWfzmzisq9P9awmXBkCk74Skglx2LKHa/mNz9ivg6YzQ5pQFUEWS0DfomGBXVtqvBlOXMCRxp69oWaMsnfjnBV+0J7vHbXzUIkqBLdXSNfM9Ag5qdRDrJC3CqB65EJ3ARWVzZTTcXSdMW9i3qzEZPawPNPe5yPYbMZIoXLcrqvEZnRK1oak67/ihf7iwPJqdc+68ZYEmmdqwunOvRdjq89fQMVelmqcRD9RYe08v+xDxG9Co9z7hcXGTsUquMxkh29uNawIDAQAB\n-----END PUBLIC KEY-----'

def hmac_md5(encrypt_data):
    hmac_digest = hmac.new(secret_key.encode('utf-8'), encrypt_data.encode('utf-8'), hashlib.md5).hexdigest()
    return hmac_digest

def get_pack(params):
    timestamp =datetime.datetime.now().timestamp()
    timestamp = str(int(timestamp))
    # print(timestamp)
    params = '{"type_id":"1","sort":"by_default","class":"类型","area":"地区","year":"年份","page":"3","pageSize":"21","timestamp":"1729731529"}'
    # search = '{"keyword":"现在就出发","page":"1","pageSize":"10","res_type":"by_movie_name","timestamp":"'+timestamp+'"}'

    # 使用公钥加密密码字符串
    rsakey = RSA.import_key(public_key)
    cipher = PKCS1_v1_5.new(rsakey)
    pack = base64.b64encode(cipher.encrypt(params.encode()))
    return pack
    # pack = pack.decode()
def get_sign(pack):
    sign = hmac_md5(pack)
    return sign