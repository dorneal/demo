#!/usr/bin/python3
# coding:utf-8
# Filename:demo3.py
# Author:黄鹏
# Time:2018.04.10 9:54
import http.cookiejar
import json
import random
import urllib
from urllib import parse
from urllib.request import Request
from urllib.request import urlopen

from lxml import etree

"""
    爬取携程指定起始位置、日期的机票信息
"""


def get_json2(start_date, arrivals_date, rk, CK, r):
    """
    根据构造出的url获取到航班数据
    :param start_date:  出发时间
    :param arrivals_date:  到达时间
    :param rk:  url参数
    :param CK:  url参数
    :param r:   url参数
    :return:  list
    """
    # 构造url参数
    url_dict = {
        'DCity1': 'SZX',
        'ACity1': 'SHA',
        'SearchType': 'D',
        'DDate1': start_date,
        'ACity2': 'SZX',
        'DDate2': arrivals_date,
        'IsNearAirportRecommond': 0,
        'rk': rk,
        'CK': CK,
        'r': r
    }
    # 加工构造出的url参数
    url_data = urllib.parse.urlencode(url_dict)
    # 填充url
    url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?" + url_data

    # 填充请求头
    headers = {'Host': "flights.ctrip.com",
               'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                             "65.0.3325.181 Safari/537.36",
               'Referer': "http://flights.ctrip.com/booking/SZX-SHA---D-adu-1/?dayoffset=0&ddate1=%s&ddate2=%s" % (
                   start_date, arrivals_date)}
    req = Request(url, headers=headers, method='GET')

    # 是否使用ip代理
    # proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    # opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    # urllib.request.install_opener(opener)

    # 使用http.cookiejar.CookieJar()创建CookieJar对象
    cookie_jar = http.cookiejar.CookieJar()
    # 使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
    cookie = urllib.request.HTTPCookieProcessor(cookie_jar)
    opener = urllib.request.build_opener(cookie)
    # 将opener安装为全局
    urllib.request.install_opener(opener)

    # 请求，响应结果
    res = urlopen(req)
    # 读取解码
    content = res.read().decode("gbk")
    # 将结果转为json格式
    dict_content = json.loads(content)

    # 解析json
    length = len(dict_content['fis'])
    if length == 0:
        print('\033[1;31;40m')
        print("返回为空，请检查是否存在问题！")
        print('\033[0m')
        return None
    else:
        print("共{0}种机票选择".format(length))
        result_list = []
        for i in range(length):
            result_dict = {}
            start_time = dict_content['fis'][i][u'dt']
            arrivals_time = dict_content['fis'][i][u'at']
            price = dict_content['fis'][i][u'rtp']

            # 控制台打印出发时间,到达时间
            # print(start_time + " ———— " + arrivals_time)
            # 打印机票价格
            # print("票价：" + str(price))

            # 数据装填
            result_dict['start_time'] = start_time
            result_dict['arrivals_time'] = arrivals_time
            result_dict['price'] = price
            result_list.append(result_dict)
        return result_list


def get_parameter(date1, date2):
    """
    获取重要的参数，构造url参数（反向获取参数）
    :param date1:出发日期，格式示例：2016-05-13
    :param date2:返程日期
    :return:rk,CK,r url参数
    """
    # 构造出url，第一次请求该url为了获取url的重要参数
    url = "http://flights.ctrip.com/booking/SZX-SHA---D-adu-1/?dayoffset=0&ddate1=%s&ddate2=%s" % (
        date1, date2)
    # 请求
    response = urlopen(url)
    if response.status == 200:

        # 解析html
        res = response.read()
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
    else:
        print('\033[1;31;40m')
        print("返回为空，请检查是否存在问题！")
        print('\033[0m')
        return None


if __name__ == '__main__':
    # 出发日期
    dates = ['2018-04-11', '2018-04-20', '2018-04-22']
    # 返程日期
    end_date = '2018-05-10'

    # 写入文本
    filename = r"C:\Users\Administrator\Desktop\workspace\day0410\test2.txt"
    f = open(filename, "a+", encoding="utf-8")

    for date in dates:
        rk, CK, r = get_parameter(date1=date, date2=end_date)
        print(date + "时:")
        print("====================================")
        results = get_json2(date, end_date, rk, CK, r)
        print(results)
        for result in results:
            f.write("出发时间 {0} --> 到达时间 {1} ，票价：{2}\n".format(result['start_time'],
                                                             result['arrivals_time'],
                                                             result['price']))
        f.write("\n")
        f.flush()
    f.close()
