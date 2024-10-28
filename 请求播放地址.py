# -*- coding: utf-8 -*-
# @Time    : 2024/10/23 下午5:45
# @Author  : xiaojing
# @File    : 请求播放地址.py
# @Software: PyCharm
import Utils
import requests
encrypt_data1 = '{"movie_id":"APnNO","from_code":"snm3u8","timestamp":"1729838057"}'
encrypt_data = '{"from_code":"mgtv","play_url":"parse_30a8f9bcff2a0772fe88f2646629360b24c977e74efc8d7aa070147777ad5215af8a8cff62db561dea74ed","episode_id":"43358590","type":"play","timestamp":"1730007068"}'
headers = {
    "Host": "app-v1.ecoliving168.com",
    "user-agent": "Android",
    "accept": "application/prs.55App.v2+json",
    "timestamp": "1730007079",
    "x-client-setting": "{\"pure-mode\":1}",
    "x-client-uuid": "{\"device_id\":\"d92aca9bc1e6adfeb80432c5bbbe3952\", \"type\":1,\"brand\":\"realme\", \"model\":\"RMX3783\", \"system_version\":28, \"sdk_version\":\"3.1.0.5\"}",
    "x-client-version": "3095",
    "x-app-version": "3096",
    "x-app-lang": "zh_CN"
}
# url = "https://app-v1.ecoliving168.com/api/v1/movie_addr/parse_url"
url = "https://app-v1.ecoliving168.com/api/v1/movie_addr/list"

params = {}

utils = Utils.Utils()
pack = utils.get_pack(encrypt_data1)
signature = utils.get_sign(pack)
params["pack"] = pack
params["signature"] = signature


response = requests.get(url, headers=headers, params=params)

print(response.text)
print(response)