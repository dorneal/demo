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
    爬取携程指定起始位置、日期的机票信息
"""


def get_json2(start_data, arrivals_date, rk, CK, r):
    """
    根据构造出的url获取到航班数据
    :param start_data:  出发日期
    :param rk:  url参数
    :param CK:  url参数
    :param r:   url参数
    :return:
    """
    # 构造url参数
    url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=SZX&ACity1=SHA&SearchType=D&DDate1=%s&ACity2=SZX&DDate2=%s&IsNearAirportRecommond=0&LogToken=266dfbfd421d46cebc51cd5af13d5b97&rk=%s&CK=%s7&r=%s" % (
        start_data, arrivals_date, rk, CK, r)
    # 填充请求头
    headers = {'Host': "flights.ctrip.com",
               'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
               'Referer': "http://flights.ctrip.com/booking/SZX-SHA---D-adu-1/?dayoffset=0&ddate1=%s&ddate2=%s" % (
                   start_data, arrivals_date)}
    # 请求
    req = Request(url, headers=headers)
    # 响应结果
    res = urlopen(req)
    # 读取解码
    content = res.read().decode("gbk")
    # 解析为json格式
    dict_content = json.loads(content)
    length = len(dict_content['fis'])
    print("共{0}种机票选择".format(length))
    for i in range(length):
        # 打印出发时间,到达时间
        print(dict_content['fis'][i][u'dt'] + " ———— " + dict_content['fis'][i][u'at'])
        # 打印到达时间
        # print(dict_content['fis'][i][u'at'])
        # 打印机票价格
        print("票价：" + str(dict_content['fis'][i][u'rtp']))


def get_parameter(date1, date2):
    """
    获取重要的参数，构造url参数（反向获取参数）
    :param date1:日期，格式示例：2016-05-13
    :return:rk,CK,r url参数
    """
    # 构造出url
    url = "http://flights.ctrip.com/booking/SZX-SHA---D-adu-1/?dayoffset=0&ddate1=%s&ddate2=%s" % (
        date1, date2)
    # 请求
    res = urlopen(url).read()
    # 解析xml
    tree = etree.HTML(res)
    # 解析响应的脚本，获取url，破解出重要url参数
    pp = tree.xpath('''//body/script[1]/text()''')[0].split()
    CK_original = pp[3][-34:-2]
    CK = CK_original[0:5] + CK_original[13] + CK_original[5:13] + CK_original[14:]

    rk = pp[-1][18:24]
    num = random.random() * 10
    num_str = "%.15f" % num
    rk = num_str + rk
    r = pp[-1][27:len(pp[-1]) - 3]
    # 返回重要url参数
    return rk, CK, r


if __name__ == '__main__':
    dates = ['2018-04-10', '2018-04-20', '2018-04-22', '2018-05-10']
    date2 = '2018-05-10'
    for date in dates:
        rk, CK, r = get_parameter(date, date2)
        print(date + "时:")
        get_json2(date, date2, rk, CK, r)
        print("====================================")
