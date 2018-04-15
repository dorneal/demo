#!/usr/bin/python3
# coding:utf-8
# Filename:selenium_spider.py
# Author:黄鹏
# Time:2018.04.10 12:19
import http.cookiejar
import json
import random
import telnetlib
import time
import re
import urllib
from urllib.request import urlopen
import urllib.parse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType, Proxy

"""
    未完善
    利用PhantomJs 模拟搜索，得到响应的页面内容，
    获取脚本段里面的url参数，构造一个新的url，
    再使用urllib进行连接，获取到json数据，然后进行解析提取
"""


def get_parameter(content):
    """
    根据页面内容，查找，并破解出url参数
    :param content: 页面内容
    :return: 3个url参数
    """
    # bs4解析dom
    bsObj = BeautifulSoup(content, 'html.parser')
    # 进行查找该脚本段
    scripts = bsObj.find_all('script', string=re.compile('var url'), type='text/javascript')
    # 国际航班没有该脚本段，暂未分析
    if not scripts:
        return "", "", ""
    # 解析脚本段，获取url，破解出重要url参数
    pp = str(scripts[0].get_text()).split()

    CK_original = pp[3][-34:-2]
    CK = CK_original[0:5] + CK_original[13] + CK_original[5:13] + CK_original[14:]
    rk = pp[-1][18:24]
    num = random.random() * 10
    num_str = "%.15f" % num
    rk = num_str + rk
    r = pp[-1][27:len(pp[-1]) - 3]

    # 返回重要url参数
    return r, rk, CK


def create_browser(url, ip_port):
    """
    打开一个连接
    :param url: 连接地址
    :param ip_port: 代理地址
    :return: 返回一个打开连接的driver
    """
    proxy = Proxy(
        {
            'proxyType': ProxyType.MANUAL,
            'httpProxy': "107.172.10.24:1080"  # 代理ip和端口
        }
    )
    # 新建一个“期望的技能”
    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    # 把代理ip加入到技能中
    proxy.add_to_capabilities(desired_capabilities)
    browser = webdriver.PhantomJS(
        desired_capabilities=desired_capabilities
    )
    # 设置超时时间
    browser.set_page_load_timeout(30)
    try:
        browser.get(url)
    except TimeoutException:
        # 超过设定时间，停止加载
        browser.execute_script('window.stop()')
    # 返回打开连接的driver
    return browser


def filling_search(driver, start_city, arrivals_city, start_date, return_date):
    """
    模拟输入城市，日期信息，点击搜索按钮
    :param driver:  driver对象
    :param start_city:  出发地
    :param arrivals_city: 目的地
    :param start_date: 出发日期
    :param return_date: 返回日期
    :return: 页面响应内容
    """
    # 获取城市输入，日期输入框
    print(driver.page_source)
    start_city_input = driver.find_element_by_xpath("//*[@id='DCityName1']")
    arrivals_city_input = driver.find_element_by_xpath("//*[@id='ACityName1']")
    start_date_input = driver.find_element_by_xpath("//*[@id='DDate1']")
    return_date_input = driver.find_element_by_xpath("//*[@id='ReturnDate1']")

    # 将输入框清空
    start_city_input.clear()
    arrivals_city_input.clear()
    start_date_input.clear()
    return_date_input.clear()

    # 填写输入框信息
    start_city_input.send_keys(start_city)
    arrivals_city_input.send_keys(arrivals_city)
    start_date_input.send_keys(start_date)
    return_date_input.send_keys(return_date)

    # 等待一秒，提交
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='btnReSearch']").click()
    # 返回页面内容
    return driver.page_source


def get_city(city_file):
    """
    从解析好的城市文本中读取城市信息，返回该列表
    :param city_file:  城市信息文本
    :return:  城市编号列表，城市名列表
    """
    # 从文本中读取城市信息
    city_msg = open(city_file, encoding="utf-8")
    # 城市后缀编号列表（用于传递参数）
    city_num_list = []
    # 城市名列表（用于写入提示信息）
    city_name_list = []
    for line in city_msg:
        city = line.strip()
        # 城市编号
        city_num_list.append(city[-4:-1])
        # 城市名
        city_name_list.append(city)
    return city_num_list, city_name_list


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


def get_ip_pool(pool_file):
    """
    创建一个ip代理池
    :param pool_file: ip文本
    :return: ip列表
    """
    # ip代理池
    proxy_ip_pool = []
    ip_msg = open(pool_file, encoding="utf-8")
    for line in ip_msg:
        address = line.strip()
        proxy_ip_pool.append(address)
    ip_msg.close()
    return proxy_ip_pool


def get_proxy_ip(ip_pool):
    """
    从代理池中选出一个可用的代理地址
    :param ip_pool: 代理池
    :return: ip and port，一个给urllib做代理请求头，一个给selenium做代理请求头
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
        return get_proxy_ip(ip_pool)
    else:
        return ip_port


def get_flight_msg(this_city, other_city, start_date, arrivals_date, rk, CK, r, proxy_addr):
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


if __name__ == '__main__':
    # 初始连接
    start_url = "http://flights.ctrip.com/booking/WUH-SZX---D-adu-1/?ddate1=2018-04-30&ddate2=2018-05-11"
    cities = r"C:\Users\Administrator\Desktop\workspace\day0410\cities.txt"
    # 城市信息
    cities_num_list, cities_name_list = get_city(cities)
    length = len(cities_num_list)
    # 出发往返日期
    start_date = ['2018-04-16']
    return_date = '2018-05-03'
    # 打开初始连接（以后的url在此基础上搜索）
    # 第一步，获取代理ip
    pool_file_path = r"../resource/available_ip.txt"
    proxy_pool = get_ip_pool(pool_file_path)
    proxy_ip = get_proxy_ip(proxy_pool)

    # 保存位置
    # 将航班信息保存到文本
    filename = r"C:\Users\Administrator\Desktop\workspace\day0410\test8.txt"
    save_msg = open(filename, "a+", encoding="utf-8")
    # 第一步,打开初始连接
    driver = create_browser(start_url, proxy_ip)
    for date in start_date:
        for i in range(length):
            for j in range(i + 1, length):

                # 第二步，进行搜索（新页面），返回响应内容
                page_content = filling_search(driver, cities_name_list[i], cities_name_list[j], date,
                                              return_date)

                time.sleep(3)

                # 第三步，分析响应内容，获取url参数
                r, rk, CK = get_parameter(page_content)
                # print(r, rk, CK)

                # 如果url参数解析不为空，进行航班信息查询
                if rk and CK and r:

                    time.sleep(2)
                    # 第四步，根据url参数构造新url,填充数据，进行连接
                    results = get_flight_msg(cities_num_list[i], cities_num_list[j], date, return_date, r, rk,
                                             CK, proxy_ip)

                    # 写入两城市间名字
                    save_msg.write("{0} 到 {1}\n".format(cities_name_list[i], cities_name_list[j]))

                    # 如果有航班信息
                    if results:
                        print("================{0}====================".format(date))
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
