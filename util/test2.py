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
print(requests.get(url="http://httpbin.org/ip", proxies={'http': "119.96.194.46:3128"}).json())

proxy = urllib.request.ProxyHandler({'http': "71.13.112.152:3128"})
opener1 = urllib.request.build_opener(proxy)
urllib.request.install_opener(opener1)

req = urllib.request.Request(url="http://httpbin.org/ip", headers=headers, method='GET')
print(urllib.request.urlopen(req).read())
