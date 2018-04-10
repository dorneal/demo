#!/usr/bin/python3
# coding:utf-8
# Filename:demo4.py
# Author:黄鹏
# Time:2018.04.10 11:59


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
    缺点：抓包分析难，js脚本太多，加密的参数
    优点：快速，准确，易分析，灵活性强
"""


def get_json2(this_city, other_city, start_date, arrivals_date, rk, CK, r):
    """
    根据构造出的url获取到航班数据
    :param this_city: 出发城市
    :param other_city: 目的城市
    :param start_date:  出发时间
    :param arrivals_date:  到达时间
    :param rk:  url参数
    :param CK:  url参数
    :param r:   url参数
    :return:  list
    """
    # 构造url参数
    url_dict = {
        'DCity1': this_city,
        'ACity1': other_city,
        'SearchType': 'D',
        'DDate1': start_date,
        'ACity2': this_city,
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
               'Referer': "http://flights.ctrip.com/booking/%s-%s---D-adu-1/?dayoffset=0&ddate1=%s&ddate2=%s" % (
                   this_city, other_city, start_date, arrivals_date)}
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
    length = 0
    length2 = 0
    if dict_content['fis']:
        length = len(dict_content['fis'])
    if dict_content['tf']:
        length2 = len(dict_content['tf'])

    if length == 0:
        if length2 == 0:
            print('\033[1;31;40m')
            print("暂时没有航班信息！")
            print('\033[0m')
        else:
            print("共{0}种机票选择".format(length2))
            result_list = []
            for i in range(length2):
                result_dict = {}
                start_time = dict_content['tf'][i][u'dt']
                arrivals_time = dict_content['tf'][i][u'at']
                price = dict_content['tf'][i][u'rtp']

                # 数据装填
                result_dict['start_time'] = start_time
                result_dict['arrivals_time'] = arrivals_time
                result_dict['price'] = price
                result_list.append(result_dict)
            return result_list
    else:
        print("共{0}种机票选择".format(length))
        result_list = []
        for i in range(length):
            result_dict = {}
            start_time = dict_content['fis'][i][u'dt']
            arrivals_time = dict_content['fis'][i][u'at']
            price = dict_content['fis'][i][u'rtp']

            # 数据装填
            result_dict['start_time'] = start_time
            result_dict['arrivals_time'] = arrivals_time
            result_dict['price'] = price
            result_list.append(result_dict)
        return result_list


def get_parameter(this_city, other_city, date1, date2):
    """
    获取重要的参数，构造url参数（逆向获取参数）
    :param date1:出发日期，格式示例：2016-05-13
    :param date2:返程日期
    :param this_city: 出发城市
    :param other_city: 目的城市
    :return:rk,CK,r url参数
    """
    # 构造出url，第一次请求该url为了获取url的重要参数
    url = "http://flights.ctrip.com/booking/%s-%s---D-adu-1/?dayoffset=0&ddate1=%s&ddate2=%s" % (
        this_city, other_city, date1, date2)
    # 请求
    response = urlopen(url)
    if response.status == 200:

        # 解析html
        res = response.read()
        tree = etree.HTML(res)

        # 解析响应的脚本，获取url，破解出重要url参数
        try:
            pp = tree.xpath("//body/script[1]/text()")[0].split()
        except IndexError:
            print("国际航班暂未分析Js脚本如何是如何加密参数！")
            return '', '', ''
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
        print("航班信息为空")
        print('\033[0m')


if __name__ == '__main__':
    # 出发日期
    dates = ['2018-04-11']
    # 返程日期
    end_date = '2018-05-10'

    # 写入文本
    filename = r"C:\Users\Administrator\Desktop\workspace\day0410\test4.txt"
    f = open(filename, "a+", encoding="utf-8")

    # 读取城市信息
    f2 = open(r"C:\Users\Administrator\Desktop\workspace\day0410\cities.txt", encoding="utf-8")
    # 城市后缀编号列表
    city_num_list = []
    # 城市名列表
    city_name_list = []
    while True:
        city = f2.readline().strip()
        if not city:
            break
        city_num_list.append(city[-4:-1])
        city_name_list.append(city[:-5])

    city_length = len(city_num_list)

    """
        在指定出发日期内访问，遍历所有城市，两两之间的航班信息
    """

    for date in dates:
        # 在该日期下，双遍历（两城市之间的航班信息）
        for i in range(city_length):
            # 下标，从+1开始
            for j in range(i + 1, city_length):
                # 获取加密url参数
                rk, CK, r = get_parameter(city_num_list[i], city_num_list[j], date1=date, date2=end_date)
                print(date + "时:")
                print("====================================")
                # 如果不为空
                if rk and CK and r:
                    # 进行航班信息加载及解析
                    results = get_json2(city_num_list[i], city_num_list[j], date, end_date, rk, CK, r)
                    print(results)
                    # 写入两城市间名字
                    f.write("{0} 到 {1}\n".format(city_name_list[i], city_name_list[j]))
                    if results:
                        # 将所有航班信息写入
                        for result in results:
                            f.write("出发时间 {0} --> 到达时间 {1} ，票价：{2}\n".format(result['start_time'],
                                                                             result['arrivals_time'],
                                                                             result['price']))
                    else:
                        f.write("暂无航班\n")
                    f.write("\n")
                    f.flush()
    f.close()
