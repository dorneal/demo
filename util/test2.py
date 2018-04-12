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
url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=AAT&ACity1=AKU&SearchType=D&DDate1=2018-04-11&ACity2=AAT&DDate2=2018-05-10&IsNearAirportRecommond=0&rk=8.768160367946448163808&CK=67A6445B9F5133B388F786D7B8500BF8&r=0.32140532119115295750119"
print(requests.get(url=url, proxies={'http': "180.168.184.179:53128"}).text)

proxy = urllib.request.ProxyHandler({'http': "180.168.184.179:53128"})
opener1 = urllib.request.build_opener(proxy)
urllib.request.install_opener(opener1)

req = urllib.request.Request(url="http://httpbin.org/ip", headers=headers, method='GET')
print(urllib.request.urlopen(req).read())
