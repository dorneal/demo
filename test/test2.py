#!/usr/bin/python3
# coding:utf-8
# Filename:test2.py
# Author:黄鹏
# Time:2018.04.12 10:18
import urllib.request

import requests

"""
测试代理
"""

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                         "65.0.3325.181 Safari/537.36"}
url = "http://icanhazip.com/"
proxies = {
    "http": "http://180.250.174.251:8080"
}
print(requests.get(url=url, headers=headers, proxies=proxies, timeout=30).text)

proxy = urllib.request.ProxyHandler(proxies)
opener1 = urllib.request.build_opener(proxy)
urllib.request.install_opener(opener1)

req = urllib.request.Request(url=url, headers=headers, method='GET')
print(urllib.request.urlopen(req).read())
