#!/usr/bin/python3
# coding:utf-8
# Filename:demo4.py
# Author:黄鹏
# Time:2018.04.10 11:59
import http
import json
import random
import urllib
from urllib import parse
from urllib.request import Request
import requests
from lxml import etree

"""
    为完善版
"""


def filling_headers(url, headers, proxy_addr):
    """
    请求头的填充
    :param url: Url地址
    :param headers: 头部信息
    :param proxy_addr: 代理ip
    :return: 响应对象
    """

    # 使用ip代理
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener1 = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener1)

    req = urllib.request.Request(url=url, headers=headers, method='GET')

    # 返回响应
    return req


def get_flight_msg(this_city, other_city, start_date, arrivals_date, proxy_addr, rk, CK, r):
    """
    根据构造出的url获取到航班数据
    :param this_city: 出发城市
    :param other_city: 目的城市
    :param start_date:  出发时间
    :param arrivals_date:  到达时间
    :param proxy_addr: 代理IP
    :param rk:  url参数
    :param CK:  url参数
    :param r:   url参数
    :return:  list
    """
    # 构造url参数
    url_dict = {
        'DCity1': this_city,
        'ACity1': other_city,
        'SearchType': 'D',  # 搜索类型D为往返，S为单程
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

    # url添加参数
    url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?" + url_data

    headers = {
        'Host': "flights.ctrip.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/65.0.3325.181 Safari/537.36",
        'Referer': "http://flights.ctrip.com/booking/%s-%s---D-adu-1/?dayoffset=0&ddate1=%s&ddate2=%s" % (
            this_city, other_city, start_date, arrivals_date)}

    # 填充信息
    req = filling_headers(url, headers, proxy_addr)

    # 请求，响应结果
    try:
        res = urllib.request.urlopen(req, timeout=30)
    except:
        # TODO 待解决
        print("-_-||，失去响应!!!，url地址为 {0} ".format(url))
        return None

    # 读取解码
    content = res.read().decode("gbk")
    # 将结果转为json格式
    dict_content = json.loads(content)

    # 如果出现错误
    if dict_content['Error']:
        if dict_content['Error']['Code'] == 103:
            print(dict_content['Error']['Message'])
        if dict_content['Error']['Code'] == 1004:
            print("IP被封！")
            return None

    # 解析json
    # 直达航班信息
    direct_length = len(dict_content['fis']) if dict_content['fis'] else 0
    # 中转航班信息
    transfer_length = len(dict_content['tf']) if dict_content['tf'] else 0

    if direct_length == 0:
        if transfer_length == 0:
            print("暂时没有航班信息！")
        else:
            # TODO 暂未做航班的分类，中转航班未做处理
            # 中转航班信息
            print("共{0}种机票选择".format(transfer_length))

            # 数据装填
            result_list = []
            for i in range(transfer_length):
                result_dict = {
                    'start_time': dict_content['tf'][i][u'dt'],
                    'arrivals_time': dict_content['tf'][i][u'at'],
                    'price': dict_content['tf'][i][u'rtp']}

                result_list.append(result_dict)
            return result_list
    else:
        # 直达航班信息
        print("共{0}种机票选择".format(direct_length))

        # 数据装填
        result_list = []
        for i in range(direct_length):
            result_dict = {
                'start_time': dict_content['fis'][i][u'dt'],
                'arrivals_time': dict_content['fis'][i][u'at'],
                'price': dict_content['fis'][i][u'rtp']}

            result_list.append(result_dict)
        return result_list


def get_parameter(this_city, other_city, proxy_addr, date1, date2):
    """
    获取重要的参数，构造url参数（逆向获取参数）
    :param date1:出发日期，格式示例：2016-05-13
    :param date2:返程日期
    :param this_city: 出发城市
    :param other_city: 目的城市
    :param proxy_addr: 代理IP
    :return:rk,CK,r url参数
    """
    # 构造出url，第一次请求该url为了获取url的重要参数
    url = "http://flights.ctrip.com/booking/%s-%s---D-adu-1/?dayoffset=0&ddate1=%s&ddate2=%s&searchtype=D" % (
        this_city, other_city, date1, date2)

    headers = {
        'Host': "flights.ctrip.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "65.0.3325.181 Safari/537.36",
        'Referer': "http://flights.ctrip.com/"}

    # 填充信息
    req = filling_headers(url, headers, proxy_addr)

    # 请求
    try:
        response = urllib.request.urlopen(req, timeout=30)
    except:
        # TODO 待解决
        print("在求参的时候超时！！！请求地址为 {0} ".format(url))
        return "", "", ""

    cookie = http.cookiejar.CookieJar()
    cookieProc = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookieProc)
    urllib.request.install_opener(opener)

    if response.status == 200:
        # 解析html
        res = response.read()
        tree = etree.HTML(res)

        # 解析响应的脚本，获取url，破解出重要url参数
        try:
            pp = tree.xpath("//body/script[1]/text()")[0].split()
        except IndexError:
            print("国际航班暂未分析Js脚本如何是如何加密参数！")
            return None, None, None
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
        print("响应失败！响应码{0}".format(response.status))
        return '', '', ''


def test_proxy_ip(ip_pool):
    """
    从代理池中选出一个可用的代理地址
    :param ip_pool: 代理池
    :return: ip and port
    """
    # 随机从代理池中选出一个IP、Port
    ip_port = random.choice(ip_pool)
    try:
        requests.get("http://flights.ctrip.com", proxies={"http": ip_port}, timeout=30)
    except:
        print('代理ip：{0} 不可用！'.format(ip_port))
        # 该ip不可用时，继续选取
        ip_pool.remove(ip_port)
        return test_proxy_ip(ip_pool)
    else:
        print('可用代理：{0}'.format(ip_port))
        return ip_port


if __name__ == '__main__':
    # 出发日期
    dates = ['2018-04-11']
    # 返程日期
    return_date = '2018-05-10'

    # 将航班信息保存到文本
    filename = r"C:\Users\Administrator\Desktop\workspace\day0410\test7.txt"
    save_msg = open(filename, "a+", encoding="utf-8")

    # 读取城市信息
    city_msg = open(r"../resource/cities.txt", encoding="utf-8")
    # 城市后缀编号列表（用于传递参数）
    city_num_list = []
    # 城市名列表（用于写入提示信息）
    city_name_list = []
    for line in city_msg:
        city = line.strip()
        # 城市编号
        city_num_list.append(city[-4:-1])
        # 城市名
        city_name_list.append(city[:-5])
    # 城市数量
    city_count = len(city_num_list)
    city_msg.close()

    # ip代理池
    proxy_ip_pool = []
    ip_msg = open(r"../resource/available_ip.txt", encoding="utf-8")
    for line in ip_msg:
        address = line.strip()
        proxy_ip_pool.append(address)
    ip_msg.close()

    """
    在指定出发日期内访问，遍历所有城市，两两之间的航班信息
    """

    # 随机从代理池中选取一个代理ip，并测试是否可用
    ip_and_port = test_proxy_ip(proxy_ip_pool)

    for date in dates:
        # 在该日期下，双遍历（两城市之间的航班信息）
        for i in range(city_count):
            # 下标，从i+1开始
            for j in range(i + 1, city_count):
                # 写入两城市间名字
                save_msg.write("{0} 到 {1}\n".format(city_name_list[i], city_name_list[j]))

                # 获取加密url参数
                rk, CK, r = get_parameter(city_num_list[i], city_num_list[j], ip_and_port, date, return_date)

                # 如果url参数解析不为空，进行航班信息查询
                if rk and CK and r:
                    # 进行航班信息加载及解析
                    results = get_flight_msg(city_num_list[i], city_num_list[j], date, return_date, ip_and_port, rk, CK,
                                             r)

                    # 如果有航班信息
                    if results:
                        print("============={0}================".format(date))
                        print(results)

                        # 将所有航班信息写入文本
                        for result in results:
                            save_msg.write("出发时间 {0} --> 到达时间 {1} ，票价：{2}\n".format(result['start_time'],
                                                                                    result['arrivals_time'],
                                                                                    result['price']))
                    elif results is None:
                        # 如果返回为空，则说明ip被封，则重新挑选ip代理
                        print("{0} 代理ip被封，切换ip".format(ip_and_port))
                        ip_and_port = test_proxy_ip(proxy_ip_pool)
                    elif len(results) == 0:
                        save_msg.write("暂无航班信息\n")
                    # 换行
                    save_msg.write("\n")
                elif rk is None and CK is None and r is None:
                    save_msg.write("国际航班\n")
                else:
                    # 如果返回为空，则说明ip被封，则重新挑选ip代理
                    print("{0} 代理ip被封，切换ip".format(ip_and_port))
                    ip_and_port = test_proxy_ip(proxy_ip_pool)
                save_msg.flush()
    save_msg.close()
