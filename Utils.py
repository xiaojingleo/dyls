# -*- coding: utf-8 -*-
# @Time    : 2024/10/24 上午10:07
# @Author  : xiaojing
# @File    : Utils.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2024/10/23 下午5:48
# @Author  : xiaojing
# @File    : 参数破解.py
# @Software: PyCharm
# __all__ = ['get_pack', 'get_sign', 'get_search_params']

import datetime
import hmac
import hashlib
import json

import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

import base64


class Utils:
    def __init__(self):
        self.secret_key = "635a580fcb5dc6e60caa39c31a7bde48"
        self.public_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA02F/kPg5A2NX4qZ5JSns+bjhVMCC6JbTiTKpbgNgiXU+Kkorg6Dj76gS68gB8llhbUKCXjIdygnHPrxVHWfzmzisq9P9awmXBkCk74Skglx2LKHa/mNz9ivg6YzQ5pQFUEWS0DfomGBXVtqvBlOXMCRxp69oWaMsnfjnBV+0J7vHbXzUIkqBLdXSNfM9Ag5qdRDrJC3CqB65EJ3ARWVzZTTcXSdMW9i3qzEZPawPNPe5yPYbMZIoXLcrqvEZnRK1oak67/ihf7iwPJqdc+68ZYEmmdqwunOvRdjq89fQMVelmqcRD9RYe08v+xDxG9Co9z7hcXGTsUquMxkh29uNawIDAQAB\n-----END PUBLIC KEY-----'
        self.headers = {
            "Host": "app-v1.ecoliving168.com",
            "user-agent": "Android",
            "accept": "application/prs.55App.v2+json",
            "timestamp": "1731958146",
            "x-client-setting": "{\"pure-mode\":1}",
            "x-client-uuid": "{\"device_id\":\"d92aca9bc1e6adfeb80432c5bbbe3952\", \"type\":1,\"brand\":\"realme\", \"model\":\"RMX3783\", \"system_version\":28, \"sdk_version\":\"3.1.0.5\"}",
            "x-client-version": "3096",
            "x-app-version": "3096",
            "x-app-lang": "zh_CN"
        }
        self.url = "https://app-v1.ecoliving168.com/api/v1/movie/index_recommend"
        self.params = {
            "pack": "WG9fMSsATFFhTWK2Q3X5pGD7oSm0PTClZDZCaso8sGrLxxEjL-q6WLpXkPCEmd9lGYG7lm-bHdQ5GwItKfyP9TsbQac7h7xLwqCDtwOLL_M-f2vk6_jpRWIMql8Q4v-qtyg0_5sifv5hhTzDUvGDgk-T88PP6eOIPuVrhVGuydrgO-uqCTYDpbF8zUh3haBoAnIUnfVdeGvm1QdhXolU_ufbOdNYB6_MuF-0ocqi4W7UrxANNC2dI68yDgOhnhTxR8DsnWnRv2SgmFWg3WNmqo5EF76WWcTczyaRR8pYI_TNRnSoqH9vLv8Ye-w7arlUJPsv4fR3Mq_zCtwXRY-DVA",
            "signature": "05fced1957924a1429a35f5ad3ec5492"
        }

    def get_timestamp(self):
        timestamp = str(int(datetime.datetime.now().timestamp()))
        return timestamp

    def hmac_md5(self, encrypt_data):
        hmac_digest = hmac.new(self.secret_key.encode('utf-8'), encrypt_data.encode('utf-8'), hashlib.md5).hexdigest()
        return hmac_digest

    def get_pack(self, params):
        # 使用公钥加密密码字符串
        rsakey = RSA.import_key(self.public_key)
        cipher = PKCS1_v1_5.new(rsakey)
        pack = base64.b64encode(cipher.encrypt(params.encode()))
        return pack.decode()
        # pack = pack.decode()

    def get_sign(self, pack):
        sign = self.hmac_md5(pack)
        return sign

    def get_search_params(self, keyword, page="1", pageSize="10", res_type="by_movie_name"):
        json_data = {
            "keyword": keyword,
            "page": page,
            "pageSize": "10",
            "res_type": "by_movie_name",
            "timestamp": self.get_timestamp()
        }
        return json.dumps(json_data)

    """
    type_id: 类型id 电影：1，电视剧：2，综艺：3，动漫：4，短视频：36，隐藏：26
    """

    def get_list_params(self, type_id, _class='类型', area="地区", year="年份", page="1", pagesize="21"):
        json_data = {
            "type_id": type_id,
            "sort": "by_default",
            "class": "类型",
            "area": "地区",
            "year": "年份",
            "page": page,
            "pageSize": "21",
            "timestamp": self.get_timestamp()
        }
        return json.dumps(json_data)

    def get_detail_params(self, movie_id):
        json_data = {
            "id": movie_id,
            "timestamp": self.get_timestamp()
        }
        return json.dumps(json_data)

    def get_list(self, type_id, page="1", _class='类型', area="地区", year="年份", pagesize="21"):
        # self.url = "https://app-v1.ecoliving168.com/api/v1/movie/index_recommend"
        self.url = "https://app-v1.ecoliving168.com/api/v1/movie/screen/list"
        params = {
            "pack": "",
            "signature": ""
        }
        par = self.get_list_params(type_id, _class, area, year, page, pagesize)
        params["pack"] = self.get_pack(par)
        # params["pack"] = "bUEIIS8KD/0q6rWgtdvpbuCoZtekVXTEQFMXJN/e1vrxnpDoKrpl2nKmY0GiE0PJ04e2BHPamZSoBGaer0Pxi245fbvLY/NszhJT6cFSV4cZAD9RlMP6fmv1/TeHaBEBw5iKuy6+uC7zddRL4jARL9X3OrZbV9BvaWGJXbXJUNJJJwV+8+c1uNShX+xo/VUYmQWZTAvaLPITKyU8la6rQqrL+PHAmJIj/RrpmmmlgRsN09e89bW+EgP+F2BpXsEQY821jSgQSCh7FFsaDnd2iElYjzHj2Kdz0UDtbQbsVjVnJ3++2xUKx4BPt+fcfr93r/bqXm7rXnl2a2zEy4XW+g=="
        params["signature"] = self.get_sign(params["pack"])

        print(params)
        response = requests.get(self.url, headers=self.headers, params=params)
        return response.text

    def get_search_list(self, keyword):
        self.url = "https://app-v1.ecoliving168.com/api/v1/movie/search"
        response = requests.get(self.url, headers=self.headers, params=self.params)
        return response.text

    def get_detail(self, id):
        self.url = "https://app-v1.ecoliving168.com/api/v1/movie/detail"
        par = self.get_detail_params(id)
        params = {}
        params["pack"] = self.get_pack(par)
        params["signature"] = self.get_sign(params["pack"])
        response = requests.get(self.url, headers=self.headers, params=params)
        return response.text

    # def get_play(self):
    #     self.url = "https://app-v1.ecoliving168.com/api/v1/movie/play"
    #     response = requests.get(self.url, headers=self.headers, params=self.params)
    #     return response.text

    def get_play_url(self, id, from_code="youku", play_url="parse_30a8f9bcff2a0772ffd1fc257e25375369c575a517c1d124f6350a2e27dd386afdf9c0833ba60f38da48b31f79d2d7fadbf90cbe",episode_id="13283680"):
        json_data = {"movie_id": id, "from_code": from_code, "timestamp": self.get_timestamp()}
        match from_code:
            case "youku":
                self.url = 'https://app-v1.ecoliving168.com/api/v1/movie_addr/parse_url'
                json_data = {"from_code":"youku","play_url":play_url,"episode_id":episode_id,"type":"play","timestamp":self.get_timestamp()}
            case _:
                self.url = "https://app-v1.ecoliving168.com/api/v1/movie_addr/list"
        par = json.dumps(json_data)
        self.params["pack"] = self.get_pack(par)
        self.params["signature"] = self.get_sign(self.params["pack"])
        response = requests.get(self.url, headers=self.headers, params=self.params)
        return response.text

utils = Utils()
print(utils.get_play_url())

