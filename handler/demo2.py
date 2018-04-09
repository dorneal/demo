#!/usr/bin/python3
# coding:utf-8
# Filename:demo2.py
# Author:Neal
# Time:2018 04 09 21:07

import json
import random
from urllib.request import Request
from urllib.request import urlopen

from lxml import etree

"""
    爬取携程的机票信息
"""


def get_json2(date, rk, CK, r):
    """
    根据构造出的url获取到航班数据
    :param date:  出发日期
    :param rk:  url参数
    :param CK:  url参数
    :param r:   url参数
    :return:
    """
    url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=SZX&ACity1=SHA&SearchType=D&DDate1=%s&ACity2=SZX&DDate2=2018-05-10&IsNearAirportRecommond=0&LogToken=266dfbfd421d46cebc51cd5af13d5b97&rk=%s&CK=%s7&r=%s" % (
        date, rk, CK, r)
    headers = {'Host': "flights.ctrip.com",
               'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
               'Referer': "http://flights.ctrip.com/booking/hrb-sha-day-1.html?ddate1=2018-04-29"}
    headers['Referer'] = "http://flights.ctrip.com/booking/hrb-sha-day-1.html?ddate1=%s" % date
    req = Request(url, headers=headers)
    res = urlopen(req)
    # 读取解码
    content = res.read().decode("gbk")
    # 解析json
    dict_content = json.loads(content)
    length = len(dict_content['fis'])
    # print length
    for i in range(length):
        # 打印出发时间
        print(dict_content['fis'][i][u'dt'])
        # 打印到达时间
        print(dict_content['fis'][i][u'at'])
        # 打印机票价格
        print(dict_content['fis'][i][u'rtp'])


def get_parameter(date):
    """
    获取重要的参数，构造url参数（反向获取参数）
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
