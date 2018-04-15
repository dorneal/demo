#!/usr/bin/python3
# coding:utf-8
# Filename:demo.py
# Author:黄鹏
# Time:2018.04.12 10:15
import http.cookiejar
import json
import random
import socket
import telnetlib
import urllib
from urllib import parse
import re
from bs4 import BeautifulSoup
import urllib.error
import urllib.request

"""
    使用自带的爬虫库urllib
    爬取携程指定起始位置、日期的机票信息
    缺点：抓包分析难，js脚本太多，加密的参数（携程自称OceanBall）
    优点：快速，准确，易分析，灵活性强

    携程反爬机制：url前端加密参数（需要具体分析OceanBall.js），短时间大访问量封ip（半个小时）。
    目前存在问题：
        速度太快，容易封ip
        国际航班暂未分析出来
        考虑到修改问题，代码暂未优化(耦合性太高,健壮性不够)
    本爬虫使用了“请求头填充、设置代理、cookie伪装、get数据填充”
    
    本程序的性能，取决于代理池的质量
"""


def get_flight_msg(dict_content):
    """
    根据构造出的url获取到航班数据
    :param dict_content: 响应的内容
    :return:  分析结果
    """
    # 转换为json
    dict_content = json.loads(dict_content)
    # 如果出现错误
    if dict_content['Error']:
        if dict_content['Error']['Code'] == 103:
            print(dict_content['Error']['Message'])
            return 0
        if dict_content['Error']['Code'] == 1004:
            print("IP被封！")
            return 1

    # 解析json
    # 直达航班信息
    direct_length = len(dict_content['fis']) if dict_content['fis'] else 0
    # 中转航班信息
    transfer_length = len(dict_content['tf']) if dict_content['tf'] else 0

    if direct_length == 0:
        if transfer_length == 0:
            print("暂时没有航班信息！")
        else:
            # 中转航班信息
            print("中转 共{0}种机票选择".format(transfer_length))

            # 数据装填
            result_list = []
            for index in range(transfer_length):
                result_dict = {
                    'transfer': 1,
                    "transfer_city": dict_content['tf'][index][u'Routes'][0][u'tcn'],
                    'start_time': dict_content['tf'][index][u'dt'],
                    'arrivals_time': dict_content['tf'][index][u'at'],
                    'price': dict_content['tf'][index][u'rtp']}

                result_list.append(result_dict)
            return result_list
    else:
        # 直达航班信息
        print("直达 共{0}种机票选择".format(direct_length))

        # 数据装填
        result_list = []
        for index in range(direct_length):
            result_dict = {
                'transfer': 0,
                'start_time': dict_content['fis'][index][u'dt'],
                'arrivals_time': dict_content['fis'][index][u'at'],
                'price': dict_content['fis'][index][u'rtp']}

            result_list.append(result_dict)
        return result_list


def get_parameter(this_city, other_city, proxy_address, date1, date2):
    """
    第一次打开连接，获取到url参数，第二次打开数据连接，获取到Json数据
    两次的头部不同，cookie的使用，头部referer的不同
    :param date1:出发日期，格式示例：2016-05-13
    :param date2:返程日期
    :param this_city: 出发城市  格式示例(城市编号)：AAT
    :param other_city: 目的城市
    :param proxy_address: 代理IP
    :return:响应内容
    """

    url_dict = {
        "dayoffset": 0,
        "ddate1": date1,
        "ddate2": date2
    }
    url_data = urllib.parse.urlencode(url_dict)

    # 构造出url，第一次请求该url为了获取url的重要参数
    url = "http://flights.ctrip.com/booking/%s-%s---D-adu-1/?%s" % (this_city, other_city, url_data)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age = 0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        'Host': "flights.ctrip.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "65.0.3325.181 Safari/537.36",
        'Referer': "http://flights.ctrip.com/"}
    # 代理
    proxies = {
        "http": "http://{0}".format(proxy_address)
    }
    proxy = urllib.request.ProxyHandler(proxies)
    opener1 = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener1)

    # 填充信息
    try:
        request = urllib.request.Request(url=url, headers=headers, method="GET")
        response = urllib.request.urlopen(request, timeout=30)
    except:
        print("在求参的时候失去响应 ,请求地址为 {0} ".format(url))
        return 0

    # 请求
    if response.status == 200:
        # bs4解析dom
        response_dom = response.read().decode("gbk")
        bs_obj = BeautifulSoup(response_dom, 'html.parser')
        # 进行查找该脚本段
        try:
            # 解析响应的脚本，获取url，破解出重要url参数(国际航班没有该脚本，解析会出现异常)
            pp = bs_obj.find_all('script', string=re.compile('var url'), type='text/javascript')[0].get_text().split()
        except IndexError:
            # TODO 需要分析国际航班
            print("国际航班暂未分析Js脚本如何是如何加密参数！")
            return 1
        # 响应出错，页面不可分析
        except TypeError:
            print("响应400!!!")
            return 4

        # 获取到参数
        ck_original = pp[3][-34:-2]
        ck = ck_original[0:5] + ck_original[13] + ck_original[5:13] + ck_original[14:]
        rk = pp[-1][18:24]
        num = random.random() * 10
        num_str = "%.15f" % num
        rk = num_str + rk
        r = pp[-1][27:len(pp[-1]) - 3]

        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            'Host': "flights.ctrip.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                          "65.0.3325.181 Safari/537.36",
            'Referer': "http://flights.ctrip.com/booking/%s-%s---D-adu-1/?dayoffset=0&ddate1=%s&ddate2=%s" % (
                this_city, other_city, date1, date2)}
        # 添加cookie
        cookie = http.cookiejar.CookieJar()
        cookie_process = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(cookie_process)
        urllib.request.install_opener(opener)

        # 构造url参数
        url_dict = {
            'DCity1': this_city,
            'ACity1': other_city,
            'SearchType': 'D',  # 搜索类型D为往返，S为单程
            'DDate1': date1,
            'ACity2': this_city,
            'DDate2': date2,
            'IsNearAirportRecommond': 0,
            'rk': rk,
            'CK': ck,
            'r': r
        }

        # 加工构造出的url参数
        url_data = urllib.parse.urlencode(url_dict)
        url = "http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?" + url_data

        try:
            request = urllib.request.Request(url=url, headers=headers, method="GET")
            response = urllib.request.urlopen(request, timeout=30)
        except:
            # TODO 待解决
            print("-_-||，失去响应，url地址为 {0} ".format(url))
            return 2
        # 返会响应的内容
        if response.status == 200:
            return response.read().decode("gbk")
        else:
            print("响应错误，响应码{0}".format(response.status))
            return 5
    else:
        print("响应失败！响应码{0}".format(response.status))
        return 3


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
        telnetlib.Telnet(ip, port=port, timeout=5)
    except:
        # 该ip不可用时，删除当前这个，继续选取
        ip_pool.remove(ip_port)
        print("代理 {0} 不可用,IP代理池深度为：{1}".format(ip_port, len(ip_pool)))
        test_proxy_ip(ip_pool)
    else:
        ip_pool.remove(ip_port)
        print("当前使用代理:{0} ,IP代理池深度为：{1}".format(ip_port, len(ip_pool)))
        return ip_port


if __name__ == '__main__':
    # 出发日期
    dates = ['2018-04-16']
    # 返程日期
    return_date = '2018-05-10'

    # 将航班信息保存到文本
    filename = r"../resource/results2.txt"
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
    ip_msg = open(r"../resource/ctrip_ip3.txt", encoding="utf-8")
    for line in ip_msg:
        address = line.strip()
        proxy_ip_pool.append(address)
    ip_msg.close()

    # 被封ip集
    ban_ip = open("../resource/ban_ip2.txt", "a+", encoding="utf-8")
    """
    在指定出发日期内访问，遍历所有城市，两两之间的航班信息
    """

    # 随机从代理池中选取一个代理ip，并测试是否可用
    ip_and_port = test_proxy_ip(proxy_ip_pool)

    # 在该日期下，双遍历（两城市之间的航班信息）
    for date in dates:
        tag = 0
        for i in range(city_count):
            while True:
                tag += 1
                if tag > city_count:
                    break
                # 避免城市相同
                if i != tag:
                    # 获取加密url参数
                    res = get_parameter(city_num_list[i], city_num_list[tag], ip_and_port, date, return_date)

                    if res == 0 or res == 1 or res == 2 or res == 3 or res == 4 or res == 5:
                        # 随机从代理池中选取一个代理ip，并测试是否可用
                        ip_and_port = test_proxy_ip(proxy_ip_pool)
                        # 重新从这个城市开始
                        tag -= 1
                        continue
                    else:
                        # 写入两城市间名字
                        save_msg.write("{0} 到 {1}\n".format(city_name_list[i], city_name_list[tag]))

                        # 进行航班信息加载及解析
                        results = get_flight_msg(res)
                        # 如果有航班信息
                        if isinstance(results, list):
                            print("====={1}======{0}====={2}=====".format(date, city_name_list[i], city_name_list[tag]))
                            print(results)
                            # 将所有航班信息写入文本
                            for result in results:
                                # 中转城市
                                if result['transfer'] == 1:
                                    save_msg.write("出发时间 {0} --中转 {3} --> 到达时间 {1} ，票价：{2}\n".format(
                                        result['start_time'], result['arrivals_time'],
                                        result['price'], result['transfer_city']))
                                elif result['transfer'] == 0:
                                    # 直达
                                    save_msg.write("出发时间 {0} --> 到达时间 {1} ，票价：{2}\n".format(
                                        result['start_time'], result['arrivals_time'], result['price']))
                        elif results == 1:
                            # 随机从代理池中选取一个代理ip，并测试是否可用
                            ban_ip.write("{0} IP被封！\n".format(ip_and_port))
                            ban_ip.flush()
                            ip_and_port = test_proxy_ip(proxy_ip_pool)
                        elif results == 0:
                            save_msg.write("暂无航班信息\n")
                        else:
                            print("出现未知错误！{0}".format(results))
                            tag -= 1
                        save_msg.write("\n")
                    save_msg.flush()
    save_msg.close()
    ban_ip.close()
