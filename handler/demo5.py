#!/usr/bin/python3
# coding:utf-8
# Filename:demo5.py
# Author:黄鹏
# Time:2018.04.10 12:19
import random
import time

import re
from lxml import etree

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

"""
    使用selenium 爬取携程航班信息
    缺点：速度慢，解析需要等待js渲染，难分析提取想要的数据
    优点：不需要抓包信息，简单
"""

driver = webdriver.PhantomJS()
url = "http://flights.ctrip.com/booking/WUH-SZX---D-adu-1/?ddate1=2018-04-30&ddate2=2018-05-11"

# 设置超时时间
driver.set_page_load_timeout(30)
try:
    driver.get(url)
except TimeoutException:
    # 超过设定时间，停止加载
    driver.execute_script('window.stop()')

# 获取城市输入，日期输入框
start_city_input = driver.find_element_by_xpath("//*[@id='DCityName1']")
arrivals_city_input = driver.find_element_by_xpath("//*[@id='ACityName1']")
start_date_input = driver.find_element_by_xpath("//*[@id='DDate1']")
return_date_input = driver.find_element_by_xpath("//*[@id='ReturnDate1']")

# 从文本中读取城市信息
f2 = open(r"C:\Users\Administrator\Desktop\workspace\day0410\cities.txt", encoding="utf-8")
city_list = []
while True:
    city = f2.readline().strip()
    if not city:
        break
    city_list.append(city)

# 将输入框清空
start_city_input.clear()
arrivals_city_input.clear()
start_date_input.clear()
return_date_input.clear()

# 填写输入框信息
start_city_input.send_keys(city_list[0])
arrivals_city_input.send_keys(city_list[1])
start_date_input.send_keys("2018-04-12")
return_date_input.send_keys("2018-05-11")

# 等待一秒，提交
time.sleep(1)
driver.find_element_by_xpath("//*[@id='btnReSearch']").click()

# 等待三秒，获取所有搜索信息
time.sleep(3)
div_list = driver.find_elements_by_xpath("//*[@id='J_flightlist2']/div")

bsObj = BeautifulSoup(driver.page_source, 'html.parser')
script = bsObj.find_all('script', string=re.compile('var url'), type='text/javascript')[0]

# 解析响应的脚本，获取url，破解出重要url参数
pp = script.split()

CK_original = pp[3][-34:-2]
CK = CK_original[0:5] + CK_original[13] + CK_original[5:13] + CK_original[14:]
rk = pp[-1][18:24]
num = random.random() * 10
num_str = "%.15f" % num
rk = num_str + rk
r = pp[-1][27:len(pp[-1]) - 3]
print(r, rk, CK)

"""
获取脚本段里面的url，再使用request进行连接，获取到数据，然后进行解析
"""
