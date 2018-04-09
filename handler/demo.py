#!/usr/bin/python3
# coding:utf-8
# Filename:demo.py
# Author:Neal
# Time:2018 04 09 19:36


import json
import random
from urllib.request import Request
from urllib.request import urlopen

from lxml import etree


def get_json2(date, rk, CK, r):
    """
    根据构造出的url获取到航班数据
    :param date:  日期
    :param rk:
    :param CK:
    :param r:
    :return:
    """

    url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=SHA&ACity1=SIA&SearchType=S&DDate1=%s&IsNearAirportRecommond=0&rk=%s&CK=%s&r=%s" % (
        date, rk, CK, r)
    headers = {'Host': "flights.ctrip.com",
               'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
               'Referer': "http://flights.ctrip.com/booking/hrb-sha-day-1.html?ddate1=2018-04-29"}
    headers['Referer'] = "http://flights.ctrip.com/booking/hrb-sha-day-1.html?ddate1=%s" % date
    req = Request(url, headers=headers)
    res = urlopen(req)
    content = res.read().decode("gbk")
    dict_content = json.loads(content)
    length = len(dict_content['fis'])
    # print length
    for i in range(length):
        if ((dict_content['fis'][i][u'lp']) < 600):
            print(dict_content['fis'][i][u'dt']),
            print(dict_content['fis'][i][u'at']),
            print(dict_content['fis'][i][u'rtp'])
            # print (dict_content['fis'][i][u'dpbn'])


def get_parameter(date):
    """
    获取重要的参数
    :param date:日期，格式示例：2016-05-13
    :return:
    """

    url = 'http://flights.ctrip.com/booking/hrb-sha-day-1.html?ddate1=%s' % date
    res = urlopen(url).read()
    tree = etree.HTML(res)
    pp = tree.xpath('''//body/script[1]/text()''')[0].split()
    CK_original = pp[3][-34:-2]
    CK = CK_original[0:5] + CK_original[13] + CK_original[5:13] + CK_original[14:]

    rk = pp[-1][18:24]
    num = random.random() * 10
    num_str = "%.15f" % num
    rk = num_str + rk
    r = pp[-1][27:len(pp[-1]) - 3]

    return rk, CK, r


if __name__ == '__main__':
    dates = ['2018-04-10', '2018-04-20', '2018-04-22', '2018-05-10']

    for date in dates:
        rk, CK, r = get_parameter(date)
        get_json2(date, rk, CK, r)
        print("-----")
