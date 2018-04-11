#!/usr/bin/python3
# coding:utf-8
# Filename:demo4.py
# Author:黄鹏
# Time:2018.04.10 11:59

import http.cookiejar
import json
import random
import telnetlib
import urllib
from urllib import parse
from urllib.request import Request

import time
from lxml import etree

"""
    爬取携程指定起始位置、日期的机票信息
    缺点：抓包分析难，js脚本太多，加密的参数（携程自称OceanBall）
    优点：快速，准确，易分析，灵活性强
    
    携程反爬机制：url前端加密参数（需要具体分析demo.js），短时间大访问量封ip（半个小时）。
    目前存在问题：
        速度太快，容易封ip
        国际航班暂未分析出来
        考虑到修改问题，代码暂未优化(耦合性太高,健壮性不够)
    本爬虫使用了“请求头填充、设置代理、cookie伪装、get数据填充”
"""


def filling_headers(url, this_city, other_city, start_date, arrivals_date, proxy_addr):
    """
    请求头的填充
    :param url: Url地址
    :param this_city:  出发地址
    :param other_city: 目的地
    :param start_date: 出发日期
    :param arrivals_date: 返回日期
    :param proxy_addr: 代理ip
    :return: 响应对象
    """
    headers = {
        'Host': "flights.ctrip.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "65.0.3325.181 Safari/537.36",
        'Referer': "http://flights.ctrip.com/booking/%s-%s---D-adu-1/?dayoffset=0&ddate1=%s&ddate2=%s" % (
            this_city, other_city, start_date, arrivals_date)}

    # 是否使用ip代理
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener1 = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener1)

    # 使用http.cookiejar.CookieJar()创建CookieJar对象
    cookie_jar = http.cookiejar.CookieJar()
    # 使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
    cookie = urllib.request.HTTPCookieProcessor(cookie_jar)
    opener2 = urllib.request.build_opener(cookie)
    # 将opener安装为全局
    urllib.request.install_opener(opener2)

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

    # 填充信息
    req = filling_headers(url, this_city, other_city, start_date, arrivals_date, proxy_addr)

    # 请求，响应结果
    res = urllib.request.urlopen(req)
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

    # 填充信息
    req = filling_headers(url, this_city, other_city, date1, date2, proxy_addr)

    # 请求
    response = urllib.request.urlopen(req)
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
    ip = ip_port.split(":")[0]
    port = ip_port.split(":")[1]
    try:
        telnetlib.Telnet(ip, port=port, timeout=10)
    except:
        print('代理ip：{0} 不可用！'.format(ip_port))
        # 该ip不可用时，继续选取
        return test_proxy_ip(ip_pool)
    else:
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

    for date in dates:
        # 在该日期下，双遍历（两城市之间的航班信息）
        for i in range(city_count):
            # 下标，从i+1开始
            for j in range(i + 1, city_count):
                # 随机从代理池中选取一个代理ip，并测试是否可用
                ip_and_port = test_proxy_ip(proxy_ip_pool)
                # 限制爬取速度，速度太快容易被封ip
                time.sleep(5)

                # 获取加密url参数
                rk, CK, r = get_parameter(city_num_list[i], city_num_list[j], ip_and_port, date, return_date)

                # 如果url参数解析不为空，进行航班信息查询
                if rk and CK and r:
                    time.sleep(2)
                    # 进行航班信息加载及解析
                    results = get_flight_msg(city_num_list[i], city_num_list[j], date, return_date, ip_and_port, rk, CK,
                                             r)

                    # 写入两城市间名字
                    save_msg.write("{0} 到 {1}\n".format(city_name_list[i], city_name_list[j]))

                    # 如果有航班信息
                    if results:
                        print(date + "时:")
                        print("====================================")
                        print(results)

                        # 将所有航班信息写入文本
                        for result in results:
                            save_msg.write("出发时间 {0} --> 到达时间 {1} ，票价：{2}\n".format(result['start_time'],
                                                                                    result['arrivals_time'],
                                                                                    result['price']))
                    else:
                        save_msg.write("暂无航班信息\n")

                    # 换行
                    save_msg.write("\n")
                    save_msg.flush()
    save_msg.close()
